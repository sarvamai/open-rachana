# #88: As Ops, I want load, backup/restore, and chain verification passed in production

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Measure performance and prove encrypted backup/restore against the PRD’s non-functional targets.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Build a reproducible load profile and restore one synthetic sealed lineage plus its audit chain into an isolated environment.

## Inputs and outputs

- Input: Specified workload/corpus, deployment configuration, backups/keys, target table in technical §11 and chain/manifests from the running system.
- Output: Measured latency/throughput and RTO/RPO, verified restored hashes/current pointers and incident/recovery evidence.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR01-EVD-04](../../requirements.md#req-asr01-evd-04) | Verification succeeds across backup and restore — restored records retain valid event and content hashes. | MUST |
| [SEC-13](../../requirements.md#req-sec-13) | Backups are encrypted, access-separated, immutable, and restoration is tested. | MUST |
| [PRD-EVD-15](../../requirements.md#req-prd-evd-15) | GAP Throughput: the chain writer must sustain at least 200 events per second, because telemetry signals are mirrored into the chain (§6.14) at up to 100 per second across 50 sessions. This is measured in Week 1 before any feature is built on it. | MUST |
| [PRD-OBS-26](../../requirements.md#req-prd-obs-26) | GAP Operator surface transport: a server-push channel (server-sent events or a web socket) carrying session snapshots and events; reconnection with exponential backoff from 1 second to a 30-second cap with jitter; on reconnect the client sends its last event identifier and the server replies with a full session snapshot plus every missed event. Signal to surface p95 ≤ 3 seconds; signal to durable audit p95 ≤ 5 seconds. | MUST |
| [PRD-VLT-17](../../requirements.md#req-prd-vlt-17) | GAP Progress: the version shows Queued, Sealing, Sealed or Failed (retrying) to the accessibility specialist who approved it and to the coordinator; 95 % of valid image-bearing artefacts seal within 30 seconds (§11). | MUST |

## Exact PRD sections

- [11. Non-functional requirements](../../prd/technical-baseline.md#11-non-functional-requirements)
- [13.5 Evidence pack](../../prd/technical-baseline.md#135-evidence-pack)
- [14.5 Week 5 — Harden, install, qualify](../../prd/technical-baseline.md#145-week-5--harden-install-qualify)

## Behaviour to demonstrate

A restore that opens the database but loses an acknowledged audit event fails. Report observed recovery time and data loss against the source targets.

Failure checks: Measure against the stated limits, restore an encrypted backup and verify audit/manifests. Record actual RTO/RPO and failures, not estimated values.

Existing issue acceptance criteria, retained for review:

- [ ] Load evidence at 50 concurrent sessions with the published ceilings
- [ ] Backup + restore leaves audit hashes intact and `verify()` green
- [ ] Retention period for sealed questions is recorded before any production seal (D-24)

## Dependencies and decisions

Required producer work: [#85](issue-85.md) (KKT), [#77](issue-77.md) (Gandharva), [#47](issue-47.md) (Gandharva).

Production capacity and recovery acceptance need Operations/Security. Do not invent a retention period or replace measurements with projections.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
