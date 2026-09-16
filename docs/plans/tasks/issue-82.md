# #82: As Assembly, I want to mark a question USED and later ARCHIVED via signed messages

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Accept signed selection/completion notifications and apply Used/Archived transitions idempotently.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement replay/signature/time/stale-version tests for one selection batch, then completion and resumable archive rotation.

## Inputs and outputs

- Input: Assembly workload identity, detached signature/key ID, notification/exam IDs, issue time, selected artefact IDs and expected primary versions.
- Output: Recorded notification result, atomic lifecycle updates/evidence, and an archive-key rewrap job with visible pending/failure state.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM06-LFC-01](../../requirements.md#req-asm06-lfc-01) | The system accepts a signed selection notification from the assembly service and atomically transitions the primary and every published language variant of the selected artefact to Used. No human actor initiates the transition. | MUST |
| [ASM06-LFC-02](../../requirements.md#req-asm06-lfc-02) | A Used artefact is immutable and is excluded from every subsequent readiness query. One that was not selected remains available in the eligible pool. | MUST |
| [ASM06-LFC-03](../../requirements.md#req-asm06-lfc-03) | On the exam-completion event, every Used artefact in that session transitions atomically to Archived. There is no return path to Published or Used. | MUST |
| [ASM06-LFC-04](../../requirements.md#req-asm06-lfc-04) | Archival writes the exam identifier, the archival timestamp and the artefact-set hash to the audit chain, so a session can be reconstructed evidentially. | MUST |
| [ASM06-LFC-05](../../requirements.md#req-asm06-lfc-05) | Read access to an Archived artefact is limited to audit and dispute roles under the break-glass procedure in §10.6. | MUST |
| [ASM06-LFC-06](../../requirements.md#req-asm06-lfc-06) | Encryption keys rotate from the active tier to the archive tier on archival, and the rotation is recorded. | MUST |
| [PRD-LFC-07](../../requirements.md#req-prd-lfc-07) | GAP D-26 Selection notification contract: POST /downstream/v1/selection-notifications with body notification identifier, exam session identifier, cycle code, list of selected artefact identifiers with the expected current primary version identifier, and issued-at; a detached signature (JSON Web Signature by the assembly signing key, key identifier included) plus mutual TLS and an audience token. Validation: signature valid against the registered key set; issued-at within 5 minutes of clock skew; notification identifier unused (a replay returns the original result); every artefact ready and its current primary matching the expected version. Proposed default: all-or-nothing per notification — any artefact not ready rejects the whole notification with SELECTION_NOT_READY listing the identifiers. On success one transaction sets the primary and every sealed variant to Used, records the exam session, writes audit events and emits artefact.used. | MUST |
| [PRD-LFC-08](../../requirements.md#req-prd-lfc-08) | GAP Exam-completion contract: POST /downstream/v1/exam-completions with exam session identifier and completed-at, signed as above. In one transaction every Used artefact of that session becomes Archived and the audit chain receives an event carrying the exam identifier, the timestamp and the artefact-set hash (SHA-256 over the sorted list of sealed content hashes). A key-rotation job then re-wraps each data key with the archive-tier key and records the rotation; until it completes the artefact is Archived with rotation pending, visible to operations. | MUST |
| [PRD-LFC-09](../../requirements.md#req-prd-lfc-09) | GAP Archived metadata (identifiers, hashes, classification, manifests) remains readable to auditors through the evidence view; content is reachable only through the break-glass procedure. | MUST |
| [PRD-LFC-10](../../requirements.md#req-prd-lfc-10) | GAP A selection notification naming an artefact that is Used, Archived, Retired or under correction is rejected with a code naming the artefact and its state, and raises an operational alert, because it indicates a stale assembly view. | MUST |
| [PRD-INT-13](../../requirements.md#req-prd-int-13) | GAP Machine-interface security: mutual TLS with certificates from the enterprise authority; tokens with audience, issuer, expiry ≤ 5 minutes and a key identifier resolved through a published key set; signed notifications use a detached JSON Web Signature with replay protection by notification identifier and a 5-minute clock-skew window; key rotation is supported without downtime. | MUST |

## Exact PRD sections

- [13. Question Lifecycle](../../prd/main-baseline.md#13-question-lifecycle)
- [6.12 Downstream lifecycle states · ASM06-LFC](../../prd/technical-baseline.md#612-downstream-lifecycle-states--asm06-lfc)
- [7.1 Mandatory interface behaviours](../../prd/technical-baseline.md#71-mandatory-interface-behaviours)

## Behaviour to demonstrate

Replay an accepted notification and return its original result. A notification with one stale primary must follow the approved batch-atomicity rule, never silently select the rest.

Failure checks: Replay, forge and reorder lifecycle events; apply valid events idempotently and never accept a human state override.

Existing issue acceptance criteria, retained for review:

- [ ] Signed notification moves FULLY_APPROVED → USED when selected for an exam session
- [ ] Signed notification moves USED → ARCHIVED when the session is complete and keys rotate to archive tier
- [ ] Human roles cannot set these states

## Dependencies and decisions

Required producer work: [#81](issue-81.md) (Kaustav).

D-26 sets batch atomicity; prototype both tests against explicit configuration until approved. R8 governs any exceptional archived-content access.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
