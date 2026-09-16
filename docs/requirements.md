# PRD requirement register

Baseline: [source and precedence](source-of-truth.md), retrieved 14 September 2026.
This register contains **302 unique IDs: 178 inherited + 124 PRD additions**.
There are 304 source rows: UI-02 and UI-03 each occur in two sections. Both
wordings are retained below. This is requirement coverage, not completion.

The Requirement column preserves the source wording, including GAP and D-nn
qualifiers. It does not ratify proposed defaults. Read it with the
[workflow](product-workflow.md) and [reconciliation items](prd-reconciliation.md)
where the source contradicts itself. ARC-12 is qualified by the decided D-38
and PRD-ARC-13. Role and state names follow the main PRD and annex §2.7.

M0–M6 are dependency/evidence gates under the [delivery plan](delivery-plan.md),
whose current target is 28 September 2026. Any Week-n wording preserved in
original rows is historical: satisfy the underlying dependency before the
related gate closes, not according to a competing calendar.

Each section supplies its proposed component, milestone, verification owner
and verification approach. These are planning assignments to roles, not
appointments of people. Every row has a distinct **planned check label**;
these labels are not existing test functions or passing tests. Implementers
must replace/link them with actual tests or manual procedures and retained
results before closure. Manual expert checks remain necessary even if a
row's automated check passes.

Status: `Unverified` means no requirement-level acceptance evidence was mapped
in this documentation review; it does not assert no related code exists.
`Partial` means relevant code/test definitions exist, with the limitations in
[delivery status](delivery-status.md). No requirement is marked accepted.
Existing evidence references E1/E2 identify inspected test definitions, not
a test run. For closure, add commit, result location, run date and owner sign-off.

## 6.1 — Cycle and taxonomy

Source: Detailed Spec §6.1. Planned component: Configuration services; admin configuration surface.

Target: M1. Verification owners: Content Operations; QA.

Verification: Create a valid versioned cycle and taxonomy; reject absent, invalid, revoked or stale configuration; retain the policy version used.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm01-cfg-01"></a>ASM01-CFG-01<br>v4: QST01-CFG-01 | A coordinator can configure a cycle: code, title, primary language, required languages, syllabus version, permitted item types, marking-policy reference, declared accommodations, and status. | MUST | `check_asm01_cfg_01` | Unverified / — |
| <a id="req-asm01-cfg-02"></a>ASM01-CFG-02<br>v4: QST01-CFG-02 | Artefacts can be created only within an active, valid cycle. | MUST | `check_asm01_cfg_02` | Unverified / — |
| <a id="req-asm01-cfg-03"></a>ASM01-CFG-03<br>v4: QST01-CFG-03 | A taxonomy administrator manages versioned Subject → Unit → Topic hierarchies plus controlled difficulty and taxonomy-level vocabularies. | MUST | `check_asm01_cfg_03` | Unverified / — |
| <a id="req-asm01-cfg-04"></a>ASM01-CFG-04<br>v4: QST01-CFG-04 | Taxonomy values in use can be retired for future selection but never deleted. Historical versions retain their original references. | MUST | `check_asm01_cfg_04` | Unverified / — |
| <a id="req-asm01-cfg-05"></a>ASM01-CFG-05<br>v4: QST01-CFG-05 | Cycle and taxonomy configuration have working interfaces — nothing can be authored until both exist. | MUST | `check_asm01_cfg_05` | Unverified / — |
| <a id="req-prd-cfg-06"></a>PRD-CFG-06 | GAP The cycle record carries, in addition to CFG-01: author cap per cycle; required review count (1 or 2) D-06; whether reviewers see the correct answer D-06; remediation-repeats-review policy D-07; assignment expiry per task type D-12; similarity threshold D-08; default marks per item from the marking policy; a monotonically increasing policy_version that increments on every change. | MUST | `check_prd_cfg_06` | Unverified / — |
| <a id="req-prd-cfg-07"></a>PRD-CFG-07 | GAP Cycle status is one of Draft (editable, nothing can be authored), Active (drafts may be created) and Closed (no new drafts; in-flight tasks, sealing and readiness continue). Changing required languages or syllabus version on an Active cycle requires re-authentication, increments the policy version and emits policy.changed; existing versions keep their recorded references. A cycle is never deleted. | MUST | `check_prd_cfg_07` | Unverified / — |
| <a id="req-prd-cfg-08"></a>PRD-CFG-08 | GAP A taxonomy version is an immutable published tree once referenced by a cycle. Node identifiers are stable across versions. Nodes carry active_from and retired_at. A new version may retire nodes; retirement is a date, never a deletion, so every historical reference resolves. | MUST | `check_prd_cfg_08` | Unverified / — |
| <a id="req-prd-cfg-09"></a>PRD-CFG-09 | GAP Controlled vocabularies are versioned lists managed by the taxonomy administrator: difficulty, taxonomy level, complexity level (used by bank indexing), item type, declared accommodation. Proposed initial values are in D-17 and D-18. Values are retired, never deleted. | MUST | `check_prd_cfg_09` | Unverified / — |
| <a id="req-prd-cfg-10"></a>PRD-CFG-10 | GAP Every decision, submission and seal records the cycle policy_version, taxonomy version and vocabulary versions in force at that moment, so the evidence pack can reproduce the rules that applied. | MUST | `check_prd_cfg_10` | Unverified / — |
| <a id="req-prd-cfg-11"></a>PRD-CFG-11 | GAP A cycle may have an empty list of required languages (single-language cycle). Readiness then requires only the sealed primary. | MUST | `check_prd_cfg_11` | Unverified / — |

## 6.2 — Identity and capability

Source: Detailed Spec §6.2. Planned component: Core authorization; identity SPI; capability registry.

Target: M1. Verification owners: Security; QA.

Verification: Exercise every operation with valid, expired, revoked, wrong-role, wrong-device and wrong-zone credentials; refuse self-approval through direct API calls.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-ins04-cap-01"></a>INS04-CAP-01<br>v4: FND04-CAP-01 | Interactive users authenticate through the enterprise identity provider. The product implements no local-password login. | MUST | `check_ins04_cap_01` | Unverified / — |
| <a id="req-ins04-cap-02"></a>INS04-CAP-02<br>v4: FND04-CAP-02 | Multi-factor authentication is enforced for all content-handling and privileged roles. | MUST | `check_ins04_cap_02` | Unverified / — |
| <a id="req-ins04-cap-03"></a>INS04-CAP-03<br>v4: FND04-CAP-03 | Sessions are short-lived with an inactivity timeout; privileged actions require re-authentication. | MUST | `check_ins04_cap_03` | Unverified / — |
| <a id="req-ins04-cap-04"></a>INS04-CAP-04<br>v4: FND04-CAP-04 | A registry records, against a pseudonymous workforce audit identifier, what each contributor is recognized to do: role, subject and language scope, accessibility qualification, issuing authority, validity window and revocation state. | MUST | `check_ins04_cap_04` | Unverified / — |
| <a id="req-ins04-cap-05"></a>INS04-CAP-05<br>v4: FND04-CAP-05 | Assignment requires a current, non-revoked, in-scope entry in the registry. Subject, language and workload matching alone do not authorize an assignment. | MUST | `check_ins04_cap_05` | Unverified / — |
| <a id="req-ins04-cap-06"></a>INS04-CAP-06<br>v4: FND04-CAP-06 | Expiry blocks new assignment and flags in-flight tasks for reassignment. It never voids a decision already recorded. | MUST | `check_ins04_cap_06` | Unverified / — |
| <a id="req-ins04-cap-07"></a>INS04-CAP-07<br>v4: FND04-CAP-07 | A user may hold multiple roles but is blocked from authoring or translating and then approving the same version. The API enforces this independently of the interface. | MUST | `check_ins04_cap_07` | Unverified / — |
| <a id="req-ins04-cap-08"></a>INS04-CAP-08<br>v4: FND04-CAP-08 | An accessibility specialist cannot act on a version they authored, translated or reviewed. | MUST | `check_ins04_cap_08` | Unverified / — |
| <a id="req-ins04-cap-09"></a>INS04-CAP-09<br>v4: FND04-CAP-09 | Access to any object outside the user's assignments returns a denial and raises a security event. | MUST | `check_ins04_cap_09` | Unverified / — |
| <a id="req-ins04-cap-10"></a>INS04-CAP-10<br>v4: FND04-CAP-10 | Revocation takes effect on the next request; an in-flight assignment becomes unactionable immediately. | MUST | `check_ins04_cap_10` | Unverified / — |
| <a id="req-ins04-cap-11"></a>INS04-CAP-11<br>v4: FND04-CAP-11 | Sign-in to any content-handling surface succeeds only from a managed workstation inside an approved network zone, proven by device certificate and posture check. A request from an unmanaged or non-compliant device is denied and raises a security event, regardless of how valid the user's credentials are. | MUST | `check_ins04_cap_11` | Unverified / — |
| <a id="req-prd-cap-12"></a>PRD-CAP-12 | GAP Identity integration uses OpenID Connect Authorization Code flow with PKCE against the enterprise identity provider. The token must carry a stable subject and an authentication-methods claim proving multi-factor authentication; a token without it is refused with FORBIDDEN_MFA_REQUIRED. Group or role claims in the token are informational only and never authorize anything (ARC-01). | MUST | `check_prd_cap_12` | Unverified / — |
| <a id="req-prd-cap-13"></a>PRD-CAP-13 | GAP Pseudonymization: on first sign-in the system generates a random, unguessable, stable workforce audit identifier and stores the mapping to the identity-provider subject in a separately access-controlled table. All business records, audit events, telemetry and screens other than the coordinator's assignment views use the audit identifier only (DAT-02). | MUST | `check_prd_cap_13` | Unverified / — |
| <a id="req-prd-cap-14"></a>PRD-CAP-14 | GAP D-14 Proposed session parameters: access token lifetime 15 minutes with silent refresh; refresh window 8 hours; inactivity timeout 20 minutes with a visible warning at 18; absolute session maximum 10 hours. Privileged actions requiring a fresh authentication (no older than 5 minutes): cycle changes, registry changes, exception approval, correction authorization, retirement, manual assignment override. | MUST | `check_prd_cap_14` | Unverified / — |
| <a id="req-prd-cap-15"></a>PRD-CAP-15 | GAP Device and zone proof (CAP-11): a client certificate from the enterprise device authority presented at the TLS edge; a posture assertion from endpoint management (disk encryption on, operating system patched, agent running) no older than the configured freshness D-14; and a source address inside the approved studio zone. All three are checked at sign-in and on every token refresh. Failure denies with FORBIDDEN_DEVICE_POSTURE and raises a security event; the user sees "This device or location isn't approved for content work". | MUST | `check_prd_cap_15` | Unverified / — |
| <a id="req-prd-cap-16"></a>PRD-CAP-16 | GAP Capability entry fields: audit identifier, role, subject scope (taxonomy subject identifiers), language scope (BCP 47 tags), accessibility qualification with credential reference, issuing authority, valid from, valid to, revoked at, revocation reason, created by, audit references. Entries are append-only with supersession; renewals create a new entry. | MUST | `check_prd_cap_16` | Unverified / — |
| <a id="req-prd-cap-17"></a>PRD-CAP-17 | GAP A valid token with no capability entry, or a role claim matching no known role, lands on a "Not provisioned — contact your administrator" screen; access is denied and a security event raised. | MUST | `check_prd_cap_17` | Unverified / — |
| <a id="req-prd-cap-18"></a>PRD-CAP-18 | GAP Authorization reads the registry on every request. Any cache is at most 5 seconds and is invalidated synchronously on revocation, so CAP-10 holds. An hourly sweep marks expired entries, flags their in-flight assignments on the coordinator board, and leaves recorded decisions untouched. | MUST | `check_prd_cap_18` | Unverified / — |
| <a id="req-prd-cap-19"></a>PRD-CAP-19 | GAP D-05 Registry maintenance (create, renew, revoke) is performed by the Coordinator role with re-authentication and is fully audited. The identity provider remains the identity authority; the registry never stores names, emails or credentials beyond the pseudonym mapping table. | MUST | `check_prd_cap_19` | Unverified / — |

## 6.3 — Assignment and My Work

Source: Detailed Spec §6.3. Planned component: Core assignment services; role task surfaces.

Target: M1/M3. Verification owners: Content Operations; QA.

