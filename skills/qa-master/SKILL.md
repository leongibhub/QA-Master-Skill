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

Before authoring or reviewing a reader-facing test case or defect draft,
including selected-specialist work and tracker/import packets, read
`../../qa_master/skills/codex/references/readable-artifacts.md`. This source-tree
path resolves the canonical readable-artifact contract; preserve required
machine fields while grounding human-readable prose in supplied facts.

When an Agent has authored cases from a finite design model, it prepares the
structured case library and runs `audit-method-cases` before delivery. The QA
user asks for this in normal chat and does not hand-fill JSON. Read
`../../qa_master/skills/codex/references/case-audit.md` for the schema, commands
and repair loop. Exact scenario binding checks only the formal model
representation; it does not establish prose correctness, executability,
approval or test execution.

When a saved finite model is revised, the Agent prepares the old bundle, new
bundle and old case library, then runs `impact-method-cases` to propose which
cases need review. The QA user asks for this in normal chat and does not
hand-fill JSON. Read
`../../qa_master/skills/codex/references/method-impact.md` for commands and
limits. The report is a declared finite-model comparison only: it never edits
cases, runs tests, grants approval or proves that regression can be skipped.

When the requested outcome is a reviewable, not-yet-applied after library, the
Agent prepares the same three inputs and runs `propose-method-case-library`.
Read `../../qa_master/skills/codex/references/case-library-proposal.md`. Its
JSON envelope contains a strict after-bound nested library plus every original,
case/row review reason, held case/gap and missing-vector context. Review every
case and row, including unchanged vectors. It has no apply path; the envelope
is not a `--cases` input. Only after human review may the Agent extract the
nested library to a new file and audit it separately.
