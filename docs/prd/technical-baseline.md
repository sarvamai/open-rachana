> Retained PRD baseline for section-level reference. Current owner amendments and conflicts are in [source precedence](../source-of-truth.md) and [reconciliation](../prd-reconciliation.md). Historical dates, role names, proposed defaults and superseded clauses below are source text, not fresh approval. Use the [engineering handoff](../plans/README.md) for the applicable task and effective rules. External source links are omitted.

National Examination Stack · Assessment group · Project Rachana Project Rachana — Content Creation MVP Product Requirements Document 

The part of the stack that turns a blank page into an approved, sealed, exam-ready question — and the evidence that proves it happened properly.

| Document | PRD v1.3 · 7 September 2026 · Draft for engineering review |
| --- | --- |
| Change log | v1.3 — project named Project Rachana; §1.5 two-layer architecture figure added; D-38 decided (AI drafting in scope as Layer 2); D-48 added. v1.2 — converged with the engineering PRD (Open Mulyankan — PRD): its role and state names are now canonical, the two-role accessibility flow, the different-reviewer-after-rejection rule, the reviewer-isolation list and versioning semantics are adopted, its open questions are answered (§2.7), and its conflicts with the specification are recorded as decisions D-38 – D-47. v1.1 — block names and codes updated to the National Examination Stack building-block map (six groups, 34 blocks); requirement identifiers re-prefixed accordingly; framework principles from §4.3 of the stack referenced. v1.0 — first complete draft. |
| Derived from | Content Creation MVP Requirements Specification v4 (August 2026), 37 pages, 178 numbered requirements; the National Examination Stack building-block map (Figure 6); the engineering PRD, Open Mulyankan — PRD (20 pages) |
| Audience | The delivery team: Technical Lead, backend and frontend engineers, DevSecOps, QA, Product Designer, Accessibility Specialist, Security Engineer, Technical Writer |
| Owner | Product Owner / Business Analyst (name to be entered at Week 0) |
| Approvers | Technical Lead, QA Lead, Security Engineer, Accessibility Specialist, Content Operations lead |
| Handling | Contains no examination content. May be shared with the delivery team and named content-operations staff. |

| How to read this document Specification requirements are carried with their wording. Every requirement of the form BLOCK-GROUP-nn (for example ASM03-ATH-02) comes from the specification v4 with its original wording kept as close as clarity allows. The leading segment is the building-block code of the National Examination Stack map (six groups, 34 blocks); the specification v4 used the earlier framework codes (QST03-ATH-02 for the same requirement), and Appendix A maps every group to its v4 code so the v4 document stays traceable. IDs prefixed PRD- are new. They close gaps the specification explicitly leaves to the team ("detailed schemas are produced by the team", "endpoint-level detail is owned by the interface definition", "the ratified severity table", "the canonicalization rule", and so on). Each is either a derived requirement — a necessary consequence of a specification requirement — or a proposed default that must be ratified. Proposed defaults carry a decision tag D-nn pointing into the decision register in §15. Priorities follow the specification: MUST is required for MVP acceptance; SHOULD is expected unless capacity forces a documented drop; MAY is optional. The tag GAP marks a row added by this PRD. What this document is not. It contains no visual design and no technology selection. §9 says what each screen must do; §10 says what any chosen stack must satisfy; §15 lists the decisions the team ratifies in Week 1. |
| --- |

## Contents

- Summary — what we are building and why 
- Scope — where the MVP starts and where it ends; convergence with the engineering PRD (2.7) 
- Goals, success measures and release gates 
- Users, roles and the permission matrix 
- Domain model and artefact lifecycle 
- Functional requirements (6.1 – 6.15) 
- Interface requirements and API contract 
- Data requirements, canonicalization and manifests 
- Screens 
- Architecture and security constraints 
- Non-functional requirements 
- Edge cases and required behaviour 
- Test and verification strategy 
- Delivery plan — start line to finish line 
- Decision register 
- Preconditions, dependencies, risks and open questions 
- Definition of Done and release criteria 
- Appendix A — Traceability · Appendix B — Glossary · Appendix C — Sample payloads 

# 1. Summary

## 1.1 What we are building

The National Examination Stack describes an examination as thirty-four building blocks across six groups. This MVP — the content-creation pipeline of the Project Rachana product — builds the part of the Assessment group that turns a blank page (or a generated candidate, see §2.7) into an approved question, plus the blocks from Institutions, Candidate Experience and Assurance that the work depends on.

Four jobs happen in order. A different person performs each one, and none can be skipped.

| Job 1AuthoringA subject expert writes the stem, the options, the correct answer, the explanation and the classification. | → | Job 2ReviewA second expert checks that it is correct, clear and fair, then approves it or returns it with findings. | → | Job 3Accessibility checkA specialist confirms every candidate can read and answer it, and records which accommodations it can be delivered under. | → | Job 4TranslationEach required language repeats jobs 1 – 3 on a variant that must be neither easier nor harder than the original. |
| --- | --- | --- | --- | --- | --- | --- |

When all four jobs are complete for the primary language and for every required language, the system seals the question into the repository and reports that it is ready. Nobody presses publish. From that moment nobody can read the question again through any routine interface.

## 1.2 The problem this solves

- Confidentiality. A leaked question invalidates an examination. Content must never leave the hardened environment, never appear in logs, telemetry or error messages, and must become unreadable to humans once sealed. 
- Independence. The person who writes a question is never the person who approves it. The API enforces this on its own, so bypassing the interface changes nothing. 
- Provable evidence. Every step must produce agreed evidence. Missing evidence blocks sealing and raises an alert. Silence is never treated as success. 
- Equivalence. Every language version and every accessible route must be as hard as the original — not harder, not easier. 
- Human judgement only. Every judgement about a question is made by a qualified person or by a published, fixed rule. The intelligence layer (§1.5) drafts candidates and translations; it never validates, reviews, approves, seals or monitors. 

## 1.3 Principles that settle arguments

When two implementation options are both plausible, these principles decide. They are restated from the specification and apply to every section that follows.

| Principle | Meaning for the engineer |
| --- | --- |
| P1 · Server-side authority | Authorization and lifecycle transitions are evaluated on the server on every request. Interface restrictions are convenience, never control. Client-supplied role claims are ignored. |
| P2 · Fail closed | If audit, key management, scanning or the object store is unavailable, the critical transition does not happen. No partial state, no silent fallback. |
| P3 · Immutable once submitted | Submitted, returned and sealed versions never change. A return creates a new linked draft; the returned version remains as evidence. No delete operation exists for content. |
| P4 · The system seals | Sealing is a system action under its own workload identity. No human role has a publish or seal control. |
| P5 · Evidence before transition | Each step declares the records it must produce. Sealing asserts they exist, are bound to the exact version hash and were produced by an actor without a duty conflict. |
| P6 · No content in the side channels | Telemetry, audit, monitoring, notifications, logs, traces, URLs, error messages and support tooling never carry stem, option, answer, explanation, asset bytes or clipboard payloads. This is enforced by build-failing tests. |
| P7 · Configuration over code | Review count, remediation policy, thresholds, expiry periods, retention periods and accommodation vocabularies are configuration with recorded policy versions, never constants. |
| P8 · Deterministic rules only | Validation, similarity, structural equivalence and scoring are rule-based and reproducible. No probabilistic or external inference service is called inside Layer 1; Layer 2 only ever supplies drafts (§1.5). |

#### Stack principles that also bind this MVP

The National Examination Stack's architectural principles (stack document §4.3) apply to every block and interface. Two are load-bearing here. Federated ownership: each record has one authorised writer that no other authority or supplier can bypass — which is why only the sealing worker writes sealed artefacts and manifests, and only the assembly service's signed notifications move an artefact to Used. Authoritative registries: a registry is the authoritative record of an entity, its recognised attributes and current status; repositories store documents, transaction records capture actions, and audit ledgers preserve evidence — and these stay distinguishable even when operated together. In this MVP the capability registry (INS-04) is the registry, the sealed store is the repository, decisions and assignments are the transaction records, and the hash chain is the ledger.

## 1.4 Timeline and team in one line

Five build weeks and a three-day closeout, with a peak of twelve people in Weeks 3 and 4 and no float. The week-by-week plan, closure evidence and staffing are in §14.

## 1.5 Two-layer architecture at a glance

Project Rachana is two layers joined by one governed connector. Layer 1 is the examination pipeline: the National Examination Stack blocks in this PRD, where every judgement is made by a qualified person or a fixed rule and where content is sealed. Layer 2 is the intelligence layer: the AI services (Sarvam) that draft candidates, translation first drafts and metadata suggestions. Layer 1 calls Layer 2; Layer 2 never calls into Layer 1, never writes to the vault, and never decides anything. The MVP and the demo show both layers (D-38, decided).

| Layer 2 · Intelligence layerAI drafts, never judges · outside the hardened zones · every output is a proposal |  |  |  |  |
| --- | --- | --- | --- | --- |
| L2-1Curriculum ingestionOCR and structuring of the uploaded curriculum (for example an NCERT textbook) | L2-2Question generationCandidate questions per cycle and blueprint parameters: required count × candidate multiplier | L2-3Translation draftsFirst-pass target-language text for the translator to edit (D-48) | L2-4Metadata suggestionProposed question type, marks, Bloom's level, difficulty, learning objective, source reference | L2-5Grounding pre-checkSource traceability and completeness screen before a candidate is offered to Layer 1 |

| The connector · one governed interface, Layer 1 → Layer 2Layer 1 sends: curriculum reference, cycle and blueprint parameters, target language, and — for translation drafts only — the primary reference text under D-48. Layer 2 returns: candidate drafts, translation drafts and suggested metadata, each stamped with generation identifier, model, configuration, source chapter and page, and timestamp. Never crosses: sealed content, decisions, audit records, reviewer identities, the vault, or any write to the workflow. Every response lands as a DRAFT or IN_TRANSLATION version with provenance generated and passes the same validation and human gates as hand-written work. |
| --- |

| Layer 1 · Examination pipeline (National Examination Stack)Hardened zones · human judgement and deterministic rules only · content is sealed and never leaves |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| ASM-03AuthoringAdmin writes or accepts a generated draft; validation; submission | ASM-03Question reviewIndependent reviewer; attestations; approve or reject | CND-02 · ASM-04AccessibilitySpecialist remediates; Accessibility Reviewer decides | ASM-04Translation and reviewPer-language variants; structural equivalence; equivalence judgement | ASM-05SealingSystem seals: canonicalize, encrypt, sign, index | ASM-05 · ASM-07Vault and readinessImmutable repository; FULLY_APPROVED metadata for assembly |
| INS-04Identity, MFA, device posture, capability registry, separation of duties | ASR-01Expected evidence and the hash-chained audit | ASR-02Session integrity monitoring and referral | ASR-04Recorded exceptions with expiry |  |  |
| DownstreamAssembly and release custody (ASM-07, DAY-01) read readiness metadata over mutual TLS and drive Used and Archived; enterprise services (identity provider, key management, monitoring, malware scanning) are reached only through the egress allowlist. |  |  |  |  |  |

Figure 1. Layer 2 sits outside the hardened zones; the connector is the only path between the layers, and it carries proposals downward and parameters upward. Everything in Layer 1 is specified in §4 – §10.

# 2. Scope — where the MVP starts and where it ends

## 2.1 Building blocks covered in full

These five blocks are implemented completely within this MVP. Every requirement in the corresponding sections is in scope.

| Block | What "in full" means here | Sections |
| --- | --- | --- |
| ASM-03 Authoring and review | Hardened authoring editor, deterministic validation, immutable submission, policy-driven review assignment, read-only review workspace, append-only decisions, return lineage. | §6.3 – §6.6 |
| ASM-04 Language and variants | Accessibility gate on the reference rendering, accommodation-capability record, translation tasks, structural locks, machine-verified equivalence checks, reviewer equivalence judgement. | §6.7 – §6.8 |
| ASM-05 Repository or vault | Sealing worker, canonicalization, encryption with managed keys, signed manifests, immutable encrypted storage, bank index, current-version resolution, end of routine human access. | §6.9, §8 |
| ASR-01 Expected evidence and audit | Hash-chained append-only audit, expected-evidence model per step, blocking completeness assertion, on-demand verification, verification after backup and restore, evidence view. | §6.13 |
| ASR-02 Monitoring and referral | Session registration and heartbeat, client signal capture and blocking, integrity scoring, threshold referral, live operator surface with reconnection, content-free telemetry enforced by test. | §6.14 |

## 2.2 Building blocks covered at the boundary

For each of these blocks the MVP owns one clearly bounded portion. The rest is managed elsewhere and reaches the MVP as configuration, as a machine interface, or not at all. The engineer builds exactly the "This MVP owns" column and nothing from the "Lives elsewhere" column.

| Block | This MVP owns | Lives elsewhere | Boundary contract |
| --- | --- | --- | --- |
| ASM-01 Construct and syllabus | Cycle configuration and a versioned Subject → Unit → Topic taxonomy with controlled vocabularies, consumed as configuration (§6.1). | The construct itself, syllabus authorship, the validity argument. | Coordinator and Taxonomy Administrator screens; versioned policy snapshots recorded on every decision and seal. |
| ASM-06 Calibration and lifecycle | The Used and Archived states inside the question bank, driven by signed notifications from the assembly service; archive key rotation (§6.12). | Calibration and statistical equating, which need candidate performance data that does not exist before an exam. The discrimination field is created and left empty. | Two inbound signed machine calls: selection notification and exam completion. |
| ASM-07 Assembly and equivalence | Readiness computation and a machine-only, metadata-only readiness interface (§6.10). | Blind assembly, selection, paper packaging — a separate service. | Outbound read over mutual TLS with an audience-restricted workload token. No content ever crosses. |
| INS-04 Trust and capability registries | The authoring-workforce capability registry: who is recognized to do what, in which subjects and languages, for how long; assignment eligibility; separation of duties (§6.2). | Enterprise identity, multi-factor policy, device management, institutional registries. | Enterprise identity provider tokens in; device certificate and posture proof in; audit pseudonyms out. |
| CND-02 Accessibility and accommodations | Question-level accessibility check, the accommodation-capability record per artefact, the equivalent-route flag and its escalation (§6.7). | Candidate-level accommodation decisions; generation of alternate-format artefacts (the data model must not preclude it). | Cycle declares its accommodations; readiness exposes what each artefact can be delivered under. |
| RES-06 Correction and reconciliation | Authorized correction of a sealed artefact, new lineage, immediate readiness revocation, variant revalidation, supersession notification and acknowledgement tracking (§6.11). | Reconciliation of papers, sessions or results that already used the superseded version. | Outbound supersession event; inbound acknowledgement; alert when unacknowledged past the window. |
| ASR-04 Conformance and exceptions | Recorded exceptions with justification, approver and expiry that permit a blocked structural check to be overridden (§6.8). | Programme-level conformance reporting and status. | Exception records are referenced from decisions and manifests and expire on schedule. |

## 2.3 Not covered in this MVP

| Excluded | Why | What the engineer must still do about it |
| --- | --- | --- |
| ASM-02 Blueprint and validity | The blueprint drives assembly, not authoring. | Build no coverage counts or "items per topic" targets. Expose classification, difficulty and taxonomy level on the readiness record so assembly can apply the blueprint. |
| AI as a judge (AI drafting is in scope — see §1.5 and D-38, decided) | Layer 1 remains free of AI by ARC-12 as re-worded under D-38; the intelligence layer is confined to drafting. | No model-based similarity, validation, auto-approval, accessibility judgement, monitoring or sealing. Generated candidates, translation drafts and metadata suggestions arrive through the connector as proposals and pass every human gate. Reject any Layer 1 dependency that embeds a model. |
| Multimedia items — audio, video, captions, transcripts, audio descriptions | They mean new item types, storage, sanitization, accessibility rules and a new test corpus. | The only item type is single-select multiple choice with text, images and equations. Keep item type, asset type and rendition format as data, not code, so nothing precludes adding them later (ASM04-ACC-09). |
| Designs and technical specifications | Separate deliverables of the Product Designer and the Technical Lead. | Use §9 for what each screen must do, §10 for constraints the stack must satisfy, §8 for the entities and rules the schema must express, and §15 for the decisions to ratify. |
| Blind assembly, master exam blueprint, paper packaging | Performed by a separate service. | Provide the readiness interface and accept the two lifecycle notifications. Nothing more. |
| Calibration and statistical equating | Needs candidate performance data. | Create the discrimination field, leave it empty, never estimate it. |
| Candidate registration, exam-day delivery, scoring, results | Separate phases with separate owners. | Nothing. Sealed content is never delivered by this MVP. |

## 2.4 The start line and the finish line

| Start line — where the MVP begins The MVP begins when a provisioned author, holding a current capability entry, signs in through the enterprise identity provider from a managed workstation inside an approved network zone, and sees an assignment in My Work inside an active cycle whose syllabus version and taxonomy are in force. Everything upstream of that moment is a precondition owned by someone else (§16.1): the identity provider and its multi-factor policy, device management and posture reporting, the hardened studio, the decision to run a cycle, the syllabus, the glossary, and the curated reference sources. The MVP consumes them; it does not build them. |
| --- |

| Finish line — where the MVP ends The MVP ends at four machine boundaries, and no examination content crosses any of them: 1. The readiness interface answers the assembly service's workload identity with metadata only (§6.10). 2. The selection notification and the exam-completion event, signed by the assembly service, are accepted and drive the artefact from Sealed to Used to Archived (§6.12). 3. Supersession notifications are emitted to downstream consumers and their acknowledgements are tracked (§6.11). 4. The evidence pack — the hash-chained audit trail, manifests and verification results — is available to auditors (§6.13). The delivery finish line is the closeout in §14.6: a release candidate installed in production, every acceptance criterion in §17 signed in one shared evidence pack, and a recorded go-live decision. |
| --- |

## 2.5 Boundary contracts

Each row is an interface the MVP has with something it does not build. The counterpart owner must be named at Week 0 (§14.0).

| Interface | Direction | Counterpart | This MVP's obligation | Section |
| --- | --- | --- | --- | --- |
| Identity (OpenID Connect) | Inbound | Enterprise identity provider (IT) | Consume tokens, require a multi-factor claim, map the subject to a pseudonymous audit identifier, build no password form. | §6.2 |
| Device certificate, posture and network zone | Inbound | Endpoint management and network (IT) | Refuse sign-in from an unmanaged or non-compliant device or an unapproved zone; raise a security event. | §6.2 |
| Key management | Outbound | Enterprise key management service (Security) | Envelope-encrypt sealed content and sign manifests without ever persisting raw key material. | §6.9 |
| Malware scanning and data-loss prevention | Outbound | Enterprise security services | Quarantine every upload until it passes; fail closed when the scanner is unavailable. | §10.5 |
| Monitoring and alerting platform | Outbound | Enterprise monitoring (Security / Operations) | Send security events and operational alerts that carry identifiers and scores, never content. | §6.14, §6.15 |
| Readiness | Outbound read | Assembly service | Paginated, metadata-only records over mutual TLS with an audience-restricted token; reject human tokens. | §6.10 |
| Selection notification, exam completion | Inbound | Assembly service | Verify signature, apply idempotently and atomically, transition Sealed → Used → Archived. | §6.12 |
| Supersession notification and acknowledgement | Outbound then inbound | Assembly service and any registered consumer | Notify on supersession, record acknowledgements, alert when unacknowledged past the configured window. | §6.11 |
| Cycle and taxonomy configuration | Inbound configuration | Review Coordinator, Taxonomy Administrator (Content Operations) | Provide the two configuration screens; nothing can be authored until both hold valid data. | §6.1 |
| Glossary, reference material, symbol palettes | Inbound content | Content Operations | Serve them read-only inside the tool so the author never leaves it and no external source is reachable. | §6.4 |

## 2.6 Explicit non-goals

- It does not assemble papers, select questions, or decide which question a candidate sees. 
- It does not register candidates, run the exam day, mark work, or publish results. 
- It does not track how questions perform in a live examination. 
- It does not let artificial intelligence validate, review, approve, seal or monitor anything. Layer 1 contains no model; Layer 2 drafts only (§1.5). 
- It does not offer download, print, export or persistent browser storage of content to anyone. 

## 2.7 Convergence with the engineering PRD

Engineering has started from its own document, Open Mulyankan — PRD (20 pages), which frames the product as a secure platform for generating, reviewing, translating, validating and assembling assessment questions from curriculum material, using Sarvam AI for OCR, curriculum processing, generation and translation drafts. This PRD converges on that document so the two never diverge: where the two agree, the engineering names are canonical (roles, states, identifiers); where the engineering document is open (its TBD cells and open questions), the answer in this PRD applies; where the engineering document conflicts with a specification MUST, the MUST stands in this text and the conflict is a numbered decision in §15 for the Product Owner to close this week — engineering should not change course on those items until the decision is recorded.

### Concept map

