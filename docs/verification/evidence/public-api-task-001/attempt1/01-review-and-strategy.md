# Collaborator Document API 1.4 — QA design review

Classification: PUBLIC_DEVELOPMENT. Document state: DRAFT_UNAPPROVED. Human baseline decision: PENDING. Execution: NOT_EXECUTED (NOT_RUN for every case). This package is an offline, agent-authored analysis of supplied proposals; it contains no observed service results or independent human review.

## Package and source notation

- `01-review-and-strategy.md`: candidate requirements, source conflicts, gaps, methods and traceability.
- `02-draft-cases.md`: functional/API case families and conditional investigative scenarios.
- `03-review-and-handoff.md`: self-review, remaining decisions and continuation boundaries.
- `read-audit.md`: actual read paths and SHA256 of their bytes.

R means `inputs/requirements.md`, Collaborator Document API 1.4 change request, PUBLIC_DEVELOPMENT proposal. A means `inputs/openapi.yaml`, OpenAPI 3.1.0, API 1.4-draft. R citations use heading and exact rule; A citations use operationId or component path. These locators and the read-audit hashes pin the inspected source content. Neither document supplies an owner, date or approved baseline; those identities are unknown. No source code, build, old contract, service or external source was inspected.

Installed guidance used: `SKILL.md`; `references/work-protocol.md` (review packet, traceability, handoff); `references/domains.md` (Web/API profile); professional `requirements-review.md` (atomic rules/conflicts), `functional-api.md` (partitions, transitions and contract checks), `structural-integration.md` (observable side effects and missing dependency contracts), `nonfunctional-compatibility.md` (workload/threshold separation), `security-recovery.md` (bounded authorization and restoration prerequisites), and `regression-evidence.md` (change impact and evidence limits). Full paths/hashes are in the audit. The domain file was read in full, but Linux and AI guidance was not applied. The optional design helper was not used; cases were reasoned directly from R and A.

## Atomic candidate requirements and traceability

All statements below are sourced candidate facts, not approved requirements. Partial means a rule exists but some acceptance or verification detail is missing. TC rows in the case file describe each obligation; listing a row does not establish coverage achieved.

| ID | Actor / trigger / observable candidate rule | Source | Design mapping / limitations |
|---|---|---|---|
| C01 | Caller creates a document; tenant comes from caller token, not body | R Purpose | TC01, TC06, TC13; tenant evidence and key namespace unknown |
| C02 | Caller with document:write creates and edits in own tenant | R Roles; A createDocument/editDocument | TC01, TC09, TC12 |
| C03 | Caller with document:read retrieves own-tenant document | R Roles; A getDocument | TC08, TC12 |
| C04 | Caller with document:publish publishes own-tenant draft | R Roles; A publishDocument | TC15, TC12 |
| C05 | Cross-tenant requests conceal existence with 404 | R Roles; A getDocument responses/403 and /404 | TC13; SOURCE_CONFLICT for GET, undocumented 404 for edit/publish |
| C06 | Missing/unusable bearer token returns 401 | R Roles; all A operations responses/401 | TC11; denial body absent; security scheme absent |
| C07 | New document has server ID, DRAFT state and integer version 1 | R Document lifecycle; A createDocument responses/201, schemas/Document | TC01 |
| C08 | Edit draft requires current If-Match | R Document lifecycle; A editDocument, parameters/IfMatch | TC09, TC10; successful edit version increment unspecified |
| C09 | Stale edit returns 412 and does not apply edit | R Document lifecycle; A editDocument responses/412 | TC10; read-back consistency timing unknown |
| C10 | Publish draft yields PUBLISHED and version increment | R Document lifecycle; A publishDocument responses/200 | TC15; proposed literal interpretation is v+1, confirm if increment amount disputed |
| C11 | Already PUBLISHED publish returns 409 | R Document lifecycle; A publishDocument responses/409 | TC16; non-state side effects unspecified; stale precondition precedence unknown |
| C12 | Same create body/key within 24 hours returns original document, no second document or create sequence | R Create retries | TC17, TC18; status, observability and mutable-response semantics incomplete |
| C13 | Every documented response has X-Request-ID | R Observability; A all responses and headers/RequestId | TC20; nonempty string in A; uniqueness/echo format not promised |
| C14 | POST and PATCH require JSON object containing title and body, no extra properties | A DocumentInput and createDocument/editDocument requestBody | TC02–TC06; PATCH is not documented as a partial body |
| C15 | title string length 1..120; body string length 1..10000 | A schemas/DocumentInput | TC02–TC04 |
| C16 | Create requires string Idempotency-Key length 8..128 | A parameters/IdempotencyKey | TC07, TC17 |
| C17 | Edit and publish require integer If-Match >=1 | A parameters/IfMatch; editDocument/publishDocument | TC09–TC10, TC14–TC16; publish malformed-input status absent |
| C18 | Path ID is required nonempty string | A parameters/DocumentId | TC19; invalid path routing and missing-object writes unspecified |
| C19 | Success Document has required id/title/body/state/version with declared types | A schemas/Document and operation success responses | TC01, TC08–TC09, TC15, TC20 |
| C20 | Missing applicable permission gives 403 per operation | A operation responses/403; R Roles | TC12; overlapping denial precedence unspecified |

## Conflicts and typed gaps

