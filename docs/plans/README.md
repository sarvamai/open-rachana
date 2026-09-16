# Plans and issue workflow

For the complete task briefs and embedded PRD, use the [engineering handoff in PR #100](https://github.com/Bodhan-AI/open-rachana/blob/pr2-product-reference/docs/plans/README.md). The starter plans on this branch are retained for PR #99 review; the expanded handoff supersedes them when #100 lands.

Status: proposed workflow in PR #99. These starter plans are ready for owner
review; they are not recorded implementation approvals.

One person owns each functional epic. The existing M2–M6 epics remain milestone
acceptance views. A task has one primary owner even when other packages review
or supply its interfaces.

1. The owner checks in the epic plan and the plan for the next small task.
2. Nikhil reviews product scope and expected behaviour. KKT coordinates
   technical/interface review; Rohit reviews tests. Record any required
   Security or Accessibility decisions with their owners.
3. Record the accepted plan revision and explicit go-ahead in the issue.
4. Implement a small PR against that plan. A planning skill may turn an
   approved plan into tickets, but must preserve requirements, dependencies
   and unresolved decisions. Tool-generated tickets do not approve themselves.
5. Link implementation, actual checks and retained results. Close only when
   the acceptance owner agrees. Preserve valid existing approvals and in-flight work.

New gap tickets initially request plan review. Existing tickets retain their
stories and acceptance criteria, with a planning handoff added at the top.
No contributor is assigned or committed on their behalf.

## Readability

Use [Humanizer](https://github.com/blader/humanizer) on plans, issue prose and
PR descriptions before asking another person to review them. Then read the
result yourself. Keep sentences direct and examples concrete. Preserve IDs,
API names, commands, numbers, MUST/MUST NOT rules, acceptance criteria and
approval status. Use the skill's documented manual guidance if an agent does
not support it. There is no AI-detection score or automatic approval gate.

## Functional epics

| Epic | Proposed owner | Plan |
|---|---|---|
| #102 — Workspaces and signed client | Divyansh | [client.md](client.md) |
| #103 — Workflow and business rules | Kaustav | [workflow.md](workflow.md) |
| #104 — Audit, sealing and vault | Gandharva | [evidence.md](evidence.md) |
| #105 — Operational observability | Irfan | [observability.md](observability.md) |
| #106 — Platform, identity and integration | KKT | [platform.md](platform.md) |
| #107 — Testing framework and acceptance evidence | Rohit | [testing.md](testing.md) |
| #108 — Product acceptance and contributor onboarding | Nikhil | [product.md](product.md) |
| #109 — Layer 2 intelligence and adapters | Sarvam team — individual lead to be confirmed | [intelligence.md](intelligence.md) |

## Integration order

Begin with real CI and a shared environment, then identity, persistent audit,
cycle/version contracts and a manual draft. Add independent review with a
self-approval refusal, a correlated trace and atomic evidence. Extend the same
flow through accessibility, sealing, languages and readiness, then qualify
recovery and operational acceptance. Diagnostic setup and Layer 2 contract
fixtures can proceed in parallel. Actual dependencies are listed per task.

The current 28 September target does not establish volunteer capacity. Owners
must confirm availability and interim checkpoints before promising dates.
No security or acceptance gate is removed to fit the target.

## Coverage and current work

Every open delivery story #39–89 and the related cleanup issue #94 has one
primary package and a checked-in task plan. Closed historical issues are left
alone. Issue #92 and PR #93 are existing recovery work; check their status before
starting overlapping extraction, CI, Makefile or canonicalisation changes.
The requirement register and unresolved decisions are reviewed in PR #100.
Owners must map their actual tests to the applicable requirements before closure;
this task inventory does not claim all 302 requirements are already implemented
or accepted.
