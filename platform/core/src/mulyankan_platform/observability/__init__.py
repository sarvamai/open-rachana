"""Observability: OpenTelemetry wiring for the core (ADR-0011, ASR02-OBS).

Everything the application knows about telemetry is here. It speaks the OTel
API only; the sink is whatever `OTEL_EXPORTER_OTLP_ENDPOINT` names.

`configure` and `register_providers` are resolved lazily: `setup` pulls in
FastAPI, the exporters and the instrumentors, and the audit chain and the
registry import this package for `metrics` and `providers` alone, which need
only the OTel API.
"""

from __future__ import annotations

from typing import Any

__all__ = ["configure", "register_providers"]


def __getattr__(name: str) -> Any:
    if name in __all__:
        from mulyankan_platform.observability import setup

        return getattr(setup, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
