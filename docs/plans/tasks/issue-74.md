# #74: As a Translator, I want submit blocked if I change locked structure, numbers, or media

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Implement all structural translation checks and scoped, expiring exception enforcement.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Build one failing fixture per STR code and the active/expired/revoked/wrong-check exception cases before wiring submit.

## Inputs and outputs

- Input: Primary/variant canonical structure, fixed numeric/unit/symbol grammars and exception record with requester/approver/check codes/expiry.
- Output: Blocking STR-01 through STR-11 findings or a validated submission with applicable exception identifiers recorded in evidence.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM04-TRN-03](../../requirements.md#req-asm04-trn-03) | Option mapping, correct-answer semantics, marks, assets, equations and structural identifiers are locked and machine-verified on submission. | MUST |
| [ASM04-TRN-06](../../requirements.md#req-asm04-trn-06) | Deterministic checks run on submission and block it where the variant diverges structurally from the primary: option count and mapping, correct-answer position, marks, asset set, canonical equation set, and every numeric value, unit and symbol. | MUST |
| [ASM04-TRN-08](../../requirements.md#req-asm04-trn-08) | A blocked structural check can be overridden only by a recorded exception carrying justification and an expiry date, consistent with ASR-04. The override is audited. | MUST |
| [ASM04-TRN-10](../../requirements.md#req-asm04-trn-10) | Coordinators see language status and artefact ownership, never sealed content. | MUST |
| [PRD-TRN-13](../../requirements.md#req-prd-trn-13) | GAP Structural check catalogue (TRN-06), each blocking and named in the response: STR-01 option count equal; STR-02 option identifier set and order equal; STR-03 correct-answer position equal; STR-04 marks equal; STR-05 asset set by checksum equal; STR-06 canonical equation multiset equal; STR-07 numeric value multiset equal (numbers including decimals, negatives and percentages, extracted by a fixed grammar); STR-08 unit multiset equal (from a maintained unit lexicon); STR-09 symbol multiset equal (non-alphabetic Unicode symbols from a fixed set); STR-10 table dimensions equal; STR-11 every primary image has alternative text in the variant unless decorative. | MUST |
| [PRD-TRN-14](../../requirements.md#req-prd-trn-14) | GAP D-15 Exception record: identifier; version identifier; check codes covered; justification (at least 50 characters); requested by; approved by (a Coordinator, re-authenticated, different from the requester); created at; expires at (at most the configured maximum, proposed 30 days); status Active, Expired, Revoked or Consumed; audit references. Only an Active exception matching the failing check code permits the submission; the exception identifier is recorded on the decision and in the manifest. An hourly sweep expires exceptions. An attempted override without a valid exception returns EXCEPTION_REQUIRED. | MUST |
| [PRD-TRN-11](../../requirements.md#req-prd-trn-11) | GAP Variant creation is part of the primary's sealing transaction. For each required language a new lineage and Draft are created with: empty target-language stem, option bodies, explanation and alternative text; locked fields copied from the primary (option identifiers and order, correct flag, marks, assets by checksum, canonical equations, classification); primary_reference_hash; and a read-only primary reference snapshot holding the primary's rendering and canonical text, classified Restricted and visible only to the assigned translator and translation reviewer. A translation assignment is created by policy. The snapshot is purged when the variant is sealed. | MUST |

## Exact PRD sections

- [11. Translation](../../prd/main-baseline.md#11-translation)
- [6.8 Translation and variant equivalence · ASM04-TRN](../../prd/technical-baseline.md#68-translation-and-variant-equivalence--asm04-trn)

## Behaviour to demonstrate

Changing marks fails STR-04. An Active exception for STR-07 does not permit the marks change. The requester cannot approve their own exception.

Failure checks: Change each locked structural element; refuse without an authorised, unexpired exception covering that exact change.

Existing issue acceptance criteria, retained for review:

- [ ] Locked: number and order of options; which option is correct; marks; every number, unit and symbol; every equation; every image
- [ ] A failed check blocks submit and names the check
- [ ] Only a recorded Admin exception with an expiry date can override a named check

## Dependencies and decisions

Required producer work: [#73](issue-73.md) (Divyansh).

D-15/D-23 fix exception policy and numeral handling. Use configurable limits; do not allow a blanket bypass of structural checks.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
