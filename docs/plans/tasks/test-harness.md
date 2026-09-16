# #115: Build shared contract fixtures and the first end-to-end acceptance harness

Owner proposed in the delivery plan: **Rohit**. Technical review: KKT; feature owners.
Epic: [#107](https://github.com/Bodhan-AI/open-rachana/issues/107). [Module route](../testing.md).

Provide shared fixtures and a contract/integration harness used by all feature owners.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement the manual draft-to-independent-review scenario and direct-API self-approval refusal; extend through accessibility/sealing/languages as producers merge.

## Inputs and outputs

- Input: Versioned task/API schemas, synthetic roles/languages/questions, provider doubles and real test persistence.
- Output: Reusable fixtures and tests spanning allowed/refused/retried operations, with results mapped to requirement IDs.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ARC-02](../../requirements.md#req-arc-02) | Every state-changing operation and its audit record commit in the same database transaction. | MUST |
| [INT-03](../../requirements.md#req-int-03) | Retryable mutations accept an idempotency key and are safe to repeat. | MUST |
| [SEC-06](../../requirements.md#req-sec-06) | Separation of duties is provable through both the interface and a hand-crafted direct API call. | MUST |
| [SEC-03](../../requirements.md#req-sec-03) | Automated tests assert that no non-permitted role receives correct-answer or sealed-plaintext fields in any response body. | MUST |

## Exact PRD sections

- [13.1 Levels](../../prd/technical-baseline.md#131-levels)
- [13.2 Mandated automated suites](../../prd/technical-baseline.md#132-mandated-automated-suites)
- [13.4 Synthetic corpus](../../prd/technical-baseline.md#134-synthetic-corpus)
- [13.5 Evidence pack](../../prd/technical-baseline.md#135-evidence-pack)

## Behaviour to demonstrate

The same actor fixture with two roles still fails own-work approval. Killing a transaction proves both the domain and audit writes roll back.

Existing issue acceptance criteria, retained for review:

- [ ] Allowed and refused examples exercise the same published API contract.
- [ ] The first author/reviewer path proves direct-API self-approval refusal.
- [ ] Failure, retry and transaction tests retain results linked to requirements.
- [ ] Desktop restrictions receive native validation; browser tests are not substituted.

## Dependencies and decisions

Required producer work: [#52](issue-52.md) (Rohit).

Rohit owns the harness; each feature owner supplies its tests. Signed-client and expert security/accessibility checks remain separate evidence types.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
