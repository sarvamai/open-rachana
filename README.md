<p align="center">
  <img src="docs/assets/project-rachana-logo.png" alt="Project Rachana logo" width="180">
</p>

<h1 align="center">Project Rachana</h1>

<p align="center">
  An open-source <strong>question paper authoring system</strong> built for
  <strong>confidentiality</strong> and <strong>control</strong>.
</p>

<p align="center">
  <a href="https://github.com/sarvamai/open-rachana/actions/workflows/ci.yml"><img src="https://github.com/sarvamai/open-rachana/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache-2.0"></a>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Node-20-339933?logo=nodedotjs&logoColor=white" alt="Node 20">
  <img src="https://img.shields.io/badge/core-deterministic%20%C2%B7%20AI%20free-2EA44F" alt="Deterministic, AI-free core">
</p>

---

**Project Rachana** turns a blank page into a sealed, exam-ready question — through four
human jobs, under rules the examining authority owns.

This repository implements **Project Rachana**, whose product baseline is the
[reference documentation maintained here](docs/source-of-truth.md).
The repository is `sarvamai/open-rachana`; existing code-package identifiers
remain unchanged pending a separate compatibility decision. The product includes Layer 1
workflow and Layer 2 drafting; this tree currently contains the Layer 1
foundation, UI mocks and a client scaffold. The delivery target is
28 September 2026 for the complete reference; named Layer 2 delivery ownership
and integration contracts still need to be recorded.

In the PRD's V1, the Admin authors. Independent Question Reviewers check.
Accessibility Specialists remediate; separate Accessibility Reviewers decide.
Translators and Translation Reviewers handle each required language, followed
by that language's accessibility gate. The system seals each approved language
version; no routine human role, including the Admin, can reopen it. Only when
all required languages are sealed does it report readiness for paper assembly.

## Why it is different

- **Confidentiality by construction.** Sealed questions are unreadable to any human role.
  The audit trail is append-only and hash-chained — tampering is detectable — and carries
  no question content. Logs, traces, and error messages never see plaintext.
- **Humans decide; rules verify.** The workflow core contains **no AI**.
  Layer 2 drafts questions, translation text and metadata through a governed
  connector; Layer 1 validates inputs and requires human submission/review.
  The exact proposal-to-draft adoption step remains an explicit
  [reconciliation item](docs/prd-reconciliation.md), not an implemented flow.
- **The authority owns the core.** The rules, the records, the seal, and the export are
  open source under Apache-2.0 — no enterprise edition, no private fork.
- **No lock-in.** Identity, storage, keys, and models plug in behind versioned,
  conformance-tested provider interfaces. Switching any of them is a configuration
  change, not a rewrite.

## How it works

```
Admin draft → Question Review → Accessibility remediation → Accessibility Review
→ System seals original → Translation + Translation Review (per language)
→ Accessibility remediation + Accessibility Review → System seals each language
→ FULLY_APPROVED readiness → Assembly (metadata only)
```

Separation of duties prevents self-approval and conflicting review assignments.
After rejection, corrected work goes to a different reviewer. A return creates
a linked draft; the original remains immutable evidence. The server is
authoritative. See the complete [workflow and permissions](docs/product-workflow.md).

## Architecture

![Rachana: intelligence, workflow and managed services connected through adapters and bindings.](docs/assets/rachana-three-layer-architecture.png)

[Open the diagram at full size](docs/assets/rachana-three-layer-architecture.png)
or read the [architecture and trust boundaries](docs/architecture.md).
This is the design target; implementation status is below.

## Status

M0 — foundation. The current delivery plan is a **three-week sprint ending
28 September 2026**, with **6–8 volunteer engineers using coding agents**.
The [delivery plan](docs/delivery-plan.md) records the seven completion
outcomes, build scope, handover and continuation roadmap. M0–M6 below are
dependency/evidence gates, not calendar weeks. Closure requires retained
evidence and sign-off.

Partial M1 audit/session code exists, but its session API is unauthenticated
and its storage is in memory. The Python CI job is still a placeholder.
The [delivery status](docs/delivery-status.md) distinguishes existing code,
inspected test definitions, UI mocks and planned work. The table below lists
**targets**, not closed milestones.

| Milestone | Scope |
|---|---|
| M0 | Repository foundation, design record, provider interfaces |
| M1 | Identity, cycle & taxonomy, audit chain, walking skeleton |
| M2 | Authoring workspace: editor, validation, similarity check, submission |
| M3 | Review + accessibility gates, operator surface |
| M4 | Translation, sealing, readiness, downstream handoff |
| M5 | Hardening: production install, penetration test, WCAG audit |
| M6 | Production acceptance and handover pack |

## Documentation

| Document | Purpose |
|---|---|
| [`docs/source-of-truth.md`](docs/source-of-truth.md) | Reference baseline, document authority and contributor reading order |
| [`docs/product-workflow.md`](docs/product-workflow.md) | Product scope, permissions, full language workflow and required controls |
| [`docs/prd-reconciliation.md`](docs/prd-reconciliation.md) | Source/ADR conflicts, proposed resolutions and decision owners |
| [`docs/prd-decisions.md`](docs/prd-decisions.md) | All 48 PRD decisions, defaults and approval status |
| [`docs/delivery-status.md`](docs/delivery-status.md) | What exists, evidence limitations and remaining delivery work |
| [`docs/delivery-plan.md`](docs/delivery-plan.md) | 28 September sprint, completion outcomes, team, handover and continuation roadmap |
| [`docs/contributor-work-packages.md`](docs/contributor-work-packages.md) | Proposed engineer packages, integration boundaries and testing responsibilities |
| [`docs/architecture.md`](docs/architecture.md) | Layers, state machine, invariants, trust boundaries |
| [`docs/adr/`](docs/adr/) | Architecture decision records |
| [`docs/provider-contracts.md`](docs/provider-contracts.md) | How providers plug in and certify |
| [`docs/traceability.md`](docs/traceability.md) | Requirement → component → test index |
| [`docs/requirements.md`](docs/requirements.md) | All 302 unique numbered requirements, v4 aliases and planned verification |
| [`docs/canonicalization.md`](docs/canonicalization.md) | Current audit bytes and the unratified PRD v1 proposal |
| [`apps/web/README.md`](apps/web/README.md) | Web app: running it, and the vendored design system |
| [`deploy/dev/README.md`](deploy/dev/README.md) | Local observability stack: Collector and Grafana for development |

## Local observability

Traces and metrics from a local run are viewable in Grafana with the compose
stack under `deploy/dev/`; see [`deploy/dev/README.md`](deploy/dev/README.md).

## Contributing

Small, meaningful PRs; tests green before review; design decisions recorded as ADRs.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Confidentiality is this system's reason to exist. If you find a way to read sealed
content, bypass separation of duties, or tamper with the audit chain, please report it
privately — see [SECURITY.md](SECURITY.md).

## Licence

Apache-2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE). One vendored build
artefact, the `@sarvam/tatva` design system under `design-system/tatva/`, is
proprietary and sits outside that licence; `NOTICE` records the exception.
