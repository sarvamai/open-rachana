# #53: As an Admin, I want to create a DRAFT and receive a receipt

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Create and autosave manual drafts under the active cycle, with author cap enforcement and server receipts.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement create, fetch and stale-write refusal for one synthetic single-select MCQ before adding AI-generated input.

## Inputs and outputs

- Input: Authorised Admin, cycle/taxonomy versions, content model, idempotency key on create and expected concurrency token on update.
- Output: Independent artefact/version identifiers, saved draft and next token, safe receipt and required atomic audit/outbox evidence.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-ATH-01](../../requirements.md#req-asm03-ath-01) | An author sees only draft questions and the minimum metadata needed to act. There is no browsable artefact repository. | MUST |
| [ASM03-ATH-06](../../requirements.md#req-asm03-ath-06) | Draft writes require an optimistic-concurrency token. A stale write is rejected and never overwrites newer content. | MUST |
| [ASM03-ATH-12](../../requirements.md#req-asm03-ath-12) | A per-author artefact cap is configurable per cycle. Reaching the cap blocks new creation and is visible to the coordinator. | MUST |
| [PRD-ATH-22](../../requirements.md#req-prd-ath-22) | GAP Author cap counting: drafts plus submitted versions authored in the cycle, excluding Withdrawn versions and excluding successor drafts created by a return. Reaching the cap returns AUTHOR_CAP_REACHED on create; the coordinator sees per-author counts against the cap. | MUST |
| [INT-04](../../requirements.md#req-int-04) | Draft updates require and return an optimistic-concurrency token; stale writes are rejected. | MUST |
| [PRD-ATH-15](../../requirements.md#req-prd-ath-15) | GAP Content model of a version: stem; ordered options, each with a structural identifier, a body and a correct flag; explanation; classification (subject, unit, topic, difficulty as proposed by the author, taxonomy level); marks; assets with checksum, alternative text and decorative flag. Stem, option bodies and explanation are restricted-HTML documents in which equations are inline equation nodes holding canonical LaTeX and images are asset references. | MUST |
| [PRD-ATH-26](../../requirements.md#req-prd-ath-26) | GAP Metadata (engineering PRD §9.2): in addition to classification, a version carries grade, curriculum reference, learning objective, competency, question type, language, source curriculum, chapter, page range and source context, status, version number, created and updated timestamps, and — where generated — generation identifier, model and configuration. Source context text is Restricted and is never shown to reviewers (D-47). | MUST |
| [ASM01-CFG-02](../../requirements.md#req-asm01-cfg-02) | Artefacts can be created only within an active, valid cycle. | MUST |
| [INT-03](../../requirements.md#req-int-03) | Retryable mutations accept an idempotency key and are safe to repeat. | MUST |

## Exact PRD sections

- [8. Authoring](../../prd/main-baseline.md#8-authoring)
- [6.4 Authoring · ASM03-ATH](../../prd/technical-baseline.md#64-authoring--asm03-ath)
- [7.1 Mandatory interface behaviours](../../prd/technical-baseline.md#71-mandatory-interface-behaviours)
- [8.2 Entities and required fields](../../prd/technical-baseline.md#82-entities-and-required-fields)

## Behaviour to demonstrate

Repeat a create with the same idempotency key: one draft exists. Two editors save from the same token: the second cannot silently overwrite the first.

Failure checks: Try anonymous, wrong-role and duplicate/concurrent create requests. Return only the permitted receipt and prove state/audit atomicity.

Existing issue acceptance criteria, retained for review:

- [ ] Authenticated Admin POSTs a minimal DRAFT (stub stem/options — not the editor)
- [ ] Response is a receipt: question id, version, content hash, timestamp
- [ ] State change + audit event commit together
- [ ] Non-Admin 403, unauthenticated 401
- [ ] No download/export path returns the body
- [ ] Traceability row lands in `docs/traceability.md`

## Dependencies and decisions

Required producer work: [#42](issue-42.md) (Kaustav), [#44](issue-44.md) (Kaustav), [#45](issue-45.md) (Kaustav), [#46](issue-46.md) (Gandharva).

R4 blocks a separate Author role and AI adoption transition only. D-13 cap and D-11 limits are configurable; existing Admin manual authoring can be specified now.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
