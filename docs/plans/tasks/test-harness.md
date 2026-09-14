# Plan: Build shared contract fixtures and the first end-to-end acceptance harness

Primary package: [Testing framework and acceptance evidence](../testing.md). Proposed owner: **Rohit**.
Technical reviewers: KKT; feature owners.
Issue: #115. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Create synthetic actors, questions, languages and provider doubles, then execute the same contract against real persistence and the shared environment.

Own the shared testing system and independent failure cases. Each feature owner writes tests for their implementation; expert security/accessibility acceptance still needs named people.

Expected locations: `CI, shared fixtures, contract/integration/end-to-end tests and evidence index`. Confirm actual paths before editing.

## Dependencies

#52

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Allowed and refused examples exercise the same published API contract.
- [ ] The first author/reviewer path proves direct-API self-approval refusal.
- [ ] Failure, retry and transaction tests retain results linked to requirements.
- [ ] Desktop restrictions receive native validation; browser tests are not substituted.

## Failure or boundary proof

Desktop restrictions receive native validation; browser tests are not substituted.

## Requirement trace

Standing verification obligations and all requirement-specific tests consumed by the harness.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
