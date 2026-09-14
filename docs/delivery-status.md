# Delivery status and evidence

Snapshot: 14 September 2026, inspected baseline commit
`5627bd1574beb56ec6a1a8de97f83a5525870c9c`. This documentation change does not
implement product features. The README's **M0 foundation** status is retained;
partial M1 session/audit scaffolding exists. No acceptance milestone is closed
by this inspection.

## What exists and what it proves

| Area | Inspected artefact | Evidence limit |
|---|---|---|
| Audit chain | [chain.py](../platform/core/src/mulyankan_platform/audit/chain.py), [tests](../platform/core/tests/test_audit_chain.py) | In-memory chain and test definitions; not durable storage, transactionally committed domain state, external checkpoints or restore qualification |
| Session integrity | [monitor.py](../platform/core/src/mulyankan_platform/sessions/monitor.py), [monitor tests](../platform/core/tests/test_session_monitor.py), [API tests](../platform/core/tests/test_sessions_api.py) | Registration/heartbeat/close, copy/cut/paste and heartbeat-gap scaffolding. Unauthenticated, in-memory; not the complete ratified signal catalogue, referral policy or production operator workflow |
| Provider registry | [registry.py](../platform/core/src/mulyankan_platform/registry.py), [tests](../platform/core/tests/test_registry.py) | Binding/load/refusal logic; does not establish a complete production provider set |
| KMS SPI | [protocol](../platform/spi/src/mulyankan_spi/kms.py), [conformance suite](../platform/spi/src/mulyankan_spi/conformance/kms.py), [tests](../platform/spi/tests/test_kms_conformance.py) | Interface and test double; no reference KMS provider or production key service supplied |
| Web surfaces | [web tree description](../apps/web/AGENTS.md) | Knowledge-base, question-bank/blueprint and exam-paper mocks; no authenticated end-to-end workflow or source-approved assembly scope |
| Desktop client | [client scaffold](../apps/client/README.md), [ADR-0010](adr/0010-thin-client-tauri.md) | Tauri scaffold; no complete signed, enrolled, contract-connected role client |
| Observability | [working spec](observability.md), [implementation plan](observability-plan.md) | Design and planned slices; ADR-0011 still Proposed; no deployment or acceptance inferred from plan code snippets |

## Inspected test definitions

These references are useful partial evidence for the requirement register.
**They were read, not run, in this documentation review.** Existing short
test names retain their historic IDs; the mapping below names the canonical
requirements without pretending the current suite fully satisfies them.

### E1 — audit-chain checks

File: [test_audit_chain.py](../platform/core/tests/test_audit_chain.py).

- ASR01-EVD-02: `test_asrevd02_chain_verifies_after_appends` and
  `test_asrevd02_concurrent_appends_keep_the_chain_verifiable`.
- ASR01-EVD-03: `test_asrevd03_tampered_event_detected` and
  `test_asrevd03_removed_event_detected`.
- ASR01-EVD-09: `test_events_are_content_free` checks that payload content
  is not stored in an audit event. This is not a scan of all logs, arbitrary
  caller-provided fields, error strings or telemetry.

All remain partial: in-memory tests do not prove persistent evidence,
workflow atomicity, authorized writers, deployment or restore.

### E2 — session-integrity checks

Files: [test_session_monitor.py](../platform/core/tests/test_session_monitor.py)
and [test_sessions_api.py](../platform/core/tests/test_sessions_api.py).

- ASR02-OBS-01: `test_asr02obs01_registered_session_heartbeats`,
  `test_asr02obs01_close_is_terminal` and
  `test_asr02obs01_register_heartbeat_signal_roundtrip` exercise part of
  session lifecycle.
- ASR02-OBS-06: `test_asr02obs01_score_deducts_and_never_recovers` exercises
  a fixed score decrement and zero floor. It does not ratify D-03 or prove
  the complete policy-configured scoring system.
- `test_asr02obs01_operator_view_publishes_no_content_fields` and
  `test_asr02obs01_signal_input_is_tight` inspect the current bounded API
  payloads, not every future role screen or leak channel.

ASR02-OBS-01 is **not closed**. The API has no token validation; the operator
view publishes the session identifier used for writes. See the existing
[security limitation](../SECURITY.md#known-limitations). All role-specific
authorization, session ownership, durable persistence, loss/retry behaviour
and full acceptance evidence remain to be demonstrated.

### E3 — KMS protocol conformance

File: [test_kms_conformance.py](../platform/spi/tests/test_kms_conformance.py).
`test_conformance_passes_a_correct_provider` and the broken-provider checks
exercise the suite against `GoodFakeKms`. That deliberately simple test
double is not production encryption, a supplied reference provider, sealing
acceptance or a security certification.

## Missing implementation contracts and paths

At the baseline, `providers/`, `db/`, `contracts/`, `tests/conformance/`
and `platform.yaml` are absent. Refer to them as planned locations until
created. The existing KMS conformance suite lives inside `platform/spi`,
not the absent top-level conformance directory.

This change adds [canonicalization.md](canonicalization.md) as a record of
the existing draft format and the proposed PRD v1 decision. That file's
existence does not implement or ratify v1.

## CI and milestone evidence

The [CI workflow](../.github/workflows/ci.yml) has real security and web
jobs, but `build-and-test` still echoes placeholder build/test messages.
It does not execute the Python tests. The org-wide private reusable workflow
call is commented out. A green `ci` badge is therefore not evidence that
Python requirement tests passed or that the PRD's acceptance criteria closed.

The target milestone ladder remains M1 identity/configuration/audit,
M2 authoring, M3 reviews/accessibility/operator, M4 translation/sealing/handoff,
M5 hardening and M6 acceptance/handover. These are dependency/evidence gates,
not calendar weeks. The [delivery plan](delivery-plan.md) sets 28 September
2026 as the current target, including full Layer 2 integration; the M4 gateway
plan is not a substitute. Named delivery owners and interim dates remain to
be assigned. Sarvam AI pilot and Bodhan AI managed-service hosting are planned
responsibilities, not evidence of provisioned services or completed handover.

## How to update this status

For each delivered slice, link the commit and actual checks, attach retained
results with date/environment, describe remaining limits and obtain the
named owner's acceptance. Update the individual requirement row and this
snapshot together. Do not treat a screenshot, mock flow, test definition or
design document as a closed acceptance criterion.
