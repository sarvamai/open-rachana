# Plan: As Security, I want a penetration test against isolation, seal, SoD, and export closed

Primary package: [Testing framework and acceptance evidence](../testing.md). Proposed owner: **Rohit**.
Technical reviewers: KKT; feature owners.
Issue: #86. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own the shared testing system and independent failure cases. Each feature owner writes tests for their implementation; expert security/accessibility acceptance still needs named people.

Expected locations: `CI, shared fixtures, contract/integration/end-to-end tests and evidence index`. Confirm actual paths before editing.

## Dependencies

#85, #60, #65, #68, #78, #81

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Pentest report filed against: reviewer isolation, sealed plaintext, SoD API, copy/export, vault
- [ ] Findings tracked to close or accepted risk
- [ ] Emergency two-person unseal (if any) is in scope

## Failure or boundary proof

Retain reproducible evidence for each attack surface and disposition each finding with the named Security owner; no assumed emergency-read exception.

## Requirement trace

SEC-01..14

## Decisions and amendments to check

- Canonicalisation, retention and scoped sealed-reference/emergency contracts have explicit gates (R6/R8, D-24). No routine human sealed-plaintext read path is authorised by this issue.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
