# Observability implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give `platform/core` and `apps/web` standard OpenTelemetry tracing, metrics and logs, content-free by construction, traceable from a browser click to a provider call, with a self-contained local backend.

**Architecture:** Auto-instrumentation for FastAPI, Next.js and the browser produces the signals; four small project layers (an attribute allowlist guard, a request-log middleware, provider-call spans at the registry, domain instruments) add what auto-instrumentation cannot know. Every process exports OTLP to one Collector whose configuration is the portable artefact; Grafana's all-in-one image is the local backend only.

**Tech Stack:** Python 3.12, FastAPI, `opentelemetry-sdk` 1.44 with contrib instrumentations 0.65b0; Next.js 16.2 on Node 20, `@opentelemetry/sdk-node` 0.222, `@opentelemetry/sdk-trace-web` 2.11, `web-vitals` 6, pino 10; OpenTelemetry Collector contrib 0.160, `grafana/otel-lgtm` 0.32.1; Docker Compose; vitest 5 and Playwright 1.63 for the web tests.

**Spec:** `docs/observability.md` (working contract) and `docs/adr/0011-opentelemetry-as-telemetry-spi.md` (the decision). The plan argues from the spec; executors read both.

## Global constraints

Copied from the spec and the repo rules; every task's requirements include these.

- No question content in any span, metric, log record, exception string or URL. The allowlist guard enforces it in-process; a sentinel test proves it.
- Telemetry never blocks or fails a request. The application serves with no Collector reachable and with `OTEL_SDK_DISABLED=true`.
- Application code names only a Collector, through `OTEL_EXPORTER_OTLP_ENDPOINT`. No backend appears in code.
- Propagator is W3C `tracecontext` only; baggage is off (D8).
- Python packages: Apache-2.0, added as mandatory dependencies (D4), floor-and-ceiling pinned in `pyproject.toml` (the repo has no Python lockfile). Node packages: exact versions in `package.json`, resolved through the lockfile; `apps/web/.npmrc` refuses versions younger than 7 days, so if `pnpm add` reports a version as unavailable, take the previous patch release and record it.
- Container images digest-pinned; GitHub Actions SHA-pinned with the version in a trailing comment.
- Requirement-facing tests carry the ID: `test_asr02obs_...` (Python) and `asr02obs ...` in the test title (web).
- British spelling in prose. Commits signed off: `git commit -s`. One concern per PR; the five slices below are five PRs, in order.
- Every slice updates the `AGENTS.md` files it makes stale, in the same PR.
- The audit chain's canonical bytes never change: no field is added to `AuditEvent`.

## Slices and their PRs

| Slice | Branch | Delivers |
|---|---|---|
| 1 | `feat/ci-python-tests` | `build-and-test` runs the Python tests (D14) |
| 2 | `feat/otel-core-python` | `platform/core` observability package, guard, request log, registry spans, audit metrics, tests |
| 3 | `feat/otel-dev-stack` | `deploy/dev/` Collector + Grafana compose stack |
| 4 | `feat/otel-web-server` | Next.js server tracing, pino logs, OTLP relay, `traceparent` meta tag, vitest |
| 5 | `feat/otel-web-browser` | Browser tracing and RUM from `instrumentation-client.ts`, Playwright end-to-end trace test |

Slices 3, 4 and 5 depend on 2 only for the end-to-end check; each is independently reviewable.

## File map

```
.github/workflows/ci.yml                                   modify (slice 1, 4, 5)
platform/core/pyproject.toml                               modify (2)
platform/core/src/mulyankan_platform/observability/
  __init__.py                                              create (2) exports configure, register_providers
  guard.py                                                 create (2) allowlists, SpanAttributeGuard, LogAttributeGuard
  metrics.py                                               create (2) domain instruments, registry gauge
  logs.py                                                  create (2) JsonFormatter, configure_logging
  http.py                                                  create (2) RequestLogMiddleware, route_template
  providers.py                                             create (2) ObservedProvider
  setup.py                                                 create (2) register_providers, configure
platform/core/src/mulyankan_platform/registry.py           modify (2) get() returns ObservedProvider
platform/core/src/mulyankan_platform/audit/chain.py        modify (2) append() records metrics + span event
platform/core/src/mulyankan_platform/core_api/main.py      modify (2) build_app calls configure; log call convention
platform/core/tests/conftest.py                            modify (2) in-memory telemetry fixture
platform/core/tests/test_observability_*.py                create (2)
platform/core/AGENTS.md, platform/AGENTS.md, AGENTS.md     modify (2, 3)
docs/traceability.md                                       modify (2, 5)
deploy/dev/{compose.yaml,otel-collector.yaml,.env.example,README.md}   create (3)
apps/web/package.json, next.config.ts, vitest.config.ts    modify/create (4)
apps/web/src/instrumentation.ts, instrumentation.node.ts   create (4)
apps/web/src/observability/{allowlist,guard,logger}.ts     create (4)
apps/web/src/observability/guard.test.ts                   create (4)
apps/web/src/app/api/otlp/v1/[signal]/route.ts (+ test)    create (4)
apps/web/src/app/layout.tsx                                modify (4) traceparent meta
apps/web/src/instrumentation-client.ts                     create (5)
apps/web/src/observability/{actor,vitals,errors}.ts        create (5)
apps/web/playwright.config.ts, e2e/trace.spec.ts           create (5)
apps/web/AGENTS.md                                         modify (4, 5)
```

---

## Slice 1: CI runs the Python tests

### Task 1: Replace the `build-and-test` placeholder

Landing separately through upstream PR #96 (pip rather than uv; same job, same tests). The observability slices assume it is merged.

**Files:**
- Modify: `.github/workflows/ci.yml:193-208`

**Interfaces:**
- Produces: a CI job named `build-and-test` that fails when `python -m pytest platform/spi platform/core -q` fails. The `ci` aggregate job already depends on it.

- [ ] **Step 1: Confirm the tests pass locally before touching CI**

Run:
```bash
uv pip install -e platform/spi -e "platform/core[dev]"
python -m pytest platform/spi platform/core -q
```
Expected: all tests pass (M0 has 12).

- [ ] **Step 2: Replace the placeholder steps**

Replace the `Build` and `Test` steps (the two `echo` lines and their comment) with:

```yaml
      - name: Set up Python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: '3.12'

      - name: Set up uv
        uses: astral-sh/setup-uv@20cfd1bf945f4377ade1205e4dbc17946fc9a30d # v10.0.1

      # Editable installs of both packages, exactly as AGENTS.md documents for
      # local work. There is no Python lockfile yet; when one lands, switch to
      # `uv sync --frozen`.
      - name: Install Python packages
        run: uv pip install --system -e platform/spi -e "platform/core[dev]"

      - name: Run Python tests
        run: python -m pytest platform/spi platform/core -q
```

- [ ] **Step 3: Make the job fail on purpose, once**

Temporarily add `assert False` to `platform/core/tests/test_healthz.py`, push to the branch, confirm the `build-and-test` check is red and the `ci` check is red. Revert the assert, push, confirm green. This is the only way to prove the gate gates.

- [ ] **Step 4: Update the docs that call CI a placeholder**

In `AGENTS.md` (root), in the paragraph beginning "**CI's gate is the aggregate `ci` job**", replace the two sentences from "`build-and-test` is still the template's `echo` placeholder" to "a green PR proves nothing about them." with:

```markdown
`build-and-test` runs the Python test suite on 3.12.
```

so the paragraph continues with "`Dockerfile` is likewise a placeholder." unchanged.

In `CONTRIBUTING.md`, the "Security checks" list item `**web** / **build-and-test** — lint, types, build.` becomes:

```markdown
- **`web`** — lint, types, build. **`build-and-test`** — the Python test suite.
```

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml AGENTS.md CONTRIBUTING.md
git commit -s -m "Run the Python test suite in CI

build-and-test was the template echo placeholder, so a green PR proved
nothing about platform/. Pin setup-python and setup-uv by SHA."
```

---

## Slice 2: `platform/core` observability

### Task 2: Dependencies and the package skeleton

**Files:**
- Modify: `platform/core/pyproject.toml`
- Create: `platform/core/src/mulyankan_platform/observability/__init__.py`
- Create: `platform/core/src/mulyankan_platform/observability/setup.py`
- Test: `platform/core/tests/test_observability_disabled.py`

**Interfaces:**
- Produces: `mulyankan_platform.observability.configure(app: FastAPI, registry: ProviderRegistry | None = None) -> None`, a no-op when `OTEL_SDK_DISABLED=true`. Fully wired in Task 8.

- [x] **Step 1: Add the dependencies**

In `platform/core/pyproject.toml`, extend `dependencies`:

```toml
dependencies = [
    "mulyankan-spi",
    "fastapi>=0.115",
    "uvicorn>=0.30",
    "pyyaml>=6.0",
    # Observability (ADR-0011). Mandatory: the content-free guard is a
    # security control. API/SDK track 1.x; contrib instrumentations track
    # the 0.x line that pairs with it.
    "opentelemetry-api>=1.44,<2",
    "opentelemetry-sdk>=1.44,<2",
    "opentelemetry-exporter-otlp-proto-http>=1.44,<2",
    "opentelemetry-instrumentation-fastapi>=0.65b0,<1",
    "opentelemetry-instrumentation-system-metrics>=0.65b0,<1",
]
```

Run: `uv pip install -e "platform/core[dev]"` and then:
```bash
python -c "import opentelemetry.sdk, opentelemetry.instrumentation.fastapi; print('ok')"
```
Expected: `ok`.

- [x] **Step 2: Write the failing test**

`platform/core/tests/test_observability_disabled.py`:

```python
"""The SDK off switch: the app serves and nothing is registered (ASR02-OBS)."""

import subprocess
import sys
import textwrap

