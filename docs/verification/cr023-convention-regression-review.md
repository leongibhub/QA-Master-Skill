# CR-023 Convention-Regression Change — Review (TASK-103)

- **Status**: PUBLIC_DEVELOPMENT / DRAFT_UNAPPROVED
- **Reviewed commit**: `a007345` — `tests/test_skill_instruction_conventions.py` (11 tests, 106 lines)
- **Reviewer**: `/root/workflow_review` (TASK-103, work `work-23f16f29c0264b81a4bf5067af6a4907`)
- **Inputs**: CR-023, CODE-SKILL-CONVENTION-REGRESSION-001, DOC-SKILL-CONVENTION-REGRESSION-001, DOC-SKILL-CONVENTION-REGRESSION-TEST-001
- **Date**: 2026-10-16

## R-checks performed

| # | Check | Result |
|---|-------|--------|
| R-01 | Asserted clauses match the delivered CR-018/CR-021 text: each asserted anchor re-verified against the packaged bytes at `a007345` | PASS — module loads anchors from `skill_bundle()`, i.e. the exact packaged bytes, and TASK-102 V5 cross-checked 14/14 against the TASK-092/097 acceptance lists |
| R-02 | Presence-only scope: no assertion can leak or reward oracle material from CR-022 precommitted assets | PASS — the module reads only repo-committed assets (`qa_master/skills/…`), never `.qa-master/`; no CR-022 oracle tokens appear among anchors (family names in the tests are public CR-021 clause examples, not CR-022 scenario content) |
| R-03 | No arm-tuning risk (OA-3 direction): the guard forbids oracle-synthesized tokens (`GRANTED`/`ALLOWED`) in arm instructions, preserving the audit's non-goal | PASS — the OA-3 class enforces absence; case-sensitive form verified as correct strictness (lowercase prose "allowed" occurs once in SKILL.md and must not trip it) |
| R-04 | Engine-vocabulary mirror is one-sided in the module but two-sided in fact: engine emission (`design_methods.py` → `CONFLICT`/`EXCLUDED`/`GAP`) is pinned by 15 existing assertions across `test_design_methods*.py`; convention-side tokens were verified literal-identical to engine emissions | PASS — no double-coverage gap |
| R-05 | Test style consistent with repo conventions: unittest classes, no new dependency, import-time asset resolution acceptable (module cache reused; failing fast if packaging breaks is the intended behaviour) | PASS |
| R-06 | Verification methodology (TASK-102): disposable tree copy, `\s+`-tolerant mutation anchors, restore-green after each kill, OA-3 injection, isolated `-I` import for wheel-safety | PASS — sound; the two throwaway-harness iterations are correctly classified as verification-tooling bugs, not product bugs |
| R-07 | Change-register and traceability: change is registered as CR-023 with dev → tester → reviewer chain; working tree clean before/after | PASS |

## Findings

- **R-F1 (P3, no action required)**: `test_declared_precision_and_scale_violation_clause` asserts the scale-violation clause in `functional-api.md`, which lives outside `skills/codex/`. This is correct (the clause is where the CR-018 upgrade lives) but means a future packaging reorg of professional skills would break the test via the bundle key string. Acceptable: the failure mode is loud (KeyError/assertion), not silent.
- **R-F2 (P3, no action required)**: The module pins clause presence, not behavioural effect. This is the correct scope; behavioural verification remains CR-022 (quota-blocked). The module docstring already states this boundary.

## Verdict

**PASS — no blocking findings.** The change is a pure regression guard: it can only detect drift, cannot influence either comparison arm, cannot leak CR-022 precommitted material, and its verification is real (mutations actually kill the suite). Recommend closure of CR-023 after change-register update.
