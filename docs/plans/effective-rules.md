# Effective rules for implementation

The task brief brings the relevant PRD clauses together. Preserve their MUST/SHOULD priorities and use the source order in [source-of-truth.md](../source-of-truth.md). This page explains existing amendments and the remaining conflicts; it does not invent new policy approvals.

## Rules that can be specified now

| Area | Applicable contract | Where to verify |
|---|---|---|
| Admin and authoring | Main PRD V1 has Admin authoring. Admin cannot approve/reject any review stage. A separate Author role is the unresolved extension in R4. | Main PRD §§5.1–5.2; #42 includes the full matrix |
| Older Coordinator/Author labels | Apply main V1’s Admin responsibilities and the effective role table. Do not implement an older annex matrix that grants Admin review approval. Keep a future separate Author capability set out until R4 is settled. | Product workflow; D-46; R4 |
| Application placement | Signed desktop client handles Admin authoring and unsealed-content tasks; web handles configuration and content-free oversight. | R1, amended ADR-0008 |
| Accessibility | Specialist remediates restricted fields and completes; independent Reviewer approves/rejects. Both steps occur for each language. Older references to specialist approval are superseded. | R7; PRD-ACC-16 through 19; main §10 |
| AI | Layer 2 produces proposals; Layer 1 validates deterministically and enforces human decisions. ARC-12’s blanket wording is scoped by PRD-ARC-13/D-38 to Layer 1. | D-38; product workflow |
| Blueprint/assembly | Curriculum, generation constraints and candidate counts belong to Rachana. Paper selection, ordering and export belong to separate assembly. | R3 and the generation/assembly ADR |
| Managed services | The adopting organisation chooses and contracts any provider(s) meeting the interfaces. Bodhan AI’s proposed reference maintenance does not appoint an operator. | Delivery plan |
| Question deletion/export | Preserve the main product contract: withdraw unsubmitted drafts, retire approved questions, preserve history; no routine question-bank download/export. PR #97 records overlapping ADR proposals and still needs review. | Main §§5, 14; D-39/D-41 |
| Readiness/state | FULLY_APPROVED is computed readiness across current language seals. It does not replace each language’s state or permit reuse of Used/Archived/Retired artefacts. | Main §13; PRD-RDY-07 |
| Diagnostics/evidence | OTel diagnostics may degrade without blocking domain work. Required audit and session-integrity evidence must remain durable and recoverable. | R9; ASR01/ASR02; observability contract |

## Decisions and work that can proceed

| Decision | Affected behaviour waiting for its owner | Work that can proceed |
|---|---|---|
| R4: separate Author and adoption | New Author permission set; automatic generated-draft versus explicit adoption transition | Existing Admin manual authoring, policy evaluator, proposal validation/provenance and independent review |
| R5: renderer contract | Final canonical reference/local rendering equivalence and release qualification | Content/task schemas, synthetic screens, bounded sanitisation and renderer fixtures |
| R6 / D-01 / D-02: bytes and chain | Adoption/migration of a new canonical byte profile and ratified checkpoint policy | Preserve draft-v0.1, persistent transaction design and fixtures with an explicit version |
| R8 / D-16: controlled sealed references | Real primary-reference release, correction decryption/seeding and exceptional access | Deny routine reads; synthetic task/reference fixtures; readiness revocation and notification contracts |
| R12 / D-06: review count | Pilot count and correct-answer visibility selection | Configurable one/two-independent-review engine and one-assignee-per-task behaviour |
| D-48: translation AI | Sending primary reference text to a model | Manual translation and a tested disabled AI channel |
| D-24: retention | Any live seal without a supplied retention period | Reject missing configuration; test storage/manifest/retry design with synthetic configured services |
| D-03/04/14 and other proposed values | Ratified severity, threshold, session and deployment settings | Configurable mechanisms and explicit test configurations; proposed defaults must not be labelled approved |
| D-29 / pilot roster | Real language and participant commitments | Language-agnostic schemas and synthetic multi-language scenarios |
| R10: dependency rights | External client redistribution until permission scope is established | Source work and appropriately authorised internal builds |

Decision values and evidence are in [prd-decisions.md](../prd-decisions.md); owners and dependencies are in [prd-reconciliation.md](../prd-reconciliation.md). New implementation choices such as module layout, indexes, worker libraries or test tooling belong to engineers within these contracts. They do not require a new product decision merely because the PRD does not name a class or function.

## Interface conventions already supplied by the PRD

Read [technical §7.1](../prd/technical-baseline.md#71-mandatory-interface-behaviours), [entity fields](../prd/technical-baseline.md#82-entities-and-required-fields) and [sample payloads](../prd/technical-baseline.md#appendix-c--sample-payloads) before proposing an API. They specify versioned audience boundaries, idempotency, concurrency tokens, safe errors, opaque identifiers, UTC times, no-store responses and machine authentication. #117 turns these into machine-readable contracts with the producing/consuming owners.

Where the existing scaffold differs, document an explicit compatibility/migration choice; do not silently declare that the desired route already exists. In particular, current `/v1/sessions` scaffolding and target `/telemetry/v1` conventions need a reviewed interface mapping.

## Review scope

A feature owner can write a technical design and fixtures from the supplied rules. Check in the intended first implementation slice and obtain the agreed plan/interface review before coding that slice. Review does not reopen settled product rules. A missing value or unresolved conflict blocks only its dependent integration or release behaviour, listed in the brief. Every expert acceptance still needs the named owner’s evidence and signature.
