# Workflow and business rules

Proposed owner: **Kaustav**. Technical reviewers: KKT; Gandharva for transaction/evidence boundaries. Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103).

Start with #42: implement and review the policy evaluator against the embedded role matrix. Then agree #45’s version/state model and #44’s configuration with the persistent evidence contract in #46. The first integrated result is manual draft creation, deterministic validation and independent review; translation/correction work comes after its specific reference-release decisions.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#42](tasks/issue-42.md) | Enforce the role-by-operation matrix on every server request and maintain the recognised-capability registry. |
| [#44](tasks/issue-44.md) | Build versioned cycle, taxonomy and vocabulary configuration with the content-free Admin surface. |
| [#45](tasks/issue-45.md) | Define artefact identity, immutable versions, lineage and the closed lifecycle used by all workflow services. |
| [#53](tasks/issue-53.md) | Create and autosave manual drafts under the active cycle, with author cap enforcement and server receipts. |
| [#61](tasks/issue-61.md) | Implement the complete deterministic validation catalogue and return stable field-specific findings. |
| [#62](tasks/issue-62.md) | Perform deterministic similarity checks against the same-language sealed bank without revealing sealed text. |
| [#67](tasks/issue-67.md) | Assign tasks by recognised capability, duty eligibility and deterministic workload order. |
| [#63](tasks/issue-63.md) | Submit a draft atomically into immutable review with evidence and a reproducible receipt. |
| [#68](tasks/issue-68.md) | Enforce separation of duties across the entire version lineage and every approval endpoint. |
| [#66](tasks/issue-66.md) | Record question-review decisions with complete attestations and immutable rejection history. |
| [#50](tasks/issue-50.md) | Complete authenticated, durable session-integrity ingestion and server-side scoring around the existing session scaffold. |
| [#71](tasks/issue-71.md) | Declare and verify expected evidence for each protected transition and sealed version. |
| [#74](tasks/issue-74.md) | Implement all structural translation checks and scoped, expiring exception enforcement. |
| [#79](tasks/issue-79.md) | Create one current translation draft and task per required language after successful primary sealing. |
| [#80](tasks/issue-80.md) | Maintain materialised readiness whenever a current seal, policy or lineage input changes. |
| [#81](tasks/issue-81.md) | Publish machine-only readiness queries for the separate assembly module. |
| [#82](tasks/issue-82.md) | Accept signed selection/completion notifications and apply Used/Archived transitions idempotently. |
| [#83](tasks/issue-83.md) | Authorise corrections, revoke readiness immediately and preserve all sealed history through revalidation and supersession. |
| [#84](tasks/issue-84.md) | Retire approved artefacts with re-authentication, preserved evidence and downstream notification. |
| [#55](tasks/issue-55.md) | Record generation blueprints and translate their counts and constraints into independent candidate requests. |
| [#64](tasks/issue-64.md) | Withdraw an unsubmitted draft without deleting its content or evidence. |

## Ownership boundaries

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.
