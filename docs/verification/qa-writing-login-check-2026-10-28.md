# QA Master login writing check

Document State: DRAFT. Scope: read-only evaluation against the user's clarified
writing standard, not a Skill modification or a business test.
Baseline main: `aaf8b1c215a9cc84834668b42f72d3a9304a4fde`.
Installed entry: `~/.agents/skills/qa-master/SKILL.md`.

## Frozen checks before fresh author outputs

| ID | Check |
| --- | --- |
| LOGIN-WRITE-01 | A concrete Chinese case title, setup and supplied data are understandable without this chat. |
| LOGIN-WRITE-02 | Every numbered action has its own explicit expected result, including preparatory actions when the fixture supplies one. No final-only expected paragraph substitutes for per-step mapping. |
| LOGIN-WRITE-03 | Supplied login behavior/text/values stay exact. Unspecified messages, timing, UI routing, security policy and root causes are not invented. |
| LOGIN-WRITE-04 | The bug draft has clear reproduction steps, actual result and expected result as separate parts. Reported observations are not claimed as the Agent's own reproduction. |
| LOGIN-WRITE-05 | Requested case/bug content is easy to scan; no unrelated lifecycle strategy, coverage matrix, handoff JSON or metadata dump. |
| LOGIN-WRITE-06 | Missing expected behavior remains visibly pending rather than invented to complete the format. |

Two fresh authors receive the same synthetic login facts. One follows the Skill
with an ordinary case/bug request; the other also receives the user's explicit
one-step/one-expected formatting preference. Their request variants, common facts
and verbatim artifacts are retained. An independent tester evaluates both against this frozen rubric.
This distinguishes default behavior from compliance after a format reminder.

## Synthetic facts

DemoLogin, build `demo-login-1`. Browser is on the login page, user logged out.
There are username and password inputs and a Login button. Entering a username
displays that exact value; entering a password fills it using masking. The fixture
declares username `unknown_user_demo` and password `invalid_password_demo` are
invalid (neither is a real credential). Clicking Login with those values must
fail and leave the user logged out. No exact error message is specified.
Separately, a fictional tester reports that this combination instead logs in
and displays the homepage; no screenshot/log/frequency or root cause is supplied.
The Agent has not reproduced it. Produce one case and one bug draft only.

## Evidence and result

Source/installed critical-rule parity: five critical files match source,
installed bytes and the managed manifest (entry, readable reference, protocol,
functional guide and regression guide).

Default fresh author: PASS for all six checks on this synthetic fixture. It
wrote three separate numbered actions, each with an adjacent expected result.
SHA-256: `9eb74002b1fa883c9f7ce0eda47e7989fd182b561a0b57016e30a65f6d9819cf`.

Explicit-format fresh author: PASS for all six checks. It wrote the three actions
and expected results in a three-column table, with clear bug reproduction,
actual-result and expected-result sections.
SHA-256: `739960b4af99fe08df6003e47375f0da0d0ce5193e83525ab737bb84b44204f3`.
Its first turn failed due to model capacity before producing an artifact; retry
succeeded. That infrastructure error is not counted as a writing-quality result.

Independent evaluation: completed by `/root/rebind_tester`; see
`evidence/cr037/login-writing-evaluation-2026-10-28.md`.

## Bounded conclusion and remaining gaps

The current installed Skill demonstrably can produce this ordinary human QA
case/bug format on the supplied login fixture. It is not yet a strictly enforced
default-format contract: readable-artifacts.md line 39 permits preparation
actions without an independent expected result. The fixture supplies input-entry
expectations, so both authors paired them; unknown expectations must remain
pending, never invented merely to fill a row.

Additional reader-style observation beyond the frozen pass/fail rubric: the
explicit output includes `source_role`, `direct_input` and a generated trace
label even though the fixture provides no required machine schema. These can
make otherwise clear prose feel less natural. Essential traceability should be
preserved, but optional machine-only metadata need not lead a human-facing case.

Thus the evidence supports writing capability on this fixture, not a guarantee
of strict default behavior across all requests, Agent hosts or language models,
and not proof that humans cannot distinguish the prose from human writing.
No source or installed Skill was changed during this assessment.

No remote issue/case is created or edited. Actual host/model portability and
human indistinguishability are not established by two synthetic samples. Company
bug-report guidance was consulted read-only; no private text or URL is copied
into this public evidence record. Existing project Gates remain unchanged.

Independent read-only reviewer `/root/rebind_reviewer` confirms the bounded
conclusion and both gaps: the preparation-step exception prevents a strict
default-format claim; optional machine metadata is a P3 usability observation,
not a factuality error or a retroactive rubric failure.
