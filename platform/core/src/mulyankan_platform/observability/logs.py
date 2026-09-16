"""Structured logging on the standard library (D19, spec §4.4).

Calling convention: the message is a static, dotted event name and every
value goes in `extra` under an allowlisted key:

    logger.info("draft.submitted", extra={"mulyankan.object_ref": ref})

Two handlers on the root logger: JSON to stdout for file-based collection,
and the OTel handler to OTLP. A filter on both rewrites the record once so
that the body rule (`guard.event_name`) holds on each path and a stray
format argument can neither raise nor leak; the OTel path is guarded again
by `LogAttributeGuard`.
"""

from __future__ import annotations

import json
import logging
import sys
import traceback
from datetime import UTC, datetime
from typing import Any

from opentelemetry import trace
from opentelemetry.instrumentation.logging.handler import LoggingHandler
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.trace import format_span_id, format_trace_id

from mulyankan_platform.observability.guard import (
    ALLOWED_LOG_ATTRIBUTES,
    UNSTRUCTURED_EVENT,
    event_name,
)


class EventNameFilter(logging.Filter):
    """Rewrite the record's message to the exported body, once, before any
    handler renders it. `record.getMessage()` is what the OTel handler
    exports and it raises on a `%` mismatch, so the arguments are consumed
    here and the message becomes the event name or the placeholder."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            rendered = record.getMessage()
        except (TypeError, ValueError):  # an event name given %-args
            rendered = None
        record.msg = (
            UNSTRUCTURED_EVENT
            if rendered is None
            else event_name(rendered, record.name)
        )
        record.args = ()
        return True


class JsonFormatter(logging.Formatter):
    """One JSON object per line, with no message value and no traceback
    message line."""

    def format(self, record: logging.LogRecord) -> str:
        line: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, UTC)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "event": event_name(record.getMessage(), record.name),
        }
        ctx = trace.get_current_span().get_span_context()
        if ctx.is_valid:
            line["trace_id"] = format_trace_id(ctx.trace_id)
            line["span_id"] = format_span_id(ctx.span_id)
        for key, value in record.__dict__.items():
            if key in ALLOWED_LOG_ATTRIBUTES:
                line[key] = value
        if record.exc_info and record.exc_info[0] is not None:
            line["exception.type"] = record.exc_info[0].__name__
            # format_tb renders frames only; the exception message is not part of it.
            line["exception.stacktrace"] = "".join(
                traceback.format_tb(record.exc_info[2])
            )
        return json.dumps(line, ensure_ascii=False, default=str)


class _StdoutHandler(logging.StreamHandler):
    """Resolves sys.stdout at emit time so test capture and redirection work."""

    def __init__(self) -> None:
        super().__init__(sys.stdout)

    @property
    def stream(self) -> Any:
        return sys.stdout

    @stream.setter
    def stream(self, value: Any) -> None:
        pass


def configure_logging(logger_provider: LoggerProvider | None) -> None:
    """Install the two root handlers once; safe to call again.

    With `logger_provider=None` (the SDK is off) the OTel handler binds to
    the API's no-op provider, so stdout still gets JSON and nothing exports.
    """
    root = logging.getLogger()
    if any(isinstance(h, LoggingHandler) for h in root.handlers):
        return
    stdout = _StdoutHandler()
    stdout.setFormatter(JsonFormatter())
    otel = LoggingHandler(logger_provider=logger_provider)
    for handler in (stdout, otel):
        handler.addFilter(EventNameFilter())
        root.addHandler(handler)
    root.setLevel(logging.INFO)
    # uvicorn installs its own plain-text handlers and stops propagation;
    # route its loggers through the root so they are JSON on stdout and
    # reach OTLP like everything else.
    for name in ("uvicorn", "uvicorn.error"):
        framework = logging.getLogger(name)
        framework.handlers.clear()
        framework.propagate = True
    # The request log middleware replaces uvicorn's access line, which prints
    # the raw path and query string (`--no-access-log` is then redundant).
    logging.getLogger("uvicorn.access").disabled = True
