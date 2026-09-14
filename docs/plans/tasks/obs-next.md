# Plan: Connect Next.js server instrumentation to API traces

Primary package: [Operational observability](../observability.md). Proposed owner: **Irfan**.
Technical reviewers: KKT; Rohit for leak and failure checks.
Issue: planned slice `obs-next`. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Configure server instrumentation, safe request logging and trace propagation without capturing payloads or raw query values.

Own diagnostic logs, metrics, traces, Collector configuration, local dashboards and alerts. Session-integrity decisions and durable audit evidence remain with workflow/evidence owners.

Expected locations: `runtime instrumentation and deploy/dev observability configuration`. Confirm actual paths before editing.

## Dependencies

planned slice `obs-python`, planned slice `obs-local`

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] One request can be followed from Next.js to Python.
- [ ] Logs/errors pass the sentinel guard.
- [ ] Missing Collector does not prevent page/API service.

## Failure or boundary proof

Missing Collector does not prevent page/API service.

## Requirement trace

ASR01-EVD-09, DAT-03 and the operational observability contract; diagnostic signals do not satisfy ASR02 integrity evidence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
