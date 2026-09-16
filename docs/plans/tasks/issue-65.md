# Plan: As a Question Reviewer, I want to see only my assigned question and the allowed metadata

Primary package: [Workspaces and signed client](../client.md). Proposed owner: **Divyansh**.
Technical reviewers: Kaustav; Accessibility lead for relevant checks.
Issue: #65. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own task screens, accessible interaction, content-client restrictions and release packaging. Consume server permissions and task responses; never infer authorization from a hidden button.

Expected locations: `apps/client and the content-free configuration/oversight parts of apps/web`. Confirm actual paths before editing.

## Dependencies

#63, #67

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] Visible: rendered question; subject, grade, curriculum name, chapter, page range; type, marks, Bloom, difficulty, language; validation warnings
- [ ] Not visible and not inferable: assessment name/title/id, final question number, other questions, candidate pool membership, other reviewers, author identity, stored source-context text, audit history
- [ ] Question ID is not a paper number and exposes no assessment context
- [ ] API tests try the forbidden fields and fail if they appear

## Failure or boundary proof

Inspect serialized API payloads and attempt forbidden IDs/fields; CSS hiding is not an isolation check.

## Requirement trace

QST03-REV · isolation

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
