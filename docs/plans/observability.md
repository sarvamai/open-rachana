# Operational observability

Proposed owner: **Irfan**. Technical reviewers: KKT; Rohit for leak and failure checks. Epic: [#105](https://github.com/Bodhan-AI/open-rachana/issues/105).

Start by verifying #111 against the merged #120 stack and continue #121 for #110. Next add server trace propagation, bounded client diagnostics and real domain dashboards. Keep durable integrity events with Kaustav and durable audit with Gandharva.

## Work and first deliverables

The order below is the module’s reading/build sequence. The dependencies in each brief determine integration order; independent fixture and design work can proceed while a producer is being built.

| Task | Deliverable |
|---|---|
| [#111](tasks/obs-local.md) | Qualify the merged local Collector/Grafana stack for another contributor’s clean environment. |
| [#110](tasks/obs-python.md) | Complete Python diagnostics around the merged OTel bootstrap without adding content leakage or workflow dependencies. |
| [#112](tasks/obs-next.md) | Propagate and observe safe request context from Next.js server routes to the Python API. |
| [#113](tasks/obs-client.md) | Add bounded diagnostics to browser oversight and the signed client under their separate runtime constraints. |
| [#114](tasks/obs-domain.md) | Create dashboards and actionable alerts for actual workflow services as they arrive. |

## Ownership boundaries

Own diagnostic logs, metrics, traces, Collector configuration, local dashboards and alerts. Session-integrity decisions and durable audit evidence remain with workflow/evidence owners.

## How to use this handoff

Read the first task brief, its exact PRD sections and the effective-rule notes. The brief contains the relevant source clauses, inputs, outputs, examples, dependencies and first deliverable. Propose implementation details in that brief or an attached plan PR; consumers review shared interfaces. Existing PRs and valid approvals stay in force. Only the named unresolved decision blocks its dependent behaviour; it does not require the whole module to wait.

For each implementation PR, retain the accepted contract/plan revision, requirement IDs, code, actual check result and remaining limits. Use [Humanizer](https://github.com/blader/humanizer) for new prose and read it yourself. Preserve quoted source text, IDs, numbers and security rules.
