# #60: As an Admin, I cannot copy, cut, paste, print, download, or export question content

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Enforce and report supported restricted actions in the signed content client before the editor starts.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Wire copy/cut/paste/context-menu/print controls around the editor and test signal capture plus ingest outage on the native client.

## Inputs and outputs

- Input: Approved capture policy, enrolled device context and authenticated integrity session from #50.
- Output: Blocked-action feedback and content-free durable integrity signals for supported actions, with separately documented OS limitations.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-ATH-10](../../requirements.md#req-asm03-ath-10) | The interface exposes no download, print, bulk export or persistent browser-storage capability. Every artefact is stored on the server immediately, leaving no residual copy on the author's machine. | MUST |
| [PRD-ATH-21](../../requirements.md#req-prd-ath-21) | GAP D-21 The hardened editor region is visually marked. Inside it copy, cut, paste, drag-and-drop of text, context menu and print are blocked and reported (§6.14). Text selection remains possible for editing. The user receives non-blocking feedback that the action was blocked and recorded. | MUST |
| [ASR02-OBS-02](../../requirements.md#req-asr02-obs-02) | The client captures and reports: copy, cut, paste, context menu, print, screenshot key combinations, developer tools opened, viewport anomaly consistent with a docked inspector, window or tab focus loss, page visibility change, concurrent-tab detection, and heartbeat gap. | MUST |
| [ASR02-OBS-03](../../requirements.md#req-asr02-obs-03) | Each captured action is blocked where technically possible and reported whether or not blocking succeeded. | MUST |
| [ASR02-OBS-04](../../requirements.md#req-asr02-obs-04) | The user receives immediate non-blocking feedback that the action was blocked and recorded. Feedback must not interrupt typing. | MUST |
| [PRD-OBS-22](../../requirements.md#req-prd-obs-22) | GAP Client capture mechanics: copy, cut and paste listeners that prevent the default action and report; a context-menu listener that prevents and reports; key listeners for print and platform screenshot combinations that prevent where the browser allows and always report; developer-tools detection by viewport-delta and timing heuristics reported as viewport anomaly and, when confirmed, developer tools opened; visibility-change and blur listeners; concurrent-tab detection through a same-origin channel; heartbeat gap computed server-side. The capture library is loaded before the editor and the editor does not initialize without it. | MUST |
| [UI-05](../../requirements.md#req-ui-05) | Authoring — a session integrity panel shows the current score, signal counts and a recent-event list, so the author knows exactly what is recorded. | MUST |

## Exact PRD sections

- [8.2 Editor rules](../../prd/main-baseline.md#82-editor-rules)
- [17. Security](../../prd/main-baseline.md#17-security)
- [18. Session Monitoring](../../prd/main-baseline.md#18-session-monitoring)
- [6.4 Authoring · ASM03-ATH](../../prd/technical-baseline.md#64-authoring--asm03-ath)
- [6.14 Session integrity, observability and referral · ASR02-OBS](../../prd/technical-baseline.md#614-session-integrity-observability-and-referral--asr02-obs)

## Behaviour to demonstrate

Attempt paste: the editor does not change and feedback appears without interrupting typing. No clipboard payload enters the event, even if posting it must retry.

Failure checks: Exercise supported blocked actions in the signed client and confirm a content-free operator signal; browser-only tests do not prove desktop controls.

Existing issue acceptance criteria, retained for review:

- [ ] Copy, cut, paste, print, download, export are blocked in the content surface
- [ ] Each blocked action is recorded and appears on the operator/session audit (content-free)
- [ ] Week 2 evidence: a copy attempt is blocked and visible to the operator

## Dependencies and decisions

Required producer work: [#50](issue-50.md) (Kaustav), [#58](issue-58.md) (Divyansh).

D-21/D-37 and R9 govern capture policy. Do not add camera capture or replay; browser heuristics do not prove all screenshot/leak prevention.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
