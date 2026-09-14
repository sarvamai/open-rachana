# Plan: Add workflow dashboards and tested operational alerts

Primary package: [Operational observability](../observability.md). Proposed owner: **Irfan**.
Technical reviewers: KKT; Rohit for leak and failure checks.
Issue: #114. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Use stable content-free domain events to show workflow latency, failures and dependency health after the real flows exist.

Own diagnostic logs, metrics, traces, Collector configuration, local dashboards and alerts. Session-integrity decisions and durable audit evidence remain with workflow/evidence owners.

Expected locations: `runtime instrumentation and deploy/dev observability configuration`. Confirm actual paths before editing.

## Dependencies

#110, #63, #77

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Dashboards show the agreed domain measures with no question content.
- [ ] An induced failure triggers an actionable alert linked to a runbook.
- [ ] Synthetic dashboard data is labelled and cannot close real-flow acceptance.

## Failure or boundary proof

Synthetic dashboard data is labelled and cannot close real-flow acceptance.

## Requirement trace

ASR01-EVD-09, DAT-03 and the operational observability contract; diagnostic signals do not satisfy ASR02 integrity evidence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
