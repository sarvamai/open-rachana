"""SDK bootstrap: build providers from the OTel environment, instrument the app.

`register_providers` runs once per process and installs the global tracer,
meter and logger providers with the guard processors in front of the OTLP
exporters. Tests inject in-memory exporters through the same function.
`configure` runs once per app and is a no-op when `OTEL_SDK_DISABLED=true`
(spec §4.1, principle 4). Every setting is an OTel environment variable
(spec §5); nothing here names a backend.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

# Stable HTTP conventions and the http.server.request.duration metric. The
# instrumentation latches this once per process the first time anything
# instruments, so it is set at import, before any instrumentor can run.
os.environ.setdefault("OTEL_SEMCONV_STABILITY_OPT_IN", "http")

from fastapi import FastAPI  # noqa: E402
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    SimpleLogRecordProcessor,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor

from mulyankan_platform.observability.guard import (
    LogAttributeGuard,
    SpanAttributeGuard,
    metric_views,
)
from mulyankan_platform.observability.http import RequestLogMiddleware
from mulyankan_platform.observability.logs import configure_logging
from mulyankan_platform.observability.metrics import (
    attributes_dropped,
    observe_registry_bindings,
)

if TYPE_CHECKING:  # registry imports this package; keep the edge type-only
    from mulyankan_platform.registry import ProviderRegistry

# Process-level instruments only; host metrics come from the Collector (§6.3).
# Label lists mirror the instrumentation's defaults for the chosen keys.
_PROCESS_METRICS = {
    "process.cpu.time": ["user", "system"],
    "process.cpu.utilization": ["user", "system"],
    "process.memory.usage": None,
    "process.memory.virtual": None,
    "process.open_file_descriptor.count": None,
    "process.thread.count": None,
    "cpython.gc.collections": None,
}


@dataclass(frozen=True)
class Providers:
    tracer_provider: TracerProvider
    meter_provider: MeterProvider
    logger_provider: LoggerProvider


_providers: Providers | None = None


def sdk_disabled() -> bool:
    return os.environ.get("OTEL_SDK_DISABLED", "").strip().lower() == "true"


def register_providers(
    *, span_exporter=None, metric_reader=None, log_exporter=None
) -> Providers:
    """Install the global providers once; later calls return the same set.

    Exporters can only be chosen by the first call: the global providers
    cannot be replaced, so a later call that asks for different ones would be
    silently ignored. It raises instead.
    """
    global _providers
    if _providers is not None:
        if span_exporter or metric_reader or log_exporter:
            raise RuntimeError(
                "providers are already installed; exporters cannot change"
            )
        return _providers

    # Resource.create() runs the env detector: OTEL_SERVICE_NAME and
    # OTEL_RESOURCE_ATTRIBUTES are the descriptor (ADR-0011).
    resource = Resource.create()

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(SpanAttributeGuard(attributes_dropped))
    if span_exporter is None:
        tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    else:
        tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[
            metric_reader or PeriodicExportingMetricReader(OTLPMetricExporter())
        ],
        views=metric_views(),  # the metric-side guard (§4.2)
    )
    metrics.set_meter_provider(meter_provider)

    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(LogAttributeGuard(attributes_dropped))
    if log_exporter is None:
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(OTLPLogExporter())
        )
    else:
        logger_provider.add_log_record_processor(SimpleLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)
    configure_logging(logger_provider)

    instrumentor = SystemMetricsInstrumentor(config=_PROCESS_METRICS)
    if not instrumentor.is_instrumented_by_opentelemetry:
        instrumentor.instrument(meter_provider=meter_provider)

    _providers = Providers(tracer_provider, meter_provider, logger_provider)
    return _providers


def configure(app: FastAPI, registry: ProviderRegistry | None = None) -> None:
    """Instrument `app`. With the SDK disabled only the structured stdout log
    and the request log remain; nothing exports. Never raises: a bad
    endpoint surfaces as exporter warnings, and the app serves.

    `registry` feeds the `mulyankan.registry.bindings` gauge.
    """
    if sdk_disabled():
        configure_logging(None)
        app.add_middleware(RequestLogMiddleware)  # no span: the line has no trace id
        return
    providers = register_providers()
    # Added first so it runs inside the OTel middleware (added by instrument_app).
    app.add_middleware(RequestLogMiddleware)
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=providers.tracer_provider,
        meter_provider=providers.meter_provider,
        # The instrumentation reads these variables at import time and treats
        # None as "use that snapshot"; resolve them here so the value at
        # configure time always wins, including "unset" (D9, spec §5).
        excluded_urls=os.environ.get(
            "OTEL_PYTHON_FASTAPI_EXCLUDED_URLS",
            os.environ.get("OTEL_PYTHON_EXCLUDED_URLS", ""),
        ),
        exclude_spans=["receive", "send"],  # the ASGI message spans are noise
    )
    if registry is not None:
        observe_registry_bindings(registry)
