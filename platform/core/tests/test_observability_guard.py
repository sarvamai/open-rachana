"""Attribute allowlist guard (ASR02-OBS): unknown keys never reach an exporter."""

from mulyankan_platform.observability.guard import (
    UNSTRUCTURED_EVENT,
    ALLOWED_METRIC_ATTRIBUTES,
    DROPPED_LABEL_LIMIT,
    ALLOWED_SPAN_ATTRIBUTES,
    LogAttributeGuard,
    SpanAttributeGuard,
    frames_only,
    metric_views,
)
from opentelemetry._logs import LogRecord, SeverityNumber
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    InMemoryLogRecordExporter,
    SimpleLogRecordProcessor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace import SpanLimits, TracerProvider
from opentelemetry.trace import StatusCode
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

SENTINEL = "SENTINEL-4f1c"


def _counter():
    reader = InMemoryMetricReader()
    meter = MeterProvider(metric_readers=[reader]).get_meter("test")
    return reader, meter.create_counter("mulyankan.observability.attributes_dropped")


def _dropped_keys(reader) -> set[str]:
    data = reader.get_metrics_data()
    keys = set()
    for rm in data.resource_metrics:
        for sm in rm.scope_metrics:
            for metric in sm.metrics:
                for point in metric.data.data_points:
                    keys.add(point.attributes["attribute"])
    return keys


def test_asr02obs_unknown_span_attributes_are_dropped_and_counted() -> None:
    reader, counter = _counter()
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SpanAttributeGuard(counter))
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test")

    with tracer.start_as_current_span("s") as span:
        span.set_attribute("http.route", "/items/{item_id}")
        span.set_attribute("url.query", f"q={SENTINEL}")
        try:
            raise ValueError(SENTINEL)
        except ValueError as exc:
            span.record_exception(exc)

    (exported,) = exporter.get_finished_spans()
    assert dict(exported.attributes) == {"http.route": "/items/{item_id}"}
    (event,) = exported.events
    assert set(event.attributes) == {"exception.type", "exception.stacktrace"}
    # record_exception renders `ValueError: <message>` into the stacktrace;
    # the guard keeps the frames and removes that line.
    assert "test_observability_guard.py" in event.attributes["exception.stacktrace"]
    assert SENTINEL not in str(dict(event.attributes))
    assert {"url.query", "exception.message", "exception.escaped"} <= _dropped_keys(
        reader
    )


def test_asr02obs_stacktrace_keeps_frames_and_drops_the_message() -> None:
    rendered = (
        "Traceback (most recent call last):\n"
        '  File "/app/x.py", line 10, in outer\n'
        "    inner()\n"
        '  File "/app/x.py", line 4, in inner\n'
        "    raise ValueError(msg)\n"
        f"ValueError: {SENTINEL}\n"
        f"  second line of the message {SENTINEL}\n"
        f"Note: {SENTINEL}\n"
    )
    kept = frames_only(rendered)
    assert SENTINEL not in kept
    assert kept.splitlines() == [
        '  File "/app/x.py", line 10, in outer',
        "    inner()",
        '  File "/app/x.py", line 4, in inner',
        "    raise ValueError(msg)",
    ]
    assert frames_only("") == ""


def test_asr02obs_unknown_log_attributes_are_dropped_and_counted() -> None:
    reader, counter = _counter()
    exporter = InMemoryLogRecordExporter()
    provider = LoggerProvider()
    provider.add_log_record_processor(LogAttributeGuard(counter))
    provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))

    # Through the logs API: the stdlib handler that maps `extra` to attributes
    # arrives with the structured-logs task, and the guard sits below it.
    provider.get_logger("guard-test").emit(
        LogRecord(
            body="draft.submitted",
            severity_number=SeverityNumber.INFO,
            attributes={"mulyankan.object_ref": "art-1", "stem": SENTINEL},
        )
    )

    (record,) = exporter.get_finished_logs()
    attributes = dict(record.log_record.attributes)
    assert attributes["mulyankan.object_ref"] == "art-1"
    assert "stem" not in attributes
    assert SENTINEL not in str(attributes)
    assert "stem" in _dropped_keys(reader)


