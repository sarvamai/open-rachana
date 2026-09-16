# Plan: As a Question Reviewer, I want to comment, approve against the checklist, or reject with a reason

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #66. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#65, #68

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Actions: read, comment, approve, reject — no edit
- [ ] Approve requires every checklist item plus attestations 1–3 (language/grammar + source; not public-domain + source; in-scope + source) and a difficulty from the controlled list
- [ ] Approve moves the version to Accessibility
- [ ] Reject requires a reason + comment; Admin gets a correction draft; a *different* Question Reviewer is assigned next
- [ ] Cycle setting controls one vs two question reviewers

## Failure or boundary proof

Omit each attestation/reason, use stale task ownership and repeat a decision; refuse incomplete/conflicting requests and preserve linked corrections.

## Requirement trace

QST03-REV

## Decisions and amendments to check

- R12 distinguishes one assignee per task from a configurable number of independent reviews; obtain the cycle-policy decision before fixing the assignment contract.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
