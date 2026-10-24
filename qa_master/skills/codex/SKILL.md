---
name: qa-master
description: Review software requirements, derive source-linked test cases, or coordinate staged QA and regression in Codex. Use for QA tasks across Web/API, Linux systems and AI computing software, including work paused until a build is available.
---
# QA Master

Use Codex's reasoning and available tools to produce the requested QA work. This
skill includes professional guides and a local state helper; the helper alone is
not a semantic testing agent or an execution authority.

## Select an available specialist

For a specialist task, read its bundled `SKILL.md` and follow its relative
references. The installed library lives at
`scripts/qa_master/skills/vendor/awesome-qa-skills/{en,zh}/{testing-workflows,testing-types,skill-engineering}/{name}/SKILL.md`,
relative to this entry. In the source checkout, use the corresponding
`qa_master/skills/vendor/awesome-qa-skills/` directory. Prefer the user's language.
You can inspect these directories directly without Python; do not require a
separate upstream installation. Preserve the included license and attribution.

The optional local `plan` command described in the work protocol returns
`vendor_skills.selected` with actual file paths. It recognizes exact catalog
names and a bounded alias set: property-based testing / 属性测试, chaos engineering
/ 混沌测试, Playwright, and RAG testing / RAG 测试. RAG selects both retrieval and
answer-quality candidates and reports `AMBIGUOUS_SPECIALIST_REQUEST`; decide from
the user's sources which work applies, or ask if that distinction matters.
Unmatched names and missing files remain explicit gaps. This keyword helper does
not understand every natural-language request. If it misses the task, inspect
the actual catalog and relevant skill descriptions instead of inventing support.

Selection means reading guidance, not running tests or granting write access.
Preserve negative instructions independently (for example, run tests but do not
submit bugs). A specialist end-to-end testing request does not imply the full
QA lifecycle. Do not run a selected skill's external commands beyond the user's
scope, and do not claim execution from the mere presence of its instructions.

## Start with the requested outcome

Identify the project, requested stages, available sources, development stage,
expected deliverables and allowed side effects. Read supplied materials and saved
project answers before asking questions. Record an explicit "none" separately from
"unknown"; do not ask again unless the information changes.

- No materials: ask for a requirement, repository, deployed system, or description.
- Repository only: ask whether requirements exist. If not, read relevant code and
  dependencies in depth. Cite revision, path and symbols; observed behaviour is a
  candidate requirement, not its own correctness oracle.
- Deployed system only: agree the observation boundary, investigate within it,
  then derive and review requirements before formal testing.
- Development incomplete: review requirements and design cases now; save a
  `WAITING_FOR_BUILD` handoff. A missing build does not block design.
- One-stage request: finish that stage. Do not expand it into execution or imports.

Use [the work protocol](references/work-protocol.md) for deliverables, local state
commands, human decisions and cross-session continuation. Use
[domain guidance](references/domains.md) to select Web/API, Linux/system or AI
computing checks. Read only the sections relevant to the object. When a task
asks for typed observations or graded answers, apply
[the typed observation conventions](references/typed-observations.md): literal
source tokens, uppercase-underscore synthesized labels, minimal observation
values and declared precision.

## Select and apply professional methods

The installed helper is `scripts/qa.py`, relative to this SKILL.md. Resolve its
absolute path before invocation; keep the working directory in the user's project.
`python "<skill>/scripts/qa.py" skills` returns actual bundled guide paths. Read
the relevant guides and apply them to the supplied sources; listing guides is not
completing the work. If Python is unavailable, read the bundled guide files directly
under `scripts/qa_master/skills/professional/` and report the unavailable helper.

For a deterministic offline finite-model design, read
`references/design-methods.md`, select the applicable guide below, create the
strict non-secret bundle from supplied facts, and run:

```text
python -I "<skill>/scripts/qa.py" design --input bundle.json --output report.json
```

