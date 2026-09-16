> Retained PRD baseline for section-level reference. Current owner amendments and conflicts are in [source precedence](../source-of-truth.md) and [reconciliation](../prd-reconciliation.md). Historical dates, role names, proposed defaults and superseded clauses below are source text, not fresh approval. Use the [engineering handoff](../plans/README.md) for the applicable task and effective rules. External source links are omitted.

# Project Rachana — PRD

Main document · v2.0 · 7 September 2026 · This is the document to read. The detailed PRD v1.3 is Annexe A. Codes like D-46 point to the decision table in section 20.

## 1. Product Overview

Project Rachana is a secure platform for creating, reviewing, translating, sealing and handing off examination questions.

It has two layers.

- Layer 1 — Examination pipeline. People decide. Fixed rules check. Content is sealed.
- Layer 2 — Intelligence layer. Sarvam AI drafts candidate questions, translation drafts and metadata suggestions.

One rule joins them: AI drafts. AI never judges.

```text
Admin
↓
Upload curriculum (PDF)
↓
Define blueprint
↓
Layer 2 generates candidate questions
↓
Question Bank (drafts)
↓
Question Review → Accessibility → Translation → Translation Review → Accessibility
↓
System seals each approved version
↓
FULLY_APPROVED
↓
Assembly (separate service) reads metadata only
```

Example:

```text
Final questions required: 5
Candidate multiplier:     3×
Questions generated:      15
```

The 15 questions are independent candidates. Each one goes through the full pipeline on its own. Only FULLY_APPROVED questions can be assembled.

## 2. Problem Statement

Creating good exam questions is slow and risky. It means:

- Understanding the curriculum.
- Writing questions grounded in it.
- Getting type, marks, Bloom's level and difficulty right.
- Reviewing quality.
- Reviewing accessibility.
- Translating, and reviewing translations.
- Keeping versions and approvals straight.
- Preventing leaks during review.
- Proving afterwards that every step happened.

Rachana puts all of this in one controlled workflow.

## 3. Goals

- Generate curriculum-grounded candidate questions with AI.
- Let the Admin define blueprints.
- Generate more candidates than the final paper needs.
- Run a controlled, multi-stage review.
- Keep reviewers isolated from assessment context.
- Support accessibility validation for every language.
- Support multiple languages, each tracked on its own.
- Keep the original and every translation.
- Version every substantive change and re-review it.
- Log every action in a tamper-evident audit trail.
- Seal approved questions so nobody can read them again.
- Hand off to assembly by metadata only.
- Watch live sessions for leakage attempts.

## 4. Non-Goals

- Assembling papers or choosing which question a candidate sees.
- Registering candidates, running exam day, marking, results.
- Calibrating questions from candidate performance data.
- Multimedia questions (audio, video).
- Any AI that validates, reviews, approves, seals or monitors.

## 5. Roles

### 5.1 RBAC matrix

✓ = allowed. Empty = not allowed. There are no TBD cells.

| Capability | Admin | Question Reviewer | Accessibility Specialist | Accessibility Reviewer | Translator | Translation Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Upload curriculum | ✓ |  |  |  |  |  |
| Create blueprint, configure cycle | ✓ |  |  |  |  |  |
| Generate or regenerate questions | ✓ |  |  |  |  |  |
| Manually create a question | ✓ |  |  |  |  |  |
| Edit a draft, add images | ✓ |  |  |  |  |  |
| Withdraw a draft ("delete") | ✓ |  |  |  |  |  |
| Retire an approved question ("delete") | ✓ |  |  |  |  |  |
| View all questions (until sealed) | ✓ |  |  |  |  |  |
| View assigned question | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Comment | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Approve or reject question review |  | ✓ |  |  |  |  |
| Remediate accessibility |  |  | ✓ |  |  |  |
| Approve or reject accessibility |  |  |  | ✓ |  |  |
| Create or edit a translation |  |  |  |  | ✓ |  |
| Approve or reject a translation |  |  |  |  |  | ✓ |
| Assign or reassign reviewers | ✓ |  |  |  |  |  |
| Authorize a correction | ✓ |  |  |  |  |  |
| Manage users and roles | ✓ |  |  |  |  |  |
| View audit logs | ✓ |  |  |  |  |  |
| Seal a question | System only |  |  |  |  |  |
| Read a sealed question | Nobody |  |  |  |  |  |
| Download or export | Nobody |  |  |  |  |  |

