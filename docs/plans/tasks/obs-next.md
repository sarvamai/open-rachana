# #112: Connect Next.js server instrumentation to API traces

Owner proposed in the delivery plan: **Irfan**. Technical review: KKT; Rohit for leak and failure checks.
Epic: [#105](https://github.com/Bodhan-AI/open-rachana/issues/105). [Module route](../observability.md).

Propagate and observe safe request context from Next.js server routes to the Python API.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Instrument one server-to-API request using the existing OTel contract; test sentinel fields and exporter-disabled mode.

## Inputs and outputs

- Input: Incoming trusted trace context, sanitised route templates, OTel SDK configuration and outbound API calls.
- Output: One correlated server trace with safe request logs/errors and bounded metrics; no payload/query/header content exported.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [DAT-03](../../requirements.md#req-dat-03) | Plaintext content never appears in URLs, analytics, traces, exception messages, infrastructure logs, browser storage, notifications, dashboards or support tickets. | MUST |
| [PRD-OBS-28](../../requirements.md#req-prd-obs-28) | GAP Application observability (§11): structured logs with correlation and trace identifiers and no content; metrics for active sessions, events per second, telemetry backlog, sealing duration and failure count, chain write latency and lag, outbox lag, assignment pool size; dashboards contain no content. | MUST |

## Exact PRD sections

- [6.14 Session integrity, observability and referral · ASR02-OBS](../../prd/technical-baseline.md#614-session-integrity-observability-and-referral--asr02-obs)
- [11. Non-functional requirements](../../prd/technical-baseline.md#11-non-functional-requirements)

## Behaviour to demonstrate

An API request containing a synthetic question in the query never exports that query value. Its server and API spans remain correlated.

Existing issue acceptance criteria, retained for review:

- [ ] One request can be followed from Next.js to Python.
- [ ] Logs/errors pass the sentinel guard.
- [ ] Missing Collector does not prevent page/API service.

## Dependencies and decisions

Required producer work: [#110](obs-python.md) (Irfan), [#111](obs-local.md) (Irfan).

No product decision for basic diagnostics. Agree attribute allowlists with Irfan and keep content/API permission work with its feature owner.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
