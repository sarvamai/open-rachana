# PRD reconciliation and review items

Prepared against the [source baseline](source-of-truth.md) on 14 September
2026. R-numbers below identify reconciliation items, **not new requirement
IDs**. An entry marked proposed has no approval implied by this document.
The [D-01–D-48 register](prd-decisions.md) retains the PRD's own owner decisions.

## Product and architecture decisions to record

| Item | Source conflict / gap | Proposed resolution and affected work | Decision owner / due gate | Status |
|---|---|---|---|---|
| R1 — Admin and application split | Main §5 / annex §2.7 make Admin the V1 author with unsealed-content access. ADR-0008 originally gave administrators only a content-free oversight web UI. | Admin authoring and unsealed-content work run in the signed desktop client. Configuration and content-free oversight run in the web app. The same person may have both surfaces without acquiring review approval powers. Session, capability and re-authentication mechanics still require implementation contracts. | Product Owner decided placement; Technical Lead + Security own the implementing contracts | Decided 2026-09-14 by the Product Owner in the repository-alignment review: “Yes—use this split”; ADR-0008 amended |
| R2 — Layer 2 delivery | D-38 explicitly includes generation, translation drafts and metadata in MVP/demo. ADR-0007 supplies only a gateway slice/reference adapter; SECURITY.md scopes this repo to Layer 1. | Retain the connector architecture. Name the Layer 2 service/repository, delivery owner, curriculum-ingestion contract, generation milestones and end-to-end acceptance evidence. A demonstration adapter alone does not close D-38. | Product Owner + Technical Lead; assign named owner and interim integration dates against the 28 September target | Scope recorded by D-38; 28 September target and Sarvam AI pilot recorded in delivery-plan.md; named integration owner and service/repository contract pending |
| R3 — Blueprint boundary | Main §§3, 6–7 require blueprint-driven generation; main §21 and annex §2.3 exclude blueprint logic/coverage counts. Mock exam-paper and blueprint surfaces exist. | Curriculum, generation constraints and candidate counts belong to Rachana. Selecting, ordering and exporting the final paper belong to a separate assembly module. Existing exam-paper mocks do not become accepted Rachana workflow features. | Product Owner decided boundary; Technical Lead owns module/interface implementation | Decided 2026-09-14 by the Product Owner: “Yes—confirm this boundary”; ADR-0012 records it; repository reference is authoritative for this boundary |
| R4 — Author role and proposal adoption | Main §7 / PRD-ATH-25 create validated generated DRAFTs; ADR-0007 requires explicit human adoption before a proposal becomes a draft. | Prefer Admin-initiated generation → validated DRAFT → Admin inspection/submission → independent review, preserving provenance. Decide whether an extra adoption action is required and amend ADR-0007 before implementing that transition. Keep all review and seal gates unchanged. | Product Owner + Technical Lead + Security; before gateway/authoring integration | Owner indicated both Admin and Author should be able to participate, but the reply was incomplete. Separate Author permissions and automatic draft creation versus explicit adoption remain pending clarification; no transition implemented |
| R5 — Render contract | PRD-ATH-18 specifies a server-executed reference renderer. ADR-0001 says the backend never renders; ADR-0008/0010 require a locally bundled signed renderer and structured task data, not executable server UI. | Define one versioned canonical rendering specification, with a protected reference-rendering job and a signed local renderer proven against the same fixtures. Explicitly decide which outputs seal into the manifest and how per-OS Tauri equivalence is accepted. Never send executable server UI to the client. | Technical Lead + Accessibility + Security; before render SPI/client contract | Proposed; renderer topology and acceptance unresolved |
| R6 — Canonical bytes | Annex §8.4 proposes v1.0; code uses draft-v0.1. D-01 is not ratified. | Document existing bytes without changing them. Ratify a precise cross-language v1 profile and fixtures, then define version dispatch, migration and historic verification. Do not silently relabel current hashes as JCS/v1.0. | Technical Lead + Security; before persistent audit/sealing schema is fixed | Current format documented; v1 approval pending |
| R7 — Accessibility acceptance wording | Main §5 / annex §6.7 separate Specialist completion from Reviewer approval; annex §17.2 still says the specialist approves. | Apply the specific two-role product flow in repository docs. Correct the stale acceptance sentence to Accessibility Reviewer and retain independent remediation. | Product Owner + Accessibility lead; before signing acceptance criteria | Repository reference resolves the wording to the explicit two-role flow; acceptance signatures still required |
| R8 — Sealed content and controlled references | Routine sealed plaintext denial coexists with primary reference access for translators, D-16 correction seeding, and annex §10.6 emergency evidence access. Current repo invariants forbid any human read path. | Keep routine APIs closed. Specify scoped system-created translation/correction references, permitted content and lifetimes. Keep emergency access outside routine workflow, with dual authorization, dedicated identity, purpose/time box and audit; approve its runbook separately. Translation AI remains off under D-48 until hosting is approved. | Security + Assessment owner + Technical Lead; before translation, correction or emergency-access implementation | Proposed contract clarification; no read path authorised by this change |
| R9 — Diagnostic versus integrity telemetry | ADR-0011 allows dropped diagnostic signals; ASR02-OBS-05 requires integrity retry/durability. ADR-0008 mentions camera and a replay store; the PRD's operator view is content-free. | Keep diagnostic observability separate from durable session integrity/audit. Diagnostic loss must not satisfy or erase required evidence. Do not infer authorization for camera capture or replay of question content; specify lawful cycle policy, data classification, access and retention before any such feature. | Security + Integrity Operator + Technical Lead; before telemetry contract/production capture | Separation documented; camera/replay scope unresolved |
| R10 — Dependency exception | ADR-0002 gives a permissive dependency allowlist; ADR-0001 and NOTICE record proprietary Tatva, whose NOTICE wording permits the web application while ADR-0010 also uses it in the client. | Keep the existing exception visible. Reconcile ADR-0002 with NOTICE and verify the scope of permission for client redistribution with the steward. Do not describe the complete dependency stack as Apache-2.0 or invent permission. | Repository steward; before external binary distribution | Existing exception recorded; client permission scope not established by this review |
| R11 — Observability decision status | ADR-0003/provider contracts speak of OTel adoption; ADR-0011 remains Proposed; observability.md has Recommended rows. | Retain the proposal and its plan. Record deciders/date and settled rows when actually approved; do not make the documents appear Accepted merely because a design PR merged. | Technical Lead; before the dependent observability implementation slice | Proposed status preserved; cross-references clarified |
| R12 — Reviewer count | Main §15 says one reviewer per stage; main §9.5 and D-06 make the required count configurable. | Interpret assignment as one assignee per review task, with distinct tasks/actors for every review required by cycle policy. Record the chosen pilot count separately. | Assessment owner + Product Owner; before review assignment contract | Proposed clarification; D-06 remains open |

