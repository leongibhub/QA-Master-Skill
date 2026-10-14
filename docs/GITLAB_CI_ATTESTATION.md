# GitLab CI metadata assessment (development)

The module `qa_master.ci_attestation` compares a manually specified `ExpectedRun` with **live GitLab REST v4 job and pipeline metadata** obtained using the read-only GitLab client. It checks project ID, job/pipeline IDs, full commit SHA, ref, protected-ref flag, job/pipeline success state and job environment.

Example:
```python
from qa_master.gitlab_adapter import GitLabReader
from qa_master.ci_attestation import ExpectedRun,assess_ci_job
import os
reader=GitLabReader(os.environ['QA_GITLAB_URL'],os.environ['QA_GITLAB_TOKEN'])
run=ExpectedRun(project_id=123,job_id=456,pipeline_id=789,commit_sha='a'*40,ref='main',environment='staging')
result=assess_ci_job(reader,run)
print(result['metadata_matches'],result['reasons'])
```

**Important security limitation:** matching job and pipeline metadata does **not** authenticate a JUnit artifact. The result deliberately retains `artifact_authenticated=False`. The release gate should continue to block imported results until the artifact itself is downloaded from the verified GitLab CI job and cryptographically bound to its provenance through a trusted execution path. The caller must supply actual, independently checked IDs and hash—not fabricate them.

Validation: 12 new CI metadata unit cases using a mock GitLab reader passed in the local test run. The local checkout used for testing did not contain the complete latest GitHub adapter; a separate, partially stale local adapter caused four additional tests to fail until its mismatch was identified. Do not claim a full latest-commit GitHub checkout green without running GitHub Actions.
