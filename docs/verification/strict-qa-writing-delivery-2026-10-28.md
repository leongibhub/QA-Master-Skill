# CR-037 strict-default follow-up delivery

Document State: DRAFT. Baseline main: `aaf8b1c`; prior read-only audit: `477ffe4`.
Fixed acceptance: `d4cdfcc`; final instruction freeze:
`e47c0f5d031f73bd150ca7c6f88377efab4e919f`.
REQ-041/042; DES-065; TASK-157–159.

## Changes

Every numbered human-facing case action, including preparation, now has its own
expected-result slot. Default presentation is step / operation / expected result;
an explicit project format may use an equivalent one-to-one mapping. Missing
expectations are precise pending questions for that step, never invented values.

Unrequested artifact/import metadata is excluded from ordinary prose. Real IDs,
source references and exact API/domain fields remain in the relevant steps and
expectations. Explicitly required raw artifact/import fields are preserved exactly
in a separate machine payload. Typed-observation activation is clarified without
changing its literal-token, precision or synthesized-label clauses. Bug templates
use clear reproduction, actual and expected sections and preserve report sources.

No Python runtime, generator, validator, audit/proposal schema, tracker adapter,
vendor source or execution permission is changed. This is a first-party authoring
instruction repair, not a deterministic proof of all future model outputs.

## Evidence

Historical outputs retain their earlier rubric results. Their unpaired preparation
step and unsolicited source_role/Trace are actual RED observations under the new
strict contract, recorded before instruction changes; no fake baseline is added.

Root ran the relevant instruction/registry/catalogue/installation-doc tests:
29 tests, exit 0, 1.966 seconds. Whitespace and protected-source checks passed.
Fresh independent authors produced ordinary login/bug, unknown-preparation and
explicit-schema probes. Their exact outputs and independent classifications are
under `evidence/cr037/strict-*` and `strict-qa-writing-test-2026-10-28.md`.
Independent fresh-probe evaluation is PASS (inapplicable checks stay N/A);
final independent review is recorded separately in
`strict-qa-writing-review-2026-10-28.md`.

The two professional-guide preflight P2 ambiguities about where required raw
metadata is displayed were corrected before freeze. Supplied API response fields
literally named source_role/Trace remain distinct from unsolicited metadata.

## Local propagation

Fresh package build: uv `--force --reinstall --link-mode=copy --python 3.13 .`,
foreground session `33842`, exited 0 (build preparation 1m54s, installation
17.35s). An initial Chinese-argument substring check failed with corrupted
expected text in the Windows command line; it was a verification-harness failure,
not counted as a product failure. Before any managed update, an ASCII-only
isolated byte comparison passed: the packaged readable reference exactly matches
the source (SHA-256 `8beeef378e1493d0cb12357a0cb2c871726901eababc10bedca3660297356288`).
The corrected managed-update process `48761` exited 0: UPDATED, 5,891 files,
with backup `qa-master.backup-afe157c111ff49fc8923e5061adada90.zip` and recovery
`.agents/.qa-master-recovery/qa-master.previous-afe157c111ff49fc8923e5061adada90`.
Independent schema-1 source/manifest/installed maps match exactly across 5,891
entries; six critical file hashes are retained in the test record. The backup ZIP
exists (6,607,992 bytes), and its prior recovery tree exists (5,902 files).
The isolated installed helper exits 0 and lists 330 bilingual resources
(165 per language). Root's final repeat installer returns UNCHANGED, exit 0.
The previously diagnosed cached-update failure is historical BUG-032; the repaired
reinstall route is used directly, without retrying the known stale-cache command.

## Publication and boundaries

Existing project Gates remain unchanged. No business test, live login/API request,
bug submission or old case rewrite is performed. Human acceptance and actual host
UI discovery are NOT_AVAILABLE/NOT_EXECUTED. Internal knowledge guidance was read
but its body, URL and company product details are not copied into public assets.

This is a pre-publication evidence snapshot. Actual PR, merge and main readback
are recorded later in Git history and the PR receipt, not fabricated here.

## Prompt provenance follow-up

The reviewer found that full dispatched probe inputs were absent from durable
evidence after the first classifications. The three original author task prompts
were then transcribed verbatim from this chat's dispatch calls into
`evidence/cr037/strict-prompts.json`. This is disclosed as a late capture, not a
pre-registered prompt hash or a new run. The acceptance/rubric was fixed before
edits; final independent factuality review rechecks the saved outputs against
these actual prompts, including their supplied echo/masking and unknown facts.
The initial provenance finding remains in the review history.

Final independent review: bounded PASS, zero open P0/P1/P2/P3 findings.
The input late-capture and Windows argument-harness histories remain explicit;
no runtime or instruction change follows the tested e47c0f5 freeze.
