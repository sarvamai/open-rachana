# Epic plan: Workspaces and signed client

Proposed owner: **Divyansh**. Technical reviewers: Kaustav; Accessibility lead for relevant checks.
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

Own task screens, accessible interaction, content-client restrictions and release packaging. Consume server permissions and task responses; never infer authorization from a hidden button.

Expected locations: `apps/client and the content-free configuration/oversight parts of apps/web`. These are shared-code ownership boundaries,
not new services. Changes to shared contracts need the consuming owner’s review.

## Child plans

| Issue | Plan |
|---|---|
| #58 | [As an Admin, I want to write and edit a single-select MCQ in the tool](tasks/issue-58.md) |
| #59 | [As an Admin, I want to add images and limited LaTeX to a question](tasks/issue-59.md) |
| #60 | [As an Admin, I cannot copy, cut, paste, print, download, or export question content](tasks/issue-60.md) |
| #65 | [As a Question Reviewer, I want to see only my assigned question and the allowed metadata](tasks/issue-65.md) |
| #69 | [As an Accessibility Specialist, I want to remediate accessibility fields only](tasks/issue-69.md) |
| #70 | [As an Accessibility Reviewer, I want to test the rendered question and decide](tasks/issue-70.md) |
| #72 | [As an Integrity Operator, I want a live board of sessions, scores, and events with no content](tasks/issue-72.md) |
| #73 | [As a Translator, I want to create and edit a translation after the original is sealed](tasks/issue-73.md) |
| #75 | [As a Translation Reviewer, I want original and translation side by side so I can approve or reject](tasks/issue-75.md) |
| #76 | [As an Accessibility Specialist, I want the same accessibility gate on every language version](tasks/issue-76.md) |
| #87 | [As the Accessibility lead, I want a WCAG 2.1 AA audit of authoring and review surfaces closed](tasks/issue-87.md) |
| planned slice `client-contract` | [Connect and release the signed desktop task client](tasks/client-contract.md) |

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
