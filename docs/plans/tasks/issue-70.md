# Plan: As an Accessibility Reviewer, I want to test the rendered question and decide

Primary package: [Workspaces and signed client](../client.md). Proposed owner: **Divyansh**.
Technical reviewers: Kaustav; Accessibility lead for relevant checks.
Issue: #70. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own task screens, accessible interaction, content-client restrictions and release packaging. Consume server permissions and task responses; never infer authorization from a hidden button.

Expected locations: `apps/client and the content-free configuration/oversight parts of apps/web`. Confirm actual paths before editing.

## Dependencies

#69, #68

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Can test rendered question with keyboard/SR workflow, record which declared accommodations it works under, comment, approve or reject
- [ ] Cannot edit
- [ ] Approve → sealing of this language version (seal story consumes the event)
- [ ] Reject with finding (element + fix): specialist corrects if it is an a11y field, Admin corrects if wording must change; a *new* Accessibility Reviewer is assigned
- [ ] Cannot act on a question they authored, remediated, or reviewed before

## Failure or boundary proof

Test the rendered task with keyboard and screen reader; reject self-review and route wording findings through a new author correction.

## Requirement trace

QST04-ACC · D-43

## Decisions and amendments to check

- Resolve the signed-local/reference-rendering and per-OS acceptance contract (R5) before the dependent implementation; native and accessibility checks remain explicit.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
