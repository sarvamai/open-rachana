# Sprint milestones, handover and continuation

Proposed reference delivery plan, 14 September 2026. This document defines the sprint
scope, completion outcomes and handover obligations. [Delivery status](delivery-status.md)
records the inspected implementation and evidence; no milestone closes merely
because it appears in this plan.

## Proposed sprint target

| Item | Current plan |
|---|---|
| Review | 15 September 2026 |
| Sprint | Three weeks; deadline **28 September 2026** |
| Engineering team | **6–8 volunteer engineers building with coding agents** |
| Sprint base | IIT Madras |
| Product | Reference implementation of the authoring engine: approved, sealed, multilingual questions with proof of every step |
| Full block scope | Five of the stack's 34 blocks: ASM-03 Authoring and review; ASM-04 Language and variants; ASM-05 Repository; ASR-01 Evidence and audit; ASR-02 Monitoring and referral |
| Architecture | Layer 2 intelligence, Layer 1 workflow, Layer 3 managed services, connected by adapters and bindings |
| Pilot intelligence | Sarvam AI; providers replaceable through capability adapters |
| Layer 3 services and hosting | Supplied by whichever provider(s) the adopting organisation contracts, subject to the agreed interfaces and acceptance requirements |
| Reference continuation | Bodhan AI is a proposed continuing maintainer of the reference implementation; this does not determine the adopter’s service providers |
| Handover support | Two-week hyper-care with the sprint team on call |

The date, team size and institutional arrangements below remain planning
proposals for maintainer and participant review, not public service commitments.

This delivery target retains all acceptance criteria, security approvals and
operational prerequisites. The sprint start date and individual interim gate
dates remain to be assigned.

The repository's M0–M6 labels are retained as **dependency and evidence gates**
for traceability, not seven new weeks or a competing calendar. Each in-scope
gate is targeted for closure by 28 September. The team must assign actual
owners and interim dates against the remaining work; an unclosed gate must
remain visible rather than being declared complete to meet the date.

Each week must close with retained evidence against the agreed gates:
tampered records detected, copy attempts visible to the operator,
self-approval refused and three languages sealed. Assign these proofs to
interim gates and carry incomplete proofs forward visibly. The requirement
register contains 178 inherited requirements plus 124 PRD additions; the
permission matrix must serve as an oracle for allowed and refused operations.
Protect confidential sprint material until its approved public release.

## The seven completion outcomes for 28 September

All seven outcomes are required. The evidence and owner-role columns below
make them reviewable using existing PRD obligations; named people remain to
be assigned. None is marked complete by this document.

| Completion outcome | Evidence to retain | PRD / verification owner roles |
|---|---|---|
| A question reaches FULLY_APPROVED in three languages; no routine person can read sealed plaintext afterwards | One primary plus two required language variants, independent approvals and language seals, manifests/hashes, and routine-human-role/API denial checks | ASM04-TRN, ASM05-VLT, ASM07-RDY, SEC-01; Assessment, Accessibility, Security, QA |
| Self-approval fails, including a hand-crafted API call | Wrong-role and same-lineage author/translator approval attempts rejected by the server, with content-free evidence | INS04-CAP-07, SEC-06; Security, QA |
| Tampering is detected and the audit still verifies after backup/restore | Altered/removed-record detection, encrypted restore drill and post-restore chain verification output | ASR01-EVD, SEC-13, DAT; QA, Security, Operations |
| Assembly receives metadata only over a machine identity | Correct workload identity succeeds; human/wrong-audience credentials fail; response schema and payload contain no question content | ASM07-RDY, ARC-06; Assembly owner, Security, QA |
| A copy attempt is blocked and visible to the operator within seconds, without content | Managed-client blocked-action test, attributable operator signal, latency measurement and content-free payload/log checks | ASR02-OBS; Integrity Operator, Security, QA. Keep the PRD's ≤3s operator-signal target |
| A generated candidate passes the same human gates as a handwritten question | Curriculum/source provenance, generation validation, human submission, review, accessibility, language gates and sealing evidence for synthetic examples | PRD-ATH-25/26, PRD-ARC-13, D-38; Product, Assessment, Accessibility, QA |
| Every acceptance criterion is signed in one evidence pack | Requirement/test/result/owner links, manual expert checks, release-gate closure, dated signatures and recorded go-live decision | Annex §§13.5 and 17; QA and all named acceptance owners |

The sealed-content statement concerns routine product identities. The
separately governed reference/seeding/emergency contracts remain R8; this plan
does not approve an unrestricted read path. D-48 still blocks translation AI
until its hosting and data handling are approved.

## Build scope and dependency gates

The complete build scope is mapped below. The M-labels are the existing
repository gates; the deadline for the in-scope sprint remains 28 September.
Component implementation and requirement evidence are in [traceability](traceability.md).

