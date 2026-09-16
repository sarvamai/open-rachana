# #86: As Security, I want a penetration test against isolation, seal, SoD, and export closed

Owner proposed in the delivery plan: **Rohit**. Technical review: KKT; feature owners.
Epic: [#107](https://github.com/Bodhan-AI/open-rachana/issues/107). [Module route](../testing.md).

Run independent security qualification against the implemented interfaces and deployment.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Build the attack matrix for forged roles, direct-API duty conflicts, sealed retrieval, upload abuse and content leakage; exercise it against the integrated environment.

## Inputs and outputs

- Input: Versioned release/environment, endpoint inventory, role/workload fixtures, data classification, threat cases and unresolved findings.
- Output: Reproducible attack results, severity/disposition/owner for each finding and named Security acceptance; untested surfaces stay explicit.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [SEC-04](../../requirements.md#req-sec-04) | Emergency evidence access sits outside the routine workflow and requires a separately approved, dual-authorized manual procedure. | MUST |
| [SEC-11](../../requirements.md#req-sec-11) | Transport is TLS 1.2 or above. Content-security policy, cross-site request forgery defence, output encoding, secure headers and no-store caching are all in place. | MUST |
| [SEC-01](../../requirements.md#req-sec-01) | Sealed plaintext is not retrievable through any human or API interface — author, reviewer, accessibility specialist, translator, coordinator, operator, auditor or administrator. | MUST |
| [SEC-03](../../requirements.md#req-sec-03) | Automated tests assert that no non-permitted role receives correct-answer or sealed-plaintext fields in any response body. | MUST |
| [SEC-05](../../requirements.md#req-sec-05) | Authorization is server-side on every operation. Interface restrictions are convenience, never control. | MUST |
| [SEC-06](../../requirements.md#req-sec-06) | Separation of duties is provable through both the interface and a hand-crafted direct API call. | MUST |
| [SEC-09](../../requirements.md#req-sec-09) | Uploads are quarantined and only released after format allowlisting, signature inspection, malware scanning, re-encoding, metadata removal and decompression limits. | MUST |
| [SEC-13](../../requirements.md#req-sec-13) | Backups are encrypted, access-separated, immutable, and restoration is tested. | MUST |

## Exact PRD sections

- [10.3 Security requirements](../../prd/technical-baseline.md#103-security-requirements)
- [10.6 Break-glass procedure requirements](../../prd/technical-baseline.md#106-break-glass-procedure-requirements)
- [13.2 Mandated automated suites](../../prd/technical-baseline.md#132-mandated-automated-suites)
- [13.3 Expert and manual verification](../../prd/technical-baseline.md#133-expert-and-manual-verification)

## Behaviour to demonstrate

Try a permitted reviewer token on an unassigned task and a platform-admin credential on sealed retrieval. Retain actual responses and evidence references without publishing Restricted content.

Failure checks: Retain reproducible evidence for each attack surface and disposition each finding with the named Security owner; no assumed emergency-read exception.

Existing issue acceptance criteria, retained for review:

- [ ] Pentest report filed against: reviewer isolation, sealed plaintext, SoD API, copy/export, vault
- [ ] Findings tracked to close or accepted risk
- [ ] Emergency two-person unseal (if any) is in scope

## Dependencies and decisions

Required producer work: [#85](issue-85.md) (KKT), [#60](issue-60.md) (Divyansh), [#65](issue-65.md) (Divyansh), [#68](issue-68.md) (Kaustav), [#78](issue-78.md) (Gandharva), [#81](issue-81.md) (Kaustav).

R8 emergency/reference procedure and R10 distribution rights are separate release prerequisites. Rohit’s harness cannot substitute for the Security owner’s sign-off.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
