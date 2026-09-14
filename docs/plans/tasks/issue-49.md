# Plan: As the System, I want CI to fail if logs, errors, or audit fixtures contain question content

Primary package: [Testing framework and acceptance evidence](../testing.md). Proposed owner: **Rohit**.
Technical reviewers: KKT; feature owners.
Issue: #49. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

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

- [ ] `tests/conformance/` scan fails when a stem/option/explanation appears in log fixtures, audit fixtures, or exception strings
- [ ] Scan is part of `build-and-test`
- [ ] A deliberate dirty fixture fails CI

## Failure or boundary proof

Inject synthetic sentinel text into logs, traces, errors and audit exports; demonstrate that the CI check fails and clean fixtures pass.

## Requirement trace

ASR01-EVD-09 · DAT-03 · standing DoD v4 §11

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