The Admin never approves or rejects. The Admin writes the questions. See D-46.

### 5.2 Admin

The Admin runs the platform and writes every question in V1. There is no separate author role.

Can:

- Upload curriculum. Manage reference material and glossary.
- Configure the cycle: languages, syllabus version, accommodations, policies.
- Generate candidate questions. Regenerate when the pool is short.
- Create, edit, validate, preview and submit questions.
- Withdraw drafts. Retire approved questions.
- Assign, reassign and release reviewers. See workload and status.
- Approve structural-check exceptions.
- Authorize corrections to approved questions.
- Manage users and their roles.
- View audit logs and user activity. No content appears there.

Cannot:

- Approve or reject at any review stage.
- Read a sealed question.
- Download, print, copy or export content.
- Delete anything permanently.

### 5.3 Question Reviewer

Can:

- View the assigned question.
- Comment.
- Approve or reject, with a reason.

Cannot:

- Edit the question.
- Copy, download or export.
- See the assessment name, ID or question number.
- See other questions in the assessment.
- See who else reviewed the question.
- See audit logs.

### 5.4 Accessibility Specialist

Receives the question after question review.

Can:

- View the assigned question.
- Add or edit alternative text.
- Mark images as decorative.
- Add table headers and captions.
- Add text descriptions for equations.
- Fix reading order.
- Comment.
- Complete the task.

Cannot:

- Change wording, options, the answer or marks.
- Change mathematical notation.
- Replace images.
- Approve or reject.

### 5.5 Accessibility Reviewer

Validates the specialist's work.

Can:

- Test the rendered question with keyboard and screen reader.
- Record which accommodations the question works under.
- Comment.
- Approve or reject.

Cannot:

- Edit.
- Act on a question they authored, remediated or reviewed before.

### 5.6 Translator

Can:

- View the original question.
- Create and edit the translated text.
- Submit for translation review.

Cannot:

- Change structure, option order, the answer, marks, numbers, units, symbols, equations or images.
- Approve their own work.

The original question is never replaced.

### 5.7 Translation Reviewer

Can:

- View the original and the translation side by side.
- Comment.
- Approve or reject.

Cannot:

- Edit the translation.
- Review a translation they wrote.

### 5.8 Other roles

- Integrity Operator. Watches live sessions. Sees actions and scores, never content.
- Auditor. Searches the audit trail. Sees records, never content.
- System. Validates, seals, indexes, computes readiness, emits events. Never takes a discretionary decision.

The Admin may hold the Integrity Operator and Auditor screens in the pilot. Both are content-free.

## 6. Core Concepts

- Curriculum. A source PDF uploaded by the Admin. Example: NCERT Class 8 Science.
- Blueprint. What the assessment needs: question type, marks, number required, candidate multiplier, weightage, Bloom's level, difficulty, learning objective, competency, language.
- Cycle. The exam cycle configuration: primary language, required languages, syllabus version, accommodations, review policy.
- Question Bank. Every draft and version in the working store, plus every sealed question in the vault.
- Question ID. Format `QB-123456`. It never relates to a final question number.
- Version. Every change is a new version. Old versions never change.
- Assessment. The final paper. Assembled elsewhere from FULLY_APPROVED questions. Final numbers exist only there.

```text
Question Bank IDs        Final paper
QB-123456                Question 1
QB-123457                Question 2
QB-123458                Question 3
(no relationship between the two columns)
```

## 7. Question Generation (Layer 2)

