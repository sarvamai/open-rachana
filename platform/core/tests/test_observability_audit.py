"""Audit chain emits metrics and links the span to the event id (ASR02-OBS)."""

from mulyankan_platform.audit import AuditLog
from opentelemetry import trace


def _metric_points(telemetry, name):
    data = telemetry.metric_reader.get_metrics_data()
    for rm in data.resource_metrics:
        for sm in rm.scope_metrics:
            for metric in sm.metrics:
                if metric.name == name:
                    return list(metric.data.data_points)
    return []


def test_asr02obs_audit_append_records_metrics_and_span_link(telemetry) -> None:
    tracer = trace.get_tracer("test")
    log = AuditLog()
    with tracer.start_as_current_span("request"):
        event = log.append(
            actor="author-001",
            action="draft.created",
            object_refs=("artefact-a1",),
            payload={"stem": "x"},
        )

    (span,) = telemetry.spans()
    (audit_event,) = [e for e in span.events if e.name == "audit.appended"]
    assert audit_event.attributes["mulyankan.audit.event_id"] == event.event_id
    assert log.verify().ok  # nothing telemetry-related touched the chain

    # The reader is cumulative for the whole session, so assert on this
    # action's point and on lower bounds rather than exact totals.
    (count,) = [
        p
        for p in _metric_points(telemetry, "mulyankan.audit.events")
        if p.attributes == {"action": "draft.created"}
    ]
    assert count.value >= 1
    (duration,) = _metric_points(telemetry, "mulyankan.audit.append.duration")
    assert duration.count >= 1


def test_registry_bindings_gauge_reports_each_binding(telemetry) -> None:
    from mulyankan_platform.observability.metrics import observe_registry_bindings
    from mulyankan_platform.registry import ProviderRegistry

    mapping = {
        "providers": {
            "kms": {"provider": "testkit_fake_provider:FakeKms", "config": {}}
        }
    }
    registry = ProviderRegistry.from_mapping(mapping)  # held weakly by the gauge
    observe_registry_bindings(registry)
    points = _metric_points(telemetry, "mulyankan.registry.bindings")
    assert {
        "spi": "kms",
        "provider.name": "fake-kms",
        "provider.version": "1.0.0",
    } in [dict(p.attributes) for p in points]
