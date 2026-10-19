# Independent catalogue visibility and provenance verification — 2026-10-19

- Artifact: `EVID-CATALOG-VISIBILITY-INDEPENDENT-2026-10-19`
- Change: `CR-029`
- Tester role: independent tester (`TASK-122`)
- Candidate attempts: `024505bd5e59df62be7b46bf4dbf0681e0911aad`,
  `5996ace97e7505097d482596b782162c595dd6ae`,
  `598a979fc1a7db6b57a5247a246482c81a9df7ed`, and final candidate
  `523ec344112f03ea350e1fa13c16d5ddc755277e`
- Environment: Windows PowerShell; Python from
  `D:\codex-rd-platform\.venv\Scripts\python.exe`; public GitHub Git-object API;
  Bash syntax checker.
- Scope: catalogue visibility, package provenance, fresh delivery, and the two
  vendored Playwright runner scripts. Browser tests were deliberately not run.

## Result register

| Test case | Candidate | Result | Observable evidence |
| --- | --- | --- | --- |
| TC-CAT-001 | 024505b | PASS | README structural test enumerated 330 bilingual leaves / 165 canonical names, with each entry once. |
| TC-CAT-002 | 024505b | PASS | README and stable-index test resolved every vendor Markdown target to an existing file. |
| TC-CAT-003 | 024505b | PASS | README test found the navigation target, catalogue headings, layer headings, and the required distribution counts. |
| TC-CAT-004 | 024505b | PASS | README and `docs/SKILL_CATALOG.md` enumerations matched the 330 physical bilingual records. |
| TC-CAT-005 | 024505b | PASS | One-entry and evidence-boundary assertions passed; sampled catalogue/README inspection found no execution, release, or superiority conclusion. |
| TC-CAT-006 | 024505b | NOT EXECUTED | A fresh wheel build was started from an isolated source archive, but did not complete before the candidate was superseded. No installation result is claimed. |
| TC-CAT-007 | 024505b | FAIL | Ubuntu CI run `39216549659` failed the provenance check: candidate digest `9748da...` differed from the Linux worktree digest `2c1a05...`. The candidate described raw file bytes, so the cross-worktree verifier contract failed. |
| TC-CAT-008 | 024505b | PASS (bounded) | GitHub API comparison at pinned upstream commit `547fbcd9c417ab8afbde1cd9f18b40ecbae0333b` found 5,816 upstream blobs, 5,816 committed vendor blobs, and 0 missing/extra/changed paths. The upstream license blob and committed vendor `LICENSE` matched. This is a pinned-snapshot comparison, not a current-upstream or superiority claim. |
| TC-CAT-007 | 5996ace | NON-PASS | The local normalization assertion passed, but independent review found the blanket `CRLF -> LF` transformation also reaches 12 binary `.docx` assets. `verification_status: VERIFIED` also conflicts with the retry record being pending. This attempt cannot be accepted. |
| TC-CAT-008 | 5996ace | NOT EXECUTED | A corrective retry is pending a frozen digest representation that preserves raw bytes for declared binary extensions and a coherent evidence state. |
| TC-CAT-007 | 598a979 | NON-PASS | Text/binary extension separation fixed the first issue, but independent review found the path-order contract was not sufficiently explicit across environments. The candidate was superseded before a final delivery conclusion. |
| TC-CAT-001 to TC-CAT-005 | 523ec34 | PASS | Focused independent suite completed 13 tests in 1.621 seconds: all 165 canonical entries / 330 bilingual files occur once, layer counts agree, links resolve, and the one-entry/evidence boundaries hold. |
| TC-CAT-006 | 523ec34 | PASS | A wheel built from a clean `git archive` was installed into a fresh virtual environment and then into a separate consumer directory. The declared 5,820 vendor inventory had 0 missing and 0 changed standalone files. The install manifest matched all 5,882 installed non-manifest files. |
| TC-CAT-007 | 523ec34 | PASS | Source archive and fresh wheel resources independently recomputed the 5,816-path canonical digest as `01c9414f426e36b8659aa08ac73d8db2042e2e1769aace4269881f7cb2c05799`, equal to metadata. The verifier uses UTF-8 bytewise POSIX path order, UTF-8-strict declared text with CRLF-to-LF normalization, and raw bytes only for declared `.docx` binaries. |
| TC-CAT-008 | 523ec34 | PASS (bounded) | Pinned upstream path/blob comparison again found 5,816 upstream and committed blobs, with 0 missing, extra, or changed; the license blob matched. It compares only the declared snapshot, not current upstream or product quality. |

## Executed checks

1. `python -m unittest tests.test_readme_catalog tests.test_vendor_skills -v` on
   final candidate `523ec34` completed 13 tests with `OK` in 1.621 seconds.
2. A clean Git archive of `523ec34` ran its provenance test in 36.524 seconds
   with `OK`, avoiding repository working-tree and uncommitted-governance files.
3. A wheel built from that archive was installed into a fresh virtual environment
   and then used, from a separate consumer directory, to run `install-codex`.
   The install command returned `INSTALLED`, `files: 5882`, and
   `execution: NOT_EXECUTED`. The declared inventory comparison and manifest
   comparison are recorded in the result table.
4. During the fresh pip installation, Python created unlisted vendor
   `__pycache__/*.pyc` files. They are not declared source assets and are omitted
   by the installer manifest. Digest recomputation correctly uses the declared
   inventory subset, rather than an unfiltered recursive directory walk.
5. The public GitHub tree at the pinned revision was enumerated. For the two
   delivered subtrees, committed Git blob SHA-1 values matched upstream exactly:
   `UPSTREAM_BLOBS=5816`, `COMMITTED_BLOBS=5816`, `MISSING=0`, `EXTRA=0`,
   `CHANGED=0`. The pinned tree is `694cf0b677cb90cee101e7806657537b016c356c`.
6. Both `ui-test-playwright/scripts/run-tests.sh` copies passed `bash -n`. Their
   committed blob is `8b2363db10e133b89920c6425256548a5b20c9aa`, equal to the
   pinned upstream blob in both languages. Static inspection also found the
   JSON-output environment variable and `list,html,json` reporter contract.

## Defect and limits

- `BUG-CR029-001` retains the failed `024505b` and non-passing `5996ace` /
  `598a979` attempts. Final candidate `523ec34` passes the independent source
  archive and fresh-wheel checks above; defect closure remains the reviewer's
  decision.
- At last observation, two Ubuntu CI jobs for `523ec34` had completed successfully
  and both Windows jobs remained in progress. Earlier failing CI applies only to
  `024505b`.
- The snapshot proves canonical declared-text content plus raw bytes only for the
  declared binary extension. Exact installed bytes are established separately by
  the `.qa-master-install.json` manifest and the fresh-install comparison; neither
  result asserts upstream currency, execution, release, or superiority. Browser
  tests were not executed; only static shell syntax and script identity were
  checked.

