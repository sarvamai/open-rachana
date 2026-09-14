# Working in this repository

Layer 1 workflow core for Project Rachana. The product includes Layer 2
drafting through a governed connector, backed by Layer 3 managed services.
The repository documentation is the maintained reference: read
`docs/source-of-truth.md`, `docs/product-workflow.md`, `docs/delivery-plan.md`
and `docs/prd-reconciliation.md` before product-facing changes.
Admin authors → question review → accessibility remediation + review →
primary seal → translation + review + accessibility per language → seals → ready.
Python/FastAPI in `platform/`, Next.js in `apps/web`, a Tauri thin
client in `apps/client/`.

## The docs plan M6; the tree is at M0

`docs/` describes targets for the three-week sprint ending 28 September 2026.
M0–M6 are dependency/evidence gates, not calendar weeks. **The tree is the fact; the doc is the intent.** `docs/delivery-status.md`
records inspected code/test definitions and their limits. Before importing a
path you read in a doc, check it exists:

```bash
ls providers db contracts tests/conformance platform.yaml 2>&1
```

Every one of those is absent today. If a task needs one, create it explicitly
and say so — don't code as if it were already there.
Only the KMS interface, conformance suite and test double exist; no reference
provider is delivered. `docs/canonicalization.md` now records the existing
draft-v0.1 format and the unratified PRD v1 proposal. It changes no bytes.

## Invariants (`docs/architecture.md` has all ten)

1. The server state machine is authoritative — never trust a client claim,
   including this repo's own React server components.
2. A state change and its audit event commit in one transaction.
3. Audit events are append-only, hash-chained, **content-free** — opaque refs
   and a payload hash, never plaintext.
4. No human seal control exists. Never add a path that seals, unseals, or
   reads sealed plaintext, for any routine role, administrators included.
   PRD translation references, correction seeding and emergency access need
   separately decided contracts (R8); this alignment authorises no read path.
5. No AI in the core. Models only *propose* via the `gateway` SPI; a human
   submits before review. The existing ADR's adoption-before-draft rule and
   the PRD's generated-draft transition are unresolved in R4; do not implement
   a choice silently. AI never validates, approves, seals or monitors.
6. Validation is deterministic — nothing probabilistic or external on a
   validation path.

Daily consequence: **no question content in logs, audit events, exception
strings, or URLs.**

## Commands

```bash
# Python (3.12+)
uv pip install -e platform/spi -e "platform/core[dev]"
python -m pytest platform/spi platform/core -q
python -m ruff check platform

# Web
cd apps/web && pnpm install && pnpm dev
```

`core_api` reads bindings from `platform.yaml` (`$MULYANKAN_PLATFORM_CONFIG`).
No such file is committed; with none, the app starts with zero bindings.

**CI's gate is the aggregate `ci` job** over `semgrep`, `gitleaks`, `trivy`,
`web` and `build-and-test`. The org-wide `shift-left-security` call is not
used here: this repository is public and `sarvamai/security-redirect` is
private, and GitHub does not let a public repository call a reusable workflow
that lives in a private one. `ci.yml` carries the call, commented out, and
says what restoring it needs. `build-and-test` is
still the template's `echo` placeholder, so the Python tests are local-only —
a green PR proves nothing about them. `Dockerfile` is likewise a placeholder.
`ruff` is unconfigured and unpinned (`>=0.6`); it reports findings in
pre-existing `platform/` code, so check `git stash`-clean output before
blaming your change.

Separately, commenting `/review` on a PR runs the `sarvam-code` reviewer
(`.github/workflows/pr-review.yml`, prompt and plumbing in `.github/review/`).
It is a reviewer, not a gate — its `Automated Code Review` status is not
required. Its prompt inlines the invariants above by lifting the
`## Invariants` section from this file and two sections from
`apps/web/AGENTS.md`, matched by heading text in
`.github/review/scripts/lib/cheat-sheet.js`: if you rename one of those
headings, update that file in the same PR or the reviewer silently falls back
to a shorter summary.

## Conventions

- Decisions become ADRs in `docs/adr/`. Amend in place with a dated note; see
  ADR-0001. Never leave a decision only in a PR description.
- Requirement-facing tests carry the requirement ID:
  `test_asrevd02_chain_verifies_after_appends`. IDs live in
  `docs/traceability.md` and `docs/requirements.md`. New work cites canonical
  PRD IDs (ASM/INS); existing QST/FND names remain valid through the crosswalk.
  Planned check labels in the register are not existing or passing tests.
- `git commit -s` (DCO). One concern per PR.
- British spelling in prose (`licence`, `artefact`).

## Open questions — ask, don't pick

- **R1 is decided; contracts remain to build.** On 2026-09-14 the Product
  Owner chose Admin authoring/unsealed-content work in the signed client and
  configuration/content-free oversight in the web UI. ADR-0008 records the
  amendment. The client scaffold serves no role until its contracts are
  authored; session, capability and re-authentication mechanics still need review.
- **Generation and rendering (R2/R4/R5).** Full Layer 2 ownership, proposal
  adoption and the server/reference versus signed-local render contract
  require decisions. R3 is decided in ADR-0012: curriculum, generation
  constraints/counts are in Rachana; final paper selection/order/export are
  in separate assembly.
  Use the concrete proposals in `docs/prd-reconciliation.md` to ask owners;
  do independent work while these remain open.
- Pilot languages are deliberately unnamed (ADR-0006) — still pending for the
  platform. `apps/web` now carries a working list for its question language
  field (`apps/web/src/components/question-bank/languages.ts`: the Eighth
  Schedule's twenty-two plus English, at the repo owner's direction). It is one
  array in the client, standing in for `cycle.required_languages` until there
  is an API to read; the ADR's own status is unchanged, and nothing in
  `platform/` names a language.
- Canonicalization is `draft-v0.1`; `docs/canonicalization.md` documents it.
  PRD v1 is pending D-01/R6. Changing the byte format changes every audit hash.

## Keeping this file true

Update it in the same PR when you: create one of the absent paths above, add a
CI job, change a documented command, add or move a nested `AGENTS.md`, or
settle an open question. Nested `AGENTS.md` files own their own trees
(`platform/` and its packages, `apps/web/`, `design-system/`, `docs/`) — put
tree-specific rules in the deepest one that fits, not here. A stale line is
worse than no line: it is read as fact.
