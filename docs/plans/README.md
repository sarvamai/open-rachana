# Engineering handoff: start here

This is the repository handoff for all eight modules: 62 task-specific briefs, the complete retained PRD, and a map of all 302 numbered requirements. The briefs state the product contract and leave implementation design to the engineer. They are proposed for technical review; publication does not claim feature delivery or expert acceptance.

If browsing `main` before PR #100 merges, the expanded files are on the `pr2-product-reference` branch. PR #99 contains the contributor allocation; PR #100 carries this complete reference and handoff. Merge #99 first. Both PRs need the repository’s required checks and code-owner approval. No contributor should need the chat history or an external document to locate a product rule.

## Pick your module

| Contributor | Module and issues | Begin with |
|---|---|---|
| Kaustav | [Workflow and business rules](workflow.md) / [#103](https://github.com/Bodhan-AI/open-rachana/issues/103) | [#42](tasks/issue-42.md) |
| Divyansh | [Workspaces and signed client](client.md) / [#102](https://github.com/Bodhan-AI/open-rachana/issues/102) | [#118](tasks/client-contract.md) |
| Gandharva | [Audit, sealing and vault](evidence.md) / [#104](https://github.com/Bodhan-AI/open-rachana/issues/104) | [#46](tasks/issue-46.md) |
| KKT | [Platform, identity and integration](platform.md) / [#106](https://github.com/Bodhan-AI/open-rachana/issues/106) | [#117](tasks/task-contract.md) |
| Irfan | [Operational observability](observability.md) / [#105](https://github.com/Bodhan-AI/open-rachana/issues/105) | [#111](tasks/obs-local.md) |
| Rohit | [Testing framework and acceptance evidence](testing.md) / [#107](https://github.com/Bodhan-AI/open-rachana/issues/107) | [#52](tasks/issue-52.md) |
| Nikhil | [Product acceptance and contributor onboarding](product.md) / [#108](https://github.com/Bodhan-AI/open-rachana/issues/108) | [#40](tasks/issue-40.md) |
| Sarvam team — individual lead to be confirmed | [Layer 2 intelligence and adapters](intelligence.md) / [#109](https://github.com/Bodhan-AI/open-rachana/issues/109) | [#54](tasks/issue-54.md) |

## Read the product contract

- [Current product workflow and permissions](../product-workflow.md): the short explanation of roles, lifecycle and boundaries.
- [Effective rules and conflicts](effective-rules.md): how source amendments apply; what an engineer may choose; what needs an owner decision.
- [Full main PRD](../prd/main-baseline.md): includes the complete role matrix and product journeys.
- [Full technical PRD](../prd/technical-baseline.md): includes field/schema definitions, validation and structural catalogues, errors, sample payloads, performance limits, edge cases and acceptance criteria.
- [Requirement coverage](coverage.md): one primary task for each of the 302 numbered requirements, with related consumers and narrative obligations.
- [Decision register](../prd-decisions.md) and [reconciliation](../prd-reconciliation.md): retain actual approval status; a proposed default is not an owner decision.

The retained PRDs contain historical wording and calendars. Use [source precedence](../source-of-truth.md), effective rules and the current [delivery plan](../delivery-plan.md) when they differ. The word `GAP` in a source clause denotes an addition made in the PRD, not missing implementation instructions.

## First integrated flow

KKT supplies identity and a shared environment; Gandharva supplies persistent audit/transaction receipts; Kaustav supplies permissions, configuration, draft and decision services; Divyansh consumes those contracts in the signed client. Rohit tests a manual draft through independent review, including a direct-API self-approval refusal. Irfan correlates diagnostics without receiving content. Nikhil verifies the expected user behaviour. The Layer 2 team can develop candidate/provenance fixtures alongside this flow.

Extend that same flow through separate accessibility remediation/review, system sealing, languages and machine-only readiness. Rendering, sealed-reference release and deployment-policy decisions stop only the affected paths. Production acceptance still requires the recorded expert and operating prerequisites.

## Work already in progress

Snapshot checked 16 September 2026 against main `55f3b1c`:

| Work | Current evidence | Contributor action |
|---|---|---|
| Python OTel bootstrap and local stack | #120 merged | Reuse it; #110/#111 are not greenfield tasks |
| Structured logs, audit metrics and provider spans | #121 open | Continue/review that PR before duplicating #110 |
| Persistent/audit verification work | #101 open | Coordinate #47; verify which backing store it covers |
| Content-leak CI suite | #98 open | Continue #49 there |
| Product decision ADRs | #97 open, changes requested | Reconcile source and numbering; do not treat it as accepted |
| Real Python CI | #96 open | Continue #52; main still has placeholder Python steps |
| Source/extraction and architecture recovery | #93 open | Coordinate #54/#94 and shared files |

Existing issue assignees and valid approvals are preserved. The names in this plan are proposed ownership, not a claim that someone committed time. Owners confirm capacity; the target date does not establish volunteer availability.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.

## Check this handoff

Run `python3 docs/plans/validate_handoff.py` from the repository root to verify task coverage, preserved requirement clauses, dependencies and local section links. This validates the documentation, not product acceptance.
