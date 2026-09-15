# ADR-0013: Soft delete — withdraw or retire, never permanent

- Status: Accepted
- Deciders: Product owner
- Date: 2026-09-14

## Context

PRD section 20, D-41.  The audit chain is append-only and hash-chained
(invariant 3).  Permanently removing a question record would leave an
unverifiable gap in the chain.

## Decision

Nothing is permanently deleted.  "Delete" means **withdraw** for drafts and
**retire** for approved items.

- **Withdraw:** applies to questions in `DRAFT` state.  The question leaves
  authoring workflows; its audit trail stays intact.
- **Retire:** applies to questions that have been approved or sealed.  The
  question leaves active use; its full history is preserved.

Both are one-way transitions.

## Consequences

- The lifecycle state machine gains `WITHDRAWN` and `RETIRED` as terminal
  states.
- The database never issues `DELETE FROM` on question records.  Storage SPIs
  must honour this.
- The audit chain records withdrawal and retirement as ordinary state
  transitions.
- UI surfaces label the action "Withdraw" or "Retire", never "Delete".
