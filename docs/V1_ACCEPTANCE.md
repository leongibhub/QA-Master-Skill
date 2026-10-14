# QA Master — V1.0 acceptance tracker (development, not released)

**As of 2026-10-14, V1.0 has NOT met the full release criteria.** This document is the source of truth for further development and prevents a prototype being advertised as an end-to-end testing platform.

## Verified in local isolated unit testing

`python -m unittest discover -s tests -q` — 134 tests passed in the local working tree, including 15 newly added enterprise adapter guardrail tests. Python compilation also passed. GitHub Actions CI should be checked independently; no live corporate service was contacted.

## Implemented foundations

- Basic task routing, dependency-aware phase planning, human approval checkpoints and persistence.
- Requirement provenance and incomplete/oracle validation.
- Requirement-driven draft test cases, coverage matrix and QA case review.
- Python AST branch candidates, partial code-derived requirement review; all remain unapproved until human signoff.
- Read-only GitLab API adapter, constrained source inventory.
- Bounded OpenAPI draft and guarded Pytest source generation.
- Generic HTTPS read-only enterprise connector, exact-scope write-approval *data structure*, SynapseRT PLAN **DRY RUN only**, machine configuration validation.

## NOT implemented or NOT validated

1. Real LLM-driven requirement/architecture semantics and full professional Skill set across functional/API/whitebox/integration/performance/load/stress/stability/compatibility/negative/security/recovery/regression.
2. Live Jira REST, Confluence API, SynapseRT version-specific management calls.
3. Actual remote SSH/WinRM/Runner scheduling, monitoring, artifact retention and network execution.
4. Secure credential vault, UI configuration, multi-user authentication/authorization and audit integrity.
5. Real defect lifecycle, Test Plan/Cycle creation, execution result writeback, GitLab CI webhook integration.
6. Project-complete release quality gate and auditable performance/security/long-run evidence.
7. Side-by-side empirically validated benchmark proving better outcomes than Awesome QA Skills.

## Non-negotiable release gates

- Use real, authorized staging systems and dedicated test accounts; never test production implicitly.
- Approvals must be bound to actual user identity and immutable artifact/version hash, not just an in-memory object.
- High-load and destructive tests must be explicit and separately authorized.
- Dry-run output must not be called a successful Jira/SynapseRT operation.
- A unit test pass is not evidence that a deployed business system passed testing.
- Upstream project contains a PolyForm Noncommercial license in LICENSE at time of audit; do not copy third-party code into this public repo or claim ownership.
- Only claim competitor superiority after evaluation of both solutions on the same independent dataset, with expert ratings and execution artifacts.

## Development approach

Complete the remaining adapters and expert testing modules behind separate feature branches, run cross-component integration tests, then release a versioned public V1.0 only after all critical criteria are passed.


## 2026-10-14: side-effect completion enforcement
- Legacy `Workflow.complete` now denies `test_plan`, `execution`, and `regression` because these stages have `side_effect=True`; no legacy free-text approval can complete them.
- `Workflow.complete_exact` validates an artifact-bound approval before recording completion.
- Added `tests/test_side_effect_gate.py` (five new test definitions).
- **Verification status:** changes are published and GitHub API file reads succeeded. Complete local repository test run is **not verified** in this session: local checkout failed because `github.com` could not resolve. Do not add these five tests to the last verified pass total until CI or an actual local run passes.
- This is a workflow-state guard, **not** authorization for remote execution; no authenticated approval server or real third-party writes are implemented.
