# #114: Add workflow dashboards and tested operational alerts

Owner proposed in the delivery plan: **Irfan**. Technical review: KKT; Rohit for leak and failure checks.
Epic: [#105](https://github.com/Bodhan-AI/open-rachana/issues/105). [Module route](../observability.md).

Create dashboards and actionable alerts for actual workflow services as they arrive.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Start from the merged service/guard/runtime dashboards; add one real producer and failure alert at a time after its workflow merges.

## Inputs and outputs

- Input: Safe metrics/events for assignment pools, audit latency, outbox lag, telemetry backlog, sealing failures/duration and active sessions.
- Output: Dashboards with units and real source labels, tested alerts and linked runbooks/operational owners.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-OBS-28](../../requirements.md#req-prd-obs-28) | GAP Application observability (§11): structured logs with correlation and trace identifiers and no content; metrics for active sessions, events per second, telemetry backlog, sealing duration and failure count, chain write latency and lag, outbox lag, assignment pool size; dashboards contain no content. | MUST |
| [PRD-NTF-03](../../requirements.md#req-prd-ntf-03) | Alerts to the monitoring platform: security events (authorization denial outside assignment, device posture failure, not provisioned, threshold referral, malicious upload, hash mismatch) and operational alerts (sealing failure after retries, chain verification failure, expected evidence missing, supersession unacknowledged, telemetry backlog beyond 60 seconds, unassigned task beyond the delay). Each carries identifiers, codes and counts only. | MUST |
| [PRD-NTF-01](../../requirements.md#req-prd-ntf-01) | In-app notifications exist for: new assignment; task returned with findings; task approaching expiry (24 hours before); exception approved, revoked or expired; correction authorized (coordinator); equivalent-route escalation (coordinator); sealing failure (coordinator and operations); supersession unacknowledged (operations); assignment pool empty (coordinator). | MUST |
| [PRD-NTF-02](../../requirements.md#req-prd-ntf-02) | No notification in any channel contains artefact content, a correct answer, or a rendering. Out-of-band channels D-19 carry only the task type and a link. | MUST |

## Exact PRD sections

- [6.14 Session integrity, observability and referral · ASR02-OBS](../../prd/technical-baseline.md#614-session-integrity-observability-and-referral--asr02-obs)
- [6.15 Notifications and alerts (cross-cutting)](../../prd/technical-baseline.md#615-notifications-and-alerts-cross-cutting)
- [11. Non-functional requirements](../../prd/technical-baseline.md#11-non-functional-requirements)

## Behaviour to demonstrate

Induce a sealing dependency failure: the alert names an opaque job/code and gives a recovery procedure without including question content.

Existing issue acceptance criteria, retained for review:

- [ ] Dashboards show the agreed domain measures with no question content.
- [ ] An induced failure triggers an actionable alert linked to a runbook.
- [ ] Synthetic dashboard data is labelled and cannot close real-flow acceptance.

## Dependencies and decisions

Required producer work: [#110](obs-python.md) (Irfan), [#63](issue-63.md) (Kaustav), [#77](issue-77.md) (Gandharva).

Alert thresholds without a source value need explicit operational configuration. Synthetic panels must be labelled and cannot close real-flow acceptance.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