Review both `method_design` and `installed_design`. They identify draft method
candidates, declared source/guide mapping, and typed gaps; they do not prove a
case usable or executable. Produce a usable draft case for each determinable
obligation, or state the missing target, observable, cleanup, source, or oracle
fact as a typed gap. The packaged example at `examples/design-methods.json` is
instructional data only and has no approved requirement baseline. When you
design tables or transitions by reading instead of running the engine, mirror
its output discipline: enumerate the full fact-defined universe with one row
per combination or transition, classify conflicts as `CONFLICT`, rule-outs as
`EXCLUDED` and uncovered combinations as `GAP`, keep every stated field per
row, and keep extra candidate ideas in the case table rather than the typed
answer.

After authoring cases from a finite model, prepare the structured case library
and run `audit-method-cases` before delivery. The QA user asks for this in
normal chat; do not require them to hand-fill JSON. Read
[the case-audit reference](references/case-audit.md) for the exact schema,
commands and repair loop. An exact scenario binding proves only that the typed
row formally represents a declared candidate. It does not prove that the case
prose is correct, executable, approved or executed; inspect the source and the
case prose separately.

When a saved finite model changes, prepare the old bundle, new bundle and the
old case library, then run `impact-method-cases` before proposing regression
work. The QA user asks for this in normal chat; do not require them to
hand-fill JSON. Read [the change-impact reference](references/method-impact.md)
for the exact commands and review loop. Formal-vector continuity can show that
the declared input point did not change, but changed requirement, source or
oracle context still requires review. The report never edits cases, runs tests,
grants approval, or authorizes skipped regression.

When the user wants a reviewable after-version case library, prepare the same
before bundle, after bundle and old case library, then run
`propose-method-case-library`. The user remains in normal chat and never
hand-fills JSON. Read [the case-library proposal reference](references/case-library-proposal.md).
The JSON-only draft is non-applied and is not itself a `--cases` file: it holds
the strict after-bound `proposed_case_library` beside originals and mandatory
per-case/per-row review reasons. Review all cases and rows, including unchanged
formal vectors; preserve prose, hold whole cases for an ineligible row or
unresolved obligation, and hold every old gap for reason review. There is no
apply command, approval, execution, or regression-skip conclusion. After human
review only, the Agent may extract the nested library to a new file and run the
separate after audit.

| Work | Guide under `scripts/qa_master/skills/professional/` |
| --- | --- |
| Sources, conflicts, reverse requirements, missing rules | `requirements-review.md` |
| Functional, boundary, state, API and negative cases | `functional-api.md` |
| Branches, conditions, integration and async behaviour | `structural-integration.md` |
| Performance, load, stress, stability and compatibility | `nonfunctional-compatibility.md` |
| Security, authorization, failure and recovery | `security-recovery.md` |
| Change impact, regression, defects and evidence | `regression-evidence.md` |

Check applicability of functional, API, white-box, integration, performance,
load/stress, stability, compatibility, negative, recovery, security and regression
coverage. Report applicable work completed, blocked work with the missing input,
or N/A with a concrete reason. Missing SLA means propose scenarios and ask for
thresholds; never invent a passing threshold. A scenario counts as designed only
when its actions and observables are specified, not when its category is listed.

## Preserve decisions and evidence

AI review precedes human confirmation of formal requirements and case baselines.
Draft cases may be created while questions remain; identify which expected results
are conditional or blocked. Human confirmation applies to an exact scope and
version. Saved approval text documents a decision, not authenticated production
execution authority.

Before SynapseRT imports or Plan/Cycle creation, resolve the project, names,
create/reuse strategy and approved cases. Before defect writes, resolve the assignee
or existing policy. Before execution, resolve source/build, target, permitted tests
and existing authorization. Preserve authorized scope; request additional decisions
only when they are actually missing. This local helper has no enterprise write or
remote execution transport; use a verified integration when available, otherwise
produce an import/execution packet and state the gap.

For continuation, read the handoff, verify source and artifact hashes, and update
only impacted work. Changed requirements/code invalidate dependent expectations,
case approvals or previous execution evidence as appropriate. Never relabel old
results as observations against a new build.

Report draft quality, unexecuted tests, actual observations, confirmed defects and
remaining risks separately. Process exit 0 is not a business PASS. Do not assert
coverage of uninspected paths, execution that did not occur, or superiority over
another skill without a defined comparison and actual outputs.
