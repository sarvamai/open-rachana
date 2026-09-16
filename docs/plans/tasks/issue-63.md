# #63: As an Admin, I want submit to freeze the version, hash it, and give me a receipt

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Submit a draft atomically into immutable review with evidence and a reproducible receipt.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Integrate #53/#61/#67 against persistence and prove repeat-submit and competing-submit behaviour.

## Inputs and outputs

- Input: Current draft token, idempotency key, validation report, policy/renderer versions and eligible assignment service.
- Output: Frozen submitted version/hash, validation/similarity evidence, review task, audit/outbox and receipt; all required database writes commit together.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-VAL-04](../../requirements.md#req-asm03-val-04) | Submission creates an immutable version and a content hash. Subsequent editing cannot alter the version under review. | MUST |
| [ASM03-VAL-05](../../requirements.md#req-asm03-val-05) | The author receives a submission confirmation of the question. | MUST |
| [PRD-VAL-10](../../requirements.md#req-prd-val-10) | GAP Submission transaction: validate → sanitize and canonicalize (§8.4) → compute content hash → create the immutable version snapshot in state In Review → persist the validation report and similarity result → write the audit event → enqueue domain events in the transactional outbox → return the receipt (version identifier, content hash, submission time, rule-set version). If the audit store is unavailable the submission fails closed (ASR01-EVD-07). | MUST |
| [PRD-VAL-11](../../requirements.md#req-prd-val-11) | GAP Submission is idempotent: repeating it with the same draft concurrency token returns the original receipt and creates no second version. | MUST |
| [ARC-02](../../requirements.md#req-arc-02) | Every state-changing operation and its audit record commit in the same database transaction. | MUST |
| [ARC-03](../../requirements.md#req-arc-03) | Domain and audit events are delivered from a transactional outbox after commit, at least once, with consumer-side deduplication by event identifier. | MUST |
| [INT-03](../../requirements.md#req-int-03) | Retryable mutations accept an idempotency key and are safe to repeat. | MUST |
| [ASM03-REV-01](../../requirements.md#req-asm03-rev-01) | Submitted versions are assigned to eligible reviewers by system policy using subject, language, workload, recognized capability and separation of duties. Authors cannot nominate reviewers. | MUST |

## Exact PRD sections

- [8.4 Submit](../../prd/main-baseline.md#84-submit)
- [6.5 Validation and submission · ASM03-VAL](../../prd/technical-baseline.md#65-validation-and-submission--asm03-val)
- [8.4 Canonicalization rule v1](../../prd/technical-baseline.md#84-canonicalization-rule-v1)

## Behaviour to demonstrate

Retry the same submitted token and receive the original receipt. If durable audit fails, no submitted version or review assignment appears.

Failure checks: Repeat and race submit requests; preserve one immutable version, receipt and legal assignment, with atomic evidence and stale-write refusal.

Existing issue acceptance criteria, retained for review:

- [ ] Submit writes an immutable version + content hash and returns a receipt
- [ ] Editing that version after submit is impossible
- [ ] A reviewer is assigned automatically (or the assignment story's hook is called)
- [ ] State becomes IN_QUESTION_REVIEW
- [ ] A later rejection creates a new linked draft; the submitted version stays as evidence

## Dependencies and decisions

Required producer work: [#53](issue-53.md) (Kaustav), [#61](issue-61.md) (Kaustav), [#67](issue-67.md) (Kaustav).

R6 affects accepted canonical bytes; use the versioned contract and do not silently change it. No new product decision is needed to require atomic submission.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
