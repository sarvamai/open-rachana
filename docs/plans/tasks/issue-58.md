# #58: As an Admin, I want to write and edit a single-select MCQ in the tool

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Build the signed-client manual authoring screen with accessible content fields, autosave and field-level validation.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Connect one synthetic draft through load/edit/autosave/stale-save UI states against the task contract.

## Inputs and outputs

- Input: Authorised draft/task from #53, taxonomy/cycle settings, asset references, validation results and draft concurrency token.
- Output: Editable MCQ fields, saved/saving/failed status, preview, findings and submit action; draft state stays in memory.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-ATH-02](../../requirements.md#req-asm03-ath-02) | The editor creates a single-select multiple-choice artefact with a stem, 2 – 8 unique non-empty options, exactly one correct option, an explanation, and all required classification and marking metadata. | MUST |
| [ASM03-ATH-03](../../requirements.md#req-asm03-ath-03) | Classification is captured against the current syllabus version and taxonomy: subject, unit, topic, difficulty and taxonomy level. | MUST |
| [ASM03-ATH-04](../../requirements.md#req-asm03-ath-04) | Content supports sanitized restricted HTML, full Unicode, sub- and superscript, lists, accessible tables, and canonical LaTeX rendered through the shared reference renderer. | MUST |
| [ASM03-ATH-05](../../requirements.md#req-asm03-ath-05) | The editor autosaves at least every 15 seconds and on field exit, and always displays saved, pending or failed status. | MUST |
| [ASM03-ATH-07](../../requirements.md#req-asm03-ath-07) | Preview uses the same rendering contract as review, accessibility check and downstream delivery. | MUST |
| [ASM03-ATH-13](../../requirements.md#req-asm03-ath-13) | Every resource an author needs is built into the authoring tool — reference material, symbol and equation palettes, and the approved glossary. The author is never required to leave the tool, and no external source is reachable from it. | MUST |
| [PRD-ATH-14](../../requirements.md#req-prd-ath-14) | GAP D-11 Proposed field limits, measured on text after markup is stripped: stem ≤ 4,000 characters; each option ≤ 1,000; explanation ≤ 6,000; alternative text 3 – 300 characters; at most 6 images per version; each image ≤ 2 MB and ≤ 4,000 × 4,000 pixels; total asset budget ≤ 8 MB per version. Limits are configuration with these defaults and are enforced server-side with field-level errors. | MUST |
| [PRD-ATH-15](../../requirements.md#req-prd-ath-15) | GAP Content model of a version: stem; ordered options, each with a structural identifier, a body and a correct flag; explanation; classification (subject, unit, topic, difficulty as proposed by the author, taxonomy level); marks; assets with checksum, alternative text and decorative flag. Stem, option bodies and explanation are restricted-HTML documents in which equations are inline equation nodes holding canonical LaTeX and images are asset references. | MUST |
| [PRD-ATH-19](../../requirements.md#req-prd-ath-19) | GAP Autosave protocol: save 2 seconds after the last change, at least every 15 seconds while dirty, and on field exit; each save sends the concurrency token and receives the next one; status shows Saved, Saving… or Failed (retrying); a stale-token rejection reloads the server copy and shows the author what differs without discarding their unsaved text. The client keeps draft state in memory only — never in persistent browser storage (ATH-10). | MUST |
| [PRD-ATH-20](../../requirements.md#req-prd-ath-20) | GAP D-20 Forced re-authentication: when the refresh window has expired, the client attempts one immediate autosave, then redirects to sign-in with the unsaved state held in memory for the same tab; on return the draft is reloaded from the server and any surviving unsaved text is offered for re-application. Loss is bounded by the autosave interval (≤ 30 s, §11). | MUST |
| [PRD-ATH-23](../../requirements.md#req-prd-ath-23) | GAP In-tool resources (ATH-13): a read-only reference-material viewer for documents loaded by Content Operations; a Unicode symbol palette organized by category; an equation palette of templates drawn only from the permitted subset; the approved glossary per language, searchable. All are served by the application from its own store; no outbound link exists anywhere in the tool. | MUST |
| [PRD-ATH-24](../../requirements.md#req-prd-ath-24) | GAP Scripts and direction: every text field accepts full Unicode, supports right-to-left direction per field, and round-trips the pilot scripts without loss through sanitization, canonicalization and rendering. | MUST |
| [UI-04](../../requirements.md#req-ui-04) | Authoring — hardened editor for stem, options, correct answer, explanation and classification, with the hardened region visually marked; live validation findings; preview; submit. | MUST |
| [UI-14](../../requirements.md#req-ui-14) | A page refresh restores equivalent state. No unsaved work is silently lost. | MUST |
| [PRD-ATH-26](../../requirements.md#req-prd-ath-26) | GAP Metadata (engineering PRD §9.2): in addition to classification, a version carries grade, curriculum reference, learning objective, competency, question type, language, source curriculum, chapter, page range and source context, status, version number, created and updated timestamps, and — where generated — generation identifier, model and configuration. Source context text is Restricted and is never shown to reviewers (D-47). | MUST |
| [INT-04](../../requirements.md#req-int-04) | Draft updates require and return an optimistic-concurrency token; stale writes are rejected. | MUST |
| [PRD-INT-14](../../requirements.md#req-prd-int-14) | GAP Content responses (draft, version, render, asset) are authorized per request with a short-lived scope and are non-cacheable (DAT-04); asset bytes are served through an authorized endpoint with a 60-second signed reference, never a stable public URL. | MUST |

## Exact PRD sections

- [8. Authoring](../../prd/main-baseline.md#8-authoring)
- [6.4 Authoring · ASM03-ATH](../../prd/technical-baseline.md#64-authoring--asm03-ath)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)

## Behaviour to demonstrate

A failed save stays visibly failed/retrying. A stale token offers a safe comparison without dropping unsaved text or writing it to localStorage.

Failure checks: Try invalid option counts, multiple correct answers, stale autosaves and failed network saves; prevent editing a submitted version and retain accessible error states.

Existing issue acceptance criteria, retained for review:

- [ ] Editor supports stem, 2–8 options, exactly one correct, explanation, marks, subject/unit/topic/difficulty/Bloom
- [ ] Other question types are rejected unless the cycle enables them (D-44)
- [ ] Reference material, glossary, symbol and equation palettes are inside the tool
- [ ] No links out of the tool
- [ ] Autosave every 15 seconds and on leaving a field

## Dependencies and decisions

Required producer work: [#53](issue-53.md) (Kaustav), [#44](issue-44.md) (Kaustav).

R5 determines canonical preview/reference equivalence; D-20 defines re-auth recovery. Use the existing Admin role while R4’s Author extension remains open.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
