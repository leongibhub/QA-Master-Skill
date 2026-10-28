# QA Master login writing — independent evaluation

**Scope:** read-only evaluation of two fresh synthetic artifacts against frozen
LOGIN-WRITE-01–06 in `docs/verification/qa-writing-login-check-2026-10-28.md`.
**Status:** `PASS` for bounded format capability on the two synthetic artifacts.
The explicit author’s first-turn capacity error is a transport event, not an
artifact-quality result. This evaluation is not proof of human
indistinguishability, host/model portability, business execution, or external
write capability.

## Default ordinary-request artifact

**Artifact:** `login-default-output.md`
**SHA-256:** `9eb74002b1fa883c9f7ce0eda47e7989fd182b561a0b57016e30a65f6d9819cf`
**Result:** `PASS` for LOGIN-WRITE-01–06 on this synthetic fixture.

| Check | Result | Observable basis |
| --- | --- | --- |
| LOGIN-WRITE-01 | PASS | Chinese title, DemoLogin `demo-login-1`, logged-out login-page state, controls, and supplied invalid values are self-contained. |
| LOGIN-WRITE-02 | PASS | Username entry, password entry, and Login click are separate numbered actions; each has adjacent explicit expectation. |
| LOGIN-WRITE-03 | PASS | Exact values and supplied masked-password/login-failure behavior are retained; no error text, timing, route, policy, or cause is invented. |
| LOGIN-WRITE-04 | PASS | Bug has numbered reproduction, separate expected/actual, and calls the report fictional/tester-supplied rather than Agent-reproduced. |
| LOGIN-WRITE-05 | PASS | One case and one bug are directly scannable; no strategy, coverage matrix, handoff JSON, or metadata dump appears. |
| LOGIN-WRITE-06 | PASS | Error text and login-state observation details are visibly pending, and the draft is `NOT_EXECUTED`/`NOT_RUN`. |

## Capability versus strict default enforcement

The default artifact demonstrates that QA Master can produce the requested
normal-human-readable case/bug format on this fixture. It does **not** prove the
format is strictly enforced for every ordinary request: pre-edit/final reference
text at `readable-artifacts.md` line 39 permits a known intermediate action to be
labelled “准备” with its test result deferred to a later assertion action. That
rule can produce a preparation action without an independent expected result,
which is weaker than LOGIN-WRITE-02’s strict user preference. No unknown fixture
fact was fabricated to fill that gap.

The explicit-format retry will test compliance after the user states the strict
one-operation/one-expected preference. Its outcome is recorded below.

## Explicit user-format-preference artifact

**Artifact:** `login-explicit-output.md`
**SHA-256:** `739960b4af99fe08df6003e47375f0da0d0ce5193e83525ab737bb84b44204f3`
**Result:** `PASS` for LOGIN-WRITE-01–06.

| Check | Result | Observable basis |
| --- | --- | --- |
| LOGIN-WRITE-01 | PASS | Concrete Chinese title plus DemoLogin `demo-login-1`, logged-out state, controls, and supplied invalid values. |
| LOGIN-WRITE-02 | PASS | Three-row step table gives exactly one operation and one explicit expected result per numbered action. |
| LOGIN-WRITE-03 | PASS | Exact values, masking behavior, failure/remaining-logged-out expectation, and homepage report are retained; error text, browser/OS, policy and cause stay unspecified. |
| LOGIN-WRITE-04 | PASS | Bug draft has three reproduction steps and separate actual/expected sections; actual is attributed to the fictional tester and Agent non-reproduction. |
| LOGIN-WRITE-05 | PASS | One case and one bug are scannable; no unrelated strategy, matrix, handoff, or lifecycle payload appears. |
| LOGIN-WRITE-06 | PASS | Error message, logged-out observation method, cleanup, evidence, frequency, severity/priority and root cause stay visibly pending; draft remains `NOT_EXECUTED`. |

## Final bounded verdict

QA Master **can reach** the user’s normal human QA format for this login fixture:
both independently authored artifacts contain readable case setup/data, separate
reproduction/actual/expected bug sections, and preserve unknowns without
fabrication. The explicit-format artifact demonstrates compliance after the user
states one-operation/one-expected preference.

Strict default enforcement remains **unproven**. The ordinary-request artifact
happened to meet LOGIN-WRITE-02, but the installed/source writing reference still
allows a preparation action with no independent expected result. Two synthetic
samples cannot establish universal model behavior, human equivalence, or strict
format enforcement for every default request. No source change, installation,
business execution, issue/case import, or external write occurred in this audit.
