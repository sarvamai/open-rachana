# #81: As Assembly, I want a machine-identity API that returns readiness metadata and never content

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Publish machine-only readiness queries for the separate assembly module.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement schema and authentication tests against #80 fixtures; then connect the materialised records.

## Inputs and outputs

- Input: Mutual TLS and assembly-readiness workload token, cycle/subject/language/status/updated-since filters and opaque cursor.
- Output: Allowlisted readiness metadata with no-store caching and bounded pagination, through the PRD list/detail endpoints.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM07-RDY-02](../../requirements.md#req-asm07-rdy-02) | A machine-only, authenticated, paginated interface exposes opaque identifiers, languages, item type, classification, difficulty, taxonomy level, marking, readiness and sealed references. | MUST |
| [ASM07-RDY-03](../../requirements.md#req-asm07-rdy-03) | The response contains no stem, option, answer, explanation, comment or asset bytes. | MUST |
| [ASM07-RDY-04](../../requirements.md#req-asm07-rdy-04) | Human tokens and wrong-audience workload tokens are rejected by the interface. | MUST |
| [PRD-RDY-08](../../requirements.md#req-prd-rdy-08) | GAP Interface: GET /assembly/v1/readiness with filters cycle, subject, language, readiness status and updated-since, opaque cursor pagination with a page size of at most 200; GET /assembly/v1/readiness/{artefact_id}. Authentication is mutual TLS plus a short-lived token whose audience is assembly-readiness; any other audience or a human token returns REJECTED_AUDIENCE. Responses are marked no-store and rate-limited per workload identity. | MUST |
| [PRD-INT-13](../../requirements.md#req-prd-int-13) | GAP Machine-interface security: mutual TLS with certificates from the enterprise authority; tokens with audience, issuer, expiry ≤ 5 minutes and a key identifier resolved through a published key set; signed notifications use a detached JSON Web Signature with replay protection by notification identifier and a 5-minute clock-skew window; key rotation is supported without downtime. | MUST |
| [INT-06](../../requirements.md#req-int-06) | Listing uses opaque cursors. Unrestricted bulk exports are prohibited. | MUST |

## Exact PRD sections

- [21. Scope](../../prd/main-baseline.md#21-scope)
- [6.10 Readiness and handoff to assembly · ASM07-RDY](../../prd/technical-baseline.md#610-readiness-and-handoff-to-assembly--asm07-rdy)
- [7.1 Mandatory interface behaviours](../../prd/technical-baseline.md#71-mandatory-interface-behaviours)

## Behaviour to demonstrate

A valid human Admin token is rejected with REJECTED_AUDIENCE. A valid assembly token receives identifiers/languages/hashes, never stem, options, answers or asset bytes.

Failure checks: Try human credentials, wrong workload audience and expired tokens; deny access and verify response fields contain metadata only.

Existing issue acceptance criteria, retained for review:

- [ ] mTLS + audience-restricted workload token
- [ ] Payload: question id, type, classification, difficulty, Bloom, marks, languages, sealed version hashes, readiness status
- [ ] Never content
- [ ] Conformance test for token audience

## Dependencies and decisions

Required producer work: [#41](issue-41.md) (KKT), [#80](issue-80.md) (Kaustav).

R3’s assembly separation is settled. Sealed references need an agreed safe representation; they must not grant plaintext retrieval.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
