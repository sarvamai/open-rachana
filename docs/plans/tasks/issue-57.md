# #57: As Security, I want the translation-draft model channel off until the model runs inside our boundary

Owner proposed in the delivery plan: **Sarvam team — individual lead to be confirmed**. Technical review: Kaustav; Security for translation hosting.
Epic: [#109](https://github.com/Bodhan-AI/open-rachana/issues/109). [Module route](../intelligence.md).

Keep the translation-draft AI channel disabled until its data-handling and hosting approval is recorded.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement the off-by-default control and an integration test showing no primary text is sent while approval is absent.

## Inputs and outputs

- Input: Channel configuration, Security approval record, private service binding and task-scoped primary-reference release contract.
- Output: A disabled-channel refusal by default, or a governed proposal returned into the ordinary translation workflow; manual translation remains available.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ARC-14](../../requirements.md#req-prd-arc-14) | GAP D-48 Translation drafts require the primary reference text to reach Layer 2. This is permitted only when Layer 2 runs inside the trust boundary (a private deployment with no data retention and no training on inputs) or when Security accepts a documented exception with the same guarantees contractually. Until then the translation-draft channel of the connector stays disabled and translators start from an empty variant. | MUST |

## Exact PRD sections

- [11. Translation](../../prd/main-baseline.md#11-translation)
- [1.5 Two-layer architecture at a glance](../../prd/technical-baseline.md#15-two-layer-architecture-at-a-glance)
- [10.2 Architecture requirements](../../prd/technical-baseline.md#102-architecture-requirements)

## Behaviour to demonstrate

Setting a boolean in a request cannot activate translation AI. An empty manual language draft still opens while the AI service is disabled.

Failure checks: Prove the channel stays off without the recorded approval; manual translation still works and toggling configuration cannot bypass the approval gate.

Existing issue acceptance criteria, retained for review:

- [ ] Translation-draft generation path is disabled by default
- [ ] Enabling it requires a recorded Security + Technical Lead decision that the model is inside the boundary, no retention, no training
- [ ] Until then, translators write by hand (translation stories still apply)

## Dependencies and decisions

Required producer work: [#40](issue-40.md) (Nikhil).

D-48 and R8 block actual primary-text release. Private hosting/no-retention/no-training guarantees require named approval; no general vault credential goes to Layer 2.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
