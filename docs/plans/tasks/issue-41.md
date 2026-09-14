# Plan: As a staff member, I want to sign in through the organisation IdP with MFA

Primary package: [Platform, identity and integration](../platform.md). Proposed owner: **KKT**.
Technical reviewers: Gandharva; Rohit for recovery evidence.
Issue: #41. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own verified identities, reproducible environments, organisation-contracted managed-service bindings, release recovery and integration. The adopting organisation may contract any provider(s) meeting the interfaces and controls; no named host is mandatory. The IdP identifies the actor; workflow determines their task permissions.

Expected locations: `deployment/configuration, identity adapters, contracts and integration pipeline`. Confirm actual paths before editing.

## Dependencies

#51

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] `identity` SPI + conformance suite exists in `platform/spi` (same shape as `kms`)
- [ ] Compose IdP (Keycloak) issues OIDC tokens; `core-api` validates them server-side on every request
- [ ] No local password form anywhere
- [ ] Unauthenticated calls return 401
- [ ] Audit events store a pseudonymous workforce id (DAT-02), not the email

## Failure or boundary proof

Try missing, expired, forged, wrong-issuer and wrong-audience tokens; refuse MFA claims that do not meet the approved policy.

## Requirement trace

FND04-CAP-01..03 · ADR-0004 · ARC-01

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
