# Artifact-bound approval gate (development milestone)

New: `qa_master/approval.py`, and `Workflow.approve_exact`, `evaluate_exact`, `complete_exact`.

## Why this exists
The legacy `Workflow.approve(kind,version,scope)` only records free-form labels. It is **not sufficient** to authorize writes or testing. The exact gate binds an approval to:
- action/approval kind
- project
- execution or review scope
- SHA-256 of canonical JSON artifact
- declared reviewer label

At the point of use the actual artifact is rehashed and compared. A changed case list, a changed requirements set, or a different project/scope causes `WAITING_APPROVAL`. Old version-only approval records fail closed when using `evaluate_exact`.

## Example
```python
from qa_master.workflow import Workflow
w=Workflow('demo')
w.request(['baseline'])
w.answer('source','requirements.json')
w.complete('requirements','requirements.json')
w.complete('review','review.json')
requirements={'id':'R1','acceptance':'HTTP 201'}
w.approve_exact('requirements','demo/release-1',requirements,'reviewer')
assert w.evaluate_exact('baseline',{'requirements':requirements},{'requirements':'demo/release-1'})=='READY'
w.complete_exact('baseline','baseline-v1.json',{'requirements':requirements},{'requirements':'demo/release-1'})
```

**Security limitations:** the reviewer name is not authenticated. This is an artifact integrity and scope guard, *not* an identity, cryptographic-signature, or access-control service. A caller with write access to the persisted JSON can forge records. Real Jira/SynapseRT writes and remote executions must require server-side identity, roles, immutable artifact storage, trusted approval logs, and enforcement through `complete_exact` (not legacy `complete`).

## Verification status
Added 12 standalone approval tests and 5 integration tests for workflow binding, stale changes, legacy approval rejection, persistence and denied completion. GitHub commit/file presence was verified. **A fresh full test run against the exact GitHub checkout could not be completed in the current runtime because GitHub DNS resolution failed.** CI status is not asserted.
