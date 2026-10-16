# TASK092 independent test report: CR-018 skill-instruction upgrades

- Artifact ID: `DOC-SKILL-INSTRUCTION-OPTIMIZATION-TEST-001`
- Proposed evidence ID: `EVD-SKILL-INSTRUCTION-OPTIMIZATION-TEST-001`
- Runtime: `work-bf0f2585f8814f92a16a7ae84ec9030c`, attempt 1 / version 1
- Subject: `CODE-SKILL-INSTRUCTION-OPTIMIZATION-001` v1 at commit `c193774`
- Tester: independent (`/root/design_acceptance`); not the implementing developer
- Date: 2026-10-16
- Classification: `SOURCE_TRACE_ONLY_NO_QUALITY_VERDICT`. Bounded verification
  of instruction-asset content and packaging. No execution, rating, comparison
  or claim is made.

## Method

Read the committed bytes at `c193774` via `git show` (not the working tree),
checked each upgrade against its mapped CR-017 failure mode, verified the
commit touches only instruction assets, and traced the installer packaging
path (`qa_master/codex_skill.py::_files`/`skill_bundle`).

## Results

| ID | Check | Result |
|---|---|---|
| T1 | `functional-api.md` contains the both-side interior-step clause and the scale-violation rejection clause (declared precision, one place beyond scale) | PASS |
| T2 | `work-protocol.md` contains the mandatory gap taxonomy: execution observable, setup and cleanup preconditions, oracle source; a gap naming only the missing rule is declared incomplete | PASS |
| T3 | `references/typed-observations.md` exists with all four conventions (literal source tokens; uppercase-underscore synthesized labels with `BELOW_1000`-style examples; minimal observation values with explicit extra-member examples; declared precision preserved) plus the both-classes answer rule | PASS |
| T4 | `SKILL.md` wires the conventions reference into the method-selection path next to work-protocol/domains | PASS |
| T5 | Commit `c193774` touches only the four instruction assets; no `.py` engine/contract/schema file changed | PASS |
| T6 | Installer packaging (`_files` recursion over `skills/codex`, `.md` suffix included) automatically ships `typed-observations.md`; no packaging code change was needed | PASS |
| T7 | Full test suite re-run independently: 752 tests OK, 8 skipped (pre-existing Windows symlink branch skips) | PASS |

## Failure-mode mapping verification

| CR-017 failure mode | Upgrade | Mapped |
|---|---|---|
| B-arm missed interior neighbour 998 (BND-003) | both-side interior step points | yes |
| both arms dropped decimal precision / scale-violation candidates (BND-002) | declared-precision text + one-beyond-scale rejection | yes |
| free-form categorical labels (`standard`, `below 1000`) broke typed equality | literal tokens + uppercase-underscore synthesized labels | yes |
| observations carried extra members (`source_refs`, `classification`) | minimal observation values | yes |
| arm-A gap quality was spontaneous, not codified | mandatory gap taxonomy (execution observable, setup/cleanup, oracle source) | yes |

## Observation

The upgrades are instruction-layer only: they change what the skill tells the
model to do, not any engine, contract or schema. Their effect on actual
behaviour is therefore not proven by this test; it requires the CR-019
re-run under the unchanged CR-017 oracle. That re-run is the only valid
measure of whether the instructions changed behaviour.

## Verdict

7/7 checks PASS. The five upgrades are present, wired, mapped and packaged as
claimed. This verifies content and packaging only; no behavioural effect,
quality verdict or comparison claim is asserted.
