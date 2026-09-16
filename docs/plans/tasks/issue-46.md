# #46: As the System, I want every state change written to a persisted hash-chained audit log in the same transaction

Owner proposed in the delivery plan: **Gandharva**. Technical review: Kaustav; Security for key/retention controls.
Epic: [#104](https://github.com/Bodhan-AI/open-rachana/issues/104). [Module route](../evidence.md).

Persist the audit chain and make required workflow writes atomic with their evidence and outbox entries.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Retain current draft-v0.1 fixtures; implement a persistent append/rollback test and a concurrency test against the selected store.

## Inputs and outputs

- Input: Trusted actor/workload context, approved event schema, action-specific safe details, subject hash, policy version and correlation identifier.
- Output: Append-only ordered event, chain head and transactional outbox record committed with the domain change; failure aborts the domain transaction.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR01-EVD-01](../../requirements.md#req-asr01-evd-01) | Every material action emits an append-only audit event: actor or service, action, subject and hash, outcome, policy version and correlation identifier. | MUST |
| [ASR01-EVD-07](../../requirements.md#req-asr01-evd-07) | Critical transitions fail closed when durable audit is unavailable. | MUST |
| [PRD-EVD-11](../../requirements.md#req-prd-evd-11) | GAP Audit event schema (§8.2, Appendix C): event identifier; chain identifier; sequence number; occurred at; actor (type user or service; audit identifier or workload identity); action from the catalogue; subject (type, identifier, version hash where applicable); outcome (success, denied, failed); policy version; correlation and trace identifiers; details as a structured object whose keys are allowlisted per action; previous hash; event hash. The schema forbids additional properties. | MUST |
| [PRD-EVD-12](../../requirements.md#req-prd-evd-12) | GAP Action catalogue (minimum): session.signed_in, session.denied, session.signed_out, session.timed_out, cycle.created, cycle.changed, taxonomy.published, taxonomy.node_retired, capability.created, capability.revoked, capability.expired, assignment.created, assignment.released, assignment.expired, assignment.reassigned, artefact.created, draft.saved (aggregated per minute, count only), asset.uploaded, asset.quarantined, asset.rejected, asset.cleared, draft.withdrawn, version.submitted, validation.failed, review.opened, review.decided, accessibility.decided, translation_review.decided, exception.requested, exception.approved, exception.revoked, exception.expired, exception.consumed, sealing.started, sealing.failed, version.sealed, variant.created, readiness.changed, correction.authorized, correction.seeded, artefact.superseded, supersession.acknowledged, supersession.overdue, artefact.retired, artefact.used, artefact.archived, key.rotated, policy.denied, security.event, integrity.signal, integrity.referred, chain.checkpoint, chain.verified, evidence.sweep, breakglass.accessed. | MUST |
| [PRD-EVD-13](../../requirements.md#req-prd-evd-13) | GAP D-02 Chain construction: the event body (every field except event_hash) is serialized with the canonical JSON rule of §8.4; event_hash = SHA-256 of the previous hash concatenated with the body bytes. The genesis record has sequence 0, a previous hash of 32 zero bytes, and carries chain identifier, creation time, schema version and environment; it is signed through the key service. Sequence numbers are strictly increasing and unique by database constraint; a single writer per chain takes a row lock on the chain head. Every 10,000 events or every hour, whichever is first, a checkpoint records the sequence and head hash, signed through the key service, and is exported to the monitoring platform as an external anchor so a store-wide rewrite is detectable. | MUST |
| [PRD-EVD-15](../../requirements.md#req-prd-evd-15) | GAP Throughput: the chain writer must sustain at least 200 events per second, because telemetry signals are mirrored into the chain (§6.14) at up to 100 per second across 50 sessions. This is measured in Week 1 before any feature is built on it. | MUST |
| [INT-10](../../requirements.md#req-int-10) | Domain events are published for creation, submission, review decision, accessibility decision, readiness change, sealing, supersession and policy denial. Events defined must have a producer. | MUST |
| [DAT-05](../../requirements.md#req-dat-05) | Canonicalization is specified once — Unicode normalization, whitespace, attribute order, option order, numeric representation and asset-hash inclusion — and is bit-stable across repeat serialization and restore. Every hash depends on it. | MUST |
| [DAT-06](../../requirements.md#req-dat-06) | The canonical schema is versioned, and a stated migration approach preserves verifiability of already-sealed artefacts. | MUST |
| [ARC-02](../../requirements.md#req-arc-02) | Every state-changing operation and its audit record commit in the same database transaction. | MUST |
| [ARC-03](../../requirements.md#req-arc-03) | Domain and audit events are delivered from a transactional outbox after commit, at least once, with consumer-side deduplication by event identifier. | MUST |

## Exact PRD sections

- [19. Evidence and Audit](../../prd/main-baseline.md#19-evidence-and-audit)
- [6.13 Expected evidence and audit · ASR01-EVD](../../prd/technical-baseline.md#613-expected-evidence-and-audit--asr01-evd)
- [8.4 Canonicalization rule v1](../../prd/technical-baseline.md#84-canonicalization-rule-v1)
- [8.5 Similarity fingerprint](../../prd/technical-baseline.md#85-similarity-fingerprint)

## Behaviour to demonstrate

Kill the transaction after inserting the domain row but before audit insertion: neither survives. Concurrent appends keep unique contiguous sequence numbers and a verifiable head.

Failure checks: Crash between attempted state and event writes: both commit or neither. Verify a persisted event matches the approved byte fixtures.

Existing issue acceptance criteria, retained for review:

- [ ] DB-backed store produces byte-identical events to `AuditEvent` in `platform/core/.../audit/chain.py`
- [ ] `verify()` results match the in-memory log (`test_audit_chain.py` stays the oracle)
- [ ] Payload is hashed and discarded; events carry opaque refs only
- [ ] A crashed mid-write leaves both state+event or neither
- [ ] `docs/canonicalization.md` exists (referenced by chain.py, missing on disk today)

## Dependencies and decisions

Required producer work: [#51](issue-51.md) (KKT).

R6 and D-01/D-02 block adoption of new canonical bytes/checkpoint policy. Store choice is an engineering proposal; cross-store atomicity cannot be assumed.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
