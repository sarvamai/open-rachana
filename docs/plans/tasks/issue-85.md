# Plan: As the authority, I want production identity, keys, and managed-device checks

Primary package: [Platform, identity and integration](../platform.md). Proposed owner: **KKT**.
Technical reviewers: Gandharva; Rohit for recovery evidence.
Issue: #85. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own verified identities, reproducible environments, organisation-contracted managed-service bindings, release recovery and integration. The adopting organisation may contract any provider(s) meeting the interfaces and controls; no named host is mandatory. The IdP identifies the actor; workflow determines their task permissions.

Expected locations: `deployment/configuration, identity adapters, contracts and integration pipeline`. Confirm actual paths before editing.

## Dependencies

#41, #43, #77

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Enterprise IdP replaces Keycloak in the production binding
- [ ] Real KMS and vault keys via provider bindings
- [ ] Managed-device / approved-location checks use production claims
- [ ] Sessions time out; sensitive actions re-authenticate

## Failure or boundary proof

Exercise revoked production identity, failed key access, invalid device claims and re-authentication expiry; no development credential fallback.

## Requirement trace

FND04-CAP · ARC-08

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
