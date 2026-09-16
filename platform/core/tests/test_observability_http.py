"""Request log: route template, sizes, status, Server-Timing (ASR02-OBS, D12)."""

import json
import logging

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from mulyankan_platform.observability.http import RequestLogMiddleware

SENTINEL = "SENTINEL-77b0"
LOGGER = "mulyankan_platform.observability.http"


def _app() -> FastAPI:
    app = FastAPI()

    @app.get("/items/{item_id}")
    def item(item_id: str, q: str | None = None) -> dict:
        return {"ok": True}

    @app.get("/boom")
    def boom() -> dict:
        raise RuntimeError(SENTINEL)

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok"}

    router = APIRouter()

    @router.post("/nested/{x}")
    def nested(x: str) -> dict:
        return {}

    app.include_router(router)

    async def raw(scope, receive, send) -> None:  # an ASGI app that omits `headers`
        await send({"type": "http.response.start", "status": 200})
        await send({"type": "http.response.body", "body": b"raw"})

    app.mount("/raw", raw)
    app.add_middleware(RequestLogMiddleware)
    return app


def _request_lines(caplog) -> list[dict]:
    return [{**r.__dict__} for r in caplog.records if r.getMessage() == "http.request"]


def test_asr02obs_request_log_uses_route_not_path(caplog) -> None:
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app())
    response = client.get(f"/items/{SENTINEL}?q={SENTINEL}")
    assert response.status_code == 200
    (line,) = _request_lines(caplog)
    assert line["http.route"] == "/items/{item_id}"
    assert line["http.request.method"] == "GET"
    assert line["http.response.status_code"] == 200
    assert line["http.response.body.size"] == len(response.content)
    assert line["mulyankan.http.request.duration"] >= 0
    assert SENTINEL not in json.dumps(line, default=str)


def test_request_log_records_500_when_the_handler_raises(caplog) -> None:
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app(), raise_server_exceptions=False)
    assert client.get("/boom").status_code == 500
    (line,) = _request_lines(caplog)
    assert line["http.response.status_code"] == 500
    assert SENTINEL not in json.dumps(line, default=str)


def test_request_log_omits_missing_fields_for_unmatched_routes(caplog) -> None:
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app())
    assert client.get(f"/nope/{SENTINEL}").status_code == 404
    (line,) = _request_lines(caplog)
    assert "http.route" not in line  # no template: omitted, never the path
    assert line["http.response.status_code"] == 404
    assert SENTINEL not in json.dumps(line, default=str)


def test_request_log_honours_the_excluded_urls(caplog, monkeypatch) -> None:
    """D9: the same exclusion as the span and the metric, so a probe leaves no line."""
    monkeypatch.setenv("OTEL_PYTHON_FASTAPI_EXCLUDED_URLS", r"^https?://[^/]+/healthz$")
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app())
    assert client.get("/healthz").status_code == 200
    assert client.get("/items/1").status_code == 200
    assert [line["http.route"] for line in _request_lines(caplog)] == [
        "/items/{item_id}"
    ]


def test_request_log_route_matches_the_span_for_included_and_partial_routes(
    caplog,
) -> None:
    """The line must join to the span and the metric by route, so it uses the
    instrumentation's own resolution: included routers and 405s included."""
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app())
    assert client.post(f"/nested/{SENTINEL}").status_code == 200
    assert client.get("/nested/1").status_code == 405  # a partial match
    routes = [line["http.route"] for line in _request_lines(caplog)]
    assert routes == ["/nested/{x}", "/nested/{x}"]
    assert SENTINEL not in json.dumps(_request_lines(caplog), default=str)


def test_request_log_survives_a_bad_content_length_and_a_headerless_response(
    caplog,
) -> None:
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app())
    assert client.get("/items/1", headers={"content-length": "abc"}).status_code == 200
    assert client.get("/raw/x").status_code == 200
    lines = _request_lines(caplog)
    assert [line["http.response.status_code"] for line in lines] == [200, 200]
    assert "http.request.body.size" not in lines[0]  # unparseable: omitted
