# Plan: As the System, I want content sessions to heartbeat and the first monitoring signal to reach the audit in seconds

Primary package: [Workflow and business rules](../workflow.md). Proposed owner: **Kaustav**.
Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Issue: #50. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. Confirm actual paths before editing.

## Dependencies

#41, #46

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Session register, 30-second heartbeat, close — platform concern, not the IdP
- [ ] One published signal implemented (copy/cut/paste or heartbeat gap)
- [ ] Signal writes a content-free audit event (action, session id, score) within seconds
- [ ] Score starts at 100, subtracts a fixed published amount, never recovers in-session
- [ ] Automatic suspension stays off

## Failure or boundary proof

Attempt another actor’s session writes, forged session identity, duplicate/out-of-order signals and temporary ingest failure; prove durable recovery.

## Requirement trace

ASR02-OBS-01 · ADR-0004

## Decisions and amendments to check

- Heartbeat/scoring/referral values remain governed by the decision register. Existing numeric defaults are proposals until ratified; diagnostic Collector outage never excuses lost integrity evidence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
