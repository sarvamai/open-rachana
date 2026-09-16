# #118: Connect and release the signed desktop task client

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Connect, enrol and package the signed desktop client for authorised content tasks.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Connect one manual draft task with an enrolled test identity before adding all role screens; retain native build/update evidence for each target OS.

## Inputs and outputs

- Input: Accepted task/identity contract, enterprise device enrolment, signed local renderer, authenticated API and agreed OS targets.
- Output: A signed client that handles re-authentication, nonpersistent task state, refused access, native controls and verified updates.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ATH-18](../../requirements.md#req-prd-ath-18) | GAP Reference renderer: one versioned rendering component, executed server-side, produces the semantic HTML with MathML and text alternatives that preview, review, accessibility check, sealing and downstream delivery all use. Its renderer_version is recorded on every decision and in every manifest. A difference in output between author preview and review for the same canonical content is a defect, not a variance. | MUST |
| [DAT-04](../../requirements.md#req-dat-04) | Content responses use short-lived authorization and are marked non-cacheable. | MUST |
| [INS04-CAP-11](../../requirements.md#req-ins04-cap-11) | Sign-in to any content-handling surface succeeds only from a managed workstation inside an approved network zone, proven by device certificate and posture check. A request from an unmanaged or non-compliant device is denied and raises a security event, regardless of how valid the user's credentials are. | MUST |
| [PRD-CAP-12](../../requirements.md#req-prd-cap-12) | GAP Identity integration uses OpenID Connect Authorization Code flow with PKCE against the enterprise identity provider. The token must carry a stable subject and an authentication-methods claim proving multi-factor authentication; a token without it is refused with FORBIDDEN_MFA_REQUIRED. Group or role claims in the token are informational only and never authorize anything (ARC-01). | MUST |
| [ASM03-ATH-10](../../requirements.md#req-asm03-ath-10) | The interface exposes no download, print, bulk export or persistent browser-storage capability. Every artefact is stored on the server immediately, leaving no residual copy on the author's machine. | MUST |
| [PRD-ATH-20](../../requirements.md#req-prd-ath-20) | GAP D-20 Forced re-authentication: when the refresh window has expired, the client attempts one immediate autosave, then redirects to sign-in with the unsaved state held in memory for the same tab; on return the draft is reloaded from the server and any surviving unsaved text is offered for re-application. Loss is bounded by the autosave interval (≤ 30 s, §11). | MUST |
| [UI-13](../../requirements.md#req-ui-13) | Every input is labelled; keyboard operation and screen-reader semantics are preserved throughout. | MUST |
| [PRD-INT-14](../../requirements.md#req-prd-int-14) | GAP Content responses (draft, version, render, asset) are authorized per request with a short-lived scope and are non-cacheable (DAT-04); asset bytes are served through an authorized endpoint with a 60-second signed reference, never a stable public URL. | MUST |

## Exact PRD sections

- [17. Security](../../prd/main-baseline.md#17-security)
- [6.2 Recognized capability and access · INS04-CAP](../../prd/technical-baseline.md#62-recognized-capability-and-access--ins04-cap)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)
- [10.7 Egress, secrets, environments](../../prd/technical-baseline.md#107-egress-secrets-environments)

## Behaviour to demonstrate

An expired session cannot submit through a stale open window. Downloading a newer signed client does not grant new server permissions or leave a persistent question cache.

Existing issue acceptance criteria, retained for review:

- [ ] A signed enrolled client completes an allowed task against the real API.
- [ ] Wrong device/identity and expired task/session access are refused.
- [ ] No persistent local question content or remote executable UI is introduced.
- [ ] Native release/update and failure behaviour are tested on each agreed OS.

## Dependencies and decisions

Required producer work: [#117](task-contract.md) (KKT), [#41](issue-41.md) (KKT), [#53](issue-53.md) (Kaustav).

R5 render equivalence, R10 dependency redistribution and supported OS selection affect release. No remote executable task UI or unsupported signing claim.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
