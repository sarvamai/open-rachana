# Plan: As Product Owner, I want Week-1 product decisions recorded as ADRs

Primary package: [Product acceptance and contributor onboarding](../product.md). Proposed owner: **Nikhil**.
Technical reviewers: KKT for technical steps; Rohit for testability.
Issue: #40. Companion reference: PR #100; contributor workflow: PR #99.

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

- [ ] ADR exists: no download/print/copy/export from the question bank; paper export is assembly
- [ ] ADR exists: delete means withdraw (draft) or retire (approved); nothing is permanently deleted
- [ ] ADR exists: Admin may view all questions until sealed; metadata only after sealing
- [ ] Permission matrix confirms Admin never approves or rejects (D-46)
- [ ] `docs/traceability.md` points at the ADRs

## Failure or boundary proof

Verify every recorded decision distinguishes an accepted owner decision from a recommendation. The separate Author role/adoption question stays open.

## Requirement trace

SEC · DAT

## Decisions and amendments to check

- The Admin content client/web split is recorded in the reference PR. A separate Author role and automatic draft creation versus explicit adoption remain R4; do not settle them by coding an old issue sentence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
