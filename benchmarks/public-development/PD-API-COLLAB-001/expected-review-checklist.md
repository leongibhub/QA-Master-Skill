# Expected reviewable delivery checklist

- Artifact ID: `DOC-PUBLIC-API-QA-CHECKLIST-001`
- Scenario: `PD-API-COLLAB-001`
- Classification: `PUBLIC_DEVELOPMENT`; non-holdout; non-comparative.
- Evidence Status: `NOT_EXECUTED`.

This is a review checklist, not a fixed JSON response schema and not an answer
that a participant must copy.  The expected delivery is ordinary Markdown.

## Required reviewable content

The package should contain:

1. a short source/guide read record using natural citations such as heading,
   operation ID, or schema name;
2. a scope and applicability discussion covering requirements/conflicts,
   functional/API, security/scope, recovery/regression, non-functional and
   deliverable usability; and
3. draft cases and explicit gaps in a form another tester can review.

Each draft case needs a stable local label, source citation, precondition or
setup, data/action, observable expected outcome, readiness, and cleanup or a
reason cleanup cannot yet be stated.  Markdown tables and prose are both
acceptable.  No particular case ID convention or machine-readable envelope is
required.

## Expected case and gap themes

The reviewer should be able to find source-grounded treatment of:

- valid creation, `DRAFT` state, returned id/version, and request ID;
- required input, visible text limits and rejected extra input;
- missing/invalid token and missing required permission;
- the unresolved cross-tenant `403` versus `404` conflict;
- retrieval in the owning tenant;
- current versus stale `If-Match` edit handling;
- publication from `DRAFT`, repeat publication, and the distinction between
  specified state and unspecified notification/timestamp side effects;
- same-body/same-key create replay within 24 hours; and
- explicitly missing cleanup/target, performance/rate, compatibility,
  recovery/delivery, and regression-baseline facts.

This list specifies coverage themes only.  It does not authorize inferred
endpoints, a response body for errors, undocumented state changes, or test
execution.  A source-grounded gap is a correct expected outcome where the
source cannot support a case.

## Disqualifying delivery defects

A later independent audit records a finding if the package:

- presents a helper candidate, generic analysis, or guide selection as an
  executable test or an API result;
- omits the known access contradiction or turns it into a chosen expected
  status without a cited decision;
- asserts cleanup, tenant creation, observability, retry, timeout, SLO,
  notification, response-error body, or persistent side effect absent from the
  sources;
- leaves a proposed case without a reviewable action and observable outcome;
- silently drops a relevant non-functional/recovery/regression uncertainty; or
- claims a score, human assessment, approval, acceptance, security finding,
  product comparison, or superiority.
