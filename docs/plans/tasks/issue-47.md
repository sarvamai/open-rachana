# #47: As an Auditor, I want chain verification to fail on a tampered or missing record

Owner proposed in the delivery plan: **Gandharva**. Technical review: Kaustav; Security for key/retention controls.
Epic: [#104](https://github.com/Bodhan-AI/open-rachana/issues/104). [Module route](../evidence.md).

Expose content-free audit verification and detect missing, changed or reordered records and invalid anchors.

## Start here

PR #101 implements audit verification; inspect and extend that contribution.

First deliverable: Continue PR #101 before writing another endpoint. Add persisted-chain and restored-chain coverage when #46 supplies that store.

## Inputs and outputs

- Input: Chain identifier, optional sequence range, persisted events and signed checkpoints/external anchor.
- Output: Verification count, first failure and failure kind, times and a recorded chain.verified event; a failed verification raises an operational alert.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR01-EVD-02](../../requirements.md#req-asr01-evd-02) | Events are hash-chained. The chain construction, genesis record and verification procedure are specified and implemented. | MUST |
| [ASR01-EVD-03](../../requirements.md#req-asr01-evd-03) | Chain verification is runnable on demand and detects any removed or altered event. | MUST |
| [PRD-EVD-14](../../requirements.md#req-prd-evd-14) | GAP Verification procedure: inputs are chain identifier and an optional sequence range (default: from the last verified checkpoint, or from genesis); the verifier walks events in sequence order, checks contiguity, recomputes each hash, compares with the stored hash and with the following event's previous hash, and verifies every checkpoint signature and the external anchor. Output: events verified, first failing sequence, failure kind (missing, altered, reordered, bad checkpoint), start and finish times. It runs on demand from the evidence view or an operator command, and daily on schedule. The result is itself written as chain.verified; a failure raises a Critical alert and invokes the runbook. | MUST |

## Exact PRD sections

- [19. Evidence and Audit](../../prd/main-baseline.md#19-evidence-and-audit)
- [6.13 Expected evidence and audit · ASR01-EVD](../../prd/technical-baseline.md#613-expected-evidence-and-audit--asr01-evd)
- [8.5 Similarity fingerprint](../../prd/technical-baseline.md#85-similarity-fingerprint)

## Behaviour to demonstrate

Delete one event from a synthetic copy: report its first missing sequence. Change an event and recompute downstream hashes: the external anchor must still detect the rewrite.

Failure checks: Alter and remove stored events; identify the first invalid link. Re-run verification after restore with unchanged canonical bytes.

Existing issue acceptance criteria, retained for review:

- [ ] Conformance test: persist N events, mutate or delete one row, `verify()` is ok=False with first_bad_seq
- [ ] On-demand verify endpoint (Admin/Auditor only) returns a content-free result
- [ ] Daily verification hook alerts on failure — alert has no question content
- [ ] CI runs the tamper test against the real store

## Dependencies and decisions

Required producer work: [#46](issue-46.md) (Gandharva).

R6/D-02 determine the accepted checkpoint/byte profile. Existing in-memory verification is useful but does not close restore or anchor checks.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
