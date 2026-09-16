# Product workflow and permissions

Design baseline: main PRD v2.0 and Detailed Spec v1.3, as identified in
[source-of-truth.md](source-of-truth.md). This document describes required
behaviour. [Delivery status](delivery-status.md) records what exists today.
Detailed numbered requirements remain in [the register](requirements.md).

## Product and boundaries

Rachana creates, reviews, translates, seals and hands off examination
questions. Layer 1 owns the controlled workflow and evidence. Layer 2 drafts
candidate questions, translation text and metadata. AI never validates,
reviews, approves, seals, determines readiness or monitors people.

The Admin uploads curriculum, defines generation parameters and requests
`required count × candidate multiplier` independent candidates. Each candidate
has its own opaque question identifier, provenance and version history. It
must pass deterministic validation before becoming a visible draft and must
pass the same human pipeline as a manually authored question. A failed
candidate is discarded before human review. The exact proposal-adoption
transition needs reconciliation with ADR-0007 (R4).

Generation parameters may specify question type, marks, language, learning
objective, competency, Bloom's level and difficulty. Curriculum-grounded
generation includes source references and stored source context; reviewers
must not receive the stored context text. Layer 2 receives no sealed content,
decision records, reviewer identities or credentials for Layer 1 stores.
Translation drafting remains disabled until the D-48 hosting and data-handling
approval is recorded. A translator can work manually while that channel is off.

Paper selection, assembly, paper export, exam delivery, marking, results and
performance calibration are outside this workflow. The Product Owner
confirmed the boundary on 14 September 2026 (R3, ADR-0015): curriculum,
generation constraints and candidate counts belong to Rachana; final paper
selection, ordering and export belong to separate assembly. The mock
exam-paper UI does not establish a change in scope.

## Roles and permitted operations

Permissions are enforced by the server on every request, together with
assignment, capability, cycle, subject, language and separation of duties.
Application placement was decided by the Product Owner on 14 September 2026
(R1): Admin authoring and unsealed-content work use the signed desktop client;
configuration and content-free oversight use the web app. No question body,
answer or Restricted source context may enter the oversight surface. A menu
is not an authorization control. The following table follows main §§5 and 15–17.

| Role | Permitted work | Required refusal |
|---|---|---|
| Admin | Upload curriculum; configure cycle and generation blueprint; generate/regenerate and manually author; edit drafts and images; view unsealed questions; withdraw unsubmitted drafts; retire approved questions; assign/reassign within eligibility rules; manage users; authorize corrections; inspect content-free audit/monitoring | No approval or rejection at any review stage; no human seal control; no sealed-plaintext read; no physical content deletion; no question-bank download, print or export |
| Question Reviewer | Read assigned immutable version and permitted metadata; comment; approve/reject with reason; complete attestations and assign difficulty under policy | No editing; no own-work approval; no unassigned question access; no forbidden assessment, author, reviewer or audit context |
| Accessibility Specialist | On assigned remediation draft, edit alt text, decorative flags, table headers/captions, equation text alternatives and reading order; comment; complete task | No approval/rejection; no changes to wording, options, key, marks, notation or image bytes |
| Accessibility Reviewer | Test completed rendering with keyboard/screen reader; record accommodation capability; comment; approve/reject with findings | No editing; no approval of own authored/remediated work or a conflicting earlier stage |
| Translator | Read authorised primary reference; edit translated text; submit an independently versioned language variant | No self-approval; no changes to locked structure, option order/key, marks, numbers, units, symbols, equations or images except through a valid recorded exception |
| Translation Reviewer | Read original and assigned translation together; check fidelity, terminology, grammar, answer equivalence and equivalent difficulty; comment; approve/reject | No editing; no review of own translation |
| Integrity Operator | View live sessions, scores, signals and referrals; act under operational policy | No question content; no discretionary action by AI |
| Auditor | Search and verify content-free audit/evidence records | No question plaintext |
| System workload identities | Deterministic validation, task creation/assignment, sealing, indexing, readiness and signed events within the service's permission boundary | No discretionary judgement; no provider mutation of workflow state; no machine-to-human plaintext shortcut |

In V1 the Admin is the author; there is no separate Question Creator role.
Holding a content-free Auditor or Integrity Operator view does not add review
approval powers. Reviewer eligibility considers prior actors across the
lineage, not just the currently selected role. See D-42, D-45 and D-46 for
source recommendations and approval status.

## Authoring and submission

The initial fully supported item is single-select MCQ: stem, 2–8 unique
options, one correct option, explanation, marks and controlled classification.
Images require scanning and meaningful alternatives. Equations use the
permitted bounded LaTeX subset. Other types require cycle enablement and
named rules (D-44); a type in a mock UI is not that enablement.

Autosave is every 15 seconds and on leaving a field. References, glossaries
and palettes stay inside the content tool. Copy/cut/paste, print, download,
export and external links are blocked/reported as specified. Device-level
leak prevention also depends on the PRD's managed-studio preconditions.

Submission checks required fields, option/key validity, taxonomy, clean
assets and alt text, permitted equations/markup and deterministic similarity.
Blocking findings name the field. Successful submission creates an immutable
version, content hash and receipt, then assigns review. A rejection creates
a linked correction draft; it never edits the returned version.

## Lifecycle and gates

States below follow main §13 and annex §§2.7 and 5. A human decision, its
evidence and the resulting state transition must commit atomically.

