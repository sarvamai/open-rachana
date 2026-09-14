# Plan: As an Auditor, I want to search the audit trail and never see question content

Primary package: [Audit, sealing and vault](../evidence.md). Proposed owner: **Gandharva**.
Technical reviewers: Kaustav; Security for key/retention controls.
Issue: #48. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own durable evidence, canonical bytes, encryption/manifests, sealing retries and verification. The workflow owner decides legal state changes; this package returns verified receipts.

Expected locations: `platform/core audit/sealing workers and provider contracts`. Confirm actual paths before editing.

## Dependencies

#42, #46

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Auditor can filter by actor (pseudonymous), action, object ref, time
- [ ] Response schema has no stem, options, explanation, or translation text fields
- [ ] Admin may open the same content-free view in the pilot

## Failure or boundary proof

Attempt forbidden content fields and another role’s endpoint; filters and result counts must not reveal question text or restricted context.

## Requirement trace

ASR01-EVD-09 · DAT-03

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
