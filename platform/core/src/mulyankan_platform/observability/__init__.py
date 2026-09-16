"""Observability: OpenTelemetry wiring for the core (ADR-0011, ASR02-OBS).

Everything the application knows about telemetry is here. It speaks the OTel
API only; the sink is whatever `OTEL_EXPORTER_OTLP_ENDPOINT` names.
"""

from mulyankan_platform.observability.setup import configure, register_providers

__all__ = ["configure", "register_providers"]