| Current state / event | Action and guard | Result |
|---|---|---|
| Create manual question | Eligible Admin and valid cycle/configuration | DRAFT |
| Generation response | Layer 1 validates untrusted candidate and provenance; proposal-adoption detail pending R4 | DRAFT (generated) only after applicable guards |
| DRAFT | Admin submits; all blocking validation passes | IN_QUESTION_REVIEW; immutable submitted version |
| IN_QUESTION_REVIEW | Required independent reviewer approvals, rationale and attestations complete | IN_ACCESSIBILITY |
| IN_ACCESSIBILITY | Specialist completes field-restricted remediation | IN_ACCESSIBILITY_REVIEW |
| IN_ACCESSIBILITY_REVIEW | Independent Accessibility Reviewer approves and expected evidence is complete | SEALING_REQUESTED; system sealing only |
| SEALING_REQUESTED | Worker verifies policy, actors, approvals, assets, hashes, retention and evidence; encrypts/signs/stores/indexes | SEALED for this language; safe retry on failure, never silent success |
| Primary sealed | System creates per-language drafts with locked structure and authorised read-only primary reference | IN_TRANSLATION for each required language |
| IN_TRANSLATION | Translator submits; structural checks or valid recorded exceptions pass | IN_TRANSLATION_REVIEW |
| IN_TRANSLATION_REVIEW | Independent reviewer attests fidelity and equivalent difficulty | IN_ACCESSIBILITY for that language; then its own accessibility review and seal |
| Every required language sealed on one current lineage | Readiness calculator verifies completeness | FULLY_APPROVED readiness status; metadata-only assembly access |
| Signed assembly selection / completion | Correct workload identity, valid message and idempotency checks | USED, then ARCHIVED |

FULLY_APPROVED is computed artefact readiness, not a replacement for each
language's version state. Translation never overwrites the primary. The
authorised primary reference in a translation task must not become a general
vault read endpoint; its release and lifetime require the sealed-reference
contract described in R8.

Every rejection records a reason/comment and produces a correction task.
Corrected work goes to a different reviewer. Accessibility-only findings go
to restricted remediation; wording/answer/notation/image changes return to
authoring and repeat affected gates under D-07. Annex PRD-ACC-18 also requires
a different specialist for an accessibility correction. Original decisions
and versions remain evidence.

## Review quality and isolation

Question review requires an unambiguous stem, the right key, plausible wrong
distractors, correct classification/explanation, justified images/equations,
and the three attestations: language/grammar, non-public-domain question, and
cycle guidelines/scope, with sources consulted. The required number of
independent question reviews is a cycle setting (D-06).

A reviewer receives only the assigned rendering and permitted metadata:
subject, grade, curriculum name, source chapter/page range, question type,
marks, Bloom's level, difficulty, language and validation warnings. Annex
PRD-REV-19 also names version, submission time and content hash.

Responses and discovery paths must conceal assessment identity, final question
number, other assessment questions, pool membership, selection status, other
reviewers, author identity/pseudonym, audit history and source context text.
Opaque `QB-nnnnn` identifiers must not encode assessment or final numbering.
Test the API payload and attempted access, not just hidden UI fields.

Assignment uses valid role/subject/language/capability and no duty conflict;
lowest active workload wins, then longest time since assignment. Tasks
expire and return to the pool; aging and reassignment stay visible to the
Admin. Main §15's "one reviewer per stage" must be read with the configurable
review count; the queue contract must support all required independent
reviews rather than silently hard-code one (R12).

## Sealing, correction and deletion

The system canonicalizes, hashes, encrypts and signs a manifest containing
the approvals, evidence and policy versions, stores the immutable version,
indexes safe metadata and disposes of the working copy. Missing evidence
blocks sealing. D-24 has no default retention period; production sealing is
blocked until the required period is supplied.

No routine human role can read sealed plaintext, including the Admin. The
PRD's separately governed emergency procedure is not a product button or an
implemented capability (R8). Assembly receives readiness metadata, languages
and hashes through a correctly scoped machine identity, never content from
the authoring API.

An authorised correction revokes readiness immediately and creates a new
lineage through the controlled seeding procedure (D-16). It preserves sealed
bytes, marks variants for revalidation, notifies assembly and tracks its
acknowledgement. The replacement traverses the full applicable pipeline;
supersession does not erase history. "Delete" means WITHDRAWN for an
unsubmitted draft or RETIRED for an approved question.

## Session integrity and evidence

Every content session registers and heartbeats every 30 seconds. The PRD
names copy/cut/paste, context menu, print/screenshot keys, developer tools,
focus/tab changes, concurrent tabs and heartbeat gaps. Capture/blocking
capability is bounded by the managed device; observable events never prove
that all leakage is technically impossible.

Scores start at 100, fall by a published/ratified severity table and never
recover during a session. Referral at ≤50 is the PRD's recommended threshold;
automatic suspension is off by default. Operator records contain no content.
Keep D-03, D-04 and D-22 approval status visible.

Integrity evidence must survive transport failures without silent loss.
Optional diagnostic telemetry may fail without blocking the core; it cannot
replace the durable audit/expected-evidence path. Every required action has
an append-only content-free record, and sealing asserts evidence completeness.
Verification includes tampering, missing records and restore. See annex
§§6.13–6.14 and [traceability](traceability.md) for acceptance.
