# PRD decision register

Source: Detailed Spec §15 in the [14 September baseline](source-of-truth.md).
The default, owner and timing columns below preserve the source. A proposed
default is not a recorded approval. Main PRD §20 says its recommendations
stand until the owner decides; use them for design, while keeping explicit
security, legal and production prerequisites closed until their owner acts.

Only **D-38** explicitly records a Product Owner decision in the retrieved source.
Later decisions from this alignment review are distinguished in the evidence
column: R1 settles Admin application placement and R3/ADR-0012 confirms the
generation/assembly boundary relevant to D-40. Source default text is retained.
D-38's connector controls and translation hosting still require Security action.
D-28 has a partial repository decision: ADR-0001 and ADR-0010 select stacks;
they do not settle production hosting. Bodhan AI is the planned host and
continuing maintainer in [delivery-plan.md](delivery-plan.md), with service
contracts and named contacts pending. Other rows have no approval evidence
attached by this review. The preserved Needed-by column records historical
PRD weeks. Apply its dependency order within the current 28 September target;
it does not create a second calendar or defer prerequisites beyond the sprint.

Related repository/source conflicts and proposed resolutions are tracked
separately in [PRD reconciliation](prd-reconciliation.md). Do not reuse these
D-nn IDs for the local D1–D19 observability decisions.

