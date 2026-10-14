# Source-to-requirements candidate pipeline

`qa_master.reverse_requirements` combines the bounded read-only `GitLabReader` adapter with a conservative Python AST inspection. The result is **source-linked candidate questions**, NOT a formal requirements specification.

## Usage

```python
import os
from qa_master.gitlab_adapter import GitLabReader
from qa_master.reverse_requirements import inspect_repository
reader = GitLabReader(os.environ["QA_GITLAB_URL"],os.environ["QA_GITLAB_TOKEN"])
result = inspect_repository(reader, "group/project", ref="PINNED_COMMIT_SHA")
print(result["candidates"], result["gaps"])
```

Use a pinned commit SHA, not `HEAD`, when baselining. The caller must obtain and record the actual commit SHA; the helper does not resolve it.

## Safety and quality
- Excludes common secrets and vendor/build directories; not a comprehensive secret scanner.
- Bounded file count and character count; records per-file failures and skipped files.
- AST analysis is Python-only. Other supported source file extensions are explicitly marked unsupported, never silently assumed analyzed.
- Functions are identified with source file, line, optional GitLab blob ID, requested ref and SHA-256 content hash.
- No runtime execution of inspected code. Never use current code behavior as the expected result for a formal test without human sign-off.
- No actual AI semantic business-rule reconstruction, multi-language parsing, or requirement approval. Those remain separate roadmap items.
- Test fixture validation is unit-level only; no enterprise GitLab live validation in this milestone.

## Approval handoff
1. Inspect generated candidate observations.
2. Run an AI requirements review with missing behaviors, source contradictions, permissions, reliability, safety, and performance assumptions.
3. Present a reviewable requirement draft to the human owner.
4. Only after approval, create an approved versioned requirements baseline and official test cases.