## What this documentation change resolves

- Establishes this repository as the maintained standalone reference, with
  an embedded architecture diagram and the 28 September delivery plan.
- Preserves the historical baseline and accepted amendments without external
  document links.
- Carries the explicit product roles, per-language gates and reviewer isolation
  into the repository; records the Product Owner's Admin application split.
- Records the decided generation-versus-assembly scope boundary.
- Crosswalks all 302 numbered requirements and records all 48 source decisions.
- Replaces ambiguous closure claims with target milestones and evidence status.
- Corrects the claim that an M0 reference KMS provider already exists.
- Documents the actual draft-v0.1 audit bytes without changing them.

It does not assign people, approve source defaults, implement missing
controls, change Google Docs, or declare an acceptance milestone closed.

## Sequence for maintainers

1. Implement R1's decided placement through reviewed session/API contracts.
   Apply ADR-0012's decided scope boundary. Review R2, R4, R5, R8 and R12
   with the named owner roles before implementing
   their dependent contracts. Record the decision and amend the relevant ADR
   with date and consequences; retain superseded text as history.
2. Reconcile R6 before durable schema/sealing work. Link the approved byte
   fixtures and migration plan to D-01/D-02.
3. Name Layer 2 delivery ownership, pilot languages, content people and source
   approval owners; attach evidence for prerequisite gates before dependent work; historical Week 0/1 labels are not the current calendar.
4. Replace the Python CI placeholder in a separate implementation change,
   then link actual requirement checks and retained results as slices land.
5. Record later decisions directly in this reference and update affected
   requirements, workflow and ADRs together. Review distribution and capture
   decisions R9/R10 before the affected release.
