# #44: As an Admin, I want to configure a cycle and its taxonomy

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Build versioned cycle, taxonomy and vocabulary configuration with the content-free Admin surface.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Create/read/update a synthetic cycle and publish one taxonomy. Connect the Admin configuration screen; use expected-version checks for concurrent edits.

## Inputs and outputs

- Input: Cycle code/title/status, primary and required languages, syllabus/taxonomy versions, item types, marking reference, accommodations and policy settings.
- Output: Persisted configuration and policy_version; immutable referenced taxonomy versions; audited publication, retirement and cycle changes.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM01-CFG-01](../../requirements.md#req-asm01-cfg-01) | A coordinator can configure a cycle: code, title, primary language, required languages, syllabus version, permitted item types, marking-policy reference, declared accommodations, and status. | MUST |
| [ASM01-CFG-02](../../requirements.md#req-asm01-cfg-02) | Artefacts can be created only within an active, valid cycle. | MUST |
| [ASM01-CFG-03](../../requirements.md#req-asm01-cfg-03) | A taxonomy administrator manages versioned Subject → Unit → Topic hierarchies plus controlled difficulty and taxonomy-level vocabularies. | MUST |
| [ASM01-CFG-04](../../requirements.md#req-asm01-cfg-04) | Taxonomy values in use can be retired for future selection but never deleted. Historical versions retain their original references. | MUST |
| [ASM01-CFG-05](../../requirements.md#req-asm01-cfg-05) | Cycle and taxonomy configuration have working interfaces — nothing can be authored until both exist. | MUST |
| [PRD-CFG-06](../../requirements.md#req-prd-cfg-06) | GAP The cycle record carries, in addition to CFG-01: author cap per cycle; required review count (1 or 2) D-06; whether reviewers see the correct answer D-06; remediation-repeats-review policy D-07; assignment expiry per task type D-12; similarity threshold D-08; default marks per item from the marking policy; a monotonically increasing policy_version that increments on every change. | MUST |
| [PRD-CFG-07](../../requirements.md#req-prd-cfg-07) | GAP Cycle status is one of Draft (editable, nothing can be authored), Active (drafts may be created) and Closed (no new drafts; in-flight tasks, sealing and readiness continue). Changing required languages or syllabus version on an Active cycle requires re-authentication, increments the policy version and emits policy.changed; existing versions keep their recorded references. A cycle is never deleted. | MUST |
| [PRD-CFG-08](../../requirements.md#req-prd-cfg-08) | GAP A taxonomy version is an immutable published tree once referenced by a cycle. Node identifiers are stable across versions. Nodes carry active_from and retired_at. A new version may retire nodes; retirement is a date, never a deletion, so every historical reference resolves. | MUST |
| [PRD-CFG-09](../../requirements.md#req-prd-cfg-09) | GAP Controlled vocabularies are versioned lists managed by the taxonomy administrator: difficulty, taxonomy level, complexity level (used by bank indexing), item type, declared accommodation. Proposed initial values are in D-17 and D-18. Values are retired, never deleted. | MUST |
| [PRD-CFG-10](../../requirements.md#req-prd-cfg-10) | GAP Every decision, submission and seal records the cycle policy_version, taxonomy version and vocabulary versions in force at that moment, so the evidence pack can reproduce the rules that applied. | MUST |
| [PRD-CFG-11](../../requirements.md#req-prd-cfg-11) | GAP A cycle may have an empty list of required languages (single-language cycle). Readiness then requires only the sealed primary. | MUST |
| [UI-10](../../requirements.md#req-ui-10) | Coordinator — cycle configuration, taxonomy management, assignment, author cap status, and safe progress with artefact aging. Assignment screens reveal no artefact content. | MUST |

## Exact PRD sections

- [6. Core Concepts](../../prd/main-baseline.md#6-core-concepts)
- [6.1 Cycle, syllabus and taxonomy configuration · ASM01-CFG](../../prd/technical-baseline.md#61-cycle-syllabus-and-taxonomy-configuration--asm01-cfg)
- [8.2 Entities and required fields](../../prd/technical-baseline.md#82-entities-and-required-fields)

## Behaviour to demonstrate

A Draft cycle cannot create questions. A Closed cycle blocks new drafts but permits in-flight work. Retiring a referenced taxonomy node leaves old versions resolvable.

Failure checks: Try stale taxonomy, invalid language/policy configuration and concurrent updates; retain the exact configuration version and atomic evidence.

Existing issue acceptance criteria, retained for review:

- [ ] Admin can create/update a cycle: primary language, required languages, syllabus version, declared accommodations, review policy (1 vs 2 question reviewers)
- [ ] Admin can maintain taxonomy: subject, unit, topic, difficulty, Bloom's level — versioned with the syllabus
- [ ] Invalid taxonomy codes are rejected
- [ ] Each write appends a content-free audit event in the same transaction
- [ ] Non-Admin is 403

## Dependencies and decisions

Required producer work: [#39](issue-39.md) (Nikhil), [#42](issue-42.md) (Kaustav), [#46](issue-46.md) (Gandharva).

D-06/07/08/12/13/17/18/29 are configurable owner choices. A single-language cycle is valid; do not hard-code three languages.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
