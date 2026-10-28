# CR-037 readable QA artifacts — independent review

- Artifact: `DOC-CR037-INDEPENDENT-REVIEW-001`
- Owner: TASK-156 reviewer `/root/rebind_reviewer`
- Baseline: `8a22a9f45f514c4cebd7be67317ed5044bc4cc28`
- Final instruction freeze: `94fd0b90e6a52d5e8e3391e6d78b135de498e767`
- Review state: `DECIDED`
- Evidence status: independent review `VERIFIED`; underlying authoring,
  installation and test observations remain `OBSERVED`.
- Final bounded verdict: `PASS`; unresolved P0/P1/P2/P3: `0/0/0/0`.
- Gate, release, human acceptance and external-write effect: none.

## Finding history

The source preflight found three P2 instruction-contract issues before freeze:

1. the canonical Skill required Chinese instead of the user's requested language;
2. the first reference draft moved essential commands, API paths, exact values,
   units, errors and IDs away from their applicable step/result;
3. the compact case summary could be read as permission to discard project or
   schema-required fields.

All three were repaired before final freeze. The canonical entry now follows the
requested language, Chinese examples are illustrative, essential technical facts
stay beside the relevant action or observable, and only long raw excerpts plus
trace/evidence metadata move to the support section. The reference and work
protocol explicitly preserve required risk, type, priority, oracle, automation,
approval and other machine fields in detail or compact metadata without renaming.

Subsequent review also clarified that supplied/reported actual results remain in
a defect draft with attribution even when the Agent did not reproduce them, and
that preparation steps must not receive invented intermediate expectations. The
final `94fd0b9` refinement keeps a narrow case/defect request focused instead of
automatically expanding it into a full strategy, dimension matrix, JSON handoff
or routing analysis.

BUG-032 (P2) is retained as a delivery defect rather than erased: the initial
documented `uv --force` refresh exited zero but reused stale package resources.
The existing-user update command now includes `--reinstall`; the repaired package,
managed update and independent file-map verification passed. BUG-032 is resolved
for this bounded delivery without implying closure of an external tracker issue.

## Requirements and architecture conformance

REQ-041 and REQ-042 are satisfied within the documented instruction scope:

- case details use concrete titles, known environment/data, ordered single-action
  steps, adjacent observable expectations, cleanup where known and precise gaps;
- defect drafts separate expected and actual results, preserve supplied actuals
  with provenance, and do not invent severity, frequency, evidence, root cause or
  remediation state;
- exact commands, API/error tokens, IDs, values, units, constraints and sources
  remain intact; required project/tracker/schema fields are not discarded;
- missing UI routes, messages, builds, thresholds, credentials, evidence and
  execution facts remain explicit questions or gaps, with affected artifacts
  draft and unexecuted;
- drafting, rewriting and import/tracker packet preparation grant no execution,
  approval, external-write or regression-skip authority;
- source and installed paths resolve through the canonical entry, work protocol
  and both original professional guides. The new reference is included in the
  packaged Skill bundle;
- English-request transfer was observed despite Chinese templates/examples. No
  private company knowledge-base body, URL, product identifier or command appears
  in the reviewed public diff.

The generator, runtime Python modules, audit/impact/proposal contracts, tracker
adapters, vendored specialist content and permissions are unchanged. Generated
placeholder rows remain candidates requiring source-grounded authoring; the new
guidance does not convert them into usable-case proof.

## Evidence readback

- The frozen baseline artifact and rubric precede the instruction edits. Baseline
  facts and permission boundaries passed; only R-READ-09 presentation failed.
- Fresh same-facts artifacts passed R-READ-01 through R-READ-10. The final focused
  English case/defect at `94fd0b9` also passed the narrow-request guard while
  preserving `DOC-FILE-EMPTY`, `sv-2`, `blank.txt`, `0 bytes`, `EMPTY_FILE`, the
  supplied `Upload complete` report and `NOT_EXECUTED` state.
- Root's final focused source/document checks ran 29 tests, exit zero. Frozen
  `git diff --check` passed; Python and vendored-skill diffs from baseline are
  empty.
- Repaired package session `22757` exited zero and exposed the new reference/rule.
  Managed session `34031` returned `UPDATED`, 5,891 files and
  `execution: NOT_EXECUTED`, retaining both backup archive and recovery tree.
- TASK-155 independently found exact equality across all 5,891 source-bundle,
  manifest and installed-file hashes. Reviewer readback independently matched the
  source and installed hashes for `SKILL.md`, `readable-artifacts.md`,
  `functional-api.md` and `regression-evidence.md`; the installed manifest is
  schema 1 and contains the new reference. The isolated installed helper returned
  330 vendor resources, 165 in each language.
- Root's final repeat of the managed installer returned `UNCHANGED`, 5,891 files
  and exit zero. The four staged sample Git blobs were byte-identical to their
  retained original hashes.
- The initial cached-package failure and the corrected evidence-location grading
  history remain preserved. Scoped `.gitattributes` protects the original output
  bytes used by the retained hashes.

## Limits

No real user-provided unreadable case or bug report was available; all authoring
examples are explicitly synthetic. These checks do not prove universal model
quality, future artifact correctness, human readability acceptance, business test
execution, tracker import, host UI discovery, or external defect closure. Git/PR
publication and main-branch identity require later readback and are not inferred
by this pre-publication review.