Verification: Assign by eligibility and workload, break ties deterministically, expire/reassign tasks, reject conflicts, and route corrected work to a different reviewer.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm03-rev-01"></a>ASM03-REV-01<br>v4: QST03-REV-01 | Submitted versions are assigned to eligible reviewers by system policy using subject, language, workload, recognized capability and separation of duties. Authors cannot nominate reviewers. | MUST | `check_asm03_rev_01` | Unverified / — |
| <a id="req-asm03-rev-08"></a>ASM03-REV-08<br>v4: QST03-REV-08 | An open question or artefact is locked to the assigned reviewer. A second actor attempting a decision on an already-decided version is rejected with a clear message. | MUST | `check_asm03_rev_08` | Unverified / — |
| <a id="req-asm03-rev-09"></a>ASM03-REV-09<br>v4: QST03-REV-09 | Tasks expire after a configured period and return to the assignment pool. Aging is visible to coordinators. | MUST | `check_asm03_rev_09` | Unverified / — |
| <a id="req-ui-02"></a>UI-02 | §6.3: My Work shows assigned tasks with type, cycle, subject, language, state, age and deadline. No unassigned content is reachable.; §9.2: My Work — assigned tasks with type, cycle, subject, language, state, age and deadline. No unassigned content is reachable. | MUST | `check_ui_02` | Unverified / — |
| <a id="req-ui-03"></a>UI-03 | §6.3: A task becoming available is actively surfaced to the assignee; work does not sit unannounced in a queue nobody is prompted to check.; §9.2: My Work — a task becoming available is actively surfaced to the assignee; work does not sit unannounced in a queue nobody is prompted to check. | MUST | `check_ui_03` | Unverified / — |
| <a id="req-prd-asg-01"></a>PRD-ASG-01 | GAP Task types: author_primary, review, accessibility_check, translate, translation_review, revalidate_variant, correct_primary. Each maps to exactly one role. | MUST | `check_prd_asg_01` | Unverified / — |
| <a id="req-prd-asg-02"></a>PRD-ASG-02 | GAP Assignment record: identifier, task type, user audit identifier, subject reference (version, lineage or artefact), cycle, language, created at, expires at, status (Active, Completed, Released, Expired, Reassigned), release reason, policy version used. Assignments are append-only; reassignment closes one and opens another. | MUST | `check_prd_asg_02` | Unverified / — |
| <a id="req-prd-asg-03"></a>PRD-ASG-03 | GAP Eligibility: a current, non-revoked capability entry whose role matches the task type and whose subject and language scope cover the artefact; accessibility qualification for accessibility tasks; no separation-of-duties conflict (§4.4); open-task workload below the configured cap D-13. The version's author can never be in the pool for that lineage. | MUST | `check_prd_asg_03` | Unverified / — |
| <a id="req-prd-asg-04"></a>PRD-ASG-04 | GAP Selection is deterministic: lowest current open workload first, then longest time since last assignment, then stable ordering by audit identifier. The policy version and the candidate count are recorded on the assignment. A coordinator's manual assignment must pass the same eligibility check server-side. | MUST | `check_prd_asg_04` | Unverified / — |
| <a id="req-prd-asg-05"></a>PRD-ASG-05 | GAP When no eligible user exists the task stays Unassigned, appears on the coordinator board immediately, and raises an operational alert after the configured delay D-12. | MUST | `check_prd_asg_05` | Unverified / — |
| <a id="req-prd-asg-06"></a>PRD-ASG-06 | GAP Expiry: an assignment past its deadline is released to the pool by a sweep running at least every 5 minutes, audited, and shown in coordinator aging. The version's state is unchanged. A decision recorded before expiry is never voided. | MUST | `check_prd_asg_06` | Unverified / — |
| <a id="req-prd-asg-07"></a>PRD-ASG-07 | GAP Surfacing (UI-03): a new or returned task is pushed to the assignee's open My Work screen over the server-push channel and shown as an in-app notification badge. Any out-of-band notification channel D-19 carries only "You have a new task" and a link — no artefact identifier, subject or content (DAT-03). | MUST | `check_prd_asg_07` | Unverified / — |
| <a id="req-prd-asg-08"></a>PRD-ASG-08 | GAP Locking (REV-08): opening a review or accessibility task records the opening time; a decision is accepted only from the assignee and only while the version is still in the decided-from state. A second decision on an already-decided version returns CONFLICT_ALREADY_DECIDED and the caller's queue refreshes. | MUST | `check_prd_asg_08` | Unverified / — |
| <a id="req-prd-asg-09"></a>PRD-ASG-09 | GAP When an assignee leaves or loses recognized capability mid-task, the assignment is released to the pool by the next request or the sweep, whichever is first; no task is orphaned; decisions already recorded remain valid. | MUST | `check_prd_asg_09` | Unverified / — |
| <a id="req-prd-asg-10"></a>PRD-ASG-10 | GAP Different reviewer after rejection (engineering PRD): the successor version of a rejected version is assigned, at the same stage, to a reviewer other than the one who rejected it and other than any earlier rejecting reviewer of that lineage. If no other eligible reviewer exists the task stays Unassigned and the Admin is alerted; the Admin cannot override this rule. | MUST | `check_prd_asg_10` | Unverified / — |
| <a id="req-prd-asg-11"></a>PRD-ASG-11 | GAP Task types are extended for the converged workflow: accessibility_remediation (Accessibility Specialist) is distinct from accessibility_review (Accessibility Reviewer); the Admin's assignment board shows both. | MUST | `check_prd_asg_11` | Unverified / — |

## 6.4 — Authoring and generation

Source: Detailed Spec §6.4. Planned component: Core artefact services; signed content client; Layer 2 connector and service.

Target: M2/M4; by 28 September 2026. Verification owners: Product; QA; Security.

Verification: Create, autosave, validate and submit manual and generated drafts; preserve provenance and immutable submissions; refuse blocked egress and unsupported content. AI never approves.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm03-ath-01"></a>ASM03-ATH-01<br>v4: QST03-ATH-01 | An author sees only draft questions and the minimum metadata needed to act. There is no browsable artefact repository. | MUST | `check_asm03_ath_01` | Unverified / — |
| <a id="req-asm03-ath-02"></a>ASM03-ATH-02<br>v4: QST03-ATH-02 | The editor creates a single-select multiple-choice artefact with a stem, 2 – 8 unique non-empty options, exactly one correct option, an explanation, and all required classification and marking metadata. | MUST | `check_asm03_ath_02` | Unverified / — |
| <a id="req-asm03-ath-03"></a>ASM03-ATH-03<br>v4: QST03-ATH-03 | Classification is captured against the current syllabus version and taxonomy: subject, unit, topic, difficulty and taxonomy level. | MUST | `check_asm03_ath_03` | Unverified / — |
| <a id="req-asm03-ath-04"></a>ASM03-ATH-04<br>v4: QST03-ATH-04 | Content supports sanitized restricted HTML, full Unicode, sub- and superscript, lists, accessible tables, and canonical LaTeX rendered through the shared reference renderer. | MUST | `check_asm03_ath_04` | Unverified / — |
| <a id="req-asm03-ath-05"></a>ASM03-ATH-05<br>v4: QST03-ATH-05 | The editor autosaves at least every 15 seconds and on field exit, and always displays saved, pending or failed status. | MUST | `check_asm03_ath_05` | Unverified / — |
| <a id="req-asm03-ath-06"></a>ASM03-ATH-06<br>v4: QST03-ATH-06 | Draft writes require an optimistic-concurrency token. A stale write is rejected and never overwrites newer content. | MUST | `check_asm03_ath_06` | Unverified / — |
| <a id="req-asm03-ath-07"></a>ASM03-ATH-07<br>v4: QST03-ATH-07 | Preview uses the same rendering contract as review, accessibility check and downstream delivery. | MUST | `check_asm03_ath_07` | Unverified / — |
| <a id="req-asm03-ath-08"></a>ASM03-ATH-08<br>v4: QST03-ATH-08 | Images are supported in stem, options and explanation. Every meaningful image requires alternative text; decorative images require an explicit flag. | MUST | `check_asm03_ath_08` | Unverified / — |
| <a id="req-asm03-ath-09"></a>ASM03-ATH-09<br>v4: QST03-ATH-09 | Equations are stored as canonical LaTeX and rendered to an accessible representation. | MUST | `check_asm03_ath_09` | Unverified / — |
| <a id="req-asm03-ath-10"></a>ASM03-ATH-10<br>v4: QST03-ATH-10 | The interface exposes no download, print, bulk export or persistent browser-storage capability. Every artefact is stored on the server immediately, leaving no residual copy on the author's machine. | MUST | `check_asm03_ath_10` | Unverified / — |
| <a id="req-asm03-ath-11"></a>ASM03-ATH-11<br>v4: QST03-ATH-11 | An author can withdraw an unsubmitted draft; withdrawal is audited and removes it from active counts. | MUST | `check_asm03_ath_11` | Unverified / — |
| <a id="req-asm03-ath-12"></a>ASM03-ATH-12<br>v4: QST03-ATH-12 | A per-author artefact cap is configurable per cycle. Reaching the cap blocks new creation and is visible to the coordinator. | MUST | `check_asm03_ath_12` | Unverified / — |
| <a id="req-asm03-ath-13"></a>ASM03-ATH-13<br>v4: QST03-ATH-13 | Every resource an author needs is built into the authoring tool — reference material, symbol and equation palettes, and the approved glossary. The author is never required to leave the tool, and no external source is reachable from it. | MUST | `check_asm03_ath_13` | Unverified / — |
| <a id="req-prd-ath-14"></a>PRD-ATH-14 | GAP D-11 Proposed field limits, measured on text after markup is stripped: stem ≤ 4,000 characters; each option ≤ 1,000; explanation ≤ 6,000; alternative text 3 – 300 characters; at most 6 images per version; each image ≤ 2 MB and ≤ 4,000 × 4,000 pixels; total asset budget ≤ 8 MB per version. Limits are configuration with these defaults and are enforced server-side with field-level errors. | MUST | `check_prd_ath_14` | Unverified / — |
| <a id="req-prd-ath-15"></a>PRD-ATH-15 | GAP Content model of a version: stem; ordered options, each with a structural identifier, a body and a correct flag; explanation; classification (subject, unit, topic, difficulty as proposed by the author, taxonomy level); marks; assets with checksum, alternative text and decorative flag. Stem, option bodies and explanation are restricted-HTML documents in which equations are inline equation nodes holding canonical LaTeX and images are asset references. | MUST | `check_prd_ath_15` | Unverified / — |
| <a id="req-prd-ath-16"></a>PRD-ATH-16 | GAP D-09 Restricted-HTML allowlist (SEC-10). Elements: p, br, strong, em, u, s, sub, sup, ul, ol, li, table, caption, thead, tbody, tr, th, td, img, span, eq. Attributes: th[scope], td&#124;th[colspan&#124;rowspan ≤ 8], img[src (asset: scheme only), alt, data-decorative], ol[start], span[dir, lang], eq[data-latex]. No hyperlinks, no style attributes, no event handlers, no comments, no scripts, no external URL scheme of any kind. Sanitization removes anything else and reports each removal to the author as a warning; the sanitized form is what is validated, previewed and stored. | MUST | `check_prd_ath_16` | Unverified / — |
| <a id="req-prd-ath-17"></a>PRD-ATH-17 | GAP D-10 Permitted LaTeX subset (SEC-10): arithmetic and relations; \frac, \sqrt[n]{}, superscript and subscript; Greek letters; \sin \cos \tan \log \ln \exp \lim \sum \prod \int with limits; \left \right with round, square and brace delimiters and vertical bars; \vec \hat \bar \overline \dot; \text{}; pmatrix, bmatrix and cases up to 6 × 6; aligned up to 6 lines; the operator symbols \cdot \times \div \pm \mp \le \ge \ne \approx \equiv \infty \to \in \notin \subset \subseteq \cup \cap \forall \exists \partial \nabla \degree \angle \perp \parallel; spacing commands. Prohibited: any macro definition (\def, \newcommand, \let), file or catcode commands, \href \url, colour commands, raw HTML. Bounds: 2,000 characters, nesting depth 12, 200 ms render budget per equation. Anything outside is rejected with a bounded-subset message and no unbounded rendering work is performed. | MUST | `check_prd_ath_17` | Unverified / — |
| <a id="req-prd-ath-18"></a>PRD-ATH-18 | GAP Reference renderer: one versioned rendering component, executed server-side, produces the semantic HTML with MathML and text alternatives that preview, review, accessibility check, sealing and downstream delivery all use. Its renderer_version is recorded on every decision and in every manifest. A difference in output between author preview and review for the same canonical content is a defect, not a variance. | MUST | `check_prd_ath_18` | Unverified / — |
| <a id="req-prd-ath-19"></a>PRD-ATH-19 | GAP Autosave protocol: save 2 seconds after the last change, at least every 15 seconds while dirty, and on field exit; each save sends the concurrency token and receives the next one; status shows Saved, Saving… or Failed (retrying); a stale-token rejection reloads the server copy and shows the author what differs without discarding their unsaved text. The client keeps draft state in memory only — never in persistent browser storage (ATH-10). | MUST | `check_prd_ath_19` | Unverified / — |
| <a id="req-prd-ath-20"></a>PRD-ATH-20 | GAP D-20 Forced re-authentication: when the refresh window has expired, the client attempts one immediate autosave, then redirects to sign-in with the unsaved state held in memory for the same tab; on return the draft is reloaded from the server and any surviving unsaved text is offered for re-application. Loss is bounded by the autosave interval (≤ 30 s, §11). | MUST | `check_prd_ath_20` | Unverified / — |
| <a id="req-prd-ath-21"></a>PRD-ATH-21 | GAP D-21 The hardened editor region is visually marked. Inside it copy, cut, paste, drag-and-drop of text, context menu and print are blocked and reported (§6.14). Text selection remains possible for editing. The user receives non-blocking feedback that the action was blocked and recorded. | MUST | `check_prd_ath_21` | Unverified / — |
| <a id="req-prd-ath-22"></a>PRD-ATH-22 | GAP Author cap counting: drafts plus submitted versions authored in the cycle, excluding Withdrawn versions and excluding successor drafts created by a return. Reaching the cap returns AUTHOR_CAP_REACHED on create; the coordinator sees per-author counts against the cap. | MUST | `check_prd_ath_22` | Unverified / — |
| <a id="req-prd-ath-23"></a>PRD-ATH-23 | GAP In-tool resources (ATH-13): a read-only reference-material viewer for documents loaded by Content Operations; a Unicode symbol palette organized by category; an equation palette of templates drawn only from the permitted subset; the approved glossary per language, searchable. All are served by the application from its own store; no outbound link exists anywhere in the tool. | MUST | `check_prd_ath_23` | Unverified / — |
| <a id="req-prd-ath-24"></a>PRD-ATH-24 | GAP Scripts and direction: every text field accepts full Unicode, supports right-to-left direction per field, and round-trips the pilot scripts without loss through sanitization, canonicalization and rendering. | MUST | `check_prd_ath_24` | Unverified / — |
| <a id="req-prd-ath-25"></a>PRD-ATH-25 | GAP D-38 Generated candidates: a generation request by the Admin (curriculum, cycle, question type, marks, required count × candidate multiplier) produces independent artefacts, each with one DRAFT of provenance generated, owned by the requesting Admin. Every generated draft records generation identifier, model identifier, generation configuration, source curriculum, chapter, page range, stored source context, and timestamp. A generated draft that fails the automated validation catalogue (§6.5) is discarded before any human sees it. Generated drafts are never grouped as alternatives of one question. The generation service runs outside the hardened zones and never receives content from the pipeline. | MUST | `check_prd_ath_25` | Unverified / — |
| <a id="req-prd-ath-26"></a>PRD-ATH-26 | GAP Metadata (engineering PRD §9.2): in addition to classification, a version carries grade, curriculum reference, learning objective, competency, question type, language, source curriculum, chapter, page range and source context, status, version number, created and updated timestamps, and — where generated — generation identifier, model and configuration. Source context text is Restricted and is never shown to reviewers (D-47). | MUST | `check_prd_ath_26` | Unverified / — |
| <a id="req-prd-ath-27"></a>PRD-ATH-27 | GAP D-44 Question types: single-select multiple choice is fully supported. Other types the blueprint may name (for example short answer) are stored with the same content model minus options, and may enter the pipeline only when the cycle enables them; the validation and structural rule sets for such types are reduced accordingly and named per type. | SHOULD | `check_prd_ath_27` | Unverified / — |

