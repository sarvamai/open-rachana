# Plan: As the System, I want sealing the original to create the translation drafts

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #79. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#77, #67

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] On original SEALED, one IN_TRANSLATION draft is created per required language
- [ ] Assignment story places one translator per language
- [ ] Original bytes are not copied into an editable original; translators see a read view

## Failure or boundary proof

Replay primary-seal events; create exactly one current task per required language and preserve locked structure without a general vault-read path.

## Requirement trace

QST04-TRN · QST05-VLT

## Decisions and amendments to check

- Canonicalisation, retention and scoped sealed-reference/emergency contracts have explicit gates (R6/R8, D-24). No routine human sealed-plaintext read path is authorised by this issue.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
