# Plan: Verify the contributor first-run guide and first-PR path

Primary package: [Product acceptance and contributor onboarding](../product.md). Proposed owner: **Nikhil**.
Technical reviewers: KKT for technical steps; Rohit for testability.
Issue: #119. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Follow setup as a new contributor; document actual commands, one synthetic acceptance scenario and the reviewed PR process.

Own scope, understandable issue briefs, user journeys and product acceptance. Do not invent pilot languages, participant commitments or technical/security approvals.

Expected locations: `product decisions, acceptance examples, contributor documentation`. Confirm actual paths before editing.

## Dependencies

#51, #52, #94

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] A second contributor follows the guide from a clean environment.
- [ ] Failures are tracked rather than described as working.
- [ ] The guide includes plan review, Humanizer readability, tests and required evidence.

## Failure or boundary proof

The guide includes plan review, Humanizer readability, tests and required evidence.

## Requirement trace

Product acceptance, contributor documentation and retained evidence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
