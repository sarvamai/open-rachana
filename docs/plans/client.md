# Workspaces and signed client

Proposed owner: **Divyansh**. Technical reviewers: Kaustav; Accessibility lead for relevant checks. Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102).

Start with the #118 client integration boundary and #58 manual draft screen. Use #117’s synthetic contract while server producers are under construction. Ship the first real draft flow before adding every role screen. Each content surface runs in the signed client; only configuration/content-free oversight belongs in the web app.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#118](tasks/client-contract.md) | Connect, enrol and package the signed desktop client for authorised content tasks. |
| [#58](tasks/issue-58.md) | Build the signed-client manual authoring screen with accessible content fields, autosave and field-level validation. |
| [#59](tasks/issue-59.md) | Implement safe image and equation handling from upload through rendering and validation. |
| [#60](tasks/issue-60.md) | Enforce and report supported restricted actions in the signed content client before the editor starts. |
| [#65](tasks/issue-65.md) | Deliver a read-only review workspace with strict payload isolation and assigned-task access. |
| [#69](tasks/issue-69.md) | Build field-limited accessibility remediation and immutable completion by the Accessibility Specialist. |
| [#70](tasks/issue-70.md) | Implement independent accessibility review with structured findings and accommodation outcomes. |
| [#72](tasks/issue-72.md) | Build the content-free Integrity Operator surface and reconnecting live session feed. |
| [#73](tasks/issue-73.md) | Build the translation workspace around a scoped read-only primary reference and editable target text. |
| [#75](tasks/issue-75.md) | Implement independent translation review and explicit equivalent-difficulty judgement. |
| [#76](tasks/issue-76.md) | Apply the accessibility remediation and independent review pipeline to each language variant. |
| [#87](tasks/issue-87.md) | Qualify all required role surfaces with keyboard, screen reader and supported-script checks. |

## Ownership boundaries

Own task screens, accessible interaction, content-client restrictions and release packaging. Consume server permissions and task responses; never infer authorization from a hidden button.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.
