# Release Quality Gate — executable module

Implementation: `qa_master/release_gate.py`.

This deterministic gate evaluates case records, execution-result evidence, approved case identifiers, waived skips, and defects. It returns only:
- `BLOCKED`: release review cannot proceed.
- `READY_FOR_HUMAN_REVIEW`: evidence conditions passed but final release still requires an authorized human decision.

**Important rules:** unknown defect status blocks; unknown or duplicate run IDs are rejected; PASS/FAIL without evidence cannot be counted as evidenced PASS; unapproved cases block; unapproved SKIPPED cases block; all-skipped or zero-evidenced-PASS runs block even with waivers; no test cases block. It does not authenticate approval identities or verify evidence content. It cannot issue a deployment or release.

Local verification in the working project: `python -m unittest discover -s tests -q` — **188 tests passed** including 20 release gate tests. GitHub Actions must be checked separately for the public commit.

Example:
```python
from qa_master.release_gate import assess_release
assessment=assess_release(
  cases=[{"id":"TC-1"}],
  runs=[{"case_id":"TC-1","status":"PASS","evidence":"artifact://run/1"}],
  defects=[],
  approved_case_ids={"TC-1"}
)
print(assessment.to_dict())
# READY_FOR_HUMAN_REVIEW; NOT approval to deploy.
```

Still missing: authenticated release approver, SHA-based case/test-run provenance, immutable evidence storage, test plan/cycle completeness reconciliation, and actual Jira/SynapseRT connectivity. Use only as a supporting safety check.
