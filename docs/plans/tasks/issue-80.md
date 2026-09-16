# #80: As the System, I want FULLY_APPROVED only when the original and every required language are sealed

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Maintain materialised readiness whenever a current seal, policy or lineage input changes.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement a truth table for primary-only and multilingual cycles, then subscribe each relevant state change through the transaction service.

## Inputs and outputs

- Input: Current primary and required-language seals, primary bindings, correction/revalidation/used/retired state and applicable accommodation/exclusion metadata.
- Output: FULLY_APPROVED, NOT_READY or REVOKED record updated with its inputs transactionally, plus readiness.changed.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM07-RDY-01](../../requirements.md#req-asm07-rdy-01) | An artefact is ready only when the current primary and every required language variant are sealed against the same lineage. | MUST |
| [ASM07-RDY-05](../../requirements.md#req-asm07-rdy-05) | Superseded sealed versions remain as evidence but are never returned by new readiness queries. | MUST |
| [ASM07-RDY-06](../../requirements.md#req-asm07-rdy-06) | Where two artefacts must not appear in the same paper, the relationship is recorded and carried on the readiness record. Automated detection of such pairs is out of scope. | SHOULD |
| [PRD-RDY-07](../../requirements.md#req-prd-rdy-07) | GAP The readiness status values are FULLY_APPROVED (engineering name for ready), NOT_READY and REVOKED. The readiness record schema is fixed in §8.2 and Appendix C. It is computed by the rule in §5.4, stored, and updated inside the transaction that changes any of its inputs, so the interface reads a materialized record rather than computing on request. | MUST |
| [PRD-RDY-09](../../requirements.md#req-prd-rdy-09) | GAP D-34 Exclusion pairs (RDY-06): a coordinator records a pair of artefact identifiers with a reason; the pair appears on both readiness records; removal is audited. No detection logic exists. | SHOULD |
| [PRD-RDY-10](../../requirements.md#req-prd-rdy-10) | GAP Every change of readiness emits readiness.changed with the artefact identifier, previous and new status and the reason (sealed, correction, used, retired, revalidation). | MUST |
| [PRD-CFG-11](../../requirements.md#req-prd-cfg-11) | GAP A cycle may have an empty list of required languages (single-language cycle). Readiness then requires only the sealed primary. | MUST |
| [PRD-COR-09](../../requirements.md#req-prd-cor-09) | GAP Readiness is revoked in the same transaction as the authorization (COR-02), and stays revoked until the new primary and every required variant are sealed against it. The reason is carried on readiness.changed. | MUST |
| [ASM04-TRN-05](../../requirements.md#req-asm04-trn-05) | Each language variant receives its own accessibility check and its own sealed artefact. | MUST |

## Exact PRD sections

- [11. Translation](../../prd/main-baseline.md#11-translation)
- [13. Question Lifecycle](../../prd/main-baseline.md#13-question-lifecycle)
- [14. Versioning and Corrections](../../prd/main-baseline.md#14-versioning-and-corrections)
- [6.10 Readiness and handoff to assembly · ASM07-RDY](../../prd/technical-baseline.md#610-readiness-and-handoff-to-assembly--asm07-rdy)

## Behaviour to demonstrate

An old translation sealed against primary hash H1 cannot satisfy readiness after corrected H2 seals. A cycle with no variants is ready after its current primary seals.

Failure checks: Remove one seal, change the required language set and supersede a lineage; readiness must be false for incomplete or stale language seals.

Existing issue acceptance criteria, retained for review:

- [ ] FULLY_APPROVED iff original + every cycle.required_languages version is SEALED
- [ ] Week 4 evidence: one question reaches FULLY_APPROVED in three languages
- [ ] Readiness is a computed record, not a human checkbox

## Dependencies and decisions

Required producer work: [#76](issue-76.md) (Divyansh), [#77](issue-77.md) (Gandharva).

D-17 accommodation treatment and D-34 exclusion-pair scope remain owner settings. Readiness cannot ignore supersession or revalidation.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
