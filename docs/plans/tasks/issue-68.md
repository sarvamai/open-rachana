# #68: As the System, I want self-approval and cross-stage reuse of the same person to fail on the API

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Enforce separation of duties across the entire version lineage and every approval endpoint.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Create a shared conflict evaluator used by assignment and decision APIs; exercise each role combination directly.

## Inputs and outputs

- Input: Actor’s current capabilities plus authors, translators, remediators, prior reviewers and rejecting reviewers for the lineage.
- Output: Server-side refusal with unchanged task/version and content-free evidence whenever an actor conflicts.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INS04-CAP-07](../../requirements.md#req-ins04-cap-07) | A user may hold multiple roles but is blocked from authoring or translating and then approving the same version. The API enforces this independently of the interface. | MUST |
| [INS04-CAP-08](../../requirements.md#req-ins04-cap-08) | An accessibility specialist cannot act on a version they authored, translated or reviewed. | MUST |
| [SEC-06](../../requirements.md#req-sec-06) | Separation of duties is provable through both the interface and a hand-crafted direct API call. | MUST |
| [PRD-ASG-03](../../requirements.md#req-prd-asg-03) | GAP Eligibility: a current, non-revoked capability entry whose role matches the task type and whose subject and language scope cover the artefact; accessibility qualification for accessibility tasks; no separation-of-duties conflict (§4.4); open-task workload below the configured cap D-13. The version's author can never be in the pool for that lineage. | MUST |
| [PRD-ASG-10](../../requirements.md#req-prd-asg-10) | GAP Different reviewer after rejection (engineering PRD): the successor version of a rejected version is assigned, at the same stage, to a reviewer other than the one who rejected it and other than any earlier rejecting reviewer of that lineage. If no other eligible reviewer exists the task stays Unassigned and the Admin is alerted; the Admin cannot override this rule. | MUST |
| [ARC-01](../../requirements.md#req-arc-01) | Authorization is evaluated server-side on every request using role, assignment, version, language, lifecycle state, cycle policy, recognized capability and separation of duties. Client-supplied role claims are never trusted. | MUST |

## Exact PRD sections

- [5. Roles](../../prd/main-baseline.md#5-roles)
- [15. Reviewer Assignment](../../prd/main-baseline.md#15-reviewer-assignment)
- [17. Security](../../prd/main-baseline.md#17-security)
- [4.4 Separation-of-duties rules](../../prd/technical-baseline.md#44-separation-of-duties-rules)
- [6.2 Recognized capability and access · INS04-CAP](../../prd/technical-baseline.md#62-recognized-capability-and-access--ins04-cap)
- [6.3 Work assignment and My Work](../../prd/technical-baseline.md#63-work-assignment-and-my-work)

## Behaviour to demonstrate

Giving the author a second reviewer role does not allow approval. An Accessibility Specialist cannot remediate a version they previously reviewed.

Failure checks: Call every approval endpoint as the author/remediator/translator and as a conflicting prior reviewer; prove server refusal across the lineage.

Existing issue acceptance criteria, retained for review:

- [ ] The person who writes never approves — 403 on a direct API call
- [ ] A reviewer who already touched the item at another stage cannot act again
- [ ] Accessibility Reviewer cannot act on a question they authored, remediated, or reviewed before
- [ ] Translation Reviewer cannot review a translation they wrote
- [ ] Tests live under `tests/conformance/`

## Dependencies and decisions

Required producer work: [#42](issue-42.md) (Kaustav), [#45](issue-45.md) (Kaustav).

R4’s separate Author extension must preserve these restrictions. Product policy is not inferred from whichever role is selected in the UI.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
