# #40: As Product Owner, I want Week-1 product decisions recorded as ADRs

Owner proposed in the delivery plan: **Nikhil**. Technical review: KKT for technical steps; Rohit for testability.
Epic: [#108](https://github.com/Bodhan-AI/open-rachana/issues/108). [Module route](../product.md).

Maintain the product decision record and resolve the specific contradictions affecting the first implementation slices.

## Start here

PR #97 records product ADRs and has requested changes. Its proposals are not yet merged approvals.

First deliverable: Review #97 against the current source and existing ADR numbers. Record only actual owner decisions; avoid creating a second competing decision PR.

## Inputs and outputs

- Input: Existing D-01 through D-48 register, R1 through R12 reconciliation, owner answers and in-flight PR #97.
- Output: Dated decisions with actor, scope, affected requirements and effective policy; unresolved recommendations remain labelled.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INT-09](../../requirements.md#req-int-09) | A role-by-operation permission matrix is authored, implemented, and used as the test oracle for authorization. | MUST |

## Exact PRD sections

- [20. Decisions](../../prd/main-baseline.md#20-decisions)
- [23. Open Questions](../../prd/main-baseline.md#23-open-questions)
- [15. Decision register](../../prd/technical-baseline.md#15-decision-register)

## Behaviour to demonstrate

The main PRD forbids Admin review approval. An older matrix must not silently grant it; show the effective rule and the superseded source in the decision record.

Failure checks: Verify every recorded decision distinguishes an accepted owner decision from a recommendation. The separate Author role/adoption question stays open.

Existing issue acceptance criteria, retained for review:

- [ ] ADR exists: no download/print/copy/export from the question bank; paper export is assembly
- [ ] ADR exists: delete means withdraw (draft) or retire (approved); nothing is permanently deleted
- [ ] ADR exists: Admin may view all questions until sealed; metadata only after sealing
- [ ] Permission matrix confirms Admin never approves or rejects (D-46)
- [ ] `docs/traceability.md` points at the ADRs

## Dependencies and decisions

No upstream feature is required to prepare the first deliverable.

R4/R5/R6/R8/R12 need their listed owners. This task records decisions; it does not grant Security approval.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
