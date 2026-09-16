# #71: As the System, I want missing expected evidence to block the next step and raise an alert

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Declare and verify expected evidence for each protected transition and sealed version.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement the pre-seal assertion against synthetic complete and individually missing evidence sets; add the scheduled sealed-version sweep.

## Inputs and outputs

- Input: Version/hash, policy-versioned expected-record model, decisions/capability references, validation/asset/renderer records and actual audit entries.
- Output: Pass only when every required record is present, bound to the exact version and duty-clean; otherwise refusal plus an attributable alert.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR01-EVD-05](../../requirements.md#req-asr01-evd-05) | Each step declares the evidence it must produce. Before sealing, the system asserts that every expected record exists, verifies against the exact version hash, and was produced by an actor with no separation-of-duties conflict. | MUST |
| [ASR01-EVD-06](../../requirements.md#req-asr01-evd-06) | A missing, unbound or mismatched record blocks sealing and raises an alert naming the step and the absent record. Absence of expected evidence is an alert condition, not a silent pass. | MUST |
| [ASR01-EVD-10](../../requirements.md#req-asr01-evd-10) | A scheduled sweep re-asserts evidence completeness across sealed versions and alerts on drift. | SHOULD |
| [PRD-EVD-16](../../requirements.md#req-prd-evd-16) | GAP The expected-evidence model (table below) is declarative configuration versioned with the policy, so a new step or record can be added without code. The completeness assertion at sealing evaluates it and names the step and record on failure (EVD-05, EVD-06). | MUST |
| [PRD-EVD-19](../../requirements.md#req-prd-evd-19) | GAP D-35 Daily sweep (EVD-10) re-runs the completeness assertion for every sealed version and alerts on any drift with the version identifier and the absent record. | SHOULD |
| [ARC-02](../../requirements.md#req-arc-02) | Every state-changing operation and its audit record commit in the same database transaction. | MUST |
| [ASR01-EVD-07](../../requirements.md#req-asr01-evd-07) | Critical transitions fail closed when durable audit is unavailable. | MUST |

## Exact PRD sections

- [19. Evidence and Audit](../../prd/main-baseline.md#19-evidence-and-audit)
- [6.13 Expected evidence and audit · ASR01-EVD](../../prd/technical-baseline.md#613-expected-evidence-and-audit--asr01-evd)

## Behaviour to demonstrate

Replace a review record with one for an older version: sealing remains blocked although the number of records is unchanged.

Failure checks: Remove each expected record in turn; the protected transition must stop and produce an attributable content-free alert.

Existing issue acceptance criteria, retained for review:

- [ ] Each step declares the records it must produce
- [ ] A transition without those records fails and alerts (no content in the alert)
- [ ] A test that deletes an evidence row blocks the next transition

## Dependencies and decisions

Required producer work: [#45](issue-45.md) (Kaustav), [#46](issue-46.md) (Gandharva).

D-35 sweep cadence is configuration. The completeness assertion itself is required and cannot be waived by a successful diagnostic trace.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