## 6.5 — Validation and submission

Source: Detailed Spec §6.5. Planned component: Core deterministic validators; sanitize/similarity/render interfaces.

Target: M2. Verification owners: Assessment owner; QA.

Verification: Use valid and invalid synthetic fixtures for every named rule; show field-specific blocking findings; deny submission until blockers clear, without model calls.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm03-val-01"></a>ASM03-VAL-01<br>v4: QST03-VAL-01 | Validation is deterministic and rule-based only. It performs schema, answer, taxonomy, asset, equation, prohibited-markup, accessibility-completeness and within-artefact duplicate checks. | MUST | `check_asm03_val_01` | Unverified / — |
| <a id="req-asm03-val-02"></a>ASM03-VAL-02<br>v4: QST03-VAL-02 | Blocking findings prevent submission; each is reported against the specific field with actionable text. | MUST | `check_asm03_val_02` | Unverified / — |
| <a id="req-asm03-val-03"></a>ASM03-VAL-03<br>v4: QST03-VAL-03 | Validation causes no state change and calls no probabilistic or external inference service. | MUST | `check_asm03_val_03` | Unverified / — |
| <a id="req-asm03-val-04"></a>ASM03-VAL-04<br>v4: QST03-VAL-04 | Submission creates an immutable version and a content hash. Subsequent editing cannot alter the version under review. | MUST | `check_asm03_val_04` | Unverified / — |
| <a id="req-asm03-val-05"></a>ASM03-VAL-05<br>v4: QST03-VAL-05 | The author receives a submission confirmation of the question. | MUST | `check_asm03_val_05` | Unverified / — |
| <a id="req-asm03-val-06"></a>ASM03-VAL-06<br>v4: QST03-VAL-06 | Submission runs a deterministic similarity check of the stem and options against every sealed question in the question bank. A match above the configured threshold is a blocking finding naming the matched identifiers. The comparison uses normalized text and is rule-based; no model is involved. | MUST | `check_asm03_val_06` | Unverified / — |
| <a id="req-prd-val-07"></a>PRD-VAL-07 | GAP The validation rule catalogue below is the complete set for the MVP. Each rule has a stable code, a severity (blocking or warning), and reports the field path it applies to. The rule-set version is recorded with every validation report. | MUST | `check_prd_val_07` | Unverified / — |
| <a id="req-prd-val-08"></a>PRD-VAL-08 | GAP A validation report is returned to the client and stored with the submission as evidence: rule-set version, renderer version, and one entry per finding with code, severity, field path and message. Validation is a pure function of the draft and the configuration. | MUST | `check_prd_val_08` | Unverified / — |
| <a id="req-prd-val-09"></a>PRD-VAL-09 | GAP D-08 Similarity check design (VAL-06): text is normalized (markup stripped, equations reduced to their LaTeX text, Unicode NFC, case-folded, punctuation removed, whitespace collapsed) and tokenized into words; the fingerprint is the set of 64-bit hashes of word 3-grams over stem plus options. At sealing, the fingerprint of every sealed version is stored in the bank index as Restricted derived data D-31. At submission, the candidate's fingerprint is compared by Jaccard similarity against every sealed fingerprint in the same language across the whole bank; a result at or above the threshold (proposed 0.80) is a blocking VAL-SIM-01 naming the matched artefact identifiers. The computation is exact and reproducible. | MUST | `check_prd_val_09` | Unverified / — |
| <a id="req-prd-val-10"></a>PRD-VAL-10 | GAP Submission transaction: validate → sanitize and canonicalize (§8.4) → compute content hash → create the immutable version snapshot in state In Review → persist the validation report and similarity result → write the audit event → enqueue domain events in the transactional outbox → return the receipt (version identifier, content hash, submission time, rule-set version). If the audit store is unavailable the submission fails closed (ASR01-EVD-07). | MUST | `check_prd_val_10` | Unverified / — |
| <a id="req-prd-val-11"></a>PRD-VAL-11 | GAP Submission is idempotent: repeating it with the same draft concurrency token returns the original receipt and creates no second version. | MUST | `check_prd_val_11` | Unverified / — |

## 6.6 — Question review

Source: Detailed Spec §6.6. Planned component: Core decisions service; Question Reviewer surface.

Target: M3. Verification owners: Assessment owner; QA.

Verification: Complete every attestation and rationale; test isolation in response payloads and access attempts, read-only review, conflict refusal and rejection lineage.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm03-rev-02"></a>ASM03-REV-02<br>v4: QST03-REV-02 | The review workspace is read-only and shows the exact submitted version, its content hash, permitted metadata and a mandatory structured checklist. | MUST | `check_asm03_rev_02` | Unverified / — |
| <a id="req-asm03-rev-03"></a>ASM03-REV-03<br>v4: QST03-REV-03 | No review endpoint accepts content fields. Direct editing is never offered. | MUST | `check_asm03_rev_03` | Unverified / — |
| <a id="req-asm03-rev-04"></a>ASM03-REV-04<br>v4: QST03-REV-04 | The reviewer validates correctness and checks the classification, difficulty and taxonomy level assigned by the author against the syllabus version in force. | MUST | `check_asm03_rev_04` | Unverified / — |
| <a id="req-asm03-rev-05"></a>ASM03-REV-05<br>v4: QST03-REV-05 | Approval requires a complete checklist. Return requires a reason code and actionable comments. | MUST | `check_asm03_rev_05` | Unverified / — |
| <a id="req-asm03-rev-06"></a>ASM03-REV-06<br>v4: QST03-REV-06 | Approval moves the exact version to accessibility check. A return creates a new linked draft carrying the findings; the returned version remains as immutable evidence. | MUST | `check_asm03_rev_06` | Unverified / — |
| <a id="req-asm03-rev-07"></a>ASM03-REV-07<br>v4: QST03-REV-07 | Decisions are append-only and bind the checklist, rationale, reviewer audit identifier, duration and version hash. | MUST | `check_asm03_rev_07` | Unverified / — |
| <a id="req-asm03-rev-10"></a>ASM03-REV-10<br>v4: QST03-REV-10 | Whether one or two independent reviews are required before approval is configuration, not code. | MUST | `check_asm03_rev_10` | Unverified / — |
| <a id="req-asm03-rev-11"></a>ASM03-REV-11<br>v4: QST03-REV-11 | The reviewer records an explicit attestation, inside the mandatory checklist, covering three checks: language and grammatical correctness; that the artefact is not available in the public domain; and that it complies with the prescribed guidelines and curriculum scope for the cycle. Each is recorded separately with the source consulted, not as a single combined tick. | MUST | `check_asm03_rev_11` | Unverified / — |
| <a id="req-asm03-rev-12"></a>ASM03-REV-12<br>v4: QST03-REV-12 | The reviewer assigns a difficulty value from the controlled vocabulary at the point of approval. The field for discrimination is created and left empty; it is populated only from candidate performance data after an exam and is never estimated. | MUST | `check_asm03_rev_12` | Unverified / — |
| <a id="req-prd-rev-13"></a>PRD-REV-13 | GAP D-19 The structured checklist is a configured template per cycle with the items listed below. Every item is Pass, Fail or Not applicable (with a reason). Approval requires every item Pass or Not applicable and all three attestations complete with a source. The equivalence-judgement item appears only for variants. | MUST | `check_prd_rev_13` | Unverified / — |
| <a id="req-prd-rev-14"></a>PRD-REV-14 | GAP D-19 Return reason codes are a controlled vocabulary (below). A return requires one code and comments of at least 20 characters; the controls stay disabled until both are satisfied. | MUST | `check_prd_rev_14` | Unverified / — |
| <a id="req-prd-rev-15"></a>PRD-REV-15 | GAP Decision record fields: identifier; version identifier and version hash; decision type (review, translation review, accessibility); outcome; checklist responses; attestations with sources; reason code; comments; difficulty assigned; equivalence judgement; reviewer audit identifier; capability entry identifier valid at the time; renderer version; policy version; opened at; decided at; duration; correlation identifier. The record's own hash is written into the audit event. | MUST | `check_prd_rev_15` | Unverified / — |
| <a id="req-prd-rev-16"></a>PRD-REV-16 | GAP Two-review policy (REV-10): when the cycle requires two reviews, the version stays In Review until two approvals from different, duty-clean reviewers exist; the second reviewer cannot see the first reviewer's checklist until their own decision is recorded; a single return sends the version back regardless of other approvals. | MUST | `check_prd_rev_16` | Unverified / — |
| <a id="req-prd-rev-17"></a>PRD-REV-17 | GAP A return creates the successor Draft with derived_from set, attaches the findings so they appear inside the editor beside the fields they name, and assigns the draft to the original author, or to the pool if that author is no longer eligible. | MUST | `check_prd_rev_17` | Unverified / — |
| <a id="req-prd-rev-18"></a>PRD-REV-18 | GAP D-06 Correct-answer visibility in review is governed by the cycle flag reviewer_sees_key (SEC-02). Proposed default: true, because validating correctness (REV-04) requires knowing the key. When false, the reviewer is asked to identify the key and the workspace records whether it matched. | MUST | `check_prd_rev_18` | Unverified / — |
| <a id="req-prd-rev-19"></a>PRD-REV-19 | GAP Reviewer isolation (engineering PRD §10, §20, adopted verbatim). The review workspace shows the reference rendering, the content hash, and only the metadata needed to evaluate the question: subject, grade, curriculum name, question type, marks, Bloom's level, difficulty, language, version number, submission time, the validation warnings, and the source chapter and page range for grounding checks (D-47). It never shows: assessment name, title or identifier; final question number; other questions in any assessment; candidate-pool membership or selection status; which users reviewed the question or any other reviewer; the audit history; the author's identity or pseudonym; the stored source context text. The artefact identifier QB-nnnnn is not a question number and reveals no assessment context. | MUST | `check_prd_rev_19` | Unverified / — |
| <a id="req-prd-rev-21"></a>PRD-REV-21 | GAP Comments: every review role may add free-text comments to its decision; comments are Restricted, visible to the Admin and carried into the successor draft, and never visible to any other reviewer (engineering PRD). | MUST | `check_prd_rev_21` | Unverified / — |
| <a id="req-prd-rev-20"></a>PRD-REV-20 | GAP The worklist locks to the open task until a decision is recorded, then advances to the next assigned task (UI-07). Leaving the workspace without deciding keeps the assignment active and records the duration so far. | MUST | `check_prd_rev_20` | Unverified / — |

## 6.7 — Accessibility

Source: Detailed Spec §6.7. Planned component: Core remediation and decisions; Specialist and Reviewer surfaces; render contract.

Target: M3. Verification owners: Accessibility lead; QA.

