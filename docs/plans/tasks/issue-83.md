# #83: As an Admin, I want to authorise a correction that revokes readiness and starts a new lineage

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Authorise corrections, revoke readiness immediately and preserve all sealed history through revalidation and supersession.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement authorisation/revocation/outbox atomically using a synthetic seeding result; connect real seeding only after R8.

## Inputs and outputs

- Input: Re-authenticated authorised actor, reason/scope, current sealed version, seeding authorisation and downstream registered consumers.
- Output: Immutable authorisation, readiness revocation, new primary or variant lineage, revalidation tasks, supersession notification and tracked acknowledgements.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM04-TRN-09](../../requirements.md#req-asm04-trn-09) | When the primary changes, dependent variants are marked as requiring revalidation and the translator is shown what changed. | MUST |
| [PRD-TRN-16](../../requirements.md#req-prd-trn-16) | GAP Revalidation (TRN-09, RES06-COR-03): when a corrected primary is sealed, each variant lineage is flagged requires_revalidation and a revalidate_variant task is created. Its workspace shows a field-level difference between the previous and new primary reference. The translator produces a new variant version bound to the new primary hash; it passes every gate; readiness returns only when every required language is resealed against the new primary. | MUST |
| [RES06-COR-01](../../requirements.md#req-res06-cor-01) | A correction to a sealed primary requires a recorded authorization and reason. | MUST |
| [RES06-COR-02](../../requirements.md#req-res06-cor-02) | A correction creates a new lineage, never overwrites sealed bytes, and immediately revokes readiness. | MUST |
| [RES06-COR-03](../../requirements.md#req-res06-cor-03) | Every dependent language variant is marked as requiring revalidation until resealed against the new primary. | MUST |
| [RES06-COR-04](../../requirements.md#req-res06-cor-04) | The superseded version records a reference to the version that replaced it. | MUST |
| [RES06-COR-05](../../requirements.md#req-res06-cor-05) | Downstream consumers are notified of supersession and must acknowledge. Unacknowledged supersession beyond a configured window raises an operational alert. | MUST |
| [PRD-COR-07](../../requirements.md#req-prd-cor-07) | GAP Correction authorization record: identifier, artefact identifier, sealed version identifier, scope (primary or a named variant), authorized by (Coordinator, re-authenticated), reason of at least 50 characters, created at, audit references. It emits correction.authorized. | MUST |
| [PRD-COR-08](../../requirements.md#req-prd-cor-08) | GAP D-16 Correction draft seeding. Because no human can read sealed plaintext, the system creates the correction draft: under the authorization record, the correction-seeding identity decrypts the sealed version in memory, creates a new lineage with a Draft holding that content, and assigns it to an eligible author by policy (the original author is eligible). The sealed bytes are untouched; the draft is Restricted and visible only to the assignee; the audit event records the source version hash and the authorization identifier. This is the only routine path by which sealed content re-enters the authoring tier, and it is a system action, never a read interface. | MUST |
| [PRD-COR-09](../../requirements.md#req-prd-cor-09) | GAP Readiness is revoked in the same transaction as the authorization (COR-02), and stays revoked until the new primary and every required variant are sealed against it. The reason is carried on readiness.changed. | MUST |
| [PRD-COR-10](../../requirements.md#req-prd-cor-10) | GAP D-25 Supersession notification: sealing the corrected primary marks the previous version Superseded with replaced_by, and the outbox delivers artefact.superseded to every registered consumer over mutual TLS (webhook), at least once with consumer-side deduplication by event identifier. Consumers acknowledge with POST /downstream/v1/supersession-acks carrying the event identifier, consumer identifier and a signature. A notice unacknowledged beyond the configured window (proposed 24 hours) raises an operational alert and appears on the coordinator board until acknowledged. | MUST |
| [PRD-COR-12](../../requirements.md#req-prd-cor-12) | GAP A correction scoped to one variant (a translation defect with a sound primary) creates a new lineage for that language only; the primary and other variants are untouched; readiness is revoked until the variant is resealed against the unchanged primary hash. | MUST |
| [PRD-VLT-11](../../requirements.md#req-prd-vlt-11) | GAP Encryption model: envelope encryption with a fresh 256-bit data key per sealed version (authenticated encryption), the data key wrapped by the active repository-tier key in the key management service. Key policy grants encrypt to the sealing identity only; decrypt to the verification identity (in-memory verification only, no plaintext output), the correction-seeding identity under a recorded authorization (§6.11), and the break-glass identity (§10.6). No human principal and no platform-administrator role holds decrypt. Every key use is logged by the key service and mirrored into audit. | MUST |
| [PRD-RDY-10](../../requirements.md#req-prd-rdy-10) | GAP Every change of readiness emits readiness.changed with the artefact identifier, previous and new status and the reason (sealed, correction, used, retired, revalidation). | MUST |

## Exact PRD sections

- [14. Versioning and Corrections](../../prd/main-baseline.md#14-versioning-and-corrections)
- [6.11 Correction and supersession (approval reset) · RES06-COR](../../prd/technical-baseline.md#611-correction-and-supersession-approval-reset--res06-cor)

## Behaviour to demonstrate

A translation-only defect revokes readiness and replaces that language lineage without rewriting the sound primary. Delayed assembly acknowledgement stays visible and alerts after the configured window.

Failure checks: Repeat correction requests and delay assembly acknowledgement; revoke readiness immediately, preserve old seals and surface overdue acknowledgement.

Existing issue acceptance criteria, retained for review:

- [ ] Admin authorises a correction with a recorded reason
- [ ] Readiness is revoked immediately; assembly is notified and must acknowledge
- [ ] New draft in a new lineage; sealed version becomes SUPERSEDED (never overwritten)
- [ ] Every translation is marked for re-validation; translators see what changed
- [ ] Full path again: Question Review → Accessibility → Translation → Translation Review → Accessibility
- [ ] Default: original Admin may write the correction of their own approved question

## Dependencies and decisions

Required producer work: [#80](issue-80.md) (Kaustav), [#81](issue-81.md) (Kaustav).

R8/D-16 block live decryption/seeding; D-25 sets acknowledgement delivery/window. A correction is never a general sealed-read endpoint.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
