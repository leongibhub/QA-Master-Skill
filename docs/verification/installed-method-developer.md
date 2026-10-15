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

Observed: 598 tests passed in 93.019 seconds, with 3 pre-existing
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
| `qa_master/__main__.py` | `37352C6AE304732A66DC24298F4D95AC01CEA772EF2209759E75EEAA762BBE2B` |
| `qa_master/campaign_cli.py` | `630EAB0DB06D7C7A57A661F377E7089137353FD137872005F6B27379F3D93564` |
| `qa_master/skills/codex/references/design-methods.md` | `0AC902F51EC4060A896ADE1284E1055633171D4AC385C5D5A3912F8AA8B5CE6F` |
| `qa_master/skills/codex/examples/design-methods.json` | `D2F52BDE97B461C8EC49F264F05C0EBC8EE6BEA303F4990FE5B25DA2F1187F06` |
| `tests/test_installed_design_route.py` | `DC2EC95FA71F8C28E11FCCC0EAD922FED4793B120BEF1A8679724436A10206EF` |

## Evidence boundary

This is developer-owned local verification only. It does not establish the
separate independent test or review tasks, a representative task-level Codex
artifact, human assessment, any Gate result, product quality, or superiority
over Awesome QA Skills. Those items remain pending or not executed.