Verification: Restrict remediation fields, separate completion from approval, test keyboard and screen reader behaviour, record accommodations and route content changes back through review.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm04-acc-01"></a>ASM04-ACC-01<br>v4: QST04-ACC-01 | The accessibility specialist tests the same reference rendering intended for downstream candidate delivery, in a read-only mode that cannot alter content. | MUST | `check_asm04_acc_01` | Unverified / — |
| <a id="req-asm04-acc-02"></a>ASM04-ACC-02<br>v4: QST04-ACC-02 | The workspace provides keyboard and screen-reader test affordances against the rendered artefact. | MUST | `check_asm04_acc_02` | Unverified / — |
| <a id="req-asm04-acc-03"></a>ASM04-ACC-03<br>v4: QST04-ACC-03 | Evaluation covers screen-reader compatibility, alternative text, colour contrast, font readability, plain-language clarity, reading order, focus, keyboard operation, tables, equations, and whether the artefact relies solely on visual or auditory cues. | MUST | `check_asm04_acc_03` | Unverified / — |
| <a id="req-asm04-acc-04"></a>ASM04-ACC-04<br>v4: QST04-ACC-04 | Approval requires no unresolved blocking findings and mandatory comments. A return records the affected element and the required remediation. | MUST | `check_asm04_acc_04` | Unverified / — |
| <a id="req-asm04-acc-05"></a>ASM04-ACC-05<br>v4: QST04-ACC-05 | Approval requests sealing into the repository. A return creates a new linked draft. | MUST | `check_asm04_acc_05` | Unverified / — |
| <a id="req-asm04-acc-06"></a>ASM04-ACC-06<br>v4: QST04-ACC-06 | Whether remediation repeats review is policy-driven configuration, defaulting to repeat when content, answer or metadata changed. | MUST | `check_asm04_acc_06` | Unverified / — |
| <a id="req-asm04-acc-07"></a>ASM04-ACC-07<br>v4: QST04-ACC-07 | The decision records which of the cycle's declared accommodations the rendered artefact can be delivered under. | MUST | `check_asm04_acc_07` | Unverified / — |
| <a id="req-asm04-acc-08"></a>ASM04-ACC-08<br>v4: QST04-ACC-08 | An artefact that cannot be delivered under a declared accommodation is recorded as needing an equivalent route, with a reason, and is escalated rather than silently approved. | MUST | `check_asm04_acc_08` | Unverified / — |
| <a id="req-asm04-acc-09"></a>ASM04-ACC-09<br>v4: QST04-ACC-09 | Generation of alternate-format artefacts is out of scope; the data model must not preclude it. | MAY | `check_asm04_acc_09` | Unverified / — |
| <a id="req-prd-acc-10"></a>PRD-ACC-10 | GAP The evaluation checklist implements ACC-03 item by item (table below). Each item is Pass, Fail (with at least one finding) or Not applicable (with reason). | MUST | `check_prd_acc_10` | Unverified / — |
| <a id="req-prd-acc-11"></a>PRD-ACC-11 | GAP A finding records: element reference (structural identifier or field path), criterion, severity (blocking or advisory), description, required remediation. A return requires at least one blocking finding; an approval requires zero unresolved blocking findings and comments of at least 20 characters. Advisory findings travel to the successor draft as guidance without blocking. | MUST | `check_prd_acc_11` | Unverified / — |
| <a id="req-prd-acc-12"></a>PRD-ACC-12 | GAP D-17 Accommodation capability: for every accommodation declared by the cycle the decision records deliverable or needs equivalent route with a reason. Any needs equivalent route creates an escalation task for the coordinator with an operational alert. Proposed default: the flag does not block sealing or readiness; it is carried on the readiness record so assembly can respect it. | MUST | `check_prd_acc_12` | Unverified / — |
| <a id="req-prd-acc-13"></a>PRD-ACC-13 | GAP Test affordances (ACC-02) provided on the reference rendering without altering content: keyboard-only navigation mode with visible focus order; screen-reader-oriented view exposing the accessible name, role and MathML of each element; text-only view; zoom at 200 % and 400 %; contrast measurement per text element; a reading-order outline. | MUST | `check_prd_acc_13` | Unverified / — |
| <a id="req-prd-acc-14"></a>PRD-ACC-14 | GAP D-07 Remediation routing policy values: always_repeat_review, repeat_when_content_changed (default), never_repeat. "Changed" is defined in §5.4. | MUST | `check_prd_acc_14` | Unverified / — |
| <a id="req-prd-acc-15"></a>PRD-ACC-15 | GAP To honour ACC-09, renditions are modelled as a separate entity keyed by version, format and status, with the reference rendering as the first format. No code path assumes a single format. | MUST | `check_prd_acc_15` | Unverified / — |
| <a id="req-prd-acc-16"></a>PRD-ACC-16 | GAP Accessibility remediation task (engineering IN_ACCESSIBILITY): on question-review approval the system creates an accessibility draft derived from the approved version and assigns an Accessibility Specialist by policy. The draft exposes only accessibility fields: alternative text and decorative flags, table headers and captions, equation text alternatives, reading-order markup and accessibility metadata. Stem, options, correct flag, explanation, marks, classification, image bytes and mathematical notation are locked and machine-verified unchanged on completion. The specialist completes the evaluation checklist as a self-check, may comment, and completes the task, which creates the immutable version that enters IN_ACCESSIBILITY_REVIEW. | MUST | `check_prd_acc_16` | Unverified / — |
| <a id="req-prd-acc-17"></a>PRD-ACC-17 | GAP A finding that needs an authoring change (wording, image, notation) is recorded by the specialist as a comment and by the reviewer as an RC-A11Y-* rejection to the author; the specialist never edits those fields. | MUST | `check_prd_acc_17` | Unverified / — |
| <a id="req-prd-acc-18"></a>PRD-ACC-18 | GAP The Accessibility Reviewer decides on the completed accessibility version: approval requests sealing; rejection creates an accessibility-correction draft for a different Accessibility Specialist (accessibility findings) or an authoring-correction draft for the author (authoring findings), and the next accessibility review is by a different Accessibility Reviewer (PRD-ASG-10). | MUST | `check_prd_acc_18` | Unverified / — |
| <a id="req-prd-acc-19"></a>PRD-ACC-19 | GAP D-43 Every language version — the primary and each variant — has its own remediation task and review (ASM04-TRN-05). For variants the remediation is normally limited to translated alternative text and captions. | MUST | `check_prd_acc_19` | Unverified / — |

## 6.8 — Translation

Source: Detailed Spec §6.8. Planned component: Core variant services; Translator and Translation Reviewer surfaces; guarded Layer 2 channel.

Target: M4. Verification owners: Assessment owner; Accessibility lead; QA.

Verification: Preserve locked structure and the primary reference; reject mismatches without a valid exception; independently review, check accessibility and seal every required language.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm04-trn-01"></a>ASM04-TRN-01<br>v4: QST04-TRN-01 | Sealing the primary version creates one question or artefact per required language. | MUST | `check_asm04_trn_01` | Unverified / — |
| <a id="req-asm04-trn-02"></a>ASM04-TRN-02<br>v4: QST04-TRN-02 | Translators edit only target-language fields, besides a read-only primary reference and the supplied glossary. | MUST | `check_asm04_trn_02` | Unverified / — |
| <a id="req-asm04-trn-03"></a>ASM04-TRN-03<br>v4: QST04-TRN-03 | Option mapping, correct-answer semantics, marks, assets, equations and structural identifiers are locked and machine-verified on submission. | MUST | `check_asm04_trn_03` | Unverified / — |
| <a id="req-asm04-trn-04"></a>ASM04-TRN-04<br>v4: QST04-TRN-04 | Each language variant is reviewed independently for fidelity, terminology, script-specific grammar and answer equivalence. | MUST | `check_asm04_trn_04` | Unverified / — |
| <a id="req-asm04-trn-05"></a>ASM04-TRN-05<br>v4: QST04-TRN-05 | Each language variant receives its own accessibility check and its own sealed artefact. | MUST | `check_asm04_trn_05` | Unverified / — |
| <a id="req-asm04-trn-06"></a>ASM04-TRN-06<br>v4: QST04-TRN-06 | Deterministic checks run on submission and block it where the variant diverges structurally from the primary: option count and mapping, correct-answer position, marks, asset set, canonical equation set, and every numeric value, unit and symbol. | MUST | `check_asm04_trn_06` | Unverified / — |
| <a id="req-asm04-trn-07"></a>ASM04-TRN-07<br>v4: QST04-TRN-07 | The reviewer records an explicit judgement that the variant is neither easier nor harder than the primary, inside the existing mandatory checklist. No separate workflow step and no additional lifecycle state is introduced. | MUST | `check_asm04_trn_07` | Unverified / — |
| <a id="req-asm04-trn-08"></a>ASM04-TRN-08<br>v4: QST04-TRN-08 | A blocked structural check can be overridden only by a recorded exception carrying justification and an expiry date, consistent with ASR-04. The override is audited. | MUST | `check_asm04_trn_08` | Unverified / — |
| <a id="req-asm04-trn-09"></a>ASM04-TRN-09<br>v4: QST04-TRN-09 | When the primary changes, dependent variants are marked as requiring revalidation and the translator is shown what changed. | MUST | `check_asm04_trn_09` | Unverified / — |
| <a id="req-asm04-trn-10"></a>ASM04-TRN-10<br>v4: QST04-TRN-10 | Coordinators see language status and artefact ownership, never sealed content. | MUST | `check_asm04_trn_10` | Unverified / — |
| <a id="req-prd-trn-11"></a>PRD-TRN-11 | GAP Variant creation is part of the primary's sealing transaction. For each required language a new lineage and Draft are created with: empty target-language stem, option bodies, explanation and alternative text; locked fields copied from the primary (option identifiers and order, correct flag, marks, assets by checksum, canonical equations, classification); primary_reference_hash; and a read-only primary reference snapshot holding the primary's rendering and canonical text, classified Restricted and visible only to the assigned translator and translation reviewer. A translation assignment is created by policy. The snapshot is purged when the variant is sealed. | MUST | `check_prd_trn_11` | Unverified / — |
| <a id="req-prd-trn-12"></a>PRD-TRN-12 | GAP D-23 The translation editor exposes only translatable text: stem, option bodies, explanation, alternative text, table cell text and captions. Numbers, units, symbols, equations and image references appear as locked tokens that cannot be edited or removed. Proposed default: numeric values are preserved verbatim (no localized numerals); an exception is the only route to change one. | MUST | `check_prd_trn_12` | Unverified / — |
| <a id="req-prd-trn-13"></a>PRD-TRN-13 | GAP Structural check catalogue (TRN-06), each blocking and named in the response: STR-01 option count equal; STR-02 option identifier set and order equal; STR-03 correct-answer position equal; STR-04 marks equal; STR-05 asset set by checksum equal; STR-06 canonical equation multiset equal; STR-07 numeric value multiset equal (numbers including decimals, negatives and percentages, extracted by a fixed grammar); STR-08 unit multiset equal (from a maintained unit lexicon); STR-09 symbol multiset equal (non-alphabetic Unicode symbols from a fixed set); STR-10 table dimensions equal; STR-11 every primary image has alternative text in the variant unless decorative. | MUST | `check_prd_trn_13` | Unverified / — |
| <a id="req-prd-trn-14"></a>PRD-TRN-14 | GAP D-15 Exception record: identifier; version identifier; check codes covered; justification (at least 50 characters); requested by; approved by (a Coordinator, re-authenticated, different from the requester); created at; expires at (at most the configured maximum, proposed 30 days); status Active, Expired, Revoked or Consumed; audit references. Only an Active exception matching the failing check code permits the submission; the exception identifier is recorded on the decision and in the manifest. An hourly sweep expires exceptions. An attempted override without a valid exception returns EXCEPTION_REQUIRED. | MUST | `check_prd_trn_14` | Unverified / — |
| <a id="req-prd-trn-15"></a>PRD-TRN-15 | GAP The translation-review checklist (inside the standard review template) covers fidelity of meaning, glossary terminology, script-specific grammar, answer equivalence (the same option is correct for the same reasons), and the equivalence judgement E1 of §6.6. The reviewer sees the primary reference and the variant side by side, read-only. | MUST | `check_prd_trn_15` | Unverified / — |
| <a id="req-prd-trn-16"></a>PRD-TRN-16 | GAP Revalidation (TRN-09, RES06-COR-03): when a corrected primary is sealed, each variant lineage is flagged requires_revalidation and a revalidate_variant task is created. Its workspace shows a field-level difference between the previous and new primary reference. The translator produces a new variant version bound to the new primary hash; it passes every gate; readiness returns only when every required language is resealed against the new primary. | MUST | `check_prd_trn_16` | Unverified / — |
| <a id="req-prd-trn-17"></a>PRD-TRN-17 | GAP The coordinator's language status view lists, per artefact, each language's state, current assignee and age. It shows names for assignment purposes but never content, never the correct answer, and never a rendering. | MUST | `check_prd_trn_17` | Unverified / — |

## 6.9 — Sealing and vault

Source: Detailed Spec §6.9. Planned component: Protected sealing worker; kms/storage providers; manifests.

Target: M4. Verification owners: Security; QA.

