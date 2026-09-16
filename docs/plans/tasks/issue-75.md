# #75: As a Translation Reviewer, I want original and translation side by side so I can approve or reject

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Implement independent translation review and explicit equivalent-difficulty judgement.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement complete/incomplete equivalence cases and self-review refusal, then the read-only side-by-side workspace.

## Inputs and outputs

- Input: Read-only primary and variant, current assignment, fidelity/terminology/grammar/answer-equivalence checklist and judgement rationale.
- Output: Append-only translation decision; approval creates language-specific accessibility work; rejection returns a new version with findings.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM04-TRN-04](../../requirements.md#req-asm04-trn-04) | Each language variant is reviewed independently for fidelity, terminology, script-specific grammar and answer equivalence. | MUST |
| [ASM04-TRN-07](../../requirements.md#req-asm04-trn-07) | The reviewer records an explicit judgement that the variant is neither easier nor harder than the primary, inside the existing mandatory checklist. No separate workflow step and no additional lifecycle state is introduced. | MUST |
| [PRD-TRN-15](../../requirements.md#req-prd-trn-15) | GAP The translation-review checklist (inside the standard review template) covers fidelity of meaning, glossary terminology, script-specific grammar, answer equivalence (the same option is correct for the same reasons), and the equivalence judgement E1 of §6.6. The reviewer sees the primary reference and the variant side by side, read-only. | MUST |
| [PRD-REV-15](../../requirements.md#req-prd-rev-15) | GAP Decision record fields: identifier; version identifier and version hash; decision type (review, translation review, accessibility); outcome; checklist responses; attestations with sources; reason code; comments; difficulty assigned; equivalence judgement; reviewer audit identifier; capability entry identifier valid at the time; renderer version; policy version; opened at; decided at; duration; correlation identifier. The record's own hash is written into the audit event. | MUST |
| [PRD-ASG-10](../../requirements.md#req-prd-asg-10) | GAP Different reviewer after rejection (engineering PRD): the successor version of a rejected version is assigned, at the same stage, to a reviewer other than the one who rejected it and other than any earlier rejecting reviewer of that lineage. If no other eligible reviewer exists the task stays Unassigned and the Admin is alerted; the Admin cannot override this rule. | MUST |

## Exact PRD sections

- [11. Translation](../../prd/main-baseline.md#11-translation)
- [6.8 Translation and variant equivalence · ASM04-TRN](../../prd/technical-baseline.md#68-translation-and-variant-equivalence--asm04-trn)
- [6.6 Question review · ASM03-REV](../../prd/technical-baseline.md#66-question-review--asm03-rev)

## Behaviour to demonstrate

A translation can be grammatically sound but lacks equivalent-difficulty judgement: approval is refused. A translator cannot approve their own variant through the API.

Failure checks: Attempt own-translation approval and editing via the review API; preserve rejection history and assign a different reviewer after correction.

Existing issue acceptance criteria, retained for review:

- [ ] Side-by-side original and translation
- [ ] Comment, approve, reject — cannot edit
- [ ] Cannot review a translation they wrote
- [ ] Reject → translator corrects → a *new* Translation Reviewer is assigned
- [ ] Approve → accessibility for that language
- [ ] Reviewer confirms the translation is not easier and not harder than the original

## Dependencies and decisions

Required producer work: [#74](issue-74.md) (Kaustav), [#68](issue-68.md) (Kaustav).

R8 controls reference release and R5 rendering. Checklist text is D-19; no new equivalence lifecycle state is introduced.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
