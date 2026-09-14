# Plan: Provide the local Collector and Grafana observability stack

Primary package: [Operational observability](../observability.md). Proposed owner: **Irfan**.
Technical reviewers: KKT; Rohit for leak and failure checks.
Issue: planned slice `obs-local`. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Provide reproducible local Grafana, Loki, Tempo and Prometheus wiring through the Collector, with documented start, stop and reset commands.

Own diagnostic logs, metrics, traces, Collector configuration, local dashboards and alerts. Session-integrity decisions and durable audit evidence remain with workflow/evidence owners.

Expected locations: `runtime instrumentation and deploy/dev observability configuration`. Confirm actual paths before editing.

## Dependencies

No implementation prerequisite; the plan can be reviewed now.

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] A clean machine starts the stack using the documented command.
- [ ] Synthetic log, metric and trace are visible and linked.
- [ ] Backend changes require Collector/configuration changes, not domain-code changes.

## Failure or boundary proof

Backend changes require Collector/configuration changes, not domain-code changes.

## Requirement trace

ASR01-EVD-09, DAT-03 and the operational observability contract; diagnostic signals do not satisfy ASR02 integrity evidence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
