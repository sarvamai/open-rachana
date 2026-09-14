# Plan: As an Admin, I want Layer 2 to draft candidate questions from the curriculum and blueprint

Primary package: [Layer 2 intelligence and adapters](../intelligence.md). Proposed owner: **Sarvam team — individual lead to be confirmed**.
Technical reviewers: Kaustav; Security for translation hosting.
Issue: #56. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Produce grounded proposals with provenance through governed adapters. No sealed content, workflow-store credentials or AI approval/validation paths. Layer 1 owns validation and human gates.

Expected locations: `curriculum ingestion and replaceable generation/translation/metadata adapters`. Confirm actual paths before editing.

## Dependencies

#54, #55, #45, #61

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Admin can generate and regenerate when the pool is short
- [ ] Each generated item carries id, type, marks, subject, grade, curriculum, Bloom, difficulty, objective, competency, language, source chapter/page, generation id/model/config/time, status, version
- [ ] Questions are grounded in the uploaded curriculum only
- [ ] A candidate that fails automated validation is discarded — no human sees it
- [ ] A passing generated draft is treated exactly like a hand-written draft from that point
- [ ] Layer 2 never receives sealed content and cannot write into the pipeline except via the gateway propose path
- [ ] AI never validates, reviews, approves, seals, or monitors

## Failure or boundary proof

Return malformed, invalid, duplicated and timed-out provider proposals; validate deterministically and retain provenance without granting Layer 2 store access.

## Requirement trace

ARC-12 · gateway SPI (ADR-0007)

## Decisions and amendments to check

- The Admin content client/web split is recorded in the reference PR. A separate Author role and automatic draft creation versus explicit adoption remain R4; do not settle them by coding an old issue sentence.
- The old adoption-before-draft note conflicts with the proposed generated-DRAFT flow. Keep that transition blocked until R4 is decided; adapter fixtures can proceed.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
