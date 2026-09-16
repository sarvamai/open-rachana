# #50: As the System, I want content sessions to heartbeat and the first monitoring signal to reach the audit in seconds

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Complete authenticated, durable session-integrity ingestion and server-side scoring around the existing session scaffold.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Add ownership checks to the current session endpoints, then durable ingest/retry with duplicate and out-of-order fixtures.

## Inputs and outputs

- Input: Actor/session ownership, heartbeat, event identifier, client sequence, task reference, event type, blocked flag and policy version.
- Output: Persist-before-ack event ingestion, deduplication, ordered score history, referral updates and content-free operator stream.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR02-OBS-01](../../requirements.md#req-asr02-obs-01) | Every authoring, review, accessibility and translation session is registered, heartbeated, and closed on sign-out or timeout. | MUST |
| [ASR02-OBS-05](../../requirements.md#req-asr02-obs-05) | Ingest failure retries; events are never silently discarded. Durability outranks latency. | MUST |
| [ASR02-OBS-06](../../requirements.md#req-asr02-obs-06) | Each session carries an integrity score starting at 100, decremented per signal by a ratified severity table, floored at 0, and non-recovering within a session. | MUST |
| [ASR02-OBS-07](../../requirements.md#req-asr02-obs-07) | Signals are classified at least as warning or critical; critical signals are visually and audibly distinct. | MUST |
| [ASR02-OBS-08](../../requirements.md#req-asr02-obs-08) | Crossing the configured threshold refers the session — a security event to the monitoring platform and a persistent alert to the operator. | MUST |
| [ASR02-OBS-09](../../requirements.md#req-asr02-obs-09) | Repeat breaches update the existing alert rather than stacking duplicates. | MUST |
| [ASR02-OBS-10](../../requirements.md#req-asr02-obs-10) | Automatic session suspension defaults to off. Enabling it is an explicit operational decision, not a build default. | MUST |
| [ASR02-OBS-16](../../requirements.md#req-asr02-obs-16) | A monitoring event carries only event type, timestamp, session identifier, pseudonymous actor audit identifier and task reference. No stem, option, field value, clipboard payload or screenshot. | MUST |
| [PRD-OBS-19](../../requirements.md#req-prd-obs-19) | GAP Session record: session identifier; actor audit identifier; role; current task reference (assignment identifier, opaque); started at; last heartbeat at; ended at with reason (sign-out, inactivity, absolute maximum, suspension, revocation); integrity score; signal counts by kind; referred flag and alert identifier. The client heartbeats every 30 seconds; a session is flagged stale at 90 seconds without one (§11). | MUST |
| [PRD-OBS-20](../../requirements.md#req-prd-obs-20) | GAP D-03 The signal catalogue below, with proposed default severities and decrements, is the ratified severity table once signed by the Integrity Operator and Security. It is configuration with a version recorded on every integrity event. | MUST |
| [PRD-OBS-23](../../requirements.md#req-prd-obs-23) | GAP D-33 Ingest: the client queues events in memory with client sequence numbers and posts batches of at most 50 to the telemetry endpoint; the server persists before acknowledging by event identifier; unacknowledged events retry with exponential backoff and jitter without ever blocking input; ordering is restored server-side by client sequence. Capacity: 50 sessions at 2 events per second sustained, bursts to 10 per second per session. | MUST |
| [PRD-OBS-24](../../requirements.md#req-prd-obs-24) | GAP Scoring is computed server-side on ingest: score = max(0, 100 − sum of decrements), never recovering within the session; each event stores the score after it; duplicate event identifiers are ignored. | MUST |
| [PRD-OBS-25](../../requirements.md#req-prd-obs-25) | GAP D-04 Referral: when the score first reaches or falls below the threshold (proposed 50), the system sends a security event to the monitoring platform carrying session identifier, actor audit identifier, score and the counts of the top signals, and creates one persistent alert on the operator surface. Every later signal in that session updates the same alert. Automatic suspension, when enabled by configuration D-22, ends the session, releases its assignment with reason and records both; it is off by default. | MUST |
| [PRD-OBS-21](../../requirements.md#req-prd-obs-21) | GAP Telemetry event schema (Appendix C): event identifier, event type, severity, occurred at, session identifier, actor audit identifier, task reference, client sequence number, blocked flag, score after. The JSON schema forbids additional properties, and the build-failing test (OBS-17) submits events carrying content-like fields and asserts they are rejected, then inspects every persisted and forwarded event for the absence of any string from the synthetic corpus. | MUST |

## Exact PRD sections

- [18. Session Monitoring](../../prd/main-baseline.md#18-session-monitoring)
- [6.14 Session integrity, observability and referral · ASR02-OBS](../../prd/technical-baseline.md#614-session-integrity-observability-and-referral--asr02-obs)

## Behaviour to demonstrate

Drop the acknowledgement after persistence: retrying the same event must not deduct the score twice. A different user cannot post to a guessed session ID.

Failure checks: Attempt another actor’s session writes, forged session identity, duplicate/out-of-order signals and temporary ingest failure; prove durable recovery.

Existing issue acceptance criteria, retained for review:

- [ ] Session register, 30-second heartbeat, close — platform concern, not the IdP
- [ ] One published signal implemented (copy/cut/paste or heartbeat gap)
- [ ] Signal writes a content-free audit event (action, session id, score) within seconds
- [ ] Score starts at 100, subtracts a fixed published amount, never recovers in-session
- [ ] Automatic suspension stays off

## Dependencies and decisions

Required producer work: [#41](issue-41.md) (KKT), [#46](issue-46.md) (Gandharva).

D-03/D-04/D-22/D-33 set scoring/referral/suspension/batch policy. Diagnostic OTel export is not the durable integrity channel; automatic suspension stays off unless approved.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
