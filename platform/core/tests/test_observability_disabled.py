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
    # Logging is still structured on stdout, with nothing exported.
    import logging
    logging.getLogger("probe").warning("probe.event", extra={"mulyankan.object_ref": "x"})
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
    assert '"event": "probe.event"' in result.stdout  # the JSON handler is on
    assert '"mulyankan.object_ref": "x"' in result.stdout
    assert '"event": "http.request"' in result.stdout  # the request log too
    assert '"http.route": "/healthz"' in result.stdout


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


AUDIT_ONLY = textwrap.dedent(
    """
    import os, sys
    import mulyankan_platform.audit, mulyankan_platform.registry
    assert "mulyankan_platform.observability.setup" not in sys.modules, "setup imported eagerly"
    assert "fastapi" not in sys.modules, "fastapi imported by the audit chain"
    assert "OTEL_SEMCONV_STABILITY_OPT_IN" not in os.environ, "environment mutated at import"
    print("light")
    """
)


def test_audit_and_registry_import_only_the_otel_api() -> None:
    """A verifier or the M1 store imports the chain without FastAPI, the
    exporters or a mutated environment: only the OTel API comes along."""
    env = {k: v for k, v in os.environ.items() if k != "OTEL_SEMCONV_STABILITY_OPT_IN"}
    result = subprocess.run(
        [sys.executable, "-c", AUDIT_ONLY],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    assert "light" in result.stdout
