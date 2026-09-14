# Epic plan: Testing framework and acceptance evidence

Proposed owner: **Rohit**. Technical reviewers: KKT; feature owners.
Epic: #107.

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

Own the shared testing system and independent failure cases. Each feature owner writes tests for their implementation; expert security/accessibility acceptance still needs named people.

Expected locations: `CI, shared fixtures, contract/integration/end-to-end tests and evidence index`. These are shared-code ownership boundaries,
not new services. Changes to shared contracts need the consuming owner’s review.

## Child plans

| Issue | Plan |
|---|---|
| #49 | [As the System, I want CI to fail if logs, errors, or audit fixtures contain question content](tasks/issue-49.md) |
| #52 | [As an engineer, I want CI to run platform pytest so a green PR is evidence](tasks/issue-52.md) |
| #86 | [As Security, I want a penetration test against isolation, seal, SoD, and export closed](tasks/issue-86.md) |
| #115 | [Build shared contract fixtures and the first end-to-end acceptance harness](tasks/test-harness.md) |

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
