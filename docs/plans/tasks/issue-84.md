# #84: As an Admin, I want to retire an approved question rather than delete it

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Retire approved artefacts with re-authentication, preserved evidence and downstream notification.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement retirement from the allowed states and repeat/refusal tests; connect assembly’s notification consumer.

## Inputs and outputs

- Input: Authorised actor, current artefact, reason, fresh authentication and idempotency key.
- Output: Retired status, revoked readiness, retained sealed hashes/manifests/classification and artefact.retired evidence/event.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [RES06-COR-06](../../requirements.md#req-res06-cor-06) | Retiring an artefact preserves its sealed hash and classification so later analysis remains possible. | SHOULD |
| [PRD-COR-11](../../requirements.md#req-prd-cor-11) | GAP Retirement (COR-06): a re-authenticated Coordinator retires an artefact with a reason; every sealed version keeps its hash, manifest and classification; readiness is revoked; artefact.retired is emitted; there is no un-retire in the MVP. | SHOULD |
| [SEC-08](../../requirements.md#req-sec-08) | Submitted, returned and sealed versions are immutable. No deletion operation exists for artefact content. | MUST |
| [PRD-RDY-10](../../requirements.md#req-prd-rdy-10) | GAP Every change of readiness emits readiness.changed with the artefact identifier, previous and new status and the reason (sealed, correction, used, retired, revalidation). | MUST |

## Exact PRD sections

- [14. Versioning and Corrections](../../prd/main-baseline.md#14-versioning-and-corrections)
- [6.11 Correction and supersession (approval reset) · RES06-COR](../../prd/technical-baseline.md#611-correction-and-supersession-approval-reset--res06-cor)

## Behaviour to demonstrate

Retiring an artefact removes it from new readiness results while its hashes remain verifiable. A repeated request does not create a second retirement or delete bytes.

Failure checks: Attempt retirement without permission and repeat a valid request; preserve content/evidence and revoke readiness with an idempotent notification.

Existing issue acceptance criteria, retained for review:

- [ ] Admin can retire an approved/fully-approved question → RETIRED
- [ ] Nothing is physically deleted
- [ ] Readiness revoked if it was FULLY_APPROVED; assembly notified
- [ ] Drafts still use withdraw, not retire

## Dependencies and decisions

Required producer work: [#80](issue-80.md) (Kaustav), [#81](issue-81.md) (Kaustav).

D-41/PR #97 record the soft-delete rule. There is no un-retire in MVP; restore from backup does not undo the retirement event.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
