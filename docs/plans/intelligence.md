# Epic plan: Layer 2 intelligence and adapters

Proposed owner: **Sarvam team — individual lead to be confirmed**. Technical reviewers: Kaustav; Security for translation hosting.
Epic: #109.

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

Produce grounded proposals with provenance through governed adapters. No sealed content, workflow-store credentials or AI approval/validation paths. Layer 1 owns validation and human gates.

Expected locations: `curriculum ingestion and replaceable generation/translation/metadata adapters`. These are shared-code ownership boundaries,
not new services. Changes to shared contracts need the consuming owner’s review.

## Child plans

| Issue | Plan |
|---|---|
| #54 | [As an Admin, I want to upload a curriculum PDF](tasks/issue-54.md) |
| #56 | [As an Admin, I want Layer 2 to draft candidate questions from the curriculum and blueprint](tasks/issue-56.md) |
| #57 | [As Security, I want the translation-draft model channel off until the model runs inside our boundary](tasks/issue-57.md) |

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
