# Plan: As an Auditor, I want chain verification to fail on a tampered or missing record

Primary package: [Audit, sealing and vault](../evidence.md). Proposed owner: **Gandharva**.
Technical reviewers: Kaustav; Security for key/retention controls.
Issue: #47. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own durable evidence, canonical bytes, encryption/manifests, sealing retries and verification. The workflow owner decides legal state changes; this package returns verified receipts.

Expected locations: `platform/core audit/sealing workers and provider contracts`. Confirm actual paths before editing.

## Dependencies

#46

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Conformance test: persist N events, mutate or delete one row, `verify()` is ok=False with first_bad_seq
- [ ] On-demand verify endpoint (Admin/Auditor only) returns a content-free result
- [ ] Daily verification hook alerts on failure — alert has no question content
- [ ] CI runs the tamper test against the real store

## Failure or boundary proof

Alter and remove stored events; identify the first invalid link. Re-run verification after restore with unchanged canonical bytes.

## Requirement trace

ASR01-EVD-02/03

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
