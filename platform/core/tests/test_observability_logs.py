"""JSON log lines and the log-body rule (ASR02-OBS): a static event name,
allowlisted fields and trace ids, with no interpolated value."""

import json
import logging
import sys

from mulyankan_platform.observability.guard import UNSTRUCTURED_EVENT, event_name
from mulyankan_platform.observability.logs import JsonFormatter, configure_logging
from opentelemetry.instrumentation.logging.handler import LoggingHandler
from opentelemetry import trace

SENTINEL = "SENTINEL-9a2e"


def _line(record_kwargs, msg="draft.submitted", args=(), name="demo") -> dict:
    record = logging.LogRecord(
        name=name,
        level=logging.INFO,
        pathname="x.py",
        lineno=1,
        msg=msg,
        args=args,
        exc_info=None,
    )
    for key, value in record_kwargs.items():
        setattr(record, key, value)
    return json.loads(JsonFormatter().format(record))


def test_json_line_carries_event_and_allowlisted_fields_only() -> None:
    line = _line({"mulyankan.object_ref": "art-1", "stem": SENTINEL})
    assert line["event"] == "draft.submitted"
    assert line["level"] == "INFO"
    assert line["mulyankan.object_ref"] == "art-1"
    assert "stem" not in line
    assert SENTINEL not in json.dumps(line)


def test_json_line_carries_trace_ids_inside_a_span(telemetry) -> None:
    tracer = trace.get_tracer("test")
    with tracer.start_as_current_span("s") as span:
        line = _line({})
        ctx = span.get_span_context()
    assert line["trace_id"] == format(ctx.trace_id, "032x")
    assert line["span_id"] == format(ctx.span_id, "016x")


def test_json_line_reports_exception_type_and_stack_without_message() -> None:
    try:
        raise ValueError(SENTINEL)
    except ValueError:
        record = logging.LogRecord(
            "demo", logging.ERROR, "x.py", 1, "op.failed", (), sys.exc_info()
        )
    line = json.loads(JsonFormatter().format(record))
    assert line["exception.type"] == "ValueError"
    assert "test_observability_logs.py" in line["exception.stacktrace"]
    assert SENTINEL not in json.dumps(line)


def test_asr02obs_body_must_be_an_event_name() -> None:
    assert event_name("draft.submitted", "demo") == "draft.submitted"
    assert (
        event_name("platform.config.missing", "mulyankan_platform.core_api.main")
        == "platform.config.missing"
    )
    # Interpolated or free-text messages are replaced before export.
    assert event_name(f"config {SENTINEL} missing", "demo") == UNSTRUCTURED_EVENT
    assert event_name("Draft submitted", "demo") == UNSTRUCTURED_EVENT
    assert event_name("", "demo") == UNSTRUCTURED_EVENT
    # Framework loggers log constants and pass through.
    assert (
        event_name("Application startup complete.", "uvicorn.error")
        == "Application startup complete."
    )


def test_json_line_replaces_an_interpolated_message_and_drops_args() -> None:
    line = _line({}, msg=f"config {SENTINEL} missing")
    assert line["event"] == UNSTRUCTURED_EVENT
    assert SENTINEL not in json.dumps(line)
    line = _line({}, msg="config %s missing", args=(SENTINEL,))
    assert line["event"] == UNSTRUCTURED_EVENT
    assert SENTINEL not in json.dumps(line)


def test_configure_logging_is_idempotent(telemetry) -> None:
    from mulyankan_platform.observability.setup import register_providers

    root = logging.getLogger()
    before = list(root.handlers)
    configure_logging(register_providers().logger_provider)
    configure_logging(register_providers().logger_provider)
    assert root.handlers == before
    assert sum(isinstance(h, LoggingHandler) for h in root.handlers) == 1
    assert sum(isinstance(h.formatter, JsonFormatter) for h in root.handlers) == 1
    assert logging.getLogger("uvicorn.access").disabled
    # uvicorn's loggers reach the root handlers instead of their own plain ones
    assert logging.getLogger("uvicorn.error").propagate
    assert not logging.getLogger("uvicorn.error").handlers


def test_a_stray_format_argument_neither_raises_nor_exports(telemetry, capsys) -> None:
    """`logger.info("event", value)` is the slip the convention invites: the
    OTel handler renders the message too, so both handlers must see a
    sanitised record instead of raising TypeError into the caller."""
    logging.getLogger("slip").info("draft.submitted", SENTINEL)
    (record,) = [r for r in telemetry.logs() if r.body == UNSTRUCTURED_EVENT]
    assert SENTINEL not in json.dumps(dict(record.attributes or {}))
    out = capsys.readouterr().out
    assert '"event": "log.unstructured"' in out
    assert SENTINEL not in out
