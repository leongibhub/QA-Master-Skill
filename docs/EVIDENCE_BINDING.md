# JUnit execution manifest binding

`qa_master.evidence_binding` provides a **bounded verification step** between imported JUnit XML and the internal release gate. It binds the exact SHA-256 of the test-result file to a declared project, build reference, environment, run ID and allowed Test Case IDs.

Example:
```python
from qa_master.junit_ingest import ingest_junit
from qa_master.evidence_binding import RunManifest,bind_junit
import hashlib
path='test-results.xml'
digest=hashlib.sha256(open(path,'rb').read()).hexdigest()
raw=ingest_junit(path,{('tests.api','test_health'):'TC-API-001'})
manifest=RunManifest('my-project','pinned-commit','staging','ci-run-42',digest,('TC-API-001',))
bound=bind_junit(raw,manifest,path)
assert bound['manifest_validated'] and not bound['source_authenticated']
```

**Security model:** A matching manifest SHA-256 demonstrates *consistency*, NOT that a trusted CI runner produced the XML. Even if a caller passes `verified_source=True`, this module deliberately retains `UNVERIFIED_EXTERNAL_ARTIFACT` provenance. The release gate still blocks release review until a separate authenticated, provider-backed attestation exists. No such attestation is implemented here.

Test cases: nine module unit tests covering normal binding, tampering, mismatched scope, malformed digest, duplicate/mismatched Case IDs, ineffective caller Boolean flag, and fail-closed release gate. Local complete project suite: **212 passed**. GitHub CI remains independently verifiable.

Next integration: validate source via GitLab CI API artifact endpoint and authenticated job identity; reconcile job commit SHA, project ID and protected pipeline parameters before any promotion to verified evidence.
