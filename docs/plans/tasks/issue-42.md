# Plan: As the System, I want every request authorised from the capability matrix

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #42. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#41

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Roles encoded as data: Admin, Question Reviewer, Accessibility Specialist, Accessibility Reviewer, Translator, Translation Reviewer, Integrity Operator, Auditor, System
- [ ] Admin cannot approve or reject at any stage (unit + API test)
- [ ] Reviewers cannot edit; Integrity Operator and Auditor have no content fields
- [ ] Missing capability is 403; client-supplied role is ignored
- [ ] Admin can manage users and assign roles (write path + audit event)

## Failure or boundary proof

Try a client-forged role, missing capability, revoked actor and each forbidden cross-role operation. Check both response fields and writes.

## Requirement trace

FND04-CAP · INT-10 · D-46

## Decisions and amendments to check

- The Admin content client/web split is recorded in the reference PR. A separate Author role and automatic draft creation versus explicit adoption remain R4; do not settle them by coding an old issue sentence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
