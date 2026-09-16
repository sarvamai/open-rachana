# #77: As the System, I want to seal a language version after accessibility approval with no human button

Owner proposed in the delivery plan: **Gandharva**. Technical review: Kaustav; Security for key/retention controls.
Epic: [#104](https://github.com/Bodhan-AI/open-rachana/issues/104). [Module route](../evidence.md).

Seal a fully evidenced version through the dedicated worker and protected KMS/object-store interfaces.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement one synthetic seal with provider doubles, then crash/retry checkpoints against real reference services. Document the database/object-store commit and recovery protocol.

## Inputs and outputs

- Input: Version and accepted byte profile, approvals/duty checks, cleared assets, policy/evidence records, retention period and worker identity.
- Output: Encrypted immutable object, signed Restricted manifest, safe metadata index/current pointer and content-free receipt; working plaintext/caches removed after committed success.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM05-VLT-01](../../requirements.md#req-asm05-vlt-01) | Sealing is a system action. No human role has a discretionary publish control. | MUST |
| [ASM05-VLT-02](../../requirements.md#req-asm05-vlt-02) | The service revalidates approvals, lineage, separation of duties, asset scans, schema and current policy before any write. | MUST |
| [ASM05-VLT-03](../../requirements.md#req-asm05-vlt-03) | Canonical sealing strips comments, author names, revision history, unsafe attributes, source metadata and any field outside the approved schema. | MUST |
| [ASM05-VLT-04](../../requirements.md#req-asm05-vlt-04) | The service produces a SHA-256-or-stronger content hash, encrypts using managed keys, and signs a manifest without persisting raw key material. | MUST |
| [ASM05-VLT-05](../../requirements.md#req-asm05-vlt-05) | On sealing, the artefact is removed from the authoring, review and accessibility environments and indexed in the question bank by classification, complexity level, difficulty and taxonomy level. | MUST |
| [ASM05-VLT-06](../../requirements.md#req-asm05-vlt-06) | Sealing atomically writes the artefact, indexes approved metadata, emits durable audit, and ends routine human access. | MUST |
| [ASM05-VLT-07](../../requirements.md#req-asm05-vlt-07) | Sealing is idempotent and safely retryable. A failure leaves no partially sealed artefact. | MUST |
| [PRD-VLT-09](../../requirements.md#req-prd-vlt-09) | GAP The sealing pipeline runs the steps below, in order, in a worker under the sealing workload identity (ARC-05), keyed by the version identifier as its idempotency key. | MUST |
| [PRD-VLT-10](../../requirements.md#req-prd-vlt-10) | GAP Manifest content is specified in §8.6. A manifest is Restricted (DAT-01), stored beside the sealed object and in the database, and its canonical bytes are signed with an asymmetric key held in the key management service. | MUST |
| [PRD-VLT-11](../../requirements.md#req-prd-vlt-11) | GAP Encryption model: envelope encryption with a fresh 256-bit data key per sealed version (authenticated encryption), the data key wrapped by the active repository-tier key in the key management service. Key policy grants encrypt to the sealing identity only; decrypt to the verification identity (in-memory verification only, no plaintext output), the correction-seeding identity under a recorded authorization (§6.11), and the break-glass identity (§10.6). No human principal and no platform-administrator role holds decrypt. Every key use is logged by the key service and mirrored into audit. | MUST |
| [PRD-VLT-12](../../requirements.md#req-prd-vlt-12) | GAP Storage: a private object store with no public access, object versioning, retention lock with the period taken from configuration D-24 (DAT-08), provider-side encryption in addition to application-level encryption, and access only through worker identities. Object key: artefact identifier / version identifier / content hash. | MUST |
| [PRD-VLT-13](../../requirements.md#req-prd-vlt-13) | GAP Bank index row per sealed version: artefact and version identifiers, language, lineage, classification, complexity level, difficulty, taxonomy level, marks, content hash, similarity fingerprint, sealed at, current flag, accommodations deliverable. No content field exists in the index. | MUST |
| [PRD-VLT-14](../../requirements.md#req-prd-vlt-14) | GAP Post-seal removal (VLT-05): in the sealing transaction the plaintext working copy of the sealed version is deleted from the authoring-tier store and its rendering caches are purged. Returned and Withdrawn versions are not sealed; they remain immutable in the authoring tier, reachable only as findings context by the author of the successor draft and as metadata by auditors. | MUST |
| [PRD-VLT-15](../../requirements.md#req-prd-vlt-15) | GAP Current-version resolution (VLT-08): the artefact holds one current sealed version pointer per language; the pointer moves and the previous version becomes Superseded inside the same transaction, so a reader never observes two current versions or none. | MUST |
| [PRD-VLT-16](../../requirements.md#req-prd-vlt-16) | GAP Failure handling: if the key service, audit store, scanner or object store is unavailable, or any revalidation fails, the job is marked failed with a reason code, no state changes, retry uses exponential backoff up to 6 hours, an operational alert fires after the third failure, and operations can replay the job. Because the object key includes the content hash, a retry after a partial object write overwrites the same key and produces exactly one sealed object and one manifest. | MUST |
| [PRD-VLT-17](../../requirements.md#req-prd-vlt-17) | GAP Progress: the version shows Queued, Sealing, Sealed or Failed (retrying) to the accessibility specialist who approved it and to the coordinator; 95 % of valid image-bearing artefacts seal within 30 seconds (§11). | MUST |
| [DAT-07](../../requirements.md#req-dat-07) | Artefacts are encrypted in storage and in transit. | MUST |
| [DAT-08](../../requirements.md#req-dat-08) | Retention locks are implemented with the period as configuration. No default period is invented. | MUST |
| [ARC-05](../../requirements.md#req-arc-05) | The sealing worker runs under its own workload identity and is the only component permitted to write sealed artefacts and manifests. | MUST |
| [ARC-09](../../requirements.md#req-arc-09) | Asynchronous jobs are idempotent, expose pending, succeeded and failed state, and support safe replay. | MUST |
| [DAT-05](../../requirements.md#req-dat-05) | Canonicalization is specified once — Unicode normalization, whitespace, attribute order, option order, numeric representation and asset-hash inclusion — and is bit-stable across repeat serialization and restore. Every hash depends on it. | MUST |
| [DAT-06](../../requirements.md#req-dat-06) | The canonical schema is versioned, and a stated migration approach preserves verifiability of already-sealed artefacts. | MUST |
| [ASR01-EVD-05](../../requirements.md#req-asr01-evd-05) | Each step declares the evidence it must produce. Before sealing, the system asserts that every expected record exists, verifies against the exact version hash, and was produced by an actor with no separation-of-duties conflict. | MUST |
| [ASR01-EVD-07](../../requirements.md#req-asr01-evd-07) | Critical transitions fail closed when durable audit is unavailable. | MUST |
| [PRD-TRN-11](../../requirements.md#req-prd-trn-11) | GAP Variant creation is part of the primary's sealing transaction. For each required language a new lineage and Draft are created with: empty target-language stem, option bodies, explanation and alternative text; locked fields copied from the primary (option identifiers and order, correct flag, marks, assets by checksum, canonical equations, classification); primary_reference_hash; and a read-only primary reference snapshot holding the primary's rendering and canonical text, classified Restricted and visible only to the assigned translator and translation reviewer. A translation assignment is created by policy. The snapshot is purged when the variant is sealed. | MUST |

## Exact PRD sections

- [12. Sealing and the Vault](../../prd/main-baseline.md#12-sealing-and-the-vault)
- [6.9 Sealing and the repository · ASM05-VLT](../../prd/technical-baseline.md#69-sealing-and-the-repository--asm05-vlt)
- [8.4 Canonicalization rule v1](../../prd/technical-baseline.md#84-canonicalization-rule-v1)
- [8.6 Manifest format](../../prd/technical-baseline.md#86-manifest-format)

## Behaviour to demonstrate

Interrupt after object upload but before final database commit: replay reconciles the same operation without a second successful seal. Missing retention configuration refuses sealing.

Failure checks: Fail keys/storage and interrupt the job after an external write; retry safely with no half-sealed success, human seal button or missing evidence.

Existing issue acceptance criteria, retained for review:

- [ ] No person has a seal or publish control
- [ ] Worker re-checks every approval and every expected record; missing anything stops and alerts
- [ ] Canonicalize → SHA-256 → encrypt with managed keys → signed manifest (hashes, approvals, policy versions) → vault → metadata index → delete working copy → audit
- [ ] KMS/storage behind existing SPI (`mulyankan_spi.kms`)

## Dependencies and decisions

Required producer work: [#70](issue-70.md) (Divyansh), [#71](issue-71.md) (Kaustav), [#46](issue-46.md) (Gandharva).

R6/D-01 bytes, D-24 retention and R8 controlled-reference handling are hard dependencies for live seals. Storage atomicity and immutable-lock retries need a reviewed design, not an assumed cross-service transaction.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
