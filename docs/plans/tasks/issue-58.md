# Plan: As an Admin, I want to write and edit a single-select MCQ in the tool

Primary package: [Workspaces and signed client](../client.md). Proposed owner: **Divyansh**.
Technical reviewers: Kaustav; Accessibility lead for relevant checks.
Issue: #58. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own task screens, accessible interaction, content-client restrictions and release packaging. Consume server permissions and task responses; never infer authorization from a hidden button.

Expected locations: `apps/client and the content-free configuration/oversight parts of apps/web`. Confirm actual paths before editing.

## Dependencies

#53, #44

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Editor supports stem, 2–8 options, exactly one correct, explanation, marks, subject/unit/topic/difficulty/Bloom
- [ ] Other question types are rejected unless the cycle enables them (D-44)
- [ ] Reference material, glossary, symbol and equation palettes are inside the tool
- [ ] No links out of the tool
- [ ] Autosave every 15 seconds and on leaving a field

## Failure or boundary proof

Try invalid option counts, multiple correct answers, stale autosaves and failed network saves; prevent editing a submitted version and retain accessible error states.

## Requirement trace

QST03-ATH

## Decisions and amendments to check

- The Admin content client/web split is recorded in the reference PR. A separate Author role and automatic draft creation versus explicit adoption remain R4; do not settle them by coding an old issue sentence.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