| ID / type | Source evidence and uncertainty | Affected design / required decision or evidence |
|---|---|---|
| G01 SOURCE_CONFLICT | R Roles says other-tenant document requests return 404; A getDocument/403 includes wrong tenant and /404 only absent | TC13: preserve both oracles; source owner must reconcile specification. Do not silently choose a status. PATCH/publish lack documented 404 altogether. |
| G02 AUTH_POLICY_UNCONFIRMED | R names bearer token/scopes; A has no securitySchemes or security declarations | Missing schema is a documentation gap, not proof of anonymous access. Need issuer/token usability rules, scope representation and controlled identity fixtures. TC11–TC13. |
| G03 ORACLE_MISSING | R leaves edit of PUBLISHED unspecified; successful edit version behavior absent | TC09 must not assert v+1; TC21 conditional. Need permitted transition and response/state rule. |
| G04 CONTRACT_MISSING | R only defines same-body retry within 24h; A only lists new-create 201 | Replay HTTP status, inclusive/exclusive exact 24h boundary, TTL start/clock, different body, expired key, timeout, key tenant namespace and concurrent requests unspecified. TC17–TC18, TC22–TC23. |
| G05 OBSERVABILITY_MISSING | R forbids second create sequence but supplies no event/log/count route; Document has no tenant field | Matching returned ID is insufficient to prove one sequence or tenant assignment. Need permitted persisted-document/count/event evidence, correlation semantics and read-after-write timing. No invented list/audit endpoint. TC01, TC10, TC13, TC17–TC18. |
| G06 SIDE_EFFECT_ORACLE_MISSING | R expressly leaves repeat publish timestamps/notifications/other effects open; no delivery guarantee | TC16 cannot assert zero notifications or timestamp invariance. Need side-effect contract, destinations and reversible inspection. TC24. |
| G07 CONTRACT_MISSING | Denials have no body schema; publish has no 400; no 404 for write operations; no media-type failures | No error JSON fields, 415, 422 or publish invalid-header code asserted. Need error body, unsupported-media, unknown-ID write, header serialization and precedence rules. TC05, TC11–TC14, TC19, TC25. |
| G08 ENVIRONMENT_UNIDENTIFIED / AUTHORIZATION_MISSING | No target/build/test permission provided; task explicitly forbids execution and credentials | Every case remains NOT_RUN. Need a separate bounded execution assignment, target/build identity, disposable tenants/accounts, proof level, window, stop conditions and responsible owner. Current task grants design only. |
| G09 CLEANUP_MISSING | R says no cleanup route supplied | No delete endpoint assumed. Need an approved reset/disposal method and any dependent notification/event cleanup. All prospective mutations remain execution-blocked. |
| G10 SLA_UNCONFIRMED / WORKLOAD_MODEL_MISSING | R supplies no latency, capacity, availability, rate limits | TC26–TC29: need demand, mixes, data volume, arrival/ramp/concurrency, duration, resources, telemetry, SLOs and abort limits. No invented thresholds. |
| G11 RECOVERY_OBJECTIVE_UNCONFIRMED | R supplies no recovery procedure | TC23/TC30: need failure injection scope, dependency topology, backup identity, RPO/RTO, restore and reconciliation ownership. |
| G12 SUPPORT_POLICY_MISSING | R supplies no supported-client matrix | TC31: supported API clients/versions/runtime/transport stack, tiers and incompatibility rules pending. |
| G13 IMPACT_UNCONFIRMED | No regression baseline, old/new code revisions, caller inventory or defects | TC32: smoke candidates only; no actual regression coverage conclusion. |
| G14 ORACLE_MISSING | Simultaneous write serialization, precedence of stale-version versus PUBLISHED/tenant/permission errors not defined | TC16 uses current version to isolate 409; TC22 separate collision investigation. Need atomicity and precedence rules. |
| G15 BASELINE_UNCONFIRMED | Both inputs are draft; owner/version approval absent | All candidates require bounded review before formal baselining. Missing approval does not stop this offline design. |

## Method selection and scope

| Method | Applied design and rationale | Remaining boundary |
|---|---|---|
| Requirements review | C01–C20 split actor/trigger/rule; G01 preserves conflicting oracles | Formal baseline PENDING |
| Functional and API | Success schemas, role matrix, state transitions, idempotency, headers | TC01–TC20; no service evidence |
| Equivalence partitions / boundaries / negatives | Omitted/null/empty/wrong-type vs valid fields; endpoint/inside/outside length values; integer/header constraints | TC02–TC07, TC14; invalid routing and some failure codes missing |
| State-transition testing | absent→DRAFT by writer; DRAFT→DRAFT edit with current version; stale edit unchanged; DRAFT→PUBLISHED by publisher; PUBLISHED publish 409 | PUBLISHED edit and simultaneous decisions lack oracle, TC21–TC22 |
| Decision combinations / security | Valid own-tenant appropriate scope vs missing scope vs unusable token vs cross-tenant valid scope isolates each rule | Functional authorization proof plan only; no credential or intrusive testing, TC11–TC13 |
| White-box | Relevant in later implementation review but not designable from these inputs | No code/control flow/revision; no branch, path or MC/DC coverage claim |
| Integration | Create→read→edit→read→publish→read; replay reconciliation and request correlation | Public journey designed; persistence/event/notification ownership missing, TC17, TC24 |
| Performance / load / stress / stability | Distinct actions and measurements in TC26–TC29 | Workload/SLA/telemetry/abort parameters pending; no pass thresholds |
| Recovery | Timeout-retry and isolated restore scenario outlines TC23, TC30 | Recovery objectives and reversible procedure missing |
| Compatibility | Repeat contract journey for each supported client/version once matrix is supplied, TC31 | Matrix unknown; browser/UI testing N/A for the supplied API-only scope |
| Regression | Risk-based proposed smoke/direct/adjacent map, TC32 | Baseline/change map missing; no measured regression coverage |

No UI routes, pagination/sorting, Linux/kernel behavior or AI computation features occur in the inspected API; these are N/A to this bounded design, not declarations that the eventual product lacks them.
