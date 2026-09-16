# Plan: As an Admin, I want to upload a curriculum PDF

Primary package: [Layer 2 intelligence and adapters](../intelligence.md). Proposed owner: **Sarvam team — individual lead to be confirmed**.
Technical reviewers: Kaustav; Security for translation hosting.
Issue: #54. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Produce grounded proposals with provenance through governed adapters. No sealed content, workflow-store credentials or AI approval/validation paths. Layer 1 owns validation and human gates.

Expected locations: `curriculum ingestion and replaceable generation/translation/metadata adapters`. Confirm actual paths before editing.

## Dependencies

#41, #51

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Admin uploads a PDF (example: NCERT Class 8 Science) and it is stored as reference material
- [ ] Upload is quarantined, scanned, and re-encoded before use
- [ ] Audit event records the upload (no file bytes in the event)
- [ ] Reviewers never see the stored source-context text later

## Failure or boundary proof

Try a malformed, oversized, scanned-failed and text-poor PDF; preserve quarantine/provenance and prevent source text from reaching logs.

## Requirement trace

QST03-ATH (source) · SEC image/upload quarantine applies to files

## Decisions and amendments to check

- Check open PR #93 before starting. It already proposes extraction, CI, deployment helpers and canonicalisation/as-built work; reuse accepted results and fill remaining gaps rather than duplicate it.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
