# #110: Instrument Python API logs, metrics and traces

Owner proposed in the delivery plan: **Irfan**. Technical review: KKT; Rohit for leak and failure checks.
Epic: [#105](https://github.com/Bodhan-AI/open-rachana/issues/105). [Module route](../observability.md).

Complete Python diagnostics around the merged OTel bootstrap without adding content leakage or workflow dependencies.

## Start here

PR #120 merged the SDK, guard and local stack. PR #121 adds structured logs, request logs, audit metrics and provider spans; inspect it before coding.

First deliverable: Continue PR #121’s logs/request/audit/provider work. Compare its acceptance evidence with #110 before adding another implementation.

## Inputs and outputs

- Input: Existing observability setup/guard, FastAPI routes, audit append and provider registry, OTel resource configuration.
- Output: Correlated structured logs, traces and metrics with fixed event names and approved attributes; exporter outage leaves domain decisions unchanged.

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

A provider throws a synthetic-content exception: the request still follows its error contract while no exception message/content leaves through logs or spans.

Existing issue acceptance criteria, retained for review:

- [ ] A request yields a correlated trace, metric and structured log.
- [ ] Synthetic Restricted text never leaves the process.
- [ ] Collector outage and SDK-disabled mode leave domain decisions unchanged.

## Dependencies and decisions

Required producer work: [#49](issue-49.md) (Rohit), [#52](issue-52.md) (Rohit).

ADR-0011/spec decision status stays visible. Diagnostic drops must not erase mandatory audit or integrity evidence.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
