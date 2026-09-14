# Plan: Phase 1 leftovers: Makefile, canonicalization spec, as-built page

Primary package: [Platform, identity and integration](../platform.md). Proposed owner: **KKT**.
Technical reviewers: Gandharva; Rohit for recovery evidence.
Issue: #94. Companion reference: PR #100; contributor workflow: PR #99.

Draft plan: owner review and implementation go-ahead are pending. Follow the
[review and readability workflow](../README.md) before implementation.

## Outcome and boundary

Implement the existing story within the package boundary below. Retain its acceptance criteria and record any approved amendments explicitly.

Own verified identities, reproducible environments, organisation-contracted managed-service bindings, release recovery and integration. The adopting organisation may contract any provider(s) meeting the interfaces and controls; no named host is mandatory. The IdP identifies the actor; workflow determines their task permissions.

Expected locations: `deployment/configuration, identity adapters, contracts and integration pipeline`. Confirm actual paths before editing.

## Dependencies

No implementation prerequisite; the plan can be reviewed now.

Dependencies order implementation, not permission to draft a plan. Use agreed
fixtures while a producer is under construction; real integration is still required.

## Work sequence

1. Inspect the current code and in-flight PRs; agree the input/output and refusal contract with the named reviewers.
2. Implement one reviewable slice with its relevant allowed, refused and interrupted-operation examples.
3. Integrate it into the shared flow and retain the result, configuration and remaining limits.

## Acceptance criteria

- [ ] `make test` and `make lint` run the real gates from a clean shell
- [ ] `docs/canonicalization.md` matches `audit/chain.py` exactly (worked example computed, not invented); root `AGENTS.md` no longer lists it as absent
- [ ] `docs/as-built.md` exists with as-is + target diagrams and the gap table; linked from README and `docs/AGENTS.md`

## Failure or boundary proof

Check PR #93 first. Verify merged commands and canonical bytes against actual code; add only missing work and do not close on overlapping documentation alone.

## Requirement trace

See the existing issue and the reference requirement register.

## Decisions and amendments to check

- Check open PR #93 before starting. It already proposes extraction, CI, deployment helpers and canonicalisation/as-built work; reuse accepted results and fill remaining gaps rather than duplicate it.

## Evidence required to close

Link the accepted plan revision, implementation PR/commit, actual test or manual
procedure, dated result/environment and reviewer sign-off. Record remaining
limitations. A mock, generated test, screenshot or checked box alone is not
acceptance. Product/security/accessibility signatures remain with their owners.
