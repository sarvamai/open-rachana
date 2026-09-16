# #43: As a staff member, I am refused unless device posture and network zone claims are present

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Enforce managed-device and approved-zone access at sign-in and refresh.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Specify which trusted edge component verifies each proof, then test missing, expired and forged proofs independently.

## Inputs and outputs

- Input: Enterprise device certificate verified at the TLS edge; endpoint posture assertion with age; source network zone; trusted identity context.
- Output: An admitted session or FORBIDDEN_DEVICE_POSTURE plus a content-free security event. Do not trust client-supplied posture headers.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INS04-CAP-11](../../requirements.md#req-ins04-cap-11) | Sign-in to any content-handling surface succeeds only from a managed workstation inside an approved network zone, proven by device certificate and posture check. A request from an unmanaged or non-compliant device is denied and raises a security event, regardless of how valid the user's credentials are. | MUST |
| [PRD-CAP-15](../../requirements.md#req-prd-cap-15) | GAP Device and zone proof (CAP-11): a client certificate from the enterprise device authority presented at the TLS edge; a posture assertion from endpoint management (disk encryption on, operating system patched, agent running) no older than the configured freshness D-14; and a source address inside the approved studio zone. All three are checked at sign-in and on every token refresh. Failure denies with FORBIDDEN_DEVICE_POSTURE and raises a security event; the user sees "This device or location isn't approved for content work". | MUST |

## Exact PRD sections

- [17. Security](../../prd/main-baseline.md#17-security)
- [6.2 Recognized capability and access · INS04-CAP](../../prd/technical-baseline.md#62-recognized-capability-and-access--ins04-cap)
- [10.7 Egress, secrets, environments](../../prd/technical-baseline.md#107-egress-secrets-environments)

## Behaviour to demonstrate

A user with valid MFA on an unmanaged laptop is denied. A compliant device outside the approved zone is also denied; neither condition substitutes for the other.

Failure checks: Remove posture/zone claims one at a time and try stale/invalid values; refuse without exposing identity or question content.

Existing issue acceptance criteria, retained for review:

- [ ] Token without posture or zone claims is refused
- [ ] Compose IdP can mint a token that includes both claims for happy-path tests
- [ ] Refusal is audited content-free

## Dependencies and decisions

Required producer work: [#41](issue-41.md) (KKT).

D-14 posture freshness and the adopter’s trusted authorities/zones require configuration. Test fixtures must not become production allowlists.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
