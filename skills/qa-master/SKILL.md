---
name: qa-master
description: Review requirements, design source-linked software tests and coordinate staged QA in Codex.
---
# QA Master source-tree entry

Read `../../qa_master/skills/codex/SKILL.md`, relative to this file, for the
canonical workflow and its linked references. This source-tree entry preserves
existing repository instructions; it is not the standalone installation bundle.

Install the complete skill with `python -m qa_master install-codex --user`, or
`python -m qa_master install-codex --project <project-directory>`. The installer
copies the canonical entry, references, professional guides and local helper into
one discoverable skill folder. No separate QA Skills repository is required.

When an Agent has authored cases from a finite design model, it prepares the
structured case library and runs `audit-method-cases` before delivery. The QA
user asks for this in normal chat and does not hand-fill JSON. Read
`../../qa_master/skills/codex/references/case-audit.md` for the schema, commands
and repair loop. Exact scenario binding checks only the formal model
representation; it does not establish prose correctness, executability,
approval or test execution.
