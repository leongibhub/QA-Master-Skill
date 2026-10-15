# Evaluator audit ledger: Collaborator Document API

- Artifact ID: `DOC-PUBLIC-API-QA-FACTS-001`
- Scenario: `PD-API-COLLAB-001`
- Classification: `PUBLIC_DEVELOPMENT`; not a holdout or comparison input.
- Use: independent audit material.  It is deliberately excluded from a later
  participant's allowed read paths so it does not become an answer sheet.
- Status: `NOT_EXECUTED`; no rating, acceptance, or Gate conclusion.

The rows below are source locations and audit expectations, not a participant
response schema and not a requirement that a participant use IDs.  A later
reviewer may cite these rows when checking the participant's natural source
citations.

| Source location | Visible fact or absence | Audit expectation |
|---|---|---|
| requirements.md / Purpose | Tenant is selected by bearer token; client must not set tenant in body. | Tenant-isolation and request-body scope are considered. |
| requirements.md / Roles / first three bullets | `write`, `publish`, and `read` are distinct permissions. | Method selection includes role/permission negatives where applicable. |
| requirements.md / Roles / fourth bullet | Cross-tenant retrieval is described as `404`. | The OpenAPI conflict below is recorded, not silently resolved. |
| openapi.yaml / getDocument / 403 | Cross-tenant or missing-read access is described as `403`. | Mark a source conflict and name the decision needed before a definitive expected result. |
| requirements.md / Roles / final bullet plus OpenAPI 401 rows | Unusable token is `401`; denial body is unspecified. | Draft denial coverage does not invent an error body. |
| openapi.yaml / DocumentInput | `title` and `body` are required strings with exact visible length bounds and no extra fields. | Boundary/schema cases use only these visible bounds. |
| requirements.md / Document lifecycle / first bullet | Create produces `DRAFT`, server id and version 1. | Create result observation covers supplied fields/state. |
| requirements.md / Document lifecycle / second bullet plus editDocument / 412 | Edit needs current `If-Match`; stale update is `412` and edit is not applied. | State/version assertion is source-bound; any persistence observation beyond “edit not applied” is not invented. |
| requirements.md / Document lifecycle / third and fourth bullets plus publishDocument | Publish changes `DRAFT` to `PUBLISHED` and increments version; second publish is `409`. | Drafts distinguish known state outcome from unknown timestamp/notification side effects. |
| requirements.md / Document lifecycle / final bullet | Editability after publish is unspecified. | Retain a typed question/gap rather than a test expected outcome. |
| requirements.md / Create retries / first bullet | Same create request/key in 24 hours returns original document and creates neither second document nor second create sequence. | Include a repeat/idempotency design with the stated two observables. |
| requirements.md / Create retries / second bullet | Key reuse with changed body, expiry, and server-timeout behavior are unspecified. | Do not fabricate retry, collision, expiry, or timeout outcomes. |
| requirements.md / Observability / first bullet plus OpenAPI headers | `X-Request-ID` is present on every documented success/failure response. | Cases may name it as an observable, without inventing its format or correlation store. |
| requirements.md / Observability / second bullet | SLO, rate limit, client matrix, cleanup route, delivery guarantee, recovery procedure and regression baseline are absent. | Classify each relevant area as an explicit gap/deferred item, not `NOT_APPLICABLE` merely because it is hard. |
| requirements.md / Scope boundary | No target call, credentials, tenant, mutation or result authority. | Deliverable remains draft-only and records no execution. |

Minimum independent audit questions:

1. Does the output expose the `403`/`404` access conflict and avoid choosing a
   fixed expected code without an approved resolution?
2. Do source-grounded case/gap citations account for all rows above, including
   stated absences?
3. Are normal, denial, schema/boundary, optimistic-concurrency, lifecycle,
   idempotency and request-ID concerns considered when the source supports
   them?
4. Is each proposed case usable for review, with setup/data/action/observable,
   cleanup-or-reason, readiness and source citation; are unavailable target
   details gaps rather than invented execution steps?
5. Is the prose free of an execution result, approval, human rating, aggregate,
   superiority, or invented endpoint/role/status/body/side-effect claim?
