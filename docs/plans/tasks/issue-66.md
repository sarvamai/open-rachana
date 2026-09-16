# #66: As a Question Reviewer, I want to comment, approve against the checklist, or reject with a reason

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Record question-review decisions with complete attestations and immutable rejection history.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement one-review approve/return cases and then the configured two-review aggregation, including competing decisions.

## Inputs and outputs

- Input: Assignee/version/hash, structured checklist, three separate attestations and sources, rationale/reason, difficulty, policy and renderer versions.
- Output: Append-only decision and atomic state/evidence update; rejection creates a linked draft with findings for the author and a different future reviewer.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-REV-04](../../requirements.md#req-asm03-rev-04) | The reviewer validates correctness and checks the classification, difficulty and taxonomy level assigned by the author against the syllabus version in force. | MUST |
| [ASM03-REV-05](../../requirements.md#req-asm03-rev-05) | Approval requires a complete checklist. Return requires a reason code and actionable comments. | MUST |
| [ASM03-REV-06](../../requirements.md#req-asm03-rev-06) | Approval moves the exact version to accessibility check. A return creates a new linked draft carrying the findings; the returned version remains as immutable evidence. | MUST |
| [ASM03-REV-07](../../requirements.md#req-asm03-rev-07) | Decisions are append-only and bind the checklist, rationale, reviewer audit identifier, duration and version hash. | MUST |
| [ASM03-REV-10](../../requirements.md#req-asm03-rev-10) | Whether one or two independent reviews are required before approval is configuration, not code. | MUST |
| [ASM03-REV-11](../../requirements.md#req-asm03-rev-11) | The reviewer records an explicit attestation, inside the mandatory checklist, covering three checks: language and grammatical correctness; that the artefact is not available in the public domain; and that it complies with the prescribed guidelines and curriculum scope for the cycle. Each is recorded separately with the source consulted, not as a single combined tick. | MUST |
| [ASM03-REV-12](../../requirements.md#req-asm03-rev-12) | The reviewer assigns a difficulty value from the controlled vocabulary at the point of approval. The field for discrimination is created and left empty; it is populated only from candidate performance data after an exam and is never estimated. | MUST |
| [PRD-REV-13](../../requirements.md#req-prd-rev-13) | GAP D-19 The structured checklist is a configured template per cycle with the items listed below. Every item is Pass, Fail or Not applicable (with a reason). Approval requires every item Pass or Not applicable and all three attestations complete with a source. The equivalence-judgement item appears only for variants. | MUST |
| [PRD-REV-14](../../requirements.md#req-prd-rev-14) | GAP D-19 Return reason codes are a controlled vocabulary (below). A return requires one code and comments of at least 20 characters; the controls stay disabled until both are satisfied. | MUST |
| [PRD-REV-15](../../requirements.md#req-prd-rev-15) | GAP Decision record fields: identifier; version identifier and version hash; decision type (review, translation review, accessibility); outcome; checklist responses; attestations with sources; reason code; comments; difficulty assigned; equivalence judgement; reviewer audit identifier; capability entry identifier valid at the time; renderer version; policy version; opened at; decided at; duration; correlation identifier. The record's own hash is written into the audit event. | MUST |
| [PRD-REV-16](../../requirements.md#req-prd-rev-16) | GAP Two-review policy (REV-10): when the cycle requires two reviews, the version stays In Review until two approvals from different, duty-clean reviewers exist; the second reviewer cannot see the first reviewer's checklist until their own decision is recorded; a single return sends the version back regardless of other approvals. | MUST |
| [PRD-REV-17](../../requirements.md#req-prd-rev-17) | GAP A return creates the successor Draft with derived_from set, attaches the findings so they appear inside the editor beside the fields they name, and assigns the draft to the original author, or to the pool if that author is no longer eligible. | MUST |
| [PRD-REV-18](../../requirements.md#req-prd-rev-18) | GAP D-06 Correct-answer visibility in review is governed by the cycle flag reviewer_sees_key (SEC-02). Proposed default: true, because validating correctness (REV-04) requires knowing the key. When false, the reviewer is asked to identify the key and the workspace records whether it matched. | MUST |
| [PRD-REV-21](../../requirements.md#req-prd-rev-21) | GAP Comments: every review role may add free-text comments to its decision; comments are Restricted, visible to the Admin and carried into the successor draft, and never visible to any other reviewer (engineering PRD). | MUST |
| [ASM03-REV-08](../../requirements.md#req-asm03-rev-08) | An open question or artefact is locked to the assigned reviewer. A second actor attempting a decision on an already-decided version is rejected with a clear message. | MUST |
| [PRD-ASG-10](../../requirements.md#req-prd-asg-10) | GAP Different reviewer after rejection (engineering PRD): the successor version of a rejected version is assigned, at the same stage, to a reviewer other than the one who rejected it and other than any earlier rejecting reviewer of that lineage. If no other eligible reviewer exists the task stays Unassigned and the Admin is alerted; the Admin cannot override this rule. | MUST |

## Exact PRD sections

- [9.3 Actions](../../prd/main-baseline.md#93-actions)
- [9.4 Checklist](../../prd/main-baseline.md#94-checklist)
- [9.5 Approval](../../prd/main-baseline.md#95-approval)
- [9.6 Rejection](../../prd/main-baseline.md#96-rejection)
- [6.6 Question review · ASM03-REV](../../prd/technical-baseline.md#66-question-review--asm03-rev)

## Behaviour to demonstrate

Omit the public-domain attestation source and approval fails. In a two-review cycle, one approval does not advance; any return sends the version back.

Failure checks: Omit each attestation/reason, use stale task ownership and repeat a decision; refuse incomplete/conflicting requests and preserve linked corrections.

Existing issue acceptance criteria, retained for review:

- [ ] Actions: read, comment, approve, reject — no edit
- [ ] Approve requires every checklist item plus attestations 1–3 (language/grammar + source; not public-domain + source; in-scope + source) and a difficulty from the controlled list
- [ ] Approve moves the version to Accessibility
- [ ] Reject requires a reason + comment; Admin gets a correction draft; a *different* Question Reviewer is assigned next
- [ ] Cycle setting controls one vs two question reviewers

## Dependencies and decisions

Required producer work: [#65](issue-65.md) (Divyansh), [#68](issue-68.md) (Kaustav).

D-06/D-19 and R12 govern review count/checklist values. Support configurable count and isolation between independent reviewers.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
