# Testing framework and acceptance evidence

Proposed owner: **Rohit**. Technical reviewers: KKT; feature owners. Epic: [#107](https://github.com/Bodhan-AI/open-rachana/issues/107).

Start by continuing #96 for #52 and #98 for #49. Establish #115’s shared fixtures and the first manual-draft/independent-review path. Feature owners keep responsibility for their own tests; Rohit owns the shared harness and independent failure cases.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#52](tasks/issue-52.md) | Replace placeholder Python CI with actual tests and preserve the aggregate ci gate. |
| [#49](tasks/issue-49.md) | Make leakage of synthetic Restricted content fail the build across application logs, audit and diagnostics. |
| [#115](tasks/test-harness.md) | Provide shared fixtures and a contract/integration harness used by all feature owners. |
| [#86](tasks/issue-86.md) | Run independent security qualification against the implemented interfaces and deployment. |

## Ownership boundaries

Own the shared testing system and independent failure cases. Each feature owner writes tests for their implementation; expert security/accessibility acceptance still needs named people.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.
