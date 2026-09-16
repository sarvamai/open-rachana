# #78: As any human, including Admin, I cannot read a sealed question

Owner proposed in the delivery plan: **Gandharva**. Technical review: Kaustav; Security for key/retention controls.
Epic: [#104](https://github.com/Bodhan-AI/open-rachana/issues/104). [Module route](../evidence.md).

Prove that routine human and administrator credentials cannot retrieve sealed plaintext.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Enumerate every retrieval route and test all routine roles using a synthetic sealed artefact, then verify the infrastructure policies with Security.

## Inputs and outputs

- Input: Role/workload access matrix, sealed object/reference identifiers and all application, storage, key and support interfaces.
- Output: Automated denial tests and deployment permission evidence; permitted metadata remains available with no decryption route.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM05-VLT-08](../../requirements.md#req-asm05-vlt-08) | Sealed artefacts are immutable and remain encrypted at rest with no plaintext copy accessible to any user or administrator. Which version is current is always resolvable. | MUST |
| [SEC-01](../../requirements.md#req-sec-01) | Sealed plaintext is not retrievable through any human or API interface — author, reviewer, accessibility specialist, translator, coordinator, operator, auditor or administrator. | MUST |
| [PRD-VLT-11](../../requirements.md#req-prd-vlt-11) | GAP Encryption model: envelope encryption with a fresh 256-bit data key per sealed version (authenticated encryption), the data key wrapped by the active repository-tier key in the key management service. Key policy grants encrypt to the sealing identity only; decrypt to the verification identity (in-memory verification only, no plaintext output), the correction-seeding identity under a recorded authorization (§6.11), and the break-glass identity (§10.6). No human principal and no platform-administrator role holds decrypt. Every key use is logged by the key service and mirrored into audit. | MUST |
| [SEC-04](../../requirements.md#req-sec-04) | Emergency evidence access sits outside the routine workflow and requires a separately approved, dual-authorized manual procedure. | MUST |
| [ARC-10](../../requirements.md#req-arc-10) | Infrastructure administration through privileged-access management grants no application-level content access. | MUST |

## Exact PRD sections

- [12. Sealing and the Vault](../../prd/main-baseline.md#12-sealing-and-the-vault)
- [17. Security](../../prd/main-baseline.md#17-security)
- [6.9 Sealing and the repository · ASM05-VLT](../../prd/technical-baseline.md#69-sealing-and-the-repository--asm05-vlt)
- [10.3 Security requirements](../../prd/technical-baseline.md#103-security-requirements)
- [10.6 Break-glass procedure requirements](../../prd/technical-baseline.md#106-break-glass-procedure-requirements)

## Behaviour to demonstrate

An infrastructure administrator with object-list rights still cannot decrypt a sealed object. Altering a readiness reference must not turn it into a download URL.

Failure checks: Try every routine human role and a platform administrator; deny sealed plaintext through all supported interfaces and preserve metadata-only access.

Existing issue acceptance criteria, retained for review:

- [ ] Every human role, Admin and platform administrator included, receives no plaintext for a sealed version
- [ ] Admin sees metadata only after seal
- [ ] Conformance test: sealed-plaintext denial for every role
- [ ] Emergency access (if implemented) needs two named approvers and is logged — default is no emergency path in V1 unless Security asks

## Dependencies and decisions

Required producer work: [#42](issue-42.md) (Kaustav), [#77](issue-77.md) (Gandharva).

R8 separates any specifically authorised system reference/seeding path. Emergency access remains outside routine APIs and requires its own approved procedure.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
