# #119: Verify the contributor first-run guide and first-PR path

Owner proposed in the delivery plan: **Nikhil**. Technical review: KKT for technical steps; Rohit for testability.
Epic: [#108](https://github.com/Bodhan-AI/open-rachana/issues/108). [Module route](../product.md).

Make the repository’s first-run and first-contribution route work for a new person.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Ask a contributor to follow the guide from a clean checkout, locate their first brief and run its smallest available fixture/test.

## Inputs and outputs

- Input: Current setup commands, contributor’s intended module, engineering handoff, synthetic acceptance scenario and PR review rules.
- Output: A short start page, verified commands and a recorded second-person walkthrough; failures link to issues instead of being described as working.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [UI-13](../../requirements.md#req-ui-13) | Every input is labelled; keyboard operation and screen-reader semantics are preserved throughout. | MUST |

## Exact PRD sections

- [14.1 Week 1 — Foundation and evidence backbone](../../prd/technical-baseline.md#141-week-1--foundation-and-evidence-backbone)
- [17.4 Release](../../prd/technical-baseline.md#174-release)

## Behaviour to demonstrate

A newcomer can find their module, its first issue, exact PRD rules and existing implementation PR without reading a chat transcript.

Existing issue acceptance criteria, retained for review:

- [ ] A second contributor follows the guide from a clean environment.
- [ ] Failures are tracked rather than described as working.
- [ ] The guide includes plan review, Humanizer readability, tests and required evidence.

## Dependencies and decisions

Required producer work: [#51](issue-51.md) (KKT), [#52](issue-52.md) (Rohit), [#94](issue-94.md) (KKT).

No new product decision. Keep private credentials and Restricted data out of the public guide; owner availability is not assumed.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
