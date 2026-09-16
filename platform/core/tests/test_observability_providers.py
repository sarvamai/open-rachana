"""Every provider call is a content-free span (ASR02-OBS, ADR-0003 rule 2)."""

import asyncio
import sys
import types

import pytest
from mulyankan_platform.observability.metrics import observe_registry_bindings
from mulyankan_platform.registry import ProviderRegistry
from mulyankan_spi.descriptor import ProviderDescriptor
from mulyankan_spi.kms import KmsProvider

SENTINEL = b"SENTINEL-c3d1"
MAPPING = {
    "providers": {"kms": {"provider": "testkit_fake_provider:FakeKms", "config": {}}}
}


def test_asr02obs_provider_calls_are_spanned_content_free(telemetry) -> None:
    kms = ProviderRegistry.from_mapping(MAPPING).get("kms")
    assert isinstance(kms, KmsProvider)

    ciphertext = kms.encrypt("dev-key-1", SENTINEL)
    assert kms.decrypt("dev-key-1", ciphertext) == SENTINEL

    names = [s.name for s in telemetry.spans()]
    assert names == ["kms.encrypt", "kms.decrypt"]
    for span in telemetry.spans():
        assert dict(span.attributes) == {
            "mulyankan.spi": "kms",
            "mulyankan.provider.name": "fake-kms",
            "mulyankan.provider.version": "1.0.0",
        }
    assert SENTINEL.decode() not in telemetry.dump()


def test_provider_exceptions_propagate_and_are_recorded_without_message(
    telemetry,
) -> None:
    kms = ProviderRegistry.from_mapping(MAPPING).get("kms")
    with pytest.raises(TypeError):
        kms.encrypt("dev-key-1", None)  # FakeKms concatenates bytes; None raises
    (span,) = telemetry.spans()
    (event,) = [e for e in span.events if e.name == "exception"]
    assert "exception.message" not in event.attributes
    assert not span.status.description


class _Probe:
    """A provider with the shapes a real one has and FakeKms does not."""

    describe_calls = 0

    class Error(Exception):
        pass

    def __init__(self, config: dict) -> None:
        self.config = config

    @property
    def client(self):  # a lazy connection: touching it is a side effect
        raise RuntimeError("property evaluated")

    def describe(self) -> ProviderDescriptor:
        type(self).describe_calls += 1
        return ProviderDescriptor(
            name="probe", version="2.0", deterministic=True, data_handling="test"
        )

    def sync_call(self, x):
        return x

    async def async_call(self, x):
        await asyncio.sleep(0.01)
        raise self.Error(x)


class _NoDescribe:
    def __init__(self, config: dict) -> None:
        pass

    def call(self):
        return 1


def _register_probe_module():
    module = types.ModuleType("probe_provider")
    module.Probe = _Probe
    module.NoDescribe = _NoDescribe
    sys.modules["probe_provider"] = module


def test_observed_provider_forwards_attributes_and_wraps_once(telemetry) -> None:
    _register_probe_module()
    registry = ProviderRegistry.from_mapping(
        {
            "providers": {
                "probe": {"provider": "probe_provider:Probe", "config": {"k": 1}}
            }
        }
    )
    before = _Probe.describe_calls
    first, second = registry.get("probe"), registry.get("probe")
    assert first is second  # wrapped once per binding
    assert _Probe.describe_calls == before  # the descriptor was resolved at bind time
    assert first.config == {"k": 1}  # plain attributes forward
    assert first.Error is _Probe.Error  # a nested class is still a class
    with pytest.raises(RuntimeError, match="property evaluated"):
        first.client  # a property is evaluated only when read
    assert [s.name for s in telemetry.spans()] == []  # and none of that made a span


def test_observed_provider_spans_cover_an_async_method(telemetry) -> None:
    _register_probe_module()
    registry = ProviderRegistry.from_mapping(
        {"providers": {"probe": {"provider": "probe_provider:Probe", "config": {}}}}
    )
    probe = registry.get("probe")
    with pytest.raises(_Probe.Error):
        asyncio.run(probe.async_call(SENTINEL))
    (span,) = [s for s in telemetry.spans() if s.name == "probe.async_call"]
    assert (
        span.end_time - span.start_time >= 10_000_000
    )  # the await ran inside the span
    assert any(e.name == "exception" for e in span.events)
    assert SENTINEL.decode() not in telemetry.dump()


def test_span_and_gauge_agree_on_the_provider_name(telemetry) -> None:
    _register_probe_module()
    registry = ProviderRegistry.from_mapping(
        {"providers": {"nd": {"provider": "probe_provider:NoDescribe", "config": {}}}}
    )
    observe_registry_bindings(registry)
    registry.get("nd").call()
    (span,) = [s for s in telemetry.spans() if s.name == "nd.call"]
    points = [
        dict(p.attributes)
        for rm in telemetry.metric_reader.get_metrics_data().resource_metrics
        for sm in rm.scope_metrics
        for m in sm.metrics
        if m.name == "mulyankan.registry.bindings"
        for p in m.data.data_points
        if p.attributes.get("spi") == "nd"
    ]
    assert (
        points
        and points[0]["provider.name"] == span.attributes["mulyankan.provider.name"]
    )
