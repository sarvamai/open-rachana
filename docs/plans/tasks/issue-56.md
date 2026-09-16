# #56: As an Admin, I want Layer 2 to draft candidate questions from the curriculum and blueprint

Owner proposed in the delivery plan: **Sarvam team — individual lead to be confirmed**. Technical review: Kaustav; Security for translation hosting.
Epic: [#109](https://github.com/Bodhan-AI/open-rachana/issues/109). [Module route](../intelligence.md).

Integrate Layer 2 generation as untrusted proposals with provenance and deterministic validation.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Publish request/response fixtures and a provider double; validate malformed and invalid outputs before wiring the pilot service.

## Inputs and outputs

- Input: Approved curriculum references and blueprint parameters from #54/#55; provider response including model/configuration/source references.
- Output: One independent artefact per accepted candidate with provenance; invalid candidates discarded before human visibility; retriable job state without duplicate drafts.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ATH-25](../../requirements.md#req-prd-ath-25) | GAP D-38 Generated candidates: a generation request by the Admin (curriculum, cycle, question type, marks, required count × candidate multiplier) produces independent artefacts, each with one DRAFT of provenance generated, owned by the requesting Admin. Every generated draft records generation identifier, model identifier, generation configuration, source curriculum, chapter, page range, stored source context, and timestamp. A generated draft that fails the automated validation catalogue (§6.5) is discarded before any human sees it. Generated drafts are never grouped as alternatives of one question. The generation service runs outside the hardened zones and never receives content from the pipeline. | MUST |
| [PRD-ATH-26](../../requirements.md#req-prd-ath-26) | GAP Metadata (engineering PRD §9.2): in addition to classification, a version carries grade, curriculum reference, learning objective, competency, question type, language, source curriculum, chapter, page range and source context, status, version number, created and updated timestamps, and — where generated — generation identifier, model and configuration. Source context text is Restricted and is never shown to reviewers (D-47). | MUST |
| [PRD-ARC-13](../../requirements.md#req-prd-arc-13) | GAP D-38 Scope of ARC-12 after the decision: it binds Layer 1 (every zone in §10.1). Layer 2 is the only place a model runs. The connector is a client of Layer 2 with these properties: outbound only; requests carry curriculum references and parameters, never sealed content; responses are treated as untrusted input and pass sanitization, validation and the human gates; Layer 2 holds no credential for any Layer 1 store or endpoint; the AI-dependency scan (§13.2) fails the build if a model runtime or inference client appears in any Layer 1 artefact. | MUST |
| [ARC-12](../../requirements.md#req-arc-12) | No component, dependency, endpoint, deployment artefact or runtime configuration provides AI capability. | MUST |
| [ASM03-VAL-01](../../requirements.md#req-asm03-val-01) | Validation is deterministic and rule-based only. It performs schema, answer, taxonomy, asset, equation, prohibited-markup, accessibility-completeness and within-artefact duplicate checks. | MUST |

## Exact PRD sections

- [7. Question Generation (Layer 2)](../../prd/main-baseline.md#7-question-generation-layer-2)
- [1.5 Two-layer architecture at a glance](../../prd/technical-baseline.md#15-two-layer-architecture-at-a-glance)
- [6.4 Authoring · ASM03-ATH](../../prd/technical-baseline.md#64-authoring--asm03-ath)
- [10.2 Architecture requirements](../../prd/technical-baseline.md#102-architecture-requirements)

## Behaviour to demonstrate

A returned candidate with two correct options never becomes a visible draft. Retry after a provider timeout cannot create a second copy of an already accepted candidate.

Failure checks: Return malformed, invalid, duplicated and timed-out provider proposals; validate deterministically and retain provenance without granting Layer 2 store access.

Existing issue acceptance criteria, retained for review:

- [ ] Admin can generate and regenerate when the pool is short
- [ ] Each generated item carries id, type, marks, subject, grade, curriculum, Bloom, difficulty, objective, competency, language, source chapter/page, generation id/model/config/time, status, version
- [ ] Questions are grounded in the uploaded curriculum only
- [ ] A candidate that fails automated validation is discarded — no human sees it
- [ ] A passing generated draft is treated exactly like a hand-written draft from that point
- [ ] Layer 2 never receives sealed content and cannot write into the pipeline except via the gateway propose path
- [ ] AI never validates, reviews, approves, seals, or monitors

## Dependencies and decisions

Required producer work: [#54](issue-54.md) (Sarvam team — individual lead to be confirmed), [#55](issue-55.md) (Kaustav), [#45](issue-45.md) (Kaustav), [#61](issue-61.md) (Kaustav).

R4 blocks automatic-draft versus explicit-adoption finalisation; R2 identifies the actual service. Build parsing, validation and provenance independently. AI never reviews or seals.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
