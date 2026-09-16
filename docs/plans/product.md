# Epic plan: Product acceptance and contributor onboarding

Proposed owner: **Nikhil**. Technical reviewers: KKT for technical steps; Rohit for testability.
Epic: #108.

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

Own scope, understandable issue briefs, user journeys and product acceptance. Do not invent pilot languages, participant commitments or technical/security approvals.

Expected locations: `product decisions, acceptance examples, contributor documentation`. These are shared-code ownership boundaries,
not new services. Changes to shared contracts need the consuming owner’s review.

## Child plans

| Issue | Plan |
|---|---|
| #39 | [As Content Operations, I want pilot languages and named people recorded](tasks/issue-39.md) |
| #40 | [As Product Owner, I want Week-1 product decisions recorded as ADRs](tasks/issue-40.md) |
| #89 | [As Product Owner, I want every acceptance criterion signed in one evidence pack and go-live recorded](tasks/issue-89.md) |
| #119 | [Verify the contributor first-run guide and first-PR path](tasks/onboarding.md) |

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