Verification: Remove each prerequisite in turn and prove sealing stops; verify hashes, signatures, retention, idempotent retry, working-copy disposal and denial of routine human plaintext access.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm05-vlt-01"></a>ASM05-VLT-01<br>v4: QST05-VLT-01 | Sealing is a system action. No human role has a discretionary publish control. | MUST | `check_asm05_vlt_01` | Unverified / — |
| <a id="req-asm05-vlt-02"></a>ASM05-VLT-02<br>v4: QST05-VLT-02 | The service revalidates approvals, lineage, separation of duties, asset scans, schema and current policy before any write. | MUST | `check_asm05_vlt_02` | Unverified / — |
| <a id="req-asm05-vlt-03"></a>ASM05-VLT-03<br>v4: QST05-VLT-03 | Canonical sealing strips comments, author names, revision history, unsafe attributes, source metadata and any field outside the approved schema. | MUST | `check_asm05_vlt_03` | Unverified / — |
| <a id="req-asm05-vlt-04"></a>ASM05-VLT-04<br>v4: QST05-VLT-04 | The service produces a SHA-256-or-stronger content hash, encrypts using managed keys, and signs a manifest without persisting raw key material. | MUST | `check_asm05_vlt_04` | Unverified / — |
| <a id="req-asm05-vlt-05"></a>ASM05-VLT-05<br>v4: QST05-VLT-05 | On sealing, the artefact is removed from the authoring, review and accessibility environments and indexed in the question bank by classification, complexity level, difficulty and taxonomy level. | MUST | `check_asm05_vlt_05` | Unverified / — |
| <a id="req-asm05-vlt-06"></a>ASM05-VLT-06<br>v4: QST05-VLT-06 | Sealing atomically writes the artefact, indexes approved metadata, emits durable audit, and ends routine human access. | MUST | `check_asm05_vlt_06` | Unverified / — |
| <a id="req-asm05-vlt-07"></a>ASM05-VLT-07<br>v4: QST05-VLT-07 | Sealing is idempotent and safely retryable. A failure leaves no partially sealed artefact. | MUST | `check_asm05_vlt_07` | Unverified / — |
| <a id="req-asm05-vlt-08"></a>ASM05-VLT-08<br>v4: QST05-VLT-08 | Sealed artefacts are immutable and remain encrypted at rest with no plaintext copy accessible to any user or administrator. Which version is current is always resolvable. | MUST | `check_asm05_vlt_08` | Unverified / — |
| <a id="req-prd-vlt-09"></a>PRD-VLT-09 | GAP The sealing pipeline runs the steps below, in order, in a worker under the sealing workload identity (ARC-05), keyed by the version identifier as its idempotency key. | MUST | `check_prd_vlt_09` | Unverified / — |
| <a id="req-prd-vlt-10"></a>PRD-VLT-10 | GAP Manifest content is specified in §8.6. A manifest is Restricted (DAT-01), stored beside the sealed object and in the database, and its canonical bytes are signed with an asymmetric key held in the key management service. | MUST | `check_prd_vlt_10` | Unverified / — |
| <a id="req-prd-vlt-11"></a>PRD-VLT-11 | GAP Encryption model: envelope encryption with a fresh 256-bit data key per sealed version (authenticated encryption), the data key wrapped by the active repository-tier key in the key management service. Key policy grants encrypt to the sealing identity only; decrypt to the verification identity (in-memory verification only, no plaintext output), the correction-seeding identity under a recorded authorization (§6.11), and the break-glass identity (§10.6). No human principal and no platform-administrator role holds decrypt. Every key use is logged by the key service and mirrored into audit. | MUST | `check_prd_vlt_11` | Unverified / — |
| <a id="req-prd-vlt-12"></a>PRD-VLT-12 | GAP Storage: a private object store with no public access, object versioning, retention lock with the period taken from configuration D-24 (DAT-08), provider-side encryption in addition to application-level encryption, and access only through worker identities. Object key: artefact identifier / version identifier / content hash. | MUST | `check_prd_vlt_12` | Unverified / — |
| <a id="req-prd-vlt-13"></a>PRD-VLT-13 | GAP Bank index row per sealed version: artefact and version identifiers, language, lineage, classification, complexity level, difficulty, taxonomy level, marks, content hash, similarity fingerprint, sealed at, current flag, accommodations deliverable. No content field exists in the index. | MUST | `check_prd_vlt_13` | Unverified / — |
| <a id="req-prd-vlt-14"></a>PRD-VLT-14 | GAP Post-seal removal (VLT-05): in the sealing transaction the plaintext working copy of the sealed version is deleted from the authoring-tier store and its rendering caches are purged. Returned and Withdrawn versions are not sealed; they remain immutable in the authoring tier, reachable only as findings context by the author of the successor draft and as metadata by auditors. | MUST | `check_prd_vlt_14` | Unverified / — |
| <a id="req-prd-vlt-15"></a>PRD-VLT-15 | GAP Current-version resolution (VLT-08): the artefact holds one current sealed version pointer per language; the pointer moves and the previous version becomes Superseded inside the same transaction, so a reader never observes two current versions or none. | MUST | `check_prd_vlt_15` | Unverified / — |
| <a id="req-prd-vlt-16"></a>PRD-VLT-16 | GAP Failure handling: if the key service, audit store, scanner or object store is unavailable, or any revalidation fails, the job is marked failed with a reason code, no state changes, retry uses exponential backoff up to 6 hours, an operational alert fires after the third failure, and operations can replay the job. Because the object key includes the content hash, a retry after a partial object write overwrites the same key and produces exactly one sealed object and one manifest. | MUST | `check_prd_vlt_16` | Unverified / — |
| <a id="req-prd-vlt-17"></a>PRD-VLT-17 | GAP Progress: the version shows Queued, Sealing, Sealed or Failed (retrying) to the accessibility specialist who approved it and to the coordinator; 95 % of valid image-bearing artefacts seal within 30 seconds (§11). | MUST | `check_prd_vlt_17` | Unverified / — |

## 6.10 — Readiness and handoff

Source: Detailed Spec §6.10. Planned component: Core readiness calculator; machine-only assembly API.

Target: M4. Verification owners: Assembly owner; QA; Security.

Verification: Require all language seals on one lineage; accept the correct workload audience only; return metadata without content; revoke readiness immediately on correction.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm07-rdy-01"></a>ASM07-RDY-01<br>v4: QST07-RDY-01 | An artefact is ready only when the current primary and every required language variant are sealed against the same lineage. | MUST | `check_asm07_rdy_01` | Unverified / — |
| <a id="req-asm07-rdy-02"></a>ASM07-RDY-02<br>v4: QST07-RDY-02 | A machine-only, authenticated, paginated interface exposes opaque identifiers, languages, item type, classification, difficulty, taxonomy level, marking, readiness and sealed references. | MUST | `check_asm07_rdy_02` | Unverified / — |
| <a id="req-asm07-rdy-03"></a>ASM07-RDY-03<br>v4: QST07-RDY-03 | The response contains no stem, option, answer, explanation, comment or asset bytes. | MUST | `check_asm07_rdy_03` | Unverified / — |
| <a id="req-asm07-rdy-04"></a>ASM07-RDY-04<br>v4: QST07-RDY-04 | Human tokens and wrong-audience workload tokens are rejected by the interface. | MUST | `check_asm07_rdy_04` | Unverified / — |
| <a id="req-asm07-rdy-05"></a>ASM07-RDY-05<br>v4: QST07-RDY-05 | Superseded sealed versions remain as evidence but are never returned by new readiness queries. | MUST | `check_asm07_rdy_05` | Unverified / — |
| <a id="req-asm07-rdy-06"></a>ASM07-RDY-06<br>v4: QST07-RDY-06 | Where two artefacts must not appear in the same paper, the relationship is recorded and carried on the readiness record. Automated detection of such pairs is out of scope. | SHOULD | `check_asm07_rdy_06` | Unverified / — |
| <a id="req-prd-rdy-07"></a>PRD-RDY-07 | GAP The readiness status values are FULLY_APPROVED (engineering name for ready), NOT_READY and REVOKED. The readiness record schema is fixed in §8.2 and Appendix C. It is computed by the rule in §5.4, stored, and updated inside the transaction that changes any of its inputs, so the interface reads a materialized record rather than computing on request. | MUST | `check_prd_rdy_07` | Unverified / — |
| <a id="req-prd-rdy-08"></a>PRD-RDY-08 | GAP Interface: GET /assembly/v1/readiness with filters cycle, subject, language, readiness status and updated-since, opaque cursor pagination with a page size of at most 200; GET /assembly/v1/readiness/{artefact_id}. Authentication is mutual TLS plus a short-lived token whose audience is assembly-readiness; any other audience or a human token returns REJECTED_AUDIENCE. Responses are marked no-store and rate-limited per workload identity. | MUST | `check_prd_rdy_08` | Unverified / — |
| <a id="req-prd-rdy-09"></a>PRD-RDY-09 | GAP D-34 Exclusion pairs (RDY-06): a coordinator records a pair of artefact identifiers with a reason; the pair appears on both readiness records; removal is audited. No detection logic exists. | SHOULD | `check_prd_rdy_09` | Unverified / — |
| <a id="req-prd-rdy-10"></a>PRD-RDY-10 | GAP Every change of readiness emits readiness.changed with the artefact identifier, previous and new status and the reason (sealed, correction, used, retired, revalidation). | MUST | `check_prd_rdy_10` | Unverified / — |

## 6.11 — Correction and supersession

Source: Detailed Spec §6.11. Planned component: Core correction services; seeding worker; outbox and notify provider.

Target: M4. Verification owners: Assessment owner; Assembly owner; QA.

Verification: Authorize a correction, create a new lineage, preserve old seals, revoke readiness, revalidate languages and prove delivery, acknowledgement and overdue escalation.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-res06-cor-01"></a>RES06-COR-01 | A correction to a sealed primary requires a recorded authorization and reason. | MUST | `check_res06_cor_01` | Unverified / — |
| <a id="req-res06-cor-02"></a>RES06-COR-02 | A correction creates a new lineage, never overwrites sealed bytes, and immediately revokes readiness. | MUST | `check_res06_cor_02` | Unverified / — |
| <a id="req-res06-cor-03"></a>RES06-COR-03 | Every dependent language variant is marked as requiring revalidation until resealed against the new primary. | MUST | `check_res06_cor_03` | Unverified / — |
| <a id="req-res06-cor-04"></a>RES06-COR-04 | The superseded version records a reference to the version that replaced it. | MUST | `check_res06_cor_04` | Unverified / — |
| <a id="req-res06-cor-05"></a>RES06-COR-05 | Downstream consumers are notified of supersession and must acknowledge. Unacknowledged supersession beyond a configured window raises an operational alert. | MUST | `check_res06_cor_05` | Unverified / — |
| <a id="req-res06-cor-06"></a>RES06-COR-06 | Retiring an artefact preserves its sealed hash and classification so later analysis remains possible. | SHOULD | `check_res06_cor_06` | Unverified / — |
| <a id="req-prd-cor-07"></a>PRD-COR-07 | GAP Correction authorization record: identifier, artefact identifier, sealed version identifier, scope (primary or a named variant), authorized by (Coordinator, re-authenticated), reason of at least 50 characters, created at, audit references. It emits correction.authorized. | MUST | `check_prd_cor_07` | Unverified / — |
| <a id="req-prd-cor-08"></a>PRD-COR-08 | GAP D-16 Correction draft seeding. Because no human can read sealed plaintext, the system creates the correction draft: under the authorization record, the correction-seeding identity decrypts the sealed version in memory, creates a new lineage with a Draft holding that content, and assigns it to an eligible author by policy (the original author is eligible). The sealed bytes are untouched; the draft is Restricted and visible only to the assignee; the audit event records the source version hash and the authorization identifier. This is the only routine path by which sealed content re-enters the authoring tier, and it is a system action, never a read interface. | MUST | `check_prd_cor_08` | Unverified / — |
| <a id="req-prd-cor-09"></a>PRD-COR-09 | GAP Readiness is revoked in the same transaction as the authorization (COR-02), and stays revoked until the new primary and every required variant are sealed against it. The reason is carried on readiness.changed. | MUST | `check_prd_cor_09` | Unverified / — |
| <a id="req-prd-cor-10"></a>PRD-COR-10 | GAP D-25 Supersession notification: sealing the corrected primary marks the previous version Superseded with replaced_by, and the outbox delivers artefact.superseded to every registered consumer over mutual TLS (webhook), at least once with consumer-side deduplication by event identifier. Consumers acknowledge with POST /downstream/v1/supersession-acks carrying the event identifier, consumer identifier and a signature. A notice unacknowledged beyond the configured window (proposed 24 hours) raises an operational alert and appears on the coordinator board until acknowledged. | MUST | `check_prd_cor_10` | Unverified / — |
| <a id="req-prd-cor-11"></a>PRD-COR-11 | GAP Retirement (COR-06): a re-authenticated Coordinator retires an artefact with a reason; every sealed version keeps its hash, manifest and classification; readiness is revoked; artefact.retired is emitted; there is no un-retire in the MVP. | SHOULD | `check_prd_cor_11` | Unverified / — |
| <a id="req-prd-cor-12"></a>PRD-COR-12 | GAP A correction scoped to one variant (a translation defect with a sound primary) creates a new lineage for that language only; the primary and other variants are untouched; readiness is revoked until the variant is resealed against the unchanged primary hash. | MUST | `check_prd_cor_12` | Unverified / — |

