# Plan: As a staff member, I am refused unless device posture and network zone claims are present

Primary package: [Platform, identity and integration](../platform.md). Proposed owner: **KKT**.
Technical reviewers: Gandharva; Rohit for recovery evidence.
Issue: #43. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own verified identities, reproducible environments, organisation-contracted managed-service bindings, release recovery and integration. The adopting organisation may contract any provider(s) meeting the interfaces and controls; no named host is mandatory. The IdP identifies the actor; workflow determines their task permissions.

Expected locations: `deployment/configuration, identity adapters, contracts and integration pipeline`. Confirm actual paths before editing.

## Dependencies

#41

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Token without posture or zone claims is refused
- [ ] Compose IdP can mint a token that includes both claims for happy-path tests
- [ ] Refusal is audited content-free

## Failure or boundary proof

Remove posture/zone claims one at a time and try stale/invalid values; refuse without exposing identity or question content.

## Requirement trace

FND04-CAP-11 · ADR-0004

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
