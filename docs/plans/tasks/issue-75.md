# Plan: As a Translation Reviewer, I want original and translation side by side so I can approve or reject

Primary package: [Workspaces and signed client](../client.md). Proposed owner: **Divyansh**.
Technical reviewers: Kaustav; Accessibility lead for relevant checks.
Issue: #75. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own task screens, accessible interaction, content-client restrictions and release packaging. Consume server permissions and task responses; never infer authorization from a hidden button.

Expected locations: `apps/client and the content-free configuration/oversight parts of apps/web`. Confirm actual paths before editing.

## Dependencies

#74, #68

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Side-by-side original and translation
- [ ] Comment, approve, reject — cannot edit
- [ ] Cannot review a translation they wrote
- [ ] Reject → translator corrects → a *new* Translation Reviewer is assigned
- [ ] Approve → accessibility for that language
- [ ] Reviewer confirms the translation is not easier and not harder than the original

## Failure or boundary proof

Attempt own-translation approval and editing via the review API; preserve rejection history and assign a different reviewer after correction.

## Requirement trace

QST04-TRN

## Decisions and amendments to check

- Resolve the signed-local/reference-rendering and per-OS acceptance contract (R5) before the dependent implementation; native and accessibility checks remain explicit.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
