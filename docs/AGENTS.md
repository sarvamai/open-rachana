# `docs/` — the design record

This directory is the reason the project can claim the authority owns its
rules. Treat it as a record, not as notes: it is written to be read by a
reviewer, an auditor, and an implementer years from now.

Read the root `AGENTS.md` first.

## What each file is for

| File | Contract |
|---|---|
| `source-of-truth.md` | Product baseline, source precedence, tab versions and retrieved revision. |
| `product-workflow.md` | PRD scope, permissions, full per-language workflow and acceptance-relevant controls. |
| `prd-reconciliation.md` | Source/ADR conflicts, proposed resolutions, owner roles and dependent work. R-numbers are review items, not requirements. |
| `prd-decisions.md` | All 48 source D-nn decisions, defaults and evidence of approval. |
| `requirements.md` | All 302 unique numbered PRD requirements, source wording, aliases, planned checks and evidence status. |
| `delivery-status.md` | Dated implementation snapshot, inspected test definitions and evidence limits. |
| `delivery-plan.md` | Sprint baseline, seven completion outcomes, build gates, managed services, handover and roadmap. |
| `contributor-work-packages.md` | Proposed contributor allocation, module boundaries, first contributions, shared contracts and acceptance responsibilities; not confirmed assignments. |
| `canonicalization.md` | Existing draft-v0.1 audit bytes; proposed v1 kept separate until ratified. |
| `plans/README.md` | Epic ownership, checked-in task plans, review/go-ahead workflow and Humanizer readability guidance. |
| `architecture.md` | Layers, the state machine, the ten numbered invariants, trust boundaries, non-functional targets. The invariants are the normative part. |
| `adr/NNNN-<slug>.md` | One decision each, numbered sequentially; preserve its actual accepted/proposed status. |
| `provider-contracts.md` | The working contract for provider authors: lifecycle, rules, SPI catalogue. |
| `traceability.md` | Canonical/v4 crosswalk, planned components/milestones, narrative acceptance obligations and closure rules. |
| `observability.md` | Working contract for observability: decisions table, what is instrumented, the content-free guard, configuration, local stack, infra guidance. ADR-0011 is the decision. |
| `observability-plan.md` | The execution plan for `observability.md`: five slices, one PR each, with tests and code. Tick tasks as they land; delete or archive it when the last slice merges. |

These documents describe the target through M6 and may name paths that do
not exist yet (`providers/`, `db/`, `contracts/`, `tests/conformance/`,
`platform.yaml`). Label those as planned. Preserve the target architecture
while keeping delivery status and acceptance evidence distinct. The root
`AGENTS.md` and `delivery-status.md` list the gap; a document is not evidence
that a component exists.

## Writing an ADR

Copy the shape of an existing one; do not invent a new template. The sections
are `Status` / `Deciders` / `Date`, then `## Context`, `## Decision`,
`## Rationale`, `## Alternatives considered`, `## Consequences`.

- **Alternatives considered is not a formality.** Every existing ADR names the
  real competing options and why each lost — including options that were
  better on some axis. An ADR with a straw-man alternative is worse than none.
- **Consequences includes the costs**, not just the benefits. ADR-0001 records
  that two runtimes now exist in CI; ADR-0003 records what pluggability costs.
- **Amend, never silently contradict.** When a decision changes, amend the ADR
  in place with a dated note in `Status` and a subsection explaining the
  change and its consequences — ADR-0001's Next.js amendment is the worked
  example. Supersede with a new ADR only when the whole decision is replaced.
- Cite canonical PRD IDs (ASM/INS/ARC/SEC/DAT/INT/ASR/RES/UI/PRD) inline
  where applicable. Existing QST/FND IDs remain traceable through the v4
  crosswalk. Don't invent IDs; `requirements.md` retains the source rows.

## Discipline that is easy to break

- **Never put question content, real candidate data, or anything Restricted in
  an example.** Examples use placeholders and opaque references — the same rule
  the audit chain enforces in code.
- Keep traceability honest: target milestones and planned check labels are
  intent; acceptance requires a linked commit, actual check, dated result and
  named sign-off. Update `requirements.md` and `delivery-status.md` as evidence
  lands. Never infer closure from a test name or a UI mock.
- Retain GAP and D-nn qualifiers in extracted source wording. Update both
  source tabs/revision when refreshing; do not silently turn a recommendation
  into an approved value. Source contradictions belong in `prd-reconciliation.md`.
- British spelling, as used throughout (`licence`, `artefact`, `behaviour`).
- Use tables and prose to explain controls. The Product Owner explicitly
  requested the architecture diagram: preserve it in
  `assets/rachana-three-layer-architecture.png`. These repository documents
  are the standalone reference; external source links are not required.
  The review deck's slide 4 and all its information are excluded.
- M0–M6 are evidence gates; `delivery-plan.md` supplies the current calendar
  target. Keep planned responsibilities distinct from delivery evidence.

## Keeping this file true

Update it when you add a document here, change the ADR template, or create a
planned file the root `AGENTS.md` still lists as absent.

## Plans and readability

Before new implementation, check in or update the relevant `docs/plans/` plan.
Link its approved revision and go-ahead in the issue. Preserve valid prior
approvals and existing work; new plans do not silently reset them.
Use the Humanizer skill linked in `plans/README.md`, then check the prose
personally. Preserve requirements, numbers, interfaces and security rules.