```text
Admin
↓
Upload curriculum
↓
Define blueprint
↓
Specify required questions and candidate multiplier
↓
Layer 2: OCR, curriculum processing, generation
↓
Automated validation
↓
Candidates that pass become DRAFT questions in the Question Bank
```

Every generated question carries:

- Question ID, type, marks, subject, grade, curriculum.
- Bloom's level, difficulty, learning objective, competency, language.
- Source curriculum, chapter, page range, source context (stored, never shown to reviewers).
- Generation ID, model, configuration, timestamp.
- Status, version, created and updated timestamps.

Rules:

- Questions are grounded in the uploaded curriculum only.
- Generated questions are independent. They are never grouped as alternatives.
- A candidate that fails automated validation is discarded. No human sees it.
- A generated draft is treated exactly like a hand-written draft from that point on.
- Layer 2 never receives sealed content and cannot write into the pipeline.
- Translation drafts need the original text. That channel stays off until Security approves where the model runs. See D-48.

## 8. Authoring

### 8.1 Question format (V1)

- Single-select multiple choice.
- Stem, 2 to 8 options, exactly one correct option, explanation.
- Classification: subject, unit, topic, difficulty, Bloom's level.
- Marks.
- Images allowed. Every meaningful image needs alternative text.
- Equations in a limited LaTeX subset.

Other question types enter only when a cycle enables them. See D-44.

### 8.2 Editor rules

- Autosave every 15 seconds and on leaving a field.
- Reference material, glossary, symbol and equation palettes are inside the tool.
- No links out. No copy, cut, paste, print, download or export.
- Every blocked action is recorded and shown on the operator screen.

### 8.3 Validation before submit

- Required fields present.
- 2 to 8 unique options. Exactly one correct.
- Classification values exist in the current syllabus.
- Images scanned clean. Alternative text present.
- Equations inside the permitted subset.
- No prohibited markup.
- Not too similar to any sealed question in the bank.

Blocking findings stop submission. Each names the field.

### 8.4 Submit

```text
Submit
↓
Immutable version + content hash
↓
Receipt to the author
↓
Reviewer assigned automatically
```

Editing after submit is not possible. A rejection creates a new draft.

## 9. Question Review

### 9.1 What the reviewer sees

- The rendered question.
- Subject, grade, curriculum name, chapter and page range.
- Question type, marks, Bloom's level, difficulty, language.
- Validation warnings.

### 9.2 What the reviewer must not know

- Assessment name, title or ID.
- Final question number.
- Other questions in the assessment.
- Candidate pool membership. Which questions were selected.
- Which users reviewed the question.
- The author's identity.
- The stored source context text.

### 9.3 Actions

- Read.
- Comment.
- Approve.
- Reject.

The reviewer cannot edit.

### 9.4 Checklist

Approval needs every item.

- Stem is unambiguous.
- Exactly one option is correct, and it is the marked one.
- Distractors are plausible and wrong.
- Classification matches the syllabus.
- Explanation is correct.
- Images and equations are right and needed.
- Attestation 1: language and grammar are correct. Source consulted.
- Attestation 2: the question is not in the public domain. Source consulted.
- Attestation 3: the question follows the cycle guidelines and scope. Source consulted.
- Difficulty assigned from the controlled list.

### 9.5 Approval

```text
Question Review approved
↓
Accessibility
```

Whether one or two reviewers are needed is a cycle setting.

### 9.6 Rejection

```text
Question Reviewer
↓
Rejection + reason + comment
↓
Admin corrects (new draft)
↓
New Question Reviewer assigned
↓
Question Review
```

The corrected question always goes to a different reviewer.

## 10. Accessibility

Two roles. The specialist works. The reviewer decides.

```text
Question Review approved
↓
Accessibility Specialist remediates (accessibility fields only)
↓
Specialist completes
↓
Accessibility Reviewer tests and decides
↓
Approve → Sealing        Reject → correction
```

The reviewer checks:

- Screen reader reads everything correctly.
- Alternative text is right. Decorative images are marked.
- Colour contrast and font readability.
- Plain language.
- Reading order, focus, keyboard operation.
- Tables and equations are navigable.
- The question does not rely on sight or hearing alone.
- Which declared accommodations the question works under.

If a finding needs a wording change, the question goes back to the Admin as a rejection. The specialist never edits wording.

```text
Accessibility Reviewer
↓
Rejection + finding (element + fix)
↓
Accessibility Specialist corrects   or   Admin corrects
↓
New Accessibility Reviewer assigned
↓
Accessibility Review
```

Accessibility applies to the original and to every translation. See D-43.

## 11. Translation

Translation starts after the original is sealed.

```text
Original sealed
↓
Translator (one per language)
↓
Translated question
↓
Translation Reviewer
↓
Accessibility (for that language)
↓
Sealed
```

Each language has its own:

- Translation.
- Translator.
- Version.
- Review status.
- Reviewer.
- Comments.
- Approval history.

```text
Original (English)
├── Hindi
│    └── Hindi review → Hindi accessibility → sealed
├── Kannada
│    └── Kannada review → Kannada accessibility → sealed
└── Tamil
└── Tamil review → Tamil accessibility → sealed
```

The translator edits text only. Locked and checked by machine on submit:

- Number and order of options.
- Which option is correct.
- Marks.
- Every number, unit and symbol.
- Every equation.
- Every image.

A failed check blocks submission and names the check. Only a recorded exception, approved by the Admin with an expiry date, can override it.

The Translation Reviewer checks fidelity, terminology, grammar and answer equivalence, and confirms the translation is not easier and not harder than the original.

```text
Translation Reviewer
↓
Rejection + comment
↓
Translator corrects
↓
New Translation Reviewer assigned
```

The original never changes.

## 12. Sealing and the Vault

Sealing is done by the system. No person has a seal or publish button.

When: after accessibility approval of a language version.

The system:

- Re-checks every approval and every expected record.
- Canonicalizes the content and computes a SHA-256 hash.
- Encrypts the content with managed keys.
- Signs a manifest listing hashes, approvals and policy versions.
- Stores the sealed version in the vault.
- Indexes metadata: classification, difficulty, Bloom's level, marks.
- Deletes the working copy and writes the audit record.

If anything is missing, sealing stops and raises an alert.

After sealing:

- Nobody can read the question. Not the Admin, not an administrator.
- The Admin sees metadata only.
- Sealing the original creates the translation drafts.

FULLY_APPROVED = the original and every required language are sealed.

Assembly reads readiness records over a machine identity:

- Question ID, type, classification, difficulty, Bloom's level, marks.
- Languages and sealed version hashes.
- Readiness status.

Never content.

Later states, driven by signed messages from assembly:

- USED. Selected for an exam session.
- ARCHIVED. The exam session is complete. Keys rotate to the archive tier.

## 13. Question Lifecycle

```text
DRAFT  (generated or manual)
↓
IN_QUESTION_REVIEW
├── REJECTED → correction draft → new reviewer → IN_QUESTION_REVIEW
└── APPROVED
↓
IN_ACCESSIBILITY  (specialist)
↓
IN_ACCESSIBILITY_REVIEW
├── REJECTED → correction → new reviewer → IN_ACCESSIBILITY_REVIEW
└── APPROVED
↓
SEALED  (original)
↓
IN_TRANSLATION  (one per language)
↓
IN_TRANSLATION_REVIEW
├── REJECTED → correction → new reviewer → IN_TRANSLATION_REVIEW
└── APPROVED
↓
IN_ACCESSIBILITY → IN_ACCESSIBILITY_REVIEW  (that language)
↓
SEALED  (that language)

All required languages SEALED  →  FULLY_APPROVED
FULLY_APPROVED  →  USED  →  ARCHIVED
```

Other states: WITHDRAWN (draft withdrawn), RETIRED (approved question retired), SUPERSEDED (replaced by a correction).

