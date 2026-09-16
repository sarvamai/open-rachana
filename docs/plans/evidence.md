# Audit, sealing and vault

Proposed owner: **Gandharva**. Technical reviewers: Kaustav; Security for key/retention controls. Epic: [#104](https://github.com/Bodhan-AI/open-rachana/issues/104).

Start with #46’s persistent atomic evidence contract. Coordinate with PR #101 for #47’s verifier. Publish the receipt, canonical-byte version and failure behaviour consumed by Kaustav before implementing sealing in #77.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#46](tasks/issue-46.md) | Persist the audit chain and make required workflow writes atomic with their evidence and outbox entries. |
| [#47](tasks/issue-47.md) | Expose content-free audit verification and detect missing, changed or reordered records and invalid anchors. |
| [#48](tasks/issue-48.md) | Give auditors a restricted evidence search and verification result without a question-content path. |
| [#77](tasks/issue-77.md) | Seal a fully evidenced version through the dedicated worker and protected KMS/object-store interfaces. |
| [#78](tasks/issue-78.md) | Prove that routine human and administrator credentials cannot retrieve sealed plaintext. |

## Ownership boundaries

Own durable evidence, canonical bytes, encryption/manifests, sealing retries and verification. The workflow owner decides legal state changes; this package returns verified receipts.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.
