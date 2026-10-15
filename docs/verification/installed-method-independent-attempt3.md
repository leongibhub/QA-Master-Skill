# TASK-057 independent installed workflow retest — attempt 3

Subject 8b5017af42c7675cd32f941b71c85cf79b30d499; Runtime work-866f7a327bb84f33b8939f65dd385af0 version9/attempt3. CODE-INSTALLED-METHOD-WORKFLOW-001 v3. Scope REQ025/NFR009, DES055, BUG014 targeted documentation retest. This report records observed independent evidence, not defect closure or a Gate/acceptance decision.

## Automated verification

8 focused tests PASS (4.926s), including the original seven plus TC-IMD013 positive/negative legacy semantics checks. A new wheel was built with system Python, installed into a new venv, and the same eight tester-owned checks passed against site-packages (5.497s). TC-IMD013 checks complete tester-owned requirement and installed example produce nonempty generic cases without missing-content/provenance/acceptance findings; removing each field yields its expected finding; draft approval is retained. Existing isolated CLI, finite method, sentinel, mapping, determinism and side-effect checks remain exercised.

The first focused run failed only a new tester assertion requiring literal `case_count` wording in reference. That spelling was not a requirement; it was removed while behavioral count assertions remain. Original failure, correction explanation and retest logs are retained. No product change was made by tester.

Product delta against prior f62932b is exactly reference/example (66 insertions/1 deletion), no engine changes. Prior full strict result remains scoped to that prior attempt: 605 tests OK with three Windows symlink privilege skips. Full strict was deliberately not repeated for this documentation-only retest, per assigned scope; no new 605-test execution is claimed.

Commands: `python -m pip wheel . --no-deps --no-build-isolation --wheel-dir .qa-master/cr013-independent-attempt3/wheels`; new venv and `pip install --no-index <wheel>`; venv Python `-I -m qa_master install-codex --project <external temp project>`; `python -W error::ResourceWarning -m unittest discover -s tests -p test_installed_method_independent.py -v`; venv Python `-I -W error::ResourceWarning docs/verification/evidence/cr013-independent-attempt3/run-installed-tests.py`. Logs and exact actual-task invocation reside in the evidence directory.

## Actual task and review boundary

A new fork_turns=none execution agent received only new installed Skill/materials, same frozen facts, unrelated cwd, output directory and offline design restrictions. Neither prior failure nor corrective field names/expected answers were supplied. Source SHA256 A52B944D6A6D406C40090AED4C4E2680263D8A9BA96955571421A72631284B7C is unchanged. Instruction/read scopes are recorded; isolation is not OS-enforced. Tester oracle ledger was not supplied to the task agent. No product execution or external writes occurred; all quality review remains AGENT_REVIEW_ONLY.

Historical attempt2 FAIL/P2 report and manifest hashes were rechecked unchanged: CC65CC9A1B8C6FF01470FB37500792DDEC6BA726E0F19A12319ACDC00C032E97 and 8F7E71A22D7B5F7758A54A5CB211384847E06757EA3F5D8FAFF235822919F9E5. This attempt does not overwrite their observations.

## Observed task result

Installed helper exited 0. Three source-grounded requirements supplied text/source/acceptance, and requirement review returned zero findings. Generic projection contains 3 draft cases, expected acceptance strings and declared source locator; three UNAPPROVED_TRACE issues and PENDING_HUMAN remain. Generic setup/actions are still placeholders, explicitly noted by author; generic counts alone do not demonstrate usable cases. Finite projection has 13 candidates and zero finite-model obligations; zero obligations does not imply complete QA facts.

Execution agent read 10 installed resources (recorded hashes); packaged example is not among its recorded reads. It completed 14 policy drafts (13 candidate-linked plus explicit initial DRAFT state) and 15 typed gaps. Tester inspected every finite row and ran an independent artifact checker: six exact boundary points/classes, four boolean rebate assignments, three declared transitions, unique complete candidate links, source/gap references and unapproved/unexecuted statuses match supplied facts. DRAFT publish only asserts remaining DRAFT and explicitly does not assert other persisted data; unspecified pairs remain gaps. Initial-state draft matches F-03. Setup, observable binding, cleanup, target, environment, authorization and thresholds remain missing rather than invented.

Ledger IMD-O01..O05 SATISFIED for finite supplied policy semantics; O06 SATISFIED for explicit missing-fact gaps; O07 SATISFIED only for reviewable policy drafts, not executable readiness; O08 SATISFIED for actual installed read/author/invoke route; O09 SATISFIED for evidence/claim limits. The independent artifact checker checks structure/exact finite values, while expected-text/source sufficiency was reviewed by tester; neither is a human judgment. Additional requirements beyond supplied facts remain ORACLE_MISSING/unspecified.

Targeted BUG014 symptom was not reproduced in this new attempt: generic fields were authored from installed documentation without corrective prompt hints, and missing-field findings are absent. This is retest evidence only, not a unilateral defect closure or overall project acceptance decision. All final cases remain DRAFT_UNAPPROVED/NOT_EXECUTED with incomplete target bindings; quality-superiority, pilot, release, human approval and Gate conclusions are outside scope. Original attempt2 failure remains intact.
