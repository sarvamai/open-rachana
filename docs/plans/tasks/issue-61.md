# #61: As an Admin, I want submit blocked until validation passes, with each finding naming the field

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Implement the complete deterministic validation catalogue and return stable field-specific findings.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Turn each catalogue rule into valid, invalid and boundary fixtures; invoke through a validation endpoint before submission wiring.

## Inputs and outputs

- Input: Draft, cycle/type configuration, taxonomy and asset status, sanitised content, renderer/rule-set versions and similarity result from #62.
- Output: Stored/returned validation report with code, severity, field path and safe message; validation itself makes no lifecycle transition.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [PRD-ATH-27](../../requirements.md#req-prd-ath-27) | GAP D-44 Question types: single-select multiple choice is fully supported. Other types the blueprint may name (for example short answer) are stored with the same content model minus options, and may enter the pipeline only when the cycle enables them; the validation and structural rule sets for such types are reduced accordingly and named per type. | SHOULD |
| [ASM03-VAL-01](../../requirements.md#req-asm03-val-01) | Validation is deterministic and rule-based only. It performs schema, answer, taxonomy, asset, equation, prohibited-markup, accessibility-completeness and within-artefact duplicate checks. | MUST |
| [ASM03-VAL-02](../../requirements.md#req-asm03-val-02) | Blocking findings prevent submission; each is reported against the specific field with actionable text. | MUST |
| [ASM03-VAL-03](../../requirements.md#req-asm03-val-03) | Validation causes no state change and calls no probabilistic or external inference service. | MUST |
| [PRD-VAL-07](../../requirements.md#req-prd-val-07) | GAP The validation rule catalogue below is the complete set for the MVP. Each rule has a stable code, a severity (blocking or warning), and reports the field path it applies to. The rule-set version is recorded with every validation report. | MUST |
| [PRD-VAL-08](../../requirements.md#req-prd-val-08) | GAP A validation report is returned to the client and stored with the submission as evidence: rule-set version, renderer version, and one entry per finding with code, severity, field path and message. Validation is a pure function of the draft and the configuration. | MUST |

## Exact PRD sections

- [8.3 Validation before submit](../../prd/main-baseline.md#83-validation-before-submit)
- [6.5 Validation and submission · ASM03-VAL](../../prd/technical-baseline.md#65-validation-and-submission--asm03-val)

## Behaviour to demonstrate

Duplicate options produce a finding on their fields. Running validation twice on unchanged input/configuration produces the same findings and no new version.

Failure checks: Provide one failing fixture per rule and boundary cases; no model calls occur and every blocking finding identifies its field.

Existing issue acceptance criteria, retained for review:

- [ ] Required fields present
- [ ] 2–8 unique options; exactly one correct
- [ ] Classification values exist in the current syllabus
- [ ] Images scanned clean; alt text present for meaningful images
- [ ] Equations inside the permitted subset; no prohibited markup
- [ ] Blocking findings stop submit and name the field
- [ ] Validation is deterministic — no model, no external probabilistic service

## Dependencies and decisions

Required producer work: [#44](issue-44.md) (Kaustav), [#59](issue-59.md) (Divyansh).

D-09/D-10/D-11 and D-44 configure rules; R5 affects rendering checks. Preserve catalogue codes and keep all model calls outside validation.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
