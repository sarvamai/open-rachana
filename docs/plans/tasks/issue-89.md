# #89: As Product Owner, I want every acceptance criterion signed in one evidence pack and go-live recorded

Owner proposed in the delivery plan: **Nikhil**. Technical review: KKT for technical steps; Rohit for testability.
Epic: [#108](https://github.com/Bodhan-AI/open-rachana/issues/108). [Module route](../product.md).

Assemble release acceptance and handover evidence across every required product and operational obligation.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Trace one complete synthetic primary/translation journey from requirement through commit/test/evidence/sign-off, then audit the entire coverage index.

## Inputs and outputs

- Input: Requirement-to-task coverage, merged implementations, actual checks, decision records, expert findings, restore results and named acceptance owners.
- Output: A release evidence index with accepted, failed and pending obligations; runbooks, support owners and explicit limitations.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASR01-EVD-04](../../requirements.md#req-asr01-evd-04) | Verification succeeds across backup and restore — restored records retain valid event and content hashes. | MUST |
| [SEC-13](../../requirements.md#req-sec-13) | Backups are encrypted, access-separated, immutable, and restoration is tested. | MUST |
| [UI-13](../../requirements.md#req-ui-13) | Every input is labelled; keyboard operation and screen-reader semantics are preserved throughout. | MUST |

## Exact PRD sections

- [13.5 Evidence pack](../../prd/technical-baseline.md#135-evidence-pack)
- [17. Definition of Done and release criteria](../../prd/technical-baseline.md#17-definition-of-done-and-release-criteria)

## Behaviour to demonstrate

A checked issue with no retained result remains unaccepted. Missing Security, accessibility or retention approval stays a release blocker rather than an assumed default.

Failure checks: Trace every required criterion to its implementation and retained result; missing signatures or evidence block closeout and do not become implicit defaults.

Existing issue acceptance criteria, retained for review:

- [ ] Each Week 1–5 'done when' maps to a test, log, or signed artefact
- [ ] `docs/traceability.md` has a component and test for every in-scope requirement
- [ ] Open questions recorded with defaults: rejected-version visibility (findings only); author may correct own approved item (yes); closed cycle never reopens (no); accommodation 'needs equivalent route' flags, does not block (no); only assembly acks a correction; difficulty change is an override with both values stored
- [ ] Go-live decision recorded as an ADR or signed minute

## Dependencies and decisions

Required producer work: [#86](issue-86.md) (Rohit), [#87](issue-87.md) (Divyansh), [#88](issue-88.md) (KKT).

The 28 September target does not waive prerequisites. Reference maintenance and adopter-contracted operations have separate owners.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
