# Traceability — PRD → component → verification → acceptance

The [PRD requirement register](requirements.md) is the individual index: all
302 unique numbered requirements from the retrieved annex, their original
wording and priority, a v4 alias where needed, planned component and check,
and current evidence status. The [source hierarchy](source-of-truth.md)
controls conflicts. Existing code/test names may retain old IDs; do not rename
them merely to change prefixes. New work cites the canonical PRD ID.

## Identifier crosswalk

These mappings come from the PRD's Appendix A. Preserve the group suffix and
number. They identify the same inherited requirement, not an added feature.

| PRD prefix | v4 prefix | Number range | Annex section |
|---|---|---|---|
| ASM01-CFG | QST01-CFG | ASM01-CFG-01..05 | §6.1 |
| ASM03-ATH | QST03-ATH | ASM03-ATH-01..13 | §6.4 |
| ASM03-VAL | QST03-VAL | ASM03-VAL-01..06 | §6.5 |
| ASM03-REV | QST03-REV | ASM03-REV-01..12 | §6.3 (REV-01, 08, 09), §6.6 |
| ASM04-ACC | QST04-ACC | ASM04-ACC-01..09 | §6.7 |
| ASM04-TRN | QST04-TRN | ASM04-TRN-01..10 | §6.8 |
| ASM05-VLT | QST05-VLT | ASM05-VLT-01..08 | §6.9, §8 |
| ASM06-LFC | QST06-LFC | ASM06-LFC-01..06 | §6.12 |
| ASM07-RDY | QST07-RDY | ASM07-RDY-01..06 | §6.10 |
| INS04-CAP | FND04-CAP | INS04-CAP-01..11 | §6.2, §4 |
| RES06-COR | RES06-COR | RES06-COR-01..06 | §6.11 |
| ASR01-EVD | ASR01-EVD | ASR01-EVD-01..10 | §6.13 |
| ASR02-OBS | ASR02-OBS | ASR02-OBS-01..18 | §6.14 |
| ARC | ARC | ARC-01..12 | §10.2 |
| DAT | DAT | DAT-01..08 | §8.1 |
| INT | INT | INT-01..10 | §7.1 |
| UI | UI | UI-01..14 | §9.2, §6.3 (UI-02, 03) |
| SEC | SEC | SEC-01..14 | §10.3 |

`PRD-*` IDs are additions and have no v4 alias. INT ends at **INT-10** in
the supplied annex; the former `INT-01..11` range in this repository was not
supported by that source. UI-02 and UI-03 appear in both §6.3 and §9.2 and
are counted once. All 48 decisions remain in [the decision register](prd-decisions.md).

## Planned component and milestone map

Milestones are dependency/evidence gates, not calendar weeks or closed work.
The [delivery plan](delivery-plan.md) targets the in-scope gates for
28 September 2026. The README's M0 status and partial M1 scaffolding do not
change merely because a target is listed below.

