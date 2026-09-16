# #111: Provide the local Collector and Grafana observability stack

Owner proposed in the delivery plan: **Irfan**. Technical review: KKT; Rohit for leak and failure checks.
Epic: [#105](https://github.com/Bodhan-AI/open-rachana/issues/105). [Module route](../observability.md).

Qualify the merged local Collector/Grafana stack for another contributor’s clean environment.

## Start here

PR #120 merged deploy/dev and dashboards. The issue is still open; verify remaining acceptance on that implementation.

First deliverable: Run the existing guide on a clean machine instead of rebuilding the stack; record platform prerequisites and any gaps against the issue.

## Inputs and outputs

- Input: deploy/dev configuration from #120, local ports, exporter endpoints and synthetic API requests.
- Output: Documented setup with correlated log/trace/metric views and verified safe reset; remaining missing signal wiring tracked separately.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [DAT-03](../../requirements.md#req-dat-03) | Plaintext content never appears in URLs, analytics, traces, exception messages, infrastructure logs, browser storage, notifications, dashboards or support tickets. | MUST |
| [PRD-OBS-28](../../requirements.md#req-prd-obs-28) | GAP Application observability (§11): structured logs with correlation and trace identifiers and no content; metrics for active sessions, events per second, telemetry backlog, sealing duration and failure count, chain write latency and lag, outbox lag, assignment pool size; dashboards contain no content. | MUST |

## Exact PRD sections

- [11. Non-functional requirements](../../prd/technical-baseline.md#11-non-functional-requirements)
- [14.1 Week 1 — Foundation and evidence backbone](../../prd/technical-baseline.md#141-week-1--foundation-and-evidence-backbone)

## Behaviour to demonstrate

Stop the Collector: core health/domain behaviour remains available. Restart it and verify new synthetic signals appear without editing domain code.

Existing issue acceptance criteria, retained for review:

- [ ] A clean machine starts the stack using the documented command.
- [ ] Synthetic log, metric and trace are visible and linked.
- [ ] Backend changes require Collector/configuration changes, not domain-code changes.

## Dependencies and decisions

No upstream feature is required to prepare the first deliverable.

No product blocker. #120 supplies the stack; final acceptance still requires the requested clean-machine and correlation evidence, including #121’s log wiring.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
