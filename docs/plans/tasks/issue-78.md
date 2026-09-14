# Plan: As any human, including Admin, I cannot read a sealed question

Primary package: [Audit, sealing and vault](../evidence.md). Proposed owner: **Gandharva**.
Technical reviewers: Kaustav; Security for key/retention controls.
Issue: #78. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own durable evidence, canonical bytes, encryption/manifests, sealing retries and verification. The workflow owner decides legal state changes; this package returns verified receipts.

Expected locations: `platform/core audit/sealing workers and provider contracts`. Confirm actual paths before editing.

## Dependencies

#42, #77

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Every human role, Admin and platform administrator included, receives no plaintext for a sealed version
- [ ] Admin sees metadata only after seal
- [ ] Conformance test: sealed-plaintext denial for every role
- [ ] Emergency access (if implemented) needs two named approvers and is logged — default is no emergency path in V1 unless Security asks

## Failure or boundary proof

Try every routine human role and a platform administrator; deny sealed plaintext through all supported interfaces and preserve metadata-only access.

## Requirement trace

SEC-01

## Decisions and amendments to check

- Canonicalisation, retention and scoped sealed-reference/emergency contracts have explicit gates (R6/R8, D-24). No routine human sealed-plaintext read path is authorised by this issue.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