## 14. Versioning and Corrections

Every question is versioned.

```text
QB-12345
v1  └── AI generated
v2  └── Admin edited
v3  └── Admin edited again
```

Every version keeps:

- Previous content.
- New content.
- Editor.
- Timestamp.
- Reason or comment.
- Review status.

Old versions never change. Rejected versions stay as evidence.

Approval reset:

```text
FULLY_APPROVED
↓
Admin authorizes a correction (reason recorded)
↓
Readiness revoked immediately
↓
New draft in a new lineage
↓
Question Review → Accessibility → Translation → Translation Review → Accessibility
↓
FULLY_APPROVED
```

- The sealed version is never overwritten. It becomes SUPERSEDED.
- Every translation is marked for re-validation. Translators see what changed.
- Assembly is notified and must acknowledge.
- "Delete" means withdraw (a draft) or retire (an approved question). Nothing is deleted.

## 15. Reviewer Assignment

Assignment is automated. One reviewer per question per stage.

```text
100 questions

Reviewer A → 34
Reviewer B → 33
Reviewer C → 33
```

Algorithm:

- Eligible: right role, subject, language, a valid registry entry, no conflict of duty.
- Lowest active workload first.
- Tie-break: longest time since last assignment.

Rules:

- A corrected question goes to a different reviewer.
- A reviewer never gets a question they authored, translated or reviewed at another stage.
- A task nobody answers expires and returns to the pool. The Admin sees aging.
- The Admin can reassign, within the same rules.

## 16. Reviewer Isolation

A reviewer has access only to questions assigned to them.

They must not be able to discover or infer:

- Assessment identity.
- Question number.
- Other assessment questions.
- Candidate pool membership.
- Question selection.
- Other reviewers.
- Audit history.
- The stored source context.

The Question ID is not a question number and exposes no assessment context.

## 17. Security

- Sign-in through the organisation's identity provider only. No local passwords.
- Multi-factor authentication for every role.
- Content screens open only from managed devices in approved locations.
- Sessions time out. Sensitive actions ask for re-authentication.
- Authorization is checked on the server for every request. Screen restrictions are not the control.
- The person who writes never approves. Enforced in the API, even for hand-crafted calls.
- No download, print, copy or export from the question bank. Paper export belongs to the assembly module.
- Sealed content is encrypted. No plaintext copy exists for anyone.
- Emergency access to sealed content needs two named approvers and is logged.
- Uploaded images are quarantined, scanned and re-encoded before use.
- Content never appears in logs, monitoring, notifications, error messages or support tickets.

## 18. Session Monitoring

Every content session is registered and heartbeats every 30 seconds.

The client captures and blocks where possible:

- Copy, cut, paste, context menu.
- Print, screenshot key combinations.
- Developer tools opened.
- Focus loss, tab switching, concurrent tabs.
- Heartbeat gaps.

Scoring:

- Each session starts at 100.
- Each signal subtracts a fixed amount from a published table.
- The score never recovers within a session.
- At 50 or below, the session is referred: alert to the operator and a security event.
- Automatic suspension is off by default.

The operator screen shows all live sessions, scores and events. It never shows content.

## 19. Evidence and Audit

- Every action writes an audit record: who, what, which version, hash, outcome, time.
- Records are hash-chained. Removing or altering one is detectable.
- Verification runs on demand and daily.
- Each step declares the records it must produce. Sealing checks they all exist.
- Missing evidence is an alert, never a silent pass.
- Audit records contain no question content.
- The audit survives backup and restore with hashes intact.

## 20. Decisions

Decided:

| Decision | Outcome |
| --- | --- |
| D-38 AI in the product | Yes. Layer 2 drafts questions, translations and metadata. AI never judges. |
| Block codes | National Examination Stack codes (ASM, INS, CND, RES, ASR). |
| Project name | Project Rachana. |

Open. Each has a recommendation that stands until the owner decides.

