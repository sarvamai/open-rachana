# Plan: As an Admin, I want submit blocked until validation passes, with each finding naming the field

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #61. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#44, #59

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Required fields present
- [ ] 2–8 unique options; exactly one correct
- [ ] Classification values exist in the current syllabus
- [ ] Images scanned clean; alt text present for meaningful images
- [ ] Equations inside the permitted subset; no prohibited markup
- [ ] Blocking findings stop submit and name the field
- [ ] Validation is deterministic — no model, no external probabilistic service

## Failure or boundary proof

Provide one failing fixture per rule and boundary cases; no model calls occur and every blocking finding identifies its field.

## Requirement trace

QST03-VAL-03 (deterministic)

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
