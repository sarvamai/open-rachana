"""One content-free log line per request, and the trace id for humans (D12).

Pure ASGI so it sits inside the OTel ASGI middleware: the server span is
current while it runs, so the log line gets the trace id and the
`Server-Timing` header can carry it. Requests the instrumentation excludes
(D9, `OTEL_PYTHON_FASTAPI_EXCLUDED_URLS`) leave no line either.
"""

from __future__ import annotations

import logging
import os
import time
from collections.abc import Awaitable, Callable, MutableMapping
from typing import Any

from opentelemetry import trace
from opentelemetry.instrumentation.asgi import get_host_port_url_tuple
from opentelemetry.instrumentation.fastapi import _get_route_details
from opentelemetry.trace import format_span_id, format_trace_id
from opentelemetry.util.http import ExcludeList, parse_excluded_urls

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]

logger = logging.getLogger(__name__)


def route_template(scope: Scope) -> str | None:
    """The route as the server span records it, such as `/items/{item_id}`,
    so the log line joins to the span and the metric. Included routers are
    flattened and a partial match (a 405) still names the route; the raw
    path is not used."""
    try:
        return _get_route_details(scope)
    except Exception:  # a scope without an app, or a foreign router
        return None


def _header(scope: Scope, name: bytes) -> str | None:
    for key, value in scope.get("headers") or []:
        if key == name:
            return value.decode("latin-1")
    return None


def _content_length(scope: Scope) -> int | None:
    value = _header(scope, b"content-length")
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:  # a lax server let it through; the line must still emit
        return None


def _exclusions() -> ExcludeList | None:
    pattern = os.environ.get(
        "OTEL_PYTHON_FASTAPI_EXCLUDED_URLS",
        os.environ.get("OTEL_PYTHON_EXCLUDED_URLS", ""),
    )
    return parse_excluded_urls(pattern) if pattern else None


class RequestLogMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self._excluded = _exclusions()  # resolved once, when the stack is built

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or self._is_excluded(scope):
            await self.app(scope, receive, send)
            return

        route = route_template(scope)  # before the router mutates the scope
        started = time.perf_counter()
        status: int | None = None
        response_bytes = 0

        async def send_wrapper(message: Message) -> None:
            nonlocal status, response_bytes
            if message["type"] == "http.response.start":
                status = message["status"]
                ctx = trace.get_current_span().get_span_context()
                if ctx.is_valid:
                    headers = message.setdefault("headers", [])  # optional per ASGI
                    value = (
                        f'traceparent;desc="00-{format_trace_id(ctx.trace_id)}'
                        f'-{format_span_id(ctx.span_id)}-{ctx.trace_flags:02x}"'
                    )
                    headers.append((b"server-timing", value.encode("latin-1")))
            elif message["type"] == "http.response.body":
                response_bytes += len(message.get("body", b""))
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            fields: dict[str, Any] = {
                "http.request.method": scope["method"],
                "http.response.status_code": status if status is not None else 500,
                "http.response.body.size": response_bytes,
                "mulyankan.http.request.duration": round(
                    time.perf_counter() - started, 6
                ),
            }
            # Omitted when absent: the handler drops a null attribute with a
            # warning, and the raw path must not stand in for the route.
            if route:
                fields["http.route"] = route
            request_bytes = _content_length(scope)
            if request_bytes is not None:
                fields["http.request.body.size"] = request_bytes
            client = (scope.get("client") or ("", 0))[0]
            if client:
                fields["client.address"] = client
            actor = (scope.get("state") or {}).get("enduser_pseudo_id")
            if actor:
                fields["enduser.pseudo.id"] = actor  # set by the M1 session dependency
            logger.info("http.request", extra=fields)

    def _is_excluded(self, scope: Scope) -> bool:
        if self._excluded is None:
            return False
        _, _, url = get_host_port_url_tuple(scope)
        return self._excluded.url_disabled(url)