| Decision | Recommendation | Owner | When |
| --- | --- | --- | --- |
| D-46 Admin approve and reject | Remove. The Admin writes the questions. | Product Owner | Now |
| D-39 Download and export | None from the question bank. Paper export is an assembly function. | Product Owner, Security | Week 1 |
| D-41 Delete | Withdraw a draft. Retire an approved question. Nothing is deleted. | Product Owner | Week 1 |
| D-42 Admin views all questions | Yes until sealed, because the Admin writes them. Metadata only after sealing. | Security | Week 1 |
| D-40 Assembly inside the product | Separate module. Selects by metadata only. | Product Owner, Technical Lead | Week 2 |
| D-44 Question types beyond MCQ | MCQ only unless a cycle enables more. | Assessment owner | Week 2 |
| D-48 Where the AI runs for translation drafts | Inside our boundary, no retention, no training. Until then, that channel is off. | Security, Technical Lead | Week 2 |
| D-43 Accessibility for every language | Keep. Dropping it must be a recorded choice. | Accessibility lead | Week 3 |
| D-24 Retention period for sealed questions | Legal supplies it. The system will not seal to production without it. | Content Operations, Legal | Week 4 |
| D-29 Pilot languages and named people | Primary plus two languages. Named authors, reviewers, accessibility professional, translators. | Content Operations | Week 0 |

The full list of 48 decisions is in Annexe A, section 15.

## 21. Scope

In:

- Authoring, question review, accessibility, translation, translation review.
- Sealing and the vault.
- Audit trail and expected evidence.
- Session monitoring.
- Layer 2 drafting.
- Readiness handoff to assembly.

At the boundary:

- Cycle and syllabus configuration.
- Reviewer registry.
- Corrections after approval.
- USED and ARCHIVED states.

Out:

- Blueprint logic and paper assembly.
- Exam-day delivery, marking, results.
- Calibration from candidate data.
- Multimedia questions.

## 22. Timeline

Five build weeks and a three-day closeout. A week closes on evidence, not a demo.

| Week | Done when |
| --- | --- |
| 0 | Team named. Pilot languages chosen. Assembly team engaged. Test tenants reachable. |
| 1 | Pipeline deploys itself. Sign-in works. The audit chain detects a tampered record. A monitoring signal reaches the audit in seconds, with no content. |
| 2 | An author writes and submits unassisted. A copy attempt is blocked and visible to the operator. A near-duplicate is refused. |
| 3 | Both review gates work with real reviewers. Self-approval fails even through a direct API call. Deleting evidence blocks the next step. |
| 4 | A question reaches FULLY_APPROVED in three languages. Nobody can read it. Assembly gets metadata only. |
| 5 | Installed in production. Penetration test and accessibility audit closed. Load, restore and verification passed. |
| Closeout | Every acceptance criterion signed in one evidence pack. Go-live decision recorded. |

Team: twelve people at peak in weeks 3 and 4. Named content people with reserved time: two authors, two reviewers, one accessibility professional, two translators, one coordinator, one operator.

## 23. Open Questions

- After a rejection, can the original author still read the rejected version, or only the findings? Default: only the findings.
- May the original author write the correction of their own approved question? Default: yes.
- Does a closed cycle ever reopen? Default: no.
- Should "needs equivalent route" for an accommodation block readiness? Default: no, it is flagged.
- Which consumers besides assembly must acknowledge a correction? Default: assembly only.
- Is a reviewer's difficulty change a rejection reason or an override at approval? Default: override, both values recorded.

## 24. Annexes

- Annexe A. Project Rachana — Detailed PRD v1.3. Every requirement, contract, data rule, screen, test, plan and decision. Use its contents page. Nobody needs to read it end to end.
- Annexe B. Content Creation MVP Requirements Specification v4. The source specification with 178 numbered requirements.
- Annexe C. Open Mulyankan — PRD. Engineering's original document, now merged into this one.
- Annexe D. Project Rachana — the 4-page memo. For readers who need only the shape.
