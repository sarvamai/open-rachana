"""Test fixtures: a fake provider module the registry can load.

The registry resolves "module:attr" targets via importlib. To test that
without the reference provider (a separate PR), this conftest registers a
minimal kms double as a real importable module for the duration of the test
session.
"""

import json
import sys
import types

import pytest
from mulyankan_platform.observability import register_providers
from mulyankan_spi.descriptor import ProviderDescriptor
from opentelemetry.sdk._logs.export import InMemoryLogRecordExporter
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

FAKE_MODULE_NAME = "testkit_fake_provider"


class FakeKms:
    """Minimal kms double satisfying the KmsProvider Protocol."""

    def __init__(self, config: dict) -> None:
        self.config = config

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name="fake-kms",
            version="1.0.0",
            deterministic=True,
            data_handling="in-memory test double; no retention, no network",
        )

    def encrypt(self, key_id: str, plaintext: bytes) -> bytes:
        return b"FAKE:" + plaintext

    def decrypt(self, key_id: str, ciphertext: bytes) -> bytes:
        return ciphertext[len(b"FAKE:") :]

    def sign(self, key_id: str, data: bytes) -> bytes:
        return b"FAKE-SIG"

    def verify_signature(self, key_id: str, data: bytes, signature: bytes) -> bool:
        return signature == b"FAKE-SIG"


def _register() -> None:
    module = types.ModuleType(FAKE_MODULE_NAME)
    module.FakeKms = FakeKms
    sys.modules[FAKE_MODULE_NAME] = module


_register()


# --- In-memory telemetry (ASR02-OBS) -------------------------------------
#
# The OTel global providers can be installed once per process, and
# `configure` (called from `build_app`) installs them on first use.
# The first app any test builds installs them, so the in-memory providers
# must exist before that: they are created here at conftest import time,
# not in a fixture. Tests that need a fresh
# process (SDK disabled, Collector unreachable) run a subprocess instead.


class Telemetry:
    """Everything exported during a test, in memory."""

    def __init__(self) -> None:
        self.span_exporter = InMemorySpanExporter()
        self.metric_reader = InMemoryMetricReader()
        self.log_exporter = InMemoryLogRecordExporter()
        register_providers(
            span_exporter=self.span_exporter,
            metric_reader=self.metric_reader,
            log_exporter=self.log_exporter,
        )

    def reset(self) -> None:
        self.span_exporter.clear()
        self.log_exporter.clear()

    def spans(self):
        return list(self.span_exporter.get_finished_spans())

    def logs(self):
        return [d.log_record for d in self.log_exporter.get_finished_logs()]

    def dump(self) -> str:
        """Serialise every exported span, log and metric point for assertions."""
        out = {"spans": [], "logs": [], "metrics": []}
        for span in self.spans():
            out["spans"].append(
                {
                    "name": span.name,
                    "attributes": dict(span.attributes or {}),
                    "events": [
                        {"name": e.name, "attributes": dict(e.attributes or {})}
                        for e in span.events
                    ],
                    "resource": dict(span.resource.attributes),
                }
            )
        for record in self.logs():
            out["logs"].append(
                {"body": record.body, "attributes": dict(record.attributes or {})}
            )
        data = self.metric_reader.get_metrics_data()
        for rm in data.resource_metrics:
            for sm in rm.scope_metrics:
                for metric in sm.metrics:
                    for point in metric.data.data_points:
                        out["metrics"].append(
                            {"name": metric.name, "attributes": dict(point.attributes)}
                        )
        return json.dumps(out, default=str, ensure_ascii=False)


_TELEMETRY = Telemetry()  # before any test module imports core_api.main


@pytest.fixture
def telemetry() -> Telemetry:
    _TELEMETRY.reset()
    return _TELEMETRY
