# Plan: As the System, I want to seal a language version after accessibility approval with no human button

Primary package: [Audit, sealing and vault](../evidence.md). Proposed owner: **Gandharva**.
Technical reviewers: Kaustav; Security for key/retention controls.
Issue: #77. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own durable evidence, canonical bytes, encryption/manifests, sealing retries and verification. The workflow owner decides legal state changes; this package returns verified receipts.

Expected locations: `platform/core audit/sealing workers and provider contracts`. Confirm actual paths before editing.

## Dependencies

#70, #71, #46

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] No person has a seal or publish control
- [ ] Worker re-checks every approval and every expected record; missing anything stops and alerts
- [ ] Canonicalize → SHA-256 → encrypt with managed keys → signed manifest (hashes, approvals, policy versions) → vault → metadata index → delete working copy → audit
- [ ] KMS/storage behind existing SPI (`mulyankan_spi.kms`)

## Failure or boundary proof

Fail keys/storage and interrupt the job after an external write; retry safely with no half-sealed success, human seal button or missing evidence.

## Requirement trace

QST05-VLT · ARC-05 · SEC-01

## Decisions and amendments to check

- Canonicalisation, retention and scoped sealed-reference/emergency contracts have explicit gates (R6/R8, D-24). No routine human sealed-plaintext read path is authorised by this issue.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
