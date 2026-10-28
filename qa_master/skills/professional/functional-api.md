---
id: functional-api-design
title: Functional state, boundary, API contract, authentication and negative design
dimensions: functional, api, negative
intents: design, review, code_refinement
risks: low, medium, high
artifacts: functional-case-set, api-contract-matrix, auth-negative-matrix
---
# Functional and API design

Use this guide when a requirement needs testable examples before any execution. It designs cases; it neither sends API requests nor creates external cases.

Before authoring or reviewing reader-facing cases, follow the QA Master
`readable-artifacts` reference as resolved by the entry Skill. The installed
professional guide is packaged under `scripts/qa_master/skills/professional/`;
the reference is at the Skill root, not beside this guide. Keep exact API and
machine contract fields, then write grounded readable case details.

## Inputs and output contract

Inputs are an approved requirement ID and oracle, data domain or state model, API contract/version where relevant, identities and authorization policy, and a declared environment. Output is the requested scoped artifact: a `functional-case-set` with trace IDs, data partitions, state transitions, preconditions, exact expected result and `execution: NOT_RUN`; add an `api-contract-matrix` or `auth-negative-matrix` only when the request or project contract needs it. For a narrow case request, return the cases and relevant gaps, not a default full strategy, all-dimension matrix, JSON handoff or routing analysis.

Default human-facing case detail uses `步骤 | 操作步骤 | 预期结果`, unless an explicit
project format requires an equivalent mapping. Every numbered action, including
preparation, has a fact-grounded expected result or `待确认：具体缺什么，影响第几步`.
Keep actual supplied API/domain/response literals and fields where relevant.
Raw artifact/import metadata keys never enter human prose; when a user, project
or schema explicitly requires them, preserve their exact names and values only
in a separate payload/support block.

## Method

Partition input domains into valid equivalence classes, invalid classes and boundaries. For an ordered range, include each endpoint, just-inside and just-outside values; never use arbitrary values as a substitute for a declared bound. Cover **both** ends of the range with interior step points: when the domain has a declared step or natural unit, include one interior step point adjacent to each endpoint (for example a `2..9` whole-number range includes both `2`, `3` and `8`, `9` as accepted neighbours), not just one side. Build a state-transition table: each allowed transition has a triggering role and effect; each forbidden transition has its denial and invariant. For APIs, compare method, path, parameters, headers, media types, status, response schema, idempotency and error shape to the contract. Exercise authentication absence, invalid credentials, expired credentials, wrong tenant and authorized-but-forbidden roles according to the documented policy.

When a range is decimal with a declared precision or scale, boundary values must be expressed in that declared precision (for example `0.50`, not `0.5`, when the rule states hundredths), and the rejected set must include at least one value that violates the scale by one place beyond it (for example `0.505` when the scale is two), alongside the numeric just-outside neighbours.

## Executable acceptance oracle examples

For quantity `1..100`, a test oracle can assert that `1` and `100` create the order, `0` and `101` receive documented validation responses, and no rejected request creates an order. For `POST /orders`, the matrix can assert HTTP `201`, a response body conforming to the declared schema, a nonempty server order ID, and a repeated request with the same idempotency key has the documented single-effect outcome. Expected status alone is insufficient when the contract specifies a body or state effect.

## Missing information

Unknown bounds, response schemas, idempotency rules, privilege matrix or error contracts become `ORACLE_MISSING`, `CONTRACT_MISSING` or `AUTH_POLICY_UNCONFIRMED`. Keep the affected case draft blocked; do not invent a `401` versus `403` distinction or success payload.

## Review checklist

- Does each partition map to a real domain rule and each transition preserve stated invariants?
- Are API versions and request/response contracts pinned to a source?
- Do negative cases prove no unintended state change?
- Are identity, tenant and permission assumptions explicit and safe for the target environment?
