# Semantic quality evaluator — developer verification

- Evidence ID: `EVD-SEMANTIC-QUALITY-DEVELOPER-001`
- Task: `TASK-061`, runtime `work-3911e2660e3641f1be3840560a51465c`, attempt 5
- Change: `CR-013`; requirements: `REQ-025` Phase 2 local portion, `NFR-009`
- Design: `DES-060` v4, commit `38f5073`, SHA-256 `4611C6C9ADD08AE913E25512361B45369C1F439715CF620FCF875D7B51148B42`
- Evidence Status: `OBSERVED`
- Date: 2026-10-15
- Source commit: pending orchestrator commit; exact source hashes below bind this verification.

## Delivered implementation

The additive `python -m qa_master.semantic_quality` module implements local `validate`, `evaluate`, and `inspect`. It validates the published bundle, source/fact/oracle/category partitions and fixed resources; derives independent SHAPE, SEMANTIC, USABILITY and PROVENANCE rows; retains diagnostics without discarding intact sibling channels; applies canonical typed equality; and checks case/gap identity, readiness and reference bindings.

All new executable evaluator logic is in `qa_master/semantic_quality.py`, including the copied runtime-equivalent secret scanner. Four temporary implementation fragments were integrated and removed before final validation and wheel construction. No private executable dependency escapes the evaluator-byte identity. Six canonical JSON resources are packaged, loaded through importlib.resources and pinned by SHA-256 in the implementation.

Publication stages bounded data, exclusively reserves the result ID, verifies copied bytes and commits the manifest last. Inspection reads retained bytes without temporary files, process/network calls or execution of retained Python. It checks the installed/retained binding and uses the same pure derivation to detect a coherent profile-plus-manifest rewrite. No legacy grader, campaign behavior or installed design implementation was changed.

## Actual developer verification

| Check | Observed result |
| --- | --- |
| `D:\codex-rd-platform\.venv\Scripts\python.exe -m unittest tests.test_semantic_quality -q` | 42 tests passed, 16.474 seconds |
| `D:\codex-rd-platform\.venv\Scripts\python.exe -m unittest discover -s tests -q` | 648 tests completed, OK, 3 platform-specific skips, 123.732 seconds |
| Fresh wheel: system Python `-m pip wheel . --no-deps --no-build-isolation --wheel-dir .qa-master/task061/wheels` | Built successfully |
| New venv: wheel installed with `pip install --no-index` | Installed successfully |
| New venv `python -I .qa-master/task061/check-installed.py` | 42 tests passed against site-packages, 22.917 seconds |
| Installed resource reads | Exactly six resources; all exact bytes and SHA-256 match source |
| Isolated installed CLI in unrelated temporary cwd | validate returned VALIDATED_NOT_EVALUATED; evaluate returned EVALUATED_DRAFT_ONLY; inspect returned INTACT |
| Fresh project Codex skill installation | Evaluator and all six resources exact byte matches |
| `git diff --check` | Passed |
| `git diff --exit-code HEAD -- qa_master/paired_evaluation.py qa_master/paired_runtime.py docs/verification/evidence/paired-pilot-001 benchmarks/paired-pilot/public-development/oracles` | No differences |

Focused checks cover strict JSON boolean/integer distinction, decimal/integer/text/depth/node/reference/claim bounds, 256 versus 257 obligations, 256 observations versus overflow, 256 source/fact capacity, source byte bounds, category linkage, complete and duplicate cases, invalid optional cases/readiness, channel isolation, definite-reference precedence, unknown-only observation isolation, honest missing/conflict/source gaps, legacy projection, absent response, extensions, secret/claim rejection, process/network sentinels, racing publication, injected commit failure, inspection precedence, undeclared directories, role mutation, read-only inspection and coherent profile/manifest rewriting.

The first expanded run had one failing test because the developer fixture incorrectly set an ABSENT response's declared_projection_id to null. The fixture was corrected to retain the nonempty registered ID required by DES-060; all recorded final runs above include this correction. An initial pytest command found pytest absent; verification used the repository's unittest workflow. These were not product acceptance failures or independent findings.

## Exact artifact identities

| Artifact | SHA-256 |
| --- | --- |
| `qa_master/semantic_quality.py` | `65dd50954784b6eb8d632869cd95162b6f028ff6f63618ddd83739658a220295` |
| `tests/test_semantic_quality.py` | `5dba8c48ac46b048208f99afababc3e99424ac53773883676df4053bd9a3a994` |
| `contract.json` | `ec9d623230989ab75d0526a64531680280bfb38dde4e4b9f1a1c502e0433804a` |
| `projection.json` | `25aa3f1b01dbbe36d75c3e73f73d9256ded70a1d1780804d4f8c93c217ca4c55` |
| `legacy-paired-projection.json` | `de207a596e3e39203a0b6fecd2955a066c68e0096897d3695caa74fbbbe1f8f3` |
| `normalizer.json` | `a3c9d024e130425c3bc9594e775021e06869485c1f0681655971b97527b2c2d9` |
| `secret-scanner.json` | `fb26ef33f478e3c0340e02f70c0039cebb1b409b58991a2f68225d586fbd2176` |
| `result-schema.json` | `fd356165b1a97c7cd6f7e66aa7e326d3a427d890b5f57e4e7281e703af36247d` |
| fresh wheel | `59487f1136dc14c2e69f86a4a805a1253eab10b9dd844177f8c70cb0b312abdb` |

The fresh environment, wheel and installed verification script are local reproducibility artifacts under `.qa-master/task061/`; they are not committed production output. Tests create and clean their own temporary evidence roots. The wheel includes only the final integrated implementation, not temporary helper fragments.

## Handoff boundary

