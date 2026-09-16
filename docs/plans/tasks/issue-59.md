# #59: As an Admin, I want to add images and limited LaTeX to a question

Owner proposed in the delivery plan: **Divyansh**. Technical review: Kaustav; Accessibility lead for relevant checks.
Epic: [#102](https://github.com/Bodhan-AI/open-rachana/issues/102). [Module route](../client.md).

Implement safe image and equation handling from upload through rendering and validation.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement quarantine-to-cleared image fixtures, then attach-by-reference and malicious/oversized/equation-boundary cases.

## Inputs and outputs

- Input: Permitted image bytes, alt/decorative metadata, checksums, bounded LaTeX and approved HTML rules.
- Output: Only cleared, re-encoded, stripped assets become usable; rejected assets have safe findings; equations use the shared accessible rendering contract.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [ASM03-ATH-08](../../requirements.md#req-asm03-ath-08) | Images are supported in stem, options and explanation. Every meaningful image requires alternative text; decorative images require an explicit flag. | MUST |
| [ASM03-ATH-09](../../requirements.md#req-asm03-ath-09) | Equations are stored as canonical LaTeX and rendered to an accessible representation. | MUST |
| [PRD-ATH-16](../../requirements.md#req-prd-ath-16) | GAP D-09 Restricted-HTML allowlist (SEC-10). Elements: p, br, strong, em, u, s, sub, sup, ul, ol, li, table, caption, thead, tbody, tr, th, td, img, span, eq. Attributes: th[scope], td&#124;th[colspan&#124;rowspan ≤ 8], img[src (asset: scheme only), alt, data-decorative], ol[start], span[dir, lang], eq[data-latex]. No hyperlinks, no style attributes, no event handlers, no comments, no scripts, no external URL scheme of any kind. Sanitization removes anything else and reports each removal to the author as a warning; the sanitized form is what is validated, previewed and stored. | MUST |
| [PRD-ATH-17](../../requirements.md#req-prd-ath-17) | GAP D-10 Permitted LaTeX subset (SEC-10): arithmetic and relations; \frac, \sqrt[n]{}, superscript and subscript; Greek letters; \sin \cos \tan \log \ln \exp \lim \sum \prod \int with limits; \left \right with round, square and brace delimiters and vertical bars; \vec \hat \bar \overline \dot; \text{}; pmatrix, bmatrix and cases up to 6 × 6; aligned up to 6 lines; the operator symbols \cdot \times \div \pm \mp \le \ge \ne \approx \equiv \infty \to \in \notin \subset \subseteq \cup \cap \forall \exists \partial \nabla \degree \angle \perp \parallel; spacing commands. Prohibited: any macro definition (\def, \newcommand, \let), file or catcode commands, \href \url, colour commands, raw HTML. Bounds: 2,000 characters, nesting depth 12, 200 ms render budget per equation. Anything outside is rejected with a bounded-subset message and no unbounded rendering work is performed. | MUST |
| [ARC-04](../../requirements.md#req-arc-04) | Uploaded assets are unusable until they pass quarantine, validation, malware scanning, re-encoding and metadata stripping. | MUST |
| [SEC-09](../../requirements.md#req-sec-09) | Uploads are quarantined and only released after format allowlisting, signature inspection, malware scanning, re-encoding, metadata removal and decompression limits. | MUST |
| [SEC-10](../../requirements.md#req-sec-10) | Restricted-HTML sanitization uses an explicitly defined allowlist of tags, attributes and URL schemes. The permitted LaTeX subset is likewise defined and bounded. | MUST |
| [ASM03-ATH-04](../../requirements.md#req-asm03-ath-04) | Content supports sanitized restricted HTML, full Unicode, sub- and superscript, lists, accessible tables, and canonical LaTeX rendered through the shared reference renderer. | MUST |
| [ASM03-ATH-07](../../requirements.md#req-asm03-ath-07) | Preview uses the same rendering contract as review, accessibility check and downstream delivery. | MUST |
| [PRD-ATH-14](../../requirements.md#req-prd-ath-14) | GAP D-11 Proposed field limits, measured on text after markup is stripped: stem ≤ 4,000 characters; each option ≤ 1,000; explanation ≤ 6,000; alternative text 3 – 300 characters; at most 6 images per version; each image ≤ 2 MB and ≤ 4,000 × 4,000 pixels; total asset budget ≤ 8 MB per version. Limits are configuration with these defaults and are enforced server-side with field-level errors. | MUST |

## Exact PRD sections

- [8. Authoring](../../prd/main-baseline.md#8-authoring)
- [6.4 Authoring · ASM03-ATH](../../prd/technical-baseline.md#64-authoring--asm03-ath)
- [10.5 Asset pipeline](../../prd/technical-baseline.md#105-asset-pipeline)

## Behaviour to demonstrate

A renamed executable is rejected after signature inspection. A meaningful image without alt text blocks submission; decorative status must be explicit.

Failure checks: Try malicious/failed-scan images and unsupported equation markup; reject attachment before it becomes usable and keep required alternative text.

Existing issue acceptance criteria, retained for review:

- [ ] Images are quarantined, scanned, and re-encoded before use
- [ ] Meaningful images require alternative text; decorative can be marked later by accessibility
- [ ] Equations accept only the documented LaTeX subset
- [ ] Failed scan or illegal markup blocks attach and names the field

## Dependencies and decisions

Required producer work: [#53](issue-53.md) (Kaustav).

D-09/D-10/D-11 govern allowlists and limits; R5 governs renderer equivalence. These settings must be explicit, with proposed defaults labelled.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
