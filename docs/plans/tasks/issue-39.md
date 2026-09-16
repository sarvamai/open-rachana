# #39: As Content Operations, I want pilot languages and named people recorded

Owner proposed in the delivery plan: **Nikhil**. Technical review: KKT for technical steps; Rohit for testability.
Epic: [#108](https://github.com/Bodhan-AI/open-rachana/issues/108). [Module route](../product.md).

Prepare the named pilot roster and operating prerequisites used to configure a cycle.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Create a synthetic roster illustrating a duty-clean primary and language review path; obtain private confirmation of real participants separately.

## Inputs and outputs

- Input: People nominated by the adopting organisation; recognised subject/language capabilities; accessibility credentials; available review capacity.
- Output: Roster by role and language, a record of unresolved appointments, and the actual operating-precondition checklist. Keep personal contact details outside public GitHub.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ASG-03](../../requirements.md#req-prd-asg-03) | GAP Eligibility: a current, non-revoked capability entry whose role matches the task type and whose subject and language scope cover the artefact; accessibility qualification for accessibility tasks; no separation-of-duties conflict (§4.4); open-task workload below the configured cap D-13. The version's author can never be in the pool for that lineage. | MUST |

## Exact PRD sections

- [5. Roles](../../prd/main-baseline.md#5-roles)
- [15. Reviewer Assignment](../../prd/main-baseline.md#15-reviewer-assignment)
- [17. Security](../../prd/main-baseline.md#17-security)
- [14.0 Week 0 — the start line](../../prd/technical-baseline.md#140-week-0--the-start-line)
- [14.7 People](../../prd/technical-baseline.md#147-people)
- [16.1 Operating preconditions](../../prd/technical-baseline.md#161-operating-preconditions)

## Behaviour to demonstrate

If one participant authored a version, assigning them as its reviewer must remain prohibited even when the roster gives them both roles. A language with no qualified reviewer is a visible capacity gap.

Failure checks: Reject an incomplete or conflicting roster; keep pilot languages configurable. Separate remediation and approval roles even when a professional holds more than one role.

Existing issue acceptance criteria, retained for review:

- [ ] ADR-0006 is amended in place with the three pilot language names (primary + two variants)
- [ ] A roster of named people and roles is recorded (no credentials): 2 Admins, 2 Question Reviewers, 1 accessibility professional, 2 Translators, 1 coordinator, 1 Integrity Operator
- [ ] Languages remain `cycle.required_languages` configuration — no `if lang ==` in platform/

## Dependencies and decisions

No upstream feature is required to prepare the first deliverable.

D-29; D-45. Naming languages and participants belongs to Content Operations and the adopter; no invented commitments.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
