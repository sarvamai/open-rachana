# #54: As an Admin, I want to upload a curriculum PDF

Owner proposed in the delivery plan: **Sarvam team — individual lead to be confirmed**. Technical review: Kaustav; Security for translation hosting.
Epic: [#109](https://github.com/Bodhan-AI/open-rachana/issues/109). [Module route](../intelligence.md).

Ingest curriculum through quarantine, extraction and provenance records for generation.

## Start here

PR #93 contains source/extraction recovery and provider code; it is unmerged.

First deliverable: Inspect #93’s source/extraction code and continue its contract. Test a valid synthetic PDF plus rejected format, scan failure and text-poor input.

## Inputs and outputs

- Input: Admin upload, file bytes/type/checksum, curriculum metadata and a bounded extraction request.
- Output: Quarantined/failed/ready source status, extracted chapter/page references and restricted source context, with no source text in diagnostics.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ARC-04](../../requirements.md#req-arc-04) | Uploaded assets are unusable until they pass quarantine, validation, malware scanning, re-encoding and metadata stripping. | MUST |
| [PRD-ATH-25](../../requirements.md#req-prd-ath-25) | GAP D-38 Generated candidates: a generation request by the Admin (curriculum, cycle, question type, marks, required count × candidate multiplier) produces independent artefacts, each with one DRAFT of provenance generated, owned by the requesting Admin. Every generated draft records generation identifier, model identifier, generation configuration, source curriculum, chapter, page range, stored source context, and timestamp. A generated draft that fails the automated validation catalogue (§6.5) is discarded before any human sees it. Generated drafts are never grouped as alternatives of one question. The generation service runs outside the hardened zones and never receives content from the pipeline. | MUST |
| [PRD-ATH-26](../../requirements.md#req-prd-ath-26) | GAP Metadata (engineering PRD §9.2): in addition to classification, a version carries grade, curriculum reference, learning objective, competency, question type, language, source curriculum, chapter, page range and source context, status, version number, created and updated timestamps, and — where generated — generation identifier, model and configuration. Source context text is Restricted and is never shown to reviewers (D-47). | MUST |

## Exact PRD sections

- [6. Core Concepts](../../prd/main-baseline.md#6-core-concepts)
- [7. Question Generation (Layer 2)](../../prd/main-baseline.md#7-question-generation-layer-2)
- [1.5 Two-layer architecture at a glance](../../prd/technical-baseline.md#15-two-layer-architecture-at-a-glance)
- [10.5 Asset pipeline](../../prd/technical-baseline.md#105-asset-pipeline)

## Behaviour to demonstrate

A PDF that has not cleared scanning cannot supply generation context. An extraction failure retains an actionable status without logging its text.

Failure checks: Try a malformed, oversized, scanned-failed and text-poor PDF; preserve quarantine/provenance and prevent source text from reaching logs.

Existing issue acceptance criteria, retained for review:

- [ ] Admin uploads a PDF (example: NCERT Class 8 Science) and it is stored as reference material
- [ ] Upload is quarantined, scanned, and re-encoded before use
- [ ] Audit event records the upload (no file bytes in the event)
- [ ] Reviewers never see the stored source-context text later

## Dependencies and decisions

Required producer work: [#41](issue-41.md) (KKT), [#51](issue-51.md) (KKT).

R2 requires the named Layer 2 service and integration owner. Schema/adapters can be developed with fixtures; production source/content rights remain the adopter’s responsibility.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
