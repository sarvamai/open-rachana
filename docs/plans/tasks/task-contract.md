# #117: Publish versioned task and identity contracts for parallel implementation

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Publish the versioned identity, task, decision and error contracts consumed across modules.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Freeze the minimum draft/create/save/submit and review-task contracts with Divyansh, Kaustav and Gandharva; keep other endpoints additive.

## Inputs and outputs

- Input: PRD field definitions and sample payloads, current endpoints, assigned-task permission rules and producer/consumer needs.
- Output: Machine-readable schemas and synthetic allowed/denied/stale/retried examples, with explicit versions and consumer contract tests.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INT-01](../../requirements.md#req-int-01) | All interfaces are versioned and published as a machine-readable definition kept current with the implementation. | MUST |
| [INT-03](../../requirements.md#req-int-03) | Retryable mutations accept an idempotency key and are safe to repeat. | MUST |
| [INT-05](../../requirements.md#req-int-05) | Errors return a stable machine-readable code, a safe message, a correlation identifier, field-level detail and retry ability — never echoing Restricted content. | MUST |
| [INT-06](../../requirements.md#req-int-06) | Listing uses opaque cursors. Unrestricted bulk exports are prohibited. | MUST |
| [INT-07](../../requirements.md#req-int-07) | Timestamps are UTC and identifiers are opaque. | MUST |
| [INT-08](../../requirements.md#req-int-08) | Rate limits vary by user, workload identity, endpoint sensitivity and source zone. | MUST |
| [PRD-INT-11](../../requirements.md#req-prd-int-11) | GAP Conventions: JSON request and response bodies; base path /api/v1 for interactive surfaces, /assembly/v1, /downstream/v1, /telemetry/v1, /operator/v1 and /evidence/v1 for their audiences; identifiers are ULIDs; timestamps are RFC 3339 in UTC; idempotency key in the Idempotency-Key header for every POST that creates or transitions, retained 24 hours; concurrency token via ETag and If-Match on drafts; cursor pagination returns items and next_cursor with a maximum page size of 200; every response carries Cache-Control: no-store and the correlation identifier. | MUST |
| [PRD-INT-12](../../requirements.md#req-prd-int-12) | GAP Rate-limit classes (INT-08): interactive content endpoints 60 requests per minute per user; autosave 30 per minute per draft; telemetry 600 events per minute per session; assembly readiness 600 per minute per workload identity; downstream notifications 60 per minute; sign-in 10 per minute per source. Limits are configuration; exceeding one returns RATE_LIMITED with a retry-after value. | MUST |
| [PRD-INT-13](../../requirements.md#req-prd-int-13) | GAP Machine-interface security: mutual TLS with certificates from the enterprise authority; tokens with audience, issuer, expiry ≤ 5 minutes and a key identifier resolved through a published key set; signed notifications use a detached JSON Web Signature with replay protection by notification identifier and a 5-minute clock-skew window; key rotation is supported without downtime. | MUST |
| [PRD-INT-14](../../requirements.md#req-prd-int-14) | GAP Content responses (draft, version, render, asset) are authorized per request with a short-lived scope and are non-cacheable (DAT-04); asset bytes are served through an authorized endpoint with a 60-second signed reference, never a stable public URL. | MUST |
| [ARC-01](../../requirements.md#req-arc-01) | Authorization is evaluated server-side on every request using role, assignment, version, language, lifecycle state, cycle policy, recognized capability and separation of duties. Client-supplied role claims are never trusted. | MUST |
| [PRD-ATH-15](../../requirements.md#req-prd-ath-15) | GAP Content model of a version: stem; ordered options, each with a structural identifier, a body and a correct flag; explanation; classification (subject, unit, topic, difficulty as proposed by the author, taxonomy level); marks; assets with checksum, alternative text and decorative flag. Stem, option bodies and explanation are restricted-HTML documents in which equations are inline equation nodes holding canonical LaTeX and images are asset references. | MUST |
| [PRD-REV-15](../../requirements.md#req-prd-rev-15) | GAP Decision record fields: identifier; version identifier and version hash; decision type (review, translation review, accessibility); outcome; checklist responses; attestations with sources; reason code; comments; difficulty assigned; equivalence judgement; reviewer audit identifier; capability entry identifier valid at the time; renderer version; policy version; opened at; decided at; duration; correlation identifier. The record's own hash is written into the audit event. | MUST |
| [PRD-ASG-02](../../requirements.md#req-prd-asg-02) | GAP Assignment record: identifier, task type, user audit identifier, subject reference (version, lineage or artefact), cycle, language, created at, expires at, status (Active, Completed, Released, Expired, Reassigned), release reason, policy version used. Assignments are append-only; reassignment closes one and opens another. | MUST |
| [PRD-EVD-11](../../requirements.md#req-prd-evd-11) | GAP Audit event schema (§8.2, Appendix C): event identifier; chain identifier; sequence number; occurred at; actor (type user or service; audit identifier or workload identity); action from the catalogue; subject (type, identifier, version hash where applicable); outcome (success, denied, failed); policy version; correlation and trace identifiers; details as a structured object whose keys are allowlisted per action; previous hash; event hash. The schema forbids additional properties. | MUST |

## Exact PRD sections

- [7.1 Mandatory interface behaviours](../../prd/technical-baseline.md#71-mandatory-interface-behaviours)
- [8.2 Entities and required fields](../../prd/technical-baseline.md#82-entities-and-required-fields)
- [16. Reviewer Isolation](../../prd/main-baseline.md#16-reviewer-isolation)

## Behaviour to demonstrate

A consumer cannot parse forbidden source-context or author fields because the review schema never includes them. Stale draft writes return the agreed stable error envelope.

Existing issue acceptance criteria, retained for review:

- [ ] Machine-readable schemas and synthetic examples are checked in.
- [ ] Producer and consumer contract tests agree, including stale and wrong-role requests.
- [ ] Schema and migration ownership are explicit; incompatible changes require reviewed versioning.

## Dependencies and decisions

Required producer work: [#40](issue-40.md) (Nikhil).

R4/R5/R8 affect specific role/render/reference contracts. Publish unaffected fields now and mark the exact unresolved fields; do not block every interface.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
