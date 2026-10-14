# JUnit XML import — original QA Master module

`qa_master.junit_ingest.ingest_junit(path,case_map)` parses a bounded, UTF-8-compatible JUnit XML artifact from an actual test runner. Requires an explicit mapping `(classname,testname) -> approved Case ID`. Rejects DTD/entity declarations, empty/unmapped/duplicate testcases, malformed XML, conflicting results, oversized files and duplicate mapping to one case.

Maps: success → PASS; failure → FAIL; error → BLOCKED; skipped → SKIPPED. Exports source SHA-256 and evidence references for correlation.

**Trust boundary:** imported XML is marked `UNVERIFIED_EXTERNAL_ARTIFACT`, and `release_gate.assess_release` now blocks `UNVERIFIED_SOURCE` when this provenance is present. The XML file cannot prove who ran the test, against which environment, or that its contents were not fabricated. Only an independently authenticated Runner/CI artifact verification step can upgrade provenance (not yet implemented).

Example:
```python
from qa_master.junit_ingest import ingest_junit
report=ingest_junit('test-results.xml',{('tests.test_api','test_health'):'TC-API-001'})
print(report['runs'])
```

Tests: local `python -m unittest discover -s tests -q` **203 passed** in the current working copy after the provenance gate update. Source files and tests were published via GitHub API; remote CI requires independent confirmation.

This is not a live Jira/SynapseRT connector and cannot automatically write execution results back to a test cycle.
