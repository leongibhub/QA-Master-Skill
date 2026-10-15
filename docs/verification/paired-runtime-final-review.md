# TASK-043 independent paired-runtime review

- Artifact ID: `DOC-PAIRED-RUNTIME-FINAL-REVIEW-001`
- Evidence ID: `EVD-PAIRED-EVALUATION-REVIEW-001`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Reviewer: `/root/workflow_review`
- Review work: `work-b8a3b3e9bf774575abd11ed537fbf5fb` v7 / attempt 1
- Change / task: `CR-011` / `TASK-043`
- Date: 2026-10-15
- Bounded verdict: **PASS WITH P3 FOLLOW-UP**
- Severity count: **P0 0 / P1 0 / P2 0 / P3 2**

## Findings

No unresolved P0, P1, or P2 finding remains in the reviewed paired-runtime
increment.

### P3-001 — Windows link defenses were not executed on this host

- **Requirement / design:** `REQ-020`, `NFR-006`, `NFR-007`, and DES-040 require path
  containment and rejection of symlinks, junctions, and reparse points.
- **Evidence:** `TC-PE-216` and two existing installer link tests were skipped
  because the Windows account could not create the required links. The final
  focused run was 25 tests with one skip; the final strict run was 595 tests
  with three skips.
- **Failure mode and impact:** a Windows privilege- or filesystem-specific link
  handling regression could remain undetected by this execution. The reviewed
  implementation performs component-wise `lstat` / reparse checks, but that is
  source evidence rather than an executed result for these cases.
- **Reproduction:** run `TC-PE-216` and the two skipped installer link tests on
  a Windows worker permitted to create symbolic links/junction fixtures.
- **Follow-up:** archive a passing privileged-Windows execution before claiming
  that Windows link behavior is verified across supported environments.

### P3-002 — the 32-scenario capacity ceiling is implementation-specific

- **Requirement / design:** the frozen CR-011 requirement/design baseline does
  not define the implementation's 32-scenario ceiling.
- **Evidence:** independent `TC-PE-217` verifies that 32 scenarios materialize
  and 33 are rejected before output-root creation. The prepared exploratory
  pilot contains three scenarios, so the ceiling does not block that run.
- **Failure mode and impact:** callers may infer broader capacity from the
  requirement text and receive a deterministic rejection above 32 scenarios.
  This affects future general use, not the bounded three-scenario pilot.
- **Reproduction:** submit otherwise valid manifests with 32 and 33 scenarios
  and compare materialization behavior.
- **Follow-up:** baseline the ceiling in requirements/design or raise it with
  independent resource-boundary tests before presenting the runtime as a
  general-capacity interface.

## Subject and inputs

The reviewed combined source subject is commit
`96926a282739865f90bcedf9eab2ec6c5ada6176`. Its paired-runtime source hashes
are:

| File | SHA-256 |
|---|---|
| `qa_master/_paired_contract.py` | `4D8ADA7CD03E62CE1BEBCA5865E878EF895C9FCF33847BB41E1495D92F3BD235` |
| `qa_master/_paired_process.py` | `3155104B5625F99A9FB60A125F9078315D1092A65317D92A9B1BC5AFEAE8E700` |
| `qa_master/paired_evaluation.py` | `0401C3AA4814CC46C250C546EA414643D5076D6608B049BBB3D2F4B601BCA8EF` |

Normative and evidence inputs were:

| Input | Identity / SHA-256 |
|---|---|
| Paired-runtime requirements | `DOC-PAIRED-EVALUATION-RUNTIME-REQ-001`; `E4E896DFD7FFFCEF13A965BD9AFEFB5A196B83049EBC14820AF075BAE225D8C2` |
| Runtime design | `DES-040`; `BF260FEB85CE1662AF4B055CA114B8BA40A3E6752B959463DD2B947486F42330` |
| Architecture decision | `ADR-005`; `AD141E168B4A3578CDE7E29C4CE6B4BE7218E2D84F0C54590E0879DD15B5A0F5` |
| Typed-value correction | `DOC-PAIRED-VALUE-ENCODING-CLARIFICATION-001`; `BD58F2D722A8F355D6302FFBCBA486DA9F08CD19D2D97B4D22502342C7507B92` |
| Independent test evidence | `EVD-PAIRED-EVALUATION-INDEPENDENT-002` v1 |
| Independent test report | `8F4C2D7031344EBE5F2420F00528AC319C3AE93F20E479F394017E1E85F35A39` |
| Independent test source | `521F57E9443B97CE01B17AB4424C589ECDA8C4B85F1038D0924EAD50F7BE1CC6` |
| Independent evidence index | `E6D29CFCFD8447728F8F8F92E42D1D19FED939FD198C706C1979E4F5A147F827` |

