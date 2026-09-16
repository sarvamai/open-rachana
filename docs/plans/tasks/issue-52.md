# #52: As an engineer, I want CI to run platform pytest so a green PR is evidence

Owner proposed in the delivery plan: **Rohit**. Technical review: KKT; feature owners.
Epic: [#107](https://github.com/Bodhan-AI/open-rachana/issues/107). [Module route](../testing.md).

Replace placeholder Python CI with actual tests and preserve the aggregate ci gate.

## Start here

PR #96 implements real Python CI; #93 also touches the same setup.

First deliverable: Continue #96; coordinate with #93’s overlapping CI changes. Prove a deliberate test failure in disposable validation work before merging the correct version.

## Inputs and outputs

- Input: SPI/core packages and dev dependencies, test command, existing security/web jobs and PR #96.
- Output: A CI job that runs the Python suite and fails on an assertion, alongside the unchanged required aggregate result.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ARC-12](../../requirements.md#req-arc-12) | No component, dependency, endpoint, deployment artefact or runtime configuration provides AI capability. | MUST |
| [ASR02-OBS-17](../../requirements.md#req-asr02-obs-17) | OBS-16 is enforced by an automated test that fails the build — not by reviewer discipline. | MUST |
| [PRD-ARC-13](../../requirements.md#req-prd-arc-13) | GAP D-38 Scope of ARC-12 after the decision: it binds Layer 1 (every zone in §10.1). Layer 2 is the only place a model runs. The connector is a client of Layer 2 with these properties: outbound only; requests carry curriculum references and parameters, never sealed content; responses are treated as untrusted input and pass sanitization, validation and the human gates; Layer 2 holds no credential for any Layer 1 store or endpoint; the AI-dependency scan (§13.2) fails the build if a model runtime or inference client appears in any Layer 1 artefact. | MUST |

## Exact PRD sections

- [13.1 Levels](../../prd/technical-baseline.md#131-levels)
- [13.2 Mandated automated suites](../../prd/technical-baseline.md#132-mandated-automated-suites)

## Behaviour to demonstrate

A Python test failure must make ci fail even when web, Gitleaks and Trivy pass. Do not count an echo command as a test.

Failure checks: Run a deliberately failing platform assertion in a disposable validation branch and retain the failed result; restore the assertion before merging.

Existing issue acceptance criteria, retained for review:

- [ ] `build-and-test` in `.github/workflows/ci.yml` runs pytest over `platform/spi` and `platform/core`
- [ ] A failing `test_audit_chain.py` assertion fails CI
- [ ] Draft PRs still skip, same as sibling jobs
- [ ] AGENTS.md no longer says Python tests are local-only

## Dependencies and decisions

No upstream feature is required to prepare the first deliverable.

No product approval is needed to execute existing tests. Agree dependency pinning and test scope with KKT; do not disable failing security jobs.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
