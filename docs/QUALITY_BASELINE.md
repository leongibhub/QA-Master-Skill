# QA Master V0.2 — Quality baseline

## Verified locally (2026-10-14)
- `python -m unittest discover -s tests -v`: **39 tests PASS** (21 original + 18 new)
- Coverage: requirement provenance, ambiguous acceptance statements, code-derived requirement human approval, duplicate requirement IDs, case ID/required fields/priorities/expected results/traceability, missing requirement mapping, evidence requirement for PASS/FAIL, unknown defect count, release must not be automatically approved.
- Domain results are deterministic **validators**, not AI-generated complete semantic test analysis.

## Competitor benchmark standard
- Benchmark professional skills with the same input artifacts, model and scoring protocol. Test at least: conflicting specs, code-only candidate requirements, high-risk positive/negative/boundary, API contract/auth, performance without SLA, unreliable outputs, security side effects, 24-hour soak environment, regression impact and evidence-backed release report.
- Every professional module must have: input contract, method/prompt, executable output schema, example, evaluations and run-time validation.
- Do **not** claim QA Master surpasses the upstream skill library until actual side-by-side results are recorded.

## Limits
- No GitLab, Jira, SynapseRT, Confluence, browser, SSH or CI execution adapters.
- No runtime AI invocation of specialized skills.
- No source-code reverse-engineering engine yet.
- No real test execution evidence or release decision workflow.
- GitHub cloud CI results should be independently checked.
