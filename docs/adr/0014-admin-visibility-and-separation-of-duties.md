# ADR-0014: Admin visibility and separation of duties

- Status: Accepted
- Deciders: Product owner
- Date: 2026-09-14

## Context

PRD section 20, D-42 and D-46.  Two constraints on the Admin role need to be
settled before the capability matrix (issue #42) is built:

1. Admins need full question visibility to manage the authoring pipeline, but
   invariant 6 says sealed plaintext is unreadable by any human role.  The
   boundary has to be explicit.
2. The person who manages content must not be the person who approves or
   rejects it.  Admins manage people and configuration; they do not act as
   reviewers.

## Decision

- **Before sealing:** Admins may view all questions, including body content,
  in every pre-seal state: `DRAFT`, `IN_REVIEW`, `APPROVED`,
  `IN_ACCESSIBILITY`, and `IN_TRANSLATION`.
- **After sealing:** Admins see metadata only (ID, version, state,
  timestamps, audit trail).  Sealed plaintext is inaccessible (invariant 6).
- **Approve and reject:** The permission matrix carries an explicit **deny**
  for Admin on `approve` and `reject`.  This is not the absence of a grant —
  it is an affirmative denial that cannot be overridden by any other role the
  same user holds.

## Consequences

- The capability matrix (issue #42) has a `deny` row for Admin on `approve`
  and `reject`.
- The RBAC layer distinguishes "not granted" from "explicitly denied".
- Tests cover: Admin reads a pre-seal question (200), Admin reads sealed body
  (403), Admin approves (403), Admin rejects (403).  Test names carry SEC and
  DAT requirement IDs.
- The Integrity Operator view (ASR02-OBS-01) is unaffected — it is already
  content-free.
