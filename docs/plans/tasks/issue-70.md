# #70: As an Accessibility Reviewer, I want to test the rendered question and decide

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Implement independent accessibility review with structured findings and accommodation outcomes.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Provide keyboard/screen-reader evaluation fixtures and test both correction routes, including different specialist/reviewer assignment.

## Inputs and outputs

- Input: Completed remediation version, independent reviewer, checklist, element-level findings, comments and cycle accommodations.
- Output: Approval with no blocking findings requests system sealing; rejection creates the correct author/accessibility correction and preserves the decision.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM04-ACC-01](../../requirements.md#req-asm04-acc-01) | The accessibility specialist tests the same reference rendering intended for downstream candidate delivery, in a read-only mode that cannot alter content. | MUST |
| [ASM04-ACC-02](../../requirements.md#req-asm04-acc-02) | The workspace provides keyboard and screen-reader test affordances against the rendered artefact. | MUST |
| [ASM04-ACC-03](../../requirements.md#req-asm04-acc-03) | Evaluation covers screen-reader compatibility, alternative text, colour contrast, font readability, plain-language clarity, reading order, focus, keyboard operation, tables, equations, and whether the artefact relies solely on visual or auditory cues. | MUST |
| [ASM04-ACC-04](../../requirements.md#req-asm04-acc-04) | Approval requires no unresolved blocking findings and mandatory comments. A return records the affected element and the required remediation. | MUST |
| [ASM04-ACC-05](../../requirements.md#req-asm04-acc-05) | Approval requests sealing into the repository. A return creates a new linked draft. | MUST |
| [ASM04-ACC-06](../../requirements.md#req-asm04-acc-06) | Whether remediation repeats review is policy-driven configuration, defaulting to repeat when content, answer or metadata changed. | MUST |
| [ASM04-ACC-07](../../requirements.md#req-asm04-acc-07) | The decision records which of the cycle's declared accommodations the rendered artefact can be delivered under. | MUST |
| [ASM04-ACC-08](../../requirements.md#req-asm04-acc-08) | An artefact that cannot be delivered under a declared accommodation is recorded as needing an equivalent route, with a reason, and is escalated rather than silently approved. | MUST |
| [ASM04-ACC-09](../../requirements.md#req-asm04-acc-09) | Generation of alternate-format artefacts is out of scope; the data model must not preclude it. | MAY |
| [PRD-ACC-10](../../requirements.md#req-prd-acc-10) | GAP The evaluation checklist implements ACC-03 item by item (table below). Each item is Pass, Fail (with at least one finding) or Not applicable (with reason). | MUST |
| [PRD-ACC-11](../../requirements.md#req-prd-acc-11) | GAP A finding records: element reference (structural identifier or field path), criterion, severity (blocking or advisory), description, required remediation. A return requires at least one blocking finding; an approval requires zero unresolved blocking findings and comments of at least 20 characters. Advisory findings travel to the successor draft as guidance without blocking. | MUST |
| [PRD-ACC-12](../../requirements.md#req-prd-acc-12) | GAP D-17 Accommodation capability: for every accommodation declared by the cycle the decision records deliverable or needs equivalent route with a reason. Any needs equivalent route creates an escalation task for the coordinator with an operational alert. Proposed default: the flag does not block sealing or readiness; it is carried on the readiness record so assembly can respect it. | MUST |
| [PRD-ACC-13](../../requirements.md#req-prd-acc-13) | GAP Test affordances (ACC-02) provided on the reference rendering without altering content: keyboard-only navigation mode with visible focus order; screen-reader-oriented view exposing the accessible name, role and MathML of each element; text-only view; zoom at 200 % and 400 %; contrast measurement per text element; a reading-order outline. | MUST |
| [PRD-ACC-14](../../requirements.md#req-prd-acc-14) | GAP D-07 Remediation routing policy values: always_repeat_review, repeat_when_content_changed (default), never_repeat. "Changed" is defined in §5.4. | MUST |
| [PRD-ACC-15](../../requirements.md#req-prd-acc-15) | GAP To honour ACC-09, renditions are modelled as a separate entity keyed by version, format and status, with the reference rendering as the first format. No code path assumes a single format. | MUST |
| [PRD-ACC-18](../../requirements.md#req-prd-acc-18) | GAP The Accessibility Reviewer decides on the completed accessibility version: approval requests sealing; rejection creates an accessibility-correction draft for a different Accessibility Specialist (accessibility findings) or an authoring-correction draft for the author (authoring findings), and the next accessibility review is by a different Accessibility Reviewer (PRD-ASG-10). | MUST |
| [UI-08](../../requirements.md#req-ui-08) | Accessibility Check — rendered artefact with keyboard and screen-reader affordances, structured findings capture, accommodation capability capture, approve and return. In the converged model this is the Accessibility Reviewer's screen. | MUST |
| [PRD-ACC-16](../../requirements.md#req-prd-acc-16) | GAP Accessibility remediation task (engineering IN_ACCESSIBILITY): on question-review approval the system creates an accessibility draft derived from the approved version and assigns an Accessibility Specialist by policy. The draft exposes only accessibility fields: alternative text and decorative flags, table headers and captions, equation text alternatives, reading-order markup and accessibility metadata. Stem, options, correct flag, explanation, marks, classification, image bytes and mathematical notation are locked and machine-verified unchanged on completion. The specialist completes the evaluation checklist as a self-check, may comment, and completes the task, which creates the immutable version that enters IN_ACCESSIBILITY_REVIEW. | MUST |
| [PRD-ACC-17](../../requirements.md#req-prd-acc-17) | GAP A finding that needs an authoring change (wording, image, notation) is recorded by the specialist as a comment and by the reviewer as an RC-A11Y-* rejection to the author; the specialist never edits those fields. | MUST |

## Exact PRD sections

- [10. Accessibility](../../prd/main-baseline.md#10-accessibility)
- [6.7 Accessibility remediation and review · ASM04-ACC](../../prd/technical-baseline.md#67-accessibility-remediation-and-review--asm04-acc)

## Behaviour to demonstrate

A blocking equation-reading finding prevents approval. An accessibility-only rejection goes to a different specialist; a wording defect returns to the author.

Failure checks: Test the rendered task with keyboard and screen reader; reject self-review and route wording findings through a new author correction.

Existing issue acceptance criteria, retained for review:

- [ ] Can test rendered question with keyboard/SR workflow, record which declared accommodations it works under, comment, approve or reject
- [ ] Cannot edit
- [ ] Approve → sealing of this language version (seal story consumes the event)
- [ ] Reject with finding (element + fix): specialist corrects if it is an a11y field, Admin corrects if wording must change; a *new* Accessibility Reviewer is assigned
- [ ] Cannot act on a question they authored, remediated, or reviewed before

## Dependencies and decisions

Required producer work: [#69](issue-69.md) (Divyansh), [#68](issue-68.md) (Kaustav).

D-17 decides equivalent-route readiness treatment; D-07 routing and R5 rendering remain explicit. Source wording saying the Specialist approves is superseded by R7.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
