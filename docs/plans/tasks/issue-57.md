# Plan: As Security, I want the translation-draft model channel off until the model runs inside our boundary

Primary package: [Layer 2 intelligence and adapters](../intelligence.md). Proposed owner: **Sarvam team — individual lead to be confirmed**.
Technical reviewers: Kaustav; Security for translation hosting.
Issue: #57. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Produce grounded proposals with provenance through governed adapters. No sealed content, workflow-store credentials or AI approval/validation paths. Layer 1 owns validation and human gates.

Expected locations: `curriculum ingestion and replaceable generation/translation/metadata adapters`. Confirm actual paths before editing.

## Dependencies

#40

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Translation-draft generation path is disabled by default
- [ ] Enabling it requires a recorded Security + Technical Lead decision that the model is inside the boundary, no retention, no training
- [ ] Until then, translators write by hand (translation stories still apply)

## Failure or boundary proof

Prove the channel stays off without the recorded approval; manual translation still works and toggling configuration cannot bypass the approval gate.

## Requirement trace

ADR-0007 · D-48

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
