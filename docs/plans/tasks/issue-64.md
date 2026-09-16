# #64: As an Admin, I want to withdraw a draft instead of deleting it

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Withdraw an unsubmitted draft without deleting its content or evidence.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Add a draft-only withdrawal command and tests for repeated calls and submitted-version refusal.

## Inputs and outputs

- Input: Authorised actor, draft/version reference, expected current state and idempotency key.
- Output: Withdrawn state, removal from active cap counts, safe receipt and required audit event; retained historical version.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-ATH-11](../../requirements.md#req-asm03-ath-11) | An author can withdraw an unsubmitted draft; withdrawal is audited and removes it from active counts. | MUST |
| [SEC-08](../../requirements.md#req-sec-08) | Submitted, returned and sealed versions are immutable. No deletion operation exists for artefact content. | MUST |

## Exact PRD sections

- [8. Authoring](../../prd/main-baseline.md#8-authoring)
- [14. Versioning and Corrections](../../prd/main-baseline.md#14-versioning-and-corrections)
- [6.4 Authoring · ASM03-ATH](../../prd/technical-baseline.md#64-authoring--asm03-ath)

## Behaviour to demonstrate

Withdrawing DRAFT A decreases its author’s counted total. Calling the same command on submitted B fails and does not delete B.

Failure checks: Attempt to withdraw a submitted/sealed version through the draft path; refuse and retain the original evidence and content.

Existing issue acceptance criteria, retained for review:

- [ ] Admin can withdraw a DRAFT → WITHDRAWN
- [ ] Content is not physically deleted
- [ ] Approved/sealed questions cannot be withdrawn this way (retire is a later story)
- [ ] Action is audited

## Dependencies and decisions

Required producer work: [#53](issue-53.md) (Kaustav), [#42](issue-42.md) (Kaustav).

D-41/PR #97 record the soft-delete policy; no hard-delete route is permitted by the baseline.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
