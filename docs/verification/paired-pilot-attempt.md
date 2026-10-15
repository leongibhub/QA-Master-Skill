# Exploratory paired-pilot attempt

- Evidence ID: `EVD-PAIRED-PILOT-ATTEMPT-001`
- Runtime task: `TASK-044`, attempt 1
- Change context: `CR-011`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Pilot status: `COMPLETE`

## FACT and EVIDENCE

The local native Codex runner completed the single authorized schedule: six calls,
one AB or BA pair for each public-development scenario. The run root is ignored
local evidence at:

`D:\QA-Master-PR2\.qa-master\paired-pilot\observed-v4-final-freeze\CR011-EXPLORATORY-PUBLIC-DEV-001`

The frozen source identity remains `96926a282739865f90bcedf9eab2ec6c5ada6176`.
The manifest, result, preflight, and bound-assertion grade SHA-256 values are,
respectively, `1c05657cf897f8e599cea1893accb642e4e245e9c298e81b238c729f076f4a44`,
`b2cb38fa826184be698ebb2dd4c04fb6587f91fe559150dca69671db4c004ffe`,
`a2443fa867762f7b6faa1c3bc656be94941fb537ef39dc634b1e57395a120b3b`, and
`8cfb753182db0ec0c325f3c0f0f8ac739a40e832a0e21165e23cf2ba3fda2c6b`.
The six redacted stdout/final captures remain in the ignored run root; their hashes
are preserved in [paired-pilot-trace-index-001.json](evidence/paired-pilot-trace-index-001.json).
Git-verifiable copies of the six final/envelope pairs, `result.json`, existing
`grade.json`, and the process-free `inspect.json` are at
[`evidence/paired-pilot-001/`](evidence/paired-pilot-001/). Its
[`index.json`](evidence/paired-pilot-001/index.json) binds the original relative
paths, byte counts, SHA-256 values, and unchanged-redaction checks. It excludes
stdin, participant context, prompt/template, stdout traces, and all upstream assets.

All six records report `EXITED_ZERO`, `COMPLETE`, `COMPLETED_PROCESS`,
`SENT_COMPLETE`, and `NO_VIOLATION_OBSERVED`. The final process-free inspection
reports `INTACT` and `RECORDED`. Every trace has two recorded configuration warnings;
the warnings were preserved as observations and did not change the process outcome.
The runner recorded provider revision as `NOT_AVAILABLE` and system baseline as
`UNVERIFIED`.

The bound assertion evaluator produced its twelve individual statuses in
[paired-pilot-attempt-001.json](evidence/paired-pilot-attempt-001.json). This is
exact equality against three public development-oracle bundles. It is not a human
rating, quality grade, aggregate score, fairness finding, winner, strict comparison,
or superiority claim.

### Exact assertion observations

| Call | Assertion observations |
| --- | --- |
| `PE-BND-001-P1-A` | `AS-BND-001` and `AS-BND-002` are `SATISFIED`: both native values and required fact references exactly match the public bundle. |
| `PE-BND-001-P1-B` | `AS-BND-002` is `SATISFIED`. `AS-BND-001` is `VIOLATED` because its JSON value includes two additional members, `expectation_scope` and `step`; the grader requires exact structural equality. |
| `PE-DTT-001-P1-A` | `AS-DTT-002` is `SATISFIED`. `AS-DTT-001` is `VIOLATED`: the response uses a richer decision-table representation, including detailed classifications and rule/source details, rather than the compact exact object in the public oracle. |
| `PE-DTT-001-P1-B` | `AS-DTT-002` is `SATISFIED`. `AS-DTT-001` is `VIOLATED`: its richer audit, conflict, and rule-detail members do not exactly equal the compact public-oracle JSON object. |
| `PE-STT-001-P1-A` | `AS-STT-002` is `SATISFIED`. `AS-STT-001` is `VIOLATED`: it names its collections and state fields differently (`valid_candidates`/`invalid_candidates`, `from_state`, and related detail) from the public oracle's exact JSON shape. |
| `PE-STT-001-P1-B` | `AS-STT-002` is `SATISFIED`. `AS-STT-001` is `VIOLATED`: its candidate-recommendation representation has a different, more detailed JSON structure than the exact public oracle. |

These reasons distinguish exact-oracle mismatch from process or parser failure; they
do not decide whether either representation is preferable for another use case.

## INFERENCE

The run is valid as `EXPLORATORY_CONFIGURED_SAME_MODEL` evidence for these exact
bytes and this configuration. Its local integrity supports reading each recorded
assertion status; it does not generalize beyond the three public fixtures.

## RISK

- Read-only sandbox and disabled-feature settings remain
  `WRITE_RESTRICTED_READ_SCOPE_UNVERIFIED`; no filesystem-read or network-isolation
  proof exists.
- Provider revision and system baseline are unavailable, so this cannot be treated
  as strict same-model evidence.
- The fixtures and assertions are public development material rather than holdout
  evaluation data.

## RECOMMENDATION

Preserve the raw ignored run root and this hash index unchanged. Any decision about
future product changes needs separate requirements/design review and independent
validation; this attempt does not make a Gate, acceptance, release, or product
comparison decision.
