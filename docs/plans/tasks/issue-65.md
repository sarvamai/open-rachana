# #65: As a Question Reviewer, I want to see only my assigned question and the allowed metadata

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Deliver a read-only review workspace with strict payload isolation and assigned-task access.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Define an allowlisted response schema and direct-API negative tests, then render that response in the signed client.

## Inputs and outputs

- Input: Authenticated reviewer, active assignment, exact version/hash, permitted metadata and cycle key-visibility flag.
- Output: A minimal review response/rendering and locked worklist; no author, assessment, pool, other-reviewer or source-context data.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [UI-02](../../requirements.md#req-ui-02) | My Work shows assigned tasks with type, cycle, subject, language, state, age and deadline. No unassigned content is reachable. | MUST |
| [UI-03](../../requirements.md#req-ui-03) | A task becoming available is actively surfaced to the assignee; work does not sit unannounced in a queue nobody is prompted to check. | MUST |
| [ASM03-REV-02](../../requirements.md#req-asm03-rev-02) | The review workspace is read-only and shows the exact submitted version, its content hash, permitted metadata and a mandatory structured checklist. | MUST |
| [ASM03-REV-03](../../requirements.md#req-asm03-rev-03) | No review endpoint accepts content fields. Direct editing is never offered. | MUST |
| [PRD-REV-19](../../requirements.md#req-prd-rev-19) | GAP Reviewer isolation (engineering PRD §10, §20, adopted verbatim). The review workspace shows the reference rendering, the content hash, and only the metadata needed to evaluate the question: subject, grade, curriculum name, question type, marks, Bloom's level, difficulty, language, version number, submission time, the validation warnings, and the source chapter and page range for grounding checks (D-47). It never shows: assessment name, title or identifier; final question number; other questions in any assessment; candidate-pool membership or selection status; which users reviewed the question or any other reviewer; the audit history; the author's identity or pseudonym; the stored source context text. The artefact identifier QB-nnnnn is not a question number and reveals no assessment context. | MUST |
| [PRD-REV-20](../../requirements.md#req-prd-rev-20) | GAP The worklist locks to the open task until a decision is recorded, then advances to the next assigned task (UI-07). Leaving the workspace without deciding keeps the assignment active and records the duration so far. | MUST |
| [UI-06](../../requirements.md#req-ui-06) | Review — read-only version, hash, permitted metadata, mandatory checklist, rationale entry, approve and return. Correct-answer visibility per policy. | MUST |
| [UI-07](../../requirements.md#req-ui-07) | Review — the worklist locks to the open task until a decision is recorded, then advances. | MUST |
| [SEC-02](../../requirements.md#req-sec-02) | Correct-answer visibility is limited to the assigned author before submission, and to reviewers only where the ratified policy requires it. It is never exposed to coordinators, operators or administrators. | MUST |
| [SEC-03](../../requirements.md#req-sec-03) | Automated tests assert that no non-permitted role receives correct-answer or sealed-plaintext fields in any response body. | MUST |
| [ARC-01](../../requirements.md#req-arc-01) | Authorization is evaluated server-side on every request using role, assignment, version, language, lifecycle state, cycle policy, recognized capability and separation of duties. Client-supplied role claims are never trusted. | MUST |
| [PRD-REV-18](../../requirements.md#req-prd-rev-18) | GAP D-06 Correct-answer visibility in review is governed by the cycle flag reviewer_sees_key (SEC-02). Proposed default: true, because validating correctness (REV-04) requires knowing the key. When false, the reviewer is asked to identify the key and the workspace records whether it matched. | MUST |

## Exact PRD sections

- [9.1 What the reviewer sees](../../prd/main-baseline.md#91-what-the-reviewer-sees)
- [9.2 What the reviewer must not know](../../prd/main-baseline.md#92-what-the-reviewer-must-not-know)
- [16. Reviewer Isolation](../../prd/main-baseline.md#16-reviewer-isolation)
- [6.6 Question review · ASM03-REV](../../prd/technical-baseline.md#66-question-review--asm03-rev)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)

## Behaviour to demonstrate

A reviewer guessing another task ID is denied. Inspecting JSON/network traffic reveals no author pseudonym or assessment ID even when the UI never displayed it.

Failure checks: Inspect serialized API payloads and attempt forbidden IDs/fields; CSS hiding is not an isolation check.

Existing issue acceptance criteria, retained for review:

- [ ] Visible: rendered question; subject, grade, curriculum name, chapter, page range; type, marks, Bloom, difficulty, language; validation warnings
- [ ] Not visible and not inferable: assessment name/title/id, final question number, other questions, candidate pool membership, other reviewers, author identity, stored source-context text, audit history
- [ ] Question ID is not a paper number and exposes no assessment context
- [ ] API tests try the forbidden fields and fail if they appear

## Dependencies and decisions

Required producer work: [#63](issue-63.md) (Kaustav), [#67](issue-67.md) (Kaustav).

D-06 key visibility is cycle policy; R5 controls rendering and D-47 source metadata. Never send hidden forbidden fields for client filtering.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
