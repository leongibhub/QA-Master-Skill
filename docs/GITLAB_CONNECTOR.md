# GitLab read-only connector — V1.0 development milestone

The standalone `qa_master.gitlab_adapter.GitLabReader` performs GitLab REST v4 **read-only** operations. It is a real HTTP client when no mock transport is provided. It does **not** clone repositories, create commits, create Jira objects, execute tests, or automatically reconstruct a product's requirements.

Supported methods:
- `project(project_id_or_path)`: project identifier, namespace, default branch and web URL.
- `tree(project_id_or_path, ref='HEAD', max_pages=10)`: bounded recursive file inventory.
- `file(project_id_or_path, path, ref='HEAD')`: text file contents, blob ID and explicit `SOURCE_CODE_UNREVIEWED` provenance.

Example (do not hard-code credentials):
```python
import os
from qa_master.gitlab_adapter import GitLabReader
reader=GitLabReader(os.environ['QA_GITLAB_URL'],os.environ.get('QA_GITLAB_TOKEN'))
metadata=reader.project('group/project')
inventory=reader.tree('group/project',ref='main')
content=reader.file('group/project','README.md',ref='main')
print(metadata, len(inventory),content['path'])
```

## Configuration and security
- TLS/HTTPS is mandatory by default; internal HTTP GitLab requires explicit `allow_http=True`. Use a dedicated **read-only** GitLab token.
- Secrets are passed at runtime, not embedded in the repo.
- Responses and source files have size limits. Tree traversal has a page cap and reports incomplete inventory as an error.
- A GitLab source file is *observed implementation*, not a confirmed business requirement.
- Do not run this against an untrusted target, and do not feed arbitrary URL input directly into a privileged network environment without host allowlisting and access policy.

## Validation
15 local mock-adapter unit tests passed; no live GitLab service was accessed. The full local development test suite is reported separately. GitHub Actions results must be checked on GitHub before making cloud CI claims.

## Next integration
Add a version-pinned source crawler, explicit file allowlist, source-to-requirement candidate model, a human review stage and project-level configuration UI. Distinguish code-derived hypotheses from approved requirement baselines. 
