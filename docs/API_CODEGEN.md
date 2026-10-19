# V0.4 API execution boundary

V0.4 adds `qa_master/api_codegen.py`, an original Pytest generator using explicit, approved API scenarios.

**Input:** each scenario must have `method`, resolved relative `path`, integer `expected_statuses` and `approved: true`. Mutating methods also require `allow_mutation: true` at case preparation time.

**Output:** `generate_pytest(scenarios)` returns Python source and `write_pytest(scenarios, path)` saves it. The generated suite needs `pytest` and `requests` installed. It will not run until `QA_EXECUTION_APPROVED=YES` and `QA_TARGET_URL` are set. Mutating methods additionally need `QA_MUTATION_APPROVED=YES`. Authentication is read at runtime from `QA_API_TOKEN`, never embedded in generated files.

Example (no network execution):
```python
from qa_master.api_codegen import write_pytest
write_pytest(
    [{"method":"GET","path":"/health","expected_statuses":[200],"approved":True}],
    "generated/test_api.py"
)
```

The generated tests should **only be run against explicitly authorized isolated environments**, after reviewing the script, origin, data, scopes and side effects.

V0.4 scope: basic status and optional complete JSON equality assertions. No request-schema synthesis, parameter substitution, credentials management, remote runner, attack fuzzing, or network execution by the generator. `tests/test_api_codegen.py` provides offline tests; cloud CI results should be checked separately. The locally developed variant passed 74 tests in total, but the published test file currently contains fewer scenarios; GitHub CI is the authoritative evidence for the published commit.

This is not evidence of superiority to the upstream skill library. A fair feature-and-quality benchmark remains pending.
