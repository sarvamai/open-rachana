# Plan: As an engineer, I want CI to run platform pytest so a green PR is evidence

Primary package: [Testing framework and acceptance evidence](../testing.md). Proposed owner: **Rohit**.
Technical reviewers: KKT; feature owners.
Issue: #52. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own the shared testing system and independent failure cases. Each feature owner writes tests for their implementation; expert security/accessibility acceptance still needs named people.

Expected locations: `CI, shared fixtures, contract/integration/end-to-end tests and evidence index`. Confirm actual paths before editing.

## Dependencies

No implementation prerequisite; the plan can be reviewed now.

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] `build-and-test` in `.github/workflows/ci.yml` runs pytest over `platform/spi` and `platform/core`
- [ ] A failing `test_audit_chain.py` assertion fails CI
- [ ] Draft PRs still skip, same as sibling jobs
- [ ] AGENTS.md no longer says Python tests are local-only

## Failure or boundary proof

Run a deliberately failing platform assertion in a disposable validation branch and retain the failed result; restore the assertion before merging.

## Requirement trace

v4 §11

## Decisions and amendments to check

- Check open PR #93 before starting. It already proposes extraction, CI, deployment helpers and canonicalisation/as-built work; reuse accepted results and fill remaining gaps rather than duplicate it.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
