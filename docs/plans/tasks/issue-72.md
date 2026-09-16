# #72: As an Integrity Operator, I want a live board of sessions, scores, and events with no content

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Build the content-free Integrity Operator surface and reconnecting live session feed.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Connect a synthetic snapshot/event stream, test reconnect recovery, then integrate #50’s authenticated durable service.

## Inputs and outputs

- Input: Authorised operator, session snapshots, ordered integrity events, score/referral state and last received event ID.
- Output: Active-session list, event feed, drill-down, persistent referral alert, distinct critical feedback and reconnect/backoff state.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR02-OBS-11](../../requirements.md#req-asr02-obs-11) | The operator surface shows all active sessions with role, subject, artefact state, integrity score and time since last heartbeat. | MUST |
| [ASR02-OBS-12](../../requirements.md#req-asr02-obs-12) | A rolling feed presents newest-first events across all sessions, with severity and pseudonymous actor identifier. | MUST |
| [ASR02-OBS-13](../../requirements.md#req-asr02-obs-13) | A per-session drill-down shows the full ordered event history and score progression. | MUST |
| [ASR02-OBS-14](../../requirements.md#req-asr02-obs-14) | The surface updates by server push, not manual reload, and displays a reconnecting state with backoff on transport loss. | MUST |
| [ASR02-OBS-15](../../requirements.md#req-asr02-obs-15) | On reconnect the surface re-synchronizes session state, so no live session is missing or stale. | MUST |
| [ASR02-OBS-18](../../requirements.md#req-asr02-obs-18) | The operator role can reach no artefact content through any interface. | MUST |
| [PRD-OBS-26](../../requirements.md#req-prd-obs-26) | GAP Operator surface transport: a server-push channel (server-sent events or a web socket) carrying session snapshots and events; reconnection with exponential backoff from 1 second to a 30-second cap with jitter; on reconnect the client sends its last event identifier and the server replies with a full session snapshot plus every missed event. Signal to surface p95 ≤ 3 seconds; signal to durable audit p95 ≤ 5 seconds. | MUST |
| [PRD-OBS-27](../../requirements.md#req-prd-obs-27) | GAP The operator's authorization scope contains no content endpoint at all; the operator API's response schemas are tested for the absence of content field names, and the operator UI is served without the editor or renderer bundles. | MUST |
| [UI-11](../../requirements.md#req-ui-11) | Operator — live sessions, event feed, per-session drill-down, alert banner, connection state. Distinct visual treatment for the operational context. | MUST |

## Exact PRD sections

- [18. Session Monitoring](../../prd/main-baseline.md#18-session-monitoring)
- [6.14 Session integrity, observability and referral · ASR02-OBS](../../prd/technical-baseline.md#614-session-integrity-observability-and-referral--asr02-obs)
- [9.2 Screen requirements](../../prd/technical-baseline.md#92-screen-requirements)

## Behaviour to demonstrate

Disconnect after event E and reconnect: receive a full current snapshot and missed events without hiding an active session or duplicating alerts.

Failure checks: Exercise invalid session access and referral events under the approved scoring policy; confirm the operator payload never carries question content.

Existing issue acceptance criteria, retained for review:

- [ ] Live sessions list with score and recent events
- [ ] Signals include (where the client can see them): copy/cut/paste/context menu, print/screenshot chords, devtools, focus loss, tab switch, concurrent tabs, heartbeat gaps
- [ ] At score ≤ 50 the session is referred: operator alert + security event; auto-suspend remains off
- [ ] Screen has no stem, options, or other question body
- [ ] Admin may hold this screen in the pilot

## Dependencies and decisions

Required producer work: [#42](issue-42.md) (Kaustav), [#50](issue-50.md) (Kaustav).

D-03/D-04/D-22 determine operational policy. UI must not expose suspend powers merely because a score crossed a proposed threshold.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