## 6.12 — Downstream lifecycle

Source: Detailed Spec §6.12. Planned component: Core lifecycle services; signed inbound notifications.

Target: M4. Verification owners: Assembly owner; QA.

Verification: Reject forged, invalid and conflicting messages; replay valid notifications idempotently; prove Used/Archived transitions and archive key handling.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asm06-lfc-01"></a>ASM06-LFC-01<br>v4: QST06-LFC-01 | The system accepts a signed selection notification from the assembly service and atomically transitions the primary and every published language variant of the selected artefact to Used. No human actor initiates the transition. | MUST | `check_asm06_lfc_01` | Unverified / — |
| <a id="req-asm06-lfc-02"></a>ASM06-LFC-02<br>v4: QST06-LFC-02 | A Used artefact is immutable and is excluded from every subsequent readiness query. One that was not selected remains available in the eligible pool. | MUST | `check_asm06_lfc_02` | Unverified / — |
| <a id="req-asm06-lfc-03"></a>ASM06-LFC-03<br>v4: QST06-LFC-03 | On the exam-completion event, every Used artefact in that session transitions atomically to Archived. There is no return path to Published or Used. | MUST | `check_asm06_lfc_03` | Unverified / — |
| <a id="req-asm06-lfc-04"></a>ASM06-LFC-04<br>v4: QST06-LFC-04 | Archival writes the exam identifier, the archival timestamp and the artefact-set hash to the audit chain, so a session can be reconstructed evidentially. | MUST | `check_asm06_lfc_04` | Unverified / — |
| <a id="req-asm06-lfc-05"></a>ASM06-LFC-05<br>v4: QST06-LFC-05 | Read access to an Archived artefact is limited to audit and dispute roles under the break-glass procedure in §10.6. | MUST | `check_asm06_lfc_05` | Unverified / — |
| <a id="req-asm06-lfc-06"></a>ASM06-LFC-06<br>v4: QST06-LFC-06 | Encryption keys rotate from the active tier to the archive tier on archival, and the rotation is recorded. | MUST | `check_asm06_lfc_06` | Unverified / — |
| <a id="req-prd-lfc-07"></a>PRD-LFC-07 | GAP D-26 Selection notification contract: POST /downstream/v1/selection-notifications with body notification identifier, exam session identifier, cycle code, list of selected artefact identifiers with the expected current primary version identifier, and issued-at; a detached signature (JSON Web Signature by the assembly signing key, key identifier included) plus mutual TLS and an audience token. Validation: signature valid against the registered key set; issued-at within 5 minutes of clock skew; notification identifier unused (a replay returns the original result); every artefact ready and its current primary matching the expected version. Proposed default: all-or-nothing per notification — any artefact not ready rejects the whole notification with SELECTION_NOT_READY listing the identifiers. On success one transaction sets the primary and every sealed variant to Used, records the exam session, writes audit events and emits artefact.used. | MUST | `check_prd_lfc_07` | Unverified / — |
| <a id="req-prd-lfc-08"></a>PRD-LFC-08 | GAP Exam-completion contract: POST /downstream/v1/exam-completions with exam session identifier and completed-at, signed as above. In one transaction every Used artefact of that session becomes Archived and the audit chain receives an event carrying the exam identifier, the timestamp and the artefact-set hash (SHA-256 over the sorted list of sealed content hashes). A key-rotation job then re-wraps each data key with the archive-tier key and records the rotation; until it completes the artefact is Archived with rotation pending, visible to operations. | MUST | `check_prd_lfc_08` | Unverified / — |
| <a id="req-prd-lfc-09"></a>PRD-LFC-09 | GAP Archived metadata (identifiers, hashes, classification, manifests) remains readable to auditors through the evidence view; content is reachable only through the break-glass procedure. | MUST | `check_prd_lfc_09` | Unverified / — |
| <a id="req-prd-lfc-10"></a>PRD-LFC-10 | GAP A selection notification naming an artefact that is Used, Archived, Retired or under correction is rejected with a code naming the artefact and its state, and raises an operational alert, because it indicates a stale assembly view. | MUST | `check_prd_lfc_10` | Unverified / — |

## 6.13 — Expected evidence and audit

Source: Detailed Spec §6.13. Planned component: Core audit store, verifier, expected-evidence assertions and evidence view.

Target: M1/M3. Verification owners: QA; Security; Operations.

Verification: Detect altered and removed records, prove state/event atomicity and content-freedom, block missing evidence, verify again after restore and sign the evidence results.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asr01-evd-01"></a>ASR01-EVD-01 | Every material action emits an append-only audit event: actor or service, action, subject and hash, outcome, policy version and correlation identifier. | MUST | `check_asr01_evd_01` | Unverified / — |
| <a id="req-asr01-evd-02"></a>ASR01-EVD-02 | Events are hash-chained. The chain construction, genesis record and verification procedure are specified and implemented. | MUST | `check_asr01_evd_02` | Partial / [E1](delivery-status.md) |
| <a id="req-asr01-evd-03"></a>ASR01-EVD-03 | Chain verification is runnable on demand and detects any removed or altered event. | MUST | `check_asr01_evd_03` | Partial / [E1](delivery-status.md) |
| <a id="req-asr01-evd-04"></a>ASR01-EVD-04 | Verification succeeds across backup and restore — restored records retain valid event and content hashes. | MUST | `check_asr01_evd_04` | Unverified / — |
| <a id="req-asr01-evd-05"></a>ASR01-EVD-05 | Each step declares the evidence it must produce. Before sealing, the system asserts that every expected record exists, verifies against the exact version hash, and was produced by an actor with no separation-of-duties conflict. | MUST | `check_asr01_evd_05` | Unverified / — |
| <a id="req-asr01-evd-06"></a>ASR01-EVD-06 | A missing, unbound or mismatched record blocks sealing and raises an alert naming the step and the absent record. Absence of expected evidence is an alert condition, not a silent pass. | MUST | `check_asr01_evd_06` | Unverified / — |
| <a id="req-asr01-evd-07"></a>ASR01-EVD-07 | Critical transitions fail closed when durable audit is unavailable. | MUST | `check_asr01_evd_07` | Unverified / — |
| <a id="req-asr01-evd-08"></a>ASR01-EVD-08 | An evidence view provides read-only audit search by actor, action, artefact and time range, and displays the verification result. (P1 — may reduce to a scripted operator procedure if Week 3 capacity is strained.) | SHOULD | `check_asr01_evd_08` | Unverified / — |
| <a id="req-asr01-evd-09"></a>ASR01-EVD-09 | Audit events contain no artefact plaintext. | MUST | `check_asr01_evd_09` | Partial / [E1](delivery-status.md) |
| <a id="req-asr01-evd-10"></a>ASR01-EVD-10 | A scheduled sweep re-asserts evidence completeness across sealed versions and alerts on drift. | SHOULD | `check_asr01_evd_10` | Unverified / — |
| <a id="req-prd-evd-11"></a>PRD-EVD-11 | GAP Audit event schema (§8.2, Appendix C): event identifier; chain identifier; sequence number; occurred at; actor (type user or service; audit identifier or workload identity); action from the catalogue; subject (type, identifier, version hash where applicable); outcome (success, denied, failed); policy version; correlation and trace identifiers; details as a structured object whose keys are allowlisted per action; previous hash; event hash. The schema forbids additional properties. | MUST | `check_prd_evd_11` | Unverified / — |
| <a id="req-prd-evd-12"></a>PRD-EVD-12 | GAP Action catalogue (minimum): session.signed_in, session.denied, session.signed_out, session.timed_out, cycle.created, cycle.changed, taxonomy.published, taxonomy.node_retired, capability.created, capability.revoked, capability.expired, assignment.created, assignment.released, assignment.expired, assignment.reassigned, artefact.created, draft.saved (aggregated per minute, count only), asset.uploaded, asset.quarantined, asset.rejected, asset.cleared, draft.withdrawn, version.submitted, validation.failed, review.opened, review.decided, accessibility.decided, translation_review.decided, exception.requested, exception.approved, exception.revoked, exception.expired, exception.consumed, sealing.started, sealing.failed, version.sealed, variant.created, readiness.changed, correction.authorized, correction.seeded, artefact.superseded, supersession.acknowledged, supersession.overdue, artefact.retired, artefact.used, artefact.archived, key.rotated, policy.denied, security.event, integrity.signal, integrity.referred, chain.checkpoint, chain.verified, evidence.sweep, breakglass.accessed. | MUST | `check_prd_evd_12` | Unverified / — |
| <a id="req-prd-evd-13"></a>PRD-EVD-13 | GAP D-02 Chain construction: the event body (every field except event_hash) is serialized with the canonical JSON rule of §8.4; event_hash = SHA-256 of the previous hash concatenated with the body bytes. The genesis record has sequence 0, a previous hash of 32 zero bytes, and carries chain identifier, creation time, schema version and environment; it is signed through the key service. Sequence numbers are strictly increasing and unique by database constraint; a single writer per chain takes a row lock on the chain head. Every 10,000 events or every hour, whichever is first, a checkpoint records the sequence and head hash, signed through the key service, and is exported to the monitoring platform as an external anchor so a store-wide rewrite is detectable. | MUST | `check_prd_evd_13` | Unverified / — |
| <a id="req-prd-evd-14"></a>PRD-EVD-14 | GAP Verification procedure: inputs are chain identifier and an optional sequence range (default: from the last verified checkpoint, or from genesis); the verifier walks events in sequence order, checks contiguity, recomputes each hash, compares with the stored hash and with the following event's previous hash, and verifies every checkpoint signature and the external anchor. Output: events verified, first failing sequence, failure kind (missing, altered, reordered, bad checkpoint), start and finish times. It runs on demand from the evidence view or an operator command, and daily on schedule. The result is itself written as chain.verified; a failure raises a Critical alert and invokes the runbook. | MUST | `check_prd_evd_14` | Unverified / — |
| <a id="req-prd-evd-15"></a>PRD-EVD-15 | GAP Throughput: the chain writer must sustain at least 200 events per second, because telemetry signals are mirrored into the chain (§6.14) at up to 100 per second across 50 sessions. This is measured in Week 1 before any feature is built on it. | MUST | `check_prd_evd_15` | Unverified / — |
| <a id="req-prd-evd-16"></a>PRD-EVD-16 | GAP The expected-evidence model (table below) is declarative configuration versioned with the policy, so a new step or record can be added without code. The completeness assertion at sealing evaluates it and names the step and record on failure (EVD-05, EVD-06). | MUST | `check_prd_evd_16` | Unverified / — |
| <a id="req-prd-evd-17"></a>PRD-EVD-17 | GAP D-27 Evidence view (EVD-08): read-only search by actor audit identifier, action, artefact or version identifier and time range; event detail with no content; the latest verification result and checkpoint; a "verify now" control for auditors. If reduced to a scripted procedure, the script must produce the same search and verification output to a file readable by the auditor. | SHOULD | `check_prd_evd_17` | Unverified / — |
| <a id="req-prd-evd-18"></a>PRD-EVD-18 | GAP Content ban enforcement (EVD-09): the event schema allowlists detail keys per action; an automated test writes events for every action with Restricted strings in every free field and asserts none is persisted; a log scrubber for known content field names is a second line of defence, never the first. | MUST | `check_prd_evd_18` | Unverified / — |
| <a id="req-prd-evd-19"></a>PRD-EVD-19 | GAP D-35 Daily sweep (EVD-10) re-runs the completeness assertion for every sealed version and alerts on any drift with the version identifier and the absent record. | SHOULD | `check_prd_evd_19` | Unverified / — |

## 6.14 — Session integrity

Source: Detailed Spec §6.14. Planned component: Core sessions, durable integrity ingest and operator surface; content client.

Target: M1/M3. Verification owners: Integrity Operator; Security; QA.

