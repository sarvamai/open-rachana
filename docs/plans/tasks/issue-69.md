# #69: As an Accessibility Specialist, I want to remediate accessibility fields only

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Build field-limited accessibility remediation and immutable completion by the Accessibility Specialist.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement the server field allowlist and unchanged-content comparison before exposing the remediation controls.

## Inputs and outputs

- Input: Assigned approved version, accessible rendering, locked source fields, alt/decorative/table/equation-alternative/reading-order fields and self-check.
- Output: Completed immutable accessibility version, comments and checklist, followed by independent accessibility review.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ACC-16](../../requirements.md#req-prd-acc-16) | GAP Accessibility remediation task (engineering IN_ACCESSIBILITY): on question-review approval the system creates an accessibility draft derived from the approved version and assigns an Accessibility Specialist by policy. The draft exposes only accessibility fields: alternative text and decorative flags, table headers and captions, equation text alternatives, reading-order markup and accessibility metadata. Stem, options, correct flag, explanation, marks, classification, image bytes and mathematical notation are locked and machine-verified unchanged on completion. The specialist completes the evaluation checklist as a self-check, may comment, and completes the task, which creates the immutable version that enters IN_ACCESSIBILITY_REVIEW. | MUST |
| [PRD-ACC-17](../../requirements.md#req-prd-acc-17) | GAP A finding that needs an authoring change (wording, image, notation) is recorded by the specialist as a comment and by the reviewer as an RC-A11Y-* rejection to the author; the specialist never edits those fields. | MUST |
| [PRD-UI-08a](../../requirements.md#req-prd-ui-08a) | GAP Accessibility Remediation — the Accessibility Specialist's screen: rendered artefact with the same test affordances, an editor limited to accessibility fields (alternative text, decorative flags, table headers and captions, equation text alternatives, reading order), the self-check checklist, comments, and Complete. Locked fields are shown read-only and visibly locked. | MUST |
| [PRD-ACC-18](../../requirements.md#req-prd-acc-18) | GAP The Accessibility Reviewer decides on the completed accessibility version: approval requests sealing; rejection creates an accessibility-correction draft for a different Accessibility Specialist (accessibility findings) or an authoring-correction draft for the author (authoring findings), and the next accessibility review is by a different Accessibility Reviewer (PRD-ASG-10). | MUST |
| [PRD-ACC-10](../../requirements.md#req-prd-acc-10) | GAP The evaluation checklist implements ACC-03 item by item (table below). Each item is Pass, Fail (with at least one finding) or Not applicable (with reason). | MUST |

## Exact PRD sections

- [10. Accessibility](../../prd/main-baseline.md#10-accessibility)
- [6.7 Accessibility remediation and review · ASM04-ACC](../../prd/technical-baseline.md#67-accessibility-remediation-and-review--asm04-acc)

## Behaviour to demonstrate

Changing alt text is permitted; changing an option body, correct flag or image bytes in the same request is refused. A wording problem is returned through the authoring route.

Failure checks: Attempt to change stem, options, key and marks through remediation fields; reject and preserve the immutable source version.

Existing issue acceptance criteria, retained for review:

- [ ] Can add/edit alternative text, mark decorative images, add table headers/captions, add equation text descriptions, fix reading order, comment, complete the task
- [ ] Cannot change wording, options, answer, marks, mathematical notation, or replace images
- [ ] Cannot approve or reject
- [ ] Completing the task sends the item to Accessibility Review

## Dependencies and decisions

Required producer work: [#66](issue-66.md) (Kaustav).

R5 controls reference rendering; D-07 controls routing after content changes. Specialist completion is never approval.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
