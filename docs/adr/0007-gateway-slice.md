# ADR-0007: Gateway slice in the MVP — proposals only, thin

- Status: Accepted for the original connector slice. PRD alignment note
  added 2026-09-14; broader product scope and adoption transition require
  the decisions below before implementation.
- Date: 2026-09-07

## Context

The architecture concept note amends v4 with: a Proposal entity carrying
provenance (model id, version, adapter version, material hash,
prompt-template hash, timestamp), a content-free gateway audit event enforced
by a build-failing test, and the rule that a model removed from the approved
list is refused on the next call. Layer 2 models themselves are out of scope
for Layer 1.

## Decision

Build the thin slice in M4:

- the `gateway` SPI with the provenance envelope schema in `mulyankan-spi`;
- the content-free gateway audit event, enforced by a build-failing test
  (the OBS-17 pattern);
- one reference adapter, `providers/gateway-openai-compat/` (any
  OpenAI-compatible endpoint), used for the demonstration.

Proposals are stored Restricted (DAT-01), never exported, and become drafts
only through explicit human adoption (QST03-ATH-13 extended). No validation,
review, accessibility, sealing, or readiness code path may call the gateway —
enforced by an architecture test that fails the build.

## Consequences

- The demonstration can show the full arc: model proposes → human checks →
  sealed → ready.
- Removing a model from the approved list is a configuration change; the next
  call is refused by the registry rule in ADR-0003.
- Vendors integrate by implementing the gateway SPI and passing its
  conformance suite, never by forking the core.

## PRD alignment note — 2026-09-14

The text above records the original decision. The supplied Rachana PRD
v1.3 D-38 explicitly includes Layer 2 candidate generation, translation drafts
and metadata in the MVP/demo, while preserving an AI-free Layer 1. The thin
gateway remains useful but does not by itself satisfy that product scope.

Two unresolved items are now explicit in [PRD reconciliation](../prd-reconciliation.md):
The current target is 28 September 2026 (see [delivery plan](../delivery-plan.md)).
R2 still requires a named Layer 2 delivery owner, service boundary and interim dates;
R4 reconciles this ADR's human-adoption-before-draft rule with PRD-ATH-25's
validated generated DRAFTs. No decision changing that transition is recorded
here. Implementation must wait for the responsible owners to settle it.

D-48 separately keeps translation drafting off until Security approves its
hosting and handling of the primary reference text. A generic
OpenAI-compatible demonstration endpoint is not that approval. No AI is
allowed in validation, similarity, human decision gates, sealing, readiness
or monitoring. Consequence: connector, Layer 2 delivery and translation
hosting each need their own acceptance evidence.
