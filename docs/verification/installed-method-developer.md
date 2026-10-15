# Installed method design route — developer verification

- Evidence ID: `EVD-INSTALLED-METHOD-HELPER-001`
- Change / task: `CR-013` / `TASK-056` (`work-f654afd9202644f49ee14c94fa214a42`, v1, attempt 1)
- Requirements: `REQ-025` Phase 1; `NFR-009`; preserves `REQ-013`–`REQ-018`
- Source design: `DES-055` v1 (`DRAFT`)
- Evidence status: `OBSERVED`
- Date: 2026-10-15

## Implemented scope

The self-contained installed Skill now exposes the additive, stateless command
`python -I <skill-root>/scripts/qa.py design --input FILE --output FILE`.
It dispatches before Campaign service loading and calls the existing strict
campaign loader, preparation path and deterministic method engine. The new
installed-only report member records the selected packaged guides, declared
source mapping, method candidate/obligation IDs and typed gaps. Direct
`python -m qa_master.campaign_cli` retains its prior report and summary shape.

The bundle now contains an instructional reference and non-secret example.
They state that candidate output is draft planning input, never an approval,
executed result, usable-case proof, executable-case proof, rating, or
comparison conclusion.

## Developer checks actually run

```text
D:\codex-rd-platform\.venv\Scripts\python.exe -X utf8 -m unittest \
  tests.test_installed_design_route tests.test_campaign_cli tests.test_codex_skill -q
```

Observed: 20 tests passed in 5.559 seconds.

One final full local regression was then run after the projection-index change:

```text
D:\codex-rd-platform\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -q
```

Observed: 598 tests passed in 100.765 seconds, with 3 pre-existing
platform-specific skips.

The route-specific tests install a fresh Skill under a temporary unrelated
directory and invoke its `scripts/qa.py` with `-I`. They cover the installed
example; all three existing finite methods through a separate strict fixture;
stable relative guide locators and installed-byte digests; no state path
creation; absent/empty model and missing source gaps; invalid duplicate JSON;
duplicate or abbreviated options; output sentinel preservation; and direct
campaign compatibility. `py_compile` and `git diff --check` also passed.

## Source hashes before commit

| Path | SHA-256 |
| --- | --- |
| `qa_master/__main__.py` | `283DF2A52409C537090F26BCC9EFD4418660F91368CDDAD8E3103470654D203D` |
| `qa_master/campaign_cli.py` | `630EAB0DB06D7C7A57A661F377E7089137353FD137872005F6B27379F3D93564` |
| `qa_master/skills/codex/references/design-methods.md` | `0AC902F51EC4060A896ADE1284E1055633171D4AC385C5D5A3912F8AA8B5CE6F` |
| `qa_master/skills/codex/examples/design-methods.json` | `D2F52BDE97B461C8EC49F264F05C0EBC8EE6BEA303F4990FE5B25DA2F1187F06` |
| `tests/test_installed_design_route.py` | `9656E0F11DDFFB6CA9C7D09E501BB517B29B8054A98288D790B6FEAB62DD4C72` |

## Evidence boundary

This is developer-owned local verification only. It does not establish the
separate independent test or review tasks, a representative task-level Codex
artifact, human assessment, any Gate result, product quality, or superiority
over Awesome QA Skills. Those items remain pending or not executed.

## v2 packaged-reference repair

Formal review found that the initial installed reference did not give an
installed-only user enough exact information to construct a decision-table or
state-transition model. The v2 repair expands only the packaged reference and
example, its installed-route regression, and the small README entry. It now
records all 13 dimension literals; source/oracle kind enums; exact top-level,
boundary, decision, and state field grammar; permitted empty arrays; finite
limits; stable wrapper gaps/errors; and the `installed_design` guide/source
mapping fields and declared-binding meaning. The packaged example now actually
constructs all three methods with `approved: false`.

The final v2 related suite was run after this repair: 20 tests passed in 5.565
seconds. It covers successful parsing and execution of all three packaged
example models, installed-reference contract terms, direct campaign
compatibility, and Skill installation behavior. It is developer verification,
not independent testing or a task-level Codex acceptance artifact.

After the reviewer-corrected no-dimension wording, the installed-route subset
was rerun: 3 tests passed in 2.016 seconds. This textual correction does not
alter the engine, installed wrapper, or example data.

v2 working-file hashes before commit:

| Path | SHA-256 |
| --- | --- |
| `README.md` | `E2E080D3D5EA4A54768D8381F31B2C759F14400AF80867ABEE429257745E7C3F` |
| `qa_master/skills/codex/references/design-methods.md` | `D128BDCFCC17AAD064693E73E56AF8EF907596FA563CFA815C9E5AF2DAF682B4` |
| `qa_master/skills/codex/examples/design-methods.json` | `805B3A6EB2C2AD37FFE4DFFFBA3BDAD6B3BDF47A94F8FD9246894211284085C3` |
| `tests/test_installed_design_route.py` | `88F048205A607E456CBDB67C0BA2EF1FFB1E9EC9D59B73CDDD00F7E85CA8BD38` |

## v3 legacy-requirement semantic repair

An independent installed-task attempt retained as BUG-014 found 13 finite
method candidates but zero generic cases and six each of `EMPTY_REQUIREMENT`,
`NO_PROVENANCE`, and `NO_ACCEPTANCE`. The method models were valid; the task
bundle omitted the separate legacy requirement fields consumed by the generic
campaign projection. This v3 repair does not alter the engine, schema, or that
historical attempt. It makes the installed reference and example state the
four required generic fields (`id`, `text`, `source`, `acceptance`), common
optional behavior, generic/method separation, and the zero-case
`case_review.pass` boundary.

The packaged example now supplies a concrete source-grounded generic oracle
consistent with its boundary, decision, and state models. The installed-route
test asserts one meaningful generic draft case, its exact expected outcome,
all three method results, and the absence of the three false legacy findings.

```text
D:\codex-rd-platform\.venv\Scripts\python.exe -X utf8 -m unittest \
  tests.test_installed_design_route tests.test_campaign_cli tests.test_codex_skill -q
```

Observed: 20 tests passed in 5.751 seconds. `git diff --check` passed.
This remains developer verification only; independent task testing and formal
review of the v3 source are pending.

| Path | SHA-256 |
| --- | --- |
| `qa_master/skills/codex/references/design-methods.md` | `128DF839DA4B48DF2B40DE1B943EE0E1C1B76573FDAAAEF2717E5E8087F4265F` |
| `qa_master/skills/codex/examples/design-methods.json` | `3C90119659C20A35B7A9178A0224D4D3FC5AB4456E331B8A9C25E1A60FB38E64` |
| `tests/test_installed_design_route.py` | `F97D6A55B9810F200367F09109A0BAC6E7EB45925D8C13E087F70BE44EEC491D` |
