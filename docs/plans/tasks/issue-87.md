# #87: As the Accessibility lead, I want a WCAG 2.1 AA audit of authoring and review surfaces closed

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Qualify all required role surfaces with keyboard, screen reader and supported-script checks.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Cover a full author-to-review task and configuration/oversight navigation manually, then extend to both accessibility roles and translation.

## Inputs and outputs

- Input: Built signed client and web oversight screens, agreed OS/assistive-technology matrix, synthetic corpus and reference renderer version.
- Output: Per-surface findings and retest evidence for focus/order/labels/contrast/zoom/tables/equations/language direction; named accessibility acceptance.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [UI-13](../../requirements.md#req-ui-13) | Every input is labelled; keyboard operation and screen-reader semantics are preserved throughout. | MUST |
| [PRD-ACC-13](../../requirements.md#req-prd-acc-13) | GAP Test affordances (ACC-02) provided on the reference rendering without altering content: keyboard-only navigation mode with visible focus order; screen-reader-oriented view exposing the accessible name, role and MathML of each element; text-only view; zoom at 200 % and 400 %; contrast measurement per text element; a reading-order outline. | MUST |
| [PRD-ATH-24](../../requirements.md#req-prd-ath-24) | GAP Scripts and direction: every text field accepts full Unicode, supports right-to-left direction per field, and round-trips the pilot scripts without loss through sanitization, canonicalization and rendering. | MUST |

## Exact PRD sections

- [6.7 Accessibility remediation and review · ASM04-ACC](../../prd/technical-baseline.md#67-accessibility-remediation-and-review--asm04-acc)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)
- [11. Non-functional requirements](../../prd/technical-baseline.md#11-non-functional-requirements)
- [13.3 Expert and manual verification](../../prd/technical-baseline.md#133-expert-and-manual-verification)

## Behaviour to demonstrate

Complete a review using only keyboard and screen reader. A missing accessible equation name is a recorded defect even when automated accessibility checks pass.

Failure checks: Retain manual keyboard/screen-reader findings for every required surface; automated checks alone do not close the audit.

Existing issue acceptance criteria, retained for review:

- [ ] WCAG 2.1 AA audit covers Admin editor, all review workspaces, operator/auditor content-free screens
- [ ] Findings tracked to close

## Dependencies and decisions

Required producer work: [#58](issue-58.md) (Divyansh), [#65](issue-65.md) (Divyansh), [#69](issue-69.md) (Divyansh), [#70](issue-70.md) (Divyansh), [#72](issue-72.md) (Divyansh), [#73](issue-73.md) (Divyansh), [#75](issue-75.md) (Divyansh).

R5 determines render equivalence; pilot languages/OS/assistive technologies require owner selection. Record tested coverage without claiming support for untested combinations.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