| Engineering PRD term | In this PRD and the stack | Note |
| --- | --- | --- |
| Open Mulyankan (the working name in the engineering document) | Project Rachana. This MVP is its content-creation pipeline: authoring → question review → accessibility → translation → sealing → readiness. | Generation and assembly sit at the two ends of the pipeline (§2.4). |
| Curriculum (uploaded PDF, e.g. an NCERT textbook) | Reference material and syllabus source — ASM-01 at the boundary; served read-only inside the tool (ASM03-ATH-13). | Curriculum processing and OCR are generation-side (D-38). |
| Assessment blueprint (types, marks, count, candidate multiplier, weightage, Bloom's, difficulty, learning objective, competency, language) | Two things: its cycle-level fields (subject, grade, languages, permitted question types, marks) are the Cycle configuration (§6.1); its count, multiplier and weightage are generation and assembly parameters (ASM-02, ASM-07) that the review pipeline never displays. | Reviewer isolation forbids showing blueprint identity to reviewers. |
| Question Bank | The artefact store: the working store for drafts and versions under review, and the sealed repository for approved versions (ASM-05). | Same idea, two trust zones (§10.1). |
| Question ID QB-nnnnn | The artefact identifier: opaque, stable across languages and versions, unrelated to any final question number. | Adopted verbatim; the stack requires opaque identifiers (INT-07). |
| Candidate question (one of N generated) | One artefact with its own Draft. Candidates are independent artefacts, never grouped as alternatives. | Adopted verbatim. |
| GENERATED (v1, AI generated) | A Draft whose provenance is generated, carrying generation metadata (§6.4). It enters the identical human pipeline. | Subject to D-38. |
| Admin edits question (v2, v3 …) | Before submission: autosaved edits to the Draft. After approval: a correction — new lineage, readiness revoked, full pipeline again (§6.11). | Equals the engineering "approval reset". |
| Approval reset | Correction and supersession (RES06-COR-01..04). | Same rule; sealed bytes are never overwritten. |
| FULLY_APPROVED | Artefact readiness: the primary and every required language version are sealed against the same lineage (§5.4, §6.10). | The readiness status value is named FULLY_APPROVED. |
| Assessment / final question paper; final numbering | Assembly (ASM-07) and release custody (DAY-01), outside the pipeline; assembly consumes readiness metadata only. Final numbers exist only in the assembled paper. | D-40 covers building the assembly module in V1. |
| Reviewer isolation | Need-to-know at request time (§4.2) plus the permitted-metadata list in §6.6, which adopts the engineering list verbatim. | Core security requirement in both documents. |
| Reviewer assignment (automated; algorithm TBD) | Assignment policy §6.3: eligibility and separation-of-duties filters, then lowest active workload with a deterministic tie-break — one of the options the engineering document lists — plus its rule that a corrected question goes to a different reviewer. | Closes the engineering open question. |
| Comment (any review role) | Findings and comments on decisions (§6.6). Visible to the Admin and carried to the successor draft; never visible to other reviewers. | Adopted. |
| Audit logs; user activity | The hash-chained audit and the evidence view (§6.13), content-free by construction. | Admin may hold the Auditor view (D-45). |

### Role map

| Engineering PRD role | This PRD | Constraints that travel with the role |
| --- | --- | --- |
| Admin | A composite of the specification's Coordinator, Author, Taxonomy Administrator and Auditor capabilities. There is no separate Question Creator in V1, so the Admin authors every question. | Because the Admin authors, the Admin can never approve or reject at any review stage (separation of duties, D-46); cannot read sealed plaintext; cannot download, export or physically delete content (D-39, D-41); cannot seal. |
| Question Reviewer | Reviewer (§6.6). | Read-only; cannot copy, download or export; sees only the assigned question and its permitted metadata. |
| Accessibility Specialist | New remediation role: works the accessibility task on a field-restricted draft (alternative text, decorative flags, table headers and captions, equation text alternatives, reading-order markup), comments, and completes the task (§6.7). | Cannot change stem, options, answer, marks or mathematical notation; cannot approve; cannot act on a version they authored or question-reviewed. |
| Accessibility Reviewer | The accessibility gate: approves or rejects with findings and records accommodation capability (§6.7). | Cannot edit; cannot act on a version they authored, remediated or question-reviewed. |
| Translator | Translator (§6.8). | Target-language fields only; locked structure; cannot approve own work. |
| Translation Reviewer | Translation Reviewer (§6.8). | Cannot edit; different reviewer after each rejection. |
| — (not in the engineering PRD) | Integrity Operator, Auditor, System, Platform Administrator, Assembly service. | Retained from the specification; the Admin may hold the Auditor and Integrity Operator views because those surfaces carry no content (D-45). |

### State map

The canonical state enumeration for implementation is the engineering one, extended with the post-approval states the stack requires. §5.2 defines each state; this table shows the correspondence.

| Engineering PRD state | Canonical state in this PRD | Note |
| --- | --- | --- |
| GENERATED | DRAFT with provenance generated | Manually created questions are DRAFT with provenance manual. |
| IN_QUESTION_REVIEW | IN_QUESTION_REVIEW | Immutable submitted version. |
| REJECTED | REJECTED | Terminal for that version; it stays as evidence. |
| QUESTION_CORRECTION | DRAFT with provenance correction, linked to the rejected version | A successor draft, never an edit of the rejected version. |
| NEW_QUESTION_REVIEWER | An assignment event, not a state | The different-reviewer rule (PRD-ASG-10). |
| IN_ACCESSIBILITY | IN_ACCESSIBILITY | The Accessibility Specialist's remediation draft is open. |
| ACCESSIBILITY_CORRECTION, NEW_ACCESSIBILITY_REVIEWER | Successor accessibility draft; assignment event | As for question review. |
| IN_ACCESSIBILITY_REVIEW | IN_ACCESSIBILITY_REVIEW | The Accessibility Reviewer's gate. |
| — | SEALING_REQUESTED, SEALED | Added by the stack: after accessibility approval the system seals the language version (§6.9). |
| IN_TRANSLATION | IN_TRANSLATION | A variant draft per required language, created when the primary seals. |
| IN_TRANSLATION_REVIEW, TRANSLATION_CORRECTION, NEW_TRANSLATION_REVIEWER | IN_TRANSLATION_REVIEW; successor variant draft; assignment event | After approval the variant has its own accessibility remediation and review (D-43) and is then sealed. |
| FULLY_APPROVED | Artefact readiness status FULLY_APPROVED | All required language versions sealed; the only status assembly may select. |
| — | WITHDRAWN, SUPERSEDED, USED, ARCHIVED, RETIRED | Added by the stack (§5.2). |

### Adopted from the engineering PRD without change

- State and role names above; question identifiers of the form `QB-nnnnn` with no relation to final numbering. 
- The two-role accessibility flow: the Accessibility Specialist works, the Accessibility Reviewer approves or rejects. 
- After any rejection the corrected work goes to a different reviewer (`PRD-ASG-10`). 
- The reviewer-isolation list: no assessment name, title or identifier; no final question number; no other questions; no candidate-pool membership or selection status; no other reviewers; no audit history (`PRD-REV-19`). 
- Comments at every review stage; every substantive modification is versioned and re-reviewed; the original question is never replaced; each language is independently trackable with its own translator, version, review status, reviewer, comments and approval history. 
- Version records preserve previous content, new content, editor, timestamp, reason and review status — provided here by the immutable version plus the decision record (§8.2). 
- The question metadata list (question type, marks, subject, grade, curriculum, Bloom's level, difficulty, learning objective, competency, language, source curriculum, chapter, page and context, status, version, timestamps, generation identifier, model and configuration) — added to the content model in §6.4. 
- The generation-validation list (grounding, type, marks, blueprint constraints, Bloom's, difficulty, duplicates, answer validity, completeness, metadata completeness) — mapped onto the validation catalogue in §6.5; questions failing automated validation never reach human review. 

### Engineering open questions, answered

| Open question in the engineering PRD | Answer in this PRD |
| --- | --- |
| What exactly does the Accessibility Specialist do? | Remediates the rendered question for accessibility: writes or edits alternative text, marks decorative images, adds table headers and captions, supplies text alternatives for equations, fixes reading-order markup, and flags anything that needs an authoring change. Then completes the task (§6.7, PRD-ACC-16). |
| Is accessibility evaluated through a structured checklist? | Yes. The specialist completes the evaluation checklist as a self-check; the Accessibility Reviewer completes it as the gate (§6.7). |
| Can the specialist modify accessibility metadata? Add alt text? | Yes, both — on an accessibility draft restricted to accessibility fields. |
| Can the specialist modify images? | No. Image bytes are author-owned, scanned and hashed; the specialist requests re-authoring through a finding. |
| Can the specialist modify question formatting? | Only accessibility-relevant markup (headers, captions, reading order), never wording. |
| Can the specialist modify mathematical notation? | No. A text alternative may be added; a notation change is an authoring correction. |
| Does accessibility apply to the original, translations, or both? | Both: each language version gets its own remediation and review (ASM04-TRN-05; see D-43). |
| What constitutes an accessibility rejection? | At least one blocking finding naming the element, criterion and required remediation (PRD-ACC-11). |
| Can an accessibility issue require an authoring change? | Yes: the reviewer returns it with an RC-A11Y-* reason to the author; the remediation-routing policy decides whether question review repeats (§5.4, D-07). |
| What accessibility standards? | WCAG 2.1 AA for the rendering and the surfaces (§11), plus the cycle's declared accommodations (D-17). |
| Explicit "complete" action before the reviewer? | Yes: the specialist submits the accessibility draft, which creates the immutable version that enters IN_ACCESSIBILITY_REVIEW. |
| Should the specialist comment? Approve or reject? | Comment: yes. Approve or reject: no — approval belongs to the Accessibility Reviewer. The two TBD cells in the engineering RBAC matrix resolve to "no access". |
| Exact assignment algorithm? | Eligibility and separation-of-duties filters, then lowest active workload with a deterministic tie-break (PRD-ASG-04); availability-aware weighting can be added later without changing the contract. |
| Exact source information visible to reviewers? | Subject, grade, curriculum name and source chapter and page range, so grounding can be checked; never the full source context text, the blueprint or the assessment (D-47). |

### Conflicts with the specification, recorded as decisions

| Decision | Engineering PRD says | Specification says | Recommended resolution in this PRD |
| --- | --- | --- | --- |
| D-38 | Questions and translation drafts are generated by Sarvam AI from the curriculum. | ARC-12: no component provides AI capability; every judgement is a person or a fixed rule. | Decided by the Product Owner on 7 September 2026: AI capabilities are in the MVP and the demo as Layer 2. The prohibition is narrowed to Layer 1: AI may draft (generation, translation first draft, metadata suggestion) but never judge — no AI in validation, similarity, review, accessibility, sealing, readiness or monitoring. Generated text enters as a Draft with provenance and passes the identical human pipeline. Layer 2 sits outside the hardened zones behind the single connector (§1.5). Security still ratifies the hosting model for translation drafts (D-48). |
| D-39 | Admin can download and export. | ASM03-ATH-10, INT-06: no download, print, export or bulk export from the pipeline. | No role downloads or exports from the question bank. Exporting the assembled paper is a release-custody function (DAY-01) of the assembly module, with its own controls and audit, outside this pipeline. |
| D-40 | Admin assembles the assessment, selects final questions and reorders them in the product. | ASM-07 is a separate service; selection is blind; sealed content is unreadable. | Build assembly as a separate module that consumes the readiness interface and selects by metadata against the blueprint — which is blind assembly. Paper rendering pulls sealed content through the release-custody path, never through authoring surfaces. |
| D-41 | Admin can delete questions. | SEC-08: no deletion operation exists for content. | "Delete" means Withdraw (unsubmitted draft) or Retire (approved or sealed). Nothing is physically deleted; the button may still say Delete. |
| D-42 | Admin views all questions and all metadata. | Need-to-know; sealed plaintext is unreadable (SEC-01). | Allowed for unsealed versions because the Admin authors every question in V1. Once sealed, metadata only. If a separate Author role is added later, the Admin's content view shrinks to own drafts. |
| D-43 | One accessibility pass on the original; translations go straight from translation review to FULLY_APPROVED. | ASM04-TRN-05: each language variant receives its own accessibility check. | Keep the per-language check: the variant remediation is small (translated alternative text and captions) and the reviewer gate is quick. Deferring it for the pilot is a documented drop, not a silent one. |
| D-44 | The blueprint supports several question types (for example Short Answer). | The MVP item type is single-select multiple choice. | Item type stays data. Validation and structural checks are complete for MCQ. Other types may flow through the same pipeline with a reduced rule set only when enabled per cycle by the Assessment owner. |
| D-45 | Admin views audit logs and user activity. | Auditor and Integrity Operator are distinct roles that reach no content. | Admin may hold both views because they carry no content. A distinct Integrity Operator person is recommended for the pilot so the person monitoring authors is not the author. |
| D-46 | The RBAC matrix gives Admin Approve and Reject at every stage. | INS04-CAP-07: whoever authored or translated a version cannot approve it; the API enforces this. | Remove Approve and Reject from the Admin column. The Admin assigns, reassigns and releases reviewers and authorizes corrections, but never decides a review stage. |
| D-47 | "The exact source information visible to reviewers is subject to the security design." | Reviewer isolation; no content beyond the assigned question. | Show subject, grade, curriculum name, chapter and page range; hide the stored source context text, the blueprint and the assessment. |

Not in the engineering PRD but retained from the specification: multi-factor authentication and device posture at sign-in (`INS04-CAP-02`, `INS04-CAP-11`), session integrity monitoring (§6.14), the hash-chained audit (§6.13), sealing and the readiness interface (§6.9 – 6.10). None of these changes the engineering workflow; they wrap it.

# 3. Goals, success measures and release gates

| Goal | Outcome | How it is measured |
| --- | --- | --- |
| G1 | A question passes all four jobs in the primary language and two further languages and is sealed without any human seal control. | End-to-end acceptance in §17.2 demonstrated with real role users and synthetic content; no seal endpoint exists for any human role. |
| G2 | No plaintext leakage. No role, including administrators, can retrieve sealed plaintext; no Restricted content appears in logs, traces, telemetry, notifications, dashboards or error messages. | Automated no-content assertions pass on every build; penetration test closes with no open Critical or High finding. |
| G3 | Separation of duties cannot be bypassed through the interface or the API. | The role-by-operation permission matrix (§4.3) runs as an automated test oracle; a hand-crafted direct API call by a multi-role user is refused. |
| G4 | Evidence integrity is provable. | Chain verification passes across the full data set, still passes after backup and restore, and detects a deliberately altered, removed or reordered event in a copy of the store. |
| G5 | Live integrity monitoring works from the first keystroke. | A deliberate blocked action appears on the operator surface within p95 ≤ 3 s and in durable audit within p95 ≤ 5 s, scored and attributed, carrying no content. |
| G6 | The service meets its operating targets. | §11 targets met under load with evidence retained: 50 concurrent sessions, 100,000 artefacts, 500,000 versions, RTO ≤ 4 h, RPO ≤ 15 min, WCAG 2.1 AA. |
| G7 | Production acceptance on evidence, not demonstration. | Release candidate installed in production; every §17 criterion signed in one evidence pack; go-live decision recorded with its rationale. |

### Release gates

- No unresolved Critical or High finding from the penetration test or the accessibility audit. 
- Stated capacity, latency and recovery targets met under load, with evidence retained. 
- Backup, restore and chain verification pass end to end; hashes verify after restore. 
- Every runbook has a named owner and has been walked through once. 
- Signatures from Product, Architecture, Security, Accessibility, Content Operations, QA and Operations. 

# 4. Users, roles and the permission matrix

## 4.1 Roles

Role names follow the engineering PRD (§2.7). A role grants a capability class. Whether a person may act on a specific version is decided at request time by assignment, language, state, cycle policy, recognized capability and separation of duties (§4.2). The "Explicitly cannot" column is normative: it is tested, not assumed.

| Role | Responsibility | Explicitly cannot | Primary surface |
| --- | --- | --- | --- |
| Admin | Holds the specification's Coordinator, Author, Taxonomy Administrator and Auditor capabilities. Uploads curriculum and reference material; configures cycles, blueprint-level settings and taxonomy; triggers generation; creates, edits, validates, previews and submits questions (the Admin authors every question in V1); withdraws or retires questions; assigns, reassigns and releases reviewers; views workload, review status, safe progress and aging; approves exceptions; authorizes corrections; manages users and their capability entries; views the content-free audit. | Approve or reject at any review stage (D-46); read sealed plaintext; download, export or physically delete content; seal; browse another author's drafts if a separate Author role is ever introduced. | Admin workspace: My Work, Authoring, Configuration, Assignment, Evidence (UI-02, 04, 05, 10, 12) |
| Question Reviewer | Assess an assigned immutable version; comment; approve or reject with rationale; record the three attestations; assign difficulty. | Edit content; copy, download or export; see assessment identity, other questions, other reviewers or audit history; review a version they authored or translated. | Review (UI-06, UI-07) |
| Accessibility Specialist | Remediate the rendered question on an accessibility draft: alternative text, decorative flags, table headers and captions, equation text alternatives, reading-order markup; comment; complete the task for review. | Change stem, options, answer, marks or mathematical notation; replace images; approve or reject; act on a version they authored or question-reviewed. | Accessibility remediation (UI-08a) |
| Accessibility Reviewer | Test the rendered artefact; comment; approve or reject with findings; record accommodation capability and equivalent-route needs. | Edit content; act on a version they authored, remediated or question-reviewed. | Accessibility review (UI-08) |
| Translator | Produce an assigned target-language version from a read-only primary reference and the glossary; comment; submit for translation review. | Alter primary fields, structure, locked values or answer semantics; approve their own work. | Translation (UI-09) |
| Translation Reviewer | Validate fidelity, terminology, script-specific grammar and answer equivalence; comment; record the equivalence judgement; approve or reject. | Edit the variant; approve their own work; review a translation they produced. | Review (UI-06) |
| Integrity Operator | Observe live session integrity; act on referred sessions. | View artefact content or perform any workflow action. | Operator (UI-11) |
| Auditor | Inspect audit events, decisions, hashes, policy outcomes and verification results. The Admin may hold this view (D-45). | Perform workflow actions or browse plaintext content. | Evidence (UI-12) |
| System | Revalidate, sanitize, canonicalize, hash, encrypt, seal, index, compute readiness, emit events, apply downstream notifications, create generated drafts on the Admin's request. | Accept a human login or make a discretionary decision. | Workers (no UI) |
| Platform Administrator | Operate infrastructure through privileged-access management. | Inherit content permissions or bypass application policy. | Infrastructure tooling only |
| Assembly service (workload) | Read readiness records; select by metadata; send selection notifications, exam completions and supersession acknowledgements. In V1 the assembly module is operated by the Admin (D-40). | Receive any content field through the readiness interface; use a human token. | Machine interface (§7.3) |

## 4.2 The authorization decision

Every request is evaluated server-side against all of the following. A single failing check denies the request with a machine-readable code (§7.2), writes an audit event, and — for any object outside the user's assignments — raises a security event (`INS04-CAP-09`).

| Key | Check | Rule |
| --- | --- | --- |
| A | Assignment | An Active assignment binds this user to this task and this version, lineage or artefact. The Admin acts on configuration and assignment surfaces without artefact assignments, and on drafts as their author. |
| S | State | The version's lifecycle state permits the operation (§5.3). DRAFT, IN_ACCESSIBILITY and IN_TRANSLATION are the only editable states, each restricted to its own field set. |
| D | Duty | No separation-of-duties conflict on the lineage (§4.4). |
| C | Capability | A current, non-revoked capability entry exists for this role whose subject scope and language scope cover the artefact. Subject, language and workload matching alone never authorize (INS04-CAP-05). |
| P | Policy | The cycle is Active (or Closed for completing in-flight work) and the operation is permitted under the cycle's policy version. |
| R | Re-authentication | A privileged action requires a fresh authentication with the identity provider (§6.2, D-14). |
| W | Workload | Mutual TLS plus an audience-restricted, short-lived workload token for the named service. Human bearer tokens are rejected. |

## 4.3 Role-by-operation permission matrix

This matrix satisfies `INT-09` and supersedes the engineering RBAC matrix: it keeps every capability row from that matrix, resolves its TBD cells, and adds the operations the stack requires. A cell shows the request-time conditions (keys from §4.2) that must all hold; "—" means never. Any operation absent from this table is denied by default.

| Operation | Admin | Question Reviewer | Access. Specialist | Access. Reviewer | Translator | Trans. Reviewer | Integrity Op. | System | Platform Admin | Assembly |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Upload curriculum; manage reference material, glossary and palettes | R | — | — | — | — | — | — | — | — | — |
| Create, change, activate or close a cycle and its blueprint-level settings; manage taxonomy and vocabularies | P R | — | — | — | — | — | — | — | — | — |
| Manage users and capability entries (create, renew, revoke) D-05 | R | — | — | — | — | — | — | — | — | — |
| Generate or regenerate candidate questions D-38 | C P | — | — | — | — | — | — | ✓ (creates drafts with provenance) | — | — |
| Manually create a question (draft, cap not reached) | A C P | — | — | — | — | — | — | — | — | — |
| Edit a draft, add images, validate, preview | A S C | — | — | — | — | — | — | — | — | — |
| See the correct answer of an unsubmitted draft | A S | — | — | — | A S (locked) | — | — | — | — | — |
| Submit a draft to question review | A S C P | — | — | — | — | — | — | — | — | — |
| "Delete": withdraw an unsubmitted draft D-41 | A S | — | — | — | — | — | — | — | — | — |
| "Delete": retire an approved or sealed question D-41 | R | — | — | — | — | — | — | — | — | — |
| View all questions and metadata (content only while unsealed) D-42 | ✓ | — | — | — | — | — | — | — | — | — |
| View an assigned version read-only (content, hash, permitted metadata) | — | A S D C | A S D C | A S D C | — | A S D C | — | — | — | — |
| See the correct answer of a version under review | — | A S D, where cycle policy requires D-06 | A S D | A S D | — | A S D, same policy | — | — | — | — |
| Comment | ✓ (own drafts and findings) | A | A | A | A | A | — | — | — | — |
| Approve or reject question review (with attestations and difficulty) | — D-46 | A S D C P | — | — | — | — | — | — | — | — |
| Remediate accessibility (accessibility fields only) and complete | — | — | A S D C | — | — | — | — | — | — | — |
| Approve or reject accessibility review; record accommodation capability | — | — | — (resolves TBD) | A S D C P | — | — | — | — | — | — |
| Create or edit a translation (target fields only); submit | — | — | — | — | A S C P | — | — | — | — | — |
| Approve or reject translation review with equivalence judgement | — | — | — | — | — | A S D C P | — | — | — | — |
| Request a structural-check exception D-15 | — | — | — | — | A | A | — | — | — | — |
| Approve or revoke an exception (approver ≠ requester) | R D | — | — | — | — | — | — | — | — | — |
| Assign, reassign or release reviewers; view reviewer workload and review status | ✓ | — | — | — | — | — | — | ✓ (policy) | — | — |
| View safe progress, aging, author caps, language status, escalations | ✓ | — | — | — | — | — | — | — | — | — |
| Seal a version | — | — | — | — | — | — | — | ✓ (sealing identity only) | — | — |
| Read sealed plaintext | — | — | — | — | — | — | — | Verification and seeding identities, in memory only | — | — |
| Authorize a correction to a sealed question (approval reset) D-16 | R | — | — | — | — | — | — | — | — | — |
| Assemble an assessment: select final questions by metadata, reorder, number D-40 | via the assembly module | — | — | — | — | — | — | — | — | W |
| Download or export from the question bank D-39 | Nobody. Paper export is a release-custody function of the assembly module (DAY-01), outside this pipeline. |  |  |  |  |  |  |  |  |  |
| Read readiness records; send selection notification, exam completion, supersession acknowledgement | — | — | — | — | — | — | — | — | — | W (signed) |
| View operator surface: sessions, event feed, drill-down, alerts | ✓ if holding the role D-45 | — | — | — | — | — | ✓ | — | — | — |
| View audit logs and user activity; run chain verification | ✓ (content-free) | — | — | — | — | — | — | ✓ (scheduled) | — | — |
| Operate infrastructure via privileged-access management | — | — | — | — | — | — | — | — | ✓ (no content path) | — |
| Any object outside the user's assignments | Denied with FORBIDDEN_NOT_ASSIGNED; a security event is raised (INS04-CAP-09). |  |  |  |  |  |  |  |  |  |

## 4.4 Separation-of-duties rules

These rules are evaluated per lineage at every decision endpoint, independently of the interface (`INS04-CAP-07`), and must be provable by both the interface and a hand-crafted direct API call (`SEC-06`).

| Rule | Statement | Source |
| --- | --- | --- |
| SoD-1 | A user who authored, generated-and-submitted, or translated any version in a lineage cannot question-review, accessibility-remediate, accessibility-review or translation-review any version in that lineage, or in any lineage of the same artefact and language derived from it. In V1 this means the Admin never decides a review stage. | INS04-CAP-07, ASM03-REV-01, D-46 |
| SoD-2 | A user who question-reviewed a version cannot remediate or accessibility-review it; the Accessibility Reviewer of a version cannot be its Accessibility Specialist. | INS04-CAP-08 |
| SoD-3 | A translator cannot approve their own variant. The translation reviewer of a variant cannot be its translator or the author of the primary it was derived from. | ASM04-TRN-04, roles table |
| SoD-4 | The approver of an exception must differ from its requester. | GAP derived from ASM04-TRN-08 |
| SoD-5 | The authorizer of a correction cannot be the reviewer who later decides on it; in V1 the Admin authorizes and also authors the correction, so the reviewer must be a different person from any earlier reviewer of that lineage. | GAP derived from RES06-COR-01 |
| SoD-6 | After any rejection, the next review of that lineage at the same stage is assigned to a different reviewer from the one who rejected it. | Engineering PRD; PRD-ASG-10 |
| SoD-7 | Expiry or revocation of a capability blocks new assignment and flags in-flight tasks for reassignment, but never voids a decision already recorded. | INS04-CAP-06, INS04-CAP-10 |

# 5. Domain model and artefact lifecycle

## 5.1 Concepts

| Concept | Definition |
| --- | --- |
| Cycle | The configuration boundary for an examination cycle: primary and required languages, syllabus version, permitted question types, marking-policy reference, declared accommodations, author cap, review policy, status. Holds the cycle-level fields of the engineering blueprint. |
| Blueprint (generation and assembly parameters) | Required count, candidate multiplier, weightage and selection targets. Consumed by generation and assembly; never shown inside the review pipeline. |
| Artefact (question, QB-nnnnn) | A stable opaque identity for one question across its primary language and every language variant. Holds the current primary, per-language status and readiness. Unrelated to any final question number. |
| Lineage | The ordered chain of versions of one artefact in one language, from first draft through rejections to a sealed version. A correction (approval reset) starts a new lineage; the superseded lineage is retained. |
| Version | Either a working draft (DRAFT, IN_ACCESSIBILITY, IN_TRANSLATION) or an immutable snapshot (every other state) with language, state, lineage, provenance, canonical content, classification and content hash. |
| Provenance | How a draft came to exist: generated, manual, correction, accessibility, translation, revalidation; generated drafts carry generation metadata (§6.4). |
| Variant | A version in a required non-primary language, bound to the primary sealed version it was derived from by that primary's content hash. |
| Option | A stable, ordered choice within a version, with a structural identifier and a correct-answer flag. Structural identifiers survive translation. |
| Asset | A private image referenced by a version: object key, checksum, scan status, alternative text, decorative flag. |
| Assignment | The authorization binding between one user and one task, with type, expiry and status. |
| Capability Entry | What a contributor is recognized to do: role, subject and language scope, accessibility qualification, issuing authority, validity window, revocation state — against a pseudonymous audit identifier. |
| Decision | An append-only question-review, translation-review or accessibility-review decision bound to a version hash, with checklist, comments, findings, reviewer audit identifier and duration. |
| Comment | Free-text remark attached to a decision or to an accessibility or translation task; visible to the Admin and carried to the successor draft; never to other reviewers. |
| Exception | A recorded, approved, expiring permission to override a named blocked structural check on a named version. |
| Manifest | Verifiable evidence for one sealed version: hashes, approval references, policy version, key reference, signature, sealed location. |
| Readiness Record | The metadata-only contract read by assembly; its status is FULLY_APPROVED when every required language version is sealed. |
| Session | A per-login telemetry record: role, task context, timestamps, integrity score. |
| Integrity Event | One record per captured signal: kind, severity, timestamp, session, score after. |
| Audit Event | A tamper-evident, hash-chained record of every material action. |
| Taxonomy Node | A node in a versioned Subject → Unit → Topic hierarchy with active dates and retirement state. |

## 5.2 Lifecycle states

The server-side state machine is authoritative. Interface labels, cached state and client-supplied role claims never cause a transition. A rejection never edits the rejected version — it creates a new linked draft, and the rejected version remains as immutable evidence. State names are the engineering enumeration, extended with the post-approval states the stack requires (§2.7).

| StateDRAFTEditable. Visible only to its author. | → | StateIN_QUESTION_REVIEWImmutable. Awaiting the Question Reviewer. | → | StatesIN_ACCESSIBILITY → IN_ACCESSIBILITY_REVIEWSpecialist remediates; Accessibility Reviewer decides. | → | StateSEALEDIn the repository, encrypted. Routine human access has ended. |
| --- | --- | --- | --- | --- | --- | --- |

| State | Definition | Origin |
| --- | --- | --- |
| DRAFT | Editable working version, autosaved, visible only to its author (the Admin in V1). Provenance generated (engineering GENERATED), manual, or correction (engineering QUESTION_CORRECTION). The only state in which stem, options, answer, explanation and classification change. | Both |
| IN_QUESTION_REVIEW | Immutable submitted snapshot with a content hash, awaiting one or two independent question-review decisions (per cycle policy). For variants, this stage is IN_TRANSLATION_REVIEW. | Both |
| REJECTED | Terminal state of a version rejected at any stage. Immutable evidence carrying the decision and comments; a new linked draft was created from it and will be reviewed by a different reviewer. | Both |
| IN_ACCESSIBILITY | An accessibility draft is open for the Accessibility Specialist. Only accessibility fields are editable (alternative text, decorative flags, table headers and captions, equation text alternatives, reading-order markup). Completing the task submits an immutable version. | Engineering; field restriction from the specification |
| IN_ACCESSIBILITY_REVIEW | Immutable, awaiting the Accessibility Reviewer's decision on the reference rendering. A rejection creates an accessibility-correction draft (engineering ACCESSIBILITY_CORRECTION) or an authoring-correction draft, per finding. | Both |
| SEALING_REQUESTED | Immutable, queued for the sealing worker after accessibility approval. Progress is visible; failure keeps the version here with a retryable job. | Specification |
| SEALED | Canonicalized, encrypted and indexed in the repository with a signed manifest; the current version for its artefact and language; routine human access has ended. Sealing the primary creates the variant drafts. | Specification |
| IN_TRANSLATION | A variant draft is open for the Translator; only target-language fields are editable; structure is locked. Provenance translation, correction (engineering TRANSLATION_CORRECTION) or revalidation. | Both |
| IN_TRANSLATION_REVIEW | Immutable variant awaiting the Translation Reviewer's decision, including the equivalence judgement. Approval sends the variant to its own IN_ACCESSIBILITY (D-43). | Both |
| FULLY_APPROVED | Artefact-level readiness status, not a version state: the primary and every required language version are SEALED against the same lineage and nothing has revoked readiness. The only status assembly may select. | Both |
| SUPERSEDED | A newer version has been sealed for the same artefact and language after a correction (approval reset). Retained as evidence with a reference to its replacement; never returned by readiness. | Specification |
| WITHDRAWN | Terminal state of an unsubmitted draft withdrawn by its author ("Delete" on a draft). Audited; removed from active counts and from the author cap. | Specification; engineering "Delete" |
| USED | Selected by the assembly service for an exam session. Immutable; excluded from every readiness query. | Specification |
| ARCHIVED | The exam session that used it has completed. Read access limited to audit and dispute roles under the break-glass procedure; keys rotated to the archive tier. No return path. | Specification |
| RETIRED | Withdrawn from future use by an authorized Admin decision with reason ("Delete" on an approved or sealed question). Sealed hash and classification preserved; excluded from readiness. | Specification; engineering "Delete" |

## 5.3 Transitions

Every transition writes its audit event in the same database transaction (`ARC-02`). An invalid transition is rejected with a conflict response and a descriptive message (`SEC-07`).

| From | Action | Actor | Conditions | To |
| --- | --- | --- | --- | --- |
| — | Create (manual) | Admin as author | Active cycle; capability current; author cap not reached. | DRAFT (manual) |
| — | Generate | System, on the Admin's generation request | Cycle active; generation enabled (D-38); automated validation passed; provenance and generation metadata recorded. Failing candidates are never created as drafts. | DRAFT (generated) |
| — | Create variant drafts | System, on sealing the primary | One draft per required language, carrying locked structure and a read-only primary reference (§6.8). | IN_TRANSLATION |
| — | Seed correction draft (approval reset) | System, on recorded Admin authorization | New lineage; readiness revoked (§6.11). | DRAFT (correction) |
| DRAFT | Submit | Admin as author | All blocking validations pass; durable audit available. | IN_QUESTION_REVIEW |
| DRAFT | Withdraw ("Delete") | Admin as author | Never submitted. | WITHDRAWN |
| IN_QUESTION_REVIEW | Approve | Question Reviewer | No duty conflict; complete checklist including the three attestations; difficulty assigned; required number of independent approvals reached. Creates the accessibility task. | IN_ACCESSIBILITY |
| IN_QUESTION_REVIEW | Reject | Question Reviewer | Reason code and comments. Successor draft to the author; next review by a different reviewer. | REJECTED + new DRAFT |
| IN_ACCESSIBILITY | Complete | Accessibility Specialist | Accessibility self-check complete; only accessibility fields changed (machine-verified); no duty conflict. | IN_ACCESSIBILITY_REVIEW |
| IN_ACCESSIBILITY_REVIEW | Approve | Accessibility Reviewer | No duty conflict; no unresolved blocking finding; mandatory comments; accommodation capability recorded; equivalent-route need recorded and escalated where applicable. | SEALING_REQUESTED |
| IN_ACCESSIBILITY_REVIEW | Reject | Accessibility Reviewer | Affected element and required remediation recorded. Accessibility findings go to the specialist as an accessibility-correction draft; authoring findings go to the author, and question review repeats per policy (§5.4). Next review by a different reviewer. | REJECTED + new draft |
| SEALING_REQUESTED | Seal | System (sealing identity) | Approvals, expected evidence, lineage, scans, schema, policy and cryptography all available and revalidated (§6.9). | SEALED |
| SEALING_REQUESTED | Seal fails | System | Any dependency unavailable or any check failing. No state change; job marked failed; safe retry; alert on repeated failure. | SEALING_REQUESTED |
| IN_TRANSLATION | Submit | Translator | Target fields non-empty; structural checks pass or an active exception covers them. | IN_TRANSLATION_REVIEW |
| IN_TRANSLATION_REVIEW | Approve | Translation Reviewer | No duty conflict; checklist complete; equivalence judged. Creates the variant's accessibility task (D-43). | IN_ACCESSIBILITY (variant) |
| IN_TRANSLATION_REVIEW | Reject | Translation Reviewer | Reason code and comments; successor variant draft to the translator; next review by a different reviewer. | REJECTED + new IN_TRANSLATION |
| All required versions SEALED | Readiness | System | Primary and every required language sealed against the same lineage; no revalidation pending; no correction open. | Artefact FULLY_APPROVED |
| SEALED | Supersede | System | A new version is sealed for the same artefact and language after a correction. | SUPERSEDED |
| SEALED | Selection notification | System, on a signed assembly notification | Primary and every sealed language variant of the artefact move together, atomically. | USED |
| USED | Exam completion | System, on a signed assembly event | Every used artefact in that session moves atomically; exam identifier, timestamp and artefact-set hash written to the audit chain; keys rotated to the archive tier. | ARCHIVED |
| SEALED | Retire ("Delete") | Admin (re-authenticated) | Reason recorded. SHOULD | RETIRED |
| Any pre-seal state | Assignment released, expired or capability revoked | System | The assignment changes state; the version does not. Recorded decisions remain valid. | Unchanged |

#### Invariants

- I1 A version in any state other than `DRAFT`, `IN_ACCESSIBILITY` or `IN_TRANSLATION` is byte-for-byte immutable; its content hash never changes. Each editable state permits only its own field set. 
- I2 No delete operation exists for artefact content in any state (`SEC-08`); "Delete" is Withdraw or Retire. 
- I3 For each artefact and language, at most one version is current (`SEALED`, `USED` or `ARCHIVED` and not `SUPERSEDED`). The pointer flips in the sealing transaction. 
- I4 Every transition and its audit event commit together or not at all. 
- I5 A rejected version is never edited. Its successor draft records `derived_from` and carries the findings and comments. 
- I6 A version never moves backwards. Remediation is always a new version, and the next review of it is by a different reviewer. 
- I7 The original (primary) question is never replaced by a translation; every language version is retained. 

## 5.4 Variants, readiness and revalidation

- Variant creation. Sealing the primary creates one `IN_TRANSLATION` draft per required language of the cycle (`ASM04-TRN-01`). Each carries the locked structure — option identifiers and order, correct-answer flag, marks, assets, canonical equations, classification — and a read-only snapshot of the primary's rendering and canonical text, visible only to the assigned Translator and, later, the Translation Reviewer. 
- Variant gates. A variant goes through Submit → `IN_TRANSLATION_REVIEW` (with the equivalence judgement inside the checklist) → its own `IN_ACCESSIBILITY` and `IN_ACCESSIBILITY_REVIEW` → sealing. No additional lifecycle state exists beyond these (`ASM04-TRN-07`). 
- Readiness rule. An artefact is `FULLY_APPROVED` when: the current primary is `SEALED`; for every required language a `SEALED` variant exists whose `primary_reference_hash` equals the current primary's content hash; no variant carries `requires_revalidation`; the artefact is not `USED`, `ARCHIVED` or `RETIRED`; and readiness has not been revoked by an open correction (`ASM07-RDY-01`). 
- Approval reset (revalidation). When the Admin corrects an approved or sealed question, readiness is revoked immediately, a new lineage starts, every dependent variant is flagged `requires_revalidation`, and the Translator is shown a field-level difference between the old and new primary reference (`ASM04-TRN-09`, `RES06-COR-03`). The full pipeline runs again. 
- Remediation routing. Whether a version rejected at accessibility review must repeat question review is cycle policy (`ASM04-ACC-06`). The default repeats question review when the successor draft changed content, answer or metadata — stem, option bodies, correct flag, explanation, classification or marks. A change confined to accessibility fields — alternative text, decorative flag, table headers or caption, equation text alternatives — goes back to accessibility review only. "Changed" is computed as a field-level difference of canonical content against the rejected version. GAP D-07 

# 6. Functional requirements

Requirements are grouped by the job they serve. Each group opens with the specification's requirements, carried with their IDs, followed by the gap-filling requirements this PRD adds, and closes with acceptance criteria the QA Lead uses to close the group.

## 6.1 Cycle, syllabus and taxonomy configuration · ASM01-CFG

Boundary block. The MVP consumes the construct, syllabus and taxonomy as configuration. Nothing can be authored until a cycle and a taxonomy version exist and are valid.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM01-CFG-01 | A coordinator can configure a cycle: code, title, primary language, required languages, syllabus version, permitted item types, marking-policy reference, declared accommodations, and status. | MUST |
| ASM01-CFG-02 | Artefacts can be created only within an active, valid cycle. | MUST |
| ASM01-CFG-03 | A taxonomy administrator manages versioned Subject → Unit → Topic hierarchies plus controlled difficulty and taxonomy-level vocabularies. | MUST |
| ASM01-CFG-04 | Taxonomy values in use can be retired for future selection but never deleted. Historical versions retain their original references. | MUST |
| ASM01-CFG-05 | Cycle and taxonomy configuration have working interfaces — nothing can be authored until both exist. | MUST |
| PRD-CFG-06 | GAP The cycle record carries, in addition to CFG-01: author cap per cycle; required review count (1 or 2) D-06; whether reviewers see the correct answer D-06; remediation-repeats-review policy D-07; assignment expiry per task type D-12; similarity threshold D-08; default marks per item from the marking policy; a monotonically increasing policy_version that increments on every change. | MUST |
| PRD-CFG-07 | GAP Cycle status is one of Draft (editable, nothing can be authored), Active (drafts may be created) and Closed (no new drafts; in-flight tasks, sealing and readiness continue). Changing required languages or syllabus version on an Active cycle requires re-authentication, increments the policy version and emits policy.changed; existing versions keep their recorded references. A cycle is never deleted. | MUST |
| PRD-CFG-08 | GAP A taxonomy version is an immutable published tree once referenced by a cycle. Node identifiers are stable across versions. Nodes carry active_from and retired_at. A new version may retire nodes; retirement is a date, never a deletion, so every historical reference resolves. | MUST |
| PRD-CFG-09 | GAP Controlled vocabularies are versioned lists managed by the taxonomy administrator: difficulty, taxonomy level, complexity level (used by bank indexing), item type, declared accommodation. Proposed initial values are in D-17 and D-18. Values are retired, never deleted. | MUST |
| PRD-CFG-10 | GAP Every decision, submission and seal records the cycle policy_version, taxonomy version and vocabulary versions in force at that moment, so the evidence pack can reproduce the rules that applied. | MUST |
| PRD-CFG-11 | GAP A cycle may have an empty list of required languages (single-language cycle). Readiness then requires only the sealed primary. | MUST |

#### Acceptance criteria

- A coordinator creates a cycle with two required languages and activates it; an author in that cycle can create a draft; an author in a Draft or Closed cycle cannot, and receives `CYCLE_INACTIVE`. 
- Retiring a topic blocks its selection in new drafts (`TAXONOMY_RETIRED`) while an existing version that references it still renders its classification. 
- Changing the required languages of an Active cycle is refused without re-authentication and, once made, appears as a `policy.changed` domain event with the new policy version. 

## 6.2 Recognized capability and access · INS04-CAP

Boundary block. The official record of who in the authoring workforce is recognized, and what each is permitted to do.

| ID | Requirement | Priority |
| --- | --- | --- |
| INS04-CAP-01 | Interactive users authenticate through the enterprise identity provider. The product implements no local-password login. | MUST |
| INS04-CAP-02 | Multi-factor authentication is enforced for all content-handling and privileged roles. | MUST |
| INS04-CAP-03 | Sessions are short-lived with an inactivity timeout; privileged actions require re-authentication. | MUST |
| INS04-CAP-04 | A registry records, against a pseudonymous workforce audit identifier, what each contributor is recognized to do: role, subject and language scope, accessibility qualification, issuing authority, validity window and revocation state. | MUST |
| INS04-CAP-05 | Assignment requires a current, non-revoked, in-scope entry in the registry. Subject, language and workload matching alone do not authorize an assignment. | MUST |
| INS04-CAP-06 | Expiry blocks new assignment and flags in-flight tasks for reassignment. It never voids a decision already recorded. | MUST |
| INS04-CAP-07 | A user may hold multiple roles but is blocked from authoring or translating and then approving the same version. The API enforces this independently of the interface. | MUST |
| INS04-CAP-08 | An accessibility specialist cannot act on a version they authored, translated or reviewed. | MUST |
| INS04-CAP-09 | Access to any object outside the user's assignments returns a denial and raises a security event. | MUST |
| INS04-CAP-10 | Revocation takes effect on the next request; an in-flight assignment becomes unactionable immediately. | MUST |
| INS04-CAP-11 | Sign-in to any content-handling surface succeeds only from a managed workstation inside an approved network zone, proven by device certificate and posture check. A request from an unmanaged or non-compliant device is denied and raises a security event, regardless of how valid the user's credentials are. | MUST |
| PRD-CAP-12 | GAP Identity integration uses OpenID Connect Authorization Code flow with PKCE against the enterprise identity provider. The token must carry a stable subject and an authentication-methods claim proving multi-factor authentication; a token without it is refused with FORBIDDEN_MFA_REQUIRED. Group or role claims in the token are informational only and never authorize anything (ARC-01). | MUST |
| PRD-CAP-13 | GAP Pseudonymization: on first sign-in the system generates a random, unguessable, stable workforce audit identifier and stores the mapping to the identity-provider subject in a separately access-controlled table. All business records, audit events, telemetry and screens other than the coordinator's assignment views use the audit identifier only (DAT-02). | MUST |
| PRD-CAP-14 | GAP D-14 Proposed session parameters: access token lifetime 15 minutes with silent refresh; refresh window 8 hours; inactivity timeout 20 minutes with a visible warning at 18; absolute session maximum 10 hours. Privileged actions requiring a fresh authentication (no older than 5 minutes): cycle changes, registry changes, exception approval, correction authorization, retirement, manual assignment override. | MUST |
| PRD-CAP-15 | GAP Device and zone proof (CAP-11): a client certificate from the enterprise device authority presented at the TLS edge; a posture assertion from endpoint management (disk encryption on, operating system patched, agent running) no older than the configured freshness D-14; and a source address inside the approved studio zone. All three are checked at sign-in and on every token refresh. Failure denies with FORBIDDEN_DEVICE_POSTURE and raises a security event; the user sees "This device or location isn't approved for content work". | MUST |
| PRD-CAP-16 | GAP Capability entry fields: audit identifier, role, subject scope (taxonomy subject identifiers), language scope (BCP 47 tags), accessibility qualification with credential reference, issuing authority, valid from, valid to, revoked at, revocation reason, created by, audit references. Entries are append-only with supersession; renewals create a new entry. | MUST |
| PRD-CAP-17 | GAP A valid token with no capability entry, or a role claim matching no known role, lands on a "Not provisioned — contact your administrator" screen; access is denied and a security event raised. | MUST |
| PRD-CAP-18 | GAP Authorization reads the registry on every request. Any cache is at most 5 seconds and is invalidated synchronously on revocation, so CAP-10 holds. An hourly sweep marks expired entries, flags their in-flight assignments on the coordinator board, and leaves recorded decisions untouched. | MUST |
| PRD-CAP-19 | GAP D-05 Registry maintenance (create, renew, revoke) is performed by the Coordinator role with re-authentication and is fully audited. The identity provider remains the identity authority; the registry never stores names, emails or credentials beyond the pseudonym mapping table. | MUST |

#### Acceptance criteria

- Sign-in from a workstation without a valid device certificate, or with a stale posture assertion, is refused before any content surface loads, and a security event reaches the monitoring platform. 
- Revoking a reviewer's entry while their review workspace is open causes the very next request from that workspace to be denied with `FORBIDDEN_CAPABILITY_EXPIRED`; the decision they recorded a minute earlier remains valid. 
- A user holding Author and Reviewer entries who authored version V cannot record a decision on V through the interface or through a hand-crafted API call. 

## 6.3 Work assignment and My Work

Assignment is cross-cutting: it is the only way any workforce user reaches any version. The specification states the policy inputs; this section states the algorithm.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM03-REV-01 | Submitted versions are assigned to eligible reviewers by system policy using subject, language, workload, recognized capability and separation of duties. Authors cannot nominate reviewers. | MUST |
| ASM03-REV-08 | An open question or artefact is locked to the assigned reviewer. A second actor attempting a decision on an already-decided version is rejected with a clear message. | MUST |
| ASM03-REV-09 | Tasks expire after a configured period and return to the assignment pool. Aging is visible to coordinators. | MUST |
| UI-02 | My Work shows assigned tasks with type, cycle, subject, language, state, age and deadline. No unassigned content is reachable. | MUST |
| UI-03 | A task becoming available is actively surfaced to the assignee; work does not sit unannounced in a queue nobody is prompted to check. | MUST |
| PRD-ASG-01 | GAP Task types: author_primary, review, accessibility_check, translate, translation_review, revalidate_variant, correct_primary. Each maps to exactly one role. | MUST |
| PRD-ASG-02 | GAP Assignment record: identifier, task type, user audit identifier, subject reference (version, lineage or artefact), cycle, language, created at, expires at, status (Active, Completed, Released, Expired, Reassigned), release reason, policy version used. Assignments are append-only; reassignment closes one and opens another. | MUST |
| PRD-ASG-03 | GAP Eligibility: a current, non-revoked capability entry whose role matches the task type and whose subject and language scope cover the artefact; accessibility qualification for accessibility tasks; no separation-of-duties conflict (§4.4); open-task workload below the configured cap D-13. The version's author can never be in the pool for that lineage. | MUST |
| PRD-ASG-04 | GAP Selection is deterministic: lowest current open workload first, then longest time since last assignment, then stable ordering by audit identifier. The policy version and the candidate count are recorded on the assignment. A coordinator's manual assignment must pass the same eligibility check server-side. | MUST |
| PRD-ASG-05 | GAP When no eligible user exists the task stays Unassigned, appears on the coordinator board immediately, and raises an operational alert after the configured delay D-12. | MUST |
| PRD-ASG-06 | GAP Expiry: an assignment past its deadline is released to the pool by a sweep running at least every 5 minutes, audited, and shown in coordinator aging. The version's state is unchanged. A decision recorded before expiry is never voided. | MUST |
| PRD-ASG-07 | GAP Surfacing (UI-03): a new or returned task is pushed to the assignee's open My Work screen over the server-push channel and shown as an in-app notification badge. Any out-of-band notification channel D-19 carries only "You have a new task" and a link — no artefact identifier, subject or content (DAT-03). | MUST |
| PRD-ASG-08 | GAP Locking (REV-08): opening a review or accessibility task records the opening time; a decision is accepted only from the assignee and only while the version is still in the decided-from state. A second decision on an already-decided version returns CONFLICT_ALREADY_DECIDED and the caller's queue refreshes. | MUST |
| PRD-ASG-09 | GAP When an assignee leaves or loses recognized capability mid-task, the assignment is released to the pool by the next request or the sweep, whichever is first; no task is orphaned; decisions already recorded remain valid. | MUST |
| PRD-ASG-10 | GAP Different reviewer after rejection (engineering PRD): the successor version of a rejected version is assigned, at the same stage, to a reviewer other than the one who rejected it and other than any earlier rejecting reviewer of that lineage. If no other eligible reviewer exists the task stays Unassigned and the Admin is alerted; the Admin cannot override this rule. | MUST |
| PRD-ASG-11 | GAP Task types are extended for the converged workflow: accessibility_remediation (Accessibility Specialist) is distinct from accessibility_review (Accessibility Reviewer); the Admin's assignment board shows both. | MUST |

#### Acceptance criteria

- Submitting a version produces a review assignment within 5 seconds to an eligible reviewer who did not author it, and that reviewer's open My Work updates without a reload. 
- Two reviewers open the same task; the first decision succeeds, the second receives `CONFLICT_ALREADY_DECIDED` and sees the task leave their list. 
- An assignment past its expiry appears in coordinator aging, is audited as expired, and is picked up by the next eligible reviewer. 

## 6.4 Authoring · ASM03-ATH

Implements the authoring half of ASM-03: writing the question inside a hardened editor from which nothing can leave. In V1 the Admin is the only author; a draft may be written by hand or arrive as a generated candidate (§2.7, D-38) — the pipeline treats both identically from the first autosave onward.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM03-ATH-01 | An author sees only draft questions and the minimum metadata needed to act. There is no browsable artefact repository. | MUST |
| ASM03-ATH-02 | The editor creates a single-select multiple-choice artefact with a stem, 2 – 8 unique non-empty options, exactly one correct option, an explanation, and all required classification and marking metadata. | MUST |
| ASM03-ATH-03 | Classification is captured against the current syllabus version and taxonomy: subject, unit, topic, difficulty and taxonomy level. | MUST |
| ASM03-ATH-04 | Content supports sanitized restricted HTML, full Unicode, sub- and superscript, lists, accessible tables, and canonical LaTeX rendered through the shared reference renderer. | MUST |
| ASM03-ATH-05 | The editor autosaves at least every 15 seconds and on field exit, and always displays saved, pending or failed status. | MUST |
| ASM03-ATH-06 | Draft writes require an optimistic-concurrency token. A stale write is rejected and never overwrites newer content. | MUST |
| ASM03-ATH-07 | Preview uses the same rendering contract as review, accessibility check and downstream delivery. | MUST |
| ASM03-ATH-08 | Images are supported in stem, options and explanation. Every meaningful image requires alternative text; decorative images require an explicit flag. | MUST |
| ASM03-ATH-09 | Equations are stored as canonical LaTeX and rendered to an accessible representation. | MUST |
| ASM03-ATH-10 | The interface exposes no download, print, bulk export or persistent browser-storage capability. Every artefact is stored on the server immediately, leaving no residual copy on the author's machine. | MUST |
| ASM03-ATH-11 | An author can withdraw an unsubmitted draft; withdrawal is audited and removes it from active counts. | MUST |
| ASM03-ATH-12 | A per-author artefact cap is configurable per cycle. Reaching the cap blocks new creation and is visible to the coordinator. | MUST |
| ASM03-ATH-13 | Every resource an author needs is built into the authoring tool — reference material, symbol and equation palettes, and the approved glossary. The author is never required to leave the tool, and no external source is reachable from it. | MUST |
| PRD-ATH-14 | GAP D-11 Proposed field limits, measured on text after markup is stripped: stem ≤ 4,000 characters; each option ≤ 1,000; explanation ≤ 6,000; alternative text 3 – 300 characters; at most 6 images per version; each image ≤ 2 MB and ≤ 4,000 × 4,000 pixels; total asset budget ≤ 8 MB per version. Limits are configuration with these defaults and are enforced server-side with field-level errors. | MUST |
| PRD-ATH-15 | GAP Content model of a version: stem; ordered options, each with a structural identifier, a body and a correct flag; explanation; classification (subject, unit, topic, difficulty as proposed by the author, taxonomy level); marks; assets with checksum, alternative text and decorative flag. Stem, option bodies and explanation are restricted-HTML documents in which equations are inline equation nodes holding canonical LaTeX and images are asset references. | MUST |
| PRD-ATH-16 | GAP D-09 Restricted-HTML allowlist (SEC-10). Elements: p, br, strong, em, u, s, sub, sup, ul, ol, li, table, caption, thead, tbody, tr, th, td, img, span, eq. Attributes: th[scope], td&#124;th[colspan&#124;rowspan ≤ 8], img[src (asset: scheme only), alt, data-decorative], ol[start], span[dir, lang], eq[data-latex]. No hyperlinks, no style attributes, no event handlers, no comments, no scripts, no external URL scheme of any kind. Sanitization removes anything else and reports each removal to the author as a warning; the sanitized form is what is validated, previewed and stored. | MUST |
| PRD-ATH-17 | GAP D-10 Permitted LaTeX subset (SEC-10): arithmetic and relations; \frac, \sqrt[n]{}, superscript and subscript; Greek letters; \sin \cos \tan \log \ln \exp \lim \sum \prod \int with limits; \left \right with round, square and brace delimiters and vertical bars; \vec \hat \bar \overline \dot; \text{}; pmatrix, bmatrix and cases up to 6 × 6; aligned up to 6 lines; the operator symbols \cdot \times \div \pm \mp \le \ge \ne \approx \equiv \infty \to \in \notin \subset \subseteq \cup \cap \forall \exists \partial \nabla \degree \angle \perp \parallel; spacing commands. Prohibited: any macro definition (\def, \newcommand, \let), file or catcode commands, \href \url, colour commands, raw HTML. Bounds: 2,000 characters, nesting depth 12, 200 ms render budget per equation. Anything outside is rejected with a bounded-subset message and no unbounded rendering work is performed. | MUST |
| PRD-ATH-18 | GAP Reference renderer: one versioned rendering component, executed server-side, produces the semantic HTML with MathML and text alternatives that preview, review, accessibility check, sealing and downstream delivery all use. Its renderer_version is recorded on every decision and in every manifest. A difference in output between author preview and review for the same canonical content is a defect, not a variance. | MUST |
| PRD-ATH-19 | GAP Autosave protocol: save 2 seconds after the last change, at least every 15 seconds while dirty, and on field exit; each save sends the concurrency token and receives the next one; status shows Saved, Saving… or Failed (retrying); a stale-token rejection reloads the server copy and shows the author what differs without discarding their unsaved text. The client keeps draft state in memory only — never in persistent browser storage (ATH-10). | MUST |
| PRD-ATH-20 | GAP D-20 Forced re-authentication: when the refresh window has expired, the client attempts one immediate autosave, then redirects to sign-in with the unsaved state held in memory for the same tab; on return the draft is reloaded from the server and any surviving unsaved text is offered for re-application. Loss is bounded by the autosave interval (≤ 30 s, §11). | MUST |
| PRD-ATH-21 | GAP D-21 The hardened editor region is visually marked. Inside it copy, cut, paste, drag-and-drop of text, context menu and print are blocked and reported (§6.14). Text selection remains possible for editing. The user receives non-blocking feedback that the action was blocked and recorded. | MUST |
| PRD-ATH-22 | GAP Author cap counting: drafts plus submitted versions authored in the cycle, excluding Withdrawn versions and excluding successor drafts created by a return. Reaching the cap returns AUTHOR_CAP_REACHED on create; the coordinator sees per-author counts against the cap. | MUST |
| PRD-ATH-23 | GAP In-tool resources (ATH-13): a read-only reference-material viewer for documents loaded by Content Operations; a Unicode symbol palette organized by category; an equation palette of templates drawn only from the permitted subset; the approved glossary per language, searchable. All are served by the application from its own store; no outbound link exists anywhere in the tool. | MUST |
| PRD-ATH-24 | GAP Scripts and direction: every text field accepts full Unicode, supports right-to-left direction per field, and round-trips the pilot scripts without loss through sanitization, canonicalization and rendering. | MUST |
| PRD-ATH-25 | GAP D-38 Generated candidates: a generation request by the Admin (curriculum, cycle, question type, marks, required count × candidate multiplier) produces independent artefacts, each with one DRAFT of provenance generated, owned by the requesting Admin. Every generated draft records generation identifier, model identifier, generation configuration, source curriculum, chapter, page range, stored source context, and timestamp. A generated draft that fails the automated validation catalogue (§6.5) is discarded before any human sees it. Generated drafts are never grouped as alternatives of one question. The generation service runs outside the hardened zones and never receives content from the pipeline. | MUST |
| PRD-ATH-26 | GAP Metadata (engineering PRD §9.2): in addition to classification, a version carries grade, curriculum reference, learning objective, competency, question type, language, source curriculum, chapter, page range and source context, status, version number, created and updated timestamps, and — where generated — generation identifier, model and configuration. Source context text is Restricted and is never shown to reviewers (D-47). | MUST |
| PRD-ATH-27 | GAP D-44 Question types: single-select multiple choice is fully supported. Other types the blueprint may name (for example short answer) are stored with the same content model minus options, and may enter the pipeline only when the cycle enables them; the validation and structural rule sets for such types are reduced accordingly and named per type. | SHOULD |

#### Acceptance criteria

- A representative author creates, validates, previews, autosaves and submits a question with an image, a table and two equations without assistance (Week 2 closure). 
- A stale write is rejected with `CONFLICT_STALE_WRITE` and no data is lost; a page refresh restores the same draft state. 
- Pasting into the stem is blocked, the author sees the blocked notice without losing focus, and the event appears on the operator surface within 3 seconds. 
- An equation using `\newcommand` is rejected with a message naming the bounded subset; a 6 × 6 matrix renders within budget. 

## 6.5 Validation and submission · ASM03-VAL

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM03-VAL-01 | Validation is deterministic and rule-based only. It performs schema, answer, taxonomy, asset, equation, prohibited-markup, accessibility-completeness and within-artefact duplicate checks. | MUST |
| ASM03-VAL-02 | Blocking findings prevent submission; each is reported against the specific field with actionable text. | MUST |
| ASM03-VAL-03 | Validation causes no state change and calls no probabilistic or external inference service. | MUST |
| ASM03-VAL-04 | Submission creates an immutable version and a content hash. Subsequent editing cannot alter the version under review. | MUST |
| ASM03-VAL-05 | The author receives a submission confirmation of the question. | MUST |
| ASM03-VAL-06 | Submission runs a deterministic similarity check of the stem and options against every sealed question in the question bank. A match above the configured threshold is a blocking finding naming the matched identifiers. The comparison uses normalized text and is rule-based; no model is involved. | MUST |
| PRD-VAL-07 | GAP The validation rule catalogue below is the complete set for the MVP. Each rule has a stable code, a severity (blocking or warning), and reports the field path it applies to. The rule-set version is recorded with every validation report. | MUST |
| PRD-VAL-08 | GAP A validation report is returned to the client and stored with the submission as evidence: rule-set version, renderer version, and one entry per finding with code, severity, field path and message. Validation is a pure function of the draft and the configuration. | MUST |
| PRD-VAL-09 | GAP D-08 Similarity check design (VAL-06): text is normalized (markup stripped, equations reduced to their LaTeX text, Unicode NFC, case-folded, punctuation removed, whitespace collapsed) and tokenized into words; the fingerprint is the set of 64-bit hashes of word 3-grams over stem plus options. At sealing, the fingerprint of every sealed version is stored in the bank index as Restricted derived data D-31. At submission, the candidate's fingerprint is compared by Jaccard similarity against every sealed fingerprint in the same language across the whole bank; a result at or above the threshold (proposed 0.80) is a blocking VAL-SIM-01 naming the matched artefact identifiers. The computation is exact and reproducible. | MUST |
| PRD-VAL-10 | GAP Submission transaction: validate → sanitize and canonicalize (§8.4) → compute content hash → create the immutable version snapshot in state In Review → persist the validation report and similarity result → write the audit event → enqueue domain events in the transactional outbox → return the receipt (version identifier, content hash, submission time, rule-set version). If the audit store is unavailable the submission fails closed (ASR01-EVD-07). | MUST |
| PRD-VAL-11 | GAP Submission is idempotent: repeating it with the same draft concurrency token returns the original receipt and creates no second version. | MUST |

### Validation rule catalogue

| Code | Check | Severity | Field |
| --- | --- | --- | --- |
| VAL-SCHEMA-01 | Stem, at least two options, explanation and classification are present and non-blank after markup is stripped. | Blocking | each missing field |
| VAL-OPT-01 | Option count is between 2 and 8. | Blocking | options |
| VAL-OPT-02 | Options are unique after normalization (NFC, case fold, whitespace collapse, markup strip). | Blocking | options[n] |
| VAL-OPT-03 | No option is identical to the stem or to the explanation (within-artefact duplicate). | Blocking | options[n] |
| VAL-ANS-01 | Exactly one option is flagged correct. | Blocking | options |
| VAL-TAX-01 | Subject, unit and topic are present and belong to the cycle's syllabus version. | Blocking | classification |
| VAL-TAX-02 | No selected node is retired at submission time. | Blocking | classification.* |
| VAL-TAX-03 | Difficulty and taxonomy level are values of the current controlled vocabularies. | Blocking | classification.* |
| VAL-HTML-01 | Content conforms to the restricted allowlist; the sanitized form equals the submitted form. | Blocking | field with prohibited markup |
| VAL-EQN-01 | Every equation parses within the permitted LaTeX subset. | Blocking | field, equation index |
| VAL-EQN-02 | Every equation is within length, depth and render-time bounds. | Blocking | field, equation index |
| VAL-ASSET-01 | Every referenced asset exists, belongs to this version, and has scan status clean. | Blocking | assets[n] |
| VAL-ASSET-02 | Every image has non-empty alternative text or an explicit decorative flag, never both. | Blocking | assets[n].alt |
| VAL-ASSET-03 | Image count and total asset budget are within limits. | Blocking | assets |
| VAL-A11Y-01 | Every table has header cells with scope and a caption; no header cell is empty. | Blocking | field, table index |
| VAL-A11Y-02 | Alternative text is not the file name and is not identical to the stem. | Warning | assets[n].alt |
| VAL-LEN-01 | Every field is within its configured length limit. | Blocking | field |
| VAL-MARK-01 | Marks satisfy the marking policy referenced by the cycle. | Blocking | marks |
| VAL-SIM-01 | Similarity to any sealed artefact in the bank is below the configured threshold; otherwise the finding names the matched identifiers. | Blocking | stem, options |
| VAL-VAR-01 | (Variants) Every target-language field is non-empty and every structural check in §6.8 passes or is covered by an active exception. | Blocking | named check |
| VAL-WARN-01 | Stem does not end with a question mark or an imperative instruction. | Warning | stem |
| VAL-WARN-02 | Longest option is more than three times the length of the shortest. | Warning | options |
| VAL-WARN-03 | An option matches an "all of the above" or "none of the above" pattern in the cycle's primary language. | Warning | options[n] |

#### Acceptance criteria

- Every blocking rule in the catalogue has an automated test that produces the finding against the named field and an automated test that passes when corrected. 
- A near-duplicate of a seeded bank question is refused at submission naming the matched identifier; a question sharing only common phrasing is not. 
- A submitted version's content hash equals the hash recomputed from its stored canonical bytes; editing the successor draft leaves the hash unchanged. 

## 6.6 Question review · ASM03-REV

Implements the review half of ASM-03: an independent Question Reviewer assesses the exact submitted version, comments, and either approves it or rejects it with findings. "Return" in the specification is "Reject" in the engineering PRD; the two words mean the same transition.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM03-REV-02 | The review workspace is read-only and shows the exact submitted version, its content hash, permitted metadata and a mandatory structured checklist. | MUST |
| ASM03-REV-03 | No review endpoint accepts content fields. Direct editing is never offered. | MUST |
| ASM03-REV-04 | The reviewer validates correctness and checks the classification, difficulty and taxonomy level assigned by the author against the syllabus version in force. | MUST |
| ASM03-REV-05 | Approval requires a complete checklist. Return requires a reason code and actionable comments. | MUST |
| ASM03-REV-06 | Approval moves the exact version to accessibility check. A return creates a new linked draft carrying the findings; the returned version remains as immutable evidence. | MUST |
| ASM03-REV-07 | Decisions are append-only and bind the checklist, rationale, reviewer audit identifier, duration and version hash. | MUST |
| ASM03-REV-10 | Whether one or two independent reviews are required before approval is configuration, not code. | MUST |
| ASM03-REV-11 | The reviewer records an explicit attestation, inside the mandatory checklist, covering three checks: language and grammatical correctness; that the artefact is not available in the public domain; and that it complies with the prescribed guidelines and curriculum scope for the cycle. Each is recorded separately with the source consulted, not as a single combined tick. | MUST |
| ASM03-REV-12 | The reviewer assigns a difficulty value from the controlled vocabulary at the point of approval. The field for discrimination is created and left empty; it is populated only from candidate performance data after an exam and is never estimated. | MUST |
| PRD-REV-13 | GAP D-19 The structured checklist is a configured template per cycle with the items listed below. Every item is Pass, Fail or Not applicable (with a reason). Approval requires every item Pass or Not applicable and all three attestations complete with a source. The equivalence-judgement item appears only for variants. | MUST |
| PRD-REV-14 | GAP D-19 Return reason codes are a controlled vocabulary (below). A return requires one code and comments of at least 20 characters; the controls stay disabled until both are satisfied. | MUST |
| PRD-REV-15 | GAP Decision record fields: identifier; version identifier and version hash; decision type (review, translation review, accessibility); outcome; checklist responses; attestations with sources; reason code; comments; difficulty assigned; equivalence judgement; reviewer audit identifier; capability entry identifier valid at the time; renderer version; policy version; opened at; decided at; duration; correlation identifier. The record's own hash is written into the audit event. | MUST |
| PRD-REV-16 | GAP Two-review policy (REV-10): when the cycle requires two reviews, the version stays In Review until two approvals from different, duty-clean reviewers exist; the second reviewer cannot see the first reviewer's checklist until their own decision is recorded; a single return sends the version back regardless of other approvals. | MUST |
| PRD-REV-17 | GAP A return creates the successor Draft with derived_from set, attaches the findings so they appear inside the editor beside the fields they name, and assigns the draft to the original author, or to the pool if that author is no longer eligible. | MUST |
| PRD-REV-18 | GAP D-06 Correct-answer visibility in review is governed by the cycle flag reviewer_sees_key (SEC-02). Proposed default: true, because validating correctness (REV-04) requires knowing the key. When false, the reviewer is asked to identify the key and the workspace records whether it matched. | MUST |
| PRD-REV-19 | GAP Reviewer isolation (engineering PRD §10, §20, adopted verbatim). The review workspace shows the reference rendering, the content hash, and only the metadata needed to evaluate the question: subject, grade, curriculum name, question type, marks, Bloom's level, difficulty, language, version number, submission time, the validation warnings, and the source chapter and page range for grounding checks (D-47). It never shows: assessment name, title or identifier; final question number; other questions in any assessment; candidate-pool membership or selection status; which users reviewed the question or any other reviewer; the audit history; the author's identity or pseudonym; the stored source context text. The artefact identifier QB-nnnnn is not a question number and reveals no assessment context. | MUST |
| PRD-REV-21 | GAP Comments: every review role may add free-text comments to its decision; comments are Restricted, visible to the Admin and carried into the successor draft, and never visible to any other reviewer (engineering PRD). | MUST |
| PRD-REV-20 | GAP The worklist locks to the open task until a decision is recorded, then advances to the next assigned task (UI-07). Leaving the workspace without deciding keeps the assignment active and records the duration so far. | MUST |

### Review checklist template (proposed, D-19)

| Item | Statement the reviewer confirms | Evidence captured |
| --- | --- | --- |
| R1 | The stem is unambiguous and asks exactly one thing. | Pass / Fail / N/A |
| R2 | Exactly one option is defensibly correct, and it is the flagged key. | Pass / Fail |
| R3 | Every distractor is plausible and unambiguously incorrect. | Pass / Fail |
| R4 | Subject, unit and topic are correct against the syllabus version in force. | Pass / Fail |
| R5 | The taxonomy level is appropriate for the cognitive demand of the item. | Pass / Fail |
| R6 | The explanation is correct and sufficient for a candidate to learn from. | Pass / Fail / N/A |
| R7 | Images, tables and equations render correctly and are necessary to answer. | Pass / Fail / N/A |
| A1 | Attestation: language and grammar are correct for the target register. | Confirmed + source consulted (style guide reference) |
| A2 | Attestation: the item is not available in the public domain. | Confirmed + sources consulted from the curated reference list |
| A3 | Attestation: the item complies with the prescribed guidelines and curriculum scope for the cycle. | Confirmed + guideline reference |
| D1 | Difficulty assigned from the controlled vocabulary. | Value (required at approval) |
| E1 | (Variants only) The variant is neither easier nor harder than the primary. | Judgement: equivalent / not equivalent + note |

### Return reason codes (proposed, D-19)

| Review | Accessibility | Translation review |
| --- | --- | --- |
| RC-INCORRECT-KEY, RC-AMBIGUOUS-STEM, RC-MULTIPLE-CORRECT, RC-WEAK-DISTRACTOR, RC-CLASSIFICATION, RC-TAXONOMY-LEVEL, RC-LANGUAGE, RC-PUBLIC-DOMAIN, RC-OUT-OF-SCOPE, RC-ASSET, RC-EQUATION, RC-EXPLANATION, RC-OTHER | RC-A11Y-ALT-TEXT, RC-A11Y-CONTRAST, RC-A11Y-READING-ORDER, RC-A11Y-TABLE, RC-A11Y-EQUATION, RC-A11Y-VISUAL-ONLY, RC-A11Y-PLAIN-LANGUAGE, RC-A11Y-FOCUS-KEYBOARD, RC-A11Y-FONT, RC-A11Y-OTHER | RC-TRN-FIDELITY, RC-TRN-TERMINOLOGY, RC-TRN-GRAMMAR, RC-TRN-ANSWER-EQUIV, RC-TRN-DIFFICULTY-SHIFT, RC-TRN-LOCKED-VALUE, RC-TRN-OTHER |

#### Acceptance criteria

- Approval with any checklist item unanswered or any attestation without a source is refused server-side with field-level detail. 
- A return produces a new Draft carrying the findings; the returned version's hash, state and decision are unchanged afterwards. 
- A multi-role user is refused approval of their own work through the interface and through a hand-crafted API call. 
- Keyboard-only and screen-reader review of the workspace passes (Week 3 closure). 

## 6.7 Accessibility remediation and review · ASM04-ACC

Implements CND-02 Accessibility and accommodations at artefact level, and the accessibility half of ASM-04 Language and variants. Following the engineering PRD, accessibility is two roles: the Accessibility Specialist remediates the question on an accessibility draft and completes the task; the Accessibility Reviewer tests the same reference rendering intended for candidate delivery and approves or rejects. The specification's "accessibility specialist" requirements below therefore bind the Accessibility Reviewer where they concern the decision, and the Accessibility Specialist where they concern remediation.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM04-ACC-01 | The accessibility specialist tests the same reference rendering intended for downstream candidate delivery, in a read-only mode that cannot alter content. | MUST |
| ASM04-ACC-02 | The workspace provides keyboard and screen-reader test affordances against the rendered artefact. | MUST |
| ASM04-ACC-03 | Evaluation covers screen-reader compatibility, alternative text, colour contrast, font readability, plain-language clarity, reading order, focus, keyboard operation, tables, equations, and whether the artefact relies solely on visual or auditory cues. | MUST |
| ASM04-ACC-04 | Approval requires no unresolved blocking findings and mandatory comments. A return records the affected element and the required remediation. | MUST |
| ASM04-ACC-05 | Approval requests sealing into the repository. A return creates a new linked draft. | MUST |
| ASM04-ACC-06 | Whether remediation repeats review is policy-driven configuration, defaulting to repeat when content, answer or metadata changed. | MUST |
| ASM04-ACC-07 | The decision records which of the cycle's declared accommodations the rendered artefact can be delivered under. | MUST |
| ASM04-ACC-08 | An artefact that cannot be delivered under a declared accommodation is recorded as needing an equivalent route, with a reason, and is escalated rather than silently approved. | MUST |
| ASM04-ACC-09 | Generation of alternate-format artefacts is out of scope; the data model must not preclude it. | MAY |
| PRD-ACC-10 | GAP The evaluation checklist implements ACC-03 item by item (table below). Each item is Pass, Fail (with at least one finding) or Not applicable (with reason). | MUST |
| PRD-ACC-11 | GAP A finding records: element reference (structural identifier or field path), criterion, severity (blocking or advisory), description, required remediation. A return requires at least one blocking finding; an approval requires zero unresolved blocking findings and comments of at least 20 characters. Advisory findings travel to the successor draft as guidance without blocking. | MUST |
| PRD-ACC-12 | GAP D-17 Accommodation capability: for every accommodation declared by the cycle the decision records deliverable or needs equivalent route with a reason. Any needs equivalent route creates an escalation task for the coordinator with an operational alert. Proposed default: the flag does not block sealing or readiness; it is carried on the readiness record so assembly can respect it. | MUST |
| PRD-ACC-13 | GAP Test affordances (ACC-02) provided on the reference rendering without altering content: keyboard-only navigation mode with visible focus order; screen-reader-oriented view exposing the accessible name, role and MathML of each element; text-only view; zoom at 200 % and 400 %; contrast measurement per text element; a reading-order outline. | MUST |
| PRD-ACC-14 | GAP D-07 Remediation routing policy values: always_repeat_review, repeat_when_content_changed (default), never_repeat. "Changed" is defined in §5.4. | MUST |
| PRD-ACC-15 | GAP To honour ACC-09, renditions are modelled as a separate entity keyed by version, format and status, with the reference rendering as the first format. No code path assumes a single format. | MUST |
| PRD-ACC-16 | GAP Accessibility remediation task (engineering IN_ACCESSIBILITY): on question-review approval the system creates an accessibility draft derived from the approved version and assigns an Accessibility Specialist by policy. The draft exposes only accessibility fields: alternative text and decorative flags, table headers and captions, equation text alternatives, reading-order markup and accessibility metadata. Stem, options, correct flag, explanation, marks, classification, image bytes and mathematical notation are locked and machine-verified unchanged on completion. The specialist completes the evaluation checklist as a self-check, may comment, and completes the task, which creates the immutable version that enters IN_ACCESSIBILITY_REVIEW. | MUST |
| PRD-ACC-17 | GAP A finding that needs an authoring change (wording, image, notation) is recorded by the specialist as a comment and by the reviewer as an RC-A11Y-* rejection to the author; the specialist never edits those fields. | MUST |
| PRD-ACC-18 | GAP The Accessibility Reviewer decides on the completed accessibility version: approval requests sealing; rejection creates an accessibility-correction draft for a different Accessibility Specialist (accessibility findings) or an authoring-correction draft for the author (authoring findings), and the next accessibility review is by a different Accessibility Reviewer (PRD-ASG-10). | MUST |
| PRD-ACC-19 | GAP D-43 Every language version — the primary and each variant — has its own remediation task and review (ASM04-TRN-05). For variants the remediation is normally limited to translated alternative text and captions. | MUST |

### Accessibility evaluation checklist

| Criterion | Pass means | Typical remediation recorded |
| --- | --- | --- |
| Screen-reader compatibility | Every element is announced with a correct name and role in a sensible sequence. | Restructure markup; add table headers; replace visual-only layout. |
| Alternative text | Every meaningful image's alternative text conveys what a sighted candidate gains; decorative images are flagged. | Rewrite alternative text; flag as decorative. |
| Colour contrast | All text in the reference rendering meets WCAG 2.1 AA contrast; no meaning is carried by colour alone. | Image re-authoring; textual cue added. |
| Font readability | Text inside images is legible at 200 % or is duplicated in text. | Provide text equivalent. |
| Plain-language clarity | The stem and options avoid unnecessary complexity for the target level. | Simplify wording (returned to author). |
| Reading order | The DOM order matches the intended reading order. | Reorder content. |
| Focus | Focus is visible and moves predictably through options. | Renderer defect — raised as a defect, not a finding. |
| Keyboard operation | Every option can be reached and selected by keyboard alone. | Renderer defect. |
| Tables | Headers, scope and caption make the table navigable. | Add caption or headers. |
| Equations | MathML and the text alternative read correctly in a screen reader. | Rewrite equation; add text alternative. |
| Sole reliance on visual or auditory cues | The item can be answered without sight or hearing given the declared accommodations. | Record equivalent-route need; escalate. |

#### Acceptance criteria

- An approval records a deliverable / equivalent-route value for every accommodation declared by the cycle; omitting one is refused. 
- Marking any accommodation as needs equivalent route creates a coordinator escalation and an alert; the artefact is not silently approved. 
- A return names the affected element and required remediation, and the successor draft shows them beside the element. 

## 6.8 Translation and variant equivalence · ASM04-TRN

Implements the language half of ASM-04: every language version must be as hard as the original, not harder, not easier. Exceptions implement the MVP's portion of ASR-04.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM04-TRN-01 | Sealing the primary version creates one question or artefact per required language. | MUST |
| ASM04-TRN-02 | Translators edit only target-language fields, besides a read-only primary reference and the supplied glossary. | MUST |
| ASM04-TRN-03 | Option mapping, correct-answer semantics, marks, assets, equations and structural identifiers are locked and machine-verified on submission. | MUST |
| ASM04-TRN-04 | Each language variant is reviewed independently for fidelity, terminology, script-specific grammar and answer equivalence. | MUST |
| ASM04-TRN-05 | Each language variant receives its own accessibility check and its own sealed artefact. | MUST |
| ASM04-TRN-06 | Deterministic checks run on submission and block it where the variant diverges structurally from the primary: option count and mapping, correct-answer position, marks, asset set, canonical equation set, and every numeric value, unit and symbol. | MUST |
| ASM04-TRN-07 | The reviewer records an explicit judgement that the variant is neither easier nor harder than the primary, inside the existing mandatory checklist. No separate workflow step and no additional lifecycle state is introduced. | MUST |
| ASM04-TRN-08 | A blocked structural check can be overridden only by a recorded exception carrying justification and an expiry date, consistent with ASR-04. The override is audited. | MUST |
| ASM04-TRN-09 | When the primary changes, dependent variants are marked as requiring revalidation and the translator is shown what changed. | MUST |
| ASM04-TRN-10 | Coordinators see language status and artefact ownership, never sealed content. | MUST |
| PRD-TRN-11 | GAP Variant creation is part of the primary's sealing transaction. For each required language a new lineage and Draft are created with: empty target-language stem, option bodies, explanation and alternative text; locked fields copied from the primary (option identifiers and order, correct flag, marks, assets by checksum, canonical equations, classification); primary_reference_hash; and a read-only primary reference snapshot holding the primary's rendering and canonical text, classified Restricted and visible only to the assigned translator and translation reviewer. A translation assignment is created by policy. The snapshot is purged when the variant is sealed. | MUST |
| PRD-TRN-12 | GAP D-23 The translation editor exposes only translatable text: stem, option bodies, explanation, alternative text, table cell text and captions. Numbers, units, symbols, equations and image references appear as locked tokens that cannot be edited or removed. Proposed default: numeric values are preserved verbatim (no localized numerals); an exception is the only route to change one. | MUST |
| PRD-TRN-13 | GAP Structural check catalogue (TRN-06), each blocking and named in the response: STR-01 option count equal; STR-02 option identifier set and order equal; STR-03 correct-answer position equal; STR-04 marks equal; STR-05 asset set by checksum equal; STR-06 canonical equation multiset equal; STR-07 numeric value multiset equal (numbers including decimals, negatives and percentages, extracted by a fixed grammar); STR-08 unit multiset equal (from a maintained unit lexicon); STR-09 symbol multiset equal (non-alphabetic Unicode symbols from a fixed set); STR-10 table dimensions equal; STR-11 every primary image has alternative text in the variant unless decorative. | MUST |
| PRD-TRN-14 | GAP D-15 Exception record: identifier; version identifier; check codes covered; justification (at least 50 characters); requested by; approved by (a Coordinator, re-authenticated, different from the requester); created at; expires at (at most the configured maximum, proposed 30 days); status Active, Expired, Revoked or Consumed; audit references. Only an Active exception matching the failing check code permits the submission; the exception identifier is recorded on the decision and in the manifest. An hourly sweep expires exceptions. An attempted override without a valid exception returns EXCEPTION_REQUIRED. | MUST |
| PRD-TRN-15 | GAP The translation-review checklist (inside the standard review template) covers fidelity of meaning, glossary terminology, script-specific grammar, answer equivalence (the same option is correct for the same reasons), and the equivalence judgement E1 of §6.6. The reviewer sees the primary reference and the variant side by side, read-only. | MUST |
| PRD-TRN-16 | GAP Revalidation (TRN-09, RES06-COR-03): when a corrected primary is sealed, each variant lineage is flagged requires_revalidation and a revalidate_variant task is created. Its workspace shows a field-level difference between the previous and new primary reference. The translator produces a new variant version bound to the new primary hash; it passes every gate; readiness returns only when every required language is resealed against the new primary. | MUST |
| PRD-TRN-17 | GAP The coordinator's language status view lists, per artefact, each language's state, current assignee and age. It shows names for assignment purposes but never content, never the correct answer, and never a rendering. | MUST |

#### Acceptance criteria

- Sealing a primary in a cycle with two required languages creates exactly two variant drafts with translation assignments; a coordinator sees both languages as "Translation in progress". 
- A variant that changes a numeric value or the position of the correct option is refused at submission naming `STR-07` or `STR-03`; with a valid, unexpired exception covering that code the submission succeeds and the exception identifier appears on the decision and manifest. 
- One primary plus two language variants reach readiness and every manifest verifies (Week 4 closure). 

## 6.9 Sealing and the repository · ASM05-VLT

Implements ASM-05: where approved artefacts are kept, which version is current, and who is allowed near them. Sealing is the system's job and the only way content enters the repository.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM05-VLT-01 | Sealing is a system action. No human role has a discretionary publish control. | MUST |
| ASM05-VLT-02 | The service revalidates approvals, lineage, separation of duties, asset scans, schema and current policy before any write. | MUST |
| ASM05-VLT-03 | Canonical sealing strips comments, author names, revision history, unsafe attributes, source metadata and any field outside the approved schema. | MUST |
| ASM05-VLT-04 | The service produces a SHA-256-or-stronger content hash, encrypts using managed keys, and signs a manifest without persisting raw key material. | MUST |
| ASM05-VLT-05 | On sealing, the artefact is removed from the authoring, review and accessibility environments and indexed in the question bank by classification, complexity level, difficulty and taxonomy level. | MUST |
| ASM05-VLT-06 | Sealing atomically writes the artefact, indexes approved metadata, emits durable audit, and ends routine human access. | MUST |
| ASM05-VLT-07 | Sealing is idempotent and safely retryable. A failure leaves no partially sealed artefact. | MUST |
| ASM05-VLT-08 | Sealed artefacts are immutable and remain encrypted at rest with no plaintext copy accessible to any user or administrator. Which version is current is always resolvable. | MUST |
| PRD-VLT-09 | GAP The sealing pipeline runs the steps below, in order, in a worker under the sealing workload identity (ARC-05), keyed by the version identifier as its idempotency key. | MUST |
| PRD-VLT-10 | GAP Manifest content is specified in §8.6. A manifest is Restricted (DAT-01), stored beside the sealed object and in the database, and its canonical bytes are signed with an asymmetric key held in the key management service. | MUST |
| PRD-VLT-11 | GAP Encryption model: envelope encryption with a fresh 256-bit data key per sealed version (authenticated encryption), the data key wrapped by the active repository-tier key in the key management service. Key policy grants encrypt to the sealing identity only; decrypt to the verification identity (in-memory verification only, no plaintext output), the correction-seeding identity under a recorded authorization (§6.11), and the break-glass identity (§10.6). No human principal and no platform-administrator role holds decrypt. Every key use is logged by the key service and mirrored into audit. | MUST |
| PRD-VLT-12 | GAP Storage: a private object store with no public access, object versioning, retention lock with the period taken from configuration D-24 (DAT-08), provider-side encryption in addition to application-level encryption, and access only through worker identities. Object key: artefact identifier / version identifier / content hash. | MUST |
| PRD-VLT-13 | GAP Bank index row per sealed version: artefact and version identifiers, language, lineage, classification, complexity level, difficulty, taxonomy level, marks, content hash, similarity fingerprint, sealed at, current flag, accommodations deliverable. No content field exists in the index. | MUST |
| PRD-VLT-14 | GAP Post-seal removal (VLT-05): in the sealing transaction the plaintext working copy of the sealed version is deleted from the authoring-tier store and its rendering caches are purged. Returned and Withdrawn versions are not sealed; they remain immutable in the authoring tier, reachable only as findings context by the author of the successor draft and as metadata by auditors. | MUST |
| PRD-VLT-15 | GAP Current-version resolution (VLT-08): the artefact holds one current sealed version pointer per language; the pointer moves and the previous version becomes Superseded inside the same transaction, so a reader never observes two current versions or none. | MUST |
| PRD-VLT-16 | GAP Failure handling: if the key service, audit store, scanner or object store is unavailable, or any revalidation fails, the job is marked failed with a reason code, no state changes, retry uses exponential backoff up to 6 hours, an operational alert fires after the third failure, and operations can replay the job. Because the object key includes the content hash, a retry after a partial object write overwrites the same key and produces exactly one sealed object and one manifest. | MUST |
| PRD-VLT-17 | GAP Progress: the version shows Queued, Sealing, Sealed or Failed (retrying) to the accessibility specialist who approved it and to the coordinator; 95 % of valid image-bearing artefacts seal within 30 seconds (§11). | MUST |

### Sealing pipeline

| Step | Action | Fails closed when |
| --- | --- | --- |
| 1 | Load the version; confirm state is Sealing Requested; if already Sealed with this identifier, return success (idempotent). | State is anything else. |
| 2 | Revalidate: approvals present (review, and for variants translation review, and accessibility); separation of duties across all actors on the lineage; lineage consistent; every asset scan status clean; schema valid; cycle policy version current. | Any check fails — recorded as a sealing failure naming the check. |
| 3 | Expected-evidence assertion (§6.13): every declared record for every completed step exists, is bound to this exact version hash, and was produced by a duty-clean actor. | Any record missing, unbound or mismatched — alert names the step and the absent record. |
| 4 | Canonicalize (§8.4) and strip everything outside the approved schema (VLT-03); recompute the content hash and compare with the hash recorded at submission. | Hash mismatch — treated as tampering, Critical alert. |
| 5 | Compute the similarity fingerprint for the bank index. | — |
| 6 | Generate a data key, encrypt the canonical bytes, wrap the data key with the repository-tier key; write the ciphertext to the object store under retention lock. | Key service or object store unavailable. |
| 7 | Build the manifest (§8.6), canonicalize it, sign it through the key service, store it. | Signing unavailable. |
| 8 | In one database transaction: set state Sealed; move the current pointer and mark the predecessor Superseded; write the bank index row; delete the plaintext working copy; create variant drafts for required languages (primary only); recompute readiness; write the audit event; enqueue version.sealed, readiness.changed and, if applicable, artefact.superseded in the outbox. | Audit store unavailable — the transaction rolls back and the object written in step 6 is superseded by the retry. |
| 9 | Acknowledge the job; a sweep removes orphaned objects whose manifest transaction never committed. | — |

#### Acceptance criteria

- A sealing job replayed three times yields one sealed object, one manifest and one audit event; the version's hash is unchanged. 
- With the key service unavailable, the job fails, the version remains Sealing Requested, nothing is written to the repository, and the retry succeeds after recovery. 
- No human role, including a platform administrator with database and object-store access, can obtain sealed plaintext through any interface; the manifest signature verifies with the public key. 

## 6.10 Readiness and handoff to assembly · ASM07-RDY

Boundary block. This is the outbound edge of the MVP: a metadata-only contract read by a separate assembly service.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM07-RDY-01 | An artefact is ready only when the current primary and every required language variant are sealed against the same lineage. | MUST |
| ASM07-RDY-02 | A machine-only, authenticated, paginated interface exposes opaque identifiers, languages, item type, classification, difficulty, taxonomy level, marking, readiness and sealed references. | MUST |
| ASM07-RDY-03 | The response contains no stem, option, answer, explanation, comment or asset bytes. | MUST |
| ASM07-RDY-04 | Human tokens and wrong-audience workload tokens are rejected by the interface. | MUST |
| ASM07-RDY-05 | Superseded sealed versions remain as evidence but are never returned by new readiness queries. | MUST |
| ASM07-RDY-06 | Where two artefacts must not appear in the same paper, the relationship is recorded and carried on the readiness record. Automated detection of such pairs is out of scope. | SHOULD |
| PRD-RDY-07 | GAP The readiness status values are FULLY_APPROVED (engineering name for ready), NOT_READY and REVOKED. The readiness record schema is fixed in §8.2 and Appendix C. It is computed by the rule in §5.4, stored, and updated inside the transaction that changes any of its inputs, so the interface reads a materialized record rather than computing on request. | MUST |
| PRD-RDY-08 | GAP Interface: GET /assembly/v1/readiness with filters cycle, subject, language, readiness status and updated-since, opaque cursor pagination with a page size of at most 200; GET /assembly/v1/readiness/{artefact_id}. Authentication is mutual TLS plus a short-lived token whose audience is assembly-readiness; any other audience or a human token returns REJECTED_AUDIENCE. Responses are marked no-store and rate-limited per workload identity. | MUST |
| PRD-RDY-09 | GAP D-34 Exclusion pairs (RDY-06): a coordinator records a pair of artefact identifiers with a reason; the pair appears on both readiness records; removal is audited. No detection logic exists. | SHOULD |
| PRD-RDY-10 | GAP Every change of readiness emits readiness.changed with the artefact identifier, previous and new status and the reason (sealed, correction, used, retired, revalidation). | MUST |

#### Acceptance criteria

- A human bearer token and a workload token with a different audience are both refused; the approved identity succeeds and receives metadata only (Week 4 closure). 
- An automated test asserts that no field of any readiness response matches a content field name or a content value from the synthetic corpus. 

## 6.11 Correction and supersession (approval reset) · RES06-COR

Boundary block. Implements RES-06 at artefact level: when something changes after sealing, everyone who relied on it is told. This is the engineering PRD's approval reset: an Admin edit after approval loses the approval state and the full pipeline runs again — here as a new lineage rather than an in-place edit, because sealed and approved versions are immutable.

| ID | Requirement | Priority |
| --- | --- | --- |
| RES06-COR-01 | A correction to a sealed primary requires a recorded authorization and reason. | MUST |
| RES06-COR-02 | A correction creates a new lineage, never overwrites sealed bytes, and immediately revokes readiness. | MUST |
| RES06-COR-03 | Every dependent language variant is marked as requiring revalidation until resealed against the new primary. | MUST |
| RES06-COR-04 | The superseded version records a reference to the version that replaced it. | MUST |
| RES06-COR-05 | Downstream consumers are notified of supersession and must acknowledge. Unacknowledged supersession beyond a configured window raises an operational alert. | MUST |
| RES06-COR-06 | Retiring an artefact preserves its sealed hash and classification so later analysis remains possible. | SHOULD |
| PRD-COR-07 | GAP Correction authorization record: identifier, artefact identifier, sealed version identifier, scope (primary or a named variant), authorized by (Coordinator, re-authenticated), reason of at least 50 characters, created at, audit references. It emits correction.authorized. | MUST |
| PRD-COR-08 | GAP D-16 Correction draft seeding. Because no human can read sealed plaintext, the system creates the correction draft: under the authorization record, the correction-seeding identity decrypts the sealed version in memory, creates a new lineage with a Draft holding that content, and assigns it to an eligible author by policy (the original author is eligible). The sealed bytes are untouched; the draft is Restricted and visible only to the assignee; the audit event records the source version hash and the authorization identifier. This is the only routine path by which sealed content re-enters the authoring tier, and it is a system action, never a read interface. | MUST |
| PRD-COR-09 | GAP Readiness is revoked in the same transaction as the authorization (COR-02), and stays revoked until the new primary and every required variant are sealed against it. The reason is carried on readiness.changed. | MUST |
| PRD-COR-10 | GAP D-25 Supersession notification: sealing the corrected primary marks the previous version Superseded with replaced_by, and the outbox delivers artefact.superseded to every registered consumer over mutual TLS (webhook), at least once with consumer-side deduplication by event identifier. Consumers acknowledge with POST /downstream/v1/supersession-acks carrying the event identifier, consumer identifier and a signature. A notice unacknowledged beyond the configured window (proposed 24 hours) raises an operational alert and appears on the coordinator board until acknowledged. | MUST |
| PRD-COR-11 | GAP Retirement (COR-06): a re-authenticated Coordinator retires an artefact with a reason; every sealed version keeps its hash, manifest and classification; readiness is revoked; artefact.retired is emitted; there is no un-retire in the MVP. | SHOULD |
| PRD-COR-12 | GAP A correction scoped to one variant (a translation defect with a sound primary) creates a new lineage for that language only; the primary and other variants are untouched; readiness is revoked until the variant is resealed against the unchanged primary hash. | MUST |

#### Acceptance criteria

- Authorizing a correction on a ready artefact revokes readiness within the same request and the assembly interface stops returning it as ready on its next call. 
- After the corrected primary seals, the old version reads Superseded with `replaced_by` set, both variants show `requires_revalidation`, and the supersession event reaches the registered consumer; withholding the acknowledgement past the window raises the alert. 

## 6.12 Downstream lifecycle states · ASM06-LFC

Boundary block. Blind assembly is performed by a separate service; this MVP owns the states that service drives inside the question bank.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASM06-LFC-01 | The system accepts a signed selection notification from the assembly service and atomically transitions the primary and every published language variant of the selected artefact to Used. No human actor initiates the transition. | MUST |
| ASM06-LFC-02 | A Used artefact is immutable and is excluded from every subsequent readiness query. One that was not selected remains available in the eligible pool. | MUST |
| ASM06-LFC-03 | On the exam-completion event, every Used artefact in that session transitions atomically to Archived. There is no return path to Published or Used. | MUST |
| ASM06-LFC-04 | Archival writes the exam identifier, the archival timestamp and the artefact-set hash to the audit chain, so a session can be reconstructed evidentially. | MUST |
| ASM06-LFC-05 | Read access to an Archived artefact is limited to audit and dispute roles under the break-glass procedure in §10.6. | MUST |
| ASM06-LFC-06 | Encryption keys rotate from the active tier to the archive tier on archival, and the rotation is recorded. | MUST |
| PRD-LFC-07 | GAP D-26 Selection notification contract: POST /downstream/v1/selection-notifications with body notification identifier, exam session identifier, cycle code, list of selected artefact identifiers with the expected current primary version identifier, and issued-at; a detached signature (JSON Web Signature by the assembly signing key, key identifier included) plus mutual TLS and an audience token. Validation: signature valid against the registered key set; issued-at within 5 minutes of clock skew; notification identifier unused (a replay returns the original result); every artefact ready and its current primary matching the expected version. Proposed default: all-or-nothing per notification — any artefact not ready rejects the whole notification with SELECTION_NOT_READY listing the identifiers. On success one transaction sets the primary and every sealed variant to Used, records the exam session, writes audit events and emits artefact.used. | MUST |
| PRD-LFC-08 | GAP Exam-completion contract: POST /downstream/v1/exam-completions with exam session identifier and completed-at, signed as above. In one transaction every Used artefact of that session becomes Archived and the audit chain receives an event carrying the exam identifier, the timestamp and the artefact-set hash (SHA-256 over the sorted list of sealed content hashes). A key-rotation job then re-wraps each data key with the archive-tier key and records the rotation; until it completes the artefact is Archived with rotation pending, visible to operations. | MUST |
| PRD-LFC-09 | GAP Archived metadata (identifiers, hashes, classification, manifests) remains readable to auditors through the evidence view; content is reachable only through the break-glass procedure. | MUST |
| PRD-LFC-10 | GAP A selection notification naming an artefact that is Used, Archived, Retired or under correction is rejected with a code naming the artefact and its state, and raises an operational alert, because it indicates a stale assembly view. | MUST |

#### Acceptance criteria

- A simulated signed selection notification moves the primary and both variants to Used atomically; a replay returns the same result without a second transition; exam completion moves them to Archived and the audit chain carries the artefact-set hash (Week 4 closure). 
- After archival the wrapped data key references the archive-tier key and the rotation is present in audit. 

## 6.13 Expected evidence and audit · ASR01-EVD

Implements ASR-01: agreeing beforehand what proof each step must produce, so that missing proof is itself a warning.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASR01-EVD-01 | Every material action emits an append-only audit event: actor or service, action, subject and hash, outcome, policy version and correlation identifier. | MUST |
| ASR01-EVD-02 | Events are hash-chained. The chain construction, genesis record and verification procedure are specified and implemented. | MUST |
| ASR01-EVD-03 | Chain verification is runnable on demand and detects any removed or altered event. | MUST |
| ASR01-EVD-04 | Verification succeeds across backup and restore — restored records retain valid event and content hashes. | MUST |
| ASR01-EVD-05 | Each step declares the evidence it must produce. Before sealing, the system asserts that every expected record exists, verifies against the exact version hash, and was produced by an actor with no separation-of-duties conflict. | MUST |
| ASR01-EVD-06 | A missing, unbound or mismatched record blocks sealing and raises an alert naming the step and the absent record. Absence of expected evidence is an alert condition, not a silent pass. | MUST |
| ASR01-EVD-07 | Critical transitions fail closed when durable audit is unavailable. | MUST |
| ASR01-EVD-08 | An evidence view provides read-only audit search by actor, action, artefact and time range, and displays the verification result. (P1 — may reduce to a scripted operator procedure if Week 3 capacity is strained.) | SHOULD |
| ASR01-EVD-09 | Audit events contain no artefact plaintext. | MUST |
| ASR01-EVD-10 | A scheduled sweep re-asserts evidence completeness across sealed versions and alerts on drift. | SHOULD |
| PRD-EVD-11 | GAP Audit event schema (§8.2, Appendix C): event identifier; chain identifier; sequence number; occurred at; actor (type user or service; audit identifier or workload identity); action from the catalogue; subject (type, identifier, version hash where applicable); outcome (success, denied, failed); policy version; correlation and trace identifiers; details as a structured object whose keys are allowlisted per action; previous hash; event hash. The schema forbids additional properties. | MUST |
| PRD-EVD-12 | GAP Action catalogue (minimum): session.signed_in, session.denied, session.signed_out, session.timed_out, cycle.created, cycle.changed, taxonomy.published, taxonomy.node_retired, capability.created, capability.revoked, capability.expired, assignment.created, assignment.released, assignment.expired, assignment.reassigned, artefact.created, draft.saved (aggregated per minute, count only), asset.uploaded, asset.quarantined, asset.rejected, asset.cleared, draft.withdrawn, version.submitted, validation.failed, review.opened, review.decided, accessibility.decided, translation_review.decided, exception.requested, exception.approved, exception.revoked, exception.expired, exception.consumed, sealing.started, sealing.failed, version.sealed, variant.created, readiness.changed, correction.authorized, correction.seeded, artefact.superseded, supersession.acknowledged, supersession.overdue, artefact.retired, artefact.used, artefact.archived, key.rotated, policy.denied, security.event, integrity.signal, integrity.referred, chain.checkpoint, chain.verified, evidence.sweep, breakglass.accessed. | MUST |
| PRD-EVD-13 | GAP D-02 Chain construction: the event body (every field except event_hash) is serialized with the canonical JSON rule of §8.4; event_hash = SHA-256 of the previous hash concatenated with the body bytes. The genesis record has sequence 0, a previous hash of 32 zero bytes, and carries chain identifier, creation time, schema version and environment; it is signed through the key service. Sequence numbers are strictly increasing and unique by database constraint; a single writer per chain takes a row lock on the chain head. Every 10,000 events or every hour, whichever is first, a checkpoint records the sequence and head hash, signed through the key service, and is exported to the monitoring platform as an external anchor so a store-wide rewrite is detectable. | MUST |
| PRD-EVD-14 | GAP Verification procedure: inputs are chain identifier and an optional sequence range (default: from the last verified checkpoint, or from genesis); the verifier walks events in sequence order, checks contiguity, recomputes each hash, compares with the stored hash and with the following event's previous hash, and verifies every checkpoint signature and the external anchor. Output: events verified, first failing sequence, failure kind (missing, altered, reordered, bad checkpoint), start and finish times. It runs on demand from the evidence view or an operator command, and daily on schedule. The result is itself written as chain.verified; a failure raises a Critical alert and invokes the runbook. | MUST |
| PRD-EVD-15 | GAP Throughput: the chain writer must sustain at least 200 events per second, because telemetry signals are mirrored into the chain (§6.14) at up to 100 per second across 50 sessions. This is measured in Week 1 before any feature is built on it. | MUST |
| PRD-EVD-16 | GAP The expected-evidence model (table below) is declarative configuration versioned with the policy, so a new step or record can be added without code. The completeness assertion at sealing evaluates it and names the step and record on failure (EVD-05, EVD-06). | MUST |
| PRD-EVD-17 | GAP D-27 Evidence view (EVD-08): read-only search by actor audit identifier, action, artefact or version identifier and time range; event detail with no content; the latest verification result and checkpoint; a "verify now" control for auditors. If reduced to a scripted procedure, the script must produce the same search and verification output to a file readable by the auditor. | SHOULD |
| PRD-EVD-18 | GAP Content ban enforcement (EVD-09): the event schema allowlists detail keys per action; an automated test writes events for every action with Restricted strings in every free field and asserts none is persisted; a log scrubber for known content field names is a second line of defence, never the first. | MUST |
| PRD-EVD-19 | GAP D-35 Daily sweep (EVD-10) re-runs the completeness assertion for every sealed version and alerts on any drift with the version identifier and the absent record. | SHOULD |

### Expected evidence model

| Step | Records that must exist before sealing | Binding and duty checks |
| --- | --- | --- |
| Creation | artefact.created audit event; an assignment Active at creation time. | Actor is the assignee; capability current at that time. |
| Submission | Immutable version with content hash; validation report (pass); similarity result; version.submitted event; receipt. | Report and event bound to the version hash; actor is the assigned author or translator. |
| Review | Approve decision(s) as many as the policy requires; complete checklist with three attestations and sources; difficulty; review.decided event. | Bound to the version hash; reviewer ≠ author or translator; capability valid at decision time; two reviewers distinct when two are required. |
| Translation review (variants) | Approve decision with equivalence judgement; structural check report (pass, or an exception identifier per failed check); translation_review.decided. | Reviewer ≠ translator and ≠ primary author; exception Active at submission time and approver ≠ requester. |
| Accessibility check | Approve decision; complete evaluation checklist; accommodation capability for every declared accommodation; accessibility.decided. | Specialist ≠ author, translator or reviewer; qualification present. |
| Assets | Scan record clean for every referenced asset with checksum. | Checksums match those in the canonical content. |
| Policy | Cycle policy version and taxonomy version in force; renderer version. | Match the versions recorded on every decision. |

#### Acceptance criteria

- Chain verification passes on seeded data and detects a deliberately altered event in a copy of the store (Week 1 closure); it still passes after backup and restore (Week 5). 
- Deleting an expected evidence record blocks the next transition and raises the alert naming the step and record (Week 3 closure). 
- The chain writer sustains 200 events per second in the integration environment with p95 write latency under 50 ms. 

## 6.14 Session integrity, observability and referral · ASR02-OBS

Implements ASR-02: spotting patterns that suggest something is wrong and referring them to someone who can decide. Monitoring starts at the first keystroke and never sees content.

| ID | Requirement | Priority |
| --- | --- | --- |
| ASR02-OBS-01 | Every authoring, review, accessibility and translation session is registered, heartbeated, and closed on sign-out or timeout. | MUST |
| ASR02-OBS-02 | The client captures and reports: copy, cut, paste, context menu, print, screenshot key combinations, developer tools opened, viewport anomaly consistent with a docked inspector, window or tab focus loss, page visibility change, concurrent-tab detection, and heartbeat gap. | MUST |
| ASR02-OBS-03 | Each captured action is blocked where technically possible and reported whether or not blocking succeeded. | MUST |
| ASR02-OBS-04 | The user receives immediate non-blocking feedback that the action was blocked and recorded. Feedback must not interrupt typing. | MUST |
| ASR02-OBS-05 | Ingest failure retries; events are never silently discarded. Durability outranks latency. | MUST |
| ASR02-OBS-06 | Each session carries an integrity score starting at 100, decremented per signal by a ratified severity table, floored at 0, and non-recovering within a session. | MUST |
| ASR02-OBS-07 | Signals are classified at least as warning or critical; critical signals are visually and audibly distinct. | MUST |
| ASR02-OBS-08 | Crossing the configured threshold refers the session — a security event to the monitoring platform and a persistent alert to the operator. | MUST |
| ASR02-OBS-09 | Repeat breaches update the existing alert rather than stacking duplicates. | MUST |
| ASR02-OBS-10 | Automatic session suspension defaults to off. Enabling it is an explicit operational decision, not a build default. | MUST |
| ASR02-OBS-11 | The operator surface shows all active sessions with role, subject, artefact state, integrity score and time since last heartbeat. | MUST |
| ASR02-OBS-12 | A rolling feed presents newest-first events across all sessions, with severity and pseudonymous actor identifier. | MUST |
| ASR02-OBS-13 | A per-session drill-down shows the full ordered event history and score progression. | MUST |
| ASR02-OBS-14 | The surface updates by server push, not manual reload, and displays a reconnecting state with backoff on transport loss. | MUST |
| ASR02-OBS-15 | On reconnect the surface re-synchronizes session state, so no live session is missing or stale. | MUST |
| ASR02-OBS-16 | A monitoring event carries only event type, timestamp, session identifier, pseudonymous actor audit identifier and task reference. No stem, option, field value, clipboard payload or screenshot. | MUST |
| ASR02-OBS-17 | OBS-16 is enforced by an automated test that fails the build — not by reviewer discipline. | MUST |
| ASR02-OBS-18 | The operator role can reach no artefact content through any interface. | MUST |
| PRD-OBS-19 | GAP Session record: session identifier; actor audit identifier; role; current task reference (assignment identifier, opaque); started at; last heartbeat at; ended at with reason (sign-out, inactivity, absolute maximum, suspension, revocation); integrity score; signal counts by kind; referred flag and alert identifier. The client heartbeats every 30 seconds; a session is flagged stale at 90 seconds without one (§11). | MUST |
| PRD-OBS-20 | GAP D-03 The signal catalogue below, with proposed default severities and decrements, is the ratified severity table once signed by the Integrity Operator and Security. It is configuration with a version recorded on every integrity event. | MUST |
| PRD-OBS-21 | GAP Telemetry event schema (Appendix C): event identifier, event type, severity, occurred at, session identifier, actor audit identifier, task reference, client sequence number, blocked flag, score after. The JSON schema forbids additional properties, and the build-failing test (OBS-17) submits events carrying content-like fields and asserts they are rejected, then inspects every persisted and forwarded event for the absence of any string from the synthetic corpus. | MUST |
| PRD-OBS-22 | GAP Client capture mechanics: copy, cut and paste listeners that prevent the default action and report; a context-menu listener that prevents and reports; key listeners for print and platform screenshot combinations that prevent where the browser allows and always report; developer-tools detection by viewport-delta and timing heuristics reported as viewport anomaly and, when confirmed, developer tools opened; visibility-change and blur listeners; concurrent-tab detection through a same-origin channel; heartbeat gap computed server-side. The capture library is loaded before the editor and the editor does not initialize without it. | MUST |
| PRD-OBS-23 | GAP D-33 Ingest: the client queues events in memory with client sequence numbers and posts batches of at most 50 to the telemetry endpoint; the server persists before acknowledging by event identifier; unacknowledged events retry with exponential backoff and jitter without ever blocking input; ordering is restored server-side by client sequence. Capacity: 50 sessions at 2 events per second sustained, bursts to 10 per second per session. | MUST |
| PRD-OBS-24 | GAP Scoring is computed server-side on ingest: score = max(0, 100 − sum of decrements), never recovering within the session; each event stores the score after it; duplicate event identifiers are ignored. | MUST |
| PRD-OBS-25 | GAP D-04 Referral: when the score first reaches or falls below the threshold (proposed 50), the system sends a security event to the monitoring platform carrying session identifier, actor audit identifier, score and the counts of the top signals, and creates one persistent alert on the operator surface. Every later signal in that session updates the same alert. Automatic suspension, when enabled by configuration D-22, ends the session, releases its assignment with reason and records both; it is off by default. | MUST |
| PRD-OBS-26 | GAP Operator surface transport: a server-push channel (server-sent events or a web socket) carrying session snapshots and events; reconnection with exponential backoff from 1 second to a 30-second cap with jitter; on reconnect the client sends its last event identifier and the server replies with a full session snapshot plus every missed event. Signal to surface p95 ≤ 3 seconds; signal to durable audit p95 ≤ 5 seconds. | MUST |
| PRD-OBS-27 | GAP The operator's authorization scope contains no content endpoint at all; the operator API's response schemas are tested for the absence of content field names, and the operator UI is served without the editor or renderer bundles. | MUST |
| PRD-OBS-28 | GAP Application observability (§11): structured logs with correlation and trace identifiers and no content; metrics for active sessions, events per second, telemetry backlog, sealing duration and failure count, chain write latency and lag, outbox lag, assignment pool size; dashboards contain no content. | MUST |

### Integrity signal catalogue (proposed severity table, D-03)

| Signal | Severity | Decrement | Blocked? | Notes |
| --- | --- | --- | --- | --- |
| Copy | Critical | 25 | Yes | Anywhere on a content surface. |
| Cut | Critical | 25 | Yes |  |
| Paste | Warning | 10 | Yes | External text cannot enter the editor D-21. |
| Context menu | Warning | 5 | Yes |  |
| Print | Critical | 40 | Yes | Print styles also render nothing. |
| Screenshot key combination | Critical | 40 | Where possible | Operating-system capture cannot be reliably blocked; the attempt is always reported. |
| Developer tools opened | Critical | 100 | No | Highest severity; refers immediately. |
| Viewport anomaly (docked inspector) | Critical | 50 | No |  |
| Window or tab focus loss | Warning | 2 | No |  |
| Page visibility change | Warning | 2 | No |  |
| Concurrent tab detected | Warning | 15 | No | Both tabs keep working; one session record. |
| Heartbeat gap (over 90 s) | Warning | 5 | No | Computed server-side. |

#### Acceptance criteria

- A deliberate copy attempt is blocked, scored, visible on the operator surface within 3 seconds and durable in the audit chain within 5 seconds, carrying no content (Week 2 closure). 
- Opening developer tools refers the session; a second critical signal updates the existing alert instead of creating a new one. 
- Dropping the operator transport shows the reconnecting state; on reconnect no live session is missing or stale. 
- The build fails when a telemetry event with an extra field is accepted by the schema. 

## 6.15 Notifications and alerts (cross-cutting)

GAP The specification requires active surfacing of tasks, operator alerts and operational alerts in several places; this section collects them so one component owns them.

| ID | Requirement | Priority |
| --- | --- | --- |
| PRD-NTF-01 | In-app notifications exist for: new assignment; task returned with findings; task approaching expiry (24 hours before); exception approved, revoked or expired; correction authorized (coordinator); equivalent-route escalation (coordinator); sealing failure (coordinator and operations); supersession unacknowledged (operations); assignment pool empty (coordinator). | MUST |
| PRD-NTF-02 | No notification in any channel contains artefact content, a correct answer, or a rendering. Out-of-band channels D-19 carry only the task type and a link. | MUST |
| PRD-NTF-03 | Alerts to the monitoring platform: security events (authorization denial outside assignment, device posture failure, not provisioned, threshold referral, malicious upload, hash mismatch) and operational alerts (sealing failure after retries, chain verification failure, expected evidence missing, supersession unacknowledged, telemetry backlog beyond 60 seconds, unassigned task beyond the delay). Each carries identifiers, codes and counts only. | MUST |

# 7. Interface requirements and API contract

Endpoint-level detail is owned by the published, versioned interface definition (`INT-01`). This section fixes the behaviours that definition must satisfy and names the resources it must contain, so the definition can be written in Week 1 and kept current by contract tests.

## 7.1 Mandatory interface behaviours

| ID | Requirement | Priority |
| --- | --- | --- |
| INT-01 | All interfaces are versioned and published as a machine-readable definition kept current with the implementation. | MUST |
| INT-02 | Interactive calls carry a bearer token from the enterprise identity provider. Service-to-service calls use mutual TLS and audience-restricted short-lived workload tokens. | MUST |
| INT-03 | Retryable mutations accept an idempotency key and are safe to repeat. | MUST |
| INT-04 | Draft updates require and return an optimistic-concurrency token; stale writes are rejected. | MUST |
| INT-05 | Errors return a stable machine-readable code, a safe message, a correlation identifier, field-level detail and retry ability — never echoing Restricted content. | MUST |
| INT-06 | Listing uses opaque cursors. Unrestricted bulk exports are prohibited. | MUST |
| INT-07 | Timestamps are UTC and identifiers are opaque. | MUST |
| INT-08 | Rate limits vary by user, workload identity, endpoint sensitivity and source zone. | MUST |
| INT-09 | A role-by-operation permission matrix is authored, implemented, and used as the test oracle for authorization. | MUST |
| INT-10 | Domain events are published for creation, submission, review decision, accessibility decision, readiness change, sealing, supersession and policy denial. Events defined must have a producer. | MUST |
| PRD-INT-11 | GAP Conventions: JSON request and response bodies; base path /api/v1 for interactive surfaces, /assembly/v1, /downstream/v1, /telemetry/v1, /operator/v1 and /evidence/v1 for their audiences; identifiers are ULIDs; timestamps are RFC 3339 in UTC; idempotency key in the Idempotency-Key header for every POST that creates or transitions, retained 24 hours; concurrency token via ETag and If-Match on drafts; cursor pagination returns items and next_cursor with a maximum page size of 200; every response carries Cache-Control: no-store and the correlation identifier. | MUST |
| PRD-INT-12 | GAP Rate-limit classes (INT-08): interactive content endpoints 60 requests per minute per user; autosave 30 per minute per draft; telemetry 600 events per minute per session; assembly readiness 600 per minute per workload identity; downstream notifications 60 per minute; sign-in 10 per minute per source. Limits are configuration; exceeding one returns RATE_LIMITED with a retry-after value. | MUST |
| PRD-INT-13 | GAP Machine-interface security: mutual TLS with certificates from the enterprise authority; tokens with audience, issuer, expiry ≤ 5 minutes and a key identifier resolved through a published key set; signed notifications use a detached JSON Web Signature with replay protection by notification identifier and a 5-minute clock-skew window; key rotation is supported without downtime. | MUST |
| PRD-INT-14 | GAP Content responses (draft, version, render, asset) are authorized per request with a short-lived scope and are non-cacheable (DAT-04); asset bytes are served through an authorized endpoint with a 60-second signed reference, never a stable public URL. | MUST |

## 7.2 Error contract and code catalogue

Every error body has the shape shown in Appendix C: `code`, `message`, `correlation_id`, `retryable` and `fields` (a list of path, code and message). Messages are fixed strings chosen from a catalogue; they never interpolate user content.

| Code | HTTP | Retryable | Meaning |
| --- | --- | --- | --- |
| AUTH_REQUIRED | 401 | No | No valid token; the client redirects to sign-in. |
| FORBIDDEN_MFA_REQUIRED | 403 | No | Token lacks the multi-factor claim. |
| FORBIDDEN_DEVICE_POSTURE | 403 | No | Device certificate, posture or zone check failed; security event raised. |
| NOT_PROVISIONED | 403 | No | Valid identity with no capability entry or unknown role; security event raised. |
| FORBIDDEN_NOT_ASSIGNED | 403 | No | Object outside the user's assignments; security event raised. |
| FORBIDDEN_DUTY_CONFLICT | 403 | No | Separation-of-duties rule violated (names the rule). |
| FORBIDDEN_CAPABILITY_EXPIRED | 403 | No | Capability entry expired or revoked. |
| FORBIDDEN_REAUTH_REQUIRED | 403 | No | Privileged action needs a fresh authentication. |
| REJECTED_AUDIENCE | 403 | No | Human token or wrong-audience workload token on a machine interface. |
| SIGNATURE_INVALID | 400 | No | Downstream notification signature or replay check failed. |
| VALIDATION_FAILED | 422 | No | One or more blocking findings; fields lists each with its rule code. |
| SIMILARITY_BLOCK | 422 | No | Similarity above threshold; fields carries the matched artefact identifiers. |
| STRUCTURAL_CHECK_FAILED | 422 | No | Variant diverges from primary; lists the failing check codes. |
| EXCEPTION_REQUIRED | 422 | No | Override attempted without an Active exception covering the check. |
| CONFLICT_STALE_WRITE | 409 | No | Concurrency token does not match; the client reloads. |
| CONFLICT_INVALID_TRANSITION | 409 | No | Lifecycle transition not permitted from the current state; message names both states. |
| CONFLICT_ALREADY_DECIDED | 409 | No | A decision already exists for this version. |
| CONFLICT_STATE_CHANGED | 409 | No | The version left the expected state before the request arrived. |
| CYCLE_INACTIVE | 409 | No | Cycle is not Active. |
| AUTHOR_CAP_REACHED | 409 | No | Per-author cap for the cycle reached. |
| TAXONOMY_RETIRED | 422 | No | A selected node is retired. |
| ASSET_REJECTED | 422 | No | Upload failed quarantine (format, signature, scan, bomb); reason category only. |
| ASSET_TOO_LARGE | 413 | No | Image or asset budget exceeded; limit stated. |
| SELECTION_NOT_READY | 409 | No | Selection notification names an artefact that is not ready; lists identifiers and states. |
| RATE_LIMITED | 429 | Yes | Limit exceeded; retry-after provided. |
| DEPENDENCY_UNAVAILABLE | 503 | Yes | Audit, key service, scanner or object store unavailable; the operation failed closed. |
| INTERNAL | 500 | Yes | Unexpected failure; correlation identifier only, no detail. |

## 7.3 Resource and endpoint catalogue

The catalogue names what the interface definition must contain. Paths are indicative; the definition may refine them, but every row must exist with the stated audience and behaviour.

| Area | Endpoint | Audience | Behaviour |
| --- | --- | --- | --- |
| Session | GET /me | Any signed-in user | Role, capability summary, session expiry, active assignment count. No content. |
| Session | POST /sessions/heartbeat, POST /sessions/sign-out | Any | Heartbeat every 30 s; sign-out closes the session record. |
| Configuration | GET&#124;POST /cycles, GET&#124;PATCH /cycles/{id}, POST /cycles/{id}/activate, POST /cycles/{id}/close | Coordinator (re-auth on change) | Cycle lifecycle; policy version increments. |
| Configuration | GET&#124;POST /taxonomy/versions, POST /taxonomy/versions/{v}/publish, POST /taxonomy/nodes/{id}/retire, GET&#124;POST /vocabularies | Taxonomy Administrator | Versioned tree and vocabularies; retire, never delete. |
| Registry | GET&#124;POST /capabilities, POST /capabilities/{id}/revoke | Coordinator (re-auth) | Append-only entries against audit identifiers. |
| Assignments | GET /my/tasks | Workforce roles | Own active assignments only. |
| Assignments | GET /assignments, POST /assignments, POST /assignments/{id}/release, POST /assignments/{id}/reassign | Coordinator | Manual assignment passes the same eligibility policy. |
| Coordinator | GET /coordinator/progress, /aging, /author-caps, /language-status, /escalations | Coordinator | State, ownership, age, counts. Never content. |
| Drafts | POST /drafts, GET /drafts/{id}, PATCH /drafts/{id} (If-Match) | Assigned author or translator | Create within an active cycle; autosave with concurrency token. |
| Drafts | POST /drafts/{id}/assets, GET /assets/{id} | Assigned author | Upload into quarantine; fetch only when clean, signed reference, no-store. |
| Drafts | POST /drafts/{id}/validate, POST /drafts/{id}/preview, POST /drafts/{id}/submit, POST /drafts/{id}/withdraw | Assigned author or translator | Pure validation; reference rendering; immutable submission with receipt; withdraw unsubmitted. |
| Resources | GET /resources/reference, /glossary?lang=, /symbols, /equation-templates | Author, Translator | Read-only in-tool resources. |
| Versions | GET /versions/{id}, GET /versions/{id}/render, GET /versions/{id}/receipt, GET /versions/{id}/diff-primary | Assigned reviewer, specialist, translation reviewer; author for receipt | Read-only; correct-answer field filtered by policy; primary difference for revalidation tasks. |
| Decisions | POST /versions/{id}/review-decisions, /accessibility-decisions, /translation-review-decisions | Assigned role, duty-clean | Append-only; no content fields accepted; conflict on already decided. |
| Exceptions | GET&#124;POST /exceptions, POST /exceptions/{id}/approve, POST /exceptions/{id}/revoke | Requester roles; Coordinator approves (re-auth) | Approver ≠ requester; expiry mandatory. |
| Corrections | POST /artefacts/{id}/corrections, POST /artefacts/{id}/retire, POST /artefacts/{id}/exclusions | Coordinator (re-auth) | Authorization with reason; readiness revoked; exclusion pairs. |
| Sealing | GET /sealing-jobs/{id}, POST /sealing-jobs/{id}/retry | Coordinator (status); Operations (retry) | Job status and safe replay. |
| Assembly | GET /assembly/v1/readiness, GET /assembly/v1/readiness/{artefact_id} | Assembly workload (W) | Metadata only; cursor pagination. |
| Downstream | POST /downstream/v1/selection-notifications, /exam-completions, /supersession-acks | Assembly workload (W, signed) | Idempotent, atomic transitions; acknowledgement tracking. |
| Telemetry | POST /telemetry/v1/events | Client of any content session | Batched, durable before acknowledgement, schema-enforced. |
| Operator | GET /operator/v1/sessions, GET /operator/v1/stream, GET /operator/v1/sessions/{id}, POST /operator/v1/alerts/{id}/acknowledge | Integrity Operator | Push stream with resume; no content route exists. |
| Evidence | GET /evidence/v1/events, POST /evidence/v1/verifications, GET /evidence/v1/verifications/{id}, GET /evidence/v1/manifests/{version_id} | Auditor | Search, verify, inspect manifests and hashes; no content. |
| Health | GET /healthz, GET /readyz | Platform | Dependency status codes only. |

## 7.4 Domain event catalogue

Events are written to the transactional outbox in the same transaction as the state change and delivered at least once with consumer-side deduplication by event identifier (`ARC-03`). Every event carries: event identifier, type, occurred at, correlation identifier, policy version, and the subject identifiers and hashes named below. No event carries content.

| Event | Producer / trigger | Payload keys beyond the envelope | Consumers |
| --- | --- | --- | --- |
| artefact.created | Draft creation | artefact_id, lineage_id, cycle, language, actor_audit_id | Coordinator board, audit |
| version.submitted | Submission | version_id, artefact_id, content_hash, rule_set_version | Assignment policy, audit |
| review.decided | Review decision | version_id, version_hash, outcome, decision_id, decision_hash, successor_draft_id? | Assignment policy, audit, notifications |
| translation_review.decided | Translation-review decision | as above plus equivalence_judgement | Assignment policy, audit |
| accessibility.decided | Accessibility decision | version_id, version_hash, outcome, decision_id, accommodations, equivalent_route_needed | Sealing worker, coordinator escalations |
| assignment.created / released / expired / reassigned | Assignment changes | assignment_id, task_type, actor_audit_id, subject reference | My Work push, coordinator board |
| exception.requested / approved / revoked / expired | Exception lifecycle | exception_id, version_id, check_codes, expires_at | Notifications, audit |
| version.sealed | Sealing step 8 | version_id, artefact_id, language, content_hash, manifest_id, superseded_version_id? | Readiness, variant creation, audit |
| variant.created | Sealing of a primary | artefact_id, language, variant_draft_id, primary_reference_hash | Assignment policy |
| readiness.changed | Any readiness input change | artefact_id, previous_status, new_status, reason | Assembly (via readiness record), coordinator board |
| correction.authorized | Correction authorization | artefact_id, sealed_version_id, authorization_id, scope | Seeding worker, audit, notifications |
| artefact.superseded | Sealing of a corrected version | artefact_id, language, superseded_version_id, replaced_by_version_id, replaced_by_hash | Assembly and registered consumers (acknowledgement required) |
| artefact.used / artefact.archived | Downstream notifications | artefact_id, exam_session_id, version_ids, artefact_set_hash (archived) | Audit, coordinator board |
| artefact.retired | Retirement | artefact_id, reason_code | Readiness, audit |
| policy.denied | Any authorization denial | actor_audit_id, operation, subject reference, denial_code, rule | Monitoring platform, audit |
| policy.changed | Cycle or vocabulary change | cycle, policy_version, changed_keys | Audit, coordinator board |
| integrity.referred | Threshold breach | session_id, actor_audit_id, score, top_signals | Monitoring platform, operator alert |
| sealing.failed | Sealing job failure after retries | version_id, job_id, reason_code, attempt | Operations alert, coordinator |

# 8. Data requirements, canonicalization and manifests

Detailed schemas, field types and constraints are produced by the team as a versioned migration set. This section fixes the entities, their required fields and the rules that govern them, so the migration set can be reviewed against it.

## 8.1 Data rules

| ID | Requirement | Priority |
| --- | --- | --- |
| DAT-01 | Artefact text, answers, explanations, assets, review comments and manifests are classified Restricted. | MUST |
| DAT-02 | Business records reference stable pseudonymous workforce audit identifiers; the identity provider remains the identity authority. | MUST |
| DAT-03 | Plaintext content never appears in URLs, analytics, traces, exception messages, infrastructure logs, browser storage, notifications, dashboards or support tickets. | MUST |
| DAT-04 | Content responses use short-lived authorization and are marked non-cacheable. | MUST |
| DAT-05 | Canonicalization is specified once — Unicode normalization, whitespace, attribute order, option order, numeric representation and asset-hash inclusion — and is bit-stable across repeat serialization and restore. Every hash depends on it. | MUST |
| DAT-06 | The canonical schema is versioned, and a stated migration approach preserves verifiability of already-sealed artefacts. | MUST |
| DAT-07 | Artefacts are encrypted in storage and in transit. | MUST |
| DAT-08 | Retention locks are implemented with the period as configuration. No default period is invented. | MUST |
| PRD-DAT-09 | GAP Data lives in three stores with distinct identities: the working store (relational; drafts, versions, decisions, assignments, configuration, sessions), the repository (sealed objects, manifests, bank index; separate credentials and network segment, ARC-11), and the audit store (append-only chain, checkpoints, integrity events). The pseudonym mapping table is in a fourth, most restricted schema. | MUST |
| PRD-DAT-10 | GAP Every table carrying Restricted fields is enumerated in a data-classification register checked into the repository; log scrubbing, backup access separation and the no-content tests are generated from that register. | MUST |

## 8.2 Entities and required fields

GAP Field lists are minimum requirements; the migration set may add operational columns but may not remove or repurpose these. Types: id = opaque ULID; ts = UTC timestamp; hash = lowercase hex SHA-256; enum = closed vocabulary.

| Entity | Required fields | Rules |
| --- | --- | --- |
| Cycle | id, code (unique), title, primary_language, required_languages[], syllabus_version_id, permitted_item_types[], marking_policy_ref, default_marks, declared_accommodations[], author_cap, review_count_required, reviewer_sees_key, remediation_policy (enum), assignment_expiry_by_task_type, similarity_threshold, status (enum), policy_version, created_at, updated_at | Code immutable; no delete; policy_version increments on every change. |
| TaxonomyVersion / TaxonomyNode | version_id, published_at, status; node_id (stable), version_id, parent_id, level (subject&#124;unit&#124;topic), label, active_from, retired_at | Published versions immutable; retire never deletes. |
| Vocabulary / VocabularyValue | vocabulary (enum: difficulty, taxonomy_level, complexity_level, accommodation, item_type), value_id, label, sort_order, active_from, retired_at, version | Retire never deletes. |
| AuditIdentity | audit_id (random, stable), idp_subject (unique), created_at | Separate restricted schema; only the sign-in service reads it. |
| CapabilityEntry | id, audit_id, role (enum), subject_scope[], language_scope[], accessibility_qualified, credential_ref, issuing_authority, valid_from, valid_to, revoked_at, revoked_reason, created_by, supersedes_id | Append-only; renewal supersedes. |
| Artefact | id, cycle_id, item_type, current_primary_version_id, current_variant_version_ids{language}, readiness_status (enum), readiness_revoked_reason, created_at, retired_at, retire_reason | Stable identity across all languages and lineages. |
| Lineage | id, artefact_id, language, kind (primary&#124;variant), primary_reference_hash (variants), supersedes_lineage_id, created_by_reason (initial&#124;return&#124;correction&#124;revalidation), requires_revalidation | A correction opens a new lineage. |
| Version | id, lineage_id, artefact_id, language, sequence_in_lineage, state (enum), derived_from_version_id, content (Restricted; Draft only mutable), canonical_bytes (immutable states), content_hash, canonical_schema_version, canonicalization_rule_version, renderer_version, classification{subject_id, unit_id, topic_id, difficulty, taxonomy_level}, marks, policy_version, submitted_at, concurrency_token, created_by_audit_id, sealed_manifest_id, replaced_by_version_id, exam_session_id | Immutable outside Draft (database trigger); content column null once sealed (VLT-05). |
| Option | version_id, option_id (structural, stable across variants), position, body (Restricted), is_correct | Exactly one is_correct per version; position order canonical. |
| Asset | id, version_id, object_key, checksum, byte_size, width, height, format, scan_status (quarantined&#124;clean&#124;rejected), scan_report_ref, alt_text (Restricted), decorative, created_at | Referenced only when clean. |
| Rendition | id, version_id, format (reference_html&#124;…), renderer_version, object_key or inline, status | Extensible for alternate formats (ACC-09). |
| Assignment | id, task_type (enum), audit_id, subject_type, subject_id, cycle_id, language, created_at, expires_at, status (enum), released_reason, policy_version, candidate_count, opened_at, completed_at | Append-only. |
| Decision | id, version_id, version_hash, type (enum), outcome (enum), checklist (json), attestations (json), reason_code, comments (Restricted), difficulty_assigned, equivalence_judgement, accommodations (json), findings (json, Restricted), exception_ids[], reviewer_audit_id, capability_entry_id, renderer_version, policy_version, opened_at, decided_at, duration_ms, correlation_id, decision_hash | Append-only; no update or delete. |
| Exception | id, version_id, check_codes[], justification, requested_by, approved_by, created_at, expires_at, status (enum), revoked_reason | approved_by ≠ requested_by. |
| CorrectionAuthorization | id, artefact_id, sealed_version_id, scope, authorized_by, reason, created_at, seeded_draft_id | Emits readiness revocation in the same transaction. |
| Manifest | id, version_id, fields per §8.6, canonical_bytes, signature, signing_key_id, created_at | Restricted; immutable. |
| BankIndex | version_id, artefact_id, language, lineage_id, classification, complexity_level, difficulty, taxonomy_level, marks, content_hash, similarity_fingerprint (Restricted derived), sealed_at, is_current, accommodations_deliverable[] | No content column may be added. |
| ReadinessRecord | artefact_id, cycle_code, item_type, classification, difficulty, taxonomy_level, marks, marking_policy_ref, languages[{language, sealed_version_id, content_hash, manifest_id}], readiness_status, ready_since, revoked_reason, exclusion_pair_ids[], accommodations_deliverable[], updated_at | Materialized; updated transactionally. |
| ExclusionPair | id, artefact_id_a, artefact_id_b, reason, recorded_by, created_at, removed_at | SHOULD |
| SupersessionNotice | id, event_id, artefact_id, consumer_id, sent_at, acknowledged_at, overdue_alert_id | Overdue after the configured window. |
| Session | id, audit_id, role, task_ref, started_at, last_heartbeat_at, ended_at, end_reason, integrity_score, signal_counts (json), referred_at, alert_id, severity_table_version | One per login. |
| IntegrityEvent | id, session_id, audit_id, task_ref, event_type (enum), severity (enum), occurred_at, received_at, client_seq, blocked, score_after | Schema forbids extra fields. |
| AuditEvent | event_id, chain_id, sequence, occurred_at, actor_type, actor_id, action (enum), subject_type, subject_id, subject_hash, outcome, policy_version, correlation_id, trace_id, details (json, allowlisted keys), prev_hash, event_hash | Append-only; sequence unique. |
| ChainCheckpoint | id, chain_id, sequence, head_hash, created_at, signature, signing_key_id, external_anchor_ref | Every 10,000 events or hourly. |
| OutboxMessage | id, event_type, payload, created_at, delivered_at, attempts, next_attempt_at | Same transaction as the change. |
| SealingJob | id, version_id, status (pending&#124;running&#124;succeeded&#124;failed), attempts, last_error_code, started_at, finished_at | Idempotent by version_id. |

## 8.3 Relationships, constraints and indexes

- Artefact 1 → many Lineage; Lineage 1 → many Version (ordered by sequence); Version 1 → 2..8 Option; Version 0..6 Asset; Version 0..many Decision; Version 0..1 Manifest; Version 0..1 BankIndex row. 
- Database constraints: exactly one `is_correct` per version; unique (lineage, sequence); unique (chain, sequence); a trigger rejects any update to a Version whose state is not Draft; a trigger rejects deletes on Version, Option, Asset, Decision, Manifest and AuditEvent. 
- Indexes: Assignment by (audit_id, status); Version by (state, cycle); BankIndex by (language, classification), by (is_current, artefact_id); ReadinessRecord by (cycle_code, readiness_status, updated_at); AuditEvent by (subject_id), (actor_id, occurred_at), (action, occurred_at); IntegrityEvent by (session_id, client_seq). 
- Row-level visibility: content columns are readable only through the application's authorization layer; no reporting user or replica exposes them. 

## 8.4 Canonicalization rule v1

GAP D-01 The rule below is proposed for ratification in Week 1 and fixed as `canonicalization_rule_version = "1.0"`. Every hash in the system — content, decision, manifest and audit — is computed over bytes produced by this rule.

| Aspect | Rule |
| --- | --- |
| Container | The canonical content document is a JSON object serialized with the JSON Canonicalization Scheme (RFC 8785): object keys sorted by Unicode code point, no insignificant whitespace, strings escaped per the scheme, UTF-8 encoding. |
| Text normalization | Every string is Unicode NFC. Leading and trailing whitespace is trimmed; internal runs of whitespace (space, tab, line break) collapse to one space. Zero-width and bidirectional control characters are removed except an explicit dir attribute. |
| Restricted HTML | Serialized from the sanitized DOM: lowercase element names; attributes sorted by name; attribute values double-quoted with & < > " escaped; text nodes escaped for & < >; no comments; empty text nodes dropped; void elements written as `<br>` and `<img …>`; adjacent text nodes merged. |
| Equations | Parsed with the permitted-subset grammar and re-serialized from the syntax tree: single spaces between tokens, no comments, braces normalized, command aliases mapped to one spelling. The canonical LaTeX string is stored in eq[data-latex]. |
| Options | Serialized in display position order as objects with option_id, body and is_correct. Option identifiers are structural and stable across variants. |
| Numbers | Marks and any numeric metadata are integers or decimal strings without trailing zeros; floating-point values never appear. |
| Assets | Each image reference includes the asset's SHA-256 checksum of its sanitized, re-encoded bytes, its alternative text and decorative flag, so the content hash covers the image. |
| Fields covered | canonical_schema_version, item_type, language, stem, options, explanation, classification (node identifiers and taxonomy version), difficulty, taxonomy_level, marks, assets. |
| Fields excluded | Comments, findings, author or reviewer identifiers, timestamps, assignment identifiers, revision history, source metadata, rendering output (VLT-03). |
| Hash | content_hash = SHA-256 of the canonical bytes, lowercase hexadecimal. The same rule with the same inputs must produce identical bytes on any platform, after any restore and in any future release that supports version 1.0. |
| Stability test | A corpus of sealed artefacts and their hashes is kept in the repository; every build re-canonicalizes the corpus and fails if any hash changes. |

## 8.5 Similarity fingerprint

GAP D-08 D-31 Computed from the canonical content at sealing as defined in §6.5: normalized text of stem plus options, word 3-gram hashes (64-bit, fixed seed), stored as a sorted array in the bank index. It is derived Restricted data: it is not reversible to the full text but is treated with repository-tier access controls and is never exposed through any interface.

## 8.6 Manifest format

A manifest is the verifiable evidence for one sealed version. Its canonical JSON (same rule as §8.4) is signed through the key management service. Appendix C shows a sample.

| Field | Content |
| --- | --- |
| manifest_version | Manifest schema version. |
| version_id, artefact_id, lineage_id, language, item_type | Identity of the sealed version. |
| content_hash, canonical_schema_version, canonicalization_rule_version, renderer_version | What was hashed and how. |
| ciphertext_hash, object_key, encryption{algorithm, wrapped_data_key_ref, kms_key_id, tier} | Where the sealed bytes are and how they are protected. |
| assets[{asset_id, checksum}] | Every image included in the hash. |
| approvals[{decision_id, type, decision_hash, reviewer_audit_id, decided_at}] | Every decision that justified sealing, including exception identifiers where used. |
| evidence_assertion{model_version, passed_at} | Result of the expected-evidence assertion. |
| policy{cycle_policy_version, taxonomy_version, vocabulary_versions} | Rules in force. |
| primary_reference_hash | For variants: the primary sealed hash this variant was verified against. |
| supersedes_version_id | For corrections. |
| sealed_at, sealing_identity, audit_event_id | When, by which workload, and the chain event that records it. |
| signature, signing_key_id, signature_algorithm | Detached signature over the canonical manifest bytes without these three fields. |

## 8.7 Schema versioning and migration (DAT-06)

- Every version and manifest records `canonical_schema_version` and `canonicalization_rule_version`. The verifier keeps an implementation of every historical rule version for as long as any sealed artefact references it. 
- Migrations are additive: new columns and tables only; sealed canonical bytes, manifests and audit events are never rewritten. 
- A change to the canonical form or rule bumps the version, is applied only to newly sealed versions, and is accepted only when the stability corpus in §8.4 still verifies under every prior version. 
- Migrations run from the pipeline with no manual step, are reversible for the working store, and never touch the repository or audit store except to add tables. 

## 8.8 Classification, retention and backups

| Data | Class | Where it may appear |
| --- | --- | --- |
| Stem, options, explanation, alternative text, assets, findings, review comments, manifests, primary reference snapshots, similarity fingerprints | Restricted | Working store and repository only; role surfaces of assigned users; never any side channel (DAT-03). |
| Correct-answer flag | Restricted, tighter | Assigned author before submission; reviewer only where policy requires; never coordinator, operator, administrator or any list, event or log. |
| Identifiers, hashes, states, classification, decision outcomes, scores, timestamps | Internal | All role surfaces per matrix; audit; telemetry; monitoring; readiness interface. |
| Pseudonym mapping | Restricted, tighter | Sign-in service only. |

- Retention lock period for sealed objects and manifests is configuration supplied by Content Operations and Legal before Week 4 D-24; the software refuses to seal into a bucket without a lock configured. 
- Backups are encrypted, access-separated from the application identities, immutable for their retention, and restoration is tested in Week 5 with chain verification afterwards (`SEC-13`, `ASR01-EVD-04`). 
- Recovery targets: RTO ≤ 4 hours, RPO ≤ 15 minutes; autosave bounds draft loss to ≤ 30 seconds. 

# 9. Screens

No visual design is specified here. Each screen is defined by who uses it, what it must show, what it must let the user do, what it must never show, and the states it must implement. The Product Designer works from this section; the frontend engineers build to it.

## 9.1 Shared shell and the four states

- Shell. Every surface shares one shell: a header carrying the classification marking ("RESTRICTED — examination content" on content surfaces), the user's role, the session timeout countdown and sign-out; role-filtered navigation that shows only surfaces the user's capability entries allow. 
- Four states. Every screen implements loading (skeletons in the shape of the content), empty (explanatory, not an error, no spinner), error (inline plus notification, with retry) and success. 
- Always visible on content screens. Classification marking, session timeout, last-save status, active version identifier and hash prefix, assignment, workflow state. 
- Hardened region. Any region that renders content is visually marked and is the region where signal capture and blocking apply (§6.14). Print styles render nothing inside it. 
- No exits. No screen contains a link to an external site, a download control, a print control, an export control or a browsable list of unassigned content. 

## 9.2 Screen requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| UI-01 | Sign-in — enterprise identity redirect only. No password form is built. On return, the user lands on their role's default surface. | MUST |
| UI-02 | My Work — assigned tasks with type, cycle, subject, language, state, age and deadline. No unassigned content is reachable. | MUST |
| UI-03 | My Work — a task becoming available is actively surfaced to the assignee; work does not sit unannounced in a queue nobody is prompted to check. | MUST |
| UI-04 | Authoring — hardened editor for stem, options, correct answer, explanation and classification, with the hardened region visually marked; live validation findings; preview; submit. | MUST |
| UI-05 | Authoring — a session integrity panel shows the current score, signal counts and a recent-event list, so the author knows exactly what is recorded. | MUST |
| UI-06 | Review — read-only version, hash, permitted metadata, mandatory checklist, rationale entry, approve and return. Correct-answer visibility per policy. | MUST |
| UI-07 | Review — the worklist locks to the open task until a decision is recorded, then advances. | MUST |
| UI-08 | Accessibility Check — rendered artefact with keyboard and screen-reader affordances, structured findings capture, accommodation capability capture, approve and return. In the converged model this is the Accessibility Reviewer's screen. | MUST |
| PRD-UI-08a | GAP Accessibility Remediation — the Accessibility Specialist's screen: rendered artefact with the same test affordances, an editor limited to accessibility fields (alternative text, decorative flags, table headers and captions, equation text alternatives, reading order), the self-check checklist, comments, and Complete. Locked fields are shown read-only and visibly locked. | MUST |
| UI-09 | Translation — side-by-side read-only primary and editable target language, glossary reference, structural lock indicators, and a change summary when revalidation is required. | MUST |
| UI-10 | Coordinator — cycle configuration, taxonomy management, assignment, author cap status, and safe progress with artefact aging. Assignment screens reveal no artefact content. | MUST |
| UI-11 | Operator — live sessions, event feed, per-session drill-down, alert banner, connection state. Distinct visual treatment for the operational context. | MUST |
| UI-12 | Evidence — read-only audit search and chain-verification result. (P1.) | SHOULD |
| UI-13 | Every input is labelled; keyboard operation and screen-reader semantics are preserved throughout. | MUST |
| UI-14 | A page refresh restores equivalent state. No unsaved work is silently lost. | MUST |

## 9.3 Screen-by-screen specification

| Screen | Users | Shows | Actions | Never shows / notes |
| --- | --- | --- | --- | --- |
| Sign-in (UI-01) | All | A single "Sign in with your organisation account" control; after the redirect, the device and zone check result; a "not provisioned" or "device not approved" explanation when relevant. | Start sign-in; sign out. | No password field, no remember-me, no local account creation. |
| My Work (UI-02, 03) | Admin (as author), Question Reviewer, Accessibility Specialist, Accessibility Reviewer, Translator, Translation Reviewer | Task list sorted by deadline: type, cycle, subject, language, state, age, deadline; new-task badge; returned-task marker; expiring-soon marker; integrity score of the current session. | Open a task; create a draft (authors, if cap allows); withdraw an unsubmitted draft. | No content preview in the list; no artefacts other than own assignments; empty state explains that new tasks arrive here and are announced. |
| Authoring (UI-04, 05) | Admin (as author); generated drafts open here with their provenance panel | Hardened editor: stem, ordered options with correct-answer selector, explanation, classification pickers (subject → unit → topic from the syllabus version, difficulty, taxonomy level), marks; image upload with alternative text and decorative flag; equation editor bounded to the subset; live validation panel with findings against fields; save status; preview in the reference renderer; integrity panel (score, counts, recent events); in-tool resources drawer (reference material, symbols, equation templates, glossary); findings from a return shown beside the fields they name. | Edit; upload image; insert equation; validate; preview; submit; withdraw. | No copy, cut, paste, print, download, export or external link. Submit is disabled while blocking findings exist. Cap reached shows an explanatory blocker, not an error. |
| Review (UI-06, 07) | Question Reviewer, Translation Reviewer | Reference rendering; content hash; the permitted metadata of PRD-REV-19; the mandatory checklist with attestations and source fields; difficulty picker; equivalence judgement (variants) with the primary reference side by side; comments; reason code; opened-at timer. | Complete checklist; comment; approve; reject. | No editable content field. No author identity, assessment identity, other questions, other reviewers or audit history. Approve disabled until the checklist is complete; reject disabled until reason code and comments are present. After a decision the worklist advances. |
| Accessibility Remediation (PRD-UI-08a) | Accessibility Specialist | Reference rendering with test affordances; accessibility-field editor; locked content shown read-only; self-check checklist; comments; task status. | Edit accessibility fields; run self-check; comment; complete. | Cannot edit stem, options, answer, marks, notation or images; cannot approve. Complete is disabled while the self-check is incomplete. |
| Accessibility Review (UI-08) | Accessibility Reviewer | Reference rendering with test affordances (keyboard mode, screen-reader view, text-only, zoom, contrast, reading-order outline); evaluation checklist; findings capture with element picker; accommodation capability capture for each declared accommodation; comments. | Record findings; mark accommodations; approve; return. | Read-only content. Approve disabled while a blocking finding is unresolved or an accommodation is unrecorded. "Needs equivalent route" requires a reason and shows that it will be escalated. |
| Translation (UI-09) | Translator | Primary reference (read-only rendering and text) beside the editable target fields; locked tokens for numbers, units, symbols, equations and images; glossary panel filtered to the target language; structural lock indicators; live structural check results; change summary (field-level difference) when the task is a revalidation. | Edit target text; validate; preview; request exception; submit. | Cannot edit locked fields, reorder options, change the key or marks. Submit disabled while a structural check fails without an Active exception. |
| Admin configuration and assignment (UI-10) | Admin | Cycle configuration; taxonomy version editor; capability registry; assignment board with pool, aging and expiry; author-cap status; language status per artefact with owner; escalations (equivalent route, sealing failures, unacknowledged supersessions); exceptions awaiting approval; correction and retirement actions. | Configure; publish taxonomy; assign, reassign, release; approve exception; authorize correction; retire; record exclusion pair. | No artefact content, no renderings, no correct answers, no hashes beyond identifiers. Privileged actions prompt re-authentication. |
| Operator (UI-11) | Integrity Operator | Live session table (role, subject, artefact state, score, time since heartbeat); newest-first event feed with severity; per-session drill-down with score progression; alert banner for referred sessions; connection state (live, reconnecting with countdown, resynchronizing). | Acknowledge an alert; filter; open a session. | No content route exists. Distinct visual treatment from content surfaces. Critical signals are visually and audibly distinct. |
| Evidence (UI-12) | Auditor | Audit search by actor, action, artefact or version, time range; event detail; manifest view with hashes and signature status; latest verification result and checkpoint. | Search; run verification; inspect manifest. | No content; no workflow actions. May be delivered as a scripted procedure with equivalent output D-27. |

## 9.4 Accessibility of the surfaces

- Role surfaces and the reference rendering conform to WCAG 2.1 AA (§11) and are built accessible by construction, not remediated. 
- Every input has a programmatic label; every control is reachable and operable by keyboard with a visible focus state; a documented keyboard map covers the editor, the checklist and the option selector. 
- Save status, validation findings and integrity feedback are announced through live regions without stealing focus. 
- Motion respects reduced-motion preferences; colour never carries meaning alone; the interface is locale-aware and right-to-left ready. 

## 9.5 Refresh and resume

- Refreshing any screen restores equivalent state from the server: the same task, the same draft content (as of the last autosave), the same checklist progress (persisted server-side on each change), the same filters. 
- Token expiry mid-session refreshes silently; if the refresh window has also expired, the client autosaves, redirects to sign-in and returns to the same task (§6.4). 

# 10. Architecture and security constraints

The specification is deliberately technology-neutral. This section restates the architectural and security requirements, adds the constraints any chosen stack must satisfy, and defines the procedures the specification names but does not describe.

## 10.1 Reference architecture and trust zones

The two-layer picture in §1.5 is the high-level view: Layer 1 is everything in the table below; Layer 2 is a separate deployment reached only through the connector, which is an ordinary outbound integration under the egress allowlist and carries no sealed content.

| Zone | Components | Responsibilities and rules |
| --- | --- | --- |
| Experience | Role surfaces: Authoring, Review, Accessibility, Translation, Coordinator, Operator, Evidence | Served only inside the approved zone to managed devices. Ship the capture library before any content surface. The operator and evidence surfaces are separate bundles without the editor or renderer. |
| Application | Domain services: artefact and version, workflow and policy, translation, taxonomy and configuration, telemetry ingest, notifications | Server-side authorization on every request; state machine; transactional outbox; reference renderer; validation and similarity; assignment policy. |
| Workers | Asset sanitization, sealing, readiness, audit and event relay, sweeps (expiry, exceptions, evidence, verification, orphan cleanup), key rotation | Each under its own short-lived workload identity; idempotent; pending, succeeded and failed states; safe replay. Only the sealing worker writes sealed artefacts and manifests (ARC-05). |
| Data | Working store (relational), repository (private object store, bank index), audit store (chain, checkpoints, integrity events), quarantine store | The repository is physically and logically segregated from the authoring, review and accessibility environments (ARC-11). No reporting replica exposes content. |
| Enterprise | Identity provider, privileged-access management, key management, monitoring, malware scanning and data-loss prevention, endpoint management | Consumed, never built. Reached only through the egress allowlist. |
| Downstream | Assembly service | Reads the readiness record over mutual TLS; sends signed notifications; never receives content. |

## 10.2 Architecture requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| ARC-01 | Authorization is evaluated server-side on every request using role, assignment, version, language, lifecycle state, cycle policy, recognized capability and separation of duties. Client-supplied role claims are never trusted. | MUST |
| ARC-02 | Every state-changing operation and its audit record commit in the same database transaction. | MUST |
| ARC-03 | Domain and audit events are delivered from a transactional outbox after commit, at least once, with consumer-side deduplication by event identifier. | MUST |
| ARC-04 | Uploaded assets are unusable until they pass quarantine, validation, malware scanning, re-encoding and metadata stripping. | MUST |
| ARC-05 | The sealing worker runs under its own workload identity and is the only component permitted to write sealed artefacts and manifests. | MUST |
| ARC-06 | The downstream assembly consumer is reached only over mutual TLS with an audience-restricted workload token. | MUST |
| ARC-07 | The authoring environment operates default-deny egress and reaches only allowlisted enterprise endpoints. | MUST |
| ARC-08 | Workloads use short-lived workload identity. Static cloud credentials and embedded secrets are prohibited. | MUST |
| ARC-09 | Asynchronous jobs are idempotent, expose pending, succeeded and failed state, and support safe replay. | MUST |
| ARC-10 | Infrastructure administration through privileged-access management grants no application-level content access. | MUST |
| ARC-11 | The repository is physically and logically segregated from the authoring, review and accessibility environments. | MUST |
| ARC-12 | No component, dependency, endpoint, deployment artefact or runtime configuration provides AI capability. | MUST |
| PRD-ARC-13 | GAP D-38 Scope of ARC-12 after the decision: it binds Layer 1 (every zone in §10.1). Layer 2 is the only place a model runs. The connector is a client of Layer 2 with these properties: outbound only; requests carry curriculum references and parameters, never sealed content; responses are treated as untrusted input and pass sanitization, validation and the human gates; Layer 2 holds no credential for any Layer 1 store or endpoint; the AI-dependency scan (§13.2) fails the build if a model runtime or inference client appears in any Layer 1 artefact. | MUST |
| PRD-ARC-14 | GAP D-48 Translation drafts require the primary reference text to reach Layer 2. This is permitted only when Layer 2 runs inside the trust boundary (a private deployment with no data retention and no training on inputs) or when Security accepts a documented exception with the same guarantees contractually. Until then the translation-draft channel of the connector stays disabled and translators start from an empty variant. | MUST |

## 10.3 Security requirements

Non-negotiable. A failure here is disqualifying, not a defect.

| ID | Requirement | Priority |
| --- | --- | --- |
| SEC-01 | Sealed plaintext is not retrievable through any human or API interface — author, reviewer, accessibility specialist, translator, coordinator, operator, auditor or administrator. | MUST |
| SEC-02 | Correct-answer visibility is limited to the assigned author before submission, and to reviewers only where the ratified policy requires it. It is never exposed to coordinators, operators or administrators. | MUST |
| SEC-03 | Automated tests assert that no non-permitted role receives correct-answer or sealed-plaintext fields in any response body. | MUST |
| SEC-04 | Emergency evidence access sits outside the routine workflow and requires a separately approved, dual-authorized manual procedure. | MUST |
| SEC-05 | Authorization is server-side on every operation. Interface restrictions are convenience, never control. | MUST |
| SEC-06 | Separation of duties is provable through both the interface and a hand-crafted direct API call. | MUST |
| SEC-07 | Invalid lifecycle transitions are rejected with a conflict response and a descriptive message. | MUST |
| SEC-08 | Submitted, returned and sealed versions are immutable. No deletion operation exists for artefact content. | MUST |
| SEC-09 | Uploads are quarantined and only released after format allowlisting, signature inspection, malware scanning, re-encoding, metadata removal and decompression limits. | MUST |
| SEC-10 | Restricted-HTML sanitization uses an explicitly defined allowlist of tags, attributes and URL schemes. The permitted LaTeX subset is likewise defined and bounded. | MUST |
| SEC-11 | Transport is TLS 1.2 or above. Content-security policy, cross-site request forgery defence, output encoding, secure headers and no-store caching are all in place. | MUST |
| SEC-12 | Secrets live in the approved secret manager. None appear in source, logs, images or environment dumps. | MUST |
| SEC-13 | Backups are encrypted, access-separated, immutable, and restoration is tested. | MUST |
| SEC-14 | Support processes mask Restricted fields. No plaintext reaches tickets, screenshots, analytics or chat. | MUST |

## 10.4 Constraints the technology stack must satisfy

GAP D-28 The stack is the Technical Lead's proposal in Week 1. Any proposal is acceptable that provides all of the following; a proposal missing one is rejected.

- A relational database with serializable or equivalent transactions, row locks and constraint triggers, so state change, audit event and outbox message commit together. 
- A transactional outbox and a relay with at-least-once delivery and idempotent consumers. 
- A private object store with versioning and a compliance-mode retention lock whose period is configuration. 
- A key management service offering envelope encryption with per-object data keys, asymmetric signing and verification, per-identity key policies and a usage log. 
- Short-lived workload identities and mutual TLS for every service and worker; no static credentials anywhere. 
- Network policy capable of default-deny egress with an explicit allowlist, and of segregating the repository segment. 
- A server-push transport for the operator surface and My Work with resumable streams. 
- A deterministic, versioned server-side renderer for restricted HTML and the LaTeX subset that emits MathML and text alternatives, with no network access at render time. 
- An HTML sanitizer driven by an explicit allowlist and a LaTeX parser that rejects anything outside the grammar before rendering. 
- Integration with the enterprise malware scanner, monitoring platform and identity provider through their supported protocols. 
- A pipeline that builds immutable, signed artefacts, runs the mandated test suites (§13) on every change, and deploys to a clean environment with no manual step. 
- Infrastructure as code for every environment, with the authoring zone and repository zone as separate definitions. 
- No dependency, service, model file or runtime configuration that provides AI capability; the dependency manifest is scanned for this on every build (`ARC-12`). 

## 10.5 Asset pipeline

GAP Implements `ARC-04` and `SEC-09`.

| Step | Action | Rejection |
| --- | --- | --- |
| 1 | Upload lands in the quarantine store under a random key with status quarantined; the draft may reference it but validation fails until it is clean. | Size above the per-image limit is rejected before storage (ASSET_TOO_LARGE). |
| 2 | Format allowlist by magic bytes (PNG, JPEG) D-11; declared type must match. | Any other format, including SVG and polyglot files, is rejected. |
| 3 | Signature and structure inspection; pixel-dimension and decompression-ratio limits enforced before decoding. | Decompression bombs and malformed structures are rejected; a security event is raised. |
| 4 | Malware scan through the enterprise scanner. | Any detection rejects and raises a security event; scanner unavailable leaves the asset quarantined (fail closed). |
| 5 | Re-encode to a fresh PNG or JPEG, stripping all metadata; compute the checksum of the re-encoded bytes; store in the working store under the version. | — |
| 6 | Status clean; the asset becomes referenceable and renderable; the scan record is expected evidence at sealing. | — |

## 10.6 Break-glass procedure requirements

GAP Implements `SEC-04` and `ASM06-LFC-05`. The procedure is documented as a runbook by the Technical Writer and walked through once before go-live.

- It exists outside the routine workflow: no role surface offers it, and no routine identity can perform it. 
- It requires two named approvers from different functions (for example Security and Assessment), a ticket reference, a stated purpose (audit or dispute), a named artefact and a time box of at most 4 hours. 
- It is executed by a dedicated break-glass identity through privileged-access management, which decrypts the named sealed version in memory and renders it only inside the hardened studio; nothing is written to disk, exported or printed. 
- Every access writes `breakglass.accessed` to the audit chain with approvers, ticket, purpose, artefact and duration, and raises a security event to the monitoring platform. 
- It is tested in the closeout operations simulation with a synthetic artefact. 

## 10.7 Egress, secrets, environments

- Egress allowlist (`ARC-07`): identity provider, key management, monitoring platform, malware scanner, object store endpoints, assembly service endpoints, package mirror at build time only. Everything else is denied and logged. The client's content-security policy restricts connections to the application origin. 
- Secrets (`ARC-08`, `SEC-12`): only the approved secret manager; injected at runtime to workload identities; rotated; scanned for in source and images on every build. 
- Environments D-30: development and integration (synthetic content only, test identity tenant), staging (production-like, real enterprise services in test mode) and production. Immutable signed artefacts are promoted through them without rebuild. No real examination content exists outside production. 

# 11. Non-functional requirements

Each target is paired with how and when it is verified, so the evidence pack can show it was met rather than assumed.

| Category | Target | Verification | When |
| --- | --- | --- | --- |
| Capacity | 50 concurrent sessions; 100,000 artefacts; 500,000 immutable versions. | Load test with the synthetic corpus at 1.5× the stated volumes; queries stay within the latency targets. | Week 5 |
| Interactive performance | p95 authenticated read ≤ 2 s; p95 draft save ≤ 1.5 s, excluding upload transfer. | Load test at 50 sessions with autosave cadence; measured at the edge. | Week 5 |
| Queues and counts | p95 authorized queue or aggregate query ≤ 3 s. | Coordinator and My Work queries under full data volume. | Week 5 |
| Sealing | 95 % of valid image-bearing artefacts sealed within 30 s, with visible progress and safe retry. | Batch of 200 sealings under load; retry test with induced failures. | Week 4 – 5 |
| Telemetry latency | Signal to operator surface p95 ≤ 3 s; signal to durable audit p95 ≤ 5 s; never dropped. | Instrumented signals at 50 sessions × 2 events per second; count reconciliation. | Week 2, 5 |
| Telemetry capacity | 50 sessions at a sustained 2 events per second each, with burst headroom to 10. | Soak test for 1 hour; backlog stays under 60 s. | Week 5 |
| Heartbeat | 30-second interval; session flagged stale at 90 s. | Functional test. | Week 2 |
| Availability | 99.5 % monthly during declared authoring windows, excluding maintenance. | Failover and resilience tests; monitoring in place at go-live. | Week 5 |
| Recovery | RTO ≤ 4 h; RPO ≤ 15 min; autosave limits draft loss to ≤ 30 s. | Timed restore of all three stores followed by chain verification. | Week 5 |
| Accessibility | Role surfaces and reference rendering conform to WCAG 2.1 AA. | Pre-assessment in Week 3; formal audit in Week 5 with findings closed. | Week 3, 5 |
| Localization | Unicode end to end; locale-aware interface; right-to-left readiness; no loss across pilot scripts. | Round-trip corpus in the pilot scripts through sanitize, canonicalize, seal and verify. | Week 4 |
| Security | No open Critical or High finding at production authorization. | External penetration test starting Week 3; triage and closure in Week 5. | Week 5 |
| Observability | Every request and job carries trace and correlation identifiers; dashboards contain no content. | Trace sampling review; dashboard content scan against the synthetic corpus. | Week 1, 5 |
| Data integrity | Canonical hashes stable across repeat serialization and backup or restore. | Stability corpus on every build; restore test. | Every build; Week 5 |
| Audit chain throughput GAP | ≥ 200 events per second sustained; p95 chain write ≤ 50 ms. | Benchmark before Week 2 features are built on it. | Week 1 |

# 12. Edge cases and required behaviour

A system that returns a server error or behaves incorrectly on these inputs is not acceptable. Each case names the error code from §7.2 where one applies.

## 12.1 Authoring and lifecycle

| Case | Required behaviour | Code |
| --- | --- | --- |
| Empty or whitespace-only stem, option or explanation | Rejected with field-level validation detail; the interface validates before submission. | VALIDATION_FAILED / VAL-SCHEMA-01 |
| Fewer than 2 or more than 8 options, duplicate options, or zero or multiple correct answers | Rejected with specific field errors. | VAL-OPT-01/02, VAL-ANS-01 |
| Edit attempted on a version in review, in accessibility check, or sealed | Rejected as a conflict; the interface disables editing with an explanatory message. | CONFLICT_INVALID_TRANSITION |
| Taxonomy value that has been retired | Rejected for new use; existing versions retain their original reference. | TAXONOMY_RETIRED |
| Author submits a subject outside their assignment | Request-body value ignored in favour of the assignment, or rejected. | FORBIDDEN_NOT_ASSIGNED |
| Author reaches the configured artefact cap | Creation blocked with a clear message; visible to the coordinator. | AUTHOR_CAP_REACHED |
| Empty queue | Explanatory empty state. No spinner, no error. | — |
| Withdraw attempted after submission GAP | Rejected as a conflict; withdrawal exists only for unsubmitted drafts. | CONFLICT_INVALID_TRANSITION |
| Cycle closed while a draft is open GAP | The open draft can still be submitted and reviewed; creation of new drafts is refused. | CYCLE_INACTIVE |

## 12.2 Review and accessibility

| Case | Required behaviour | Code |
| --- | --- | --- |
| Two reviewers open the same assignment | Both may open. The second decision is rejected as already decided, and that reviewer's queue refreshes with a clear message. | CONFLICT_ALREADY_DECIDED |
| Reviewer attempts to decide on their own authored or translated version | Rejected. Filtered from the queue and independently validated at the decision endpoint. | FORBIDDEN_DUTY_CONFLICT |
| Rationale or findings below the required minimum | Rejected with field detail; controls stay disabled until satisfied. | VALIDATION_FAILED |
| Accessibility specialist opens a version the reviewer has since returned | State no longer valid; decision rejected as a conflict and the queue refreshes. | CONFLICT_STATE_CHANGED |
| Assigned reviewer leaves or loses recognized capability mid-task | Assignment released and returned to the pool; no task is orphaned; decisions already recorded remain valid. | FORBIDDEN_CAPABILITY_EXPIRED on their next request |
| Task passes its expiry | Released to the pool, audited, and visible in coordinator aging. | — |
| Artefact cannot be delivered under a declared accommodation | Recorded as needing an equivalent route and escalated; not silently approved. | — |
| Second of two required reviewers returns after the first approved GAP | The return wins: a new draft is created and the first approval remains as evidence on the returned version. | — |

## 12.3 Translation and equivalence

| Case | Required behaviour | Code |
| --- | --- | --- |
| Variant changes a numeric value, unit, or the position of the correct option | Blocking structural check; submission rejected with the failing check named. | STRUCTURAL_CHECK_FAILED |
| Structural override attempted without a recorded exception | Rejected. A valid, unexpired exception permits it and is audited. | EXCEPTION_REQUIRED |
| Primary corrected after variants are sealed | Readiness revoked; dependent variants marked for revalidation; changes shown to translators. | — |
| Exception expires between request and submission GAP | Submission rejected; the translator sees that the exception expired and can request a new one. | EXCEPTION_REQUIRED |
| Required language added to an Active cycle after primaries are sealed GAP | Readiness of every sealed artefact in the cycle is revoked; a variant draft and translation task are created for each; the coordinator is warned before confirming. | — |

## 12.4 Assets and rendering

| Case | Required behaviour | Code |
| --- | --- | --- |
| Malicious upload — script payload, polyglot file, hostile metadata, decompression bomb | Blocked at quarantine; never referenceable; security event raised. | ASSET_REJECTED |
| Oversized image or asset budget exceeded | Rejected before processing with a clear limit message. | ASSET_TOO_LARGE |
| Meaningful image without alternative text | Blocking validation finding. | VAL-ASSET-02 |
| LaTeX outside the permitted subset, or pathologically expensive input | Rejected with a bounded-subset message; no unbounded rendering work. | VAL-EQN-01/02 |
| Renderer output differs between author preview and review | Treated as a defect, not a variance — the accessibility approval depends on identity. | — |
| Scanner unavailable during upload GAP | Asset stays quarantined; the author sees "scan pending"; validation blocks submission until clean; an operational alert fires if the backlog exceeds 15 minutes. | DEPENDENCY_UNAVAILABLE |

## 12.5 Sealing and evidence

| Case | Required behaviour | Code |
| --- | --- | --- |
| Key management, audit, scanner or object store unavailable at sealing | Fail closed. No partially sealed artefact. Safe retry succeeds after recovery. | Job failed: DEPENDENCY_UNAVAILABLE |
| Sealing job repeated or replayed | Idempotent. One sealed artefact, one manifest. | — |
| Expected evidence for a completed step is missing | Sealing blocked and an alert raised naming the step and the absent record. | — |
| Manifest or content hash fails verification | Surfaced as a Critical alert, not a silent log line; runbook invoked. | — |
| Readiness interface called with a human token or wrong-audience workload token | Rejected. Only the approved workload identity succeeds. | REJECTED_AUDIENCE |
| Selection notification names an artefact that is not ready GAP | Whole notification rejected listing the identifiers and states; nothing transitions; operational alert if the artefact is Used, Archived or Retired. | SELECTION_NOT_READY |
| Selection notification replayed GAP | Original result returned; no second transition; audit records the replay. | — |

## 12.6 Monitoring, session and identity

| Case | Required behaviour | Code |
| --- | --- | --- |
| Telemetry submission fails | Recorded locally in memory, retried with backoff, never discarded, and never blocks the user's typing. | — |
| Integrity score would fall below zero | Floored at 0. Never negative. | — |
| Alert already displayed and a further critical signal occurs | Existing alert updated, not duplicated. | — |
| Operator transport drops | Reconnecting state with exponential backoff; on reconnect, session state re-synchronized. | — |
| Developer tools opened | Highest-severity signal recorded and referred. | — |
| User signs in from two tabs | Both function; one session record; concurrent-tab signal recorded. | — |
| Valid token, no provisioned account, or a role claim matching no known role | Clear "not provisioned — contact your administrator" screen; access denied and a security event raised. | NOT_PROVISIONED |
| Access token expires mid-session | Silently refreshed. If the refresh window has also expired, redirect to sign-in with unsaved draft state preserved in memory and re-applied on return. | AUTH_REQUIRED |
| Recognized capability revoked during an active session | Next request denied; active assignment becomes unactionable. | FORBIDDEN_CAPABILITY_EXPIRED |
| Device posture becomes non-compliant during a session GAP | The next token refresh fails the posture check; the session is ended with reason and a security event; the draft's last autosave is intact. | FORBIDDEN_DEVICE_POSTURE |

# 13. Test and verification strategy

GAP The specification's Definition of Done requires automated tests, an authorization oracle, no-content assertions and evidence. This section names the suites, what each proves, and when it runs, so the QA Lead can refuse a week's closure on evidence.

## 13.1 Levels

- Unit: canonicalization, hashing, validation rules, structural checks, similarity, scoring, state machine, policy evaluation. 
- Contract: every endpoint against the published interface definition; the definition is generated from or verified against the implementation on every build (`INT-01`). 
- Integration: workflow end to end on a clean environment with the synthetic corpus; outbox delivery; sealing with real key management and object store in the integration tenant. 
- Security and negative: the suites in §13.2 that must fail the build. 
- Non-functional: load, soak, resilience, failover, restore, accessibility, penetration. 
- Acceptance: the Definition of Done in §17 executed with real role users and recorded in the evidence pack. 

## 13.2 Mandated automated suites

| Suite | What it proves | Requirements | Runs |
| --- | --- | --- | --- |
| Authorization matrix oracle | For every operation in §4.3 and every role, the allowed cells succeed and every other cell is denied with the expected code; includes a wrong-role case and a separation-of-duties case per operation. | INT-09, ARC-01, SEC-05, SEC-06, INS04-CAP-07/08/09 | Every build from Week 2 |
| Direct-API duty conflict | A multi-role user who authored version V is refused approval of V by a hand-crafted request that bypasses the interface. | SEC-06 | Every build |
| No-content assertions | Every string of the synthetic corpus is absent from: logs, traces, telemetry events, audit events, domain events, notifications, operator and evidence responses, readiness responses, error bodies, URLs, metrics and dashboards exports. | DAT-03, ASR01-EVD-09, ASR02-OBS-16/17/18, ASM07-RDY-03, INT-05 | Every build from Week 2 |
| Correct-answer exposure | No non-permitted role receives the correct-answer field or sealed plaintext in any response body, including list endpoints. | SEC-01, SEC-02, SEC-03 | Every build |
| Canonicalization stability | The sealed corpus re-canonicalizes to identical bytes and hashes on every platform in the pipeline. | DAT-05, DAT-06 | Every build |
| Chain construction and verification | Verification passes on seeded data; an altered, removed or reordered event in a copy is detected with the right failure kind; checkpoints verify. | ASR01-EVD-02/03 | Every build; Week 1 closure |
| Expected-evidence completeness | Deleting any declared record blocks sealing with an alert naming the step and record. | ASR01-EVD-05/06 | Every build from Week 3 |
| Injection and sanitization | Prohibited markup, scripts, external URLs, LaTeX macros and pathological inputs are rejected or stripped with warnings. | SEC-10, ASM03-VAL-01 | Every build |
| Malicious upload | Script payloads, polyglots, hostile metadata, decompression bombs and disallowed formats are blocked at quarantine and raise security events. | SEC-09, ARC-04 | Every build |
| Concurrency | Stale writes are rejected without loss; concurrent decisions produce exactly one accepted decision; replayed sealing produces one artefact and manifest; replayed notifications produce one transition. | INT-03/04, ASM05-VLT-07, ASM06-LFC-01 | Every build |
| Telemetry schema | Events with any additional property are rejected; the persisted and forwarded event sets match the schema exactly. | ASR02-OBS-16/17 | Every build (build-failing) |
| Machine-interface authentication | Human tokens, wrong-audience tokens, expired tokens, bad signatures and replays are refused; the approved identity succeeds. | ASM07-RDY-04, ARC-06, INT-02 | Every build from Week 4 |
| Lifecycle transitions | Every row of §5.3 succeeds under its conditions and every other transition is refused with a conflict. | SEC-07, SEC-08 | Every build |
| Accessibility automation | Automated WCAG checks on every role surface and on renderings of the corpus; keyboard-path tests for editor, checklist and option selection. | UI-13, §11 | Every build from Week 3 |
| AI-dependency scan | The Layer 1 dependency manifests and container images contain no model runtime, model file or inference client; the only outbound AI call is the connector client (§1.5). | ARC-12, PRD-ARC-13 | Every build |

## 13.3 Expert and manual verification

- External penetration test starting Week 3 against the integration environment, repeated on the release candidate in Week 5; Critical and High findings closed before authorization. 
- Accessibility pre-assessment in Week 3 and a formal WCAG 2.1 AA audit in Week 5 by the Accessibility Specialist, covering role surfaces and the reference rendering. 
- Multilingual user-acceptance testing in Week 5 with the named authors, reviewers, accessibility professional and translators, executing §17.2 on synthetic content in three languages. 
- Operations simulation in closeout: dependency outage during sealing, stuck sealing job replay, credential revocation mid-task, break-glass access, incident escalation. 
- Restore drill in Week 5: timed restore of all stores followed by full chain verification and manifest verification. 

## 13.4 Synthetic corpus

- Built in Week 1: a generator producing realistic but synthetic questions in the three pilot languages with images, tables and equations, plus deliberately invalid, near-duplicate, malicious and pathological cases. 
- Every corpus string is registered so the no-content suites can search for it; the corpus is versioned with the code. 
- No real examination content ever exists outside production. 

## 13.5 Evidence pack

One shared pack, assembled in closeout, containing for every §17 criterion: the test or procedure that proves it, its output, the date, and the signature of the named owner. It includes the load-test reports, the restore-drill timing, the verification reports, the penetration-test closure, the accessibility audit, the user-acceptance sign-offs and the go-live decision.

# 14. Delivery plan — start line to finish line

Five build weeks and a three-day closeout. Closure is evidence, not demonstration: a week is closed when a named owner has signed the stated proof. The QA Lead holds the authority to refuse a week's closure; the Product Owner escalates an unclosed week the same day.

## 14.0 Week 0 — the start line

| Before Week 1, day 1 — nothing below may be open 1. Every role in §14.7 is named and full-time for its stated weeks; the two named authors, two reviewers, accessibility professional, two translators, review coordinator and integrity operator have reserved same-day capacity. 2. Every precondition in §16.1 has a named owner. 3. The three pilot languages are named D-29; glossary and curated reference sources are available for each. 4. The assembly team is named and has agreed to the machine contracts in §6.10 – §6.12 and the delivery mechanism for supersession D-25. 5. Integration tenants exist for the identity provider, key management, object store, malware scanner and monitoring platform, reachable from the integration environment. 6. Every decision in §15 marked "Week 0" or "Week 1" is scheduled with its owner. 7. The team has read this document and the specification and has raised no blocking question. |
| --- |

## 14.1 Week 1 — Foundation and evidence backbone

Goal. Close the decisions, stand up the pipeline, and prove the two mechanisms every later week depends on: the hash-chained audit trail and telemetry ingest.

#### What is built

- Integration environment, delivery pipeline, signed build baseline, synthetic corpus generator (§13.4). 
- Identity sign-in with pseudonymization; cycle and taxonomy configuration with seed data; capability registry with validity windows (§6.1, §6.2). 
- Artefact, lineage and version model; the canonicalization rule implemented to the ratified specification with the stability corpus (§8.4). 
- Transactional outbox, hash-chained audit with genesis and checkpoints, runnable chain verification, throughput benchmark (§6.13). 
- Session registration and telemetry ingest with the schema test (§6.14). 
- Device posture and network-zone check for sign-in (`INS04-CAP-11`). 
- Published interface definition v1 with the resource catalogue of §7.3 and the error contract of §7.2. 
- Walking skeleton: sign in → create a draft → persist → chained audit event. 

#### Closure — all of the following, evidenced

- Every decision in §15 due by Week 1 is ratified in writing, with the canonicalization rule fixed and versioned. 
- A clean environment deploys from the pipeline with no manual step. 
- Chain verification passes on seeded data and detects a deliberately altered event. 
- A telemetry signal reaches durable audit within the stated latency and carries no content. 
- Sign-in from a non-compliant device is refused and raises a security event. 
- The chain writer meets the throughput target in §11. 
- No design question remains open that would block Week 2. 

Full time: Technical Lead, DevSecOps Engineer, 2 Backend Engineers, 1 Frontend Engineer, QA Lead, Product Owner. Assessment and Security decision owners on call with a one-business-day turnaround.

## 14.2 Week 2 — Authoring, monitored from the first keystroke

Goal. An author completes create-to-submit inside the hardened tool, and every action is already captured.

#### What is built

- My Work and assignment-scoped authorization gated on a current capability entry (§6.3). 
- Single-select editor, classification metadata, autosave, optimistic concurrency, save-state feedback (§6.4). 
- Restricted rich text with the allowlist, asset quarantine and sanitization pipeline (§10.5), equation rendering in the subset, alternative-text enforcement. 
- In-tool resources: reference material, symbol and equation palettes, glossary (`ASM03-ATH-13`). 
- Reference renderer, used identically by preview and both later gates (`PRD-ATH-18`). 
- Deterministic validation catalogue, bank-wide similarity check (`ASM03-VAL-06`), immutable submission, content hash, receipt (§6.5). 
- Client signal capture, integrity scoring and the in-workspace integrity panel (§6.14). 
- Authorization matrix oracle and no-content suites running in the pipeline (§13.2). 

#### Closure — all of the following, evidenced

- A representative author creates, validates, previews, autosaves and submits without assistance. 
- A deliberate copy attempt is blocked, scored, visible to the operator and durable in the audit chain within the stated latency. 
- A near-duplicate of a seeded bank question is refused at submission, naming the match. 
- A stale write is rejected without data loss; a page refresh restores equivalent state. 
- Authorization-bypass, injection, malicious-upload and concurrency tests pass. 
- No Restricted content appears in any log, trace, telemetry event or error message. 

Full time: Technical Lead, 2 Backend Engineers, 2 Frontend Engineers, QA Lead, QA Automation Engineer, Product Designer, DevSecOps Engineer, Product Owner. Named Author available daily for usability feedback.

## 14.3 Week 3 — Both approval gates, and the operator surface

Goal. Independent approval is enforced and un-bypassable, and the operator can see the floor in real time.

#### What is built

- Policy-driven assignment on subject, language, workload, capability and separation of duties (§6.3). 
- Review workspace in read-only mode, mandatory checklist, immutable decisions (§6.6). 
- Reviewer attestations for language, public-domain and scope compliance (`ASM03-REV-11`) and difficulty assignment (`ASM03-REV-12`). 
- Accessibility workspace on the reference renderer, structured findings, accommodation capability, equivalent-route flagging (§6.7). 
- Return lineage, remediation routing, locking, expiry, reassignment. 
- Expected-evidence model and the blocking completeness assertion (§6.13). 
- Operator surface: live sessions, event feed, drill-down, threshold referral, reconnection (§6.14). 
- Evidence view or scripted procedure D-27. 
- External penetration test and accessibility pre-assessment begin. 

#### Closure — all of the following, evidenced

- The full primary lifecycle reaches approved-for-sealing with real role users. 
- A multi-role user is refused approval of their own work through the interface and through a hand-crafted API call. 
- A return produces a new linked draft carrying findings; the returned version stays immutable. 
- Deleting an expected evidence record blocks the next transition and raises the alert. 
- An expired capability blocks new assignment and flags in-flight work without voiding recorded decisions. 
- Keyboard and screen-reader review of both gate workspaces passes. 

Full time: Technical Lead, 3 Backend Engineers, 2 Frontend Engineers, QA Lead, QA Automation Engineer, Accessibility Specialist, DevSecOps Engineer, Product Owner. Named Reviewer and Accessibility Professional available daily.

## 14.4 Week 4 — Translation, equivalence, sealing and handoff

Goal. The artefact reaches readiness in three languages, content leaves human reach, and the downstream contract is live.

#### What is built

- Translation tasks, read-only primary comparison, structural locks and blocking equivalence checks, reviewer equivalence judgement, exception path with expiry (§6.8). 
- Target-language accessibility check. 
- Correction authorization and seeding, readiness revocation, variant revalidation with change visibility (§6.11). 
- Sealing worker: revalidation, canonicalization, sanitization, encryption, signed manifest, immutable retention, bank indexing including difficulty and the similarity fingerprint (§6.9). 
- Readiness calculation and the machine-only interface on workload identity (§6.10). 
- Downstream lifecycle states Used and Archived with the signed notification contracts (§6.12); supersession notification and acknowledgement. 
- Idempotent retry, dependency-outage handling, tamper verification, post-sealing access denial. 

#### Closure — all of the following, evidenced

- One primary plus two language variants reach readiness; every manifest verifies. 
- A variant that changes a numeric value or the position of the correct option is refused, naming the failing check. 
- No human role — including administrator — can retrieve sealed plaintext. 
- A human token and a wrong-audience workload token are both refused by the readiness interface; the approved identity succeeds. 
- A simulated selection notification moves the primary and both variants to Used atomically; exam completion moves them to Archived. 
- Key management, audit, scanner or object-store failure leaves no partially sealed artefact, and retry succeeds after recovery. 

Full time: Technical Lead, 3 Backend Engineers, 2 Frontend Engineers, QA Lead, QA Automation Engineer, DevSecOps Engineer, Accessibility Specialist, Product Owner. Named Translators for both pilot languages available daily.

## 14.5 Week 5 — Harden, install, qualify

Goal. A release candidate is installed in production with the evidence required to authorize it.

#### What is built

- Production infrastructure and installation from immutable promoted artefacts. 
- Real identity, key management, object lock with the ratified retention period, scanning, monitoring, alerting, backup and restore. 
- Load, soak, resilience, failover, recovery and data-integrity verification against §11. 
- Formal penetration test and WCAG 2.1 AA audit, with findings closed. 
- Multilingual user-acceptance testing and priority defect closure. 
- Runbooks (sealing failure, chain verification failure, break-glass, dependency outage, credential revocation, restore), support model, on-call ownership, access review, rollback plan. 

#### Closure — all of the following, evidenced

- The release candidate is installed in production and smoke-tested with representative role accounts. 
- No unresolved Critical or High finding from the penetration test or the accessibility audit. 
- Stated capacity, latency and recovery targets are met under load, with evidence retained. 
- Backup, restore and chain verification pass end to end, and hashes still verify after restore. 
- Every runbook has a named owner and has been walked through once. 
- Assurance leads recommend release in writing. 

Full time: Technical Lead, 2 Backend Engineers, 1 Frontend Engineer, QA Lead, QA Automation Engineer, DevSecOps Engineer, Security Engineer, Accessibility Specialist, Product Owner, Technical Writer.

## 14.6 Closeout — the finish line

| Three days — prove readiness, transfer ownership, decide on evidence Done: production smoke test with approved synthetic content and representative role accounts; seal and hash verification, alert test, access recertification, backup-restore spot check; operations simulation (dependency outage, stuck sealing job, credential revocation, break-glass, incident escalation); evidence-pack assembly, support handover, two-week hyper-care roster. Closed when: every acceptance criterion in §17 is signed in one shared evidence pack; Product, Architecture, Security, Accessibility, Content Operations, QA and Operations have each signed; support ownership and the hyper-care roster are active and named; the go-live decision is recorded with its rationale. Full time: Technical Lead, DevSecOps Engineer, QA Lead, Product Owner, Security Engineer, plus every approver named above for sign-off. |
| --- |

## 14.7 People

Every role is full-time on this MVP for its stated weeks — not shared with another delivery, not on standby, not attending as a reviewer. The five-week window has no float, so a person who is 50 % allocated is a 100 % risk. Peak concurrent size is twelve people in Weeks 3 and 4; below ten in those weeks the plan does not hold.

| Role | Count | Weeks | Owns |
| --- | --- | --- | --- |
| Technical Lead / Architect | 1 | 1 – 5 + closeout | Canonicalization rule, trust boundaries, sealing design, the final technical call. Accountable for the architecture holding under audit. |
| Backend Engineer | 3 | 1 – 5 | Domain model, workflow and policy engine, validation, sealing worker, telemetry ingest, readiness interface. |
| Frontend Engineer | 2 | 2 – 5 | Authoring, review, accessibility and translation surfaces; hardened editor; operator console; four screen states throughout. |
| DevSecOps Engineer | 1 | 1 – 5 + closeout | Pipeline, environments, workload identity, key management, egress control, monitoring, backup and restore. |
| QA Lead | 1 | 1 – 5 + closeout | Test strategy, the authorization matrix as test oracle, evidence pack. Holds the authority to refuse a week's closure. |
| QA Automation Engineer | 1 | 2 – 5 | Authorization, duty-conflict, injection, upload, concurrency and no-content assertions running in CI from Week 2. |
| Product Owner / Business Analyst | 1 | 1 – 5 + closeout | Scope discipline, decision chasing, acceptance criteria, and saying no. Escalates an unclosed week the same day. |
| Product Designer | 1 | 2 – 4 | Interaction design for four role surfaces plus the operator console; accessible by construction, not by remediation. |
| Accessibility Specialist | 1 | 3 – 5 | Accessibility gate design, WCAG conformance, accommodation model, and the audit. |
| Security Engineer | 1 | 5 + closeout | Penetration test coordination, finding triage, production authorization. |
| Technical Writer | 1 | 5 | Runbooks, support model, operating documentation. |
| Technical & Functional Expert | 2 | Daily | Domain expertise. |

#### Content Operations — named individuals with reserved same-day capacity

| Role | Count | Commitment | Needed for |
| --- | --- | --- | --- |
| Author (subject expert) | 2 | Daily, Weeks 2 – 5 | Authoring usability, realistic content, acceptance testing. |
| Reviewer | 2 | Daily, Weeks 3 – 5 | Review workspace, checklist design, attestation practicality. |
| Certified Accessibility Professional | 1 | Daily, Weeks 3 – 5 | Accessibility gate, accommodation capability, equivalent-route judgements. |
| Translator | 2 (one per pilot language) | Daily, Weeks 4 – 5 | Translation workspace, glossary, equivalence judgement. |
| Review Coordinator | 1 | Weeks 1 – 5 | Cycle and taxonomy configuration, assignment policy, aging. |
| Integrity Operator | 1 | Weeks 3 – 5 | Operator surface design, severity table, referral behaviour. |

## 14.8 Build order and critical path

- Walking skeleton first. Sign-in, one draft, one audit event, one telemetry event, deployed from the pipeline — before any feature. 
- Audit chain and telemetry before features, because Week 2 closure needs a copy attempt durable in the chain, and the chain's throughput must be known before it carries telemetry. 
- The renderer in Week 2, because three gates and the sealed rendition all depend on its identity; changing it later invalidates accessibility approvals. 
- The authorization oracle from Week 2, so every endpoint added in Weeks 3 and 4 is born with its matrix row. 
- Design the sealing worker in Week 1, build it in Week 4. Its key policy, object lock and identity need the enterprise services provisioned early; its code needs the approvals that only exist after Week 3. 
- Assembly contract agreed by Week 2, so the Week 4 readiness and notification work is not blocked on negotiation. 
- Critical path: decisions D-01, D-02, D-14, D-28 → skeleton and chain → editor and renderer → gates and evidence model → sealing and machine contracts → hardening and audit. A slip in any of the first three weeks cannot be recovered. 

## 14.9 If you find yourself building this, stop

| Tempting thing | Why it is out |
| --- | --- |
| Any logic that chooses which questions go in a paper, counts coverage against a blueprint, or balances difficulty | ASM-02 and ASM-07 live in the assembly service. |
| A model, embedding, classifier or "smart" suggestion of any kind | ARC-12; every judgement is a person or a fixed rule. |
| Audio, video, captions or a generic file-attachment type | Multimedia is excluded; keep the data model extensible and stop there. |
| A local password, remember-me, or account-creation form | INS04-CAP-01; the identity provider is the only authority. |
| A download, export, print or "open in new tab" control on any content surface | ASM03-ATH-10; content leaves only by sealing. |
| An administrator screen that lists or previews artefact content | SEC-01, ARC-10; no role can browse content. |
| A "publish", "approve for exam" or "seal now" button | ASM05-VLT-01; the system seals. |
| An Approve or Reject control on any Admin screen | INS04-CAP-07 and D-46; the Admin authors, so the Admin never decides a review stage. |
| A model that scores, ranks, validates, reviews or approves a question, or any Layer 1 code that imports an inference client other than the connector | D-38 and PRD-ARC-13: AI may draft, never judge; Layer 2 is the only place a model runs. |
| Estimating discrimination, calibrating difficulty from anything | ASM-06; requires exam data that does not exist. |
| Delivering sealed content to candidates or to anyone | Separate phase with separate owners. |

# 15. Decision register

Every decision the specification defers to "the ratified rule", "configuration" or "the team" is listed here with a proposed default so that nothing blocks Week 1 for want of an answer. A proposed default becomes the ratified value when its owner signs it; until then the software carries it as configuration marked proposed.

| ID | Decision | Proposed default | Owner | Needed by |
| --- | --- | --- | --- | --- |
| D-01 | Canonicalization rule v1 | §8.4 as written; JCS container, NFC, deterministic DOM serialization, options in display order, integers or decimal strings, asset checksums included. | Technical Lead | Week 1 |
| D-02 | Hash algorithm, chain granularity, checkpoints | SHA-256; one global per-event chain with a single writer; signed checkpoints every 10,000 events or hourly, anchored in the monitoring platform. | Technical Lead, Security | Week 1 |
| D-03 | Integrity signal severity table | §6.14 catalogue with the listed decrements. | Integrity Operator, Security | Week 2 |
| D-04 | Referral threshold | Refer at score ≤ 50. | Integrity Operator, Security | Week 2 |
| D-05 | Who maintains the capability registry | Coordinator role with re-authentication; every change audited; optional two-person rule deferred. | Product Owner | Week 1 |
| D-06 | Reviews required per cycle; reviewer sees the correct answer | One review for the pilot cycle; reviewer sees the key (true). | Assessment decision owner | Week 3 |
| D-07 | Remediation repeats review policy | repeat_when_content_changed with "changed" as defined in §5.4. | Assessment decision owner | Week 3 |
| D-08 | Similarity algorithm and threshold | Word 3-gram Jaccard over normalized stem plus options; block at ≥ 0.80; same-language comparison across the whole bank. | Assessment owner, Technical Lead | Week 2 |
| D-09 | Restricted-HTML allowlist | PRD-ATH-16. | Technical Lead, Security, Accessibility Specialist | Week 2 |
| D-10 | Permitted LaTeX subset and bounds | PRD-ATH-17. | Technical Lead, Accessibility Specialist, subject experts | Week 2 |
| D-11 | Field limits, image formats and budgets | PRD-ATH-14; PNG and JPEG only. | Product Owner | Week 2 |
| D-12 | Assignment expiry per task type; unassigned alert delay | Review 5 business days; accessibility 5; translation 10; translation review 5; revalidation 5; alert after 8 hours unassigned. | Review Coordinator | Week 3 |
| D-13 | Author cap default; open-task workload cap | 40 artefacts per author per cycle; 10 open tasks per user. | Review Coordinator | Week 2 |
| D-14 | Session lifetimes, inactivity timeout, re-authentication list, posture freshness | PRD-CAP-14; posture assertion no older than 30 minutes. | Security | Week 1 |
| D-15 | Exception maximum validity and approver role | 30 days; Coordinator approves with re-authentication; approver ≠ requester. | Assessment owner, Security | Week 4 |
| D-16 | How a correction draft obtains sealed content | System-seeded draft under a recorded authorization by a dedicated seeding identity (PRD-COR-08); never a read interface. | Security, Assessment owner | Week 4 |
| D-17 | Declared-accommodation vocabulary; whether "needs equivalent route" blocks readiness | screen_reader, magnification, high_contrast, large_print, reader, scribe, extended_time, braille, colour_overlay; does not block; flagged on readiness and escalated. | Accessibility Specialist | Week 3 |
| D-18 | Difficulty, taxonomy-level and complexity vocabularies | Difficulty: Easy, Moderate, Hard, Very hard. Taxonomy level: Remember, Understand, Apply, Analyse, Evaluate, Create. Complexity: Low, Medium, High (author-declared, distinct from reviewer-assigned difficulty). | Assessment decision owner | Week 1 |
| D-19 | Checklist text, reason codes, out-of-band notification channel | §6.6 templates and codes; in-app notifications only for the MVP. | Assessment owner, Content Operations | Week 3 |
| D-20 | Unsaved draft preservation across forced re-authentication | In-memory state plus autosave before redirect; no persistent browser storage. | Technical Lead | Week 2 |
| D-21 | Paste and drag-and-drop in the hardened editor | Blocked and reported; the glossary and palettes insert through their own controls. | Security, named Authors | Week 2 |
| D-22 | Automatic session suspension | Off. Enabling is an operational decision recorded in configuration. | Operations | Week 3 |
| D-23 | Localized numerals in variants | Numeric values preserved verbatim; an exception is the only route to change one. | Translators, Assessment owner | Week 4 |
| D-24 | Retention lock period for sealed objects and manifests | No default. Must be supplied in writing; the software refuses to seal without it. | Content Operations, Legal | Week 4 |
| D-25 | Supersession delivery mechanism and acknowledgement window | Mutual-TLS webhook to registered consumers; 24-hour window. | Assembly team, Technical Lead | Week 2 (agree), Week 4 (live) |
| D-26 | Selection notification atomicity | All-or-nothing per notification. | Assembly team | Week 4 |
| D-27 | Evidence view versus scripted procedure (P1) | Build the minimal view; fall back to the script only if Week 3 capacity is strained, with equivalent output. | Product Owner, QA Lead | Week 3 |
| D-28 | Technology stack and hosting | Technical Lead's proposal evaluated against §10.4. | Technical Lead, DevSecOps | Week 1 |
| D-29 | Pilot languages (primary plus two) | To be named. | Content Operations | Week 0 |
| D-30 | Environments and production topology | §10.7; four environments; repository zone separate. | DevSecOps | Week 1 |
| D-31 | Classification and location of similarity fingerprints | Restricted derived data in the repository tier; never exposed. | Security | Week 2 |
| D-32 | Chain event volume for autosave | Draft saves are aggregated into one audit event per draft per minute with a count; individual saves are not chained. | Technical Lead | Week 1 |
| D-33 | Telemetry batch size and ingest limits | 50 events per batch; 2 per second sustained and 10 burst per session. | Technical Lead | Week 1 |
| D-34 | Exclusion pairs (SHOULD) in scope | Yes, if Week 4 capacity allows; otherwise dropped with a note in the evidence pack. | Product Owner | Week 3 |
| D-35 | Evidence sweep (SHOULD) cadence | Daily. | QA Lead, Operations | Week 5 |
| D-36 | Who may see the author's identity | Only the coordinator, on assignment screens, for assignment purposes. Never reviewers or specialists. | Product Owner, Security | Week 2 |
| D-37 | Two-tab behaviour for content surfaces | Both tabs function; one session record; concurrent-tab signal recorded (per specification). | Security | Week 2 |
| D-38 | AI generation and AI translation drafts (Sarvam) versus ARC-12 | Decided 7 September 2026 (Product Owner): in scope for the MVP and the demo as Layer 2. AI may draft, never judge: candidates, translation first drafts and metadata suggestions enter as Drafts with provenance and pass the identical human pipeline; no AI in validation, similarity, review, accessibility, sealing, readiness or monitoring; Layer 2 runs outside the hardened zones behind the single connector (§1.5, PRD-ARC-13). ARC-12 is re-worded to bind Layer 1. | Product Owner (decided); Security ratifies the connector controls | Decided; Security by Week 1 |
| D-39 | Admin download and export | None from the question bank for any role; paper export belongs to the assembly module under release custody (DAY-01). | Product Owner, Security | Week 1 |
| D-40 | In-product assembly by the Admin | Build assembly as a separate module consuming the readiness interface; selection by metadata against the blueprint (blind assembly); rendering through release custody, never through authoring surfaces. | Product Owner, Technical Lead | Week 2 |
| D-41 | Admin "Delete question" | Withdraw for unsubmitted drafts, Retire for approved or sealed questions; nothing physically deleted. | Product Owner | Week 1 |
| D-42 | Admin "View all questions" | Allowed for unsealed versions because the Admin authors everything in V1; sealed versions expose metadata only. | Security | Week 1 |
| D-43 | Accessibility check per language version | Keep (specification MUST); the variant remediation is small. Deferral for the pilot is a documented drop. | Accessibility Specialist, Product Owner | Week 3 |
| D-44 | Question types beyond single-select MCQ | Item type stays data; other types enter only when enabled per cycle with a named reduced rule set. | Assessment decision owner | Week 2 |
| D-45 | Admin holding the Auditor and Integrity Operator views | Permitted (content-free surfaces); a distinct Integrity Operator person is recommended for the pilot. | Security | Week 3 |
| D-46 | Admin Approve and Reject in the engineering RBAC matrix | Removed: the Admin authors, so cannot decide any review stage; the Admin assigns, reassigns, releases and authorizes corrections. | Product Owner | Now (Week 1) |
| D-47 | Source information visible to reviewers | Subject, grade, curriculum name, chapter and page range; never the stored source context text, the blueprint or the assessment. | Security, Assessment owner | Week 2 |
| D-48 | Hosting model for Layer 2 translation drafts, which need the primary text | Private in-boundary deployment of the model with no retention and no training on inputs; otherwise the translation-draft channel stays off and translators start from an empty variant. Generation needs no pipeline content and may use the external service. | Security, Technical Lead | Week 2 |

# 16. Preconditions, dependencies, risks and open questions

## 16.1 Operating preconditions

Conditions of operation that this team does not build. Each needs a named owner before Week 1, because the software assumes them and in one case enforces them.

| Precondition | Owner | Note |
| --- | --- | --- |
| Hardened authoring studios at designated centres, under continuous surveillance and access control | Physical Security / Estates | Physical control. INS04-CAP-11 enforces the software half — sign-in only from a managed device in an approved zone. |
| Managed workstations with device certificates, disk encryption and posture reporting | IT / Endpoint Management | Directly required by INS04-CAP-11. Without it that requirement cannot be met. |
| Device bans and personal-equipment policy inside the studio | Content Operations | Administrative control supporting the deterrence model; screenshots by external devices cannot be blocked by software. |
| Curated reference sources for the public-domain check | Content Operations | Required by ASM03-REV-11. The tool cannot search the open internet — ARC-07 mandates default-deny egress — so the reviewer works from an approved list loaded into the tool. |
| Approved glossary and terminology reference per pilot language | Content Operations | Consumed by ASM03-ATH-13 and the translation workspace. |
| Relevant hardware and software services available for development | Team | Integration tenants for every enterprise service in §2.5. |
| Enterprise identity provider configured with multi-factor policy and a test tenant GAP | IT / Security | Needed for the Week 1 walking skeleton. |
| Key management service with per-identity key policies and asymmetric signing GAP | Security | Needed for the genesis record in Week 1 and sealing in Week 4. |
| Assembly service owner and contract agreement GAP | Assembly team | Needed for Week 4; agreed by Week 2. |

## 16.2 External dependencies

| System | What the MVP needs from it | Owner | Needed by |
| --- | --- | --- | --- |
| Identity provider | OpenID Connect, multi-factor claim, stable subject, test tenant, production tenant. | IT | Week 1 |
| Endpoint management and device authority | Client certificates, posture assertions, approved-zone definitions. | IT | Week 1 |
| Key management | Envelope encryption keys for active and archive tiers, signing key, per-identity policies, usage log. | Security | Week 1 (sign), Week 4 (seal) |
| Object store | Private buckets, versioning, compliance retention lock, provider encryption. | DevSecOps / Platform | Week 4 |
| Malware scanner | Synchronous scan of uploads with a verdict. | Security | Week 2 |
| Monitoring and alerting platform | Security-event and alert ingestion; external anchor storage for checkpoints. | Security / Operations | Week 1 |
| Privileged-access management | Administrative and break-glass access paths. | Security | Week 5 |
| Assembly service | Consumption of readiness; signed notifications; acknowledgement endpoint. | Assembly team | Week 4 |

## 16.3 Risks and mitigations

| Risk | Description | Mitigation |
| --- | --- | --- |
| R-01 | Sealed content must re-enter human view for translation and correction, which reads as a conflict with "nobody can read the question again". | Resolved in this PRD as system actions: the primary reference snapshot at variant creation (PRD-TRN-11) and the seeded correction draft (PRD-COR-08), both audited and visible only to one assignee. Ratify as D-16; confirm with Security in Week 1. |
| R-02 | Renderer non-determinism invalidates accessibility approvals. | One server-side renderer, versioned, pinned dependencies, output snapshot tests over the corpus, no client-side rendering variance. |
| R-03 | A single-writer audit chain becomes a bottleneck under telemetry load. | Benchmark in Week 1 (PRD-EVD-15); aggregate autosave events (D-32); if needed, shard by chain with a root checkpoint — decided before Week 2. |
| R-04 | Device posture integration arrives late, blocking Week 1 closure. | Named IT owner at Week 0; a stub that fails closed is not acceptable for closure, so escalate on day 2 if the tenant is not reachable. |
| R-05 | Assembly contract not agreed in time for Week 4. | Agree the three machine contracts in §6.10 – §6.12 by Week 2; build against a signed contract test double if the assembly team is late, and record the gap in the evidence pack. |
| R-06 | Named reviewers, translators or the accessibility professional are unavailable. | The specification is explicit: an unavailable reviewer stops Week 3 as surely as an unavailable engineer. Reserved capacity is a Week 0 gate. |
| R-07 | The LaTeX subset is too narrow for real questions, causing authoring friction. | Subject experts review the subset against a sample of real items in Week 2; extend by ratified decision, never ad hoc. |
| R-08 | Similarity threshold blocks legitimate questions; no override exists. | The specification provides no exception for similarity. Calibrate the threshold on the corpus in Week 2; the author's only remedy is to change the item; monitor block rate in hyper-care. |
| R-09 | Operating-system screenshots cannot be blocked by a browser. | Documented limitation; physical controls in the studio (§16.1) and the deterrence model carry it; attempts are still reported. |
| R-10 | Five weeks with no float and a twelve-person peak. | Same-day escalation of any unclosed week; scope is fixed by this document; SHOULD items (evidence view, exclusion pairs, retirement, sweep) are the only permissible drops. |
| R-11 | Retention lock period arrives late from Legal, blocking sealing in production. | D-24 is chased from Week 1; the software's refusal to seal without a configured lock makes the gap visible rather than silent. |
| R-12 | Drift between this PRD and the engineering PRD while engineering is already under way. | §2.7 makes the engineering names canonical and closes its open questions; the conflicts are decisions D-38 – D-47 with owners and dates; this PRD is the single source once they are recorded, and the two documents are reconciled at every weekly closure. |
| R-13 | The generation service (Sarvam) becomes a content-exfiltration path or a hidden judge. | D-38 confines it to drafting outside the hardened zones; it never receives pipeline content; generated drafts pass the same validation and human gates; the generation boundary is in scope for the penetration test. |

## 16.4 Assumptions

- The organisation's identity provider can issue tokens with a multi-factor claim and supports a test tenant. 
- The enterprise key management service supports asymmetric signing and per-identity key policies. 
- The assembly service can call mutual-TLS endpoints and sign notifications with a key the MVP can verify. 
- The pilot involves one cycle, one primary language and two required languages, and one item type. 
- Synthetic content is sufficient for every non-production environment and for production smoke tests. 

## 16.5 Open questions for the Product Owner

| Q | Question | Default until answered |
| --- | --- | --- |
| Q1 | Should a returned version's content remain readable to its original author after the successor draft exists, or only the findings? | Only the findings; the successor draft carries the content. |
| Q2 | May the original author be assigned the correction draft of their own sealed artefact? | Yes; separation of duties applies to approvers, not to re-authoring. |
| Q3 | Does a cycle ever reopen after Closed? | No; a new cycle is configured. |
| Q4 | Should "needs equivalent route" block readiness for cycles with that accommodation declared? | No; flagged and escalated (D-17). |
| Q5 | Which consumers besides the assembly service must acknowledge supersession? | Assembly only for the pilot. |
| Q6 | What is the format of the discrimination field when it is eventually populated? | Nullable decimal string; never written by this MVP. |
| Q7 | Is a difficulty change by the reviewer (versus the author's proposal) a return reason or an approval-time override? | Approval-time override, recorded on the decision with both values. |

# 17. Definition of Done and release criteria

## 17.1 Every requirement

- Implemented, peer-reviewed, and covered by automated tests at the appropriate level. 
- Authorization verified by test, including a wrong-role and a separation-of-duties case. 
- Audit events emitted and verified. 
- No Restricted content in logs, traces, telemetry or error messages. 
- Loading, empty, error and success states implemented for any user-facing element. 
- Labelled, keyboard-operable and screen-reader-navigable. 

## 17.2 The four jobs, end to end

- An author creates, validates, previews, autosaves and submits an immutable version. 
- A reviewer approves; a return instead produces a new linked draft carrying findings. 
- An accessibility specialist approves against the rendered artefact and records accommodation capability. 
- Two required languages complete their own review and accessibility check, including the structural and equivalence checks. 
- The system seals every version — no human seal control exists. 
- The artefact becomes ready and the assembly consumer reads metadata only. 
- No human role can retrieve sealed plaintext. 
- A primary correction revokes readiness and marks variants for revalidation. 

## 17.3 Evidence and observability

- Chain verification passes across the full data set, and detects an altered event in a copy of the store. 
- Verification still passes after backup and restore. 
- Removing an expected evidence record blocks sealing and raises an alert. 
- A deliberate blocked action appears on the operator surface within the stated latency, scored and attributed, carrying no content. 
- Threshold breach refers the session and raises an alert; transport loss and recovery lose no session state. 

## 17.4 Release

- Every criterion above signed in one shared evidence pack (§13.5). 
- Release gates in §3 met: no open Critical or High finding; non-functional targets met with evidence; restore drill passed; runbooks owned; seven signatures. 
- Support ownership and the two-week hyper-care roster active and named. 
- Go-live decision recorded with its rationale. 

# Appendix A — Traceability

Every numbered requirement of the specification v4 is carried in this PRD. Requirement identifiers use the National Examination Stack block code as their leading segment; the specification v4 used the earlier framework codes. To find a requirement in v4, replace the leading segment with the v4 code in the second column (for example `ASM03-ATH-02` is `QST03-ATH-02` in v4). ASM-02 Blueprint and validity (v4 QST-02) is out of scope and carries no requirements.

| Stack block | v4 code | Requirement IDs | Count | PRD section |
| --- | --- | --- | --- | --- |
| ASM-01 Construct and syllabus (boundary) | QST-01 | ASM01-CFG-01..05 | 5 | §6.1 |
| ASM-03 Authoring and review — authoring | QST-03 | ASM03-ATH-01..13 | 13 | §6.4 |
| ASM-03 Authoring and review — validation and submission | QST-03 | ASM03-VAL-01..06 | 6 | §6.5 |
| ASM-03 Authoring and review — review | QST-03 | ASM03-REV-01..12 | 12 | §6.3 (REV-01, 08, 09), §6.6 |
| ASM-04 Language and variants, with CND-02 Accessibility and accommodations at artefact level | QST-04, STD-02 | ASM04-ACC-01..09 | 9 | §6.7 |
| ASM-04 Language and variants, with ASR-04 Conformance and exceptions | QST-04, ASR-04 | ASM04-TRN-01..10 | 10 | §6.8 |
| ASM-05 Repository or vault | QST-05 | ASM05-VLT-01..08 | 8 | §6.9, §8 |
| ASM-06 Calibration and lifecycle (boundary) | QST-06 | ASM06-LFC-01..06 | 6 | §6.12 |
| ASM-07 Assembly and equivalence (boundary) | QST-07 | ASM07-RDY-01..06 | 6 | §6.10 |
| INS-04 Trust and capability registries (boundary) | FND-04 | INS04-CAP-01..11 | 11 | §6.2, §4 |
| RES-06 Correction and reconciliation (boundary) | RES-06 | RES06-COR-01..06 | 6 | §6.11 |
| ASR-01 Expected evidence and audit | ASR-01 | ASR01-EVD-01..10 | 10 | §6.13 |
| ASR-02 Monitoring and referral | ASR-02 | ASR02-OBS-01..18 | 18 | §6.14 |
| Architecture (cross-cutting) | — | ARC-01..12 | 12 | §10.2 |
| Data (cross-cutting) | — | DAT-01..08 | 8 | §8.1 |
| Interface (cross-cutting) | — | INT-01..10 | 10 | §7.1 |
| Screens (cross-cutting) | — | UI-01..14 | 14 | §9.2, §6.3 (UI-02, 03) |
| Security (cross-cutting) | — | SEC-01..14 | 14 | §10.3 |
| Roles, lifecycle, non-functional, edge cases, Definition of Done, plan, people, preconditions, exclusions | — | Specification §2, 3, 9, 10, 11, 12, 13, 14 | — | §4, §5, §11, §12, §17, §14, §16 |
| Total numbered requirements |  |  | 178 | PRD adds 124 PRD- requirements and 48 decisions |

### Block map of the National Examination Stack (for orientation)

| Group | Blocks | Relation to this MVP |
| --- | --- | --- |
| Candidate Experience — support the person throughout | CND-01 Information, notices and calendar · CND-02 Accessibility and accommodations · CND-03 Support and familiarisation · CND-04 Status, receipts and evidence · CND-05 Grievance, review and remedy | CND-02 at the boundary (artefact-level accessibility) |
| Institutions — authority and readiness | INS-01 Programme and policy · INS-02 Participation and entitlements · INS-03 Identity binding · INS-04 Trust and capability registries · INS-05 Allocation and readiness | INS-04 at the boundary (authoring workforce) |
| Assessment — prepare the material | ASM-01 Construct and syllabus · ASM-02 Blueprint and validity · ASM-03 Authoring and review · ASM-04 Language and variants · ASM-05 Repository or vault · ASM-06 Calibration and lifecycle · ASM-07 Assembly and equivalence | ASM-03, 04, 05 in full; ASM-01, 06, 07 at the boundary; ASM-02 out |
| Exam Day — conduct and accept work | DAY-01 Release and custody · DAY-02 Admission and session · DAY-03 Supervision and incidents · DAY-04 Work capture · DAY-05 Acceptance and reconciliation · DAY-06 Continuity and recovery | Out of scope |
| Result — maintain the outcome | RES-01 Scoring execution · RES-02 Human evaluation · RES-03 Comparability and adjustment · RES-04 Result readiness · RES-05 Publication and status · RES-06 Correction and reconciliation | RES-06 at the boundary (artefact level) |
| Assurance — establish and examine evidence at every stage | ASR-01 Expected evidence and audit · ASR-02 Monitoring and referral · ASR-03 Investigation and adjudication · ASR-04 Conformance and exceptions · ASR-05 Recovery and substitution tests | ASR-01, 02 in full; ASR-04 at the boundary (exceptions) |

### Engineering PRD (Open Mulyankan — PRD) — where each section lands

| Engineering PRD section | This PRD |
| --- | --- |
| 1 Product overview; 2 Problem statement; 3 Goals | §1, §2.7 (concept map), §3 |
| 4 RBAC matrix; 5 Users and roles | §4.1 roles, §4.3 matrix (every capability row kept, TBD cells resolved), §4.4 |
| 6 Core concepts (curriculum, question bank, assessment) | §2.7 concept map, §5.1 |
| 7 Assessment blueprint; 7.2 candidate generation | §2.7 (blueprint split), §6.1 (cycle fields), PRD-ATH-25, D-38, D-40 |
| 8 Curriculum-grounded generation; 9 Question generation, metadata, AI metadata assignment, generation validation | PRD-ATH-25, PRD-ATH-26, §6.5 validation catalogue, D-38, D-47 |
| 10 Question review workflow (isolation, actions, approval, rejection) | §6.6, PRD-REV-19, PRD-REV-21, PRD-ASG-10, §5.3 |
| 11 Accessibility workflow and open questions; 12 Accessibility review | §6.7 (PRD-ACC-16..19), §2.7 answers table, D-43 |
| 13 Translation workflow; 14 Translation data model; 15 Multiple languages; 16 Translation rejection | §6.8, §5.4, §8.2 (Lineage, Version), PRD-ASG-10 |
| 17 Complete question lifecycle | §5.2 – 5.3 (canonical enumeration) |
| 18 Question versioning; 18.1 approval reset | §5.1 (Version, Provenance), §6.11, §8.2 |
| 19 Reviewer assignment (algorithm TBD) | §6.3 (PRD-ASG-03..05, 10) |
| 20 Reviewer isolation | PRD-REV-19, §4.2, D-47 |
| Not in the engineering PRD | Multi-factor and device posture (§6.2), session integrity monitoring (§6.14), hash-chained audit and expected evidence (§6.13), sealing and readiness (§6.9 – 6.10), API and data contracts (§7 – 8), tests and delivery plan (§13 – 14) |

# Appendix B — Glossary

| Term | Meaning in this document |
| --- | --- |
| Artefact | One question across all its languages and lineages; the unit of readiness. |
| Audit identifier | A random, stable pseudonym for a workforce member, used in every business record instead of a name. |
| Bank index | Metadata-only index of sealed versions used for readiness, similarity and reporting. |
| Break-glass | The dual-authorized manual procedure for emergency access to sealed or archived content outside the routine workflow. |
| Canonicalization | The single fixed rule that turns content into the bytes every hash is computed over. |
| Capability entry | A registry record of what a person is recognized to do, for which subjects and languages, and until when. |
| Cycle | An examination cycle and its configuration: languages, syllabus version, policies, accommodations. |
| Envelope encryption | Encrypting content with a per-object data key that is itself encrypted by a key held in the key management service. |
| Equivalent route | An alternative way for a candidate under a declared accommodation to access an item the standard rendering cannot serve. |
| Expected evidence | The records each workflow step must produce, asserted before sealing. |
| Hash chain | An append-only sequence of audit events where each event's hash includes the previous event's hash, so alteration is detectable. |
| Integrity score | A per-session number starting at 100, reduced by captured signals, never recovering within the session. |
| Lineage | The chain of versions of one artefact in one language; a correction starts a new one. |
| Manifest | The signed evidence record for one sealed version. |
| Primary | The version in the cycle's primary language from which variants derive. |
| Readiness | The state in which the primary and every required variant are sealed against the same lineage and nothing has revoked it. |
| Reference renderer | The single versioned component whose output is used by preview, both gates, sealing and delivery. |
| Sealing | The system action that canonicalizes, encrypts, signs and indexes a version and ends routine human access. |
| Separation of duties | The rule that no one approves work they authored or translated, enforced at the API. |
| Structural check | A deterministic comparison of a variant against its primary on option structure, key position, marks, assets, equations, numbers, units and symbols. |
| Supersession | Replacement of a sealed version by a newer sealed version of the same artefact and language. |
| Variant | A version in a required non-primary language, bound to the primary it was derived from. |
| Workload identity | A short-lived, non-human identity under which a service or worker acts. |
| Project Rachana | The project name (Sanskrit racanā: composition, authoring) of the product whose content-creation pipeline this MVP is. |
| Open Mulyankan | The earlier working name, and the title of the engineering PRD converged in §2.7. |
| Question Bank | Engineering term for the artefact store: drafts and versions under review in the working store, approved versions in the sealed repository. |
| Blueprint | Engineering term for the assessment definition; its cycle-level fields are the Cycle, its counts and weightage are generation and assembly parameters. |
| Candidate multiplier | How many candidate questions generation produces per required question; candidates are independent artefacts. |
| Approval reset | Engineering term for a correction after approval: a new lineage, readiness revoked, the full pipeline again. |
| Reviewer isolation | The rule that a reviewer sees only the assigned question and the metadata needed to judge it — never assessment identity, numbering, other questions, other reviewers or audit history. |
| FULLY_APPROVED | Readiness status: every required language version is sealed; the only status assembly may select. |

# Appendix C — Sample payloads

Illustrative shapes for the interface definition. Field names are normative; values are examples using synthetic identifiers.

### Error envelope

```text
{
"code": "VALIDATION_FAILED",
"message": "The draft cannot be submitted until the blocking findings are resolved.",
"correlation_id": "01J8Z4Q2W7N9K3M1P5R8T2V6X0",
"retryable": false,
"fields": [
{ "path": "options[2].body", "code": "VAL-OPT-02", "message": "This option duplicates option 1 after normalization." },
{ "path": "assets[0].alt", "code": "VAL-ASSET-02", "message": "Provide alternative text or mark the image as decorative." }
]
}
```

### Readiness record

```text
{
"artefact_id": "01J8Z4RA7QK2M9N4P1S6T8V3W5",
"cycle_code": "CYC-2027-A",
"item_type": "single_select_mcq",
"classification": { "subject_id": "SUB-014", "unit_id": "UNI-014-03", "topic_id": "TOP-014-03-07", "syllabus_version": "SYL-2027-1" },
"difficulty": "Moderate",
"taxonomy_level": "Apply",
"marks": "1",
"marking_policy_ref": "MP-2027-STD",
"languages": [
{ "language": "en", "sealed_version_id": "01J8Z4S1…", "content_hash": "9f2c…e1a4", "manifest_id": "01J8Z4S2…" },
{ "language": "ar", "sealed_version_id": "01J8Z4T7…", "content_hash": "51b0…7c92", "manifest_id": "01J8Z4T8…" },
{ "language": "fr", "sealed_version_id": "01J8Z4U3…", "content_hash": "d7e4…03bb", "manifest_id": "01J8Z4U4…" }
],
"readiness_status": "ready",
"ready_since": "2027-02-11T09:42:17Z",
"exclusion_pair_ids": [],
"accommodations_deliverable": ["screen_reader", "magnification", "high_contrast", "extended_time"],
"updated_at": "2027-02-11T09:42:17Z"
}
```

### Audit event

```text
{
"event_id": "01J8Z4V9…",
"chain_id": "prod-main",
"sequence": 1048577,
"occurred_at": "2027-02-11T09:42:17.204Z",
"actor": { "type": "service", "id": "sealing-worker" },
"action": "version.sealed",
"subject": { "type": "version", "id": "01J8Z4S1…", "hash": "9f2c…e1a4" },
"outcome": "success",
"policy_version": 7,
"correlation_id": "01J8Z4V8…",
"trace_id": "4a1c…",
"details": { "manifest_id": "01J8Z4S2…", "superseded_version_id": null, "language": "en" },
"prev_hash": "3be2…9d10",
"event_hash": "a8c4…52f7"
}
```

### Telemetry event (complete schema — no other fields are accepted)

```text
{
"event_id": "01J8Z4W2…",
"event_type": "copy",
"severity": "critical",
"occurred_at": "2027-02-11T09:40:03.118Z",
"session_id": "01J8Z4A0…",
"actor_audit_id": "WA-7f3e9c",
"task_ref": "01J8Z3Z9…",
"client_seq": 412,
"blocked": true,
"score_after": 75
}
```

### Manifest (abridged)

```text
{
"manifest_version": "1.0",
"version_id": "01J8Z4S1…", "artefact_id": "01J8Z4RA…", "lineage_id": "01J8Z4R0…", "language": "en", "item_type": "single_select_mcq",
"content_hash": "9f2c…e1a4", "canonical_schema_version": "1.0", "canonicalization_rule_version": "1.0", "renderer_version": "2.3.1",
"ciphertext_hash": "7d0a…c3e8", "object_key": "01J8Z4RA…/01J8Z4S1…/9f2c…e1a4",
"encryption": { "algorithm": "AES-256-GCM", "wrapped_data_key_ref": "wdk-01J8Z4S1…", "kms_key_id": "repo-active-2027", "tier": "active" },
"assets": [ { "asset_id": "01J8Z4P5…", "checksum": "c1d2…44aa" } ],
"approvals": [
{ "decision_id": "01J8Z4M1…", "type": "review", "decision_hash": "e4f1…0b77", "reviewer_audit_id": "WA-2b91d0", "decided_at": "2027-02-10T15:02:41Z" },
{ "decision_id": "01J8Z4N6…", "type": "accessibility", "decision_hash": "19a8…6cd3", "reviewer_audit_id": "WA-c04e77", "decided_at": "2027-02-11T09:31:05Z" }
],
"evidence_assertion": { "model_version": "1.0", "passed_at": "2027-02-11T09:42:16Z" },
"policy": { "cycle_policy_version": 7, "taxonomy_version": "SYL-2027-1", "vocabulary_versions": { "difficulty": 1, "taxonomy_level": 1 } },
"sealed_at": "2027-02-11T09:42:17Z", "sealing_identity": "sealing-worker", "audit_event_id": "01J8Z4V9…",
"signature": "MEUCIQ…", "signing_key_id": "manifest-sign-2027", "signature_algorithm": "ECDSA_P256_SHA256"
}
```

### Selection notification

```text
POST /downstream/v1/selection-notifications
X-Signature: eyJhbGciOiJFUzI1NiIsImtpZCI6ImFzbS0yMDI3In0…   (detached JWS over the body)

{
"notification_id": "01J8Z5A1…",
"exam_session_id": "EXS-2027-03-14-A",
"cycle_code": "CYC-2027-A",
"selections": [
{ "artefact_id": "01J8Z4RA…", "expected_primary_version_id": "01J8Z4S1…" },
{ "artefact_id": "01J8Z4RB…", "expected_primary_version_id": "01J8Z4S9…" }
],
"issued_at": "2027-03-01T08:00:00Z"
}
```

End of document · Project Rachana · Content Creation MVP PRD v1.3 · Derived from the MVP Requirements Specification v4 · Contains no examination content.
