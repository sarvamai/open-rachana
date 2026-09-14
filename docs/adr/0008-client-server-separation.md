# ADR-0008: Zero Trust separation — thin task client and authoritative server

- Status: Accepted. Role placement amended 2026-09-14 by the Product Owner
  in the repository-alignment review; see the dated amendment below. Renderer
  and controlled-reference contracts remain unresolved.
- Date: 2026-09-07

## Context

The deployment model is distributed: one authoritative server (on LAN or
hosted) and many client installations on studio workstations. The team adopts
a Zero Trust posture — the client is an untrusted surface; the server is the
only authority. The v4 specification already requires server-side
authorization on every request (ARC-01), no local storage of artefacts
(QST03-ATH-10), and managed-workstation sign-in (FND04-CAP-11). The product
direction sharpens these into an architectural boundary.

## Decision

Two applications, one repository, separated by a versioned contract. Neither
side imports the other's code; they meet only at `contracts/`.

### Server (authoritative)

Used by oversight roles — coordinator/administrator, integrity operator,
auditor — through its web UI. Holds the question bank, generation, task
assignment, validation, similarity, sealing, readiness, telemetry ingest, and
the replay store. No other component holds state.

### Client (thin task surface)

A signed per-OS application for content roles — author, reviewer,
accessibility specialist, translator. It can do exactly four things:

1. **Authenticate** — author MFA plus machine attestation; the session binds
   (user × machine) and both pseudonymous identifiers are logged (DAT-02).
2. **Receive** — fetch exactly one assigned task: the question as structured
   data plus the operations the server permits for it.
3. **Act** — render the task and capture the user's response
   (approve / modify / suggest / return, per role).
4. **Report** — return the response and stream telemetry (mouse, keyboard
   timing, camera per cycle policy).

Everything else is denied: no question-bank browsing, no assignment
management, no arbitrary server API, no local storage, no offline mode. On
crash or refresh the client re-fetches task state — the server is the only
source of truth. "No ability to interact with the server" is read as: no
interaction beyond this narrow protocol.

### The contract

The client↔server protocol is a small, versioned, machine-readable surface —
authenticate, fetch task, submit response, telemetry stream, heartbeat —
defined under `contracts/` with conformance tests both sides must pass in CI.
The server supports N and N−1 client versions.

### The client renders; it never executes server UI

The client ships its own signed renderer (the shared render-contract package,
bundled at client build time). The server sends structured task data — never
HTML or JavaScript for the client to execute. A compromised server must not
gain code execution on studio machines.

### Role split follows separation of duties

Content roles work only in the client; oversight roles — who cannot view
artefact content per the v4 role table — work only in the server web UI.
Content never flows to oversight surfaces.

## Consequences

- **Machine identity becomes a first-class principal.** Device credentials
  are provisioned per studio workstation through an enrollment flow; sessions
  and audit events carry pseudonymous machine and user identifiers.
- The client enforces its own egress allowlist — the server endpoint only —
  complementing ARC-07's default-deny posture.
- The demo/eval edition (one machine running both) remains a packaging option
  without blurring the boundary.
- Candidate exam delivery remains out of scope (v4 §14.2): the client is the
  authoring workstation, not an exam-hall terminal.
- The build track gains a device-enrollment item ahead of client packaging.

## Admin role placement (amended 2026-09-14)

The original role split above predates the supplied PRD's V1 Admin-as-author
model (main §5; annex §2.7; D-42/D-46). The Admin must be able to author and
view unsealed questions without gaining review approval or sealed-content
read rights. The Product Owner confirmed “Yes—use this split” in the
repository-alignment review: **Admin authoring and unsealed-content work use
the signed desktop client; configuration and content-free oversight use the
web app.** This supersedes the original blanket administrator placement above.
The same identity may use both surfaces with server-checked capabilities;
oversight responses still contain no question content. Review approval and
routine sealed-plaintext read rights remain denied. R1 in
[PRD reconciliation](../prd-reconciliation.md) records the decision.

The trust boundary is unchanged. Session binding, capability selection and
re-authentication between surfaces must be specified and tested before
deployment; the product placement decision is not implementation evidence.

PRD-ATH-18's server reference renderer also needs reconciliation with the
locally bundled renderer (R5). Never solve that conflict by sending executable
server UI to the client. The source's controlled translation/correction
references require an explicit contract without a general vault-read route
(R8). The camera/replay wording above does not authorise capture of question
content or establish a cycle policy; R9 records that remaining decision.

Consequences: versioned role/task schemas, render equivalence and integrity
capture policy are separate acceptance prerequisites. The scaffold and this
ADR alone do not prove them.
