# #49: As the System, I want CI to fail if logs, errors, or audit fixtures contain question content

Owner proposed in the delivery plan: **Rohit**. Technical review: KKT; feature owners.
Epic: [#107](https://github.com/Bodhan-AI/open-rachana/issues/107). [Module route](../testing.md).

Make leakage of synthetic Restricted content fail the build across application logs, audit and diagnostics.

## Start here

PR #98 implements content-leak CI checks. Coordinate with that author.

First deliverable: Continue PR #98 and reuse the merged observability guard tests. Expand coverage to newly added workflow endpoints instead of duplicating the same harness.

## Inputs and outputs

- Input: Data-classification field register, action schemas, synthetic sentinel corpus and captured sinks for stdout, logs, spans, metrics and audit.
- Output: A failing check for any leaked sentinel or forbidden field, a clean positive case and retained CI evidence.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR01-EVD-09](../../requirements.md#req-asr01-evd-09) | Audit events contain no artefact plaintext. | MUST |
| [PRD-EVD-18](../../requirements.md#req-prd-evd-18) | GAP Content ban enforcement (EVD-09): the event schema allowlists detail keys per action; an automated test writes events for every action with Restricted strings in every free field and asserts none is persisted; a log scrubber for known content field names is a second line of defence, never the first. | MUST |
| [ASR02-OBS-17](../../requirements.md#req-asr02-obs-17) | OBS-16 is enforced by an automated test that fails the build — not by reviewer discipline. | MUST |
| [PRD-OBS-21](../../requirements.md#req-prd-obs-21) | GAP Telemetry event schema (Appendix C): event identifier, event type, severity, occurred at, session identifier, actor audit identifier, task reference, client sequence number, blocked flag, score after. The JSON schema forbids additional properties, and the build-failing test (OBS-17) submits events carrying content-like fields and asserts they are rejected, then inspects every persisted and forwarded event for the absence of any string from the synthetic corpus. | MUST |
| [DAT-01](../../requirements.md#req-dat-01) | Artefact text, answers, explanations, assets, review comments and manifests are classified Restricted. | MUST |
| [DAT-03](../../requirements.md#req-dat-03) | Plaintext content never appears in URLs, analytics, traces, exception messages, infrastructure logs, browser storage, notifications, dashboards or support tickets. | MUST |
| [PRD-DAT-10](../../requirements.md#req-prd-dat-10) | GAP Every table carrying Restricted fields is enumerated in a data-classification register checked into the repository; log scrubbing, backup access separation and the no-content tests are generated from that register. | MUST |
| [SEC-14](../../requirements.md#req-sec-14) | Support processes mask Restricted fields. No plaintext reaches tickets, screenshots, analytics or chat. | MUST |
| [ASR02-OBS-16](../../requirements.md#req-asr02-obs-16) | A monitoring event carries only event type, timestamp, session identifier, pseudonymous actor audit identifier and task reference. No stem, option, field value, clipboard payload or screenshot. | MUST |

## Exact PRD sections

- [17. Security](../../prd/main-baseline.md#17-security)
- [19. Evidence and Audit](../../prd/main-baseline.md#19-evidence-and-audit)
- [6.13 Expected evidence and audit · ASR01-EVD](../../prd/technical-baseline.md#613-expected-evidence-and-audit--asr01-evd)
- [6.14 Session integrity, observability and referral · ASR02-OBS](../../prd/technical-baseline.md#614-session-integrity-observability-and-referral--asr02-obs)
- [13.2 Mandated automated suites](../../prd/technical-baseline.md#132-mandated-automated-suites)

## Behaviour to demonstrate

Inject a sentinel into a request path, validation error, exception and event detail. None may appear in any captured sink; deliberately remove a guard in a disposable test to prove detection.

Failure checks: Inject synthetic sentinel text into logs, traces, errors and audit exports; demonstrate that the CI check fails and clean fixtures pass.

Existing issue acceptance criteria, retained for review:

- [ ] `tests/conformance/` scan fails when a stem/option/explanation appears in log fixtures, audit fixtures, or exception strings
- [ ] Scan is part of `build-and-test`
- [ ] A deliberate dirty fixture fails CI

## Dependencies and decisions

Required producer work: [#52](issue-52.md) (Rohit).

No product decision is needed for the content ban. New action fields need explicit classification and schema review.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