## Compliance and correctness assessment

The public `validate` and `materialize` paths remain process-free. Only the
explicit public `run` path selects the native launcher. The private injected
launcher path stamps `TEST_DOUBLE`, `TEST_DOUBLE`, and `NOT_EXECUTED`, so test
captures cannot be presented as native pilot evidence.

The implementation preserves the four independent outcome domains
(`process_outcome`, `termination_outcome`, `output_outcome`, and
`policy_outcome`) and derives terminal state with deterministic precedence.
Timeout, overflow, partial stdin, termination uncertainty, redaction, cleanup
failure, malformed trace/final data, and stop-chain behavior fail closed. Raw
and transformed artifacts are bound to the ledger; `inspect` recomputes hashes,
validates per-attempt and global ledger consistency, and rejects undeclared or
contradictory records before `grade` consumes them.

Grading uses exact typed assertions and evidence-reference inclusion. It does
not calculate a winner, aggregate score, quality rating, approval, or
superiority claim. Unknown scenario/check bindings fail atomically; absent or
ambiguous observations become `UNSCORABLE` rather than a fabricated result.

The prospective native-value correction is internally consistent across raw
JSON decoding, typed-value validation, discriminated response schema, prompt,
and assertion grading. Integer tokens are limited to 34 magnitude digits before
conversion, including integers nested in JSON values, and parsing neither
depends on nor mutates Python's process-global integer-string setting. Decimal,
boolean, string-set, structured JSON, duplicate-key, recursion/node, prohibited
field, and coercion boundaries are enforced by the local authoritative parser.

The public error boundary returns stable codes without echoing prompts,
credentials, local paths, stderr, or raw sensitive content. Environment values
are allowlisted for the child process, command recording replaces the executable
and staging path with fixed labels, sensitive retained outputs are redacted as
whole artifacts, and redaction or cleanup failure prevents a complete result.
The design explicitly limits these controls to a local exploratory runner; it
does not claim OS read/network isolation or adversarial tamper resistance.

Existing benchmark validation remains a separate schema and command surface;
the reviewed increment does not silently upgrade old benchmark submissions.

## Independent validation considered

The final TASK-042 attempt tested the same combined subject and registered
typed-value clarification:

- 25 focused paired-runtime tests passed in 44.336 seconds, with the one Windows
  link fixture recorded as `NOT_EXECUTED` through the skip;
- 595 strict full-suite tests passed in 119.303 seconds, with three Windows link
  fixtures skipped;
- a fresh wheel was installed into a new virtual environment, and four installed
  non-executing CLI checks passed with a `subprocess.Popen` sentinel;
- no model call was made.

The suite covers strict manifests and paths, source drift, count/size limits,
equal common inputs and arm separation, exact AB/BA scheduling, real local child
pipe/timeout/overflow behavior, result retention after later write failure,
artifact mutation, terminal-state contradictions, exact grading, all six native
types, nested JSON limits, secret/claim keys, 34/35-digit integer boundaries,
and installed CLI behavior. This coverage is sufficient for the bounded review;
it is not exhaustive filesystem, process-tree, concurrency, or provider testing.

## Preserved failure history

Historical `TC-PE-221` correctly failed against DES-040 v1's string-encoded
value contract. It remains failed evidence. The typed-value clarification
prospectively changed the contract before any pilot, and `TC-PE-222` through
`TC-PE-226` validate the repaired native-value implementation.

The earlier full-suite state-initialization race failure also remains in its
original evidence. The final combined run passed after the separately owned
state-lock repair; this review does not close or reclassify that defect.

## Bounded verdict and nonclaims

The reviewed increment is suitable to proceed to the separately controlled,
actual exploratory pilot task. The verdict is limited to source/design
conformance and the registered non-pilot validation evidence.

This review did not execute Codex or any model, verify a provider revision or
system baseline, verify OS read/network isolation, use a private holdout, obtain
human ratings, establish strict comparability or fairness, calculate a winner,
or demonstrate superiority. It is not a G8 or other Gate decision, product
acceptance, release approval, enterprise execution result, or full V1
completion. Any later pilot must preserve its own exact subject, manifest,
assertion bundle, raw artifacts, timeouts/errors, and `EXPLORATORY` claim
boundary.