def test_asr02obs_unknown_metric_attributes_are_dropped() -> None:
    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader], views=metric_views())
    counter = provider.get_meter("test").create_counter("mulyankan.audit.events")

    counter.add(1, {"action": "probe", "stem": SENTINEL})

    (rm,) = reader.get_metrics_data().resource_metrics
    (point,) = [
        p for sm in rm.scope_metrics for m in sm.metrics for p in m.data.data_points
    ]
    assert dict(point.attributes) == {"action": "probe"}


def test_allowlist_never_admits_the_known_leaky_keys() -> None:
    for key in (
        "url.full",
        "url.path",
        "url.query",
        "user_agent.original",
        "exception.message",
        "enduser.id",
        "db.query.text",
    ):
        assert key not in ALLOWED_SPAN_ATTRIBUTES
        assert key not in ALLOWED_METRIC_ATTRIBUTES
    # Metric labels are bounded sets; a View filters by key only, so the
    # stacktrace value and the high-cardinality identifiers stay off metrics.
    for key in (
        "exception.stacktrace",
        "client.address",
        "server.address",  # the Host header
        "enduser.pseudo.id",
        "mulyankan.object_ref",
    ):
        assert key not in ALLOWED_METRIC_ATTRIBUTES


def test_asr02obs_span_status_description_is_dropped() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SpanAttributeGuard())
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test")

    try:
        with tracer.start_as_current_span("provider.call"):
            raise RuntimeError(f"provider rejected: {SENTINEL}")
    except RuntimeError:
        pass

    (exported,) = exporter.get_finished_spans()
    assert exported.status.status_code is StatusCode.ERROR
    assert not exported.status.description  # the SDK writes the message here
    assert SENTINEL not in exported.to_json()


def test_asr02obs_frames_only_ignores_file_shaped_lines_inside_the_message() -> None:
    rendered = (
        "Traceback (most recent call last):\n"
        '  File "/app/x.py", line 4, in inner\n'
        "    raise ValueError(msg)\n"
        "ValueError: first line\n"
        '  File "smuggled", line 1, in x\n'
        f"    {SENTINEL} content\n"
    )
    assert SENTINEL not in frames_only(rendered)
    assert frames_only(rendered).splitlines() == [
        '  File "/app/x.py", line 4, in inner',
        "    raise ValueError(msg)",
    ]


def test_asr02obs_dropped_key_label_is_bounded() -> None:
    reader, counter = _counter()
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SpanAttributeGuard(counter))
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test")

    with tracer.start_as_current_span("s") as span:
        span.set_attribute(f"http.request.header.x_stem_{SENTINEL}", "1")
        for n in range(DROPPED_LABEL_LIMIT + 5):
            span.set_attribute(f"custom.key.{n}", "v")

    labels = _dropped_keys(reader)
    assert SENTINEL not in " ".join(labels)
    assert "http.request.header.*" in labels
    assert "other" in labels
    assert len(labels) <= DROPPED_LABEL_LIMIT + 2  # the prefix bucket and "other"


def test_asr02obs_guard_preserves_sdk_limit_drop_counts() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider(span_limits=SpanLimits(max_attributes=3, max_events=1))
    provider.add_span_processor(SpanAttributeGuard())
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test")

    with tracer.start_as_current_span("s") as span:
        for key in (
            "http.route",
            "url.scheme",
            "server.port",
            "error.type",
            "mulyankan.spi",
        ):
            span.set_attribute(key, "x")
        span.add_event("one")
        span.add_event("two")

    (exported,) = exporter.get_finished_spans()
    assert exported.dropped_attributes == 2
    assert exported.dropped_events == 1


def test_asr02obs_log_guard_replaces_a_free_text_body() -> None:
    reader, counter = _counter()
    exporter = InMemoryLogRecordExporter()
    provider = LoggerProvider()
    provider.add_log_record_processor(LogAttributeGuard(counter))
    provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))

    provider.get_logger("demo").emit(
        LogRecord(
            body=f"config {SENTINEL} missing", severity_number=SeverityNumber.WARN
        )
    )
    provider.get_logger("uvicorn.error").emit(
        LogRecord(
            body="Application startup complete.", severity_number=SeverityNumber.INFO
        )
    )

    bodies = [r.log_record.body for r in exporter.get_finished_logs()]
    assert bodies == [UNSTRUCTURED_EVENT, "Application startup complete."]
    assert SENTINEL not in " ".join(bodies)
    assert "body" in _dropped_keys(reader)
