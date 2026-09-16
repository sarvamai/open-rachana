# #55: As an Admin, I want to define a blueprint for an assessment

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Record generation blueprints and translate their counts and constraints into independent candidate requests.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement a validated blueprint object and the deterministic count calculation, with a request fixture consumed by #56.

## Inputs and outputs

- Input: Cycle and curriculum references, item type, marks, required count, candidate multiplier, weightage, Bloom level, difficulty, objective, competency and language.
- Output: Versioned generation configuration and requested candidate count; validation errors for invalid/stale parameters. No final paper selection or export.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ATH-25](../../requirements.md#req-prd-ath-25) | GAP D-38 Generated candidates: a generation request by the Admin (curriculum, cycle, question type, marks, required count × candidate multiplier) produces independent artefacts, each with one DRAFT of provenance generated, owned by the requesting Admin. Every generated draft records generation identifier, model identifier, generation configuration, source curriculum, chapter, page range, stored source context, and timestamp. A generated draft that fails the automated validation catalogue (§6.5) is discarded before any human sees it. Generated drafts are never grouped as alternatives of one question. The generation service runs outside the hardened zones and never receives content from the pipeline. | MUST |
| [PRD-CFG-06](../../requirements.md#req-prd-cfg-06) | GAP The cycle record carries, in addition to CFG-01: author cap per cycle; required review count (1 or 2) D-06; whether reviewers see the correct answer D-06; remediation-repeats-review policy D-07; assignment expiry per task type D-12; similarity threshold D-08; default marks per item from the marking policy; a monotonically increasing policy_version that increments on every change. | MUST |
| [PRD-ATH-27](../../requirements.md#req-prd-ath-27) | GAP D-44 Question types: single-select multiple choice is fully supported. Other types the blueprint may name (for example short answer) are stored with the same content model minus options, and may enter the pipeline only when the cycle enables them; the validation and structural rule sets for such types are reduced accordingly and named per type. | SHOULD |

## Exact PRD sections

- [6. Core Concepts](../../prd/main-baseline.md#6-core-concepts)
- [7. Question Generation (Layer 2)](../../prd/main-baseline.md#7-question-generation-layer-2)
- [1.5 Two-layer architecture at a glance](../../prd/technical-baseline.md#15-two-layer-architecture-at-a-glance)

## Behaviour to demonstrate

For a synthetic request of 5 items with multiplier 3, request 15 independent candidates. Changing the generation pool never selects or orders a final paper.

Failure checks: Try zero/negative/invalid counts and stale cycle data. Confirm count × multiplier produces independent candidate requests, never a final paper.

Existing issue acceptance criteria, retained for review:

- [ ] Blueprint captures: question type, marks, number required, candidate multiplier, weightage, Bloom, difficulty, learning objective, competency, language
- [ ] Candidates generated = required × multiplier, as independent questions (never grouped as alternatives)
- [ ] Blueprint does not assemble a paper or assign final question numbers

## Dependencies and decisions

Required producer work: [#44](issue-44.md) (Kaustav).

R3 is settled. D-44 governs enabling other item types; non-MCQ generation must not bypass type-specific validation.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