This is developer verification of public-development fixtures, not independent verification or acceptance. Independent tests and review remain `PENDING`. Human assessment, governed holdout ownership, comparison thresholds and evidence demonstrating superiority over Awesome QA Skills remain `NOT_AVAILABLE`. No model task, enterprise operation, target execution, rating, winner, approval, Gate or release conclusion was produced. The evaluator measures the bounded published contract only; it cannot substitute for a human QA assessment or prove broad product superiority.

## Corrected historical evidence check

The initial report command named a nonexistent `docs/verification/evidence/cr011` directory; that empty path comparison was not preservation evidence. Before freeze, the actual retained pilot tree and public oracle directory were verified to exist and compared against HEAD with `git diff --exit-code`, both with no differences. Current byte hashes follow; these are a live snapshot plus Git comparison, not an invented pre-task byte snapshot. No tests were rerun for this report correction.

| Existing file | Current SHA-256 |
| --- | --- |
| `docs/verification/evidence/paired-pilot-001/attempts/PE-BND-001-P1-A/final.txt` | `31ebcb9a1b10262315b0499297143ce8d7b482655e6d0a96e342246eb2dcae4d` |
| `docs/verification/evidence/paired-pilot-001/attempts/PE-BND-001-P1-B/final.txt` | `83bee59bb6ac1d7c530105127a4e35921085be859f594facced404109c78df71` |
| `docs/verification/evidence/paired-pilot-001/attempts/PE-DTT-001-P1-A/final.txt` | `54af8807268784bf818b1a05c658b5a78530fce224633960e371fc66cfeb7764` |
| `docs/verification/evidence/paired-pilot-001/attempts/PE-DTT-001-P1-B/final.txt` | `0a90dec8f758b9eb8344215f0668815ec8ac13f7a14c078a025d5560585bbd1c` |
| `docs/verification/evidence/paired-pilot-001/attempts/PE-STT-001-P1-A/final.txt` | `6a656922256cdce6385b61d2e493332bbae8d5207eaf5b3684a3d2c6ffd291de` |
| `docs/verification/evidence/paired-pilot-001/attempts/PE-STT-001-P1-B/final.txt` | `6a58f9a753bde3f47a1c9cf976d1f1a7c4feea29f2fbe7ce6180832ae263e9b6` |
| `docs/verification/evidence/paired-pilot-001/grade.json` | `8cfb753182db0ec0c325f3c0f0f8ac739a40e832a0e21165e23cf2ba3fda2c6b` |
| `benchmarks/paired-pilot/public-development/oracles/PE-BND-001.public-oracle.json` | `2ced8951c7fbce2b8830fa90df20f4b3e6abe9b067721b15efef21ca617a6a12` |
| `benchmarks/paired-pilot/public-development/oracles/PE-DTT-001.public-oracle.json` | `ce63e126ded22e18fcf740054059cf7205b9a1a46e0fddc33d5f6612cc722081` |
| `benchmarks/paired-pilot/public-development/oracles/PE-STT-001.public-oracle.json` | `50916d0d622854bc4d3057855b4dd3cd9fe6ddf5d6ac050e2870d38fc67299fd` |

## TASK-061 scoped repair — work-c016bfd9674149e6ac1bbc0cf685dbb0 v2 / attempt 2

This section appends repair evidence to the original developer record; the earlier source hashes, wheel and test outcomes remain historical. The repair starts from frozen `6905e02`. Its implementation commit is pending orchestrator freeze.

The independent attempt found two STRING_SET boundary manifestations (TC021 fact and TC022 observation) and malformed-manifest classification (TC023). A separate independent review identified case/gap fanout; that review finding was not an executed independent TC. This repair covers those three scoped defect types only:

- STRING_SET now allows at most 256 elements, consistently for facts and observations. A 257-member fact rejects validation; a 257-member observation receives OBSERVED_VALUE_INVALID.
- Inspection validates manifest field types and nested contract, digest, category, diagnostic, row, pointer-list, limitation and role structures before retained-file checks. Malformed manifests yield INCOMPLETE even with a missing retained file. Valid metadata that contradicts retained derivation continues to yield MISMATCH. Missing, changed or malformed installed assets yield MISMATCH / INSTALLED_DERIVER_MISMATCH; link/path/I/O command errors retain their own boundary.
- Derivation indexes mapped gaps once per obligation, caches exact gap validity and each case/obligation validity, and reuses the results for usability and diagnostics. Each case no longer rescans sibling gaps. Instrumented developer fixtures at 16, 32 and 256 cases/gaps verify exactly one _gap_valid and one _case_valid call per mapped item while preserving usability/provenance outcomes.

Actual developer verification: `D:\codex-rd-platform\.venv\Scripts\python.exe -m unittest tests.test_semantic_quality -q` completed with **47 tests passed in 21.505 seconds**. The preceding 46-test run passed in 23.606 seconds before the installed-asset-reason regression was added. `git diff --check` passed. No full-suite rerun or repaired fresh-wheel validation was performed in this developer repair; those belong to the separately frozen independent revalidation. The prior 648-test / original wheel results above do not validate these repaired bytes.

Repair source SHA-256: `189835888693ad727c8fc1dea269fe99cb7672d025872e85fe962877875070d8`.
Repair developer-test SHA-256: `54714ebcb202d122fe505fd90c2e6e9668fbc2c96405995875e55db53b38dc9e`.

Only `qa_master/semantic_quality.py`, `tests/test_semantic_quality.py` and this appended report changed in the repair. Packaged assets, independent tests, frozen failed-attempt evidence and historical paired records were not modified. Independent re-test/re-review remain PENDING; no Runtime completion, defect closure, acceptance or superiority claim is made here.
