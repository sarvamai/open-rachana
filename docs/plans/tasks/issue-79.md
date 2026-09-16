# #79: As the System, I want sealing the original to create the translation drafts

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Create one current translation draft and task per required language after successful primary sealing.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Use a synthetic sealed-primary event and zero/two required-language configurations; test replay and failure recovery.

## Inputs and outputs

- Input: Primary seal event/hash, current cycle language set, locked source structure and authorised reference-release contract.
- Output: Idempotent per-language lineage/draft/assignment with primary binding; no draft for the primary language or duplicate event.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM04-TRN-01](../../requirements.md#req-asm04-trn-01) | Sealing the primary version creates one question or artefact per required language. | MUST |
| [PRD-TRN-11](../../requirements.md#req-prd-trn-11) | GAP Variant creation is part of the primary's sealing transaction. For each required language a new lineage and Draft are created with: empty target-language stem, option bodies, explanation and alternative text; locked fields copied from the primary (option identifiers and order, correct flag, marks, assets by checksum, canonical equations, classification); primary_reference_hash; and a read-only primary reference snapshot holding the primary's rendering and canonical text, classified Restricted and visible only to the assigned translator and translation reviewer. A translation assignment is created by policy. The snapshot is purged when the variant is sealed. | MUST |
| [PRD-VLT-14](../../requirements.md#req-prd-vlt-14) | GAP Post-seal removal (VLT-05): in the sealing transaction the plaintext working copy of the sealed version is deleted from the authoring-tier store and its rendering caches are purged. Returned and Withdrawn versions are not sealed; they remain immutable in the authoring tier, reachable only as findings context by the author of the successor draft and as metadata by auditors. | MUST |
| [PRD-TRN-16](../../requirements.md#req-prd-trn-16) | GAP Revalidation (TRN-09, RES06-COR-03): when a corrected primary is sealed, each variant lineage is flagged requires_revalidation and a revalidate_variant task is created. Its workspace shows a field-level difference between the previous and new primary reference. The translator produces a new variant version bound to the new primary hash; it passes every gate; readiness returns only when every required language is resealed against the new primary. | MUST |

## Exact PRD sections

- [11. Translation](../../prd/main-baseline.md#11-translation)
- [13. Question Lifecycle](../../prd/main-baseline.md#13-question-lifecycle)
- [6.8 Translation and variant equivalence · ASM04-TRN](../../prd/technical-baseline.md#68-translation-and-variant-equivalence--asm04-trn)

## Behaviour to demonstrate

Deliver the same primary-sealed event twice: exactly one current draft per required language exists. With no required variants, no translation tasks are created.

Failure checks: Replay primary-seal events; create exactly one current task per required language and preserve locked structure without a general vault-read path.

Existing issue acceptance criteria, retained for review:

- [ ] On original SEALED, one IN_TRANSLATION draft is created per required language
- [ ] Assignment story places one translator per language
- [ ] Original bytes are not copied into an editable original; translators see a read view

## Dependencies and decisions

Required producer work: [#77](issue-77.md) (Gandharva), [#67](issue-67.md) (Kaustav).

R8 blocks live Restricted reference construction/purge. Agree with #77 how variant creation and seal completion remain consistent; external writes are not magically one database transaction.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
