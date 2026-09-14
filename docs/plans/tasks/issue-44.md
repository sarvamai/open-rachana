# Plan: As an Admin, I want to configure a cycle and its taxonomy

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #44. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#39, #42, #46

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Admin can create/update a cycle: primary language, required languages, syllabus version, declared accommodations, review policy (1 vs 2 question reviewers)
- [ ] Admin can maintain taxonomy: subject, unit, topic, difficulty, Bloom's level — versioned with the syllabus
- [ ] Invalid taxonomy codes are rejected
- [ ] Each write appends a content-free audit event in the same transaction
- [ ] Non-Admin is 403

## Failure or boundary proof

Try stale taxonomy, invalid language/policy configuration and concurrent updates; retain the exact configuration version and atomic evidence.

## Requirement trace

QST01-CFG · ADR-0006

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
