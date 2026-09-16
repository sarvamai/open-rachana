# Layer 2 intelligence and adapters

Proposed owner: **Sarvam team — individual lead to be confirmed**. Technical reviewers: Kaustav; Security for translation hosting. Epic: [#109](https://github.com/Bodhan-AI/open-rachana/issues/109).

Start with #54’s curriculum/extraction contract, inspecting #93 first. Agree #55’s generation request with Kaustav, then #56’s provider/provenance/validation path. #57’s translation AI stays off until the specific data-release approvals exist.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#54](tasks/issue-54.md) | Ingest curriculum through quarantine, extraction and provenance records for generation. |
| [#56](tasks/issue-56.md) | Integrate Layer 2 generation as untrusted proposals with provenance and deterministic validation. |
| [#57](tasks/issue-57.md) | Keep the translation-draft AI channel disabled until its data-handling and hosting approval is recorded. |

## Ownership boundaries

Produce grounded proposals with provenance through governed adapters. No sealed content, workflow-store credentials or AI approval/validation paths. Layer 1 owns validation and human gates.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.

[Blueprint #55](tasks/issue-55.md) is owned by Kaustav and consumed by this module. The Sarvam team must name an individual integration owner; this document does not invent one.
