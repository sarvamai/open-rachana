# Product acceptance and contributor onboarding

Proposed owner: **Nikhil**. Technical reviewers: KKT for technical steps; Rohit for testability. Epic: [#108](https://github.com/Bodhan-AI/open-rachana/issues/108).

Start with #40’s actual outstanding decisions and #39’s roster/preconditions. Verify #119 with a new contributor. Nikhil supplies expected behaviour and product acceptance; Security, Accessibility and Operations retain their own approvals.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#40](tasks/issue-40.md) | Maintain the product decision record and resolve the specific contradictions affecting the first implementation slices. |
| [#39](tasks/issue-39.md) | Prepare the named pilot roster and operating prerequisites used to configure a cycle. |
| [#119](tasks/onboarding.md) | Make the repository’s first-run and first-contribution route work for a new person. |
| [#89](tasks/issue-89.md) | Assemble release acceptance and handover evidence across every required product and operational obligation. |

## Ownership boundaries

Own scope, understandable issue briefs, user journeys and product acceptance. Do not invent pilot languages, participant commitments or technical/security approvals.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.
