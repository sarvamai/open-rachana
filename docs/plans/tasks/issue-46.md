# Plan: As the System, I want every state change written to a persisted hash-chained audit log in the same transaction

Primary package: [Audit, sealing and vault](../evidence.md). Proposed owner: **Gandharva**.
Technical reviewers: Kaustav; Security for key/retention controls.
Issue: #46. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own durable evidence, canonical bytes, encryption/manifests, sealing retries and verification. The workflow owner decides legal state changes; this package returns verified receipts.

Expected locations: `platform/core audit/sealing workers and provider contracts`. Confirm actual paths before editing.

## Dependencies

#51

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] DB-backed store produces byte-identical events to `AuditEvent` in `platform/core/.../audit/chain.py`
- [ ] `verify()` results match the in-memory log (`test_audit_chain.py` stays the oracle)
- [ ] Payload is hashed and discarded; events carry opaque refs only
- [ ] A crashed mid-write leaves both state+event or neither
- [ ] `docs/canonicalization.md` exists (referenced by chain.py, missing on disk today)

## Failure or boundary proof

Crash between attempted state and event writes: both commit or neither. Verify a persisted event matches the approved byte fixtures.

## Requirement trace

ASR01-EVD-01/02/09 · ARC-02 · DAT-05

## Decisions and amendments to check

- Check open PR #93 before starting. It already proposes extraction, CI, deployment helpers and canonicalisation/as-built work; reuse accepted results and fill remaining gaps rather than duplicate it.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
