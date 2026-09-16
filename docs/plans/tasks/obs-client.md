# #113: Add bounded browser and signed-client diagnostic telemetry

Owner proposed in the delivery plan: **Irfan**. Technical review: KKT; Rohit for leak and failure checks.
Epic: [#105](https://github.com/Bodhan-AI/open-rachana/issues/105). [Module route](../observability.md).

Add bounded diagnostics to browser oversight and the signed client under their separate runtime constraints.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Instrument one load/error path with a sentinel corpus; add native-client instrumentation only through the accepted client contract.

## Inputs and outputs

- Input: Approved navigation/load/error events, resource attributes and the task/session contract; no DOM/content capture.
- Output: Content-free diagnostic signals with tested native/browser coverage and independent durable integrity capture.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [DAT-03](../../requirements.md#req-dat-03) | Plaintext content never appears in URLs, analytics, traces, exception messages, infrastructure logs, browser storage, notifications, dashboards or support tickets. | MUST |
| [ASR02-OBS-16](../../requirements.md#req-asr02-obs-16) | A monitoring event carries only event type, timestamp, session identifier, pseudonymous actor audit identifier and task reference. No stem, option, field value, clipboard payload or screenshot. | MUST |
| [ASM03-ATH-10](../../requirements.md#req-asm03-ath-10) | The interface exposes no download, print, bulk export or persistent browser-storage capability. Every artefact is stored on the server immediately, leaving no residual copy on the author's machine. | MUST |

## Exact PRD sections

- [6.14 Session integrity, observability and referral · ASR02-OBS](../../prd/technical-baseline.md#614-session-integrity-observability-and-referral--asr02-obs)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)

## Behaviour to demonstrate

A rendering error containing synthetic text exports a safe error classification only. Disabling diagnostics does not disable required integrity capture.

Existing issue acceptance criteria, retained for review:

- [ ] No DOM snapshots, replay, input values or question text are exported.
- [ ] Only approved opaque identifiers appear.
- [ ] Browser results and native-client results are recorded separately.

## Dependencies and decisions

Required producer work: [#112](obs-next.md) (Irfan), [#118](client-contract.md) (Divyansh).

R9 forbids inferring camera/replay authorisation; R5/client packaging controls runtime integration. Browser tests cannot establish native guarantees.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