| Annex section | Area | Planned component | Target | Verification owner |
|---|---|---|---|---|
| 6.1 | Cycle and taxonomy | Configuration services; admin configuration surface | M1 | Content Operations; QA |
| 6.2 | Identity and capability | Core authorization; identity SPI; capability registry | M1 | Security; QA |
| 6.3 | Assignment and My Work | Core assignment services; role task surfaces | M1/M3 | Content Operations; QA |
| 6.4 | Authoring and generation | Core artefact services; signed content client; Layer 2 connector and service | M2/M4; by 28 September 2026 | Product; QA; Security |
| 6.5 | Validation and submission | Core deterministic validators; sanitize/similarity/render interfaces | M2 | Assessment owner; QA |
| 6.6 | Question review | Core decisions service; Question Reviewer surface | M3 | Assessment owner; QA |
| 6.7 | Accessibility | Core remediation and decisions; Specialist and Reviewer surfaces; render contract | M3 | Accessibility lead; QA |
| 6.8 | Translation | Core variant services; Translator and Translation Reviewer surfaces; guarded Layer 2 channel | M4 | Assessment owner; Accessibility lead; QA |
| 6.9 | Sealing and vault | Protected sealing worker; kms/storage providers; manifests | M4 | Security; QA |
| 6.10 | Readiness and handoff | Core readiness calculator; machine-only assembly API | M4 | Assembly owner; QA; Security |
| 6.11 | Correction and supersession | Core correction services; seeding worker; outbox and notify provider | M4 | Assessment owner; Assembly owner; QA |
| 6.12 | Downstream lifecycle | Core lifecycle services; signed inbound notifications | M4 | Assembly owner; QA |
| 6.13 | Expected evidence and audit | Core audit store, verifier, expected-evidence assertions and evidence view | M1/M3 | QA; Security; Operations |
| 6.14 | Session integrity | Core sessions, durable integrity ingest and operator surface; content client | M1/M3 | Integrity Operator; Security; QA |
| 6.15 | Notifications | Core notifications and alerts; role surfaces | M1–M4 | Content Operations; QA |
| 7.1 | Interfaces | Core API and event schemas; versioned client/server contract | M1–M4 | Technical Lead; Security; QA |
| 8.1 | Data | Core entities, migrations, canonicalization, manifests and protected storage | M1–M4 | Technical Lead; Security; QA |
| 9.2 | Role screens | Signed content client; configuration and content-free oversight web surfaces (R1 decided) | M2/M3 | Product; Accessibility lead; QA |
| 10.2 | Architecture | Core, workers, provider registry, client/server boundary and Layer 2 connector | M1–M4 | Technical Lead; Security; QA |
| 10.3 | Security | Authorization, storage, upload pipeline and deployment controls | M1–M5 | Security; QA; Operations |

## Evidence that exists in the tree

See [delivery status](delivery-status.md) for exact files, check names and
limits. E1 covers in-memory audit checks; E2 covers part of session integrity;
E3 covers the KMS protocol test double. None closes a production requirement.
In particular ASR02-OBS-01 remains open because its API does not authenticate
the caller, and the store is in memory.

## Requirements beyond the numbered rows

The 302 rows do not replace the PRD's narrative contracts. Implementers must
also cover the following at the associated component's acceptance review.

| Source | Required evidence | Target / owner |
|---|---|---|
| Main §§5, 9–16; annex §§2.7, 4–5 | Complete role/operation matrix, reviewer-isolation payload tests, transition/refusal tests, per-language gates and correction lineage | M2–M4 / Product, Assessment, QA |
| Main §§6–7; annex §§1.5, 6.4–6.5 | Curriculum-to-candidate demonstration with count × multiplier, provenance, validation refusal and human review; D-48 channel off until approved | 28 September target; named Layer 2 owner and interim dates pending / Product, Technical Lead, Security |
| Annex §§7.2–7.4 | Versioned endpoints, error catalogue, event schemas and consumer compatibility tests | M1–M4 / Technical Lead, Assembly, QA |
| Annex §§8.2–8.8 | Entities, constraints, canonical byte fixtures, signed manifests, schema migration and classification/retention evidence | M1–M4 / Technical Lead, Security, QA |
| Annex §§9.1, 9.3–9.5 | Each surface's loading, empty, error, success and resume behaviour; manual accessibility verification | M2–M5 / Product, Accessibility, QA |
| Annex §§10.4–10.7 | Stack constraints, malicious-asset corpus, privileged emergency runbook, egress and environment isolation evidence | M2–M5 / Security, Operations |
| Annex §11 | Load and latency results, availability monitoring, seal timing, restore timing, Unicode and WCAG audit | M5 / QA, Operations, Accessibility |
| Annex §12 | All listed edge cases exercised, including retries, duplicate events, lost sessions, conflicting updates and failed dependencies | Relevant milestone / QA |
| Annex §§13–14, 16–17 | Synthetic corpus, named preconditions and dependencies, milestone sign-offs, operations simulation, support handover and signed go-live pack | M0–M6 / QA, Product and named approvers |

## Closure rule

A row closes only when it links to the implementing commit, actual test or
manual procedure, retained result with date/environment, and the named
acceptance owner's sign-off. Include wrong-role/refusal cases, state/audit
atomicity, content-free output and accessibility where applicable. A UI mock,
test name, passing build, ADR, planned check or target milestone is not closure.

The final pack includes all §17 criteria, penetration-test and accessibility
closures, load/restore/chain-verification results and the recorded go-live
decision. QA can refuse milestone closure. The client/server role split,
canonical byte format and security prerequisites cannot be settled by marking
a traceability row complete.
