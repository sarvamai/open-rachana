# Reference baseline and document control

Review status: proposed for maintainer review through a documentation PR.

The documentation in this repository is intended to become the maintained
product and delivery reference for **Project Rachana** on acceptance. Contributors should use these documents
for scope, workflow, architecture, requirements, decisions and delivery
planning. External documents are historical inputs; later changes to them
do not silently change this baseline. The project name is **Project Rachana** and the current repository is
`sarvamai/open-rachana`. Existing import/package identifiers remain technical
compatibility names pending a separate rename decision.

## The reference set

| Document | Authority |
|---|---|
| [Product workflow](product-workflow.md) | Product scope, role permissions, per-language workflow and control obligations |
| [Architecture](architecture.md) | Embedded architecture diagram, three layers, trust boundaries and ten invariants |
| [Delivery plan](delivery-plan.md) | Three-week sprint ending 28 September 2026, seven completion outcomes, team, build gates, handover and continuation |
| [Requirements](requirements.md) | 302 unique numbered requirements, original wording and priority, planned verification and evidence status |
| [Traceability](traceability.md) | Requirement/component/check/acceptance mapping and narrative obligations |
| [Decision register](prd-decisions.md) | 48 inherited decisions, proposed defaults and later decision evidence |
| [Reconciliation](prd-reconciliation.md) | Remaining conflicts and unresolved contracts, with owner roles and dependent work |
| [Architecture decisions](adr/) | Accepted or proposed implementation choices, preserving each record's status |
| [Delivery status](delivery-status.md) | Inspected implementation and evidence limits; baseline commit `5627bd1574beb56ec6a1a8de97f83a5525870c9c` |

This is a design and delivery baseline, not proof that features exist or that
all defaults have been approved. Open decisions and implementation gaps
remain visible until the required owner acts and evidence is retained.

## Recorded owner decisions — 14 September 2026

- Admin authoring and unsealed-content work run in the signed desktop client;
  configuration and content-free oversight run in the web app. R1 and the
  amendment to ADR-0008 record the placement.
- Curriculum, generation constraints and candidate counts belong to Rachana.
  Final paper selection, ordering and export belong to the separate assembly
  module. R3 and ADR-0013 record the boundary.
- The repository incorporates the review plan and its actual architecture
  diagram and becomes the standalone reference. External source links are
  omitted at the owner's request. The review deck's slide 4 and all its
  information are excluded.

The current delivery target replaces the older five-build-week/three-day-
closeout calendar. M0–M6 remain dependency/evidence gates, not additional
weeks. Interim dates and named-person appointments remain to be assigned.
Sarvam AI is the planned pilot intelligence provider. The Product Owner
clarified that Layer 3 is supplied by any provider(s) contracted by the
organisation adopting the authoring engine. Bodhan AI is not a mandatory host.
Its proposed reference-maintenance role is separate from deployment services.
The separate Author-role and proposal-adoption clarification remains open in
R4; the baseline's Admin-only wording does not settle that pending decision.

## Change and conflict rules

1. Apply an explicit recorded Product Owner decision for product scope.
   Update the affected reference documents and decision evidence together.
2. Use the workflow, architecture, numbered requirements and delivery plan
   together. Preserve requirement IDs and mandatory controls. Shortening the
   schedule does not remove acceptance obligations.
3. Keep accepted ADRs that meet the product contract. An ADR cannot silently
   remove a requirement; reference wording cannot silently approve a new
   platform, role surface or production security exception.
4. Record unresolved conflicts and missing contracts in the reconciliation
   register, with proposed resolution, owner and affected work. Do not invent
   a decision or weaken an implemented control to make prose agree.
5. Establish completion from code and retained acceptance results. Update
   delivery status and requirement evidence together; design prose is not
   proof of implementation.

Open recommendations remain the design baseline until the responsible owner
decides, with open status preserved in the decision register. Explicit gates
still apply: D-24 retention has no default; D-48 translation drafting remains
off until Security approves its hosting; production acceptance requires
signed evidence. Becoming the reference does not ratify proposed defaults.

## Baseline history

The initial reconciliation used the High Level PRD v2.0 and Detailed Spec
v1.3, both dated 7 September 2026, retrieved on 14 September. The file title
was `Project_Rachana_PRD_v1.3`; the annex labelled itself Draft for engineering
review. Its numbered requirement rows, priorities and decision rows are
preserved in the local registers. Older v4 requirements are crosswalked there.
Section references to the main PRD or annex identify this historical baseline;
they do not override the later decisions recorded above.

The review plan dated 15 September 2026 supplied the sprint, team, architecture,
build scope and handover/continuation material from slides 1, 2, 3 and 5.
The architecture image is retained locally, with a text explanation in the
architecture document. No full copy of that presentation is included.

Historical extraction revision (retained for audit, not a live dependency):

`ANLCKQnY0vC7t2_jcvVwFo3N2HM94T2ElawGBLtJ_mgoyytkE_Sc09jt13D8w3MS9K9Mm0frwhHDIzE557oqabnu84Vc4AUCMETLTRxy-qk`

## Reading order

1. This baseline, the delivery plan and current delivery status.
2. Product workflow and permissions.
3. Architecture and relevant accepted ADRs.
4. Traceability, individual requirements and applicable decisions.
5. Reconciliation items before work that depends on an unresolved boundary.
