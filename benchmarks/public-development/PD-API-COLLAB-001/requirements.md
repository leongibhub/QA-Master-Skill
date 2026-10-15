# Collaborator Document API 1.4 change request

Status: `PUBLIC_DEVELOPMENT` proposal for QA design review.  This is an
original public-development scenario, not a deployed service specification or
an approved product baseline.  Execution state: `NOT_EXECUTED`.

## Purpose

Teams create draft documents, edit them, and publish a finished document.  A
document belongs to the tenant selected by the caller's access token.  Clients
must not supply or change a tenant identifier in a request body.

## Roles and visibility

- A caller with `document:write` may create and edit a document in the
  caller's tenant.
- A caller with `document:publish` may publish a draft in the caller's tenant.
- A caller with `document:read` may retrieve a document in the caller's tenant.
- To avoid disclosing whether a document exists in another tenant, a request
  for such a document returns `404`.
- A request without a usable bearer token returns `401`.  The product document
  does not define the body of any denial response.

## Document lifecycle and edits

- A newly created document has state `DRAFT`, a server-assigned `id`, and
  integer `version` 1.
- A draft may be edited only when the request supplies the current version in
  `If-Match`.  A stale version returns `412` and does not apply the edit.
- Publishing a draft changes its state to `PUBLISHED` and increments `version`.
- Publishing an already published document returns `409`; this document does
  not say whether any timestamp, notification, or other stored side effect
  changes in that case.
- The request does not state whether editing a published document is permitted.

## Create retries

- Create requests carry an `Idempotency-Key`.  Repeating the same create
  request with the same key within 24 hours returns the originally created
  document.  It must not create a second document or a second create sequence.
- The request does not state what happens when the same key is reused with a
  different body, after 24 hours, or after a server timeout.

## Observability and non-functional information

- Every documented success or failure response includes the response header
  `X-Request-ID`; a caller can use it when reporting a failure.
- No rate limit, latency SLO, availability target, supported-client matrix,
  test-data cleanup route, notification-delivery guarantee, recovery procedure,
  or regression baseline is supplied with this change request.

## Scope boundary

This request is for draft QA analysis only.  It does not authorize a call to a
service, create a test tenant, use credentials, mutate documents, or report a
test result.
