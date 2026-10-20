# TASK-113 packaging correction — developer addendum

Date: 2026-10-19. Change: CR-028. Scope: the independent fresh-wheel failure after source freeze `0ff9ad47ab0d442dff2157f6bf7d10e322a83f75`.

## Failure and correction

The installer inventory includes five tracked `.gitignore` files. Setuptools' `skills/vendor/**/*` package-data pattern omitted these dotfiles from a clean wheel. The inventory-based installer correctly rejected that incomplete distribution with `SKILL_VENDOR_RESOURCE_INVALID`; the earlier source-install success did not prove wheel completeness.

`pyproject.toml` now explicitly includes `skills/vendor/**/.gitignore`. The test extra declares `setuptools>=61` and `wheel` so regression builds use the locally installed backend without network access. No vendor content or inventory entries were removed to make the wheel pass.

New `tests/test_vendor_wheel.py` copies only the package and pyproject into a clean temporary build directory, excluding Python caches and avoiding checkout build/egg-info reuse. It builds an actual wheel, verifies inventory JSON bytes, all 5,819 inventoried resource paths and bytes, and rejects missing or extra vendor members. The test captures build logs and emits only a bounded tail on failure. Build timeout is 600 seconds for the large Windows asset set.

## Actual developer runs and limits

Work was prepared and run in `.qa-master/task113-wheel-repair` while the authoritative source remained frozen for independent testing.

| Attempt | Observed result |
|---|---|
| Initial clean-wheel regression, 180-second build timeout | ERROR: subprocess timeout; one test, 205.157 seconds. No asset assertion result was obtained. |
| Same private-copy correction with 600-second build timeout | OK: one test, 275.788 seconds, exit 0. All 5,819 inventory entries existed and matched source bytes, including the five dotfiles; inventory JSON bytes also matched. |

Build interpreter: `C:/Program Files/Python/python.exe`, setuptools 80.9.0. No additional parallel builds were started after the successful run.

The explicit *extra-member set equality* assertion was added after this successful private-copy run at review request. That added assertion has **NOT_EXECUTED** developer status here; the final independent/CI run must verify it. The prior successful run proves required-file completeness and byte identity, not absence of extra members. The successful artifact was temporary and was removed by the test's normal scoped cleanup; no retained-wheel claim is made.

After the independent run became terminal, the root released the source freeze and authorized copying the correction and test into the shared checkout. The owned `test_vendor_install.py` was also normalized to one final newline (and no UTF-8 BOM); test behavior was unchanged. Scoped `git diff --check` returned exit 0. No source or test edits occurred while the source freeze was active.

## Delivery hashes

| File | SHA-256 |
|---|---|
| `pyproject.toml` | `55891CBD5E823C84E9BD0352BE4125C900A31C010F05EB5F14D691B5B78E4DBA` |
| `tests/test_vendor_wheel.py` | `F8812BF368AFB5E6D042179813653E18F8AAE11C85BF698FE722AB9FBE13A53A` |
| `tests/test_vendor_install.py` | `FA07BF825A171A0450007916D02DC00A5AC45107880514671632034F58640743` |

This addendum preserves the earlier developer report unchanged. Final fresh-wheel acceptance, final strict regression and independent review remain outside this developer result.
