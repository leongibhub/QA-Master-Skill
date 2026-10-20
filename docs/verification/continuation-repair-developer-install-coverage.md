# Continuation repair developer verification — installation and covering metrics

- Date: 2026-10-19
- Tasks: TASK-113 (standalone vendor delivery), TASK-114 (interaction metric)
- Change: CR-028
- Source freeze: `0ff9ad47ab0d442dff2157f6bf7d10e322a83f75`
- Scope: developer verification only; independent acceptance and complete product superiority are not established here.

## Changes

The standalone installer now copies the packaged inventory of 5,819 vendor assets, including LICENSE, YAML, CSV and linked supplementary files, into its bundled helper package. Inventory paths are validated; filesystem links/reparse points are rejected before resource reads. Unlisted source-tree additions are not copied. The inventory itself is shipped so installation from an installed helper remains self-contained. Existing managed-update, backup and conflict rules are retained.

Covering-array `coverage.candidate_ready` and `coverage.oracle_missing` now count distinct t-way interactions, matching `coverage.denominator`. `analysis.candidate_row_count` and `analysis.oracle_missing_row_count` separately report row counts. These values describe draft design coverage, not executed test success. No consumer in the Python product interprets candidate_ready as row count outside its method's declared denominator.

## Actual verification

Python: `D:/codex-rd-platform/.venv/Scripts/python.exe`; Windows; checkout `D:/QA-Master-PR2`.

| Command / check | Observed result |
|---|---|
| `python -m unittest tests.test_design_methods -q` | 30 tests, 0.456 s, OK |
| `python -m unittest tests.test_vendor_install -v` | 3 tests, 51.687 s, OK |
| `git diff --check -- qa_master/codex_skill.py qa_master/design_methods.py tests/test_design_methods.py` | exit 0 |

The installation test uses an actual package-resource snapshot for its two install calls. It verifies every inventory byte against installed files, executes the installed helper outside the checkout with `-I`, discovers 330 skill directories (165 English / 165 Chinese), selects design guides whose paths exist inside the install, and observes UNCHANGED on the repeat install. Only the bundle snapshot is fixed during that test; helper results, discovery and filesystem operations are real. Separate inventory tests exercise unlisted junk exclusion, traversal/invalid-path rejection and the link-rejection branch (mocked link predicate, not an actual link claim).

Metric tests explicitly verify six selected rows cover sixteen distinct pairs; missing oracle yields zero ready / sixteen missing interactions. Four-parameter strength-three tests independently recompute thirty-two distinct triples, for both present and missing oracle, with fewer selected rows than interactions. Existing design-method tests remain green.

### Earlier attempts retained as developer observations

- First combined test run: 8 tests, 50.014 s, one failure. New test used the nonexistent `case_authoring` stage; fixed test input to actual `design` stage. Discovery and asset-byte checks had passed.
- Second installer run: 3 tests, 60.642 s, one error. Shared source files changed between the two `skill_bundle()` calls, so installer correctly required an update. This is not classified as a product idempotence defect. The final test captures one immutable resource snapshot to isolate repeat-install behavior during parallel development.
- Early strength-three test used candidate `method_data` for obligations; corrected test access to actual obligation `subject`. Final complete module result is recorded above.

## Source and test hashes (SHA-256)

| File | SHA-256 |
|---|---|
| `qa_master/codex_skill.py` | `30DA7CD4153D8BF51E6EF2163B5E05A00EE55BB71DEBC56783C1D2EAD3D530AE` |
| `qa_master/design_methods.py` | `764EC2D397D95ADF5416E4C6050B5700C3B35726EE1B64EE371FE599AF67E866` |
| `qa_master/skills/vendor-files.json` | `3EEE20918E72F05A1502B12B196A4939E4D3006E0B0D160DFC425C8A084F5D21` |
| `tests/test_vendor_install.py` | `DEABC9308F7E89EDF7D1AB5A7A5C3A9BAD298251346D127D333966AC9F8A96C3` |
| `tests/test_design_methods.py` | `79F5096F54294C699C420FD50BF9E0EC51E64D0BD89FCC52768458A880754FB4` |

## Remaining verification boundary

Fresh-wheel installation, independent regression and independent review are assigned outside this implementation task. No upstream assets or network resources were changed by this developer. The inventory covers the current pinned asset set and must be deliberately refreshed when vendor resources change; recursive untracked-file discovery is intentionally not used.

## Legacy managed-update compatibility

`python -m unittest tests.test_codex_skill.CodexSkillTests.test_managed_upgrade_keeps_restorable_archive tests.test_codex_skill.CodexSkillTests.test_upgrade_rename_failure_restores_original -v`

Observed terminal result: **2 tests, 194.237 s, OK**, exit 0. The unchanged legacy tests exercised actual full-bundle update/archive creation and injected publication-rename failure followed by original-tree restoration. This run began before the final freeze; the product installer and metric source hashes above remained unchanged through completion. It supplements the 33 focused tests; it is not the independent fresh-wheel/full-suite result.
