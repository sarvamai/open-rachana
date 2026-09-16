"""Content-free guard: attribute allowlists applied before export (ASR02-OBS).

The FastAPI and ASGI instrumentations emit `url.query`, `url.path`,
`user_agent.original` and `exception.message`, any of which can carry what a
user typed. The root invariant is that no question content reaches logs,
traces or metrics, so every attribute is removed unless it is listed here.
Removed keys are counted so a new attribute from an upgraded instrumentation
shows up in a metric rather than leaking silently.

Filtering is by key, with one exception: `exception.stacktrace`. The SDK's
`record_exception` renders the trace with `traceback.format_exception`, whose
last line is `ExceptionType: message`, so the value is rewritten to its frame
lines before export (`frames_only`). Metric attributes go through an SDK
`View` (`metric_views`) rather than a processor; a View drops silently, so
metric drops are not counted and the §7 sentinel test is the check.

This list is what an auditor reads: one entry per line, with the reason.
The Collector's redaction list mirrors the union of the three sets below
(`tests/test_dev_stack.py` pins that), and the web tier's allowlist will
mirror it when that slice lands.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from typing import Any

from opentelemetry.attributes import BoundedAttributes
from opentelemetry.metrics import Counter
from opentelemetry.sdk._logs import LogRecordProcessor
from opentelemetry.sdk.metrics.view import View
from opentelemetry.sdk.trace import Event, ReadableSpan, SpanProcessor
from opentelemetry.sdk.util import BoundedList
from opentelemetry.trace import Status

ALLOWED_SPAN_ATTRIBUTES: frozenset[str] = frozenset(
    {
        "http.request.method",  # the verb only
        "http.route",  # the template; the concrete path is dropped
        "http.response.status_code",
        "http.request.body.size",
        "http.response.body.size",
        "url.scheme",
        "server.address",
        "server.port",
        "network.protocol.version",
        "client.address",  # D10: operational security signal, not content
        "error.type",  # status class or exception class name
        "exception.type",
        "exception.stacktrace",  # frame lines only: frames_only() removes the message
        "enduser.pseudo.id",  # DAT-02 pseudonymous workforce id, never enduser.id
        "mulyankan.spi",
        "mulyankan.provider.name",
        "mulyankan.provider.version",
        "mulyankan.audit.event_id",
        "mulyankan.object_ref",  # opaque identifiers only
        "mulyankan.state.from",
        "mulyankan.state.to",
        "mulyankan.http.request.duration",  # seconds, request log only
        "db.system.name",  # M1
        "db.operation.name",  # M1
        "db.collection.name",  # M1; db.query.text is decided by D11
    }
)

ALLOWED_LOG_ATTRIBUTES: frozenset[str] = ALLOWED_SPAN_ATTRIBUTES | frozenset(
    {
        "code.function.name",
        "code.file.path",
        "code.line.number",
    }
)

# Metric data-point attributes (spec §3.2). Spelled out rather than derived
# from the span set: a View filters by key only and never sanitises a value,
# and every key here must be a bounded set (a metric label is a series).
# `exception.stacktrace`, `client.address`, `enduser.pseudo.id` and the
# `mulyankan.*` identifiers are therefore span-only.
ALLOWED_METRIC_ATTRIBUTES: frozenset[str] = frozenset(
    {
        # http.server.request.duration and the request/response body sizes
        "http.request.method",
        "http.route",
        "http.response.status_code",
        "url.scheme",
        "network.protocol.version",
        # server.address and server.port stay off metrics: the address is the
        # request's Host header, so a client would control the series count.
        "error.type",  # status class or exception class name
        # mulyankan.observability.attributes_dropped
        "signal",
        "attribute",  # a bounded key label, see `dropped_key_label`
        "action",  # mulyankan.audit.events
        "spi",  # mulyankan.registry.bindings
        "provider.name",  # mulyankan.registry.bindings
        "provider.version",  # mulyankan.registry.bindings
        "from_state",  # mulyankan.workflow.transitions (M1)
        "to_state",  # mulyankan.workflow.transitions (M1)
        "type",  # process.cpu.time: user | system
        "generation",  # cpython.gc.collections: 0 | 1 | 2
    }
)

# The log body is not an attribute, so the allowlist cannot see it. The
# rule (spec §4.4) is that a body is a static, dotted event name such as
# `draft.submitted`; anything else is an interpolated or free-text message
# and is replaced before export. Framework loggers (uvicorn) log constants
# about the process and pass through.
UNSTRUCTURED_EVENT = "log.unstructured"
_EVENT_NAME = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$")
_FRAMEWORK_LOGGERS = ("uvicorn",)


def event_name(body: object, logger_name: str) -> str:
    """The body to export: the event name itself, or the placeholder."""
    if not isinstance(body, str):
        return UNSTRUCTURED_EVENT
    if logger_name.split(".", 1)[0] in _FRAMEWORK_LOGGERS:
        return body
    return body if _EVENT_NAME.match(body) else UNSTRUCTURED_EVENT


# The `attribute` label of the dropped counter is a key NAME, but names are
# not always code-controlled: captured request headers become
# `http.request.header.<name>` keys, and a client picks the name. Bucket
# those by prefix, and cap the distinct labels this process will ever emit.
DROPPED_LABEL_LIMIT = 64
_BUCKETED_PREFIXES = ("http.request.header.", "http.response.header.")
_seen_dropped_keys: set[str] = set()


def dropped_key_label(key: str) -> str:
    for prefix in _BUCKETED_PREFIXES:
        if key.startswith(prefix):
            return prefix + "*"
    if key in _seen_dropped_keys:
        return key
    if len(_seen_dropped_keys) >= DROPPED_LABEL_LIMIT:
        return "other"
    _seen_dropped_keys.add(key)
    return key


# A rendered traceback is one or more sections, each `Traceback (most recent
# call last):`, then frames (`  File "<path>", line <n>, in <name>` plus
# indented source and caret lines), then the `Type: message` line and any
# notes. Frames are only read while a section's header has armed them and
# the first non-frame line (the message) disarms until the next header, so
# a message that itself contains a File-shaped line cannot smuggle its
# following lines through. Header-less input (`traceback.format_tb`) arms
# from the start.
_HEADER_LINE = "Traceback (most recent call last):"
_FRAME_LINE = re.compile(r'^\s+File ".*", line \d+, in .*$')


def frames_only(stacktrace: str) -> str:
    """Reduce a `traceback.format_exception` rendering to its frame lines."""
    kept: list[str] = []
    lines = stacktrace.splitlines()
    armed = bool(lines) and _FRAME_LINE.match(lines[0]) is not None
    in_frame = False
    for line in lines:
        if line == _HEADER_LINE:
            armed, in_frame = True, False
        elif not armed:
            continue
        elif _FRAME_LINE.match(line):
            in_frame = True
            kept.append(line)
        elif in_frame and line.startswith("    "):
            kept.append(line)
        else:
            armed, in_frame = False, False  # the message line ends the section
    return "\n".join(kept)


_SANITISERS: dict[str, Callable[[Any], Any]] = {
    "exception.stacktrace": lambda v: frames_only(v) if isinstance(v, str) else "",
}


def metric_views() -> list[View]:
    """One View matching every instrument: the SDK drops unlisted keys at
    aggregation time, before any reader sees them."""
    return [View(instrument_name="*", attribute_keys=set(ALLOWED_METRIC_ATTRIBUTES))]


def filter_attributes(
    attributes: Mapping[str, Any] | None,
    allowed: frozenset[str],
    dropped: Counter | None,
    signal: str,
) -> dict[str, Any]:
    kept: dict[str, Any] = {}
    for key, value in (attributes or {}).items():
        if key in allowed:
            sanitise = _SANITISERS.get(key)
            kept[key] = sanitise(value) if sanitise else value
        elif dropped is not None:
            dropped.add(1, {"signal": signal, "attribute": dropped_key_label(key)})
    return kept


def _rebound(old: Any, kept: dict[str, Any]) -> Any:
    """Keep the SDK's limit bookkeeping: a plain dict would report zero
    dropped attributes and hide that a span or log limit is cutting data."""
    if not isinstance(old, BoundedAttributes):
        return kept
    new = BoundedAttributes(
        maxlen=old.maxlen,
        attributes=kept,
        immutable=True,
        max_value_len=old.max_value_len,
    )
    new.dropped = old.dropped
    return new


class SpanAttributeGuard(SpanProcessor):
    """Strips unlisted attributes from a span and its events at end time.

    `ReadableSpan` has no setter; the SDK keeps attributes in `_attributes`
    and events in `_events`, and exporters read both after `on_end`. The
    guard test pins this so an SDK upgrade cannot reopen the leak unnoticed.
    Register this processor before the exporting processor.
    """

    def __init__(self, dropped: Counter | None = None) -> None:
        self._dropped = dropped

    def on_start(self, span, parent_context=None) -> None:
        return None

    def on_end(self, span: ReadableSpan) -> None:
        span._attributes = _rebound(
            span._attributes,
            filter_attributes(
                span.attributes, ALLOWED_SPAN_ATTRIBUTES, self._dropped, "span"
            ),
        )
        old_events = span._events
        events = BoundedList(
            old_events._dq.maxlen if isinstance(old_events, BoundedList) else None
        )
        for event in span.events:
            events.append(
                Event(
                    event.name,
                    filter_attributes(
                        event.attributes, ALLOWED_SPAN_ATTRIBUTES, self._dropped, "span"
                    ),
                    event.timestamp,
                )
            )
        events.dropped = getattr(old_events, "dropped", 0)
        span._events = events
        # The SDK renders the escaped exception as `Type: message` into the
        # status description; the OTLP encoder exports it as Status.message.
        if span.status.description:
            span._status = Status(span.status.status_code)

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


class LogAttributeGuard(LogRecordProcessor):
    """Strips unlisted attributes from a log record before export."""

    def __init__(self, dropped: Counter | None = None) -> None:
        self._dropped = dropped

    def on_emit(self, record) -> None:
        # SDK >= 1.44 hands the processor a ReadWriteLogRecord wrapping the
        # API LogRecord; the attributes live on the inner record.
        inner = record.log_record
        inner.attributes = _rebound(
            inner.attributes,
            filter_attributes(
                inner.attributes, ALLOWED_LOG_ATTRIBUTES, self._dropped, "log"
            ),
        )
        scope = record.instrumentation_scope
        exported = event_name(inner.body, scope.name if scope else "")
        if exported != inner.body:
            inner.body = exported
            if self._dropped is not None:
                self._dropped.add(1, {"signal": "log", "attribute": "body"})

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True
