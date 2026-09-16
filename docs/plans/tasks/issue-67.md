# #67: As the System, I want to assign one eligible reviewer per question per stage by workload

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Assign tasks by recognised capability, duty eligibility and deterministic workload order.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement eligibility and deterministic tie-breaking as pure tests, then transactional assignment and expiry/revocation handling.

## Inputs and outputs

- Input: Task type, subject/language, lineage actors, valid registry entries, open workloads, assignment history and policy version.
- Output: Append-only assignment/release/reassignment records, expiry handling, My Work notification and visible unassigned state.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INS04-CAP-05](../../requirements.md#req-ins04-cap-05) | Assignment requires a current, non-revoked, in-scope entry in the registry. Subject, language and workload matching alone do not authorize an assignment. | MUST |
| [INS04-CAP-06](../../requirements.md#req-ins04-cap-06) | Expiry blocks new assignment and flags in-flight tasks for reassignment. It never voids a decision already recorded. | MUST |
| [ASM03-REV-01](../../requirements.md#req-asm03-rev-01) | Submitted versions are assigned to eligible reviewers by system policy using subject, language, workload, recognized capability and separation of duties. Authors cannot nominate reviewers. | MUST |
| [ASM03-REV-08](../../requirements.md#req-asm03-rev-08) | An open question or artefact is locked to the assigned reviewer. A second actor attempting a decision on an already-decided version is rejected with a clear message. | MUST |
| [ASM03-REV-09](../../requirements.md#req-asm03-rev-09) | Tasks expire after a configured period and return to the assignment pool. Aging is visible to coordinators. | MUST |
| [PRD-ASG-01](../../requirements.md#req-prd-asg-01) | GAP Task types: author_primary, review, accessibility_check, translate, translation_review, revalidate_variant, correct_primary. Each maps to exactly one role. | MUST |
| [PRD-ASG-02](../../requirements.md#req-prd-asg-02) | GAP Assignment record: identifier, task type, user audit identifier, subject reference (version, lineage or artefact), cycle, language, created at, expires at, status (Active, Completed, Released, Expired, Reassigned), release reason, policy version used. Assignments are append-only; reassignment closes one and opens another. | MUST |
| [PRD-ASG-03](../../requirements.md#req-prd-asg-03) | GAP Eligibility: a current, non-revoked capability entry whose role matches the task type and whose subject and language scope cover the artefact; accessibility qualification for accessibility tasks; no separation-of-duties conflict (§4.4); open-task workload below the configured cap D-13. The version's author can never be in the pool for that lineage. | MUST |
| [PRD-ASG-04](../../requirements.md#req-prd-asg-04) | GAP Selection is deterministic: lowest current open workload first, then longest time since last assignment, then stable ordering by audit identifier. The policy version and the candidate count are recorded on the assignment. A coordinator's manual assignment must pass the same eligibility check server-side. | MUST |
| [PRD-ASG-05](../../requirements.md#req-prd-asg-05) | GAP When no eligible user exists the task stays Unassigned, appears on the coordinator board immediately, and raises an operational alert after the configured delay D-12. | MUST |
| [PRD-ASG-06](../../requirements.md#req-prd-asg-06) | GAP Expiry: an assignment past its deadline is released to the pool by a sweep running at least every 5 minutes, audited, and shown in coordinator aging. The version's state is unchanged. A decision recorded before expiry is never voided. | MUST |
| [PRD-ASG-07](../../requirements.md#req-prd-asg-07) | GAP Surfacing (UI-03): a new or returned task is pushed to the assignee's open My Work screen over the server-push channel and shown as an in-app notification badge. Any out-of-band notification channel D-19 carries only "You have a new task" and a link — no artefact identifier, subject or content (DAT-03). | MUST |
| [PRD-ASG-08](../../requirements.md#req-prd-asg-08) | GAP Locking (REV-08): opening a review or accessibility task records the opening time; a decision is accepted only from the assignee and only while the version is still in the decided-from state. A second decision on an already-decided version returns CONFLICT_ALREADY_DECIDED and the caller's queue refreshes. | MUST |
| [PRD-ASG-09](../../requirements.md#req-prd-asg-09) | GAP When an assignee leaves or loses recognized capability mid-task, the assignment is released to the pool by the next request or the sweep, whichever is first; no task is orphaned; decisions already recorded remain valid. | MUST |
| [PRD-ASG-10](../../requirements.md#req-prd-asg-10) | GAP Different reviewer after rejection (engineering PRD): the successor version of a rejected version is assigned, at the same stage, to a reviewer other than the one who rejected it and other than any earlier rejecting reviewer of that lineage. If no other eligible reviewer exists the task stays Unassigned and the Admin is alerted; the Admin cannot override this rule. | MUST |
| [PRD-ASG-11](../../requirements.md#req-prd-asg-11) | GAP Task types are extended for the converged workflow: accessibility_remediation (Accessibility Specialist) is distinct from accessibility_review (Accessibility Reviewer); the Admin's assignment board shows both. | MUST |
| [PRD-NTF-01](../../requirements.md#req-prd-ntf-01) | In-app notifications exist for: new assignment; task returned with findings; task approaching expiry (24 hours before); exception approved, revoked or expired; correction authorized (coordinator); equivalent-route escalation (coordinator); sealing failure (coordinator and operations); supersession unacknowledged (operations); assignment pool empty (coordinator). | MUST |
| [PRD-NTF-02](../../requirements.md#req-prd-ntf-02) | No notification in any channel contains artefact content, a correct answer, or a rendering. Out-of-band channels D-19 carry only the task type and a link. | MUST |
| [INS04-CAP-04](../../requirements.md#req-ins04-cap-04) | A registry records, against a pseudonymous workforce audit identifier, what each contributor is recognized to do: role, subject and language scope, accessibility qualification, issuing authority, validity window and revocation state. | MUST |
| [INS04-CAP-07](../../requirements.md#req-ins04-cap-07) | A user may hold multiple roles but is blocked from authoring or translating and then approving the same version. The API enforces this independently of the interface. | MUST |
| [INS04-CAP-08](../../requirements.md#req-ins04-cap-08) | An accessibility specialist cannot act on a version they authored, translated or reviewed. | MUST |
| [PRD-CAP-18](../../requirements.md#req-prd-cap-18) | GAP Authorization reads the registry on every request. Any cache is at most 5 seconds and is invalidated synchronously on revocation, so CAP-10 holds. An hourly sweep marks expired entries, flags their in-flight assignments on the coordinator board, and leaves recorded decisions untouched. | MUST |

## Exact PRD sections

- [15. Reviewer Assignment](../../prd/main-baseline.md#15-reviewer-assignment)
- [6.3 Work assignment and My Work](../../prd/technical-baseline.md#63-work-assignment-and-my-work)
- [6.15 Notifications and alerts (cross-cutting)](../../prd/technical-baseline.md#615-notifications-and-alerts-cross-cutting)

## Behaviour to demonstrate

When no eligible reviewer exists, keep the task Unassigned and alert under configured policy. Admin manual assignment cannot select an earlier rejecting reviewer for the corrected version.

Failure checks: Create ties, expired work, changed eligibility and prior-lineage conflicts; demonstrate deterministic assignment and a new reviewer after correction.

Existing issue acceptance criteria, retained for review:

- [ ] Eligible = right role, subject, language, valid registry entry, no conflict of duty
- [ ] Lowest active workload first; tie-break = longest time since last assignment
- [ ] A corrected question goes to a different reviewer
- [ ] A reviewer never gets an item they authored, translated, or reviewed at another stage
- [ ] Unanswered tasks expire back to the pool; Admin sees aging
- [ ] Admin can reassign or release, still inside the same rules

## Dependencies and decisions

Required producer work: [#42](issue-42.md) (Kaustav), [#44](issue-44.md) (Kaustav), [#45](issue-45.md) (Kaustav).

D-12/D-13/D-19 and R12 configure timing/workload/count. One review task has one assignee; a cycle may require several independent tasks.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
