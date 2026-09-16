# Platform, identity and integration

Proposed owner: **KKT**. Technical reviewers: Gandharva; Rohit for recovery evidence. Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106).

Start with #117’s shared identity/task contract and #51’s development environment. Coordinate existing #93/#96 work. Build identity and device proof next; qualify production bindings and recovery only against the adopter’s selected services.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#117](tasks/task-contract.md) | Publish the versioned identity, task, decision and error contracts consumed across modules. |
| [#51](tasks/issue-51.md) | Provide a reproducible development environment for the API, persistence and service bindings. |
| [#41](tasks/issue-41.md) | Authenticate interactive users with the organisation IdP and produce the trusted identity context consumed by authorisation. |
| [#43](tasks/issue-43.md) | Enforce managed-device and approved-zone access at sign-in and refresh. |
| [#85](tasks/issue-85.md) | Bind and qualify production identities, keys, zones and privileged-operation controls. |
| [#116](tasks/release-recovery.md) | Define and demonstrate safe recovery from a failed application/schema release. |
| [#88](tasks/issue-88.md) | Measure performance and prove encrypted backup/restore against the PRD’s non-functional targets. |
| [#94](tasks/issue-94.md) | Keep commands, paths, byte-format descriptions and implementation status consistent with the merged repository. |

## Ownership boundaries

Own verified identities, reproducible environments, organisation-contracted managed-service bindings, release recovery and integration. The adopting organisation may contract any provider(s) meeting the interfaces and controls; no named host is mandatory. The IdP identifies the actor; workflow determines their task permissions.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.
