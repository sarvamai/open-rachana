# Epic plan: Platform, identity and integration

Proposed owner: **KKT**. Technical reviewers: Gandharva; Rohit for recovery evidence.
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

Own verified identities, reproducible environments, organisation-contracted managed-service bindings, release recovery and integration. The adopting organisation may contract any provider(s) meeting the interfaces and controls; no named host is mandatory. The IdP identifies the actor; workflow determines their task permissions.

Expected locations: `deployment/configuration, identity adapters, contracts and integration pipeline`. These are shared-code ownership boundaries,
not new services. Changes to shared contracts need the consuming owner’s review.

## Child plans

| Issue | Plan |
|---|---|
| #41 | [As a staff member, I want to sign in through the organisation IdP with MFA](tasks/issue-41.md) |
| #43 | [As a staff member, I am refused unless device posture and network zone claims are present](tasks/issue-43.md) |
| #51 | [As an engineer, I want compose, a real Dockerfile, and platform.yaml so the pipeline deploys itself](tasks/issue-51.md) |
| #85 | [As the authority, I want production identity, keys, and managed-device checks](tasks/issue-85.md) |
| #88 | [As Ops, I want load, backup/restore, and chain verification passed in production](tasks/issue-88.md) |
| #94 | [Phase 1 leftovers: Makefile, canonicalization spec, as-built page](tasks/issue-94.md) |
| planned slice `release-recovery` | [Prove failed-release recovery without losing audit or sealed content](tasks/release-recovery.md) |
| planned slice `task-contract` | [Publish versioned task and identity contracts for parallel implementation](tasks/task-contract.md) |

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
