# Plan: As Content Operations, I want pilot languages and named people recorded

Primary package: [Product acceptance and contributor onboarding](../product.md). Proposed owner: **Nikhil**.
Technical reviewers: KKT for technical steps; Rohit for testability.
Issue: #39. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own scope, understandable issue briefs, user journeys and product acceptance. Do not invent pilot languages, participant commitments or technical/security approvals.

Expected locations: `product decisions, acceptance examples, contributor documentation`. Confirm actual paths before editing.

## Dependencies

No implementation prerequisite; the plan can be reviewed now.

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] ADR-0006 is amended in place with the three pilot language names (primary + two variants)
- [ ] A roster of named people and roles is recorded (no credentials): 2 Admins, 2 Question Reviewers, 1 accessibility professional, 2 Translators, 1 coordinator, 1 Integrity Operator
- [ ] Languages remain `cycle.required_languages` configuration — no `if lang ==` in platform/

## Failure or boundary proof

Reject an incomplete or conflicting roster; keep pilot languages configurable. Separate remediation and approval roles even when a professional holds more than one role.

## Requirement trace

QST01-CFG · ADR-0006

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
