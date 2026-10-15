# TASK-042 independent paired-runtime verification

- Document State: DRAFT
- Evidence Status: OBSERVED
- Current verification result: PASS for the exercised final combined subject, with explicit environment skips. Historical contract and concurrent-initialization failures remain preserved below.
- Tester: `/root/design_acceptance`, independent of product implementation.
- Runtime work: `work-bbb7cf3e5bc8440eb0469d2e722a1754`, final combined attempt 4/version 11; earlier attempts are historical and invalidated.
- Actual model calls: 0. Test doubles and local Python child processes are not pilot evidence.

## Subject and provenance

Active worktree: `D:/QA-Master-PR2`. Initial inspected HEAD was `412109e`; repaired subject is `1e77810e`. Before repair, the three paired runtime files had identical Git blobs to frozen implementation commit `0d712c8902633902cabe07fa0e20a7881b036c8c`. Checkout CRLF conversion changes exact working bytes; these are recorded separately rather than falsely claiming exact frozen-byte equality:

| File | Current exact-byte SHA-256 | LF-normalized frozen SHA-256 |
|---|---|---|
| qa_master/_paired_contract.py | 94310ae24d7427962d12d1b9dbe89527fdfe7ee436c2f495b9cdef5e0f73ae0f | 223f1fa8bdb961c591ed1297ea301433abc54ea5a0b083c0302e0cc70ffd2353 |
| qa_master/_paired_process.py | 3155104b5625f99a9fb60a125f9078315d1092a65317d92a9b1bc5afeae8e700 | 409c5d5dcfe3cd029e3bf78c2681eca9a1eb9880c6242cf7dda7bf10dc2cf8fe |
| qa_master/paired_evaluation.py | 0401c3aa4814cc46c250c546ea414643d5076d6608b049bbb3d2f4b601bca8ef | 0b1b340166e389db4e43ed185565ba17842b956c71b623d918415e35bc0656dd |

Product source and developer tests were not edited. Independent fixture construction, expected statuses, envelopes, and process captures live in `tests/test_paired_runtime_independent.py`; developer fixture/oracle code was not imported. Fixed public prompt/schema constants are consumed as the required wire contract.

## Observed contract failure

TC-PE-221 follows frozen DES-040 section 5: every observation value uses string transport, including INTEGER value `"7"`. All six fake participant calls returned `OUTPUT_INVALID`, where design-conforming responses should produce `COMPLETED_PROCESS`. The runtime currently requires native JSON integer values instead. Evidence: `evidence/cr011-independent/design-contract-failure.txt`.

The initial twenty behavior tests did not override this normative mismatch. The registered architecture clarification `DOC-PAIRED-VALUE-ENCODING-CLARIFICATION-001` (SHA-256 `63acdff1d09c5149d53e58a3cb2b4bf975bd6bc0534a75d2b79cb96017f4a79d`) prospectively adopted native typed JSON and required bounds/strictness repairs. TASK-049 completed those repairs before this new attempt. Historical TC-PE-221 source remains `evidence/cr011-independent/historical-test-source-tc221.py.txt`; its failure has not been reclassified as a pass.

## Repaired subject and new checks

Repaired `qa_master/_paired_contract.py` exact SHA-256: `f8871c22a023916f9821479099c686f3af01c0c90d7889763a857113d7cd97de`. Other runtime source hashes remain the table values above. The repair source manifest is `paired-runtime-repair-source-manifest.json`. Independent test source exact SHA-256: `b0b1a31511fbf0e5e95253163252252143bf06322a56b2464abe972537cedd4a`.

New TC-PE-222–225 verify all six native types on both observation and assertion sides, reject coercions/boolean-as-integer/negative-zero/exponent/decimal variants, enforce set 256/257 and ordering/uniqueness, and enforce JSON depth 16/17 plus nodes 4096/4097 including object keys. They also reject nested claim/secret keys, duplicate keys, floats, and unpaired surrogates. These were authored after the architecture decision and executed only after new-source Runtime rebinding.

- Repaired focused: **24 tests, OK with 1 skip**, 32.992 seconds.
- Repaired fresh wheel: built and installed anew; **four installed non-executing CLI checks PASS** with site-packages assertion and child-process sentinel.
- Repaired full strict: **590 tests in 94.545 seconds, FAIL (1 failure, 3 skips)**. The only failure is existing `TC-SM-005` concurrent initialization: a worker raised `PermissionError` at `qa_master/state_store.py:30` (`lock.flush()`), so the expected conflict result was absent. Paired-runtime cases passed. A single isolated diagnostic rerun of that race test passed (1.017 seconds); this does not erase the failed full run or prove the race fixed. Logs: `repaired-full.txt` and `unrelated-race-recheck.txt`. No product fix was made by this tester.

## Historical executed checks and bounded coverage

- Current PR2 focused behavior run: 20 tests, OK with 1 skip, 28.818 seconds. The skip is real filesystem symlink creation denied by Windows privileges; no symlink behavior result is invented.
- Fresh wheel built from PR2, installed into a new virtual environment. Four installed public CLI scenarios passed: validate, materialize, inspect, and redacted rejection. Import path was asserted to be in `site-packages`; `subprocess.Popen` was patched to fail on any child process for these commands. No actual model was called.
- Strict full suite: 583 tests in 104.807 seconds, FAIL with 1 failure (TC-PE-221) and 3 skips. This run started before the request to hold further full-suite work and remains the real failing baseline, not an acceptance result.

