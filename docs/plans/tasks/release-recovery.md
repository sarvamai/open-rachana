# #116: Prove failed-release recovery without losing audit or sealed content

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Define and demonstrate safe recovery from a failed application/schema release.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Choose a reversible additive migration for the first drill and deliberately fail deployment after it; exercise the documented recovery path.

## Inputs and outputs

- Input: Release versions, schema compatibility plan, migration checkpoints, restore procedures and immutable audit/sealed stores.
- Output: Tested rollback or forward-recovery runbook, compatibility limits, recovery owner and evidence of preserved accepted state.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [DAT-06](../../requirements.md#req-dat-06) | The canonical schema is versioned, and a stated migration approach preserves verifiability of already-sealed artefacts. | MUST |
| [SEC-13](../../requirements.md#req-sec-13) | Backups are encrypted, access-separated, immutable, and restoration is tested. | MUST |

## Exact PRD sections

- [8.4 Canonicalization rule v1](../../prd/technical-baseline.md#84-canonicalization-rule-v1)
- [10.7 Egress, secrets, environments](../../prd/technical-baseline.md#107-egress-secrets-environments)
- [11. Non-functional requirements](../../prd/technical-baseline.md#11-non-functional-requirements)
- [17.4 Release](../../prd/technical-baseline.md#174-release)

## Behaviour to demonstrate

A rollback must not delete newly accepted audit events or rewrite sealed hashes. If an old binary cannot read the new schema, the plan uses approved forward recovery.

Existing issue acceptance criteria, retained for review:

- [ ] A failed release is recovered in the shared environment.
- [ ] Accepted audit records and sealed artefacts are neither deleted nor rewritten.
- [ ] Recovery steps, compatibility limits and named operational sign-off are retained.

## Dependencies and decisions

Required producer work: [#51](issue-51.md) (KKT), [#77](issue-77.md) (Gandharva).

KKT proposes deployment mechanics; Operations/Security accept the recovery procedure. Do not treat a destructive down-migration as a universal rollback.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
