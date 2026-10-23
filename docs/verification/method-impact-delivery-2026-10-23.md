# CR-034 method impact delivery record

- Artifact: EVD-METHOD-IMPACT-DELIVERY-001
- Document State: DRAFT; Evidence Status: OBSERVED.
- Source baseline: main `90a922667320756a758718b5002ca568d09436b5`.
- Contract recorded before implementation: `895e824`; actual host assignments
  `030e17d`. Detailed contract is orchestrator-authored, not human baseline approval.
- Source, test, review and CI freeze identities will be recorded below when observed.

## Retained preflight history

TASK-138 initially reported three developer checks and 13 old audit checks passing.
Root then inspected the implementation and found four incomplete areas before
freeze: Markdown omitted most actionable report sections and row locators;
escaping did not cover all permitted requirement IDs; per-gap mapping scanned all
candidate groups; one-sided multiplicity did not yield AMBIGUOUS. The developer
was asked to repair these areas and expand direct checks. This initial state is
not the final tested implementation or an acceptance result.

## Initial frozen evidence (retained history)

Frozen `ebfc947` independent preflight additionally reproduced orphan explicit
gap loss, suppression of concurrent context reasons, error-adapter corruption of
MethodImpactError codes, and loss of the baseline MISSING candidate identity.
The first two have targeted repair regressions; stable errors and an explicit
BASELINE_NONCONFORMANT delta marker were requested. The DES clarification above
was reviewed as coherent by the independent reviewer. These are retained
pre-repair findings, not silently replaced historical results.

Implementation freeze: `5c516a66b82d51d9473e149a426421f003e4dc95`
(runtime `58c73ec`; subsequent test EOF trim only). Root independently ran the
eight developer checks successfully with ResourceWarning treated as an error.
The earlier combined root run passed 24 checks (seven pre-final developer checks,
13 unchanged audit checks, four README checks); the final additional developer
regression passed in the eight-check run. Old design/audit module SHA-256 values
remain byte-identical to main:

- case_conformance.py: 53e4d09690d0f012960f5ed8ea0835f3e25b3ee021d583750cafcbfb2f63b490
- design_methods.py: 764ec2d397d95adf5416e4c6050b5700c3b35726ee1b64ee371fe599af67e866

Full-branch diff check passed after trimming test EOF blank lines. PR #9 is a
draft; GitHub Actions run 39958666543 at the freeze is in progress at this
recording (Ubuntu jobs succeeded; Windows jobs pending). Final CI readback will
be appended after observation.

EVD-CR034-INDEPENDENT-TEST-001 records 11 focused methods (10 PASS / 1 symbolic
link privilege SKIP, native junction PASS) plus one separate installed-delivery
method PASS: 12 total, 11 PASS / 1 SKIP, no failure/error. The product is archived
from the exact freeze; the opt-in evidence capture harness and additional
symlink subcheck were authored after that freeze and do not change product bytes.

The clean archive wheel SHA-256 is
873d45fcd383f49dd188806feeff73a4b06700ffa4fad34817a5765ae41df6a6.
`evidence/cr034/delivery/delivery-metadata.json` retains source freeze, archive,
build, venv, offline install, 5,888-file Skill install, isolated module and helper
exits (all zero), notices/warnings, and output hashes. Both consumer commands
produce DRAFT_UNAPPROVED / NOT_EXECUTED with nine review cases. The teaching
comparison retains all ten formal points, marks the exact missing baseline
candidate, and makes no false added/removed vector claims.

Independent review is PASS WITH P3 FOLLOW-UP: unresolved P0/P1/P2=0, P3=1.
The nonblocking P3 is retained: Markdown digest code spans have a trailing space,
while JSON digests remain exact. See `../08-project-management/cr034-defect-record.md`
and the independent review for complete finding history. No project Gate,
acceptance, release or superiority conclusion.

## Late repair retained after initial delivery

Root identified and independent reviewer confirmed BUG-020 on `55594d7`:
an AMBIGUOUS group with two old IDs and one new ID populated the singular new ID
on both old case rows. This implied a pairing the contract does not establish.
Final runtime `c2e795716b9b37644476978402ecf50b32d281d4` limits singular
mapping to unique RETAINED_VECTOR groups; all ambiguous IDs stay in list-valued
candidate deltas/followups. Developer and independent targeted fixtures pass.
The same repair removes the previous cosmetic Markdown hash spaces.

Root's final-source developer run: 10/10 PASS. The initial wheel/install evidence
above remains bound only to `5c516a6`; it is not relabeled as final. The runtime
change justified one additional clean-archive installed verification, which
passed against the exact final runtime. Its evidence is retained separately at
`evidence/cr034/delivery-repair/delivery-metadata.json`; all source/archive/build/
venv/offline-install/Skill-install/module/helper exits are zero. Final wheel
SHA-256: 6b5cd4e4f76b5a81deee31e63c375e12790d88e4d368e940e4589cf1331b011f.
The final Skill has 5,888 files; both consumer reports retain draft/nonexecution
status and nine review cases. No release/merge is inferred from installation.

Final independent methods: 13 total (12 PASS / 1 Windows symbolic-link privilege
SKIP), no failure/error. The native junction check and separately authored
2-before/1-after ambiguity fixture pass. The final source review has no
unresolved P0–P3 finding; prior P3 and BUG-020 history remain above.

GitHub Actions run 39960201430 binds final runtime c2e7957. Final readback at
2026-10-23 13:38:08 UTC verified all four jobs succeeded:

| Environment | Python | Tests run | Failures | Errors | Skips |
| --- | --- | --- | --- | --- | --- |
| Ubuntu | 3.10 | 870 | 0 | 0 | 12 |
| Ubuntu | 3.12 | 870 | 0 | 0 | 12 |
| Windows | 3.10 | 870 | 0 | 0 | 3 |
| Windows | 3.12 | 870 | 0 | 0 | 3 |

Readback source: actual workflow-job completion and log summary, retained in
`evidence/cr034/final-ci-summary.json`. Final reconciliation commits contain only
documentation/evidence and the independently executed extra ambiguity fixture;
they do not change the tested runtime. Root also freshly ran that additional
fixture and the four README checks: 5/5 PASS. A documentation-manager read-only
consistency review found no current-final evidence/count/link conflict.
Earlier CI runs are historical; their results are not substituted for this
final runtime. PR #9's merge and remote readback remain separate GitHub/Git
events to be checked after this evidence commit. No project Gate, acceptance,
release or whole-product quality/superiority conclusion follows from CI.

## Operational boundary (unchanged)

Only declared finite models, requirement records and source/oracle descriptors
are compared. Exact formal-vector continuity is not semantic equivalence.
NO_DECLARED_IMPACT never authorizes skipping regression. External source bytes,
code-only changes, actual test execution and host chat discovery are not proven
by this offline feature. Reports remain DRAFT_UNAPPROVED / NOT_EXECUTED.
