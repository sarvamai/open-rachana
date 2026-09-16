# #42: As the System, I want every request authorised from the capability matrix

Owner proposed in the delivery plan: **Kaustav**. Technical review: KKT; Gandharva for transaction/evidence boundaries.
Epic: [#103](https://github.com/Bodhan-AI/open-rachana/issues/103). [Module route](../workflow.md).

Enforce the role-by-operation matrix on every server request and maintain the recognised-capability registry.

## Start here

Read the current implementation snapshot in [delivery status](../../delivery-status.md) before choosing files.

First deliverable: Implement a pure policy evaluator and table-driven tests for every matrix cell, then wire one draft-create and one review-decision operation to it.

## Role-by-operation matrix

✓ = allowed. Empty = not allowed. There are no TBD cells.

| Capability | Admin | Question Reviewer | Accessibility Specialist | Accessibility Reviewer | Translator | Translation Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Upload curriculum | ✓ |  |  |  |  |  |
| Create blueprint, configure cycle | ✓ |  |  |  |  |  |
| Generate or regenerate questions | ✓ |  |  |  |  |  |
| Manually create a question | ✓ |  |  |  |  |  |
| Edit a draft, add images | ✓ |  |  |  |  |  |
| Withdraw a draft ("delete") | ✓ |  |  |  |  |  |
| Retire an approved question ("delete") | ✓ |  |  |  |  |  |
| View all questions (until sealed) | ✓ |  |  |  |  |  |
| View assigned question | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Comment | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Approve or reject question review |  | ✓ |  |  |  |  |
| Remediate accessibility |  |  | ✓ |  |  |  |
| Approve or reject accessibility |  |  |  | ✓ |  |  |
| Create or edit a translation |  |  |  |  | ✓ |  |
| Approve or reject a translation |  |  |  |  |  | ✓ |
| Assign or reassign reviewers | ✓ |  |  |  |  |  |
| Authorize a correction | ✓ |  |  |  |  |  |
| Manage users and roles | ✓ |  |  |  |  |  |
| View audit logs | ✓ |  |  |  |  |  |
| Seal a question | System only |  |  |  |  |  |
| Read a sealed question | Nobody |  |  |  |  |  |
| Download or export | Nobody |  |  |  |  |  |

The Admin never approves or rejects. The Admin writes the questions. See D-46.

This is the main PRD matrix. Read it with the request guards below: a tick never bypasses validity, scope, lifecycle or separation of duties; assignment is required for operations on assigned tasks. The main PRD names the authoring role Admin; adding a separate Author remains R4. System-only operations never become Admin powers. Auditor and Integrity Operator have content-free scopes as specified in main §5.8.

## Inputs and outputs

- Input: Verified actor from #41; requested operation; capability validity/revocation; cycle, subject, language, assignment, version state and prior actors.
- Output: Allow or deny before data access or mutation; deny with a safe error and content-free security/audit record. Registry renewals supersede append-only entries.

## Product rules for this task

The clauses below are retained source wording. `GAP` identifies an addition in the original PRD; it does not mean the clause is unspecified. Apply [effective rules and source conflicts](../effective-rules.md), especially role naming and the approval status of proposed D-nn values.

| Requirement | Required behaviour | Priority |
|---|---|---|
| [INS04-CAP-04](../../requirements.md#req-ins04-cap-04) | A registry records, against a pseudonymous workforce audit identifier, what each contributor is recognized to do: role, subject and language scope, accessibility qualification, issuing authority, validity window and revocation state. | MUST |
| [INS04-CAP-09](../../requirements.md#req-ins04-cap-09) | Access to any object outside the user's assignments returns a denial and raises a security event. | MUST |
| [INS04-CAP-10](../../requirements.md#req-ins04-cap-10) | Revocation takes effect on the next request; an in-flight assignment becomes unactionable immediately. | MUST |
| [PRD-CAP-16](../../requirements.md#req-prd-cap-16) | GAP Capability entry fields: audit identifier, role, subject scope (taxonomy subject identifiers), language scope (BCP 47 tags), accessibility qualification with credential reference, issuing authority, valid from, valid to, revoked at, revocation reason, created by, audit references. Entries are append-only with supersession; renewals create a new entry. | MUST |
| [PRD-CAP-18](../../requirements.md#req-prd-cap-18) | GAP Authorization reads the registry on every request. Any cache is at most 5 seconds and is invalidated synchronously on revocation, so CAP-10 holds. An hourly sweep marks expired entries, flags their in-flight assignments on the coordinator board, and leaves recorded decisions untouched. | MUST |
| [PRD-CAP-19](../../requirements.md#req-prd-cap-19) | GAP D-05 Registry maintenance (create, renew, revoke) is performed by the Coordinator role with re-authentication and is fully audited. The identity provider remains the identity authority; the registry never stores names, emails or credentials beyond the pseudonym mapping table. | MUST |
| [INT-09](../../requirements.md#req-int-09) | A role-by-operation permission matrix is authored, implemented, and used as the test oracle for authorization. | MUST |
| [ARC-01](../../requirements.md#req-arc-01) | Authorization is evaluated server-side on every request using role, assignment, version, language, lifecycle state, cycle policy, recognized capability and separation of duties. Client-supplied role claims are never trusted. | MUST |
| [SEC-05](../../requirements.md#req-sec-05) | Authorization is server-side on every operation. Interface restrictions are convenience, never control. | MUST |
| [INS04-CAP-07](../../requirements.md#req-ins04-cap-07) | A user may hold multiple roles but is blocked from authoring or translating and then approving the same version. The API enforces this independently of the interface. | MUST |
| [INS04-CAP-08](../../requirements.md#req-ins04-cap-08) | An accessibility specialist cannot act on a version they authored, translated or reviewed. | MUST |
| [PRD-CAP-12](../../requirements.md#req-prd-cap-12) | GAP Identity integration uses OpenID Connect Authorization Code flow with PKCE against the enterprise identity provider. The token must carry a stable subject and an authentication-methods claim proving multi-factor authentication; a token without it is refused with FORBIDDEN_MFA_REQUIRED. Group or role claims in the token are informational only and never authorize anything (ARC-01). | MUST |
| [PRD-CAP-13](../../requirements.md#req-prd-cap-13) | GAP Pseudonymization: on first sign-in the system generates a random, unguessable, stable workforce audit identifier and stores the mapping to the identity-provider subject in a separately access-controlled table. All business records, audit events, telemetry and screens other than the coordinator's assignment views use the audit identifier only (DAT-02). | MUST |
| [PRD-CAP-17](../../requirements.md#req-prd-cap-17) | GAP A valid token with no capability entry, or a role claim matching no known role, lands on a "Not provisioned — contact your administrator" screen; access is denied and a security event raised. | MUST |

## Exact PRD sections

- [5.1 RBAC matrix](../../prd/main-baseline.md#51-rbac-matrix)
- [5.8 Other roles](../../prd/main-baseline.md#58-other-roles)
- [17. Security](../../prd/main-baseline.md#17-security)
- [6.2 Recognized capability and access · INS04-CAP](../../prd/technical-baseline.md#62-recognized-capability-and-access--ins04-cap)
- [4.4 Separation-of-duties rules](../../prd/technical-baseline.md#44-separation-of-duties-rules)
- [7.1 Mandatory interface behaviours](../../prd/technical-baseline.md#71-mandatory-interface-behaviours)

## Behaviour to demonstrate

An Admin who created version V cannot approve V even if a request claims Question Reviewer. Revoke a reviewer capability after opening V: their next decision request fails and V remains undecided.

Failure checks: Try a client-forged role, missing capability, revoked actor and each forbidden cross-role operation. Check both response fields and writes.

Existing issue acceptance criteria, retained for review:

- [ ] Roles encoded as data: Admin, Question Reviewer, Accessibility Specialist, Accessibility Reviewer, Translator, Translation Reviewer, Integrity Operator, Auditor, System
- [ ] Admin cannot approve or reject at any stage (unit + API test)
- [ ] Reviewers cannot edit; Integrity Operator and Auditor have no content fields
- [ ] Missing capability is 403; client-supplied role is ignored
- [ ] Admin can manage users and assign roles (write path + audit event)

## Dependencies and decisions

Required producer work: [#41](issue-41.md) (KKT).

R4 blocks adding a separate Author permission set, not enforcing the existing Admin/reviewer restrictions. D-05 concerns registry stewardship; D-46 is the source correction removing Admin review approval.

## Engineering choices and review

The owner chooses module layout, database design and implementation algorithms within these rules. New shared schemas and transaction/retry behaviour need the named consumers’ technical review. Source defaults marked D-nn are configuration candidates, not approval records. Build tests with explicit synthetic settings while the owner selects deployment values. Only the dependent behaviour listed above waits for a product/security decision.

Use the issue and this brief as the checked-in plan. For an extended change, add the proposed design and first PR boundary here before implementation review. Keep existing valid approvals and in-flight contributions. Completion needs the implementation, actual test result and acceptance owner; a generated check name is not passing evidence.
