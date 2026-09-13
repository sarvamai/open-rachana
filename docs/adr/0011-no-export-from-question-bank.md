# ADR-0011: No export from the question bank

- Status: Accepted
- Deciders: Product owner
- Date: 2026-09-14

## Context

PRD section 20, D-39.  The question bank holds confidential examination
content.  Any path that lets a user download, print, copy, or export a
question body from the bank undermines sealing before it happens.  Paper
export — assembling selected questions into a printable paper — is a separate
pipeline with its own access controls, built in a later milestone.

## Decision

The question bank exposes no download, print, copy, or export path.  Paper
export belongs to the assembly pipeline and is out of scope here.

## Consequences

- No endpoint or UI element in the question bank returns body content as a
  downloadable artefact.  The block is enforced server-side (invariant 1),
  not by the client alone.
- The assembly pipeline gets its own ADR when that milestone starts.
- A conformance test fails CI if a question-bank endpoint serves body content
  with a download disposition.
