# `platform/core/` — `mulyankan-platform`

The workflow core: provider registry, hash-chained audit log, session
monitoring, and the FastAPI `core_api` (`GET /healthz`, plus the
session-monitoring surface of ASR02-OBS-01).

## What is here

- `registry.py` — `ProviderRegistry` resolves `"module:attr"` bindings from
  `platform.yaml` via `importlib`. The core never imports a provider any
  other way; malformed or unloadable bindings raise at startup, an unbound
  capability at call time. `get()` returns the provider wrapped in
  `ObservedProvider`, which spans each call; the wrapping is eager so runtime
  Protocol checks still pass.
- `audit/chain.py` — the append-only audit chain (below).
- `core_api/main.py` — reads `platform.yaml`
  (`$MULYANKAN_PLATFORM_CONFIG`); no such file is committed, and with none
  the app starts with zero bindings. Serves the session-monitoring endpoints
  (`/v1/sessions...`, `/v1/integrity/sessions`). `app` is a uvicorn
  factory (`uvicorn --factory ...main:app`), not an instance: `build_app`
  calls `observability.configure`, and importing the module must stay free
  of side effects, so nothing is built or instrumented until the factory
  runs.
- `observability/` — OTel wiring (ADR-0011, `docs/observability.md`):
  `setup.py` installs the providers from the `OTEL_*` environment and
  instruments FastAPI and the process metrics; `guard.py` holds the
  attribute allowlists that keep every span, log and metric content-free;
  `logs.py`, `http.py`, `providers.py` and `metrics.py` are the structured
  log, the request log, the provider-call proxy and the domain instruments.
  The package `__init__` is lazy: `audit/` and `registry.py` import
  `metrics` and `providers` without pulling in FastAPI or the exporters.
  Add an attribute only by adding it to the allowlist with a reason; the
  sentinel test `test_asr02obs_no_content_reaches_any_exporter` fails
  otherwise. `OTEL_SDK_DISABLED=true` turns it all off.
- `sessions/monitor.py` — session register/heartbeat/close (ASR02-OBS-01, a
  platform concern per ADR-0004) and the first monitoring signal:
  client-reported copy/cut/paste or a server-detected heartbeat gap. A signal
  deducts a fixed amount from the integrity score (starts at 100, never
  recovers in-session) and appends a content-free security event to the audit
  chain; automatic suspension stays off. The score rides the event's payload
  hash — event fields stay opaque. The in-memory store is M1 scaffolding; the
  database-backed store keeps each state change and its audit event in one
  transaction (ARC-02).

  Reads and writes are deliberately separate, and the split is the part the
  database store inherits:

  - `integrity_view` is **pure**. `silent` is derived from the clock, so
    polling the operator view — a refresh, a retry, a prober — cannot alter a
    score or the chain. It is also filtered and bounded (`status`, `limit`):
    "return everything" is not a shape that ports to a table.
  - `sweep` is the **only** writer of gap signals, idempotent per silence
    episode, and stamps the event at `last_heartbeat_at + GAP_THRESHOLD` — when
    the gap happened, not when the sweep noticed. One lifespan task drives it
    here; a single-writer guard drives it once there is more than one replica.
  - Every public method holds the monitor's lock, and `AuditLog.append` holds
    its own: the handlers are sync `def`, so Starlette runs them concurrently
    on the threadpool and both maps are genuinely shared.
  - The record keeps counters, not per-signal history — the chain is the log.
    Closed sessions are evicted after `CLOSED_RETENTION` (archival, in M1).

  **Unauthenticated.** Nothing validates a caller, and the `session_id` the
  operator view publishes is the bearer for every write. Read "Known
  limitations" in `SECURITY.md` before exposing this anywhere.
- `tests/` — registry, audit-chain, healthz, and session-monitor tests;
  requirement-facing names carry their ID (`test_asrevd02_...`,
  `test_asr02obs01_...`).

## `audit/chain.py` is wire format, not style

- `canonical_bytes`: sorted keys, `(",", ":")`, `ensure_ascii=False`, UTF-8.
  Changing any of it changes every hash ever computed. Versioned by
  `CANONICAL_SCHEMA_VERSION` (`draft-v0.1`), which the hash covers; bump
  deliberately.
- Chain rule: `sha256(bytes.fromhex(prev_hash) || link_bytes())`, where
  `link_bytes()` excludes the `hash` field. Genesis is 64 zeros.
- `append(payload=...)` hashes the payload and discards it. Never add a
  field that retains it — events stay content-free (opaque refs + payload
  hash).
- `append` records two metrics and adds a span event carrying the event id.
  Telemetry links point at events; no telemetry field is stored on an event,
  so the canonical bytes are unaffected.
- The in-memory `AuditLog` is M0 scaffolding; M1's database store must
  produce byte-identical events. Treat its semantics as the specification.

## Logging

Standard library `logging`. The message is a static dotted event name, and
every value goes in `extra` under an allowlisted key such as
`mulyankan.object_ref` or `mulyankan.state.to`:

```python
logger.info("draft.submitted", extra={"mulyankan.object_ref": ref})
```

`observability/logs.py` renders JSON to stdout and forwards to OTLP. A body
that is not a dotted event name (an f-string, say, or a sentence) is
exported as `log.unstructured` and counted. `extra` keys off the allowlist
are dropped and counted. uvicorn's access log is disabled; `observability/http.py` replaces it with
one `http.request` record per request, keyed on the route template and
carrying the trace id, and sets the `Server-Timing` header (D12).

## Tests

`tests/conftest.py` synthesises an importable `testkit_fake_provider` in
`sys.modules` so the registry's `importlib` path is testable without a real
provider; use that double rather than adding a provider package to make a
test pass. It also installs in-memory OTel exporters at import time, before
any test module imports `core_api.main`; the `telemetry` fixture exposes
them. Tests that need a fresh process (SDK disabled, Collector unreachable)
run a subprocess.

```bash
python -m pytest platform/core -q
```

## Keeping this file true

Update it when you add a module or endpoint, touch the canonicalization or
chain rule, or change how tests fake a provider.
