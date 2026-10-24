# README and local Skill maintenance

Document State: DRAFT. Evidence status: OBSERVED where recorded below.
User request: update the GitHub README and the already-installed local QA Master.
Baseline main: `89d095f0dee555d3b51601e24a88e29bfd781a7f`.
Branch: `codex/readme-local-skill-update`.

## Scope and actual owners

- TASK-152: `/root` coordinates package/managed Skill synchronization, evidence
  and Git publication; `/root/rebind_docs` owns only the concise README revision.
- TASK-153: `/root/rebind_tester` independently checks installed artifacts and
  smoke behavior; `/root/rebind_reviewer` independently reviews README claims
  and the final maintenance evidence.

This is maintenance of existing CR-036 behavior and CR-031 installation guidance,
not a material requirement change. No runtime or Skill behavior change is planned.
Project Gates, human acceptance, external systems and business test execution
remain outside this scope. Actual host registration is NOT_AVAILABLE; these are
Codex host assignments, not Runtime leases.

## Initial readback

The existing `qa-master` executable was installed by uv from `D:/QA-Master-PR2`.
Its help did not include audit, impact or proposal commands. The standard
`~/.agents/skills` directory existed but was empty. No QA Master target was found
in the checked user Codex, Claude, OpenCode or TRAE CN Skill directories.

README already had detailed finite-model commands, but no concise user task /
chat prompt / output table for the audit-impact-proposal flow. Its local-tools
paragraph incorrectly implied an activated virtual environment was necessary.

## Results

Package update: OBSERVED, uv foreground session `8234` exited 0. Command:
`uv tool install --force --link-mode=copy --python 3.13 .` from the current
repository. The uv receipt now points to `D:/QA-Master-Compare` rather than
`D:/QA-Master-PR2`. Distribution version remains `1.0.0`; source identity, not
that unchanged version string, establishes this update. Runtime and bundled
Skill content match baseline main `89d095f` (product freeze `ddb2fc2`).
Managed user Skill installation: OBSERVED, foreground session `87769` exited 0.
`qa-master install-codex --user --update` returned `INSTALLED`, target
`~/.agents/skills/qa-master`, 5,890 files, no backup/recovery directory and
`execution: NOT_EXECUTED`. This is a fresh complete Skill target because the
standard directory was empty; the pre-existing uv command package was updated.
No old Skill or local customization was overwritten. TASK-153 independently read back exact equality between all 5,890 source,
manifest and installed-file hashes. An additional root repeat of the managed
installer returned `UNCHANGED`, exit 0, confirming the final installed target.
Independent tests: bounded PASS in `readme-local-update-test-2026-10-24.md`.
The installed helper ran outside the source repository in isolated mode: three
new command help routes, 330 bilingual resources (165 logical skills), and the
teaching proposal all exited 0. Proposal output contained 9 proposed cases and
1 missing vector and retained draft/nonexecuted/nonapplied states. Its harmless
teaching JSON is intentionally retained in a new temporary directory; no cleanup
failure or business execution is inferred.

Final README documentation/catalog checks: 10/10 PASS, exit 0 (0.109 seconds);
`git diff --check` passed. Only README and verification records change; runtime,
Skill assets and packaging have an empty diff from baseline. Independent review
is recorded separately in `readme-local-update-review-2026-10-24.md`.
Git publication: PENDING at this pre-publication record.

Actual chat-host discovery/invocation is NOT_EXECUTED. Successful installation,
file/hash checks and local helper smoke checks do not prove host UI loading or
business-case correctness.


## Publication receipt boundary

This committed maintenance record is a pre-publication snapshot. The eventual
PR number, merge commit and main readback are recorded in Git history, the PR
body and the final user reply, rather than invented before publication.
