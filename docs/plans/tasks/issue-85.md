# #85: As the authority, I want production identity, keys, and managed-device checks

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Bind and qualify production identities, keys, zones and privileged-operation controls.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Produce a deployment identity/permission matrix and exercise one real provider binding in a non-production qualification environment.

## Inputs and outputs

- Input: Adopter-selected IdP/KMS/storage/secret providers, workload audiences, network zones, device authorities and re-auth policy.
- Output: Versioned environment bindings and evidence that wrong/expired/revoked identities fail without a development fallback.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INT-02](../../requirements.md#req-int-02) | Interactive calls carry a bearer token from the enterprise identity provider. Service-to-service calls use mutual TLS and audience-restricted short-lived workload tokens. | MUST |
| [ARC-06](../../requirements.md#req-arc-06) | The downstream assembly consumer is reached only over mutual TLS with an audience-restricted workload token. | MUST |
| [ARC-07](../../requirements.md#req-arc-07) | The authoring environment operates default-deny egress and reaches only allowlisted enterprise endpoints. | MUST |
| [ARC-08](../../requirements.md#req-arc-08) | Workloads use short-lived workload identity. Static cloud credentials and embedded secrets are prohibited. | MUST |
| [ARC-10](../../requirements.md#req-arc-10) | Infrastructure administration through privileged-access management grants no application-level content access. | MUST |
| [ARC-11](../../requirements.md#req-arc-11) | The repository is physically and logically segregated from the authoring, review and accessibility environments. | MUST |
| [SEC-12](../../requirements.md#req-sec-12) | Secrets live in the approved secret manager. None appear in source, logs, images or environment dumps. | MUST |
| [PRD-CAP-14](../../requirements.md#req-prd-cap-14) | GAP D-14 Proposed session parameters: access token lifetime 15 minutes with silent refresh; refresh window 8 hours; inactivity timeout 20 minutes with a visible warning at 18; absolute session maximum 10 hours. Privileged actions requiring a fresh authentication (no older than 5 minutes): cycle changes, registry changes, exception approval, correction authorization, retirement, manual assignment override. | MUST |
| [PRD-CAP-15](../../requirements.md#req-prd-cap-15) | GAP Device and zone proof (CAP-11): a client certificate from the enterprise device authority presented at the TLS edge; a posture assertion from endpoint management (disk encryption on, operating system patched, agent running) no older than the configured freshness D-14; and a source address inside the approved studio zone. All three are checked at sign-in and on every token refresh. Failure denies with FORBIDDEN_DEVICE_POSTURE and raises a security event; the user sees "This device or location isn't approved for content work". | MUST |
| [PRD-VLT-11](../../requirements.md#req-prd-vlt-11) | GAP Encryption model: envelope encryption with a fresh 256-bit data key per sealed version (authenticated encryption), the data key wrapped by the active repository-tier key in the key management service. Key policy grants encrypt to the sealing identity only; decrypt to the verification identity (in-memory verification only, no plaintext output), the correction-seeding identity under a recorded authorization (§6.11), and the break-glass identity (§10.6). No human principal and no platform-administrator role holds decrypt. Every key use is logged by the key service and mirrored into audit. | MUST |
| [PRD-INT-13](../../requirements.md#req-prd-int-13) | GAP Machine-interface security: mutual TLS with certificates from the enterprise authority; tokens with audience, issuer, expiry ≤ 5 minutes and a key identifier resolved through a published key set; signed notifications use a detached JSON Web Signature with replay protection by notification identifier and a 5-minute clock-skew window; key rotation is supported without downtime. | MUST |

## Exact PRD sections

- [10.1 Reference architecture and trust zones](../../prd/technical-baseline.md#101-reference-architecture-and-trust-zones)
- [10.3 Security requirements](../../prd/technical-baseline.md#103-security-requirements)
- [10.7 Egress, secrets, environments](../../prd/technical-baseline.md#107-egress-secrets-environments)

## Behaviour to demonstrate

Revoking the sealing workload’s key permission causes a visible failed job; it cannot switch to a local test KMS. Changing an Admin’s registry entry requires fresh authentication.

Failure checks: Exercise revoked production identity, failed key access, invalid device claims and re-authentication expiry; no development credential fallback.

Existing issue acceptance criteria, retained for review:

- [ ] Enterprise IdP replaces Keycloak in the production binding
- [ ] Real KMS and vault keys via provider bindings
- [ ] Managed-device / approved-location checks use production claims
- [ ] Sessions time out; sensitive actions re-authenticate

## Dependencies and decisions

Required producer work: [#41](issue-41.md) (KKT), [#43](issue-43.md) (KKT), [#77](issue-77.md) (Gandharva).

D-28/D-30 and adopter contracts select services; any contracted provider may meet the interface. Security must accept the actual deployment, not just a diagram.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
