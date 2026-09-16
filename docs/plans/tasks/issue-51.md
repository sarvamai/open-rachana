# #51: As an engineer, I want compose, a real Dockerfile, and platform.yaml so the pipeline deploys itself

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Provide a reproducible development environment for the API, persistence and service bindings.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Extend the existing deploy/dev setup with the agreed persistence and test identity services; document destructive reset separately from normal restart.

## Inputs and outputs

- Input: Versioned configuration, test credentials/identities, database and provider bindings, existing deploy/dev observability stack.
- Output: Documented start/stop/reset/health commands and isolated synthetic data, with persistent volumes where needed and explicit missing-binding failures.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-DAT-09](../../requirements.md#req-prd-dat-09) | GAP Data lives in three stores with distinct identities: the working store (relational; drafts, versions, decisions, assignments, configuration, sessions), the repository (sealed objects, manifests, bank index; separate credentials and network segment, ARC-11), and the audit store (append-only chain, checkpoints, integrity events). The pseudonym mapping table is in a fourth, most restricted schema. | MUST |

## Exact PRD sections

- [10.4 Constraints the technology stack must satisfy](../../prd/technical-baseline.md#104-constraints-the-technology-stack-must-satisfy)
- [10.7 Egress, secrets, environments](../../prd/technical-baseline.md#107-egress-secrets-environments)
- [14.1 Week 1 — Foundation and evidence backbone](../../prd/technical-baseline.md#141-week-1--foundation-and-evidence-backbone)

## Behaviour to demonstrate

A new contributor starts the environment, creates synthetic state, restarts and sees it preserved. Missing KMS binding is reported without falling back to a fake production key.

Failure checks: Follow setup on a clean environment and restart it with persisted data. Missing required bindings must fail explicitly without leaking secrets.

Existing issue acceptance criteria, retained for review:

- [ ] Dockerfile runs `core-api` (today it is a placeholder)
- [ ] Compose starts api, Postgres, Keycloak
- [ ] Example `platform.yaml` is committed with no secrets
- [ ] `db/` migrations exist for the M1 tables
- [ ] `docs/runbook.md` (or equivalent) brings a clean machine to `/healthz` with resolved provider bindings

## Dependencies and decisions

No upstream feature is required to prepare the first deliverable.

D-28/D-30 deployment selections belong to the adopter/technical lead. Local reference services do not appoint a mandatory managed-service vendor.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
