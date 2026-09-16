# Plan: As the System, I want every question to have a QB-id, immutable versions, and a closed state machine

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #45. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#46

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] IDs are `QB-` + six digits and have no relationship to a final paper number
- [ ] Every substantive change is a new immutable version (old versions never change)
- [ ] States exist: DRAFT, IN_QUESTION_REVIEW, IN_ACCESSIBILITY, IN_ACCESSIBILITY_REVIEW, SEALED, IN_TRANSLATION, IN_TRANSLATION_REVIEW, FULLY_APPROVED, USED, ARCHIVED, WITHDRAWN, RETIRED, SUPERSEDED; REJECTED is a version outcome
- [ ] Illegal transitions fail closed (e.g. DRAFT → SEALED)
- [ ] No human seal, unseal, or read-sealed path exists

## Failure or boundary proof

Try illegal state jumps and stale writes; preserve immutable submitted versions. FULLY_APPROVED is computed readiness, not a language-version state.

## Requirement trace

ARC-01 · SEC-08

## Decisions and amendments to check

- FULLY_APPROVED is computed artefact readiness; USED/ARCHIVED are downstream lifecycle states. Do not collapse these into the per-language state enum.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
