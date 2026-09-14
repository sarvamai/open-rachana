# Plan: Publish versioned task and identity contracts for parallel implementation

Primary package: [Platform, identity and integration](../platform.md). Proposed owner: **KKT**.
Technical reviewers: Gandharva; Rohit for recovery evidence.
Issue: planned slice `task-contract`. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Agree identity context, task/version schemas, error/refusal semantics, concurrency and service receipts with client, workflow and evidence owners.

Own verified identities, reproducible environments, organisation-contracted managed-service bindings, release recovery and integration. The adopting organisation may contract any provider(s) meeting the interfaces and controls; no named host is mandatory. The IdP identifies the actor; workflow determines their task permissions.

Expected locations: `deployment/configuration, identity adapters, contracts and integration pipeline`. Confirm actual paths before editing.

## Dependencies

#40

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Machine-readable schemas and synthetic examples are checked in.
- [ ] Producer and consumer contract tests agree, including stale and wrong-role requests.
- [ ] Schema and migration ownership are explicit; incompatible changes require reviewed versioning.

## Failure or boundary proof

Schema and migration ownership are explicit; incompatible changes require reviewed versioning.

## Requirement trace

ARC/INT/RES/SEC obligations relevant to identity, contracts and recovery.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
