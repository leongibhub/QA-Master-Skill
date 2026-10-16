# TASK078 independent test of the strict-profile attestation verifier

- Artifact ID: `DOC-ATTESTATION-VERIFIER-TEST-001`
- Proposed evidence ID: `EVD-ATTESTATION-VERIFIER-TEST-001`
- Runtime: `work-e4d8d04f1b7a42fdaf805df6bdae346e`, attempt 1 / version 1
- Subject: `CODE-ATTESTATION-VERIFIER-001` v1 at commit `7721dc2` (implementation) with the retained repository state at `2ad4888`
- Design under test: `DES-061` v1
- Tester: independent (`/root/design_acceptance`); the tester did not author the implementation or the developer tests
- Date: 2026-10-16
- Classification: bounded local test observation only. No model call, pair
  run, holdout release, rating, comparison, Gate, acceptance or release
  decision is made or implied.

## Method

1. Fresh-repository focused run of the new independent suite
   `tests/test_attestation_verifier_independent.py` (17 cases) plus the
   developer suite `tests/test_attestation_verifier.py` (17 cases).
2. Full-suite regression: `python -m unittest discover -s tests -q`.
3. Fresh-wheel end-to-end: `pip wheel` + clean venv install + CLI
   `validate` in exploratory, strict-pass, and strict-tamper configurations
   (executed inside `test_fresh_wheel_cli_strict_and_exploratory`).

## Results

| Suite | Result |
|---|---|
| Independent suite (17 cases) | 17 PASS |
| Developer suite (17 TC-SV cases) | 17 PASS |
| Full repository suite | OK (732 tests, 8 pre-existing Windows-link skips) |
| Fresh-wheel CLI end-to-end | PASS (exploratory no-flag, strict pass, strict tamper-fail) |

Fail-closed ordering, registry drift detection (including mid-run stop),
arm/subject signature substitution, time-inversion, unknown issuer,
schedule-order derivation, exploratory-path equivalence (with/without None
flags, no strict markers on exploratory results), and CLI flag wiring were
all confirmed within the tested scope.

## Findings (typed, bounded)

| ID | Severity | Observation |
|---|---|---|
| F-01 | P3 | DES-061 §6 promises dedicated codes (`TRUST_REGISTRY_INVALID`) for registry grammar failures, but grammar failures inside `exact`/`array`/`text` surface the contract-layer codes (`INVALID_MEMBERS`, `INVALID_ARRAY`, `INVALID_TEXT`). The §6 code is returned only for value-level failures (algorithm, subject, short key, bad timestamp, duplicate issuer). Fail-closed behavior itself is correct; only the code mapping is narrower than designed. |
| F-02 | P3 | Same class as F-01 for attestation documents: schema-version and empty-statement failures surface `INVALID_INTEGER`/`INVALID_TEXT` instead of `ATTESTATION_INVALID`. Subject/arm mismatch and time inversion do return the designed codes. |
| F-03 | P3 | A document stored with trailing whitespace (`canonical + b' '`) is accepted: `strict_json` tolerates trailing whitespace and the signature is verified over the canonical form, so the on-disk bytes are not exactly the signed bytes. The signature still binds the semantic content (tampering is caught), but DES-061 §3 "detached signature over the canonical document bytes" is not enforced against on-disk byte equality. |

All three findings are P3 (interface/documentation-precision) — no fail-open,
no security bypass, no silent upgrade path was identified. The independent
suite encodes the observed behavior with explicit FINDING annotations so a
future repair task can flip the expectations to the designed codes.

## Boundaries

1. These are local synthetic-key observations; no provider attestation
   existed or was validated.
2. `TEST_DOUBLE` runs cannot produce `STRICT_COMPARABILITY_CANDIDATE`; only
   the derivation logic was exercised, never a native strict run.
3. F-01..F-03 do not block independent review; they are recorded for a
   bounded follow-up decision under CR-015 governance.
4. Nothing here completes REQ-011, authorizes a holdout release, or changes
   any Gate status.
