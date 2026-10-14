# GitLab CI JUnit Artifact Fetch (Development)

The new `qa_master.ci_artifacts.fetch_job_junit` retrieves a ZIP artifact from a specified GitLab Job **only after** the job/pipeline metadata matches the pinned project, 40-character commit SHA, protected branch and environment.

It requires an exact ZIP entry path and rejects missing/duplicate JUnit entries, oversized ZIP/XML, excessive member counts, malformed XML, and unexpected test-case mappings. It computes archive and JUnit SHA-256 and binds imported results to the run manifest.

Example:

```python
import os
from qa_master.gitlab_adapter import GitLabReader
from qa_master.ci_attestation import ExpectedRun
from qa_master.ci_artifacts import fetch_job_junit
reader=GitLabReader(os.environ['QA_GITLAB_URL'],os.environ['QA_GITLAB_TOKEN'])
expected=ExpectedRun(123,456,789,'a'*40,'main','staging') # replace with real verified values
record=fetch_job_junit(reader,expected,{('tests.test_api','test_health'):'TC-API-001'},
                       junit_entry='reports/junit.xml')
```

The artifact transport supports deterministic mock testing. Use an authorized GitLab environment and read-only token.

**Trust limitation:** CI metadata consistency and downloading a ZIP over an authenticated GitLab API connection are not sufficient by themselves to grant release authorization. This implementation deliberately returns `source_authenticated=False`; the imported runs retain `UNVERIFIED_EXTERNAL_ARTIFACT` until independently trusted provenance and artifact approval are implemented. It does not write SynapseRT execution outcomes.

**Tests:** `tests/test_ci_artifacts.py` contains 10 targeted test cases. They passed in the local development environment. Full test suite was blocked by a stale local copy of `qa_master/gitlab_adapter.py` (an indentation error); no full remote HEAD green status is claimed.