SCRIPT = textwrap.dedent(
    """
    import os
    os.environ["OTEL_SDK_DISABLED"] = "true"
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
        [sys.executable, "-c", SCRIPT], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stderr
    assert "served" in result.stdout
```

The test runs in a subprocess because the OTel global providers can be set once per process, and the rest of the suite sets them to in-memory exporters (Task 8).

- [x] **Step 3: Run it to see it fail**

Run: `python -m pytest platform/core/tests/test_observability_disabled.py -q`
Expected: FAIL. `create_app_from_mapping` does not call anything OTel yet, so the assertion on `ProxyTracerProvider` passes, but the import of `mulyankan_platform.observability` in the next step does not exist. To make the test meaningful now, add to the script before `TestClient`: `import mulyankan_platform.observability` so it fails with `ModuleNotFoundError`.

- [x] **Step 4: Create the package with a disabled-aware `configure`**

`platform/core/src/mulyankan_platform/observability/__init__.py`:

```python
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
```

`platform/core/src/mulyankan_platform/observability/setup.py` (first version; Task 8 completes it):

```python
"""SDK bootstrap: build providers from the OTel environment, instrument the app.

`register_providers` runs once per process. `configure` runs once per app and
is a no-op when `OTEL_SDK_DISABLED=true` (spec §4.1, principle 4).
"""

from __future__ import annotations

import os

from fastapi import FastAPI

from mulyankan_platform.registry import ProviderRegistry


def sdk_disabled() -> bool:
    return os.environ.get("OTEL_SDK_DISABLED", "").strip().lower() == "true"


def register_providers() -> None:
    """Completed in Task 8."""


def configure(app: FastAPI, registry: ProviderRegistry | None = None) -> None:
    """Instrument `app`; does nothing when the SDK is disabled."""
    if sdk_disabled():
        return
```

In `core_api/main.py`, `build_app` calls it after `app.state.registry = registry`:

```python
    app.state.registry = registry
    configure(app, registry)
```

with `from mulyankan_platform.observability import configure` added to the imports.

- [x] **Step 5: Run the test to see it pass**

Run: `python -m pytest platform/core -q`
Expected: all pass, including the existing healthz tests.

- [ ] **Step 6: Commit**

```bash
git add platform/core/pyproject.toml platform/core/src/mulyankan_platform/observability platform/core/src/mulyankan_platform/core_api/main.py platform/core/tests/test_observability_disabled.py
git commit -s -m "Add the observability package skeleton and OTel dependencies"
```

### Task 3: The content-free guard

**Files:**
- Create: `platform/core/src/mulyankan_platform/observability/guard.py`
- Test: `platform/core/tests/test_observability_guard.py`

**Interfaces:**
- Produces: `ALLOWED_SPAN_ATTRIBUTES: frozenset[str]`, `ALLOWED_LOG_ATTRIBUTES: frozenset[str]`, `ALLOWED_METRIC_ATTRIBUTES: frozenset[str]`, `frames_only(stacktrace: str) -> str`, `metric_views() -> list[View]`, `SpanAttributeGuard(dropped: Counter | None = None)` (a `SpanProcessor`), `LogAttributeGuard(dropped: Counter | None = None)` (a `LogRecordProcessor`). `dropped` is an OTel `Counter`; each removed key is counted with attributes `{"signal": "span" | "log", "attribute": key}`. Keys are filtered by name; `exception.stacktrace` is the one value that is also rewritten, because the SDK renders the exception message into it. Metric attributes are filtered by the SDK `View` from `metric_views()`, which drops silently (no counter).

- [x] **Step 1: Write the failing tests**

`platform/core/tests/test_observability_guard.py`:

```python
"""Attribute allowlist guard (ASR02-OBS): unknown keys never reach an exporter."""


from opentelemetry._logs import LogRecord, SeverityNumber
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import InMemoryLogRecordExporter, SimpleLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from mulyankan_platform.observability.guard import (
    ALLOWED_METRIC_ATTRIBUTES,
    ALLOWED_SPAN_ATTRIBUTES,
    LogAttributeGuard,
    SpanAttributeGuard,
    frames_only,
    metric_views,
)

SENTINEL = "SENTINEL-4f1c"


def _counter():
    reader = InMemoryMetricReader()
    meter = MeterProvider(metric_readers=[reader]).get_meter("test")
    return reader, meter.create_counter("mulyankan.observability.attributes_dropped")


def _dropped_keys(reader) -> set[str]:
    data = reader.get_metrics_data()
    keys = set()
    for rm in data.resource_metrics:
        for sm in rm.scope_metrics:
            for metric in sm.metrics:
                for point in metric.data.data_points:
                    keys.add(point.attributes["attribute"])
    return keys


def test_asr02obs_unknown_span_attributes_are_dropped_and_counted() -> None:
    reader, counter = _counter()
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SpanAttributeGuard(counter))
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test")

    with tracer.start_as_current_span("s") as span:
        span.set_attribute("http.route", "/items/{item_id}")
        span.set_attribute("url.query", f"q={SENTINEL}")
        try:
            raise ValueError(SENTINEL)
        except ValueError as exc:
            span.record_exception(exc)

    (exported,) = exporter.get_finished_spans()
    assert dict(exported.attributes) == {"http.route": "/items/{item_id}"}
    (event,) = exported.events
    assert set(event.attributes) == {"exception.type", "exception.stacktrace"}
    # record_exception renders `ValueError: <message>` into the stacktrace;
    # the guard keeps the frames and removes that line.
    assert "test_observability_guard.py" in event.attributes["exception.stacktrace"]
    assert SENTINEL not in str(dict(event.attributes))
    assert {"url.query", "exception.message", "exception.escaped"} <= _dropped_keys(reader)


def test_asr02obs_stacktrace_keeps_frames_and_drops_the_message() -> None:
    rendered = (
        "Traceback (most recent call last):\n"
        '  File "/app/x.py", line 10, in outer\n'
        "    inner()\n"
        '  File "/app/x.py", line 4, in inner\n'
        "    raise ValueError(msg)\n"
        f"ValueError: {SENTINEL}\n"
        f"  second line of the message {SENTINEL}\n"
        f"Note: {SENTINEL}\n"
    )
    kept = frames_only(rendered)
    assert SENTINEL not in kept
    assert kept.splitlines() == [
        '  File "/app/x.py", line 10, in outer',
        "    inner()",
        '  File "/app/x.py", line 4, in inner',
        "    raise ValueError(msg)",
    ]
    assert frames_only("") == ""


def test_asr02obs_unknown_log_attributes_are_dropped_and_counted() -> None:
    reader, counter = _counter()
    exporter = InMemoryLogRecordExporter()
    provider = LoggerProvider()
    provider.add_log_record_processor(LogAttributeGuard(counter))
    provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))

    # Through the logs API: the stdlib handler that maps `extra` to attributes
    # arrives with the structured-logs task, and the guard sits below it.
    provider.get_logger("guard-test").emit(
        LogRecord(
            body="draft.submitted",
            severity_number=SeverityNumber.INFO,
            attributes={"mulyankan.object_ref": "art-1", "stem": SENTINEL},
        )
    )

    (record,) = exporter.get_finished_logs()
    attributes = dict(record.log_record.attributes)
    assert attributes["mulyankan.object_ref"] == "art-1"
    assert "stem" not in attributes
    assert SENTINEL not in str(attributes)
    assert "stem" in _dropped_keys(reader)


def test_asr02obs_unknown_metric_attributes_are_dropped() -> None:
    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader], views=metric_views())
    counter = provider.get_meter("test").create_counter("mulyankan.audit.events")

    counter.add(1, {"action": "probe", "stem": SENTINEL})

    (rm,) = reader.get_metrics_data().resource_metrics
    (point,) = [p for sm in rm.scope_metrics for m in sm.metrics for p in m.data.data_points]
    assert dict(point.attributes) == {"action": "probe"}


def test_allowlist_never_admits_the_known_leaky_keys() -> None:
    for key in ("url.full", "url.path", "url.query", "user_agent.original",
                "exception.message", "enduser.id", "db.query.text"):
        assert key not in ALLOWED_SPAN_ATTRIBUTES
        assert key not in ALLOWED_METRIC_ATTRIBUTES
```

- [x] **Step 2: Run to see them fail**

Run: `python -m pytest platform/core/tests/test_observability_guard.py -q`
Expected: FAIL with `ModuleNotFoundError: mulyankan_platform.observability.guard`.

- [x] **Step 3: Implement the guard**

`platform/core/src/mulyankan_platform/observability/guard.py`:

```python
"""Content-free guard: attribute allowlists applied before export (ASR02-OBS).

The FastAPI and ASGI instrumentations emit `url.query`, `url.path`,
`user_agent.original` and `exception.message`, any of which can carry what a
user typed. The root invariant is that no question content reaches logs,
traces or metrics, so every attribute is removed unless it is listed here.
Removed keys are counted so a new attribute from an upgraded instrumentation
shows up in a metric rather than leaking silently.

Filtering is by key, with one exception: `exception.stacktrace`. The SDK's
`record_exception` renders the trace with `traceback.format_exception`, whose
last line is `ExceptionType: message`, so the value is rewritten to its frame
lines before export (`frames_only`). Metric attributes go through an SDK
`View` (`metric_views`) rather than a processor; a View drops silently, so
metric drops are not counted and the §7 sentinel test is the check.

This list is what an auditor reads: one entry per line, with the reason.
The Collector's redaction list mirrors the union of the three sets below
(`tests/test_dev_stack.py` pins that), and the web tier's allowlist will
mirror it when that slice lands.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from typing import Any

from opentelemetry.attributes import BoundedAttributes
from opentelemetry.metrics import Counter
from opentelemetry.sdk._logs import LogRecordProcessor
from opentelemetry.sdk.metrics.view import View
from opentelemetry.sdk.trace import Event, ReadableSpan, SpanProcessor
from opentelemetry.sdk.util import BoundedList
from opentelemetry.trace import Status

ALLOWED_SPAN_ATTRIBUTES: frozenset[str] = frozenset(
    {
        "http.request.method",  # the verb only
        "http.route",  # the template; the concrete path is dropped
        "http.response.status_code",
        "http.request.body.size",
        "http.response.body.size",
        "url.scheme",
        "server.address",
        "server.port",
        "network.protocol.version",
        "client.address",  # D10: operational security signal, not content
        "error.type",  # status class or exception class name
        "exception.type",
        "exception.stacktrace",  # frame lines only: frames_only() removes the message
        "enduser.pseudo.id",  # DAT-02 pseudonymous workforce id, never enduser.id
        "mulyankan.spi",
        "mulyankan.provider.name",
        "mulyankan.provider.version",
        "mulyankan.audit.event_id",
        "mulyankan.object_ref",  # opaque identifiers only
        "mulyankan.state.from",
        "mulyankan.state.to",
        "mulyankan.http.request.duration",  # seconds, request log only
        "db.system.name",  # M1
        "db.operation.name",  # M1
        "db.collection.name",  # M1; db.query.text is decided by D11
    }
)

ALLOWED_LOG_ATTRIBUTES: frozenset[str] = ALLOWED_SPAN_ATTRIBUTES | frozenset(
    {
        "code.function.name",
        "code.file.path",
        "code.line.number",
    }
)

# Metric data-point attributes (spec §3.2). Spelled out rather than derived
# from the span set: a View filters by key only and never sanitises a value,
# and every key here must be a bounded set (a metric label is a series).
# `exception.stacktrace`, `client.address`, `enduser.pseudo.id` and the
# `mulyankan.*` identifiers are therefore span-only.
ALLOWED_METRIC_ATTRIBUTES: frozenset[str] = frozenset(
    {
        # http.server.request.duration and the request/response body sizes
        "http.request.method",
        "http.route",
        "http.response.status_code",
        "url.scheme",
        "network.protocol.version",
        # server.address and server.port stay off metrics: the address is the
        # request's Host header, so a client would control the series count.
        "error.type",  # status class or exception class name
        # mulyankan.observability.attributes_dropped
        "signal",
        "attribute",  # a bounded key label, see `dropped_key_label`
        "action",  # mulyankan.audit.events
        "spi",  # mulyankan.registry.bindings
        "provider.name",  # mulyankan.registry.bindings
        "provider.version",  # mulyankan.registry.bindings
        "from_state",  # mulyankan.workflow.transitions (M1)
        "to_state",  # mulyankan.workflow.transitions (M1)
        "type",  # process.cpu.time: user | system
        "generation",  # cpython.gc.collections: 0 | 1 | 2
    }
)

# The log body is not an attribute, so the allowlist cannot see it. The
# rule (spec §4.4) is that a body is a static, dotted event name such as
# `draft.submitted`; anything else is an interpolated or free-text message
# and is replaced before export. Framework loggers (uvicorn) log constants
# about the process and pass through.
UNSTRUCTURED_EVENT = "log.unstructured"
_EVENT_NAME = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$")
_FRAMEWORK_LOGGERS = ("uvicorn",)


def event_name(body: object, logger_name: str) -> str:
    """The body to export: the event name itself, or the placeholder."""
    if not isinstance(body, str):
        return UNSTRUCTURED_EVENT
    if logger_name.split(".", 1)[0] in _FRAMEWORK_LOGGERS:
        return body
    return body if _EVENT_NAME.match(body) else UNSTRUCTURED_EVENT


# The `attribute` label of the dropped counter is a key NAME, but names are
# not always code-controlled: captured request headers become
# `http.request.header.<name>` keys, and a client picks the name. Bucket
# those by prefix, and cap the distinct labels this process will ever emit.
DROPPED_LABEL_LIMIT = 64
_BUCKETED_PREFIXES = ("http.request.header.", "http.response.header.")
_seen_dropped_keys: set[str] = set()


def dropped_key_label(key: str) -> str:
    for prefix in _BUCKETED_PREFIXES:
        if key.startswith(prefix):
            return prefix + "*"
    if key in _seen_dropped_keys:
        return key
    if len(_seen_dropped_keys) >= DROPPED_LABEL_LIMIT:
        return "other"
    _seen_dropped_keys.add(key)
    return key


# A rendered traceback is one or more sections, each `Traceback (most recent
# call last):`, then frames (`  File "<path>", line <n>, in <name>` plus
# indented source and caret lines), then the `Type: message` line and any
# notes. Frames are only read while a section's header has armed them and
# the first non-frame line (the message) disarms until the next header, so
# a message that itself contains a File-shaped line cannot smuggle its
# following lines through. Header-less input (`traceback.format_tb`) arms
# from the start.
_HEADER_LINE = "Traceback (most recent call last):"
_FRAME_LINE = re.compile(r'^\s+File ".*", line \d+, in .*$')


def frames_only(stacktrace: str) -> str:
    """Reduce a `traceback.format_exception` rendering to its frame lines."""
    kept: list[str] = []
    lines = stacktrace.splitlines()
    armed = bool(lines) and _FRAME_LINE.match(lines[0]) is not None
    in_frame = False
    for line in lines:
        if line == _HEADER_LINE:
            armed, in_frame = True, False
        elif not armed:
            continue
        elif _FRAME_LINE.match(line):
            in_frame = True
            kept.append(line)
        elif in_frame and line.startswith("    "):
            kept.append(line)
        else:
            armed, in_frame = False, False  # the message line ends the section
    return "\n".join(kept)


_SANITISERS: dict[str, Callable[[Any], Any]] = {
    "exception.stacktrace": lambda v: frames_only(v) if isinstance(v, str) else "",
}


def metric_views() -> list[View]:
    """One View matching every instrument: the SDK drops unlisted keys at
    aggregation time, before any reader sees them."""
    return [View(instrument_name="*", attribute_keys=set(ALLOWED_METRIC_ATTRIBUTES))]


def filter_attributes(
    attributes: Mapping[str, Any] | None,
    allowed: frozenset[str],
    dropped: Counter | None,
    signal: str,
) -> dict[str, Any]:
    kept: dict[str, Any] = {}
    for key, value in (attributes or {}).items():
        if key in allowed:
            sanitise = _SANITISERS.get(key)
            kept[key] = sanitise(value) if sanitise else value
        elif dropped is not None:
            dropped.add(1, {"signal": signal, "attribute": dropped_key_label(key)})
    return kept


def _rebound(old: Any, kept: dict[str, Any]) -> Any:
    """Keep the SDK's limit bookkeeping: a plain dict would report zero
    dropped attributes and hide that a span or log limit is cutting data."""
    if not isinstance(old, BoundedAttributes):
        return kept
    new = BoundedAttributes(
        maxlen=old.maxlen,
        attributes=kept,
        immutable=True,
        max_value_len=old.max_value_len,
    )
    new.dropped = old.dropped
    return new


class SpanAttributeGuard(SpanProcessor):
    """Strips unlisted attributes from a span and its events at end time.

    `ReadableSpan` has no setter; the SDK keeps attributes in `_attributes`
    and events in `_events`, and exporters read both after `on_end`. The
    guard test pins this so an SDK upgrade cannot reopen the leak unnoticed.
    Register this processor before the exporting processor.
    """

    def __init__(self, dropped: Counter | None = None) -> None:
        self._dropped = dropped

    def on_start(self, span, parent_context=None) -> None:
        return None

    def on_end(self, span: ReadableSpan) -> None:
        span._attributes = _rebound(
            span._attributes,
            filter_attributes(
                span.attributes, ALLOWED_SPAN_ATTRIBUTES, self._dropped, "span"
            ),
        )
        old_events = span._events
        events = BoundedList(
            old_events._dq.maxlen if isinstance(old_events, BoundedList) else None
        )
        for event in span.events:
            events.append(
                Event(
                    event.name,
                    filter_attributes(
                        event.attributes, ALLOWED_SPAN_ATTRIBUTES, self._dropped, "span"
                    ),
                    event.timestamp,
                )
            )
        events.dropped = getattr(old_events, "dropped", 0)
        span._events = events
        # The SDK renders the escaped exception as `Type: message` into the
        # status description; the OTLP encoder exports it as Status.message.
        if span.status.description:
            span._status = Status(span.status.status_code)

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


class LogAttributeGuard(LogRecordProcessor):
    """Strips unlisted attributes from a log record before export."""

    def __init__(self, dropped: Counter | None = None) -> None:
        self._dropped = dropped

    def on_emit(self, record) -> None:
        # SDK >= 1.44 hands the processor a ReadWriteLogRecord wrapping the
        # API LogRecord; the attributes live on the inner record.
        inner = record.log_record
        inner.attributes = _rebound(
            inner.attributes,
            filter_attributes(
                inner.attributes, ALLOWED_LOG_ATTRIBUTES, self._dropped, "log"
            ),
        )
        scope = record.instrumentation_scope
        exported = event_name(inner.body, scope.name if scope else "")
        if exported != inner.body:
            inner.body = exported
            if self._dropped is not None:
                self._dropped.add(1, {"signal": "log", "attribute": "body"})

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True
```

- [x] **Step 4: Run to see them pass**

Run: `python -m pytest platform/core/tests/test_observability_guard.py -q`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add platform/core/src/mulyankan_platform/observability/guard.py platform/core/tests/test_observability_guard.py
git commit -s -m "Add the content-free attribute guard for spans and logs"
```

### Task 4: Domain instruments and the audit chain

**Files:**
- Create: `platform/core/src/mulyankan_platform/observability/metrics.py`
- Modify: `platform/core/src/mulyankan_platform/audit/chain.py` (only `AuditLog.append`)
- Test: `platform/core/tests/test_observability_audit.py`

**Interfaces:**
- Produces: module-level instruments `audit_events` (Counter), `audit_append_duration` (Histogram, seconds), `attributes_dropped` (Counter), and `observe_registry_bindings(registry: ProviderRegistry) -> None`.
- `AuditLog.append` adds a span event `audit.appended` with `mulyankan.audit.event_id` on the current span and records the two audit instruments.

- [x] **Step 1: Write the failing test**

`platform/core/tests/test_observability_audit.py`:

```python
"""Audit chain emits metrics and links the span to the event id (ASR02-OBS)."""

from mulyankan_platform.audit import AuditLog
from opentelemetry import trace


def _metric_points(telemetry, name):
    data = telemetry.metric_reader.get_metrics_data()
    for rm in data.resource_metrics:
        for sm in rm.scope_metrics:
            for metric in sm.metrics:
                if metric.name == name:
                    return list(metric.data.data_points)
    return []


def test_asr02obs_audit_append_records_metrics_and_span_link(telemetry) -> None:
    tracer = trace.get_tracer("test")
    log = AuditLog()
    with tracer.start_as_current_span("request"):
        event = log.append(
            actor="author-001",
            action="draft.created",
            object_refs=("artefact-a1",),
            payload={"stem": "x"},
        )

    (span,) = telemetry.spans()
    (audit_event,) = [e for e in span.events if e.name == "audit.appended"]
    assert audit_event.attributes["mulyankan.audit.event_id"] == event.event_id
    assert log.verify().ok  # nothing telemetry-related touched the chain

    # The reader is cumulative for the whole session, so assert on this
    # action's point and on lower bounds rather than exact totals.
    (count,) = [
        p
        for p in _metric_points(telemetry, "mulyankan.audit.events")
        if p.attributes == {"action": "draft.created"}
    ]
    assert count.value >= 1
    (duration,) = _metric_points(telemetry, "mulyankan.audit.append.duration")
    assert duration.count >= 1


def test_registry_bindings_gauge_reports_each_binding(telemetry) -> None:
    from mulyankan_platform.observability.metrics import observe_registry_bindings
    from mulyankan_platform.registry import ProviderRegistry

    mapping = {
        "providers": {
            "kms": {"provider": "testkit_fake_provider:FakeKms", "config": {}}
        }
    }
    registry = ProviderRegistry.from_mapping(mapping)  # held weakly by the gauge
    observe_registry_bindings(registry)
    points = _metric_points(telemetry, "mulyankan.registry.bindings")
    assert {
        "spi": "kms",
        "provider.name": "fake-kms",
        "provider.version": "1.0.0",
    } in [dict(p.attributes) for p in points]
```

`telemetry` is the fixture from Task 8. Until then this test errors on the missing fixture; write it now, run it in Task 8.

- [x] **Step 2: Implement the instruments**

`platform/core/src/mulyankan_platform/observability/metrics.py`:

```python
"""Domain instruments (spec §3.2). Names are `mulyankan.*`; attributes are
low-cardinality and content-free. Instruments are created on the API's
global meter, so they bind to whichever provider `register_providers`
installs, the in-memory one in tests included.
"""

from __future__ import annotations

import weakref
from collections.abc import Iterable
from typing import TYPE_CHECKING

from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation

if TYPE_CHECKING:  # registry imports this package; keep the edge type-only
    from mulyankan_platform.registry import ProviderRegistry

_meter = metrics.get_meter("mulyankan_platform.observability")

attributes_dropped = _meter.create_counter(
    "mulyankan.observability.attributes_dropped",
    unit="1",
    description="Attributes removed by the content-free guard, by signal and key",
)
audit_events = _meter.create_counter(
    "mulyankan.audit.events", unit="{event}", description="Audit events appended"
)
audit_append_duration = _meter.create_histogram(
    "mulyankan.audit.append.duration",
    unit="s",
    description="Time to append one audit event",
)

_registries: weakref.WeakSet[ProviderRegistry] = weakref.WeakSet()


def _bindings(options: CallbackOptions) -> Iterable[Observation]:
    for registry in list(_registries):
        for spi, info in registry.describe().items():
            descriptor = info.get("descriptor") or {}
            yield Observation(
                1,
                {
                    "spi": spi,
                    "provider.name": descriptor.get("name", info["provider"]),
                    "provider.version": descriptor.get("version", ""),
                },
            )


_meter.create_observable_gauge(
    "mulyankan.registry.bindings",
    callbacks=[_bindings],
    unit="{binding}",
    description="Provider bindings the registry resolved",
)


def observe_registry_bindings(registry: ProviderRegistry) -> None:
    """Include `registry` in the bindings gauge."""
    _registries.add(registry)
```

- [x] **Step 3: Instrument `AuditLog.append`**

In `audit/chain.py`, add imports:

```python
import time

from opentelemetry import trace

from mulyankan_platform.observability.metrics import audit_append_duration, audit_events
```

and change `append` so the body is timed and the event linked. The hashing and canonical code is untouched:

```python
    ) -> AuditEvent:
        """Append one event; `payload` is hashed and immediately discarded."""
        started = time.perf_counter()
        if payload is None:
            payload_hash = ""
        else:
            payload_hash = hashlib.sha256(canonical_bytes(payload)).hexdigest()
        prev_hash = self._events[-1].hash if self._events else GENESIS_HASH
        moment = ts or datetime.now(timezone.utc)
        event = AuditEvent(
            event_id=event_id or uuid.uuid4().hex,
            seq=len(self._events),
            ts=moment.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            actor=actor,
            action=action,
            object_refs=tuple(object_refs),
            payload_hash=payload_hash,
            prev_hash=prev_hash,
            hash="",
        )
        event = replace(event, hash=compute_hash(event))
        self._events.append(event)
        # Observability (ASR02-OBS): the link runs span -> event id, never the
        # reverse, so the canonical bytes above stay untouched.
        audit_append_duration.record(time.perf_counter() - started)
        audit_events.add(1, {"action": action})
        trace.get_current_span().add_event(
            "audit.appended", {"mulyankan.audit.event_id": event.event_id}
        )
        return event
```

Add to the module docstring's invariants list: `- Observability links point at events (span event carrying the event id); no telemetry field is ever stored on an event.`

- [x] **Step 4: Run the existing audit tests**

Run: `python -m pytest platform/core/tests/test_audit_chain.py -q`
Expected: 5 passed. Hashes are unchanged because no field was added.

- [ ] **Step 5: Commit**

```bash
git add platform/core/src/mulyankan_platform/observability/metrics.py platform/core/src/mulyankan_platform/audit/chain.py platform/core/tests/test_observability_audit.py
git commit -s -m "Record audit metrics and link spans to audit event ids"
```

### Task 5: Structured logs

This task adds `opentelemetry-instrumentation-logging` to `platform/core`'s
dependencies (its `LoggingHandler` maps `extra` to attributes) and owns the
log body rule (spec §4.4): `guard.event_name` accepts a dotted event name
and replaces anything else with `log.unstructured`, on both the OTLP path and
the stdout formatter; the sentinel test gains a log call whose message
interpolates the sentinel.

**Files:**
- Create: `platform/core/src/mulyankan_platform/observability/logs.py`
- Test: `platform/core/tests/test_observability_logs.py`

**Interfaces:**
- Produces: `JsonFormatter` (a `logging.Formatter`), `configure_logging(logger_provider) -> None` (idempotent; installs a stdout JSON handler and the OTel `LoggingHandler` on the root logger, disables `uvicorn.access`), and in `guard.py` `event_name(body, logger_name) -> str` plus `UNSTRUCTURED_EVENT`, applied by `LogAttributeGuard.on_emit` and the formatter.

- [x] **Step 1: Write the failing test**

`platform/core/tests/test_observability_logs.py`:

```python
"""JSON log lines and the log-body rule (ASR02-OBS): a static event name,
allowlisted fields and trace ids, with no interpolated value."""

import json
import logging
import sys

from mulyankan_platform.observability.guard import UNSTRUCTURED_EVENT, event_name
from mulyankan_platform.observability.logs import JsonFormatter, configure_logging
from opentelemetry.instrumentation.logging.handler import LoggingHandler
from opentelemetry import trace

SENTINEL = "SENTINEL-9a2e"


def _line(record_kwargs, msg="draft.submitted", args=(), name="demo") -> dict:
    record = logging.LogRecord(
        name=name,
        level=logging.INFO,
        pathname="x.py",
        lineno=1,
        msg=msg,
        args=args,
        exc_info=None,
    )
    for key, value in record_kwargs.items():
        setattr(record, key, value)
    return json.loads(JsonFormatter().format(record))


def test_json_line_carries_event_and_allowlisted_fields_only() -> None:
    line = _line({"mulyankan.object_ref": "art-1", "stem": SENTINEL})
    assert line["event"] == "draft.submitted"
    assert line["level"] == "INFO"
    assert line["mulyankan.object_ref"] == "art-1"
    assert "stem" not in line
    assert SENTINEL not in json.dumps(line)


def test_json_line_carries_trace_ids_inside_a_span(telemetry) -> None:
    tracer = trace.get_tracer("test")
    with tracer.start_as_current_span("s") as span:
        line = _line({})
        ctx = span.get_span_context()
    assert line["trace_id"] == format(ctx.trace_id, "032x")
    assert line["span_id"] == format(ctx.span_id, "016x")


def test_json_line_reports_exception_type_and_stack_without_message() -> None:
    try:
        raise ValueError(SENTINEL)
    except ValueError:
        record = logging.LogRecord(
            "demo", logging.ERROR, "x.py", 1, "op.failed", (), sys.exc_info()
        )
    line = json.loads(JsonFormatter().format(record))
    assert line["exception.type"] == "ValueError"
    assert "test_observability_logs.py" in line["exception.stacktrace"]
    assert SENTINEL not in json.dumps(line)


def test_asr02obs_body_must_be_an_event_name() -> None:
    assert event_name("draft.submitted", "demo") == "draft.submitted"
    assert (
        event_name("platform.config.missing", "mulyankan_platform.core_api.main")
        == "platform.config.missing"
    )
    # Interpolated or free-text messages are replaced before export.
    assert event_name(f"config {SENTINEL} missing", "demo") == UNSTRUCTURED_EVENT
    assert event_name("Draft submitted", "demo") == UNSTRUCTURED_EVENT
    assert event_name("", "demo") == UNSTRUCTURED_EVENT
    # Framework loggers log constants and pass through.
    assert (
        event_name("Application startup complete.", "uvicorn.error")
        == "Application startup complete."
    )


def test_json_line_replaces_an_interpolated_message_and_drops_args() -> None:
    line = _line({}, msg=f"config {SENTINEL} missing")
    assert line["event"] == UNSTRUCTURED_EVENT
    assert SENTINEL not in json.dumps(line)
    line = _line({}, msg="config %s missing", args=(SENTINEL,))
    assert line["event"] == UNSTRUCTURED_EVENT
    assert SENTINEL not in json.dumps(line)


def test_configure_logging_is_idempotent(telemetry) -> None:
    from mulyankan_platform.observability.setup import register_providers

    root = logging.getLogger()
    before = list(root.handlers)
    configure_logging(register_providers().logger_provider)
    configure_logging(register_providers().logger_provider)
    assert root.handlers == before
    assert sum(isinstance(h, LoggingHandler) for h in root.handlers) == 1
    assert sum(isinstance(h.formatter, JsonFormatter) for h in root.handlers) == 1
    assert logging.getLogger("uvicorn.access").disabled
    # uvicorn's loggers reach the root handlers instead of their own plain ones
    assert logging.getLogger("uvicorn.error").propagate
    assert not logging.getLogger("uvicorn.error").handlers


def test_a_stray_format_argument_neither_raises_nor_exports(telemetry, capsys) -> None:
    """`logger.info("event", value)` is the slip the convention invites: the
    OTel handler renders the message too, so both handlers must see a
    sanitised record instead of raising TypeError into the caller."""
    logging.getLogger("slip").info("draft.submitted", SENTINEL)
    (record,) = [r for r in telemetry.logs() if r.body == UNSTRUCTURED_EVENT]
    assert SENTINEL not in json.dumps(dict(record.attributes or {}))
    out = capsys.readouterr().out
    assert '"event": "log.unstructured"' in out
    assert SENTINEL not in out
```

- [x] **Step 2: Run to see it fail**

Run: `python -m pytest platform/core/tests/test_observability_logs.py -q`
Expected: FAIL with `ModuleNotFoundError`.

- [x] **Step 3: Implement**

`platform/core/src/mulyankan_platform/observability/logs.py`:

```python
"""Structured logging on the standard library (D19, spec §4.4).

Calling convention: the message is a static, dotted event name and every
value goes in `extra` under an allowlisted key:

    logger.info("draft.submitted", extra={"mulyankan.object_ref": ref})

Two handlers on the root logger: JSON to stdout for file-based collection,
and the OTel handler to OTLP. A filter on both rewrites the record once so
that the body rule (`guard.event_name`) holds on each path and a stray
format argument can neither raise nor leak; the OTel path is guarded again
by `LogAttributeGuard`.
"""

from __future__ import annotations

import json
import logging
import sys
import traceback
from datetime import UTC, datetime
from typing import Any

from opentelemetry import trace
from opentelemetry.instrumentation.logging.handler import LoggingHandler
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.trace import format_span_id, format_trace_id

from mulyankan_platform.observability.guard import (
    ALLOWED_LOG_ATTRIBUTES,
    UNSTRUCTURED_EVENT,
    event_name,
)


class EventNameFilter(logging.Filter):
    """Rewrite the record's message to the exported body, once, before any
    handler renders it. `record.getMessage()` is what the OTel handler
    exports and it raises on a `%` mismatch, so the arguments are consumed
    here and the message becomes the event name or the placeholder."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            rendered = record.getMessage()
        except (TypeError, ValueError):  # an event name given %-args
            rendered = None
        record.msg = UNSTRUCTURED_EVENT if rendered is None else event_name(rendered, record.name)
        record.args = ()
        return True


class JsonFormatter(logging.Formatter):
    """One JSON object per line, with no message value and no traceback
    message line."""

    def format(self, record: logging.LogRecord) -> str:
        line: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, UTC)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "event": event_name(record.getMessage(), record.name),
        }
        ctx = trace.get_current_span().get_span_context()
        if ctx.is_valid:
            line["trace_id"] = format_trace_id(ctx.trace_id)
            line["span_id"] = format_span_id(ctx.span_id)
        for key, value in record.__dict__.items():
            if key in ALLOWED_LOG_ATTRIBUTES:
                line[key] = value
        if record.exc_info and record.exc_info[0] is not None:
            line["exception.type"] = record.exc_info[0].__name__
            # format_tb renders frames only; the exception message is not part of it.
            line["exception.stacktrace"] = "".join(traceback.format_tb(record.exc_info[2]))
        return json.dumps(line, ensure_ascii=False, default=str)


class _StdoutHandler(logging.StreamHandler):
    """Resolves sys.stdout at emit time so test capture and redirection work."""

    def __init__(self) -> None:
        super().__init__(sys.stdout)

    @property
    def stream(self) -> Any:
        return sys.stdout

    @stream.setter
    def stream(self, value: Any) -> None:
        pass


def configure_logging(logger_provider: LoggerProvider | None) -> None:
    """Install the two root handlers once; safe to call again.

    With `logger_provider=None` (the SDK is off) the OTel handler binds to
    the API's no-op provider, so stdout still gets JSON and nothing exports.
    """
    root = logging.getLogger()
    if any(isinstance(h, LoggingHandler) for h in root.handlers):
        return
    stdout = _StdoutHandler()
    stdout.setFormatter(JsonFormatter())
    otel = LoggingHandler(logger_provider=logger_provider)
    for handler in (stdout, otel):
        handler.addFilter(EventNameFilter())
        root.addHandler(handler)
    root.setLevel(logging.INFO)
    # uvicorn installs its own plain-text handlers and stops propagation;
    # route its loggers through the root so they are JSON on stdout and
    # reach OTLP like everything else.
    for name in ("uvicorn", "uvicorn.error"):
        framework = logging.getLogger(name)
        framework.handlers.clear()
        framework.propagate = True
    # The request log middleware replaces uvicorn's access line, which prints
    # the raw path and query string (`--no-access-log` is then redundant).
    logging.getLogger("uvicorn.access").disabled = True
```

- [x] **Step 4: Run to see the first and third tests pass**

Run: `python -m pytest platform/core/tests/test_observability_logs.py -q`
Expected: 6 passed (the fixture from Task 8 already exists).

- [ ] **Step 5: Commit**

```bash
git add platform/core/src/mulyankan_platform/observability/logs.py platform/core/tests/test_observability_logs.py
git commit -s -m "Add JSON structured logging with trace correlation"
```

### Task 6: Request and response logging middleware

**Files:**
- Create: `platform/core/src/mulyankan_platform/observability/http.py`
- Test: `platform/core/tests/test_observability_http.py`

**Interfaces:**
- Produces: `RequestLogMiddleware` (pure ASGI, constructor `(app)`), `route_template(scope) -> str | None`.
- Consumes: nothing from OTel beyond `trace.get_current_span()`.

- [x] **Step 1: Write the failing test**

`platform/core/tests/test_observability_http.py`:

```python
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


def test_request_log_route_matches_the_span_for_included_and_partial_routes(caplog) -> None:
    """The line must join to the span and the metric by route, so it uses the
    instrumentation's own resolution: included routers and 405s included."""
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app())
    assert client.post(f"/nested/{SENTINEL}").status_code == 200
    assert client.get("/nested/1").status_code == 405  # a partial match
    routes = [line["http.route"] for line in _request_lines(caplog)]
    assert routes == ["/nested/{x}", "/nested/{x}"]
    assert SENTINEL not in json.dumps(_request_lines(caplog), default=str)


def test_request_log_survives_a_bad_content_length_and_a_headerless_response(caplog) -> None:
    caplog.set_level(logging.INFO, logger=LOGGER)
    client = TestClient(_app())
    assert client.get("/items/1", headers={"content-length": "abc"}).status_code == 200
    assert client.get("/raw/x").status_code == 200
    lines = _request_lines(caplog)
    assert [line["http.response.status_code"] for line in lines] == [200, 200]
    assert "http.request.body.size" not in lines[0]  # unparseable: omitted
```

The `Server-Timing` header needs the server span the OTel middleware creates, so it is asserted in Task 8's pipeline test rather than here.

- [x] **Step 2: Run to see it fail**

Run: `python -m pytest platform/core/tests/test_observability_http.py -q`
Expected: FAIL with `ModuleNotFoundError`.

- [x] **Step 3: Implement**

`platform/core/src/mulyankan_platform/observability/http.py`:

```python
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
        "OTEL_PYTHON_FASTAPI_EXCLUDED_URLS", os.environ.get("OTEL_PYTHON_EXCLUDED_URLS", "")
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
                "mulyankan.http.request.duration": round(time.perf_counter() - started, 6),
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
```

- [x] **Step 4: Run to see them pass**

Run: `python -m pytest platform/core/tests/test_observability_http.py -q`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add platform/core/src/mulyankan_platform/observability/http.py platform/core/tests/test_observability_http.py
git commit -s -m "Log one content-free line per request with the trace id"
```

### Task 7: Provider-call spans at the registry

**Files:**
- Create: `platform/core/src/mulyankan_platform/observability/providers.py`
- Modify: `platform/core/src/mulyankan_platform/registry.py` (`get`)
- Test: `platform/core/tests/test_observability_providers.py`

**Interfaces:**
- Produces: `ObservedProvider(spi: str, instance: Any)`; every public callable of `instance` is wrapped in a span named `<spi>.<method>` with `mulyankan.spi`, `mulyankan.provider.name`, `mulyankan.provider.version`. Wrapping is eager (instance attributes), so `isinstance(proxy, KmsProvider)` still holds under Python 3.12's static protocol check.
- `ProviderRegistry.get(spi)` returns an `ObservedProvider`.

- [x] **Step 1: Write the failing test**

`platform/core/tests/test_observability_providers.py`:

```python
"""Every provider call is a content-free span (ASR02-OBS, ADR-0003 rule 2)."""

import asyncio
import sys
import types

import pytest
from mulyankan_platform.observability.metrics import observe_registry_bindings
from mulyankan_platform.registry import ProviderRegistry
from mulyankan_spi.descriptor import ProviderDescriptor
from mulyankan_spi.kms import KmsProvider

SENTINEL = b"SENTINEL-c3d1"
MAPPING = {
    "providers": {"kms": {"provider": "testkit_fake_provider:FakeKms", "config": {}}}
}


def test_asr02obs_provider_calls_are_spanned_content_free(telemetry) -> None:
    kms = ProviderRegistry.from_mapping(MAPPING).get("kms")
    assert isinstance(kms, KmsProvider)

    ciphertext = kms.encrypt("dev-key-1", SENTINEL)
    assert kms.decrypt("dev-key-1", ciphertext) == SENTINEL

    names = [s.name for s in telemetry.spans()]
    assert names == ["kms.encrypt", "kms.decrypt"]
    for span in telemetry.spans():
        assert dict(span.attributes) == {
            "mulyankan.spi": "kms",
            "mulyankan.provider.name": "fake-kms",
            "mulyankan.provider.version": "1.0.0",
        }
    assert SENTINEL.decode() not in telemetry.dump()


def test_provider_exceptions_propagate_and_are_recorded_without_message(
    telemetry,
) -> None:
    kms = ProviderRegistry.from_mapping(MAPPING).get("kms")
    with pytest.raises(TypeError):
        kms.encrypt("dev-key-1", None)  # FakeKms concatenates bytes; None raises
    (span,) = telemetry.spans()
    (event,) = [e for e in span.events if e.name == "exception"]
    assert "exception.message" not in event.attributes
    assert not span.status.description


class _Probe:
    """A provider with the shapes a real one has and FakeKms does not."""

    describe_calls = 0

    class Error(Exception):
        pass

    def __init__(self, config: dict) -> None:
        self.config = config

    @property
    def client(self):  # a lazy connection: touching it is a side effect
        raise RuntimeError("property evaluated")

    def describe(self) -> ProviderDescriptor:
        type(self).describe_calls += 1
        return ProviderDescriptor(
            name="probe", version="2.0", deterministic=True, data_handling="test"
        )

    def sync_call(self, x):
        return x

    async def async_call(self, x):
        await asyncio.sleep(0.01)
        raise self.Error(x)


class _NoDescribe:
    def __init__(self, config: dict) -> None:
        pass

    def call(self):
        return 1


def _register_probe_module():
    module = types.ModuleType("probe_provider")
    module.Probe = _Probe
    module.NoDescribe = _NoDescribe
    sys.modules["probe_provider"] = module


def test_observed_provider_forwards_attributes_and_wraps_once(telemetry) -> None:
    _register_probe_module()
    registry = ProviderRegistry.from_mapping(
        {
            "providers": {
                "probe": {"provider": "probe_provider:Probe", "config": {"k": 1}}
            }
        }
    )
    before = _Probe.describe_calls
    first, second = registry.get("probe"), registry.get("probe")
    assert first is second  # wrapped once per binding
    assert _Probe.describe_calls == before  # the descriptor was resolved at bind time
    assert first.config == {"k": 1}  # plain attributes forward
    assert first.Error is _Probe.Error  # a nested class is still a class
    with pytest.raises(RuntimeError, match="property evaluated"):
        first.client  # a property is evaluated only when read
    assert [s.name for s in telemetry.spans()] == []  # and none of that made a span


def test_observed_provider_spans_cover_an_async_method(telemetry) -> None:
    _register_probe_module()
    registry = ProviderRegistry.from_mapping(
        {"providers": {"probe": {"provider": "probe_provider:Probe", "config": {}}}}
    )
    probe = registry.get("probe")
    with pytest.raises(_Probe.Error):
        asyncio.run(probe.async_call(SENTINEL))
    (span,) = [s for s in telemetry.spans() if s.name == "probe.async_call"]
    assert (
        span.end_time - span.start_time >= 10_000_000
    )  # the await ran inside the span
    assert any(e.name == "exception" for e in span.events)
    assert SENTINEL.decode() not in telemetry.dump()


def test_span_and_gauge_agree_on_the_provider_name(telemetry) -> None:
    _register_probe_module()
    registry = ProviderRegistry.from_mapping(
        {"providers": {"nd": {"provider": "probe_provider:NoDescribe", "config": {}}}}
    )
    observe_registry_bindings(registry)
    registry.get("nd").call()
    (span,) = [s for s in telemetry.spans() if s.name == "nd.call"]
    points = [
        dict(p.attributes)
        for rm in telemetry.metric_reader.get_metrics_data().resource_metrics
        for sm in rm.scope_metrics
        for m in sm.metrics
        if m.name == "mulyankan.registry.bindings"
        for p in m.data.data_points
        if p.attributes.get("spi") == "nd"
    ]
    assert (
        points
        and points[0]["provider.name"] == span.attributes["mulyankan.provider.name"]
    )
```

- [x] **Step 2: Run to see it fail**

Run: `python -m pytest platform/core/tests/test_observability_providers.py -q`
Expected: FAIL (`ModuleNotFoundError` once the fixture exists; until Task 8, fixture error).

- [x] **Step 3: Implement the proxy**

`platform/core/src/mulyankan_platform/observability/providers.py`:

```python
"""Provider-call spans (spec §4.5). The registry is the only path to a
provider, so wrapping here makes every interaction visible and content-free:
arguments and return values are not recorded, which matters most for the kms
SPI, which handles plaintext.
"""

from __future__ import annotations

import functools
import inspect
from typing import Any

from opentelemetry import trace

_tracer = trace.get_tracer("mulyankan_platform.registry")


class ObservedProvider:
    """Wraps every public method of `instance` in a span; forwards the rest.

    Methods are found statically (`inspect.getattr_static`) so a property is
    not evaluated and a nested class is not rebound, and they are bound as
    instance attributes eagerly because Python 3.12's `isinstance` against a
    runtime-checkable Protocol uses `getattr_static`, which ignores
    `__getattr__`. Everything else, attributes and properties included, is
    forwarded on read. Built once per binding by the registry.
    """

    def __init__(self, spi: str, instance: Any, descriptor: dict | None, target: str) -> None:
        self._spi = spi
        self._instance = instance
        descriptor = descriptor or {}
        self._attributes = {
            "mulyankan.spi": spi,
            "mulyankan.provider.name": descriptor.get("name", target),
            "mulyankan.provider.version": descriptor.get("version", ""),
        }
        for name in dir(instance):
            if name.startswith("_"):
                continue
            static = inspect.getattr_static(instance, name, None)
            if isinstance(static, (staticmethod, classmethod)):
                static = static.__func__
            if inspect.isfunction(static) or inspect.ismethoddescriptor(static):
                setattr(self, name, self._observed(name, getattr(instance, name)))

    def __getattr__(self, name: str) -> Any:
        return getattr(self._instance, name)

    def _observed(self, name: str, method: Any) -> Any:
        span_name = f"{self._spi}.{name}"

        if inspect.iscoroutinefunction(method):

            @functools.wraps(method)
            async def observed_async(*args: Any, **kwargs: Any) -> Any:
                with _tracer.start_as_current_span(span_name, attributes=self._attributes):
                    return await method(*args, **kwargs)

            return observed_async

        @functools.wraps(method)
        def observed(*args: Any, **kwargs: Any) -> Any:
            with _tracer.start_as_current_span(span_name, attributes=self._attributes):
                return method(*args, **kwargs)

        return observed
```

In `registry.py`, `get` becomes:

```python
    def get(self, spi: str) -> Any:
        """Return the bound provider for `spi`, wrapped for observability;
        refuse unbound capabilities."""
        binding = self._bindings.get(spi)
        if binding is None:
            raise RegistryError(f"no provider bound for spi '{spi}'")
        return binding.observed  # wrapped once, at bind time, with its descriptor
```

with `from mulyankan_platform.observability.providers import ObservedProvider` imported at module top. `registry.py` now imports the observability package, so nothing in that package may import `registry` at runtime: `metrics.py` (Task 4) and `setup.py` (Task 8) import `ProviderRegistry` under `TYPE_CHECKING` only.

- [x] **Step 4: Run the registry tests**

Run: `python -m pytest platform/core/tests/test_registry.py -q`
Expected: 5 passed, including `isinstance(provider, KmsProvider)`.

- [ ] **Step 5: Commit**

```bash
git add platform/core/src/mulyankan_platform/observability/providers.py platform/core/src/mulyankan_platform/observability/metrics.py platform/core/src/mulyankan_platform/registry.py platform/core/tests/test_observability_providers.py
git commit -s -m "Span every provider call at the registry boundary"
```

### Task 8: Wire the SDK, the fixture, and the sentinel test

**Files:**
- Modify: `platform/core/src/mulyankan_platform/observability/setup.py`
- Modify: `platform/core/tests/conftest.py`
- Modify: `platform/core/src/mulyankan_platform/core_api/main.py` (the warning call)
- Test: `platform/core/tests/test_observability_pipeline.py`

**Interfaces:**
- Produces: `register_providers(*, span_exporter=None, metric_reader=None, log_exporter=None) -> Providers` (dataclass with `tracer_provider`, `meter_provider`, `logger_provider`; idempotent, returns the existing set on repeat calls), and the completed `configure(app, registry)`.
- Test fixture `telemetry` with `.spans()`, `.logs()`, `.metric_reader`, `.dump() -> str`, `.reset()`.

- [x] **Step 1: Complete `setup.py`**

```python
"""SDK bootstrap: build providers from the OTel environment, instrument the app.

`register_providers` runs once per process and installs the global tracer,
meter and logger providers with the guard processors in front of the OTLP
exporters. Tests inject in-memory exporters through the same function.
`configure` runs once per app and is a no-op when `OTEL_SDK_DISABLED=true`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, SimpleLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor

from mulyankan_platform.observability.guard import LogAttributeGuard, SpanAttributeGuard, metric_views
from mulyankan_platform.observability.http import RequestLogMiddleware
from mulyankan_platform.observability.logs import configure_logging
from mulyankan_platform.observability.metrics import attributes_dropped, observe_registry_bindings

if TYPE_CHECKING:  # registry imports this package; keep the edge type-only
    from mulyankan_platform.registry import ProviderRegistry

# Process-level instruments only; host metrics come from the Collector (§6.3).
_PROCESS_METRICS = {
    "process.cpu.time": ["user", "system"],
    "process.cpu.utilization": None,
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


def register_providers(*, span_exporter=None, metric_reader=None, log_exporter=None) -> Providers:  # noqa: ANN001
    global _providers
    if _providers is not None:
        if span_exporter or metric_reader or log_exporter:
            raise RuntimeError("providers are already installed; exporters cannot change")
        return _providers

    # OTEL_SEMCONV_STABILITY_OPT_IN=http is set at module import (top of this
    # file): the instrumentation latches it once per process, the first time
    # anything instruments, so it must precede every instrumentor.
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
        metric_readers=[metric_reader or PeriodicExportingMetricReader(OTLPMetricExporter())],
        views=metric_views(),  # the metric-side guard (§4.2)
    )
    metrics.set_meter_provider(meter_provider)

    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(LogAttributeGuard(attributes_dropped))
    if log_exporter is None:
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
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
    """Instrument `app`; does nothing when the SDK is disabled. Never raises:
    a bad endpoint surfaces as exporter warnings, and the app serves."""
    if sdk_disabled():
        return
    providers = register_providers()
    # Added first so it runs inside the OTel middleware (added by instrument_app).
    app.add_middleware(RequestLogMiddleware)
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=providers.tracer_provider,
        meter_provider=providers.meter_provider,
        # Resolved at configure time, "" when unset, because the instrumentation
        # snapshots the environment at import and treats None as that snapshot.
        excluded_urls=os.environ.get(
            "OTEL_PYTHON_FASTAPI_EXCLUDED_URLS", os.environ.get("OTEL_PYTHON_EXCLUDED_URLS", "")
        ),
        exclude_spans=["receive", "send"],  # the ASGI message spans are noise
    )
    if registry is not None:
        observe_registry_bindings(registry)
```

`OTEL_PYTHON_FASTAPI_EXCLUDED_URLS` is read by the instrumentor from the environment, so `/healthz` exclusion is configuration (§5), not code.

- [x] **Step 2: Rewrite the one existing log call**

In `core_api/main.py`, `_default_app`:

```python
        logger.warning(
            "platform.config.missing",
            extra={"mulyankan.object_ref": DEFAULT_CONFIG_PATH},
        )
```

(A config path is not question content; it is an opaque reference for the operator.)

- [x] **Step 3: Add the telemetry fixture**

Append to `platform/core/tests/conftest.py`:

```python
import json

import pytest
from opentelemetry.sdk._logs.export import InMemoryLogExporter
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from mulyankan_platform.observability import register_providers


class Telemetry:
    """Everything exported during a test, in memory."""

    def __init__(self) -> None:
        self.span_exporter = InMemorySpanExporter()
        self.metric_reader = InMemoryMetricReader()
        self.log_exporter = InMemoryLogExporter()
        register_providers(
            span_exporter=self.span_exporter,
            metric_reader=self.metric_reader,
            log_exporter=self.log_exporter,
        )

    def reset(self) -> None:
        self.span_exporter.clear()
        self.log_exporter.clear()

    def spans(self):
        return list(self.span_exporter.get_finished_spans())

    def logs(self):
        return [d.log_record for d in self.log_exporter.get_finished_logs()]

    def dump(self) -> str:
        """Serialise every exported span, log and metric point for assertions."""
        out = {"spans": [], "logs": [], "metrics": []}
        for span in self.spans():
            out["spans"].append({
                "name": span.name,
                "attributes": dict(span.attributes or {}),
                "events": [{"name": e.name, "attributes": dict(e.attributes or {})} for e in span.events],
                "resource": dict(span.resource.attributes),
            })
        for record in self.logs():
            out["logs"].append({"body": record.body, "attributes": dict(record.attributes or {})})
        data = self.metric_reader.get_metrics_data()
        for rm in data.resource_metrics:
            for sm in rm.scope_metrics:
                for metric in sm.metrics:
                    for point in metric.data.data_points:
                        out["metrics"].append({"name": metric.name, "attributes": dict(point.attributes)})
        return json.dumps(out, default=str, ensure_ascii=False)


_TELEMETRY: Telemetry | None = None


@pytest.fixture
def telemetry() -> Telemetry:
    global _TELEMETRY
    if _TELEMETRY is None:
        _TELEMETRY = Telemetry()
    _TELEMETRY.reset()
    return _TELEMETRY
```

Because `register_providers` is idempotent, the first test that asks for the fixture installs the in-memory providers for the whole session; every `create_app_*` call afterwards instruments against them.

- [x] **Step 4: Write the pipeline tests**

`platform/core/tests/test_observability_pipeline.py`:

```python
"""The standing DoD check: no Restricted content in any exported signal, and
the app survives without a Collector (ASR02-OBS)."""

import logging
import subprocess
import sys
import textwrap

from fastapi import Header
from fastapi.testclient import TestClient

from mulyankan_platform.audit import AuditLog
from mulyankan_platform.core_api.main import create_app_from_mapping

SENTINEL = "SENTINEL-e8b4-ప్రశ్న"  # includes non-ASCII so encoding paths are covered
MAPPING = {"providers": {"kms": {"provider": "testkit_fake_provider:FakeKms", "config": {}}}}


def test_asr02obs_no_content_reaches_any_exporter(telemetry, capsys) -> None:
    app = create_app_from_mapping(MAPPING)

    @app.post("/probe/{item}")
    def probe(item: str, body: dict, q: str | None = None,
              x_probe: str | None = Header(default=None)) -> dict:
        kms = app.state.registry.get("kms")
        kms.encrypt("k", SENTINEL.encode())
        AuditLog().append(actor="author-001", action="probe", payload={"stem": SENTINEL})
        logging.getLogger("probe").info("probe.hit", extra={"stem": SENTINEL})
        raise ValueError(f"{item} {q} {x_probe} {body}")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.post(
        f"/probe/{SENTINEL}?q={SENTINEL}", headers={"x-probe": SENTINEL}, json={"stem": SENTINEL}
    )
    assert response.status_code == 500

    exported = telemetry.dump()
    assert "POST /probe/{item}" in exported  # the pipeline did see the request
    assert "kms.encrypt" in exported
    assert "probe.hit" in exported
    assert SENTINEL not in exported
    assert SENTINEL not in capsys.readouterr().out  # the stdout JSON handler

    # D12: the response tells a human which trace this was.
    (server_span,) = [s for s in telemetry.spans() if s.name == "POST /probe/{item}"]
    ctx = server_span.get_span_context()
    assert response.headers["server-timing"] == (
        f'traceparent;desc="00-{ctx.trace_id:032x}-{ctx.span_id:016x}-01"'
    )


def test_asr02obs_healthz_is_excluded_from_traces(telemetry, monkeypatch) -> None:
    monkeypatch.setenv("OTEL_PYTHON_FASTAPI_EXCLUDED_URLS", "healthz")
    client = TestClient(create_app_from_mapping({}))
    assert client.get("/healthz").json() == {"status": "ok", "providers": {}}
    assert [s.name for s in telemetry.spans()] == []


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
        [sys.executable, "-c", UNREACHABLE], capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, result.stderr
    assert "served" in result.stdout
```

- [x] **Step 5: Run the whole suite**

Run: `python -m pytest platform/spi platform/core -q`
Expected: every test passes, including the Task 4, 5, 6 and 7 tests that needed the fixture. If `test_asr02obs_no_content_reaches_any_exporter` fails, print `exported` and find which key carried the sentinel; the fix is always the allowlist, never the test.

- [x] **Step 6: Run the API by hand once**

```bash
OTEL_SERVICE_NAME=core-api OTEL_SDK_DISABLED=true \
  uvicorn --factory mulyankan_platform.core_api.main:app --no-access-log --port 8000 &
curl -si localhost:8000/healthz | head -5
```
Expected: `200`, a JSON warning line about the missing config on stdout, no access log line. Stop the server.

- [ ] **Step 7: Commit**

```bash
git add platform/core/src/mulyankan_platform/observability/setup.py platform/core/src/mulyankan_platform/core_api/main.py platform/core/tests/conftest.py platform/core/tests/test_observability_pipeline.py
git commit -s -m "Wire the OTel SDK into core-api and prove it content-free"
```

### Task 9: Docs for slice 2

**Files:**
- Modify: `platform/core/AGENTS.md`, `platform/AGENTS.md`, `AGENTS.md`, `docs/traceability.md`

- [x] **Step 1: `platform/core/AGENTS.md`**

Add to "What is here", after the `core_api/main.py` bullet:

```markdown
- `observability/` — OTel wiring (ADR-0011, `docs/observability.md`):
  `setup.configure` is called from `build_app`; `guard.py` holds the
  attribute allowlist that keeps every signal content-free. Add an attribute
  only by adding it to the allowlist with a reason; the sentinel test
  `test_asr02obs_no_content_reaches_any_exporter` fails otherwise.
```

Under the `audit/chain.py` rules add:

```markdown
- `append` records two metrics and adds a span event carrying the event id.
  Telemetry links point at events; nothing telemetry-related is ever stored
  on an event, so the canonical bytes are unaffected.
```

Under "What is here" for `registry.py`, append: "`get()` returns the provider wrapped in `ObservedProvider`, which spans each call; the wrapping is eager so runtime Protocol checks still pass."

Under Tests: "`conftest.py` also installs in-memory OTel exporters through the `telemetry` fixture; tests that need a fresh process (SDK disabled, Collector unreachable) run a subprocess."

Logging convention, new section:

```markdown
## Logging

Standard library `logging`. The message is a static dotted event name; every
value goes in `extra` under an allowlisted key (`mulyankan.object_ref`,
`mulyankan.audit.event_id`, ...). `logger.info("x %s", value)` is a review
finding. `uvicorn.access` is disabled; the request log middleware replaces it.
```

- [x] **Step 2: `platform/AGENTS.md`**

In the package table, `platform/core` depends on: `mulyankan-spi`, fastapi, uvicorn, pyyaml, opentelemetry-api/sdk, the OTLP HTTP exporter, the FastAPI and system-metrics instrumentations.

- [x] **Step 3: Root `AGENTS.md`**

The "Daily consequence" line becomes: **no question content in logs, audit events, exception strings, URLs, or span and log attributes.** Add under Commands, after the pytest line:

```bash
# Telemetry is on by default and exports to $OTEL_EXPORTER_OTLP_ENDPOINT;
# set OTEL_SDK_DISABLED=true to run without it. See docs/observability.md.
```

- [x] **Step 4: `docs/traceability.md`**

The ASR02-OBS row's "Closed in" column becomes `M1 (pipeline: this slice); M3 (operator surface)` and a new line under the table:

```markdown
ASR02-OBS tests: `test_asr02obs_no_content_reaches_any_exporter`,
`test_asr02obs_request_log_uses_route_not_path`,
`test_asr02obs_unknown_span_attributes_are_dropped_and_counted`,
`test_asr02obs_unknown_log_attributes_are_dropped_and_counted`,
`test_asr02obs_app_serves_with_collector_unreachable`,
`test_asr02obs_app_serves_with_sdk_disabled`,
`test_asr02obs_provider_calls_are_spanned_content_free`,
`test_asr02obs_audit_append_records_metrics_and_span_link`,
`test_asr02obs_healthz_is_excluded_from_traces`.
```

- [ ] **Step 5: Commit and open the PR**

```bash
git add platform/core/AGENTS.md platform/AGENTS.md AGENTS.md docs/traceability.md
git commit -s -m "Document the observability package and its tests"
```

---

## Slice 3: The local stack

### Task 10: `deploy/dev/`

**Files:**
- Create: `deploy/dev/compose.yaml`, `deploy/dev/otel-collector.yaml`, `deploy/dev/.env.example`, `deploy/dev/README.md`
- Modify: `AGENTS.md`, `docs/AGENTS.md`

**Interfaces:**
- Produces: `docker compose -f deploy/dev/compose.yaml up -d` gives OTLP on `localhost:4317`/`4318` and Grafana on `localhost:3001` (3000 is the Next.js dev server).

- [x] **Step 1: The compose file**

`deploy/dev/compose.yaml`:

```yaml
# Local observability backend. Grafana's all-in-one image is a development
# convenience (D1): a separate, unmodified AGPL service per ADR-0002, never a
# dependency of the system. The applications run on the host and export to
# the Collector; only the Collector's OTLP ports and Grafana are published,
# and only on loopback: the receiver and Grafana (admin / admin) are unauthenticated.
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.160.0@sha256:799dc6cf12c96192af37b5bdba804da8c10b3bc563b43cb90c3f3c58d9572ad6
    command: ["--config=/etc/otelcol/config.yaml"]
    volumes:
      - ./otel-collector.yaml:/etc/otelcol/config.yaml:ro
    ports:
      - "127.0.0.1:4317:4317"   # OTLP gRPC
      - "127.0.0.1:4318:4318"   # OTLP HTTP
      - "127.0.0.1:13133:13133" # health_check extension
    depends_on:
      - lgtm

  lgtm:
    image: grafana/otel-lgtm:0.32.1@sha256:7fd8eaad6bb64897ad5f644c8e15ee67c3204c97168f4bdba122adbf8f60e3c4
    ports:
      - "127.0.0.1:3001:3000"   # Grafana (admin / admin); 3000 is the Next.js dev server
    volumes:
      - lgtm-data:/data
      # Development dashboards (spec §6.2). Grafana reads the provider file
      # from its provisioning directory and the JSON from the mounted path.
      - ./grafana/dashboards.yaml:/otel-lgtm/grafana/conf/provisioning/dashboards/mulyankan.yaml:ro
      - ./grafana/dashboards:/otel-lgtm/dashboards:ro

volumes:
  lgtm-data:
```

- [x] **Step 2: The Collector configuration**

`deploy/dev/otel-collector.yaml`:

```yaml
# The portable artefact (spec §6.1): production keeps this file and changes
# only `exporters`. Redaction here is defence in depth; the applications
# apply the same allowlist in-process, which is the control.
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 256
  batch: {}
  redaction:
    allow_all_keys: false
    # Despite the name, `ignored_keys` are NOT dropped: the processor skips
    # them before the allowlist check, so they pass through untouched
    # ("ignored" by the redaction, not by the pipeline). The processor also
    # runs the allowlist over resource attributes, and without this list it
    # strips service.name and the rest of the descriptor, which breaks every
    # service-based query. Resource attributes are the operator's descriptor
    # (ADR-0011; spec §4.2 says they are not filtered). Add a key when the
    # descriptor grows (e.g. resourcedetection's host.*).
    ignored_keys:
      - service.name
      - service.namespace
      - service.version
      - service.instance.id
      - deployment.environment.name
      - telemetry.sdk.name
      - telemetry.sdk.language
      - telemetry.sdk.version
      - telemetry.distro.name
      - telemetry.distro.version
    # One processor for all three pipelines: the union of the span, log and
    # metric allowlists in platform/core/.../guard.py, which a test pins.
    allowed_keys:
      # The union of the three Python allowlists (guard.py), nothing more.
      # The web tier's keys (url.path, a query-stripped url.full, next.*,
      # the RUM keys) are added in the PR that lands apps/web's allowlist,
      # so this list never admits a key nothing in the tree emits.
      - http.request.method
      - http.route
      - http.response.status_code
      - http.request.body.size
      - http.response.body.size
      - url.scheme
      - server.address
      - server.port
      - network.protocol.version
      - client.address
      - error.type
      - exception.type
      - exception.stacktrace
      - enduser.pseudo.id
      - mulyankan.spi
      - mulyankan.provider.name
      - mulyankan.provider.version
      - mulyankan.audit.event_id
      - mulyankan.object_ref
      - mulyankan.state.from
      - mulyankan.state.to
      - mulyankan.http.request.duration
      - db.system.name
      - db.operation.name
      - db.collection.name
      # log records
      - code.function.name
      - code.file.path
      - code.line.number
      # metric data points (ALLOWED_METRIC_ATTRIBUTES)
      - signal
      - attribute
      - action
      - spi
      - provider.name
      - provider.version
      - from_state
      - to_state
      - type
      - generation
    summary: debug

exporters:
  otlp_http:
    endpoint: http://lgtm:4318
    tls:
      insecure: true

extensions:
  health_check:
    endpoint: 0.0.0.0:13133

service:
  extensions: [health_check]
  telemetry:
    metrics:
      level: normal
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, redaction, batch]
      exporters: [otlp_http]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, redaction, batch]
      exporters: [otlp_http]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, redaction, batch]
      exporters: [otlp_http]
```

- [x] **Step 3: The environment example**

`deploy/dev/.env.example`:

```bash
# Source into the shell that runs core-api and the web app.
# Every variable is the OpenTelemetry SDK's own; nothing here names a backend.
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_PROPAGATORS=tracecontext
export OTEL_TRACES_SAMPLER=parentbased_always_on
export OTEL_SEMCONV_STABILITY_OPT_IN=http
export OTEL_RESOURCE_ATTRIBUTES=service.namespace=open-mulyankan,service.version=0.1.0,deployment.environment.name=local
export OTEL_LOG_LEVEL=info

# core-api
# Anchored: the instrumentation applies it as an unanchored search over
# scheme://host/path, so a bare `healthz` would also blind any host or path
# containing the word.
export OTEL_PYTHON_FASTAPI_EXCLUDED_URLS='^https?://[^/]+/healthz$'
# OTEL_SERVICE_NAME is set per process: core-api, web.
```

- [x] **Step 4: README**

`deploy/dev/README.md`:

```markdown
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
    source deploy/dev/.env.example

    # core-api, from the repo root
    OTEL_SERVICE_NAME=core-api uvicorn --factory mulyankan_platform.core_api.main:app --no-access-log --port 8000

    # web, from apps/web
    OTEL_SERVICE_NAME=web NEXT_PUBLIC_CORE_API_ORIGIN=http://localhost:8000 pnpm dev

Open http://localhost:3001 (admin / admin), Explore, Tempo, search
`service.name = core-api`. Logs are in Loki with `trace_id` for correlation.

## Stop and reset

    docker compose -f deploy/dev/compose.yaml down -v
```

- [x] **Step 5: Verify**

```bash
docker compose -f deploy/dev/compose.yaml up -d
sleep 10 && curl -sf localhost:13133 && echo collector-ok
source deploy/dev/.env.example
OTEL_SERVICE_NAME=core-api uvicorn --factory mulyankan_platform.core_api.main:app --no-access-log --port 8000 &
sleep 2; for i in 1 2 3; do curl -s localhost:8000/healthz >/dev/null; done
curl -s "localhost:8000/nope" >/dev/null   # a 404 is traced; /healthz is excluded
```
Expected: `collector-ok`; in Grafana Explore, Tempo shows a `GET /nope`-less trace named by route (`HTTP GET` with `http.route` absent for unmatched routes) under `service.name=core-api`, and Loki shows the `http.request` JSON lines with `trace_id`. Kill uvicorn.

- [x] **Step 6: Docs**

Root `AGENTS.md`: in the `ls providers db contracts ...` paragraph, add `deploy/dev` to what now exists: "`deploy/dev/` exists (the local observability stack, `docs/observability.md` §6); the others are still absent." `docs/AGENTS.md`'s "Keeping this file true" needs no change; `docs/observability.md` §6.2 already describes the directory.

- [ ] **Step 7: Commit and open the PR**

```bash
git add deploy/dev AGENTS.md
git commit -s -m "Add the local Collector and Grafana stack under deploy/dev"
```

---

## Slice 4: Next.js server side

### Task 11: Dependencies, config, and the allowlist

**Files:**
- Modify: `apps/web/package.json`, `apps/web/next.config.ts`
- Create: `apps/web/vitest.config.ts`, `apps/web/src/observability/allowlist.ts`

- [ ] **Step 1: Add packages**

From `apps/web`:

```bash
pnpm add @opentelemetry/api@1.9.1 @opentelemetry/api-logs@0.222.0 \
  @opentelemetry/sdk-node@0.222.0 @opentelemetry/sdk-trace-base@2.11.0 \
  @opentelemetry/sdk-logs@0.222.0 @opentelemetry/resources@2.11.0 \
  @opentelemetry/core@2.11.0 @opentelemetry/semantic-conventions@1.43.0 \
  @opentelemetry/exporter-trace-otlp-http@0.222.0 \
  @opentelemetry/exporter-metrics-otlp-http@0.222.0 \
  @opentelemetry/exporter-logs-otlp-http@0.222.0 \
  @opentelemetry/sdk-metrics@2.11.0 \
  @opentelemetry/auto-instrumentations-node@0.80.0 pino@10.3.1
pnpm add -D vitest@5.0.0
```

`auto-instrumentations-node` is the official bundle (D19, spec §4.7); it
carries `instrumentation-http`, `instrumentation-pino` and
`instrumentation-runtime-node`, which are the three in use here. `sdk-metrics`
is listed explicitly because the guard imports `View` from it.

If `.npmrc`'s `minimum-release-age` rejects a version, use the newest one it accepts and note it in the commit message.

Add to `scripts`: `"test": "vitest run"`.

- [ ] **Step 2: `next.config.ts`**

Add to `nextConfig`:

```ts
  // OTel instrumentations patch modules at require time; bundling them would
  // bypass the patch. Keep the SDK, the instrumentation bundle and pino external.
  serverExternalPackages: [
    '@opentelemetry/sdk-node',
    '@opentelemetry/auto-instrumentations-node',
    '@opentelemetry/instrumentation',
    'pino',
  ],
```

- [ ] **Step 3: `vitest.config.ts`**

```ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    include: ['src/**/*.test.ts'],
  },
});
```

- [ ] **Step 4: The allowlist**

`apps/web/src/observability/allowlist.ts`:

```ts
/**
 * Content-free guard allowlist (spec §4.2). Keep identical to
 * platform/core/src/mulyankan_platform/observability/guard.py and the
 * Collector's redaction list. One entry per line, with the reason.
 */
export const ALLOWED_ATTRIBUTES: ReadonlySet<string> = new Set([
  // Stable HTTP conventions (browser fetch instrumentation, core-api)
  'http.request.method',
  'http.route',
  'http.response.status_code',
  'http.request.body.size',
  'http.response.body.size',
  'url.scheme',
  'url.path', // pathname: content-free by DAT-03; browser signals key on it
  'url.full', // kept only after stripQuery()
  'server.address',
  'server.port',
  'network.protocol.version',
  'client.address',
  'error.type',
  'exception.type',
  'exception.stacktrace', // frame lines only: framesOnly() removes the message
  'enduser.pseudo.id', // DAT-02 pseudonymous workforce id
  'session.id', // D17: random per-tab id
  // Next.js built-in spans (older HTTP conventions)
  'http.method',
  'http.status_code',
  'http.url', // kept only after stripQuery()
  'net.peer.name',
  'net.peer.port',
  'next.span_name',
  'next.span_type',
  'next.route',
  'next.page',
  'next.rsc',
  'next.segment',
  // Browser RUM
  'browser.mobile',
  'navigation.type',
  'event_type', // user-interaction instrumentation: "click"
  'target_element', // tag name
  'target_xpath', // location, never text
  'mulyankan.web.vital.rating',
]);

/** Attributes whose value is a URL: the query string is removed, the rest kept. */
export const URL_ATTRIBUTES: ReadonlySet<string> = new Set(['url.full', 'http.url']);

/**
 * Metric data-point attributes (spec §3.2): the span keys, the browser
 * instruments' own keys, and the fixed enumerations of the Node runtime
 * instrumentation. Applied by an SDK View on both the Node and browser
 * meter providers; a View drops silently, so the sentinel test is the check.
 */
export const ALLOWED_METRIC_ATTRIBUTES: ReadonlySet<string> = new Set([
  ...ALLOWED_ATTRIBUTES,
  'nodejs.eventloop.state', // active | idle
  'v8js.gc.type', // major | minor | incremental | weakcb
  'v8js.heap.space.name',
  'v8js.resource.type',
]);

/** Spans about the telemetry pipeline itself are never exported (feedback loop). */
export const RELAY_ROUTE_PREFIX = '/api/otlp';
export const OTLP_PATH = /\/v1\/(traces|metrics|logs)$/;
```

- [ ] **Step 5: Type-check and commit**

Run: `pnpm check-types && pnpm lint`
Expected: clean.

```bash
git add package.json pnpm-lock.yaml next.config.ts vitest.config.ts src/observability/allowlist.ts
git commit -s -m "Add OTel Node dependencies, vitest, and the web allowlist"
```

### Task 12: The guarded exporters

**Files:**
- Create: `apps/web/src/observability/guard.ts`
- Test: `apps/web/src/observability/guard.test.ts`

**Interfaces:**
- Produces: `stripQuery(url: string): string`, `framesOnly(stack: string | undefined): string`, `filterAttributes(attrs, onDrop?)`, `metricViews(): View[]`, `GuardedSpanExporter(inner: SpanExporter, onDrop?)`, `GuardedLogExporter(inner: LogRecordExporter, onDrop?)`. The exporters wrap an exporter, filter attributes in place, and drop relay spans before delegating. `filterAttributes` filters by key and rewrites two kinds of value: URL attributes lose their query string and `exception.stacktrace` is reduced to its `at ...` frame lines, because V8 renders `Name: message` as the first line(s) of `err.stack` and `recordException` copies it verbatim. `metricViews()` is the metric-side guard. Used by Task 14 (Node) and Task 16 (browser).

- [ ] **Step 1: Write the failing test**

`apps/web/src/observability/guard.test.ts`:

```ts
import { describe, expect, it, vi } from 'vitest';
import { AggregationTemporality, InMemoryMetricExporter, MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import type { ReadableSpan, SpanExporter } from '@opentelemetry/sdk-trace-base';
import { GuardedSpanExporter, framesOnly, metricViews, stripQuery } from './guard';

const SENTINEL = 'SENTINEL-1d9f';

function span(name: string, attributes: Record<string, unknown>, events: Array<{ name: string; attributes: Record<string, unknown> }> = []): ReadableSpan {
  return { name, attributes, events, resource: { attributes: {} } } as unknown as ReadableSpan;
}

describe('asr02obs guard', () => {
  it('strips query strings from URL attributes', () => {
    expect(stripQuery(`https://api.example/items/1?q=${SENTINEL}#frag`)).toBe('https://api.example/items/1');
    expect(stripQuery('not a url')).toBe('');
  });

  it('reduces a stack to its frame lines', () => {
    const stack = `Error: ${SENTINEL}\n  second line ${SENTINEL}\n    at inner (x.ts:4:9)\n    at outer (x.ts:10:3)`;
    expect(framesOnly(stack)).toBe('    at inner (x.ts:4:9)\n    at outer (x.ts:10:3)');
    expect(framesOnly(undefined)).toBe('');
  });

  it('removes unlisted attributes, keeps listed ones, counts drops', () => {
    const inner: SpanExporter = { export: vi.fn((_s, cb) => cb({ code: 0 })), shutdown: vi.fn(async () => {}) };
    const dropped: string[] = [];
    const exporter = new GuardedSpanExporter(inner, (k) => dropped.push(k));
    const s = span('GET', { 'http.request.method': 'GET', 'url.full': `http://x/y?q=${SENTINEL}`, 'user_agent.original': SENTINEL },
      [{ name: 'exception', attributes: { 'exception.type': 'Error', 'exception.message': SENTINEL, 'exception.stacktrace': `Error: ${SENTINEL}\n    at f (x.ts:1:1)` } }]);
    exporter.export([s], () => {});
    const exported = (inner.export as ReturnType<typeof vi.fn>).mock.calls[0][0] as ReadableSpan[];
    expect(exported[0].attributes).toEqual({ 'http.request.method': 'GET', 'url.full': 'http://x/y' });
    expect(exported[0].events[0].attributes).toEqual({ 'exception.type': 'Error', 'exception.stacktrace': '    at f (x.ts:1:1)' });
    expect(dropped).toEqual(['user_agent.original', 'exception.message']);
    expect(JSON.stringify(exported)).not.toContain(SENTINEL);
  });

  it('drops unlisted metric attributes through the view', async () => {
    const exporter = new InMemoryMetricExporter(AggregationTemporality.CUMULATIVE);
    const reader = new PeriodicExportingMetricReader({ exporter, exportIntervalMillis: 60_000 });
    const provider = new MeterProvider({ readers: [reader], views: metricViews() });
    provider.getMeter('test').createCounter('mulyankan.web.errors').add(1, { 'exception.type': 'Error', stem: SENTINEL });
    await reader.forceFlush();
    const points = exporter.getMetrics().flatMap((rm) => rm.scopeMetrics.flatMap((sm) => sm.metrics.flatMap((m) => m.dataPoints)));
    expect(points.map((p) => p.attributes)).toEqual([{ 'exception.type': 'Error' }]);
    await provider.shutdown();
  });

  it('drops spans about the relay and the exporter itself', () => {
    const inner: SpanExporter = { export: vi.fn((_s, cb) => cb({ code: 0 })), shutdown: vi.fn(async () => {}) };
    const exporter = new GuardedSpanExporter(inner);
    exporter.export([
      span('POST /api/otlp/v1/[signal]', { 'http.route': '/api/otlp/v1/[signal]' }),
      span('fetch POST', { 'http.url': 'http://localhost:4318/v1/traces' }),
      span('GET /', { 'http.route': '/' }),
    ], () => {});
    const exported = (inner.export as ReturnType<typeof vi.fn>).mock.calls[0][0] as ReadableSpan[];
    expect(exported.map((s) => s.name)).toEqual(['GET /']);
  });
});
```

- [ ] **Step 2: Run to see it fail**

Run: `pnpm test`
Expected: FAIL, cannot resolve `./guard`.

- [ ] **Step 3: Implement**

`apps/web/src/observability/guard.ts`:

```ts
/**
 * Content-free guard for the Node and browser SDKs (spec §4.2, §4.7, §4.8).
 * Implemented as exporter wrappers: at export time a span's `attributes` and
 * each event's `attributes` are plain objects, so they can be filtered in
 * place without touching SDK internals. Register the wrapper around the OTLP
 * exporter; nothing else in the pipeline sees unfiltered attributes.
 */
import type { ExportResult } from '@opentelemetry/core';
import type { ReadableLogRecord, LogRecordExporter } from '@opentelemetry/sdk-logs';
import { View } from '@opentelemetry/sdk-metrics';
import type { ReadableSpan, SpanExporter } from '@opentelemetry/sdk-trace-base';
import { ALLOWED_ATTRIBUTES, ALLOWED_METRIC_ATTRIBUTES, OTLP_PATH, RELAY_ROUTE_PREFIX, URL_ATTRIBUTES } from './allowlist';

export type OnDrop = (key: string) => void;

/**
 * V8 renders `err.stack` as `Name: message` (the message may span lines)
 * followed by `    at ...` frames, and `span.recordException` copies it into
 * `exception.stacktrace` verbatim. Keep only the frame lines.
 */
export function framesOnly(stack: string | undefined): string {
  return (stack ?? '')
    .split('\n')
    .filter((line) => /^\s+at /.test(line))
    .join('\n');
}

/** The metric-side guard: one View over every instrument (spec §4.2). */
export function metricViews(): View[] {
  return [new View({ instrumentName: '*', attributeKeys: [...ALLOWED_METRIC_ATTRIBUTES] })];
}

export function stripQuery(url: string): string {
  try {
    const u = new URL(url);
    return `${u.protocol}//${u.host}${u.pathname}`;
  } catch {
    return '';
  }
}

export function filterAttributes(attrs: Record<string, unknown>, onDrop?: OnDrop): void {
  for (const key of Object.keys(attrs)) {
    if (!ALLOWED_ATTRIBUTES.has(key)) {
      delete attrs[key];
      onDrop?.(key);
    } else if (URL_ATTRIBUTES.has(key) && typeof attrs[key] === 'string') {
      attrs[key] = stripQuery(attrs[key] as string);
    } else if (key === 'exception.stacktrace') {
      attrs[key] = framesOnly(typeof attrs[key] === 'string' ? (attrs[key] as string) : undefined);
    }
  }
}

function isPipelineSpan(span: ReadableSpan): boolean {
  const a = span.attributes as Record<string, unknown>;
  const route = String(a['http.route'] ?? a['next.route'] ?? '');
  const url = String(a['http.url'] ?? a['url.full'] ?? '');
  return route.startsWith(RELAY_ROUTE_PREFIX) || OTLP_PATH.test(url.split('?')[0]);
}

export class GuardedSpanExporter implements SpanExporter {
  constructor(private readonly inner: SpanExporter, private readonly onDrop?: OnDrop) {}

  export(spans: ReadableSpan[], resultCallback: (result: ExportResult) => void): void {
    const kept = spans.filter((s) => !isPipelineSpan(s));
    for (const span of kept) {
      filterAttributes(span.attributes as Record<string, unknown>, this.onDrop);
      for (const event of span.events) {
        if (event.attributes) filterAttributes(event.attributes as Record<string, unknown>, this.onDrop);
      }
    }
    if (kept.length === 0) {
      resultCallback({ code: 0 });
      return;
    }
    this.inner.export(kept, resultCallback);
  }

  shutdown(): Promise<void> {
    return this.inner.shutdown();
  }

  forceFlush(): Promise<void> {
    return this.inner.forceFlush?.() ?? Promise.resolve();
  }
}

export class GuardedLogExporter implements LogRecordExporter {
  constructor(private readonly inner: LogRecordExporter, private readonly onDrop?: OnDrop) {}

  export(logs: ReadableLogRecord[], resultCallback: (result: ExportResult) => void): void {
    for (const record of logs) {
      filterAttributes(record.attributes as Record<string, unknown>, this.onDrop);
    }
    this.inner.export(logs, resultCallback);
  }

  shutdown(): Promise<void> {
    return this.inner.shutdown();
  }
}
```

- [ ] **Step 4: Run to see it pass, then commit**

Run: `pnpm test && pnpm check-types`
Expected: 5 passed, types clean.

```bash
git add src/observability/guard.ts src/observability/guard.test.ts
git commit -s -m "Add guarded OTLP exporters for the web app"
```

### Task 13: The OTLP relay route

**Files:**
- Create: `apps/web/src/app/api/otlp/v1/[signal]/route.ts`
- Test: `apps/web/src/app/api/otlp/v1/[signal]/route.test.ts`

**Interfaces:**
- Produces: `POST /api/otlp/v1/{traces|metrics|logs}` forwarding the body and `Content-Type` to `${OTEL_EXPORTER_OTLP_ENDPOINT}/v1/<signal>`; `204` on success, `502` on upstream failure or a 5 s upstream timeout, `413` over 1 MiB, `429` over `RATE_LIMIT` requests per client address per minute, `404` for other signals, `204` with no forwarding when the endpoint is unset. The relay is the web app's first route handler, so it sets the limits itself (D16); the reverse proxy's limits stack on top.

- [ ] **Step 1: Write the failing test**

`route.test.ts`:

```ts
import { afterEach, describe, expect, it, vi } from 'vitest';
import { POST, RATE_LIMIT } from './route';

const params = (signal: string) => ({ params: Promise.resolve({ signal }) });

describe('asr02obs otlp relay', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.unstubAllEnvs();
  });

  it('forwards the body and content type unchanged', async () => {
    vi.stubEnv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://collector:4318/');
    const upstream = vi.fn(async () => new Response(null, { status: 200 }));
    vi.stubGlobal('fetch', upstream);
    const body = JSON.stringify({ resourceSpans: [] });
    const res = await POST(new Request('http://web/api/otlp/v1/traces', { method: 'POST', body, headers: { 'content-type': 'application/json' } }), params('traces'));
    expect(res.status).toBe(204);
    const [url, init] = upstream.mock.calls[0] as [string, RequestInit];
    expect(url).toBe('http://collector:4318/v1/traces');
    expect((init.headers as Record<string, string>)['content-type']).toBe('application/json');
    expect(new TextDecoder().decode(init.body as ArrayBuffer)).toBe(body);
  });

  it('rejects unknown signals and oversized bodies', async () => {
    vi.stubEnv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://collector:4318');
    vi.stubGlobal('fetch', vi.fn());
    expect((await POST(new Request('http://web/x', { method: 'POST', body: '{}' }), params('profiles'))).status).toBe(404);
    const big = new Uint8Array(1_048_577);
    expect((await POST(new Request('http://web/x', { method: 'POST', body: big }), params('logs'))).status).toBe(413);
  });

  it('returns 502 when the collector is unreachable and 204 when unset', async () => {
    vi.stubEnv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://collector:4318');
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('ECONNREFUSED'); }));
    expect((await POST(new Request('http://web/x', { method: 'POST', body: '{}' }), params('metrics'))).status).toBe(502);
    vi.stubEnv('OTEL_EXPORTER_OTLP_ENDPOINT', '');
    expect((await POST(new Request('http://web/x', { method: 'POST', body: '{}' }), params('metrics'))).status).toBe(204);
  });

  it('bounds the upstream call with a timeout', async () => {
    vi.stubEnv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://collector:4318');
    const upstream = vi.fn(async () => new Response(null, { status: 200 }));
    vi.stubGlobal('fetch', upstream);
    await POST(new Request('http://web/x', { method: 'POST', body: '{}' }), params('traces'));
    const [, init] = upstream.mock.calls[0] as [string, RequestInit];
    expect(init.signal).toBeInstanceOf(AbortSignal);
  });

  it('rate limits per client address', async () => {
    vi.stubEnv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://collector:4318');
    vi.stubGlobal('fetch', vi.fn(async () => new Response(null, { status: 200 })));
    const from = (ip: string) => new Request('http://web/x', { method: 'POST', body: '{}', headers: { 'x-forwarded-for': ip } });
    let last = 0;
    for (let i = 0; i < RATE_LIMIT + 1; i += 1) last = (await POST(from('10.0.0.1'), params('logs'))).status;
    expect(last).toBe(429);
    expect((await POST(from('10.0.0.2'), params('logs'))).status).toBe(204);
  });
});
```

(`RATE_LIMIT` is imported from `./route` alongside `POST`.)

- [ ] **Step 2: Run to see it fail**

Run: `pnpm test`
Expected: FAIL, cannot resolve `./route`.

- [ ] **Step 3: Implement**

`route.ts`:

```ts
/**
 * OTLP relay (spec §4.9, D16). The browser posts OTLP here and never learns
 * the Collector's address; the Collector needs no CORS policy. The body is
 * forwarded as received: never parsed, never logged.
 *
 * This is an unauthenticated write path into the telemetry pipeline, so it
 * carries its own limits (D16): a body cap, a per-client-address rate limit
 * and an upstream timeout. A browser can send any `enduser.pseudo.id` here,
 * so check a browser-reported identity against the audit chain before
 * acting on it (D17).
 */
export const dynamic = 'force-dynamic';

const SIGNALS = new Set(['traces', 'metrics', 'logs']);
const MAX_BYTES = 1_048_576;
const UPSTREAM_TIMEOUT_MS = 5_000;
/** Requests per client address per minute. A tab sends at most three batches
 * every two seconds (§4.8), so this is an order of magnitude of headroom. */
export const RATE_LIMIT = 300;
const WINDOW_MS = 60_000;
const MAX_TRACKED_CLIENTS = 10_000;

const windows = new Map<string, { until: number; count: number }>();

function overLimit(client: string, now = Date.now()): boolean {
  const current = windows.get(client);
  if (current && current.until > now) {
    current.count += 1;
    return current.count > RATE_LIMIT;
  }
  if (windows.size >= MAX_TRACKED_CLIENTS) windows.clear(); // bounded memory; a reset is harmless
  windows.set(client, { until: now + WINDOW_MS, count: 1 });
  return false;
}

function clientAddress(request: Request): string {
  return request.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || 'unknown';
}

export async function POST(request: Request, context: { params: Promise<{ signal: string }> }): Promise<Response> {
  const { signal } = await context.params;
  if (!SIGNALS.has(signal)) return new Response(null, { status: 404 });
  if (overLimit(clientAddress(request))) return new Response(null, { status: 429 });

  const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT?.replace(/\/+$/, '');
  const body = await request.arrayBuffer();
  if (body.byteLength > MAX_BYTES) return new Response(null, { status: 413 });
  if (!endpoint) return new Response(null, { status: 204 });

  try {
    const upstream = await fetch(`${endpoint}/v1/${signal}`, {
      method: 'POST',
      headers: { 'content-type': request.headers.get('content-type') ?? 'application/json' },
      body,
      signal: AbortSignal.timeout(UPSTREAM_TIMEOUT_MS),
    });
    return new Response(null, { status: upstream.ok ? 204 : 502 });
  } catch {
    return new Response(null, { status: 502 }); // includes the timeout
  }
}
```

The limiter is per process, which matches the single-host deployment shape in
spec §6.3; a multi-replica deployment moves the limit to the ingress and the
in-process one becomes the backstop.

- [ ] **Step 4: Run, then commit**

Run: `pnpm test && pnpm check-types && pnpm lint`
Expected: all pass.

```bash
git add "src/app/api/otlp/v1/[signal]/route.ts" "src/app/api/otlp/v1/[signal]/route.test.ts"
git commit -s -m "Relay browser OTLP to the Collector through the web origin"
```

### Task 14: Server instrumentation, pino, and the traceparent meta tag

**Files:**
- Create: `apps/web/src/instrumentation.ts`, `apps/web/src/instrumentation.node.ts`, `apps/web/src/observability/logger.ts`
- Modify: `apps/web/src/app/layout.tsx`

**Interfaces:**
- Produces: the Node SDK started at server boot; `logger` (pino) exported from `observability/logger.ts`; `<meta name="traceparent">` in every server-rendered document when a span is active.

- [ ] **Step 1: The instrumentation hook**

`apps/web/src/instrumentation.ts`:

```ts
// Next.js calls register() once per server runtime. The Node SDK is not
// edge-compatible, so it is loaded only for the Node runtime.
export async function register(): Promise<void> {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation.node');
  }
}
```

`apps/web/src/instrumentation.node.ts`:

```ts
import { W3CTraceContextPropagator } from '@opentelemetry/core';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { NodeSDK, logs, metrics, tracing } from '@opentelemetry/sdk-node';
import { GuardedLogExporter, GuardedSpanExporter, metricViews } from './observability/guard';

// Service name, resource attributes and the endpoint come from the standard
// OTEL_* variables (ADR-0011); nothing here names a backend.
if (process.env.OTEL_SDK_DISABLED?.toLowerCase() !== 'true') {
  const sdk = new NodeSDK({
    spanProcessors: [new tracing.BatchSpanProcessor(new GuardedSpanExporter(new OTLPTraceExporter()))],
    logRecordProcessors: [new logs.BatchLogRecordProcessor(new GuardedLogExporter(new OTLPLogExporter()))],
    metricReader: new metrics.PeriodicExportingMetricReader({ exporter: new OTLPMetricExporter() }),
    views: metricViews(), // the metric-side guard (§4.2)
    textMapPropagator: new W3CTraceContextPropagator(), // tracecontext only (D8)
    // The official bundle (D19). In use: http (the server span Next.js's own
    // spans nest under), pino (trace ids injected, records forwarded to the
    // logs SDK; on by default) and runtime-node (event loop, GC, heap). fs is
    // off by default and stays off. Whatever else the bundle emits passes the
    // same guard; OTEL_NODE_DISABLED_INSTRUMENTATIONS trims it without code.
    instrumentations: [getNodeAutoInstrumentations()],
  });
  sdk.start();
}
```

- [ ] **Step 2: The logger**

`apps/web/src/observability/logger.ts`:

```ts
import pino from 'pino';

/**
 * Server-side logger (D19). Same convention as core-api: the message is a
 * static dotted event name, fields go in the first argument under allowlisted
 * keys. The pino instrumentation (from the auto-instrumentations bundle in
 * instrumentation.node.ts) adds trace ids and forwards each record to the
 * OTel logs SDK. Never log request bodies, query strings or user input.
 *
 *   logger.info({ 'mulyankan.object_ref': ref }, 'task.fetched');
 */
export const logger = pino({ level: process.env.LOG_LEVEL ?? 'info' });
```

- [ ] **Step 3: The meta tag in the root layout**

In `apps/web/src/app/layout.tsx` add the import and helper, and render the tag inside `<html>` before `<body>`:

```tsx
import { trace } from '@opentelemetry/api';

/** Links the browser's page-load span to this server render (spec §4.7). */
function TraceparentMeta() {
  const ctx = trace.getActiveSpan()?.spanContext();
  if (!ctx || ctx.traceId === '00000000000000000000000000000000') return null;
  const flags = ctx.traceFlags.toString(16).padStart(2, '0');
  return <meta name="traceparent" content={`00-${ctx.traceId}-${ctx.spanId}-${flags}`} />;
}
```

```tsx
    <html lang="en" data-theme="default">
      <head>
        <TraceparentMeta />
      </head>
      <body className="h-svh overflow-hidden">
```

- [ ] **Step 4: Verify against the local stack**

With `deploy/dev` running and the env sourced:

```bash
OTEL_SERVICE_NAME=web pnpm dev &
sleep 8; curl -s localhost:3000/ | grep -o '<meta name="traceparent"[^>]*>'
```
Expected: one meta tag with a 32-hex trace id. In Grafana Explore, Tempo shows a trace under `service.name=web` with the http instrumentation's `POST` or `GET` server span as root, Next.js's `GET /` under it and `render route (app) /` below that; Loki shows pino lines for `web` with `trace_id`; Prometheus has `nodejs_eventloop_utilization`. If the pino lines do not reach Loki, the instrumentation did not patch pino: confirm `serverExternalPackages` from Task 11 is in effect (`pnpm build` output lists the externals) and that the logger in `logger.ts` is created after `sdk.start()` runs, which the `instrumentation.ts` ordering guarantees.

- [ ] **Step 5: Check, then commit**

Run: `pnpm check-types && pnpm lint && pnpm build`
Expected: clean.

```bash
git add src/instrumentation.ts src/instrumentation.node.ts src/observability/logger.ts src/app/layout.tsx
git commit -s -m "Start the OTel Node SDK in Next.js and link renders to the browser"
```

### Task 15: Docs and CI for slice 4

- [ ] **Step 1: `apps/web/AGENTS.md`**

"What exists" gains: `src/instrumentation.ts` + `.node.ts` (OTel Node SDK; do not import them elsewhere), `src/observability/` (allowlist, guarded exporters, pino logger), `src/app/api/otlp/v1/[signal]/route.ts` (the OTLP relay; never parse or log its body), and the `traceparent` meta tag in `layout.tsx`. Add a "Load-bearing wires" row: `next.config.ts` `serverExternalPackages` keeps pino and the OTel instrumentation bundle unbundled; removing it silently stops log forwarding. Add to the untrusted-client paragraph: "No question content in span or log attributes either; `src/observability/allowlist.ts` is the list, and adding to it needs a reason."

- [ ] **Step 2: CI `web` job**

In `.github/workflows/ci.yml`, after `Check types`, add:

```yaml
      - name: Unit tests
        run: pnpm test
```

- [ ] **Step 3: Commit and open the PR**

```bash
git add apps/web/AGENTS.md .github/workflows/ci.yml
git commit -s -m "Document the web observability wiring and run its tests in CI"
```

---

## Slice 5: Browser tracing and RUM

### Task 16: `instrumentation-client.ts`

**Files:**
- Modify: `apps/web/package.json`
- Create: `apps/web/src/instrumentation-client.ts`, `apps/web/src/observability/actor.ts`, `apps/web/src/observability/vitals.ts`, `apps/web/src/observability/errors.ts`

**Interfaces:**
- Produces: browser tracer, meter and logger started before hydration; `setActor(pseudoId: string)` for the M1 sign-in flow; `onRouterTransitionStart` navigation spans.

- [ ] **Step 1: Add packages**

```bash
pnpm add @opentelemetry/sdk-trace-web@2.11.0 \
  @opentelemetry/context-zone@2.11.0 @opentelemetry/instrumentation@0.222.0 \
  @opentelemetry/instrumentation-fetch@0.222.0 \
  @opentelemetry/instrumentation-document-load@0.67.0 \
  @opentelemetry/instrumentation-user-interaction@0.66.0 web-vitals@6.2.1
```

- [ ] **Step 2: The actor processor**

`apps/web/src/observability/actor.ts`:

```ts
import type { Context } from '@opentelemetry/api';
import type { ReadableSpan, Span, SpanProcessor } from '@opentelemetry/sdk-trace-base';

let actor: string | undefined;

/** D17: the DAT-02 pseudonymous workforce id, from the server-issued session. */
export function setActor(pseudoId: string | undefined): void {
  actor = pseudoId;
}

export function currentActor(): string | undefined {
  return actor;
}

export class ActorSpanProcessor implements SpanProcessor {
  onStart(span: Span, _parent: Context): void {
    if (actor) span.setAttribute('enduser.pseudo.id', actor);
  }
  onEnd(_span: ReadableSpan): void {}
  shutdown(): Promise<void> { return Promise.resolve(); }
  forceFlush(): Promise<void> { return Promise.resolve(); }
}
```

- [ ] **Step 3: Vitals and errors**

`apps/web/src/observability/vitals.ts`:

```ts
import type { Meter } from '@opentelemetry/api';
import { onCLS, onFCP, onINP, onLCP, onTTFB, type Metric } from 'web-vitals';

/** Web vitals as histograms (spec §3.2); the pathname is the only attribute. */
export function reportVitals(meter: Meter): void {
  const histograms = {
    LCP: meter.createHistogram('mulyankan.web.vitals.lcp', { unit: 'ms' }),
    CLS: meter.createHistogram('mulyankan.web.vitals.cls', { unit: '1' }),
    INP: meter.createHistogram('mulyankan.web.vitals.inp', { unit: 'ms' }),
    TTFB: meter.createHistogram('mulyankan.web.vitals.ttfb', { unit: 'ms' }),
    FCP: meter.createHistogram('mulyankan.web.vitals.fcp', { unit: 'ms' }),
  };
  const record = (metric: Metric) =>
    histograms[metric.name].record(metric.value, {
      'url.path': window.location.pathname,
      'mulyankan.web.vital.rating': metric.rating,
    });
  onLCP(record);
  onCLS(record);
  onINP(record);
  onTTFB(record);
  onFCP(record);
}
```

`apps/web/src/observability/errors.ts`:

```ts
import type { Counter } from '@opentelemetry/api';
import { SeverityNumber, type Logger } from '@opentelemetry/api-logs';
import { framesOnly } from './guard';

export function reportErrors(logger: Logger, counter: Counter): void {
  const emit = (error: unknown) => {
    const err = error instanceof Error ? error : undefined;
    const attributes = {
      'exception.type': err?.name ?? 'Error',
      'exception.stacktrace': framesOnly(err?.stack), // the guard does this again at export
      'url.path': window.location.pathname,
    };
    logger.emit({ severityNumber: SeverityNumber.ERROR, body: 'web.error', attributes });
    counter.add(1, { 'exception.type': attributes['exception.type'], 'url.path': attributes['url.path'] });
  };
  window.addEventListener('error', (event) => emit(event.error));
  window.addEventListener('unhandledrejection', (event) => emit(event.reason));
}
```

- [ ] **Step 4: The client instrumentation file**

`apps/web/src/instrumentation-client.ts`:

```ts
/**
 * Browser tracing and RUM (spec §4.8). Next.js runs this after the document
 * loads and before hydration. Everything exports through the relay (§4.9);
 * the relay URL is ignored by the fetch instrumentation so the pipeline never
 * traces itself. No session replay, no input capture (D18).
 */
import { metrics, trace } from '@opentelemetry/api';
import { logs } from '@opentelemetry/api-logs';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { W3CTraceContextPropagator } from '@opentelemetry/core';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-http';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { UserInteractionInstrumentation } from '@opentelemetry/instrumentation-user-interaction';
import { resourceFromAttributes } from '@opentelemetry/resources';
import { BatchLogRecordProcessor, LoggerProvider } from '@opentelemetry/sdk-logs';
import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { BatchSpanProcessor, WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from '@opentelemetry/semantic-conventions';
import { ActorSpanProcessor } from './observability/actor';
import { reportErrors } from './observability/errors';
import { GuardedLogExporter, GuardedSpanExporter, metricViews } from './observability/guard';
import { reportVitals } from './observability/vitals';

const RELAY = '/api/otlp/v1';
const CORE_API_ORIGIN = process.env.NEXT_PUBLIC_CORE_API_ORIGIN ?? '';

function sessionId(): string {
  try {
    const existing = sessionStorage.getItem('otel.session.id');
    if (existing) return existing;
    const fresh = crypto.randomUUID();
    sessionStorage.setItem('otel.session.id', fresh);
    return fresh;
  } catch {
    return crypto.randomUUID();
  }
}

try {
  const resource = resourceFromAttributes({
    [ATTR_SERVICE_NAME]: 'web-browser',
    [ATTR_SERVICE_VERSION]: process.env.NEXT_PUBLIC_APP_VERSION ?? '0.1.0',
    'session.id': sessionId(),
    'browser.mobile': /Mobi/i.test(navigator.userAgent),
  });
  const exportOptions = { scheduledDelayMillis: 2000 };

  const tracerProvider = new WebTracerProvider({
    resource,
    spanProcessors: [
      new ActorSpanProcessor(),
      new BatchSpanProcessor(new GuardedSpanExporter(new OTLPTraceExporter({ url: `${RELAY}/traces` })), exportOptions),
    ],
  });
  tracerProvider.register({
    contextManager: new ZoneContextManager(),
    propagator: new W3CTraceContextPropagator(),
  });

  const meterProvider = new MeterProvider({
    resource,
    readers: [new PeriodicExportingMetricReader({ exporter: new OTLPMetricExporter({ url: `${RELAY}/metrics` }), exportIntervalMillis: 10000 })],
    views: metricViews(), // the metric-side guard (§4.2)
  });
  metrics.setGlobalMeterProvider(meterProvider);

  const loggerProvider = new LoggerProvider({
    resource,
    processors: [new BatchLogRecordProcessor(new GuardedLogExporter(new OTLPLogExporter({ url: `${RELAY}/logs` })), exportOptions)],
  });
  logs.setGlobalLoggerProvider(loggerProvider);

  registerInstrumentations({
    instrumentations: [
      new DocumentLoadInstrumentation(),
      new FetchInstrumentation({
        propagateTraceHeaderCorsUrls: CORE_API_ORIGIN ? [new RegExp(`^${CORE_API_ORIGIN.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`)] : [],
        ignoreUrls: [/\/api\/otlp\//],
        clearTimingResources: true,
      }),
      new UserInteractionInstrumentation({ eventNames: ['click'] }),
    ],
  });

  const meter = metrics.getMeter('web-browser');
  reportVitals(meter);
  reportErrors(logs.getLogger('web-browser'), meter.createCounter('mulyankan.web.errors'));
} catch {
  // Observability never breaks the page (principle 4).
}

/** Next.js calls this on every App Router navigation. */
export function onRouterTransitionStart(url: string, navigationType: 'push' | 'replace' | 'traverse'): void {
  try {
    const span = trace.getTracer('web-browser').startSpan('navigation', {
      attributes: { 'url.path': new URL(url, window.location.origin).pathname, 'navigation.type': navigationType },
    });
    // End after the next two frames: an approximation of "painted".
    requestAnimationFrame(() => requestAnimationFrame(() => span.end()));
  } catch {
    // never throw from a router hook
  }
}
```

- [ ] **Step 5: Run and inspect**

With the stack up: `OTEL_SERVICE_NAME=web NEXT_PUBLIC_CORE_API_ORIGIN=http://localhost:8000 pnpm dev`, open `http://localhost:3000`, click the smoke page's button, then in Grafana Explore search Tempo for `service.name = web-browser`.
Expected: a `documentLoad` span whose trace id equals the `traceparent` meta tag's, a `click` span with `target_element` and `target_xpath` but no text, and in Prometheus the `mulyankan_web_vitals_lcp_milliseconds` histogram.

- [ ] **Step 6: Check, then commit**

Run: `pnpm check-types && pnpm lint && pnpm build`

```bash
git add package.json pnpm-lock.yaml src/instrumentation-client.ts src/observability/actor.ts src/observability/vitals.ts src/observability/errors.ts
git commit -s -m "Trace the browser and report web vitals and errors over OTLP"
```

### Task 17: End-to-end trace test with Playwright

**Files:**
- Modify: `apps/web/package.json`
- Create: `apps/web/playwright.config.ts`, `apps/web/e2e/trace.spec.ts`
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: the relay, the meta tag, the fetch propagation.
- Produces: a browser test proving one trace id across browser, Next.js server and the core-api request, and a browser sentinel test.

- [ ] **Step 1: Add Playwright**

```bash
pnpm add -D @playwright/test@1.63.0
pnpm exec playwright install chromium
```

Scripts: `"e2e": "playwright test"`.

`apps/web/playwright.config.ts`:

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: 'e2e',
  timeout: 60_000,
  use: { baseURL: 'http://localhost:3000' },
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    env: {
      OTEL_SERVICE_NAME: 'web',
      // Unreachable on purpose: exports fail in the background; the page serves.
      OTEL_EXPORTER_OTLP_ENDPOINT: 'http://127.0.0.1:9',
      NEXT_PUBLIC_CORE_API_ORIGIN: 'http://localhost:8000',
    },
  },
});
```

- [ ] **Step 2: Write the tests**

`apps/web/e2e/trace.spec.ts`:

```ts
import { expect, test, type Page } from '@playwright/test';

const SENTINEL = 'SENTINEL-7c2a';
type Span = { name: string; traceId: string; attributes?: Array<{ key: string }> };

function spansOf(batches: unknown[]): Span[] {
  const out: Span[] = [];
  for (const batch of batches as Array<{ resourceSpans?: Array<{ scopeSpans: Array<{ spans: Span[] }> }> }>) {
    for (const rs of batch.resourceSpans ?? []) for (const ss of rs.scopeSpans) out.push(...ss.spans);
  }
  return out;
}

async function captureRelay(page: Page) {
  const bodies: { traces: unknown[]; metrics: unknown[]; logs: unknown[] } = { traces: [], metrics: [], logs: [] };
  for (const signal of ['traces', 'metrics', 'logs'] as const) {
    await page.route(`**/api/otlp/v1/${signal}`, async (route) => {
      bodies[signal].push(route.request().postDataJSON());
      await route.fulfill({ status: 204 });
    });
  }
  return bodies;
}

test('asr02obs one trace from page load through the browser to core-api', async ({ page }) => {
  const relay = await captureRelay(page);
  let coreTraceparent: string | undefined;
  await page.route('http://localhost:8000/**', async (route) => {
    // A request carrying traceparent is not a "simple" request, so the browser
    // preflights it. The stub answers CORS the way the real core-api must
    // (spec §4.9): allow the trace headers, or the real request is never sent.
    const cors = {
      'access-control-allow-origin': 'http://localhost:3000',
      'access-control-allow-headers': 'traceparent,tracestate,content-type',
      'access-control-expose-headers': 'server-timing',
    };
    if (route.request().method() === 'OPTIONS') {
      await route.fulfill({ status: 204, headers: cors });
      return;
    }
    coreTraceparent = route.request().headers()['traceparent'];
    await route.fulfill({ status: 200, headers: cors, contentType: 'application/json', body: '{"status":"ok"}' });
  });

  await page.goto('/');
  const meta = await page.getAttribute('meta[name="traceparent"]', 'content');
  expect(meta).toMatch(/^00-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$/);
  const serverTraceId = meta!.split('-')[1];

  await page.evaluate(() => fetch('http://localhost:8000/healthz'));
  await expect.poll(() => spansOf(relay.traces).length, { timeout: 20_000 }).toBeGreaterThanOrEqual(2);

  const spans = spansOf(relay.traces);
  const documentLoad = spans.find((s) => s.name === 'documentLoad');
  expect(documentLoad?.traceId).toBe(serverTraceId);

  const fetchSpan = spans.find((s) => /^(HTTP )?GET$/.test(s.name));
  expect(fetchSpan).toBeDefined();
  expect(coreTraceparent?.split('-')[1]).toBe(fetchSpan!.traceId);
});

test('asr02obs nothing the user typed, clicked or raised reaches an exporter', async ({ page }) => {
  const relay = await captureRelay(page);
  const cors = {
    'access-control-allow-origin': 'http://localhost:3000',
    'access-control-allow-headers': 'traceparent,tracestate,content-type,x-probe',
  };
  await page.route('http://localhost:8000/**', (route) =>
    route.fulfill({ status: route.request().method() === 'OPTIONS' ? 204 : 200, headers: cors, body: '{}' }),
  );

  await page.goto(`/?q=${SENTINEL}`);
  await page.getByRole('textbox').first().fill(SENTINEL);
  await page.getByRole('button').first().click();
  // Query, header and body carry the sentinel. The path does not: path segments
  // are opaque ids by DAT-03, and the browser keeps pathnames (spec §4.8).
  await page.evaluate(
    (s) => fetch(`http://localhost:8000/items/1?q=${s}`, { method: 'POST', headers: { 'x-probe': s }, body: s }),
    SENTINEL,
  );
  await page.evaluate((s) => { setTimeout(() => { throw new Error(s); }, 0); }, SENTINEL);

  await expect.poll(() => spansOf(relay.traces).length, { timeout: 20_000 }).toBeGreaterThanOrEqual(3);
  await expect.poll(() => relay.logs.length, { timeout: 20_000 }).toBeGreaterThanOrEqual(1);

  const everything = JSON.stringify(relay);
  expect(everything).toContain('documentLoad');
  expect(everything).toContain('click');
  expect(everything).toContain('web.error');
  expect(everything).not.toContain(SENTINEL);
});
```

The smoke page has one text input and one button (`page.tsx`); when real surfaces replace it, point the selectors at a form that exists.

- [ ] **Step 3: Run**

Run: `pnpm e2e`
Expected: 2 passed. If the first test fails on `documentLoad.traceId`, the meta tag was rendered without an active span; confirm `instrumentation.node.ts` started (a `pnpm dev` log line from the SDK) before debugging the browser side.

- [ ] **Step 4: CI**

In the `web` job, after `Build`:

```yaml
      - name: Install Playwright browser
        run: pnpm exec playwright install --with-deps chromium

      - name: End-to-end trace tests
        run: pnpm e2e
```

- [ ] **Step 5: Docs**

`apps/web/AGENTS.md` "What exists": `src/instrumentation-client.ts` (browser OTel; exports `onRouterTransitionStart`), `e2e/` (Playwright; `pnpm e2e`), and the rule "no session replay, no input capture, no element text in telemetry (D18)". `docs/traceability.md`: append the two browser test titles to the ASR02-OBS list.

- [ ] **Step 6: Commit and open the PR**

```bash
git add package.json pnpm-lock.yaml playwright.config.ts e2e apps/web/AGENTS.md ../../.github/workflows/ci.yml ../../docs/traceability.md
git commit -s -m "Prove one trace from the browser to core-api and no content in RUM"
```

---

## After the five slices

- ADR-0011 status: flip from Proposed to Accepted with deciders and date once the team has reviewed slice 2 (the first PR that depends on it).
- `docs/observability.md` §8 lists the same touch points; tick them as the slices land.
- Open items the plan does not cover, by design: alert rules and production dashboards (deferred until the deployment target is known; the development dashboards under `deploy/dev/grafana` are a local convenience), the M1 database instrumentations (`opentelemetry-instrumentation-sqlalchemy` and the driver's, added with the driver), D11 on SQL text, and the ADR-0008 thin client.
