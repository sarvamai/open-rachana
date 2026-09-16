# #73: As a Translator, I want to create and edit a translation after the original is sealed

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Build the translation workspace around a scoped read-only primary reference and editable target text.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement the screen against synthetic task payloads with locked option mapping; integrate real primary release only after R8 is decided.

## Inputs and outputs

- Input: Assigned variant, primary_reference_hash, authorised primary snapshot, language glossary and locked structural identifiers.
- Output: Target-language draft with only translatable fields editable, locked tokens, autosave state and primary-change summary for revalidation.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM04-TRN-02](../../requirements.md#req-asm04-trn-02) | Translators edit only target-language fields, besides a read-only primary reference and the supplied glossary. | MUST |
| [PRD-TRN-12](../../requirements.md#req-prd-trn-12) | GAP D-23 The translation editor exposes only translatable text: stem, option bodies, explanation, alternative text, table cell text and captions. Numbers, units, symbols, equations and image references appear as locked tokens that cannot be edited or removed. Proposed default: numeric values are preserved verbatim (no localized numerals); an exception is the only route to change one. | MUST |
| [PRD-TRN-17](../../requirements.md#req-prd-trn-17) | GAP The coordinator's language status view lists, per artefact, each language's state, current assignee and age. It shows names for assignment purposes but never content, never the correct answer, and never a rendering. | MUST |
| [UI-09](../../requirements.md#req-ui-09) | Translation — side-by-side read-only primary and editable target language, glossary reference, structural lock indicators, and a change summary when revalidation is required. | MUST |
| [PRD-TRN-11](../../requirements.md#req-prd-trn-11) | GAP Variant creation is part of the primary's sealing transaction. For each required language a new lineage and Draft are created with: empty target-language stem, option bodies, explanation and alternative text; locked fields copied from the primary (option identifiers and order, correct flag, marks, assets by checksum, canonical equations, classification); primary_reference_hash; and a read-only primary reference snapshot holding the primary's rendering and canonical text, classified Restricted and visible only to the assigned translator and translation reviewer. A translation assignment is created by policy. The snapshot is purged when the variant is sealed. | MUST |
| [PRD-TRN-16](../../requirements.md#req-prd-trn-16) | GAP Revalidation (TRN-09, RES06-COR-03): when a corrected primary is sealed, each variant lineage is flagged requires_revalidation and a revalidate_variant task is created. Its workspace shows a field-level difference between the previous and new primary reference. The translator produces a new variant version bound to the new primary hash; it passes every gate; readiness returns only when every required language is resealed against the new primary. | MUST |

## Exact PRD sections

- [11. Translation](../../prd/main-baseline.md#11-translation)
- [6.8 Translation and variant equivalence · ASM04-TRN](../../prd/technical-baseline.md#68-translation-and-variant-equivalence--asm04-trn)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)

## Behaviour to demonstrate

The translator changes target wording but cannot edit the primary or remove a numeric locked token. An unassigned translator cannot open the reference.

Failure checks: Try opening a variant before primary seal, modifying the original and accessing an unassigned reference; refuse outside the approved task contract.

Existing issue acceptance criteria, retained for review:

- [ ] Translation tasks appear only after the original is sealed
- [ ] One translator per language; original is never replaced
- [ ] Each language has its own translation, translator, version, review status, reviewer, comments, approval history
- [ ] Translator can view the original, edit translated text, submit for translation review
- [ ] Translator cannot approve their own work

## Dependencies and decisions

Required producer work: [#79](issue-79.md) (Kaustav).

R8 blocks live primary-reference access; R5 controls rendering. D-48 applies only to AI assistance, so manual UI development can proceed with synthetic fixtures.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