Verification: Authenticate session ownership, capture and block named actions where possible, score by ratified policy, refer at threshold, and prove retry/recovery without silent loss or content leakage.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-asr02-obs-01"></a>ASR02-OBS-01 | Every authoring, review, accessibility and translation session is registered, heartbeated, and closed on sign-out or timeout. | MUST | `check_asr02_obs_01` | Partial / [E2](delivery-status.md) |
| <a id="req-asr02-obs-02"></a>ASR02-OBS-02 | The client captures and reports: copy, cut, paste, context menu, print, screenshot key combinations, developer tools opened, viewport anomaly consistent with a docked inspector, window or tab focus loss, page visibility change, concurrent-tab detection, and heartbeat gap. | MUST | `check_asr02_obs_02` | Unverified / — |
| <a id="req-asr02-obs-03"></a>ASR02-OBS-03 | Each captured action is blocked where technically possible and reported whether or not blocking succeeded. | MUST | `check_asr02_obs_03` | Unverified / — |
| <a id="req-asr02-obs-04"></a>ASR02-OBS-04 | The user receives immediate non-blocking feedback that the action was blocked and recorded. Feedback must not interrupt typing. | MUST | `check_asr02_obs_04` | Unverified / — |
| <a id="req-asr02-obs-05"></a>ASR02-OBS-05 | Ingest failure retries; events are never silently discarded. Durability outranks latency. | MUST | `check_asr02_obs_05` | Unverified / — |
| <a id="req-asr02-obs-06"></a>ASR02-OBS-06 | Each session carries an integrity score starting at 100, decremented per signal by a ratified severity table, floored at 0, and non-recovering within a session. | MUST | `check_asr02_obs_06` | Partial / [E2](delivery-status.md) |
| <a id="req-asr02-obs-07"></a>ASR02-OBS-07 | Signals are classified at least as warning or critical; critical signals are visually and audibly distinct. | MUST | `check_asr02_obs_07` | Unverified / — |
| <a id="req-asr02-obs-08"></a>ASR02-OBS-08 | Crossing the configured threshold refers the session — a security event to the monitoring platform and a persistent alert to the operator. | MUST | `check_asr02_obs_08` | Unverified / — |
| <a id="req-asr02-obs-09"></a>ASR02-OBS-09 | Repeat breaches update the existing alert rather than stacking duplicates. | MUST | `check_asr02_obs_09` | Unverified / — |
| <a id="req-asr02-obs-10"></a>ASR02-OBS-10 | Automatic session suspension defaults to off. Enabling it is an explicit operational decision, not a build default. | MUST | `check_asr02_obs_10` | Unverified / — |
| <a id="req-asr02-obs-11"></a>ASR02-OBS-11 | The operator surface shows all active sessions with role, subject, artefact state, integrity score and time since last heartbeat. | MUST | `check_asr02_obs_11` | Unverified / — |
| <a id="req-asr02-obs-12"></a>ASR02-OBS-12 | A rolling feed presents newest-first events across all sessions, with severity and pseudonymous actor identifier. | MUST | `check_asr02_obs_12` | Unverified / — |
| <a id="req-asr02-obs-13"></a>ASR02-OBS-13 | A per-session drill-down shows the full ordered event history and score progression. | MUST | `check_asr02_obs_13` | Unverified / — |
| <a id="req-asr02-obs-14"></a>ASR02-OBS-14 | The surface updates by server push, not manual reload, and displays a reconnecting state with backoff on transport loss. | MUST | `check_asr02_obs_14` | Unverified / — |
| <a id="req-asr02-obs-15"></a>ASR02-OBS-15 | On reconnect the surface re-synchronizes session state, so no live session is missing or stale. | MUST | `check_asr02_obs_15` | Unverified / — |
| <a id="req-asr02-obs-16"></a>ASR02-OBS-16 | A monitoring event carries only event type, timestamp, session identifier, pseudonymous actor audit identifier and task reference. No stem, option, field value, clipboard payload or screenshot. | MUST | `check_asr02_obs_16` | Unverified / — |
| <a id="req-asr02-obs-17"></a>ASR02-OBS-17 | OBS-16 is enforced by an automated test that fails the build — not by reviewer discipline. | MUST | `check_asr02_obs_17` | Unverified / — |
| <a id="req-asr02-obs-18"></a>ASR02-OBS-18 | The operator role can reach no artefact content through any interface. | MUST | `check_asr02_obs_18` | Unverified / — |
| <a id="req-prd-obs-19"></a>PRD-OBS-19 | GAP Session record: session identifier; actor audit identifier; role; current task reference (assignment identifier, opaque); started at; last heartbeat at; ended at with reason (sign-out, inactivity, absolute maximum, suspension, revocation); integrity score; signal counts by kind; referred flag and alert identifier. The client heartbeats every 30 seconds; a session is flagged stale at 90 seconds without one (§11). | MUST | `check_prd_obs_19` | Unverified / — |
| <a id="req-prd-obs-20"></a>PRD-OBS-20 | GAP D-03 The signal catalogue below, with proposed default severities and decrements, is the ratified severity table once signed by the Integrity Operator and Security. It is configuration with a version recorded on every integrity event. | MUST | `check_prd_obs_20` | Unverified / — |
| <a id="req-prd-obs-21"></a>PRD-OBS-21 | GAP Telemetry event schema (Appendix C): event identifier, event type, severity, occurred at, session identifier, actor audit identifier, task reference, client sequence number, blocked flag, score after. The JSON schema forbids additional properties, and the build-failing test (OBS-17) submits events carrying content-like fields and asserts they are rejected, then inspects every persisted and forwarded event for the absence of any string from the synthetic corpus. | MUST | `check_prd_obs_21` | Unverified / — |
| <a id="req-prd-obs-22"></a>PRD-OBS-22 | GAP Client capture mechanics: copy, cut and paste listeners that prevent the default action and report; a context-menu listener that prevents and reports; key listeners for print and platform screenshot combinations that prevent where the browser allows and always report; developer-tools detection by viewport-delta and timing heuristics reported as viewport anomaly and, when confirmed, developer tools opened; visibility-change and blur listeners; concurrent-tab detection through a same-origin channel; heartbeat gap computed server-side. The capture library is loaded before the editor and the editor does not initialize without it. | MUST | `check_prd_obs_22` | Unverified / — |
| <a id="req-prd-obs-23"></a>PRD-OBS-23 | GAP D-33 Ingest: the client queues events in memory with client sequence numbers and posts batches of at most 50 to the telemetry endpoint; the server persists before acknowledging by event identifier; unacknowledged events retry with exponential backoff and jitter without ever blocking input; ordering is restored server-side by client sequence. Capacity: 50 sessions at 2 events per second sustained, bursts to 10 per second per session. | MUST | `check_prd_obs_23` | Unverified / — |
| <a id="req-prd-obs-24"></a>PRD-OBS-24 | GAP Scoring is computed server-side on ingest: score = max(0, 100 − sum of decrements), never recovering within the session; each event stores the score after it; duplicate event identifiers are ignored. | MUST | `check_prd_obs_24` | Unverified / — |
| <a id="req-prd-obs-25"></a>PRD-OBS-25 | GAP D-04 Referral: when the score first reaches or falls below the threshold (proposed 50), the system sends a security event to the monitoring platform carrying session identifier, actor audit identifier, score and the counts of the top signals, and creates one persistent alert on the operator surface. Every later signal in that session updates the same alert. Automatic suspension, when enabled by configuration D-22, ends the session, releases its assignment with reason and records both; it is off by default. | MUST | `check_prd_obs_25` | Unverified / — |
| <a id="req-prd-obs-26"></a>PRD-OBS-26 | GAP Operator surface transport: a server-push channel (server-sent events or a web socket) carrying session snapshots and events; reconnection with exponential backoff from 1 second to a 30-second cap with jitter; on reconnect the client sends its last event identifier and the server replies with a full session snapshot plus every missed event. Signal to surface p95 ≤ 3 seconds; signal to durable audit p95 ≤ 5 seconds. | MUST | `check_prd_obs_26` | Unverified / — |
| <a id="req-prd-obs-27"></a>PRD-OBS-27 | GAP The operator's authorization scope contains no content endpoint at all; the operator API's response schemas are tested for the absence of content field names, and the operator UI is served without the editor or renderer bundles. | MUST | `check_prd_obs_27` | Unverified / — |
| <a id="req-prd-obs-28"></a>PRD-OBS-28 | GAP Application observability (§11): structured logs with correlation and trace identifiers and no content; metrics for active sessions, events per second, telemetry backlog, sealing duration and failure count, chain write latency and lag, outbox lag, assignment pool size; dashboards contain no content. | MUST | `check_prd_obs_28` | Unverified / — |

## 6.15 — Notifications

Source: Detailed Spec §6.15. Planned component: Core notifications and alerts; role surfaces.

Target: M1–M4. Verification owners: Content Operations; QA.

Verification: Deliver each specified assignment, rejection, failure and escalation notice with deduplication and safe recovery; inspect all fields for content leakage.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-prd-ntf-01"></a>PRD-NTF-01 | In-app notifications exist for: new assignment; task returned with findings; task approaching expiry (24 hours before); exception approved, revoked or expired; correction authorized (coordinator); equivalent-route escalation (coordinator); sealing failure (coordinator and operations); supersession unacknowledged (operations); assignment pool empty (coordinator). | MUST | `check_prd_ntf_01` | Unverified / — |
| <a id="req-prd-ntf-02"></a>PRD-NTF-02 | No notification in any channel contains artefact content, a correct answer, or a rendering. Out-of-band channels D-19 carry only the task type and a link. | MUST | `check_prd_ntf_02` | Unverified / — |
| <a id="req-prd-ntf-03"></a>PRD-NTF-03 | Alerts to the monitoring platform: security events (authorization denial outside assignment, device posture failure, not provisioned, threshold referral, malicious upload, hash mismatch) and operational alerts (sealing failure after retries, chain verification failure, expected evidence missing, supersession unacknowledged, telemetry backlog beyond 60 seconds, unassigned task beyond the delay). Each carries identifiers, codes and counts only. | MUST | `check_prd_ntf_03` | Unverified / — |

## 7.1 — Interfaces

Source: Detailed Spec §7.1. Planned component: Core API and event schemas; versioned client/server contract.

Target: M1–M4. Verification owners: Technical Lead; Security; QA.

Verification: Check machine-readable schemas, error/refusal behaviour, idempotency, concurrency, version compatibility, authentication and absence of Restricted content from forbidden responses.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-int-01"></a>INT-01 | All interfaces are versioned and published as a machine-readable definition kept current with the implementation. | MUST | `check_int_01` | Unverified / — |
| <a id="req-int-02"></a>INT-02 | Interactive calls carry a bearer token from the enterprise identity provider. Service-to-service calls use mutual TLS and audience-restricted short-lived workload tokens. | MUST | `check_int_02` | Unverified / — |
| <a id="req-int-03"></a>INT-03 | Retryable mutations accept an idempotency key and are safe to repeat. | MUST | `check_int_03` | Unverified / — |
| <a id="req-int-04"></a>INT-04 | Draft updates require and return an optimistic-concurrency token; stale writes are rejected. | MUST | `check_int_04` | Unverified / — |
| <a id="req-int-05"></a>INT-05 | Errors return a stable machine-readable code, a safe message, a correlation identifier, field-level detail and retry ability — never echoing Restricted content. | MUST | `check_int_05` | Unverified / — |
| <a id="req-int-06"></a>INT-06 | Listing uses opaque cursors. Unrestricted bulk exports are prohibited. | MUST | `check_int_06` | Unverified / — |
| <a id="req-int-07"></a>INT-07 | Timestamps are UTC and identifiers are opaque. | MUST | `check_int_07` | Unverified / — |
| <a id="req-int-08"></a>INT-08 | Rate limits vary by user, workload identity, endpoint sensitivity and source zone. | MUST | `check_int_08` | Unverified / — |
| <a id="req-int-09"></a>INT-09 | A role-by-operation permission matrix is authored, implemented, and used as the test oracle for authorization. | MUST | `check_int_09` | Unverified / — |
| <a id="req-int-10"></a>INT-10 | Domain events are published for creation, submission, review decision, accessibility decision, readiness change, sealing, supersession and policy denial. Events defined must have a producer. | MUST | `check_int_10` | Unverified / — |
| <a id="req-prd-int-11"></a>PRD-INT-11 | GAP Conventions: JSON request and response bodies; base path /api/v1 for interactive surfaces, /assembly/v1, /downstream/v1, /telemetry/v1, /operator/v1 and /evidence/v1 for their audiences; identifiers are ULIDs; timestamps are RFC 3339 in UTC; idempotency key in the Idempotency-Key header for every POST that creates or transitions, retained 24 hours; concurrency token via ETag and If-Match on drafts; cursor pagination returns items and next_cursor with a maximum page size of 200; every response carries Cache-Control: no-store and the correlation identifier. | MUST | `check_prd_int_11` | Unverified / — |
| <a id="req-prd-int-12"></a>PRD-INT-12 | GAP Rate-limit classes (INT-08): interactive content endpoints 60 requests per minute per user; autosave 30 per minute per draft; telemetry 600 events per minute per session; assembly readiness 600 per minute per workload identity; downstream notifications 60 per minute; sign-in 10 per minute per source. Limits are configuration; exceeding one returns RATE_LIMITED with a retry-after value. | MUST | `check_prd_int_12` | Unverified / — |
| <a id="req-prd-int-13"></a>PRD-INT-13 | GAP Machine-interface security: mutual TLS with certificates from the enterprise authority; tokens with audience, issuer, expiry ≤ 5 minutes and a key identifier resolved through a published key set; signed notifications use a detached JSON Web Signature with replay protection by notification identifier and a 5-minute clock-skew window; key rotation is supported without downtime. | MUST | `check_prd_int_13` | Unverified / — |
| <a id="req-prd-int-14"></a>PRD-INT-14 | GAP Content responses (draft, version, render, asset) are authorized per request with a short-lived scope and are non-cacheable (DAT-04); asset bytes are served through an authorized endpoint with a 60-second signed reference, never a stable public URL. | MUST | `check_prd_int_14` | Unverified / — |

## 8.1 — Data

Source: Detailed Spec §8.1. Planned component: Core entities, migrations, canonicalization, manifests and protected storage.

Target: M1–M4. Verification owners: Technical Lead; Security; QA.

