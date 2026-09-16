# #45: As the System, I want every question to have a QB-id, immutable versions, and a closed state machine

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Define artefact identity, immutable versions, lineage and the closed lifecycle used by all workflow services.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Publish the entity and transition tests for DRAFT, submitted review and linked rejection draft; extend the same transition service through later stages.

## Inputs and outputs

- Input: Opaque artefact/version identifiers, current version, prior lineage, actor, command and expected state/token.
- Output: A legal state transition with a new immutable snapshot where required, or a conflict with no mutation; readiness remains separate from per-language state.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [SEC-07](../../requirements.md#req-sec-07) | Invalid lifecycle transitions are rejected with a conflict response and a descriptive message. | MUST |
| [SEC-08](../../requirements.md#req-sec-08) | Submitted, returned and sealed versions are immutable. No deletion operation exists for artefact content. | MUST |
| [PRD-ATH-15](../../requirements.md#req-prd-ath-15) | GAP Content model of a version: stem; ordered options, each with a structural identifier, a body and a correct flag; explanation; classification (subject, unit, topic, difficulty as proposed by the author, taxonomy level); marks; assets with checksum, alternative text and decorative flag. Stem, option bodies and explanation are restricted-HTML documents in which equations are inline equation nodes holding canonical LaTeX and images are asset references. | MUST |

## Exact PRD sections

- [6. Core Concepts](../../prd/main-baseline.md#6-core-concepts)
- [13. Question Lifecycle](../../prd/main-baseline.md#13-question-lifecycle)
- [14. Versioning and Corrections](../../prd/main-baseline.md#14-versioning-and-corrections)
- [5. Domain model and artefact lifecycle](../../prd/technical-baseline.md#5-domain-model-and-artefact-lifecycle)
- [8.2 Entities and required fields](../../prd/technical-baseline.md#82-entities-and-required-fields)

## Behaviour to demonstrate

A direct DRAFT-to-SEALED request fails. Editing the successor of a rejected version never changes the rejected snapshot or its hash.

Failure checks: Try illegal state jumps and stale writes; preserve immutable submitted versions. FULLY_APPROVED is computed readiness, not a language-version state.

Existing issue acceptance criteria, retained for review:

- [ ] IDs are `QB-` + six digits and have no relationship to a final paper number
- [ ] Every substantive change is a new immutable version (old versions never change)
- [ ] States exist: DRAFT, IN_QUESTION_REVIEW, IN_ACCESSIBILITY, IN_ACCESSIBILITY_REVIEW, SEALED, IN_TRANSLATION, IN_TRANSLATION_REVIEW, FULLY_APPROVED, USED, ARCHIVED, WITHDRAWN, RETIRED, SUPERSEDED; REJECTED is a version outcome
- [ ] Illegal transitions fail closed (e.g. DRAFT → SEALED)
- [ ] No human seal, unseal, or read-sealed path exists

## Dependencies and decisions

Required producer work: [#46](issue-46.md) (Gandharva).

R6 affects canonical byte finalisation. Define versioned fields and persistence contracts now; do not relabel draft-v0.1 hashes.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
