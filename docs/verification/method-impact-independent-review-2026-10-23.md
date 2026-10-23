# CR-034 method impact independent review

- Review task: `TASK-141`
- Requirements: `REQ-032` through `REQ-036`, `NFR-014`
- Design: `DES-063` / `ADR-006`
- Initial reviewed product subject: `ebfc947`
- Final reviewed product subject: `5c516a66b82d51d9473e149a426421f003e4dc95`
  (runtime repair `58c73ec`; subsequent commit trims an independent-test EOF only)
- Document State: DRAFT
- Evidence Status: VERIFIED for the bounded source, independent test and
  installed-delivery review below.
- Review verdict: **PASS WITH P3 FOLLOW-UP**
- Final unresolved findings: **P0 0 / P1 0 / P2 0 / P3 1**

## Scope and conclusion

The final product subject implements the fixed finite-model change-impact
contract in the reviewed scope. It pairs candidates by exact typed formal bytes,
not whole-model candidate IDs or fuzzy meaning; separates requirement, source,
oracle and model context; retains baseline nonconformance, authored gaps,
obligations and unmodeled requirement changes; and produces bounded review
proposals without editing cases or executing tests.

This review covers `qa_master/method_impact.py`, the additive CLI route,
requirements/design, source and installed Skill instructions, teaching example,
developer and independent-test code, and retained installed-delivery evidence.
It does not establish requirement semantics, case-prose correctness, an actual
regression result, human acceptance, release readiness, a G0-G11 decision or
superiority over another Skill. Reports remain `DRAFT_UNAPPROVED` and
`NOT_EXECUTED`; `NO_DECLARED_IMPACT` does not authorize skipping regression.

## Finding history and recheck

### P2-001 / BUG-016 - explicit orphan gaps were lost - resolved and re-tested

On `ebfc947`, `gap_followups` iterated only known baseline candidates. An old
authored gap pointing to an unknown candidate therefore remained an orphan
finding but lost its authored reason and follow-up action.

The final runtime iterates every validated old gap occurrence, including
duplicates and orphan references, and maps known candidates through an index.
Developer and independent TC-IMPACT-007 regressions preserve duplicate orphan
gaps. This is a bounded repair/re-test result; it does not invent an external
defect closure.

### P2-002 / BUG-017 - action precedence suppressed concurrent reasons - resolved and re-tested

On `ebfc947`, action precedence replaced other applicable reasons. A baseline or
unresolved-obligation action could hide source/oracle/context change and
rebinding reasons from the row that a reviewer must assess.

Final row actions retain the union of applicable baseline, formal/context and
unresolved-obligation reasons while one action still follows the specified
precedence. Developer and independent TC-IMPACT-004/006/007 regressions passed.
This is bounded source verification, not an external defect closure.

### P2-003 / BUG-018 - public rejection codes were corrupted by nested adaptation - resolved and re-tested

The initial `_adapt` caught its own `MethodImpactError` through the generic
`ValueError` clause. Direct oversized input reported `INVALID_SCHEMA` instead of
`INPUT_TOO_LARGE`; `write_method_impact` double-adapted a correct stale-baseline
rejection into `INVALID_SCHEMA`. This broke the stable value-free public error
contract and made CLI remediation inaccurate.

The final adapter passes `MethodImpactError` through before adapting underlying
design/audit errors. Reviewer reproduction and the developer regression now
observe `INPUT_TOO_LARGE` for oversized input and `STALE_DESIGN_INPUT` from both
the writer and CLI, with no output file created. Independent TC-IMPACT-006/009
also passed; no external closure is claimed.

### P2-004 / BUG-019 - baseline MISSING identity was not actionable - resolved and re-tested

The packaged old library has one missing candidate, but CR-033 represents MISSING
in candidate state rather than `baseline_findings`. On `ebfc947`, the impact
report copied only the baseline summary and findings; it therefore exposed
`MISSING: 1` without the candidate identity. `gap_followups` was correctly empty
because no authored gap existed, so the impact report itself could not identify
the work item promised by the teaching workflow.

The final runtime adds controlled `BASELINE_NONCONFORMANT` to a candidate delta
when a before candidate is MISSING, DUPLICATE or MISMATCH. It does not fabricate
an authored gap. The packaged comparison now has ten `RETAINED_VECTOR` groups;
the exact missing old candidate is retained in one marked delta together with
rebinding and source-descriptor reasons. Requirements, design, README and the
installed reference describe the same distinction. Developer and independent
TC-IMPACT-002/006 checks passed; no external closure is claimed.

