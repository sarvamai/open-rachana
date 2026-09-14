# Epic plan: Workflow and business rules

Proposed owner: **Kaustav**. Technical reviewers: KKT; Gandharva for transaction/evidence boundaries.
Epic: to be created.

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

Own legal transitions, capability policy, assignments, validation, review/language gates, readiness and corrections. State changes and required audit events share one transaction.

Expected locations: `platform/core domain services, validators, API and event schemas`. These are shared-code ownership boundaries,
not new services. Changes to shared contracts need the consuming owner’s review.

## Child plans

| Issue | Plan |
|---|---|
| #42 | [As the System, I want every request authorised from the capability matrix](tasks/issue-42.md) |
| #44 | [As an Admin, I want to configure a cycle and its taxonomy](tasks/issue-44.md) |
| #45 | [As the System, I want every question to have a QB-id, immutable versions, and a closed state machine](tasks/issue-45.md) |
| #50 | [As the System, I want content sessions to heartbeat and the first monitoring signal to reach the audit in seconds](tasks/issue-50.md) |
| #53 | [As an Admin, I want to create a DRAFT and receive a receipt](tasks/issue-53.md) |
| #55 | [As an Admin, I want to define a blueprint for an assessment](tasks/issue-55.md) |
| #61 | [As an Admin, I want submit blocked until validation passes, with each finding naming the field](tasks/issue-61.md) |
| #62 | [As an Admin, I want submit refused when the question is too similar to a sealed question](tasks/issue-62.md) |
| #63 | [As an Admin, I want submit to freeze the version, hash it, and give me a receipt](tasks/issue-63.md) |
| #64 | [As an Admin, I want to withdraw a draft instead of deleting it](tasks/issue-64.md) |
| #66 | [As a Question Reviewer, I want to comment, approve against the checklist, or reject with a reason](tasks/issue-66.md) |
| #67 | [As the System, I want to assign one eligible reviewer per question per stage by workload](tasks/issue-67.md) |
| #68 | [As the System, I want self-approval and cross-stage reuse of the same person to fail on the API](tasks/issue-68.md) |
| #71 | [As the System, I want missing expected evidence to block the next step and raise an alert](tasks/issue-71.md) |
| #74 | [As a Translator, I want submit blocked if I change locked structure, numbers, or media](tasks/issue-74.md) |
| #79 | [As the System, I want sealing the original to create the translation drafts](tasks/issue-79.md) |
| #80 | [As the System, I want FULLY_APPROVED only when the original and every required language are sealed](tasks/issue-80.md) |
| #81 | [As Assembly, I want a machine-identity API that returns readiness metadata and never content](tasks/issue-81.md) |
| #82 | [As Assembly, I want to mark a question USED and later ARCHIVED via signed messages](tasks/issue-82.md) |
| #83 | [As an Admin, I want to authorise a correction that revokes readiness and starts a new lineage](tasks/issue-83.md) |
| #84 | [As an Admin, I want to retire an approved question rather than delete it](tasks/issue-84.md) |

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