| ID | Decision | Source default / recorded outcome | Source owner | Needed by | Evidence of decision |
|---|---|---|---|---|---|
| D-01 | Canonicalization rule v1 | §8.4 as written; JCS container, NFC, deterministic DOM serialization, options in display order, integers or decimal strings, asset checksums included. | Technical Lead | Week 1 | No approval attached; source recommendation |
| D-02 | Hash algorithm, chain granularity, checkpoints | SHA-256; one global per-event chain with a single writer; signed checkpoints every 10,000 events or hourly, anchored in the monitoring platform. | Technical Lead, Security | Week 1 | No approval attached; source recommendation |
| D-03 | Integrity signal severity table | §6.14 catalogue with the listed decrements. | Integrity Operator, Security | Week 2 | No approval attached; source recommendation |
| D-04 | Referral threshold | Refer at score ≤ 50. | Integrity Operator, Security | Week 2 | No approval attached; source recommendation |
| D-05 | Who maintains the capability registry | Coordinator role with re-authentication; every change audited; optional two-person rule deferred. | Product Owner | Week 1 | No approval attached; source recommendation |
| D-06 | Reviews required per cycle; reviewer sees the correct answer | One review for the pilot cycle; reviewer sees the key (true). | Assessment decision owner | Week 3 | No approval attached; source recommendation |
| D-07 | Remediation repeats review policy | repeat_when_content_changed with "changed" as defined in §5.4. | Assessment decision owner | Week 3 | No approval attached; source recommendation |
| D-08 | Similarity algorithm and threshold | Word 3-gram Jaccard over normalized stem plus options; block at ≥ 0.80; same-language comparison across the whole bank. | Assessment owner, Technical Lead | Week 2 | No approval attached; source recommendation |
| D-09 | Restricted-HTML allowlist | PRD-ATH-16. | Technical Lead, Security, Accessibility Specialist | Week 2 | No approval attached; source recommendation |
| D-10 | Permitted LaTeX subset and bounds | PRD-ATH-17. | Technical Lead, Accessibility Specialist, subject experts | Week 2 | No approval attached; source recommendation |
| D-11 | Field limits, image formats and budgets | PRD-ATH-14; PNG and JPEG only. | Product Owner | Week 2 | No approval attached; source recommendation |
| D-12 | Assignment expiry per task type; unassigned alert delay | Review 5 business days; accessibility 5; translation 10; translation review 5; revalidation 5; alert after 8 hours unassigned. | Review Coordinator | Week 3 | No approval attached; source recommendation |
| D-13 | Author cap default; open-task workload cap | 40 artefacts per author per cycle; 10 open tasks per user. | Review Coordinator | Week 2 | No approval attached; source recommendation |
| D-14 | Session lifetimes, inactivity timeout, re-authentication list, posture freshness | PRD-CAP-14; posture assertion no older than 30 minutes. | Security | Week 1 | No approval attached; source recommendation |
| D-15 | Exception maximum validity and approver role | 30 days; Coordinator approves with re-authentication; approver ≠ requester. | Assessment owner, Security | Week 4 | No approval attached; source recommendation |
| D-16 | How a correction draft obtains sealed content | System-seeded draft under a recorded authorization by a dedicated seeding identity (PRD-COR-08); never a read interface. | Security, Assessment owner | Week 4 | No approval attached; source recommendation |
| D-17 | Declared-accommodation vocabulary; whether "needs equivalent route" blocks readiness | screen_reader, magnification, high_contrast, large_print, reader, scribe, extended_time, braille, colour_overlay; does not block; flagged on readiness and escalated. | Accessibility Specialist | Week 3 | No approval attached; source recommendation |
| D-18 | Difficulty, taxonomy-level and complexity vocabularies | Difficulty: Easy, Moderate, Hard, Very hard. Taxonomy level: Remember, Understand, Apply, Analyse, Evaluate, Create. Complexity: Low, Medium, High (author-declared, distinct from reviewer-assigned difficulty). | Assessment decision owner | Week 1 | No approval attached; source recommendation |
| D-19 | Checklist text, reason codes, out-of-band notification channel | §6.6 templates and codes; in-app notifications only for the MVP. | Assessment owner, Content Operations | Week 3 | No approval attached; source recommendation |
| D-20 | Unsaved draft preservation across forced re-authentication | In-memory state plus autosave before redirect; no persistent browser storage. | Technical Lead | Week 2 | No approval attached; source recommendation |
| D-21 | Paste and drag-and-drop in the hardened editor | Blocked and reported; the glossary and palettes insert through their own controls. | Security, named Authors | Week 2 | No approval attached; source recommendation |
| D-22 | Automatic session suspension | Off. Enabling is an operational decision recorded in configuration. | Operations | Week 3 | No approval attached; source recommendation |
| D-23 | Localized numerals in variants | Numeric values preserved verbatim; an exception is the only route to change one. | Translators, Assessment owner | Week 4 | No approval attached; source recommendation |
| D-24 | Retention lock period for sealed objects and manifests | No default. Must be supplied in writing; the software refuses to seal without it. | Content Operations, Legal | Week 4 | No approval attached; source recommendation |
| D-25 | Supersession delivery mechanism and acknowledgement window | Mutual-TLS webhook to registered consumers; 24-hour window. | Assembly team, Technical Lead | Week 2 (agree), Week 4 (live) | No approval attached; source recommendation |
| D-26 | Selection notification atomicity | All-or-nothing per notification. | Assembly team | Week 4 | No approval attached; source recommendation |
| D-27 | Evidence view versus scripted procedure (P1) | Build the minimal view; fall back to the script only if Week 3 capacity is strained, with equivalent output. | Product Owner, QA Lead | Week 3 | No approval attached; source recommendation |
| D-28 | Technology stack and hosting | Technical Lead's proposal evaluated against §10.4. | Technical Lead, DevSecOps | Week 1 | Stack partly recorded in ADR-0001/0010; Bodhan AI hosting planned in delivery-plan.md; deployment/service contracts pending |
| D-29 | Pilot languages (primary plus two) | To be named. | Content Operations | Week 0 | No approval attached; source recommendation |
| D-30 | Environments and production topology | §10.7; four environments; repository zone separate. | DevSecOps | Week 1 | No approval attached; source recommendation |
| D-31 | Classification and location of similarity fingerprints | Restricted derived data in the repository tier; never exposed. | Security | Week 2 | No approval attached; source recommendation |
| D-32 | Chain event volume for autosave | Draft saves are aggregated into one audit event per draft per minute with a count; individual saves are not chained. | Technical Lead | Week 1 | No approval attached; source recommendation |
| D-33 | Telemetry batch size and ingest limits | 50 events per batch; 2 per second sustained and 10 burst per session. | Technical Lead | Week 1 | No approval attached; source recommendation |
| D-34 | Exclusion pairs (SHOULD) in scope | Yes, if Week 4 capacity allows; otherwise dropped with a note in the evidence pack. | Product Owner | Week 3 | No approval attached; source recommendation |
| D-35 | Evidence sweep (SHOULD) cadence | Daily. | QA Lead, Operations | Week 5 | No approval attached; source recommendation |
| D-36 | Who may see the author's identity | Only the coordinator, on assignment screens, for assignment purposes. Never reviewers or specialists. | Product Owner, Security | Week 2 | No approval attached; source recommendation |
| D-37 | Two-tab behaviour for content surfaces | Both tabs function; one session record; concurrent-tab signal recorded (per specification). | Security | Week 2 | No approval attached; source recommendation |
| D-38 | AI generation and AI translation drafts (Sarvam) versus ARC-12 | Decided 7 September 2026 (Product Owner): in scope for the MVP and the demo as Layer 2. AI may draft, never judge: candidates, translation first drafts and metadata suggestions enter as Drafts with provenance and pass the identical human pipeline; no AI in validation, similarity, review, accessibility, sealing, readiness or monitoring; Layer 2 runs outside the hardened zones behind the single connector (§1.5, PRD-ARC-13). ARC-12 is re-worded to bind Layer 1. | Product Owner (decided); Security ratifies the connector controls | Decided; Security by Week 1 | Decided in PRD; connector controls pending |
| D-39 | Admin download and export | None from the question bank for any role; paper export belongs to the assembly module under release custody (DAY-01). | Product Owner, Security | Week 1 | No approval attached; source recommendation |
| D-40 | In-product assembly by the Admin | Build assembly as a separate module consuming the readiness interface; selection by metadata against the blueprint (blind assembly); rendering through release custody, never through authoring surfaces. | Product Owner, Technical Lead | Week 2 | Separate assembly scope confirmed 2026-09-14 in R3/ADR-0012; release-custody contract still required |
| D-41 | Admin "Delete question" | Withdraw for unsubmitted drafts, Retire for approved or sealed questions; nothing physically deleted. | Product Owner | Week 1 | No approval attached; source recommendation |
| D-42 | Admin "View all questions" | Allowed for unsealed versions because the Admin authors everything in V1; sealed versions expose metadata only. | Security | Week 1 | No approval attached; source recommendation |
| D-43 | Accessibility check per language version | Keep (specification MUST); the variant remediation is small. Deferral for the pilot is a documented drop. | Accessibility Specialist, Product Owner | Week 3 | No approval attached; source recommendation |
| D-44 | Question types beyond single-select MCQ | Item type stays data; other types enter only when enabled per cycle with a named reduced rule set. | Assessment decision owner | Week 2 | No approval attached; source recommendation |
| D-45 | Admin holding the Auditor and Integrity Operator views | Permitted (content-free surfaces); a distinct Integrity Operator person is recommended for the pilot. | Security | Week 3 | No approval attached; source recommendation |
| D-46 | Admin Approve and Reject in the engineering RBAC matrix | Removed: the Admin authors, so cannot decide any review stage; the Admin assigns, reassigns, releases and authorizes corrections. | Product Owner | Now (Week 1) | No approval attached; source recommendation |
| D-47 | Source information visible to reviewers | Subject, grade, curriculum name, chapter and page range; never the stored source context text, the blueprint or the assessment. | Security, Assessment owner | Week 2 | No approval attached; source recommendation |
| D-48 | Hosting model for Layer 2 translation drafts, which need the primary text | Private in-boundary deployment of the model with no retention and no training on inputs; otherwise the translation-draft channel stays off and translators start from an empty variant. Generation needs no pipeline content and may use the external service. | Security, Technical Lead | Week 2 | No approval attached; source recommendation |