| Build area | Existing gate | Entry or acceptance dependency |
|---|---|---|
| Cycle, syllabus and versioned taxonomy | M1 | Valid configuration, controlled vocabularies and policy versions |
| Identity, MFA, device posture and capability registry | M1 | Working IdP/device claims; server authorization and revocation |
| Automatic assignment, My Work and task expiry | M1/M3 | Eligibility, workload policy, conflict checks and expiry/reassignment |
| Hardened editor, autosave and in-tool references | M2 | Managed content client, role contracts and no persistent local content |
| Deterministic validation and duplicate check | M2 | Ratified content rules, clean-asset pipeline and similarity policy |
| Question review with checklist and attestations | M3 | Independent reviewer assignments and full isolation checks |
| Accessibility remediation and review | M3 | Separate roles, accessible rendering and qualified people |
| Translation with locked structure and exceptions | M4 | Primary seal/reference contract, per-language review/accessibility; D-48 for AI drafts |
| Sealing: canonical form, hash, encryption and manifest | M4 | Ratified bytes, managed keys, retention period and complete evidence |
| Readiness interface for assembly, metadata only | M4 | All required language seals, workload identity and agreed consumer schema |
| Corrections, supersession, Used and Archived | M4 | Authorized seeding, readiness revocation, signed events and acknowledgement |
| Hash-chained audit with expected-evidence checks | M1/M3/M4 | Durable atomic storage, completeness assertions, tamper/restore verification |
| Session monitoring and operator console | M1/M3 | Authenticated session ownership, durable integrity ingest and referral policy |
| Layer 2 generation through adapters | M2/M4 integration | Curriculum and generation contracts, named delivery owner, validation and human gates |
| Notifications, four states on every screen and versioned API | M1–M4 | Content-free notices; loading/empty/error/success; schema and compatibility checks |

M5 remains hardening/qualification; M6 remains acceptance/handover. Both are
part of the completion evidence, not automatically postponed beyond the
sprint. Handover includes penetration-test and accessibility-audit evidence.

The six operating rules are defined in [product-workflow.md](product-workflow.md):
immutable submissions; writers do not approve; reviewer isolation; system-only
sealing with evidence checks; content-egress restrictions and content-free
monitoring; withdrawal/retirement instead of physical deletion. The pending
Author-role/adoption clarification is recorded in R4.

## Layer 3 and handover responsibilities

The organisation adopting the authoring engine selects and contracts its
Layer 3 providers. One provider may supply the whole environment, or different
providers may supply different services. The architecture requires compatible
interfaces and verified controls, not a particular company.

Bodhan AI is identified as a proposed continuing maintainer of the reference
implementation. That is separate from supplying or operating an adopter’s
managed services. Named maintainers, service providers, agreements and
acceptance responsibilities must be recorded for the actual deployment.

Layer 3 covers enterprise identity/MFA, HSM-backed key management, object
storage with retention lock, relational database, monitoring/alerting,
malware scanning, workload identities/mutual TLS and hosting. The interfaces,
service accounts, configuration bindings and failure tests must be agreed
with the workflow team before the dependent gate closes.

| Handover item | Required handover evidence | Proposed responsible roles |
|---|---|---|
| Open-source reference release | Identified release/tag and reproducible build, dependency notices and release approval; preserve the existing proprietary dependency exception | Repository steward, Technical Lead |
| Signed evidence pack | Acceptance signatures, verification reports, restore drill, penetration-test closure and accessibility audit | QA, Security, Accessibility, Operations |
| Runbooks and named owners | Deployment/restore/incident procedures, service ownership, credential rotation and escalation contacts | Adopting organisation, its contracted service providers and the handing-over team |
| Decision register and plain-English PRD | Current sources, resolved/open decisions and accepted implementation contracts | Product Owner, Technical Lead, continuing maintainer |
| Two-week hyper-care | Named on-call rota, escalation route, support start/end tied to actual handover | Sprint team and continuing maintainer |
| Continued code and roadmap ownership | Accepted repository/release responsibilities, issue triage, decision maintenance and change-control process | Proposed reference maintainer: Bodhan AI; scope and named contacts pending |

The completed reference release and handover must preserve the repository's
Apache-2.0 licence and the existing proprietary dependency exception. This
plan changes no repository visibility, permissions or licence.

## Continuation roadmap

The following are **after-sprint roadmap items**, not
additional 28 September acceptance requirements:

- Agency and single-point-of-contact layer.
- Reverse translation.
- Additional languages.
- Calibration hooks for difficulty and discrimination.
- Candidate challenge integration.
- The separate assembly module.

Boards and suppliers should be able to adopt or replace blocks while the
reference keeps contracts stable. Each roadmap item needs scope,
interfaces, ownership and acceptance evidence before delivery; no date or
implementation is claimed here.

## Decisions and readiness still to establish

The compressed schedule does not choose pilot languages, appoint content
reviewers or approve security defaults. Name the 6–8 engineers and the
required Assessment, Accessibility, QA, Security, content and Operations
owners; reserve reviewers/translators for the three-language proof; establish
IdP/key/store/scanner/monitoring test tenants and the assembly consumer.

Retain D-01/D-02 canonicalization, D-24 retention and D-48 translation-hosting
gates, together with the unresolved contracts in
[PRD reconciliation](prd-reconciliation.md). Track the actual completion
evidence against the deadline; do not turn this plan into a claim
that these prerequisites have already been met.
