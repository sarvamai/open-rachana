# Local observability stack

An OpenTelemetry Collector with the project's configuration, and Grafana's
all-in-one image (Grafana, Tempo, Loki, Prometheus) as the backend.

Grafana is a local development tool. It is not a dependency of the project,
and no dashboard or alert committed here may be required for the system to
function. The production backend is chosen later; it replaces the `exporters`
block in `otel-collector.yaml` and nothing else.

## Run

    docker compose -f deploy/dev/compose.yaml up -d
    curl -s localhost:13133          # Collector health
    source deploy/dev/.env.example   # the OTel SDK variables (spec §5)

    # core-api, from the repo root
    OTEL_SERVICE_NAME=core-api uvicorn --factory mulyankan_platform.core_api.main:app --no-access-log --port 8000

Open http://localhost:3001 (admin / admin), Explore, Tempo, and search
`service.name = core-api`: every request except `/healthz` is a trace named
by its route. Prometheus has `http_server_request_duration_seconds` by route
and the `process_*` runtime metrics. `OTEL_SDK_DISABLED=true` turns the SDK
off; the app serves either way. `--factory` matters: `app` is a function, so
importing the module never starts an exporter.

## What runs, and where to look

| Tool | Role | Where |
|---|---|---|
| OpenTelemetry Collector (contrib) | the only thing the apps talk to; applies the redaction allowlist | OTLP on `localhost:4317` (gRPC) and `4318` (HTTP), health on `13133` |
| Grafana | the UI for everything below | http://localhost:3001, admin / admin |
| Tempo | traces | Explore, datasource "Tempo", TraceQL `{ resource.service.name = "core-api" }` |
| Prometheus | metrics | Explore, datasource "Prometheus", PromQL `http_server_request_duration_seconds_count` |
| Loki | logs (empty until the structured-logs task lands) | Explore, datasource "Loki" |

In Grafana: **Dashboards, Mulyankan** for the three provisioned dashboards;
**Explore** for ad-hoc queries, with the datasource picker top left. From a
trace, the span attributes are the allowlisted keys and nothing else; from a
metric, the `service_name` label is the process. Pyroscope is also in the
image but nothing sends profiles to it.

## Dashboards

`grafana/dashboards/` holds three development dashboards, provisioned on
start-up under the "Mulyankan" folder: the service overview (rate, errors,
latency by route, in-flight requests, recent traces), the content-free guard
(attributes dropped per key and signal), and the process runtime. Edit them in
Grafana, then export with "Share, Export, Export as JSON" and paste the file
back; provisioned dashboards cannot be saved from the UI. Keep them keyed on
`service.name`, routes and metric names, never on a URL or a content-bearing
attribute; `platform/core/tests/test_dev_stack.py` checks the basics.

The web app joins the stack with the Next.js slice of the plan
(`docs/observability-plan.md`, Tasks 11 to 14); structured logs in Loki
arrive with Task 5.

## Stop and reset

    docker compose -f deploy/dev/compose.yaml down -v

Recreating only the `lgtm` container (for example after editing a dashboard
mount) gives it a new address that the Collector's open connections do not
follow; restart the Collector as well, or the backend stops receiving data.
