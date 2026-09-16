# #94: Phase 1 leftovers: Makefile, canonicalization spec, as-built page

Owner proposed in the delivery plan: **KKT**. Technical review: Gandharva; Rohit for recovery evidence.
Epic: [#106](https://github.com/Bodhan-AI/open-rachana/issues/106). [Module route](../platform.md).

Keep commands, paths, byte-format descriptions and implementation status consistent with the merged repository.

## Start here

PR #93 owns recovery/canonicalisation cleanup; #96 owns the Python CI change.

First deliverable: Review #93’s Makefile and canonicalisation documents, then patch only statements inconsistent with the actual merged code.

## Inputs and outputs

- Input: Current main, PR #93’s recovery changes, #96 CI, #101 verification and #120/#121 observability evidence.
- Output: Accurate onboarding/AGENTS/as-built references with implemented and planned items distinguished; no duplicate recovery implementation.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [DAT-05](../../requirements.md#req-dat-05) | Canonicalization is specified once — Unicode normalization, whitespace, attribute order, option order, numeric representation and asset-hash inclusion — and is bit-stable across repeat serialization and restore. Every hash depends on it. | MUST |
| [DAT-06](../../requirements.md#req-dat-06) | The canonical schema is versioned, and a stated migration approach preserves verifiability of already-sealed artefacts. | MUST |

## Exact PRD sections

- [13.1 Levels](../../prd/technical-baseline.md#131-levels)
- [14.1 Week 1 — Foundation and evidence backbone](../../prd/technical-baseline.md#141-week-1--foundation-and-evidence-backbone)

## Behaviour to demonstrate

If Python CI is still an echo placeholder, documentation must say so. An unmerged provider directory must not be described as installed on main.

Failure checks: Check PR #93 first. Verify merged commands and canonical bytes against actual code; add only missing work and do not close on overlapping documentation alone.

Existing issue acceptance criteria, retained for review:

- [ ] `make test` and `make lint` run the real gates from a clean shell
- [ ] `docs/canonicalization.md` matches `audit/chain.py` exactly (worked example computed, not invented); root `AGENTS.md` no longer lists it as absent
- [ ] `docs/as-built.md` exists with as-is + target diagrams and the gap table; linked from README and `docs/AGENTS.md`

## Dependencies and decisions

No upstream feature is required to prepare the first deliverable.

R6 is a format decision, not a documentation tidy-up. Do not change byte semantics to make prose look consistent.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
