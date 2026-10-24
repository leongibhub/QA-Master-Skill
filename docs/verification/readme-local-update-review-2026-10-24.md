# README and local installed-Skill update — independent review

- Artifact: `DOC-README-LOCAL-UPDATE-REVIEW-001`
- Owner: TASK-153 reviewer `/root/rebind_reviewer`
- Baseline: `89d095f0dee555d3b51601e24a88e29bfd781a7f`
- Branch: `codex/readme-local-skill-update`
- Review state: `DECIDED`
- Evidence status: independent review `VERIFIED`; underlying installation and
  test observations remain `OBSERVED`.
- Final bounded verdict: `PASS`; unresolved P0/P1/P2/P3: `0/0/0/0`.
- Gate, release and acceptance effect: none.

The review compared the README working-tree change with baseline main and used
`readme-local-skill-update-2026-10-24.md` as the persisted maintenance contract.
This repository has no `docs/agents/issue-tracker.md`; no issue-tracker evidence
was inferred. The current user request, maintenance record, existing installer
implementation and installed-test record provide the bounded specification.

## Standards axis

No open documented-standard violation or applicable smell-baseline finding was
found. The README continues to present QA Master as one self-contained product,
uses only existing audit, impact and proposal routes, and retains approval,
execution and external-write boundaries. It does not claim that any chat host
discovered or invoked the installed Skill.

One P3 wording issue was found during review: the first draft said that
`--update` “will keep a backup,” which could promise a backup for a no-op update.
The installer returns `UNCHANGED` before backup creation when installed bytes
already match. README now states that an unchanged target returns `UNCHANGED`
and that a backup is retained only when changed content is actually updated.
The reviewer read back the corrected wording; this P3 is resolved.

## Specification axis

The final README satisfies the requested maintenance scope:

- Windows users can run the source module with Python 3.10+ without creating or
  activating a virtual environment; the uv-installed `qa-master` entry point is
  distinguished from the current-checkout module entry point.
- Updating a managed Skill retains the original host and target. User-level
  `--user`, project-level `--project`, and explicit `--target` installations are
  not mixed, and Claude Code / TRAE CN targets are not redirected to the shared
  Codex/OpenCode directory.
- The managed-update guard is accurate: manually modified targets are rejected;
  a real managed update keeps the old installation backup; identical content is
  `UNCHANGED`.
- The audit, impact and proposal table names the existing commands and accurately
  limits their outputs. A proposal remains unapplied and unexecuted, requires
  human review, has no `--apply` route and is not approval evidence.
- The existing operation-guide link resolves, and no runtime, Skill asset or
  packaging change is present relative to the baseline.

No missing requirement, scope expansion or incorrectly implemented claim remains.

## Evidence readback

- `python -m unittest tests.test_installation_docs tests.test_readme_catalog -v`
  ran 10 tests and returned `OK`; the reviewer-observed run took 0.113 seconds.
  Root's final post-wording run independently retained 10/10 PASS in 0.109
  seconds.
- `git diff --check 89d095f` returned no error.
- TASK-153 independently matched all 5,890 source-bundle, manifest and installed
  file hashes. The installed helper exposed all three routes and 330 bilingual
  resources; its teaching proposal returned 9 proposed cases, 1 missing vector,
  `DRAFT_UNAPPROVED`, `NOT_EXECUTED` and `NOT_APPLIED`.
- Root's repeat installer readback returned `UNCHANGED`, 5,890 files and exit 0,
  consistent with the corrected README semantics.

The package and user Skill installation evidence does not prove VS Code, Codex,
OpenCode, Claude Code or TRAE CN UI discovery. No business test was executed, no
external system was changed, and no human acceptance, release, Gate or product
superiority conclusion is made. Git publication remains a later readback rather
than an inferred result in this pre-publication review.
