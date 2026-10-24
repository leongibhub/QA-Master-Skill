# CR-035 finite audit hardening delivery

- Artifact: EVD-CR035-DELIVERY-001; Document State: DRAFT.
- Baseline main: 8fcaba97c14a12f447d2898d1902fff05576e996.
- Frozen repaired source: 8fc8533d4ec533bc5ba1ea66e6f24ef51a92f0f6.
- PR: https://github.com/leongibhub/QA-Master-Skill/pull/10.
- Scope: existing DES-062/063 and REQ-029–036 / NFR-013–014. No new
  schema/command, application regression run, model call or enterprise write.

## Reproduced and repaired behavior

| Defect | Repair outcome |
| --- | --- |
| BUG-021 | Wrong gap-reason types reject INVALID_GAP, not raw TypeError. |
| BUG-022 | Wrong model-method types reject INVALID_SCHEMA before preflight membership. |
| BUG-023 | Preparation and cleanup I/O failures reject through stable domain codes; cleanup cannot mask an existing OUTPUT_EXISTS or OUTPUT_IO_ERROR. Post-publication cleanup failure may leave the report present and is not reported as complete success. |
| BUG-024 | Wrong direct-API format types reject INVALID_FORMAT. |
| BUG-025 | Sparse open-world state models are bounded by explicit records, preserving the valid one-candidate model that was wrongly rejected by a state-trigger grid estimate. |
| BUG-026 | Public Markdown rejects impossible state/code/finding variants, including diagnostic case cardinalities; genuine emitter variants remain renderable. |

The design engine, valid audit/impact report schemas, source interpretation,
approval/execution states and no-overwrite protections are preserved. Strict
report validation establishes structural coherence, not source authenticity.

## Source verification

Initial independent RED runs and initial CHANGES_REQUESTED (five P2 / one P3)
are retained in the independent reports and evidence/cr035/task-142-initial.
Writer cleanup and finding-cardinality follow-ups were found before the final
installed freeze; intermediate 9579467 is not substituted for final 8fc8533.

Root freshly ran 41 focused tests: six developer hardening, 12 independent
hardening and 23 pre-existing audit/impact developer checks; all passed.
Root additionally ran 32 prior independent non-packaging checks: 30 passed,
two Windows symbolic-link-privilege skips (native junction checks passed).
The tester's later test-only aggregate-budget fixture is separate from the
frozen corpus: final independent suite has 13 tests, all PASS, exit0. Its first
invalid state-record fixture failure was retained and corrected as a fixture
issue, not a product defect; the final four individually valid 2,501-row
decision models prove aggregate preflight rejects before enumeration.

## Installed-delivery evidence

The first foreground tool handoff lost its wrapper exit outcome; an erroneous
second driver wrote to the same evidence target. That duplicate was stopped
only after its owned process/tree was verified. A coherent original command
chain remains as command-level OBSERVED evidence (19 commands: 13 exit0 and
six expected exit2 rejections); its wrapper exit is NOT_AVAILABLE. Early
snapshots are not additional trials, and mixed/shared snapshots are not the
authoritative final completion proof.

A final confirmation uses its own evidence/cr035/task-142-confirmed directory,
the exact frozen archive and a persistent exec session, with a fixed wrapper
that records its exit only after fixture cleanup. Final confirmation session
36511 returned tool exit0 and durable wrapper exit0. All19 coherent commands
match expectations (13 exit0, six prescribed rejection exit2). Exact final wheel
SHA-256:ee85671a0ea42f7136eb5491b1ad8619c2865639c5f4f6906c5e40810f762a7b,
6,399,339 bytes; archive identity is bound to exact frozen8fc8533.
The installer reports5,888 copied files; later target rglob observes5,900 files.
These are different observations and are not assigned an unobserved cause.
The normal module/helper audit outputs have matching hashes; module audit and
impact JSON/Markdown plus malformed-input/blocked-path rejections and direct
format-type rejection are observed from the isolated consumer installation.
The final completion proof is task-142-confirmed/delivery-result.json and its
tool-session-completion.json/command ledger; earlier task-142-final observations
are historical and not substituted for the confirmed wrapper exit.

## Independent review and CI

Independent frozen-source review: PASS, no unresolved P0–P3 product finding.
Installed confirmation and final full CI readback are complete. PR run40074191090
binds exact8fc8533. Actual completion/log readback at2026-10-24 07:47:53 UTC:

| Environment | Python | Tests run | Failures | Errors | Skips |
| --- | --- | --- | --- | --- | --- |
| Ubuntu | 3.10 | 889 | 0 | 0 | 12 |
| Ubuntu | 3.12 | 889 | 0 | 0 | 12 |
| Windows | 3.10 | 889 | 0 | 0 | 3 |
| Windows | 3.12 | 889 | 0 | 0 | 3 |

All four jobs succeeded; evidence/cr035/final-ci-summary.json records exact
job identities. The duplicate push workflow is not counted as additional test
coverage. Final reconciliation changes only evidence/docs and the separately
executed aggregate-budget regression; runtime bytes match the frozen source.
Root freshly executed that post-freeze regression:1/1 PASS.

## Ancillary cleanup outcome

After confirmation, root verified the owned interrupted fixture directory
`C:\Users\leon.wang\AppData\Local\Temp\t142-xaxef1hn` is an ordinary directory
under the intended Temp parent. Automatic approval review rejected recursive
cleanup with only `blocked by policy`; the command was NOT_EXECUTED and the
directory remains. No workaround/delete retry was attempted. This is a disclosed
environment cleanup limitation, not a product defect or missing installed proof.

## Boundaries

All generated reports remain DRAFT_UNAPPROVED / NOT_EXECUTED. This record
supports a bounded repair only, not case prose/business correctness, human
acceptance, release readiness, a project Gate PASS or competitor superiority.
All central G0–G11 statuses remain unchanged.
