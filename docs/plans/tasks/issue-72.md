# Plan: As an Integrity Operator, I want a live board of sessions, scores, and events with no content

Primary package: [Workspaces and signed client](../client.md). Proposed owner: **Divyansh**.
Technical reviewers: Kaustav; Accessibility lead for relevant checks.
Issue: #72. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own task screens, accessible interaction, content-client restrictions and release packaging. Consume server permissions and task responses; never infer authorization from a hidden button.

Expected locations: `apps/client and the content-free configuration/oversight parts of apps/web`. Confirm actual paths before editing.

## Dependencies

#42, #50

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Live sessions list with score and recent events
- [ ] Signals include (where the client can see them): copy/cut/paste/context menu, print/screenshot chords, devtools, focus loss, tab switch, concurrent tabs, heartbeat gaps
- [ ] At score ≤ 50 the session is referred: operator alert + security event; auto-suspend remains off
- [ ] Screen has no stem, options, or other question body
- [ ] Admin may hold this screen in the pilot

## Failure or boundary proof

Exercise invalid session access and referral events under the approved scoring policy; confirm the operator payload never carries question content.

## Requirement trace

ASR02-OBS

## Decisions and amendments to check

- Heartbeat/scoring/referral values remain governed by the decision register. Existing numeric defaults are proposals until ratified; diagnostic Collector outage never excuses lost integrity evidence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