### P3-001 - Markdown digest code spans include trailing whitespace - open

The private Markdown renderer formats all three digests as `` `{} ` ``. A
generated line therefore contains a 64-character digest followed by one space
inside the code span. JSON identities and internal comparisons are exact, and
the installed module/helper completed successfully, so this does not affect
matching, safety or machine-readable integrity. Remove the three trailing spaces
in a later cosmetic patch so copied Markdown identities are visually exact.

## Architecture, correctness and safety observations

1. The matching dictionary is keyed by canonical bytes of `model_id`, `method`,
   `dimension` and typed `method_data`; SHA-256 is display-only. Boolean, integer
   and decimal-string values are not coerced. Requirement/model renames are not
   inferred.
2. A reviewer-constructed two-before/one-after formal group returned
   `AMBIGUOUS`, retained all three IDs and selected no arbitrary pair. The same
   check for obligations retained all IDs with state `AMBIGUOUS`. Candidate ID
   cardinalities are conserved by the grouping indexes.
3. Source-only descriptor churn changes engine candidate IDs while all ten
   teaching vectors remain retained. Existing rows request rebinding/review;
   there is no false ADDED/REMOVED churn.
4. Baseline validation is bound to the before design digest. Row identity uses
   normalized reference sets plus one-based duplicate occurrence; case/scenario
   order does not change the normalized library identity or sorted actions.
5. Existing CR-033 bounded JSON, depth, candidate, case/row, linked/reparse and
   exclusive-write helpers are reused. The additive route does not load campaign
   state, call a model/network/subprocess, open declared external source locators,
   modify inputs or overwrite an existing output.
6. JSON and private Markdown originate from the same report object. Markdown
   includes both design digests, the normalized library digest, counts, candidate
   and obligation deltas, row actions, baseline findings, authored gap followups,
   unknowns and limitations; permitted requirement text is escaped before table
   rendering.

## Reviewer and installed verification

Commands were run from `D:\QA-Master-Compare` against final product subject
`5c516a66b82d51d9473e149a426421f003e4dc95`:

```powershell
python -m unittest tests.test_method_impact -v
git diff --check 90a922667320756a758718b5002ca568d09436b5 5c516a66b82d51d9473e149a426421f003e4dc95
```

Observed results: 8/8 developer method-impact tests passed in 0.642 seconds and
the full-branch whitespace check passed. Reviewer-specific reproductions verified
the repaired stable errors, exact packaged MISSING identity, explicit orphan-gap
retention, ambiguity behavior and the open Markdown trailing-space finding.

The tester-owned clean-archive installed fixture is retained at
`docs/verification/evidence/cr034/delivery/delivery-metadata.json`. It binds to
the same final subject, built wheel SHA-256
`873d45fcd383f49dd188806feeff73a4b06700ffa4fad34817a5765ae41df6a6`,
installed 5,888 Skill files, and records exit 0 for source freeze, archive, wheel
build, fresh virtual environment, offline wheel installation, Skill installation,
isolated module CLI and installed helper. Both consumer entry points produced
`DRAFT_UNAPPROVED` / `NOT_EXECUTED` reports with nine review cases and all three
input identities. This is installed-delivery evidence, not execution of the
authored product test cases.

The separate tester-owned focused run executed TC-IMPACT-001 through 009 plus
the native Windows junction check: 11 tests ran, 10 passed, one ordinary symbolic
link check was skipped for unavailable account privilege, and there were zero
failures or errors. The equivalent native junction test passed. TC-IMPACT-010 is
the separate installed-delivery pass described above. Across the two executions,
12 test methods ran: 11 passed, one skipped, zero failed and zero errored. The
retained report is `docs/verification/method-impact-independent-test-2026-10-23.md`.

GitHub Actions cross-platform regression was still in progress when this review
verdict was written and is not represented as completed evidence here. The
reviewed source and installed scope has no unresolved blocker, critical or major
finding; P3-001 remains a disclosed cosmetic follow-up. This permits the bounded
TASK-141 verdict above, but it is not human acceptance, release approval or a
project Gate `PASS`.
