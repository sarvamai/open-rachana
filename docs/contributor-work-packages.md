# Contributor work packages — proposed allocation

This is a proposed work allocation for discussion with the contributors,
prepared on 14 September 2026. Names follow the Product Owner's list; availability,
acceptance of these assignments and relevant specialisms remain to be confirmed.
It does not change the product contract or record a commitment by a volunteer.
Irfan's observability scope reflects the stated intention; Rohit's testing role
is a proposed invitation. Nikhil has explicitly asked to contribute through
product work and pull requests; his package below proposes that scope.
Intelligence remains with the Sarvam/server team.

The accompanying product-reference PR supplies the expanded requirement
register and reconciliation items mentioned below. These work packages propose
ownership without independently ratifying those product or security decisions.

## Docs first, then implementation

Each epic owner checks in a plan under [docs/plans](plans/README.md) before
implementation. Nikhil reviews product scope and acceptance; KKT coordinates
technical review; Rohit reviews the test approach. Record the accepted plan
revision and go-ahead in the issue. Extended tasks get their own plan; small
tasks use a short task plan. Existing approvals and in-flight work remain valid.

Use [Humanizer](https://github.com/blader/humanizer) on plans, documentation and
PR descriptions before review, then read the result yourself. Preserve exact
requirements, IDs, interfaces, numbers and approval status. A planning skill can
turn an approved plan into tickets; it cannot approve scope or implementation.

The [plan index](plans/README.md) links eight proposed epics and the existing delivery stories,
plus missing diagnostic, contract, recovery and onboarding work. The starter
plans need their owners' review before implementation begins.

## Recommended team shape

Keep one repository and the existing core/client/web architecture. These are
ownership boundaries inside the product, not five new microservices. Each
package needs a primary maintainer, a reviewer and small independently reviewable
pull requests. KKT is the proposed integration lead with authority to settle
interface questions and coordinate shared changes. The Product Owner decides
scope and unresolved product policy.

| Package | Proposed primary | Outcome |
|---|---|---|
| 1. Workspaces and client | Divyansh | Each person can complete their permitted task through the correct interface |
| 2. Workflow and business rules | Kaustav | The server controls every transition, assignment, permission and refusal |
| 3. Audit, sealing and vault | Gandharva | Every accepted action has durable evidence; approved versions seal and verify correctly |
| 4. Operational observability | Irfan | Engineers can diagnose failures through correlated, content-free logs, metrics and traces |
| 5. Platform, identity integration and delivery | KKT, with managed-service support | The integrated application can authenticate users, deploy, recover and be handed over |
| Shared testing and acceptance | Rohit, supporting all five | A common harness independently exercises contracts, refusals, failures and complete flows |
| Product acceptance and onboarding | Nikhil | Clear product decisions, reviewable contributor briefs and concrete acceptance scenarios |
| Layer 2 intelligence | Sarvam/server team; individual lead to be named | Curriculum-grounded proposals arrive through agreed adapters with provenance |

This uses five implementation owners, Rohit's cross-team testing contribution
and Nikhil's product contribution.
KKT's primary responsibility is integration: keep his platform work to a
bounded reference deployment and service bindings, with operational support.
Do not give him a full independent feature backlog as well as all integration.
Do not build identity, databases or key-management products from scratch.
The adopting organisation contracts its managed-service providers; the team integrates
and verifies it.

## 1. Divyansh — workspaces and client

**Own:** the signed desktop content surfaces and content-free web configuration/
oversight surfaces; editor/autosave, My Work, reviewer screens, accessibility
remediation/review, translation, validation messages and permitted operator UI.
Preserve reviewer isolation and loading/empty/error/success behaviour.

**Consume:** the versioned task/API contracts, permission responses, validation
findings and integrity-ingest contract. Screen code never decides authorization,
state transitions or seal readiness. Never read the database directly.

**First three contributions:**

1. Render one assigned task from a contract fixture, with accessible navigation
   and explicit refusal/error states. A fixture is labelled as such.
2. Connect sign-in, manual draft save and submit to the real API; make the
   submitted version read-only and display the server receipt.
3. Connect review and rejection, then extend the same contract-driven pattern
   through accessibility, translation and the content-free operator view.

**Completion proof:** two distinct users complete an allowed author/reviewer
flow; direct API calls still enforce permissions; UI and payloads do not expose
forbidden context; keyboard/accessibility checks pass. Client integrity signals
are collected only under the agreed policy and never through diagnostic logging.

**Main requirement coverage:** role screens/UI, authoring interaction, review/
translation/accessibility surfaces. Domain owners retain their server obligations.
Rendering and protected-reference decisions R5/R8 gate the affected client work.

## 2. Kaustav — workflow and business rules

**Own:** cycle/taxonomy, the authoritative state machine, artefact/version and
lineage rules, capability and separation-of-duties policy, assignments/expiry,
deterministic validation, review decisions, accessibility/language gates,
corrections, readiness, notifications and downstream lifecycle handlers.
Own Layer 1's consumption of generation proposals, validation and provenance;
Layer 2 owns their production.

**Consume:** verified identity from package 5, audit append/verification and
sealing contracts from package 3, and generation adapters from Layer 2.
Provider code cannot change workflow state. Use one core transition boundary
that commits the state change and audit event in the same database transaction.

**First three contributions:**

1. Publish cycle, actor, task, version and transition contracts with synthetic
   fixtures and allowed/refused examples; name transaction and migration owners.
2. Implement persisted draft → submit → independent review → return/approve,
   with assignment, concurrency and direct-API separation-of-duties checks.
3. Extend through accessibility, primary seal request, language variants,
   per-language gates, readiness and correction-driven readiness revocation.

**Completion proof:** no role or handcrafted API call can skip a gate; a return
preserves the old version; invalid/stale concurrent requests fail; state and
audit remain atomic under injected failures. All required language versions
must seal on the current lineage before metadata-only readiness is true.

**Main requirement coverage:** CFG, CAP policy, assignment, ATH server, VAL,
REV, ACC/TRN server, RDY, LFC, notification and workflow ARC/INT obligations.
Resolve R4 before choosing a separate Author role or proposal-adoption transition.
Use a provider fixture to unblock contract work; it cannot close AI acceptance.

## 3. Gandharva — audit, sealing and vault

**Own:** durable append-only audit, canonical byte/manifest implementation once
ratified, hashes/signatures, expected-evidence verification, protected sealing
worker, encryption/key and object-store adapters, immutable version storage,
audit verification tools, and authorised correction/reference materialisation
once R8 is decided. The core workflow owner decides whether a transition is legal.

**Consume:** package 2's transaction and seal-job contract; package 5's managed
keys/storage, workload identities, retention configuration and restore environment.
Return a verifiable receipt/status to the core; do not publish a human vault-read API.

**First three contributions:**

1. Agree the audit event and atomic append contract with package 2; implement
   persistent append/verify with a ratified format and synthetic fixtures.
2. Implement one seal job with prerequisite checks, manifest verification and
   safe retries. Prove partial external writes cannot falsely mark a version SEALED.
3. Add language-seal verification, correction lineage evidence and verification
   after backup/restore with package 5.

**Completion proof:** altered or removed events are detected; absent evidence
blocks sealing; repeated jobs do not create inconsistent seals; wrong identities
cannot read sealed plaintext; backup/restore preserves audit and manifest verification.
Key-service/store failure leaves an explicit recoverable state, never silent success.

**Main requirement coverage:** EVD, VLT, canonicalisation/manifest DAT and relevant
sealing/storage SEC/ARC controls. D-01/D-02 and D-24 are real prerequisites;
engineering ownership does not grant policy approval.

## 4. Irfan — operational observability

**Own:** content-free application logs, metrics and traces; framework
instrumentation for Python/FastAPI and Next.js; context propagation; an
OpenTelemetry Collector; and a reproducible local Grafana/Loki/Tempo/Prometheus
setup. Add domain dashboards and alerts as workflow events become available.
Use the existing [observability specification](observability.md) and
[implementation slices](observability-plan.md); preserve their actual decision status.

**Consume:** framework lifecycle hooks and stable, content-free domain event
names/attributes supplied by component owners. Publish a small instrumentation
convention so each contributor instruments their own changes. Coordinate runtime
bootstrap edits with the owner of that app; do not take ownership of domain rules.

**First three contributions:**

1. With Rohit, agree the leak-sentinel checks and ensure they run in real CI.
   The current observability plan's Python-CI prerequisite belongs in Rohit's
   shared harness work, reviewed with Irfan; avoid two competing CI changes.
2. Deliver Python instrumentation and the local stack, then connect Next.js
   tracing and prove request correlation across the boundary.
3. Add workflow latency/error/failure dashboards and tested alerts with
   synthetic events; actual workflow acceptance waits for the real flows.

**Completion proof:** an induced request failure is traceable across services;
related logs and metrics can be found; sentinel question content never exports;
the application still serves when the diagnostic Collector is unavailable.
Record the separate integrity path's behaviour independently.

**Boundary:** diagnostic telemetry is not the permanent exam audit trail.
Irfan can display content-free domain signals, but the workflow owner implements
session ownership, durable integrity ingest, scoring/referral policy and actions;
the client owner implements authorised collection; the audit owner records
required evidence. Optional diagnostic loss cannot excuse lost integrity evidence.
Framework auto-instrumentation must be configured and verified; it does not
supply domain measures, content filtering or leak tests automatically.

## 5. KKT — integration, platform and recovery

**Own:** the shared API/event contract review, migration ordering and integration
queue; reference deployment/configuration; identity-provider integration,
token/MFA/device/workload verification; secrets/service bindings; release pipeline,
application rollback procedures and operational backup/restore runbooks.
Coordinate with the adopting organisation’s contracted providers for real test dependencies.

**Boundary:** the IdP proves identity; package 2 decides what that identity may do
in the current task and lineage. Contracted providers supply services; packages 2/3 own
application data semantics. Rohit owns test-gate design; KKT owns deployment/release
mechanics. Application rollback must preserve sealed records and audit history;
never implement rollback as deletion or rewriting of accepted evidence.

**First three contributions:**

1. Establish a reproducible shared development environment and the integration
   contract review; connect real user/workload identity and refuse invalid tokens.
2. Deploy the first complete flow into a shared environment with explicit
   configuration, migrations, health checks and restricted service identities.
3. Demonstrate a failed-release recovery and backup/restore with package 3;
   verify application/schema compatibility and retain the operational procedure.

**Completion proof:** another engineer can bring up the documented environment;
wrong/expired credentials fail; the deployed flow works with real persistence;
release recovery preserves evidence; restored records and seals verify. Relevant
production qualification and named operational acceptance remain separate gates.

**Main requirement coverage:** identity integration, deployment/configuration,
workload isolation, RES and operational SEC controls. The technical lead does
not independently approve unresolved product, retention or security policy.

## Rohit — the testing system and acceptance discipline

Ask Rohit to establish how the whole product is verified from the beginning.
Every package owner remains responsible for tests of their own implementation.
Rohit maintains the shared harness, supplies independent adversarial scenarios,
and reviews whether evidence is sufficient; do not make him the author of every test.

His first contribution should replace the Python CI placeholder with real
checks and establish repeatable synthetic fixtures. Then provide:

- Contract tests that allow client, workflow, storage and AI-adapter work to
  proceed independently against the same agreed examples.
- Unit and database-backed integration tests for state/audit atomicity,
  concurrency, retries, idempotency and permissions.
- Interface and end-to-end tests appropriate to the web and signed desktop
  surfaces. Browser tests alone cannot certify native desktop restrictions.
- Reusable failure cases: unavailable Collector versus unavailable required
  evidence/key/store, invalid credentials, tampering and interrupted sealing.
- A requirement → test/procedure → retained result → sign-off index, aligned
  to the existing 302 requirement register and seven completion outcomes.

Automated review can assist the maintainer; it cannot replace independent tests,
expert accessibility checks, security review or acceptance signatures. Name the
human reviewers for those checks before declaring their milestones closed.

## Nikhil — product acceptance and contributor onboarding

**Own:** product behaviour and scope, contributor briefs, the permission matrix
and examples, concrete user journeys, prioritisation, product decision records,
manual product acceptance and the contributor's first-run experience. Contribute
through normal issues and pull requests, with technical review where required.
This is a substantive implementation input: engineers and their agents need
precise allowed/refused examples to build the right behaviour.

**First three pull requests:**

1. **Product acceptance scenarios.** Write the expected behaviour for the first
   manual author/reviewer flow, including self-approval refusal, rejection and
   linked correction, and reviewer isolation. Link each scenario to its existing
   requirement IDs. Rohit reviews testability and maps scenarios into the harness.
2. **Contributor start-here guide.** Follow the setup as a new contributor;
   document the actual steps, first task, expected result and where to get help.
   Record setup failures as issues rather than describing unverified instructions
   as working. KKT reviews the technical steps.
3. **One build-ready contribution brief per active owner.** Turn the first
   integrated checkpoint into bounded issues with examples, dependencies,
   acceptance conditions and reviewer. Keep scope and the decision register
   current as owners respond. Each engineer reviews their own brief.

Example acceptance scenario Nikhil can author:

| Field | Example |
|---|---|
| Requirement | INS04-CAP-07 and SEC-06 |
| Given | A synthetic user authored and submitted a question version |
| When | That same identity attempts to approve the version through the API, even while holding a reviewer role |
| Then | The server refuses approval; neither an approval record nor the corresponding approved transition is created; the required refusal evidence contains no question content |
| Companion case | An eligible independent reviewer can act after all task and review prerequisites are satisfied |
| Implementation contract | Exact response/error code is agreed by the workflow owner; the scenario does not invent it |

Use an agent to draft the Markdown, synthetic fixtures or acceptance checks,
then inspect the proposed behaviour personally. Ask Rohit to review executable
checks so a scenario does not merely repeat the implementation's assumptions.
An example written in Markdown is a specification, not a passing test.

**PR ownership:** Nikhil can open and revise his own documentation, onboarding,
product-decision and acceptance-example PRs. Engineers review API, schema,
security and executable-test changes. Product acceptance by Nikhil does not
replace technical review, independent accessibility/security evidence or the
other named release signatures. Use synthetic content only.

**Completion proof:** another contributor can understand a brief without
reconstructing the conversation; each acceptance scenario has an observable
result and requirement link; the first-run guide was actually followed; product
findings become tracked corrections and retained acceptance results.

## Agree these boundaries before parallel implementation

| Contract | Authors / consumers | Decision to freeze in the first working session |
|---|---|---|
| Identity and capability context | KKT + Kaustav; all API consumers | Verified actor/workload identity, roles, device claims, revocation and refusal semantics |
| Task/version API | Kaustav + Divyansh; Rohit verifies | Version IDs, immutable submission, actor permissions, concurrency, errors and receipts |
| Transaction and evidence | Kaustav + Gandharva; Rohit verifies | Single state/audit transaction, event schema, expected evidence, retry/idempotency and schema migration ownership |
| Seal job and receipt | Gandharva + Kaustav + KKT | Preconditions, managed identities, partial-write recovery and exact completion receipt |
| Diagnostic instrumentation | Irfan + runtime owners | Content-free names/attributes, request correlation, export guard and diagnostic failure policy |
| Session integrity | Kaustav + Divyansh + Gandharva; Irfan consumes allowed signals | Authenticated ingest, durable evidence, policy-driven referrals and content-free operator payload |
| Generation adapter | Named Layer 2 lead + Kaustav | Request/provenance/response schema, count semantics, failures/timeouts and no sealed-content or store access |

Keep schemas and examples in the shared repository. Work against contract
fixtures while the producer is under construction, then replace the fixture
with its real implementation in the integration test. No competing workflow
state machines, private API variants or unrelated database migrations.

## First integrated checkpoint

Build one synthetic question through sign-in → persisted manual draft →
validation/submission → independent review, with an atomic audit event,
correlated diagnostic trace and a CI check that rejects self-approval.
KKT owns getting this assembled; each package delivers its contribution.
Nikhil checks the user journey and acceptance examples; Rohit checks the harness
and retained evidence. Record defects against their package owners.

Then extend that same working path through accessibility and primary sealing,
followed by the other required languages, readiness, correction and recovery.
Layer 2 connects through its contract in parallel. This progression orders the
work; it does not remove any of the seven completion outcomes or approve an
unfinished product for examination use.

Merge small contributions continuously. Hold a short integration check each
working day, and end each agreed milestone with a working shared flow and
retained evidence. Do not wait for every package to be declared complete
before attempting integration.

## Start from the existing issue backlog

Use the existing issues to track implementation; these packages group ownership
and do not close or duplicate those issues. Select one bounded first issue per
active contributor and retain its acceptance criteria.

| Package | Existing issue entry points |
|---|---|
| Workspaces and client | #53, #58–60, #65–66, #69–70, #73–75; pair with the workflow owner on the shared feature |
| Workflow and rules | #42, #44–45, #61–68, #71–72, #79–84 |
| Audit, sealing and vault | #46–48, #71, #77–78; share restore acceptance in #88 |
| Observability | #49–50 for the related evidence/leak boundaries; the observability plan covers the separate diagnostic implementation |
| Platform and integration | #41, #43, #51, #85, #88 |
| Testing and acceptance | #52, #86–89; feature owners supply their own checks |
| Product and onboarding | #39–40 and #89; reference documentation also relates to #94 |
| Layer 2 | #54–57, coordinated with the workflow owner |

Issue references were checked on 14 September 2026. Mapping an issue to a
package does not claim it is implemented, assigned or accepted. In particular,
#50 is session-integrity work, not permission to route durable evidence through
the optional diagnostic pipeline.

## What to give an engineer and their agent

One issue should describe one reviewable change, with:

1. The user/system outcome and applicable requirement IDs.
2. The primary maintainer, reviewer and scope boundaries.
3. The interface examples and dependencies it consumes or supplies.
4. Expected files/modules and any shared-file coordination required.
5. Observable acceptance examples, including at least the relevant refusal
   and failure cases; link the actual check or manual procedure.
6. Unresolved decisions that block this change, with independent work that
   can proceed. An agent must not silently settle those decisions.
7. Completion evidence: implementation, tests, configuration, documentation,
   retained results and a demonstration to another contributor.

Each package should start with the three contributions listed above, split
further when one contribution cannot be reviewed coherently. Agents may draft
code and tests; the named human maintainer is accountable for the change and
its integration. A different maintainer reviews shared security/contracts.
Use existing DCO, dependency and review conventions. Keep real examination
content and credentials out of agent prompts, examples, logs and commits.

## Capacity rule

Five named people are not five full-time engineers. Before setting individual
dates, record each person's available hours, start date, response window and
whether they will implement, review or advise. Confirm a backup maintainer for
each critical package. The 28 September date remains a target, not a capacity
estimate established by this allocation.

If only two engineers are active, use two primary implementation streams:
client/workspaces and core/evidence. Schedule Irfan's observability and Rohit's
harness as bounded enabling contributions, and have KKT support integration
and the managed environment if his availability permits. Sequence the remaining
work against the shared flow. Keep all five ownership boundaries on paper,
but do not open five simultaneous implementation backlogs without owners.
Reassess delivery scope/date explicitly if available capacity cannot cover the
required acceptance gates; do not silently drop gates to fit the calendar.
