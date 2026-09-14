# ADR-0013: Generation configuration belongs to Rachana; final paper assembly is separate

- Status: Accepted
- Deciders: Product Owner, in the repository-alignment review
- Date: 2026-09-14

## Context

Main PRD §§3, 6 and 7 include curriculum-grounded generation driven by
blueprints and candidate counts. Main §21 and annex §2.3 also exclude
blueprint logic and assembly. Without a boundary, contributors could either
omit required generation configuration or build paper assembly into the
question-authoring workflow. The web app already contains mock blueprint and
exam-paper surfaces, which are not proof of accepted product scope.

## Decision

The Product Owner confirmed: “Yes—confirm this boundary.”

- Curriculum, generation constraints and candidate counts belong to Rachana.
  Generation accepts the required count and candidate multiplier and creates
  independent candidates with provenance (PRD-ATH-25/26, D-38).
- Selecting, ordering and exporting the final paper belong to a separate
  assembly module (main non-goals; D-39/D-40 scope recommendations).
- Rachana hands off FULLY_APPROVED metadata, languages and hashes through the
  machine-only readiness interface (ASM07-RDY). It supplies no routine human
  sealed-content read or paper-export interface.
- Existing mock exam-paper surfaces do not alter that boundary. Their future
  module ownership and packaging must be recorded before API integration.

## Rationale

Generation needs a defined mix and number of candidates. Assembly makes a
different decision about which approved questions form a final paper and in
which order. The distinction preserves the PRD's required generation flow
and metadata-only selection boundary without expanding authoring permissions.

## Alternatives considered

- **Exclude all blueprint configuration.** Simpler authoring scope, but loses
  the PRD's generation constraints and count × multiplier request.
- **Combine generation and final paper assembly in Rachana's workflow.**
  Convenient to demonstrate in one UI, but mixes final selection/export with
  authoring and contradicts the stated separate-assembly boundary.

## Consequences

- Generation configuration remains on the Rachana delivery plan; Layer 2's
  owner and complete integration schedule still need to be named (R2).
- The separate assembly module owns paper selection/order/export and its
  release-custody controls. This decision does not choose its repository,
  deployment or owner, or approve any content-release path.
- UI mocks must be labelled and routed according to this boundary when
  connected to APIs. Shared presentation components do not merge authority.
- The conflicting Google Doc shorthand should be corrected separately;
  [source-of-truth.md](../source-of-truth.md) records this later decision.
