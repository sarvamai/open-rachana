"""The SDK off switch: the app serves and nothing is registered (ASR02-OBS)."""

import os
import subprocess
import sys
import textwrap

SCRIPT = textwrap.dedent(
    """
    import os
    os.environ["OTEL_SDK_DISABLED"] = "true"
    import mulyankan_platform.observability
    from fastapi.testclient import TestClient
    from mulyankan_platform.core_api.main import create_app_from_mapping
    from opentelemetry import trace
    client = TestClient(create_app_from_mapping({}))
    assert client.get("/healthz").status_code == 200
    # No SDK provider was installed: the API proxy is still in place.
    assert type(trace.get_tracer_provider()).__name__ == "ProxyTracerProvider"
    print("served")
    """
)


def test_asr02obs_app_serves_with_sdk_disabled() -> None:
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert "served" in result.stdout


IMPORT_ONLY = textwrap.dedent(
    """
    # No OTEL_SDK_DISABLED here: the SDK is on, and importing must still be free.
    import mulyankan_platform.core_api.main as main
    from opentelemetry import trace
    assert type(trace.get_tracer_provider()).__name__ == "ProxyTracerProvider", "import installed providers"
    assert callable(main.app), "app must be a factory, not an instance built at import"
    application = main.app()
    assert type(trace.get_tracer_provider()).__name__ == "TracerProvider", "the factory instruments"
    print("lazy")
    """
)


def test_asr02obs_importing_the_entrypoint_installs_nothing() -> None:
    """Importing core_api.main must not start exporters: scripts, tests and
    tooling import it without wanting telemetry. `app` is a uvicorn factory."""
    result = subprocess.run(
        [sys.executable, "-c", IMPORT_ONLY],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
        env={
            **os.environ,
            "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:9",
            "OTEL_EXPORTER_OTLP_TIMEOUT": "1",
        },
    )
    assert result.returncode == 0, result.stderr
    assert "lazy" in result.stdout