| Test IDs | Independent checks |
|---|---|
| TC-PE-201–203 | Strict malformed JSON/type/member rejection, timeout 1/1800 boundaries, retry rejection, source/executable drift, unsafe paths, 64/65 assets and 2 MiB size/total boundaries |
| TC-PE-204–206 | Materialization inventory, equal common bytes, participant-specific marker actually embedded in prompt, no recursive placeholder replacement, evaluator marker/path rejection before root creation, six exact AB/BA calls and TEST_DOUBLE/NOT_EXECUTED labels |
| TC-PE-207–208 | Nonzero, missing final, malformed trace, confirmed/unconfirmed timeout, spawn/integrity failure; exact terminal precedence, stopped schedule, typed independent process/termination fields; policy violation, redaction original hash, partial stdin |
| TC-PE-209–212 | Exact typed grader distinctions, absent observations UNSCORABLE, unknown binding atomic rejection, missing/undeclared/drift inspection, strict/unverified attestation boundaries, fixed prompt contract and CLI no-process sentinels |
| TC-PE-213–215 | Actual local Python subprocess capture through injected Popen boundary: success, nonzero, overflow and timeout; argv/shell/cwd/env and cleanup; malformed envelopes, explicit participant failure, warning-compatible trace and trace/final mismatch |
| TC-PE-216–220 | Symlink fixture (skipped if privilege denied), implementation capacity 32/33, late write fault preserving prior finalized arm, keyword-only response UNSCORABLE, existing run unchanged |
| TC-PE-221 | Historical frozen-design string-transport conformance: FAIL, retained unchanged |
| TC-PE-222–225 | Registered native-value correction and exact boundary checks; new independent conformance tests |

## Retained corrections and limitations

Historical first run errors were in the tester fixture: it expected PROHIBITED_FIELD for an unknown winner member (actual strict-schema INVALID_MEMBERS), and intercepted Windows taskkill while substituting Python for the intended child. The latter caused cleanup assertions and a ResourceWarning; the corrected interceptor delegates the captured-PID termination command to the real OS call. Historical logs remain unchanged.

The historical 256-scenario test came from a stale preparatory architecture message. Frozen implementation documents a 32-scenario ceiling; current TC-PE-217 tests 32/33 and zero output directory on rejection. This extra capacity ceiling remains an explicit design/requirements coverage limitation, not evidence of full capacity compliance.

The assertion bundle is the executable oracle. `oracle_ref` is an opaque provenance locator and is not resolved as a file. Missing bundle fails atomically; a missing participant observation is UNSCORABLE. This follows the architect clarification and introduces no new file access.

No live Codex/provider behavior, enterprise integration, OS read/network isolation, human rating, strict comparison, superiority, release, Gate or complete-product acceptance has been verified. Actual pilot remains a later task. The test suite uses representative finite fixtures; it is not exhaustive coverage of all JSON, filesystems, concurrency interleavings or process-tree behaviors.

## Intermediate bounded conclusion (superseded by final combined result below)

The registered native-value correction is independently validated for the exercised paired-runtime matrix and installed non-executing commands. No observed paired-runtime defect remains in these cases. Full regression is not clean because of the independently observed concurrent-initialization failure outside CR-011. Track and resolve it before claiming a fully green repository or release. The Windows symlink coverage gap remains explicit. Runtime TASK-042 completion records performed testing, not a Gate decision, pilot authorization, or automatic acceptance.

## Final combined subject and verification

The final subject is commit `96926a282739865f90bcedf9eab2ec6c5ada6176`, including the separately repaired state lock. Final exact SHA-256 values:

| Subject | SHA-256 |
|---|---|
| qa_master/_paired_contract.py | 4d8ada7cd03e62ce1bebca5865e878ef895c9fcf33847bb41e1495d92f3bd235 |
| qa_master/state_store.py | 94660a7f7171442e19dc40c2e67e5892bb5d7c37b17ead00bab1b1446998c911 |
| Registered typed-value clarification | bd58f2d722a8f355d6302ffbcba486da9f08cd19d2d97b4d22502342c7507b92 |
| Independent test source | 521f57e9443b97ce01b17ab4424c589ecda8c4b85f1038d0924ead50f7be1cc6 |

Other paired runtime module exact hashes remain the initial PR2 table values. TC-PE-226 adds positive and negative 34-digit acceptance and 35-digit rejection for INTEGER observations, nested JSON values and assertion bundles, under Python global conversion settings 640 and disabled (0), restoring the original setting in `finally`. All output schema/prompt fixture hashes are regenerated from the final fixed constants.

- Final focused: **25 tests, OK with 1 skip**, 44.336 seconds.
- Final fresh wheel: rebuilt and installed in a separate new venv; four installed non-executing CLI checks **PASS**, site-packages import asserted, process sentinel enabled.
- Final full strict: **595 tests in 119.303 seconds, OK with 3 skips**. All three skips are unavailable Windows symlink-creation privileges (two existing installer tests and TC-PE-216); they are not counted as verified filesystem-link behavior. The previously failing concurrent initializer passed in this combined run after its separately owned repair.

All prior failure logs remain untouched, including old TC-PE-221 and the state-lock race. No old failure was converted into a pass. Final scope still excludes model pilot, enterprise execution, human ratings, strict comparison and Gate decisions.

Final conclusion: the bounded independent paired-runtime matrix, fresh installed non-executing CLI, and final complete strict suite passed with the disclosed skips. This is sufficient test evidence for independent code review of this frozen increment, not a real-model pilot result, release approval, product-wide superiority claim, or Gate PASS.
