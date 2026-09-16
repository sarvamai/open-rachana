# #48: As an Auditor, I want to search the audit trail and never see question content

Owner proposed in the delivery plan: **Gandharva**. Technical review: Kaustav; Security for key/retention controls.
Epic: [#104](https://github.com/Bodhan-AI/open-rachana/issues/104). [Module route](../evidence.md).

Give auditors a restricted evidence search and verification result without a question-content path.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement one search query and verify action with fake safe events, then connect #46/#47 and a read-only surface or approved equivalent script.

## Inputs and outputs

- Input: Auditor capability; actor/action/artefact/time filters; opaque cursor; verification result from #47.
- Output: Paginated allowlisted event metadata and checkpoint status; on-demand verification for authorised auditors, with no Restricted free text.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR01-EVD-08](../../requirements.md#req-asr01-evd-08) | An evidence view provides read-only audit search by actor, action, artefact and time range, and displays the verification result. (P1 — may reduce to a scripted operator procedure if Week 3 capacity is strained.) | SHOULD |
| [PRD-EVD-17](../../requirements.md#req-prd-evd-17) | GAP D-27 Evidence view (EVD-08): read-only search by actor audit identifier, action, artefact or version identifier and time range; event detail with no content; the latest verification result and checkpoint; a "verify now" control for auditors. If reduced to a scripted procedure, the script must produce the same search and verification output to a file readable by the auditor. | SHOULD |
| [UI-12](../../requirements.md#req-ui-12) | Evidence — read-only audit search and chain-verification result. (P1.) | SHOULD |

## Exact PRD sections

- [5.8 Other roles](../../prd/main-baseline.md#58-other-roles)
- [19. Evidence and Audit](../../prd/main-baseline.md#19-evidence-and-audit)
- [6.13 Expected evidence and audit · ASR01-EVD](../../prd/technical-baseline.md#613-expected-evidence-and-audit--asr01-evd)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)

## Behaviour to demonstrate

An Auditor can find a version’s review event and hash, but cannot obtain the review comments, answer or rendering by expanding the result or changing the endpoint.

Failure checks: Attempt forbidden content fields and another role’s endpoint; filters and result counts must not reveal question text or restricted context.

Existing issue acceptance criteria, retained for review:

- [ ] Auditor can filter by actor (pseudonymous), action, object ref, time
- [ ] Response schema has no stem, options, explanation, or translation text fields
- [ ] Admin may open the same content-free view in the pilot

## Dependencies and decisions

Required producer work: [#42](issue-42.md) (Kaustav), [#46](issue-46.md) (Gandharva).

D-27 chooses UI versus equivalent scripted output; security of the evidence API is required in either case.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
