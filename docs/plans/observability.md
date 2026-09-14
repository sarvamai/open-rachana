# Epic plan: Operational observability

Proposed owner: **Irfan**. Technical reviewers: KKT; Rohit for leak and failure checks.
Epic: #105.

## Review before implementation

Status: draft plan; owner review and go-ahead are pending. Nikhil reviews product
scope and acceptance. KKT coordinates technical/interface review; Rohit reviews
the test approach. Record the plan PR, approved revision and go-ahead in the issue.
Security/accessibility decisions still need their named owners. Existing valid
approvals and in-flight work are preserved; this plan does not revoke them.

Run [Humanizer](https://github.com/blader/humanizer) on prose before requesting
review, then read it yourself. Preserve requirements, IDs, API names, numbers,
MUST/MUST NOT rules, acceptance criteria and approval status. Clarity is the
criterion; an AI-detection score is not. If your agent cannot load the skill,
apply its documented writing guidance manually and say so.

## Scope and interfaces

Own diagnostic logs, metrics, traces, Collector configuration, local dashboards and alerts. Session-integrity decisions and durable audit evidence remain with workflow/evidence owners.

Expected locations: `runtime instrumentation and deploy/dev observability configuration`. These are shared-code ownership boundaries,
not new services. Changes to shared contracts need the consuming owner’s review.

## Child plans

| Issue | Plan |
|---|---|
| #110 | [Instrument Python API logs, metrics and traces](tasks/obs-python.md) |
| #111 | [Provide the local Collector and Grafana observability stack](tasks/obs-local.md) |
| #112 | [Connect Next.js server instrumentation to API traces](tasks/obs-next.md) |
| #113 | [Add bounded browser and signed-client diagnostic telemetry](tasks/obs-client.md) |
| #114 | [Add workflow dashboards and tested operational alerts](tasks/obs-domain.md) |

## Owner’s first PR

Review these starter plans against current code. Settle interfaces and the first
small slice, record available capacity and return the plan PR for review. Keep
open policy decisions explicit. Extended work can use a separate plan file;
small work can remain in its linked task plan. Do not duplicate the existing
observability spec or implementation plans: reference and amend them.

## Acceptance and handover

The epic closes when its child acceptance criteria have retained evidence,
its interfaces work in the shared flow, and its runbooks/limitations are
reviewed by another contributor. The primary owner is responsible for integration
with consumers; Rohit supplies the shared harness and Nikhil reviews product
behaviour. Humanizer is a prose review step, not technical approval.
