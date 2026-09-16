"""The standing DoD check: no Restricted content in any exported signal, and
the app survives without a Collector (ASR02-OBS)."""

import subprocess
import sys
import textwrap

import pytest

from fastapi import Header
from fastapi.testclient import TestClient
from mulyankan_platform.core_api.main import create_app_from_mapping

SENTINEL = "SENTINEL-e8b4-ప్రశ్న"  # includes non-ASCII so encoding paths are covered
HEADER_SENTINEL = "SENTINEL-e8b4-header"  # HTTP header values must be ASCII


def test_asr02obs_no_content_reaches_any_exporter(telemetry) -> None:
    app = create_app_from_mapping({})

    @app.post("/probe/{item}")
    def probe(
        item: str,
        body: dict,
        q: str | None = None,
        x_probe: str | None = Header(default=None),
    ) -> dict:
        raise ValueError(f"{item} {q} {x_probe} {body}")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.post(
        f"/probe/{SENTINEL}?q={SENTINEL}",
        headers={"x-probe": HEADER_SENTINEL},
        json={"stem": SENTINEL},
    )
    assert response.status_code == 500

    exported = telemetry.dump()
    assert "POST /probe/{item}" in exported  # the pipeline did see the request
    assert SENTINEL not in exported
    assert HEADER_SENTINEL not in exported


def test_asr02obs_server_span_carries_route_not_path(telemetry) -> None:
    client = TestClient(create_app_from_mapping({}))
    assert client.post("/v1/sessions", json={"actor": SENTINEL}).status_code == 201

    (server_span,) = [s for s in telemetry.spans() if s.name == "POST /v1/sessions"]
    assert server_span.attributes["http.route"] == "/v1/sessions"
    assert "url.path" not in server_span.attributes
    assert "url.query" not in server_span.attributes
    assert "user_agent.original" not in server_span.attributes


def _metric_points(telemetry, name: str):
    return [
        point
        for rm in telemetry.metric_reader.get_metrics_data().resource_metrics
        for sm in rm.scope_metrics
        for m in sm.metrics
        if m.name == name
        for point in m.data.data_points
    ]


def test_asr02obs_request_duration_metric_is_recorded(telemetry) -> None:
    app = create_app_from_mapping({})

    @app.get("/metric-probe")  # a route only this test hits: the reader is cumulative
    def metric_probe() -> dict:
        return {}

    assert TestClient(app).get("/metric-probe").status_code == 200

    (point,) = [
        p
        for p in _metric_points(telemetry, "http.server.request.duration")
        if p.attributes.get("http.route") == "/metric-probe"
    ]
    assert point.count == 1
    assert set(point.attributes) <= {
        "http.request.method",
        "http.route",
        "http.response.status_code",
        "url.scheme",
        "network.protocol.version",
    }
    assert "server.address" not in point.attributes  # Host header: unbounded
    assert _metric_points(telemetry, "process.cpu.time")


def test_register_providers_refuses_new_exporters_once_installed() -> None:
    from mulyankan_platform.observability import register_providers

    with pytest.raises(RuntimeError):
        register_providers(span_exporter=object())


def test_asr02obs_healthz_is_excluded_from_traces(telemetry, monkeypatch) -> None:
    # The value from deploy/dev/.env.example and spec §5: anchored, because the
    # instrumentation applies it as an unanchored search over scheme://host/path.
    monkeypatch.setenv("OTEL_PYTHON_FASTAPI_EXCLUDED_URLS", r"^https?://[^/]+/healthz$")
    client = TestClient(create_app_from_mapping({}))
    assert client.get("/healthz").json() == {"status": "ok", "providers": {}}
    # Controls that contain the substring and must still be traced.
    assert client.post("/v1/sessions/healthz-7/heartbeat").status_code == 404
    assert (
        client.get(
            "/v1/integrity/sessions", headers={"host": "healthz.internal"}
        ).status_code
        == 200
    )
    assert sorted(s.name for s in telemetry.spans()) == [
        "GET /v1/integrity/sessions",
        "POST /v1/sessions/{session_id}/heartbeat",
    ]


def test_asr02obs_healthz_is_traced_when_nothing_is_excluded(
    telemetry, monkeypatch
) -> None:
    monkeypatch.delenv("OTEL_PYTHON_FASTAPI_EXCLUDED_URLS", raising=False)
    monkeypatch.delenv("OTEL_PYTHON_EXCLUDED_URLS", raising=False)
    client = TestClient(create_app_from_mapping({}))
    assert client.get("/healthz").status_code == 200
    assert [s.name for s in telemetry.spans()] == ["GET /healthz"]


UNREACHABLE = textwrap.dedent(
    """
    import os
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://127.0.0.1:9"
    os.environ["OTEL_EXPORTER_OTLP_TIMEOUT"] = "1"
    os.environ["OTEL_BSP_SCHEDULE_DELAY"] = "100"
    from fastapi.testclient import TestClient
    from mulyankan_platform.core_api.main import create_app_from_mapping
    client = TestClient(create_app_from_mapping({}))
    for _ in range(3):
        assert client.get("/healthz").status_code == 200
    print("served")
    """
)


def test_asr02obs_app_serves_with_collector_unreachable() -> None:
    result = subprocess.run(
        [sys.executable, "-c", UNREACHABLE],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert "served" in result.stdout
