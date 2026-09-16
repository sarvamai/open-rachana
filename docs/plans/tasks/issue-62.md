# #62: As an Admin, I want submit refused when the question is too similar to a sealed question

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Perform deterministic similarity checks against the same-language sealed bank without revealing sealed text.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement fixed normalisation/fingerprint fixtures, threshold boundaries and a protected index adapter using synthetic data.

## Inputs and outputs

- Input: Candidate’s normalised stem/options, versioned algorithm/threshold and repository-side restricted fingerprints.
- Output: Pass or VAL-SIM-01 with permitted matched identifiers; no text, snippets or fingerprint download. An unavailable required check cannot count as a pass.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-VAL-06](../../requirements.md#req-asm03-val-06) | Submission runs a deterministic similarity check of the stem and options against every sealed question in the question bank. A match above the configured threshold is a blocking finding naming the matched identifiers. The comparison uses normalized text and is rule-based; no model is involved. | MUST |
| [PRD-VAL-09](../../requirements.md#req-prd-val-09) | GAP D-08 Similarity check design (VAL-06): text is normalized (markup stripped, equations reduced to their LaTeX text, Unicode NFC, case-folded, punctuation removed, whitespace collapsed) and tokenized into words; the fingerprint is the set of 64-bit hashes of word 3-grams over stem plus options. At sealing, the fingerprint of every sealed version is stored in the bank index as Restricted derived data D-31. At submission, the candidate's fingerprint is compared by Jaccard similarity against every sealed fingerprint in the same language across the whole bank; a result at or above the threshold (proposed 0.80) is a blocking VAL-SIM-01 naming the matched artefact identifiers. The computation is exact and reproducible. | MUST |

## Exact PRD sections

- [8.3 Validation before submit](../../prd/main-baseline.md#83-validation-before-submit)
- [6.5 Validation and submission · ASM03-VAL](../../prd/technical-baseline.md#65-validation-and-submission--asm03-val)

## Behaviour to demonstrate

An exact synthetic duplicate is blocked. A match result contains identifiers only. Bank outage stops submit with a safe retryable failure.

Failure checks: Use synthetic sealed-bank fixtures, empty corpus and similarity-service failure. Never return sealed text or silently pass an unavailable required check.

Existing issue acceptance criteria, retained for review:

- [ ] Submit compares against sealed questions only (working drafts are not the corpus)
- [ ] A near-duplicate is refused with a content-free reason (no sealed text shown)
- [ ] Comparison is deterministic / conformance-tested behind the similarity SPI

## Dependencies and decisions

Required producer work: [#61](issue-61.md) (Kaustav), [#45](issue-45.md) (Kaustav).

D-08 algorithm/threshold and D-31 fingerprint storage need approval. Build deterministic fixtures with explicitly declared test configuration.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
