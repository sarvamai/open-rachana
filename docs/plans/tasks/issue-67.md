# Plan: As the System, I want to assign one eligible reviewer per question per stage by workload

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #67. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#42, #44, #45

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Eligible = right role, subject, language, valid registry entry, no conflict of duty
- [ ] Lowest active workload first; tie-break = longest time since last assignment
- [ ] A corrected question goes to a different reviewer
- [ ] A reviewer never gets an item they authored, translated, or reviewed at another stage
- [ ] Unanswered tasks expire back to the pool; Admin sees aging
- [ ] Admin can reassign or release, still inside the same rules

## Failure or boundary proof

Create ties, expired work, changed eligibility and prior-lineage conflicts; demonstrate deterministic assignment and a new reviewer after correction.

## Requirement trace

QST03-REV assignment

## Decisions and amendments to check

- R12 distinguishes one assignee per task from a configurable number of independent reviews; obtain the cycle-policy decision before fixing the assignment contract.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
