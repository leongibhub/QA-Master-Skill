# Local execution adapter — permission and evidence boundary

Implemented: `qa_master.local_runner.run_local`.

- Executes **local** trusted test commands with `shell=False`; permitted entrypoints are `pytest`, `python -m pytest`, or `python -m unittest`.
- Requires an explicit `RunPermit` matching project, full argv, absolute working directory and immutable artifact version. The model is a **scope record**, not a proof of authenticated identity; production approval must be implemented server-side with signed/audited identity.
- Captures process stdout/stderr, exit code, timeout and a unique evidence file; records SHA-256 checksums and an audit JSON file.
- Reports `PROCESS_SUCCEEDED`, `PROCESS_FAILED`, `TIMEOUT` or `ENVIRONMENT_ERROR`, never pretends this is a passing business test: `business_result=NOT_ASSESSED`.
- Test code may perform arbitrary actions within the executor's OS permissions. **Only run approved, trusted test repositories in isolated environments**. This module is not a security sandbox.
- Output is written outside the test workspace; no network or remote host execution is performed by the adapter itself.

Usage sketch:

```python
from pathlib import Path
from qa_master.local_runner import RunPermit,run_local
cwd=str(Path('.').resolve())
command=('python','-m','unittest','discover')
permit=RunPermit('demo',command,cwd,'approved-operator','test-tree-sha')
result=run_local('demo',list(command),cwd,'test-tree-sha',permit,'/tmp/qa-master-evidence')
print(result['process_status'], result['business_result'])
```

Unit tests: `tests/test_local_runner.py` includes success, failed assertions, approval mismatch, arbitrary interpreter/ shell denial, version mismatch and timeout bounds. Full local suite as developed: **143 passing tests**. Cloud CI, Windows command behavior and production isolation are not yet verified.

## Remaining release work
Actual task queue and lifecycle persistence, authenticated approval workflow, remote SSH/WinRM agent, test-result parsing, browser runner, controlled load-test execution, and Jira/SynapseRT/Confluence CRUD operations are not present. Do not describe this as a completed enterprise platform.
