# #41: As a staff member, I want to sign in through the organisation IdP with MFA

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Authenticate interactive users with the organisation IdP and produce the trusted identity context consumed by authorisation.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement issuer/audience/expiry/MFA refusal tests and the pseudonym mapping boundary behind an IdP fixture; integrate the actual IdP when provisioned.

## Inputs and outputs

- Input: OIDC issuer/key configuration, authorisation-code/PKCE flow, validated token subject and MFA claims, current session and pseudonym mapping.
- Output: Stable pseudonymous actor identifier, authenticated session context, sign-in/sign-out audit and a safe not-provisioned response. Role claims cannot grant task permission.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INS04-CAP-01](../../requirements.md#req-ins04-cap-01) | Interactive users authenticate through the enterprise identity provider. The product implements no local-password login. | MUST |
| [INS04-CAP-02](../../requirements.md#req-ins04-cap-02) | Multi-factor authentication is enforced for all content-handling and privileged roles. | MUST |
| [INS04-CAP-03](../../requirements.md#req-ins04-cap-03) | Sessions are short-lived with an inactivity timeout; privileged actions require re-authentication. | MUST |
| [PRD-CAP-12](../../requirements.md#req-prd-cap-12) | GAP Identity integration uses OpenID Connect Authorization Code flow with PKCE against the enterprise identity provider. The token must carry a stable subject and an authentication-methods claim proving multi-factor authentication; a token without it is refused with FORBIDDEN_MFA_REQUIRED. Group or role claims in the token are informational only and never authorize anything (ARC-01). | MUST |
| [PRD-CAP-13](../../requirements.md#req-prd-cap-13) | GAP Pseudonymization: on first sign-in the system generates a random, unguessable, stable workforce audit identifier and stores the mapping to the identity-provider subject in a separately access-controlled table. All business records, audit events, telemetry and screens other than the coordinator's assignment views use the audit identifier only (DAT-02). | MUST |
| [PRD-CAP-14](../../requirements.md#req-prd-cap-14) | GAP D-14 Proposed session parameters: access token lifetime 15 minutes with silent refresh; refresh window 8 hours; inactivity timeout 20 minutes with a visible warning at 18; absolute session maximum 10 hours. Privileged actions requiring a fresh authentication (no older than 5 minutes): cycle changes, registry changes, exception approval, correction authorization, retirement, manual assignment override. | MUST |
| [PRD-CAP-17](../../requirements.md#req-prd-cap-17) | GAP A valid token with no capability entry, or a role claim matching no known role, lands on a "Not provisioned — contact your administrator" screen; access is denied and a security event raised. | MUST |
| [DAT-02](../../requirements.md#req-dat-02) | Business records reference stable pseudonymous workforce audit identifiers; the identity provider remains the identity authority. | MUST |
| [UI-01](../../requirements.md#req-ui-01) | Sign-in — enterprise identity redirect only. No password form is built. On return, the user lands on their role's default surface. | MUST |

## Exact PRD sections

- [17. Security](../../prd/main-baseline.md#17-security)
- [6.2 Recognized capability and access · INS04-CAP](../../prd/technical-baseline.md#62-recognized-capability-and-access--ins04-cap)
- [7.1 Mandatory interface behaviours](../../prd/technical-baseline.md#71-mandatory-interface-behaviours)

## Behaviour to demonstrate

A correctly signed token without MFA is refused with FORBIDDEN_MFA_REQUIRED. A token naming Admin does not grant Admin capabilities without the registry.

Failure checks: Try missing, expired, forged, wrong-issuer and wrong-audience tokens; refuse MFA claims that do not meet the approved policy.

Existing issue acceptance criteria, retained for review:

- [ ] `identity` SPI + conformance suite exists in `platform/spi` (same shape as `kms`)
- [ ] Compose IdP (Keycloak) issues OIDC tokens; `core-api` validates them server-side on every request
- [ ] No local password form anywhere
- [ ] Unauthenticated calls return 401
- [ ] Audit events store a pseudonymous workforce id (DAT-02), not the email

## Dependencies and decisions

Required producer work: [#51](issue-51.md) (KKT).

D-14 lifetimes and freshness need approved configuration; the authentication/refusal logic can be built with explicit test values.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