Verification: Verify each data constraint and index, classification and retention, byte stability and manifest coverage, reversible deployment procedures and encrypted restore.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-dat-01"></a>DAT-01 | Artefact text, answers, explanations, assets, review comments and manifests are classified Restricted. | MUST | `check_dat_01` | Unverified / — |
| <a id="req-dat-02"></a>DAT-02 | Business records reference stable pseudonymous workforce audit identifiers; the identity provider remains the identity authority. | MUST | `check_dat_02` | Unverified / — |
| <a id="req-dat-03"></a>DAT-03 | Plaintext content never appears in URLs, analytics, traces, exception messages, infrastructure logs, browser storage, notifications, dashboards or support tickets. | MUST | `check_dat_03` | Unverified / — |
| <a id="req-dat-04"></a>DAT-04 | Content responses use short-lived authorization and are marked non-cacheable. | MUST | `check_dat_04` | Unverified / — |
| <a id="req-dat-05"></a>DAT-05 | Canonicalization is specified once — Unicode normalization, whitespace, attribute order, option order, numeric representation and asset-hash inclusion — and is bit-stable across repeat serialization and restore. Every hash depends on it. | MUST | `check_dat_05` | Unverified / — |
| <a id="req-dat-06"></a>DAT-06 | The canonical schema is versioned, and a stated migration approach preserves verifiability of already-sealed artefacts. | MUST | `check_dat_06` | Unverified / — |
| <a id="req-dat-07"></a>DAT-07 | Artefacts are encrypted in storage and in transit. | MUST | `check_dat_07` | Unverified / — |
| <a id="req-dat-08"></a>DAT-08 | Retention locks are implemented with the period as configuration. No default period is invented. | MUST | `check_dat_08` | Unverified / — |
| <a id="req-prd-dat-09"></a>PRD-DAT-09 | GAP Data lives in three stores with distinct identities: the working store (relational; drafts, versions, decisions, assignments, configuration, sessions), the repository (sealed objects, manifests, bank index; separate credentials and network segment, ARC-11), and the audit store (append-only chain, checkpoints, integrity events). The pseudonym mapping table is in a fourth, most restricted schema. | MUST | `check_prd_dat_09` | Unverified / — |
| <a id="req-prd-dat-10"></a>PRD-DAT-10 | GAP Every table carrying Restricted fields is enumerated in a data-classification register checked into the repository; log scrubbing, backup access separation and the no-content tests are generated from that register. | MUST | `check_prd_dat_10` | Unverified / — |

## 9.2 — Role screens

Source: Detailed Spec §9.2. Planned component: Signed content client; configuration and content-free oversight web surfaces (R1 decided).

Target: M2/M3. Verification owners: Product; Accessibility lead; QA.

Verification: For every role test permitted and forbidden operations, loading/empty/error/success states, resume and re-authentication, keyboard and screen-reader operation.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-ui-01"></a>UI-01 | Sign-in — enterprise identity redirect only. No password form is built. On return, the user lands on their role's default surface. | MUST | `check_ui_01` | Unverified / — |
| <a id="req-ui-04"></a>UI-04 | Authoring — hardened editor for stem, options, correct answer, explanation and classification, with the hardened region visually marked; live validation findings; preview; submit. | MUST | `check_ui_04` | Unverified / — |
| <a id="req-ui-05"></a>UI-05 | Authoring — a session integrity panel shows the current score, signal counts and a recent-event list, so the author knows exactly what is recorded. | MUST | `check_ui_05` | Unverified / — |
| <a id="req-ui-06"></a>UI-06 | Review — read-only version, hash, permitted metadata, mandatory checklist, rationale entry, approve and return. Correct-answer visibility per policy. | MUST | `check_ui_06` | Unverified / — |
| <a id="req-ui-07"></a>UI-07 | Review — the worklist locks to the open task until a decision is recorded, then advances. | MUST | `check_ui_07` | Unverified / — |
| <a id="req-ui-08"></a>UI-08 | Accessibility Check — rendered artefact with keyboard and screen-reader affordances, structured findings capture, accommodation capability capture, approve and return. In the converged model this is the Accessibility Reviewer's screen. | MUST | `check_ui_08` | Unverified / — |
| <a id="req-prd-ui-08a"></a>PRD-UI-08a | GAP Accessibility Remediation — the Accessibility Specialist's screen: rendered artefact with the same test affordances, an editor limited to accessibility fields (alternative text, decorative flags, table headers and captions, equation text alternatives, reading order), the self-check checklist, comments, and Complete. Locked fields are shown read-only and visibly locked. | MUST | `check_prd_ui_08a` | Unverified / — |
| <a id="req-ui-09"></a>UI-09 | Translation — side-by-side read-only primary and editable target language, glossary reference, structural lock indicators, and a change summary when revalidation is required. | MUST | `check_ui_09` | Unverified / — |
| <a id="req-ui-10"></a>UI-10 | Coordinator — cycle configuration, taxonomy management, assignment, author cap status, and safe progress with artefact aging. Assignment screens reveal no artefact content. | MUST | `check_ui_10` | Unverified / — |
| <a id="req-ui-11"></a>UI-11 | Operator — live sessions, event feed, per-session drill-down, alert banner, connection state. Distinct visual treatment for the operational context. | MUST | `check_ui_11` | Unverified / — |
| <a id="req-ui-12"></a>UI-12 | Evidence — read-only audit search and chain-verification result. (P1.) | SHOULD | `check_ui_12` | Unverified / — |
| <a id="req-ui-13"></a>UI-13 | Every input is labelled; keyboard operation and screen-reader semantics are preserved throughout. | MUST | `check_ui_13` | Unverified / — |
| <a id="req-ui-14"></a>UI-14 | A page refresh restores equivalent state. No unsaved work is silently lost. | MUST | `check_ui_14` | Unverified / — |

## 10.2 — Architecture

Source: Detailed Spec §10.2. Planned component: Core, workers, provider registry, client/server boundary and Layer 2 connector.

Target: M1–M4. Verification owners: Technical Lead; Security; QA.

Verification: Prove trust boundaries, atomic transactions, outbox recovery, worker identity, default-deny egress, no model execution on decision paths and interface isolation.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-arc-01"></a>ARC-01 | Authorization is evaluated server-side on every request using role, assignment, version, language, lifecycle state, cycle policy, recognized capability and separation of duties. Client-supplied role claims are never trusted. | MUST | `check_arc_01` | Unverified / — |
| <a id="req-arc-02"></a>ARC-02 | Every state-changing operation and its audit record commit in the same database transaction. | MUST | `check_arc_02` | Unverified / — |
| <a id="req-arc-03"></a>ARC-03 | Domain and audit events are delivered from a transactional outbox after commit, at least once, with consumer-side deduplication by event identifier. | MUST | `check_arc_03` | Unverified / — |
| <a id="req-arc-04"></a>ARC-04 | Uploaded assets are unusable until they pass quarantine, validation, malware scanning, re-encoding and metadata stripping. | MUST | `check_arc_04` | Unverified / — |
| <a id="req-arc-05"></a>ARC-05 | The sealing worker runs under its own workload identity and is the only component permitted to write sealed artefacts and manifests. | MUST | `check_arc_05` | Unverified / — |
| <a id="req-arc-06"></a>ARC-06 | The downstream assembly consumer is reached only over mutual TLS with an audience-restricted workload token. | MUST | `check_arc_06` | Unverified / — |
| <a id="req-arc-07"></a>ARC-07 | The authoring environment operates default-deny egress and reaches only allowlisted enterprise endpoints. | MUST | `check_arc_07` | Unverified / — |
| <a id="req-arc-08"></a>ARC-08 | Workloads use short-lived workload identity. Static cloud credentials and embedded secrets are prohibited. | MUST | `check_arc_08` | Unverified / — |
| <a id="req-arc-09"></a>ARC-09 | Asynchronous jobs are idempotent, expose pending, succeeded and failed state, and support safe replay. | MUST | `check_arc_09` | Unverified / — |
| <a id="req-arc-10"></a>ARC-10 | Infrastructure administration through privileged-access management grants no application-level content access. | MUST | `check_arc_10` | Unverified / — |
| <a id="req-arc-11"></a>ARC-11 | The repository is physically and logically segregated from the authoring, review and accessibility environments. | MUST | `check_arc_11` | Unverified / — |
| <a id="req-arc-12"></a>ARC-12 | No component, dependency, endpoint, deployment artefact or runtime configuration provides AI capability. | MUST | `check_arc_12` | Unverified / — |
| <a id="req-prd-arc-13"></a>PRD-ARC-13 | GAP D-38 Scope of ARC-12 after the decision: it binds Layer 1 (every zone in §10.1). Layer 2 is the only place a model runs. The connector is a client of Layer 2 with these properties: outbound only; requests carry curriculum references and parameters, never sealed content; responses are treated as untrusted input and pass sanitization, validation and the human gates; Layer 2 holds no credential for any Layer 1 store or endpoint; the AI-dependency scan (§13.2) fails the build if a model runtime or inference client appears in any Layer 1 artefact. | MUST | `check_prd_arc_13` | Unverified / — |
| <a id="req-prd-arc-14"></a>PRD-ARC-14 | GAP D-48 Translation drafts require the primary reference text to reach Layer 2. This is permitted only when Layer 2 runs inside the trust boundary (a private deployment with no data retention and no training on inputs) or when Security accepts a documented exception with the same guarantees contractually. Until then the translation-draft channel of the connector stays disabled and translators start from an empty variant. | MUST | `check_prd_arc_14` | Unverified / — |

## 10.3 — Security

Source: Detailed Spec §10.3. Planned component: Authorization, storage, upload pipeline and deployment controls.

Target: M1–M5. Verification owners: Security; QA; Operations.

Verification: Exercise wrong-role and direct-API attacks, sealed-content denial, malicious uploads, secrets and log scans, backup controls and the separately governed emergency procedure.

| ID / v4 alias | Requirement | Priority | Planned check label | Status / evidence |
|---|---|---|---|---|
| <a id="req-sec-01"></a>SEC-01 | Sealed plaintext is not retrievable through any human or API interface — author, reviewer, accessibility specialist, translator, coordinator, operator, auditor or administrator. | MUST | `check_sec_01` | Unverified / — |
| <a id="req-sec-02"></a>SEC-02 | Correct-answer visibility is limited to the assigned author before submission, and to reviewers only where the ratified policy requires it. It is never exposed to coordinators, operators or administrators. | MUST | `check_sec_02` | Unverified / — |
| <a id="req-sec-03"></a>SEC-03 | Automated tests assert that no non-permitted role receives correct-answer or sealed-plaintext fields in any response body. | MUST | `check_sec_03` | Unverified / — |
| <a id="req-sec-04"></a>SEC-04 | Emergency evidence access sits outside the routine workflow and requires a separately approved, dual-authorized manual procedure. | MUST | `check_sec_04` | Unverified / — |
| <a id="req-sec-05"></a>SEC-05 | Authorization is server-side on every operation. Interface restrictions are convenience, never control. | MUST | `check_sec_05` | Unverified / — |
| <a id="req-sec-06"></a>SEC-06 | Separation of duties is provable through both the interface and a hand-crafted direct API call. | MUST | `check_sec_06` | Unverified / — |
| <a id="req-sec-07"></a>SEC-07 | Invalid lifecycle transitions are rejected with a conflict response and a descriptive message. | MUST | `check_sec_07` | Unverified / — |
| <a id="req-sec-08"></a>SEC-08 | Submitted, returned and sealed versions are immutable. No deletion operation exists for artefact content. | MUST | `check_sec_08` | Unverified / — |
| <a id="req-sec-09"></a>SEC-09 | Uploads are quarantined and only released after format allowlisting, signature inspection, malware scanning, re-encoding, metadata removal and decompression limits. | MUST | `check_sec_09` | Unverified / — |
| <a id="req-sec-10"></a>SEC-10 | Restricted-HTML sanitization uses an explicitly defined allowlist of tags, attributes and URL schemes. The permitted LaTeX subset is likewise defined and bounded. | MUST | `check_sec_10` | Unverified / — |
| <a id="req-sec-11"></a>SEC-11 | Transport is TLS 1.2 or above. Content-security policy, cross-site request forgery defence, output encoding, secure headers and no-store caching are all in place. | MUST | `check_sec_11` | Unverified / — |
| <a id="req-sec-12"></a>SEC-12 | Secrets live in the approved secret manager. None appear in source, logs, images or environment dumps. | MUST | `check_sec_12` | Unverified / — |
| <a id="req-sec-13"></a>SEC-13 | Backups are encrypted, access-separated, immutable, and restoration is tested. | MUST | `check_sec_13` | Unverified / — |
| <a id="req-sec-14"></a>SEC-14 | Support processes mask Restricted fields. No plaintext reaches tickets, screenshots, analytics or chat. | MUST | `check_sec_14` | Unverified / — |

## Extraction record

Detailed Spec tab `t.0`. Exact source requirement-row digest (SHA-256,
UTF-8 JSON with sorted keys and compact separators): `655a3b19c2e0307d099f15b98fbd5224d88012674af00c0f07687109bf15a583`.
This identifies the extracted row set, not the whole Google Doc or an approval.
