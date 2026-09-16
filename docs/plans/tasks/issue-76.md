# #76: As an Accessibility Specialist, I want the same accessibility gate on every language version

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Apply the accessibility remediation and independent review pipeline to each language variant.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Reuse #69/#70 contracts with target-language fixtures and prove that the primary’s approval cannot satisfy the variant check.

## Inputs and outputs

- Input: Translation-reviewed variant, target-language alternatives/captions, cycle accommodations and task eligibility.
- Output: Separate remediation and review evidence tied to the variant hash, followed by its own seal request.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ACC-19](../../requirements.md#req-prd-acc-19) | GAP D-43 Every language version — the primary and each variant — has its own remediation task and review (ASM04-TRN-05). For variants the remediation is normally limited to translated alternative text and captions. | MUST |
| [ASM04-TRN-05](../../requirements.md#req-asm04-trn-05) | Each language variant receives its own accessibility check and its own sealed artefact. | MUST |
| [PRD-ACC-16](../../requirements.md#req-prd-acc-16) | GAP Accessibility remediation task (engineering IN_ACCESSIBILITY): on question-review approval the system creates an accessibility draft derived from the approved version and assigns an Accessibility Specialist by policy. The draft exposes only accessibility fields: alternative text and decorative flags, table headers and captions, equation text alternatives, reading-order markup and accessibility metadata. Stem, options, correct flag, explanation, marks, classification, image bytes and mathematical notation are locked and machine-verified unchanged on completion. The specialist completes the evaluation checklist as a self-check, may comment, and completes the task, which creates the immutable version that enters IN_ACCESSIBILITY_REVIEW. | MUST |
| [PRD-ACC-18](../../requirements.md#req-prd-acc-18) | GAP The Accessibility Reviewer decides on the completed accessibility version: approval requests sealing; rejection creates an accessibility-correction draft for a different Accessibility Specialist (accessibility findings) or an authoring-correction draft for the author (authoring findings), and the next accessibility review is by a different Accessibility Reviewer (PRD-ASG-10). | MUST |

## Exact PRD sections

- [10. Accessibility](../../prd/main-baseline.md#10-accessibility)
- [11. Translation](../../prd/main-baseline.md#11-translation)
- [6.7 Accessibility remediation and review · ASM04-ACC](../../prd/technical-baseline.md#67-accessibility-remediation-and-review--asm04-acc)
- [6.8 Translation and variant equivalence · ASM04-TRN](../../prd/technical-baseline.md#68-translation-and-variant-equivalence--asm04-trn)

## Behaviour to demonstrate

Primary and two translations have review approvals but one variant lacks accessibility review: that variant cannot seal and the artefact cannot become ready.

Failure checks: Attempt readiness with a language accessibility approval missing; refuse. Any proposed exception requires explicit owner review, not an implicit bypass.

Existing issue acceptance criteria, retained for review:

- [ ] After translation review approve, the language version enters Accessibility Specialist → Accessibility Reviewer
- [ ] Same field restrictions and SoD as the original-language gate
- [ ] A cycle that skips this gate must persist a recorded decision (default is keep the gate)

## Dependencies and decisions

Required producer work: [#75](issue-75.md) (Divyansh), [#70](issue-70.md) (Divyansh).

D-43 is the source per-language requirement; a pilot deferral must be an explicit scope decision. R5 rendering qualification applies to each supported script.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
