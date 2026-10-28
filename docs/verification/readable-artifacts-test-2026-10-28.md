# CR-037 readable QA artifacts — independent evaluation record

**Owner:** TASK-155 independent tester
**Basis:** REQ-041, REQ-042, CR-037 baseline `8a22a9f45f514c4cebd7be67317ed5044bc4cc28`; pre-edit canonical Skill/work protocol.
**Overall status:** `PASS` (bounded independent verification) — source wiring,
fresh same-facts/English artifacts, and the repaired managed local install pass.
The initial cached-package failure is retained below. This is not model
benchmarking, human acceptance, business test execution, or authorization for
external writes.

## Frozen rubric

Assess each applicable criterion only against supplied scenario facts. A declared unknown is acceptable; inventing a detail fails REQ-042.

| ID | Requirement | Reader-facing check | Failure boundary |
| --- | --- | --- | --- |
| R-READ-01 | REQ-041 | Concrete self-contained scenario title. | Generic/title-only label. |
| R-READ-02 | REQ-041 | Supplied setup/data is visible in plain language. | Known setup omitted or obscured by metadata. |
| R-READ-03 | REQ-041 | Numbered, ordered, concrete actions. | Placeholder/requirement-shaped actions or invented UI route. |
| R-READ-04 | REQ-041 | Observable expected result and needed cleanup. | “Works correctly” or omitted needed cleanup. |
| R-READ-05 | REQ-042 | Exact supplied technical names/values/units/IDs retained; essential jargon explained once. | Fact altered, dropped, or imprecisely paraphrased. |
| R-READ-06 | REQ-041 | Defect has symptom title, environment/setup, minimal numbered repro, separate expected/actual. | Expected/actual merged or unsupported symptom. |
| R-READ-07 | REQ-041/042 | Supplied impact/evidence is locatable; frequency only if supplied. | Invented frequency, severity, cause or evidence. |
| R-READ-08 | REQ-042 | Missing threshold/UI/build/message/credential/evidence/execution fact is a plain question and affected draft is unexecuted. | Invented missing fact or fabricated result. |
| R-READ-09 | REQ-041 | Metadata remains readable; summary may precede detail. | Wide/jargon-heavy presentation obscures setup/actions/outcome. |
| R-READ-10 | REQ-042 | No external write/execution/approval/regression-skip claim. | Draft presented as an action or authorization. |

## Scenario plan

| TC | Synthetic scenario | Status |
| --- | --- | --- |
| TC-READ-001 | Web negative case and matching observed-defect fixture | PASS after same-facts fresh author; baseline R-READ-09 failure retained below |
| TC-READ-002 | API validation case | PASS after same-facts fresh author; baseline R-READ-09 failure retained below |
| TC-READ-003 | Incomplete performance requirement | PASS after same-facts fresh author; baseline R-READ-09 failure retained below |
| TC-READ-004 | First-party instruction wiring after update | PASS — source wiring observed at `a30e541` |
| TC-READ-005 | Managed local-install verification after update | PASS — repaired install integrity and isolated helper catalog observed below; initial failure retained |

Baseline and fresh authors receive the same facts. A baseline PASS only shows a readable sample despite the confirmed instruction gap; a fresh PASS is bounded to these fixtures. No real unreadable user output was supplied (`NOT_AVAILABLE`).

## Baseline evaluation

**Artifact:** `docs/verification/evidence/cr037/baseline-output.md`
**SHA-256:** `2fb8d82a6b4677436b795314d5009639155fed7b85c476541314d40f88b106ff`
**Result:** `FAIL` for reader-facing format, while factual-boundary checks pass.

| Criterion | Result | Observable basis |
| --- | --- | --- |
| R-READ-01 | PASS | All three drafts name a concrete Web/API/log-export scenario. |
| R-READ-02 | PASS | Alice/Bob, inputs, cart/draft state, and the known/unknown performance setup are stated. |
| R-READ-03 | PASS | Actions are numbered and technically concrete, though they are packed into one long table cell. |
| R-READ-04 | PASS | Web/API expected observables and conditional cleanup are supplied; performance remains a non-executable draft. |
| R-READ-05 | PASS | Values such as `0`, `1..5`, `422`, `TITLE_TOO_LONG`, `ABCDE`, and named IDs remain exact. |
| R-READ-06 | PASS | The defect includes symptom title, environment, numbered repro, and separate expected/actual fields. |
| R-READ-07 | PASS — declared gap | `demo-cart.png` is named and the draft plainly records that its byte, hash, and storage location were not supplied or read. It does not fabricate a locator or claim verified evidence. |
| R-READ-08 | PASS | Missing threshold, route, build, credential, cleanup, and evidence details are declared rather than invented; all drafts remain `NOT_RUN`. |
| R-READ-09 | FAIL | The three artifacts use repeated two-column metadata cards (18 rows for the Web case); steps are inline in one cell and the defect is another metadata card. This makes the reader’s setup/actions/outcomes hard to scan despite valid facts. |
| R-READ-10 | PASS | The artifact explicitly makes no execution, tracker write, approval, or regression-skip claim. |

The baseline failure is an instruction/presentation finding, not an assertion that
the supplied facts are wrong or that a real product test failed. It establishes
the pre-edit comparison point for the same-facts fresh author evaluation.

## Frozen-source wiring evaluation

**Source:** `a30e54113f80f08be92c3932d8878568705d4725`
**New reference SHA-256:** `309a277e1e27f1d1e9923484741e3ed060f01d9346f9aa4a230909f704652796`
**Result:** `PASS` for TC-READ-004.

Observed links are: mandatory canonical `SKILL.md` → `references/readable-artifacts.md`;
work protocol → the same reference before authoring cases, defects, review packets
or import packets; source-tree entry → source reference; and original
`functional-api.md`/`regression-evidence.md` → the entry-resolved reference.
README adds a reader-facing Chinese invocation. The frozen diff names only these
first-party instruction/docs files and does not alter vendored specialist assets,
generator algorithms, audit schemas, adapters, or execution permissions.

## Same-facts fresh-author evaluation

**Artifact:** `docs/verification/evidence/cr037/after-output.md`
**SHA-256:** `e7c6a7a96dacccde8775aa6731785c835bfc4b0a018b42222db4444eb5ad3449`
**Result:** `PASS` for R-READ-01–10 and TC-READ-001–003.

The fresh output opens with a compact case list and gives each case a heading,
known environment/data, distinct numbered actions and adjacent observable
expectations. It retains exact supplied values (`0`, `1..5`, `422`,
`TITLE_TOO_LONG`, `ABCDE`, `0 bytes`, `sv-2`) and source identifiers. The defect
has a symptom title, setup, four reproducible actions, distinct expected/actual
sections, bounded impact, and explicitly synthetic `2/2` observation context.
Its screenshot evidence is named but explicitly unverified/unlocated; no
frequency, severity policy, root cause, browser version, cleanup mechanism or
external outcome is invented. The API draft preserves missing authentication,
endpoint, scope and cleanup facts as questions. The performance draft does not
invent a threshold, workload, UI route, environment, observability signal or
pass/fail result, and stays `NOT_EXECUTED`. Technical fields are in short support
sections/matrices rather than replacing the narrative reader flow. No external
write, execution, approval, or regression-skip claim appears.

## Separate English transfer holdout

**Artifact:** `docs/verification/evidence/cr037/english-transfer-output.md`
**Result:** `PASS` for R-READ-01–10 on this additional, independently authored
SampleVault fixture. It has a concrete title/setup, numbered upload action and
observable `EMPTY_FILE`/unchanged-list expectation; its defect keeps expected and
reported actual separate, retains `sv-2`, `blank.txt`, and `0 bytes`, and labels
frequency, root cause, routing, evidence and cleanup/reset facts as unknown or
needed. Its headings and short detail sections are scannable; it claims no
execution or external write. This is an extra bounded English probe, not a
comparison metric or a substitute for the three same-facts artifacts.

## Final focused English probe

**Final instruction source:** `94fd0b90e6a52d5e8e3391e6d78b135de498e767`
**Artifact:** `docs/verification/evidence/cr037/final-focused-output.md`
**SHA-256:** `e9f99a2e654dac911d3c150945a128411d909b4f58944be42ddfdcda3dad6f04`
**Result:** `PASS` for R-READ-01–10 and the final narrow-scope guard.

The English case and defect have concrete titles, supplied SampleVault `sv-2`/
Jo/`blank.txt`/`0 bytes` setup, separated numbered actions and observable
`EMPTY_FILE`/unchanged-list results. The defect separates supplied actual from
expected, preserves `DOC-FILE-EMPTY`, scopes impact to the reported list change,
and declares evidence, frequency, severity/priority, root cause, browser/OS,
role, cleanup and contract-version facts unknown or pending rather than inventing
them. Both artifacts remain drafts with `NOT_EXECUTED`; no tracker or execution
claim appears. The output contains only the requested case/defect and relevant
gaps—no default complete strategy, 13-dimension coverage matrix, JSON handoff, or
routing analysis. This is one focused synthetic English probe, not a benchmark or
human acceptance.

## Initial local-delivery observation

Root's first forced local package attempt (`uv` session `11491`) exited `0`, but
an isolated Python `-I` resource check resolved an older cached package: the new
`readable-artifacts.md` resource and canonical entry rule were both absent. The
managed user-skill update was therefore not run and TC-READ-005 is a delivery
failure, not an installation PASS. This does not invalidate the frozen-source or
fresh synthetic-artifact observations above. Root requested a same-path
`--reinstall` repair and will provide its actual result for one later recheck.

## Repaired managed-install verification

**Final instruction source:** `94fd0b90e6a52d5e8e3391e6d78b135de498e767`
**Result:** `PASS` for TC-READ-005.

Root reported repaired `--reinstall` session `22757` exit `0` with the new
resource and canonical rule visible before managed update. The managed installer
then reported session `34031` exit `0`, `UPDATED`, target
`C:\Users\leon.wang\.agents\skills\qa-master`, 5,891 files, and
`execution: NOT_EXECUTED`. Independent full-map readback found schema 1 and
exact equality across the 5,891-entry source bundle, managed manifest, and
installed files. Required files match in all three maps:

| Path | SHA-256 |
| --- | --- |
| `SKILL.md` | `d7c3d40d08efbb8c58612ce2a0025293596338cb41e9d15c314e66dd0db09319` |
| `references/readable-artifacts.md` | `7dca1355c2b5ae58381e2d8584aeccbe37651eb0137538d42622ed35d25b49af` |
| `scripts/qa_master/skills/professional/functional-api.md` | `80c609e62b919ffbd9b7bf8e6bd93dcf59aad7d78ede890cd32b2a306ead22dc` |
| `scripts/qa_master/skills/professional/regression-evidence.md` | `e0d5183427a49b6f30dbbe6193aa67998c8b2afbc707f287c46d66d646130131` |

The managed backup archive exists (6,651,879 bytes) and its recovery directory
exists (5,904 files); neither was modified by validation. From a non-repository
temporary directory, `py -3.13 -I ...\\scripts\\qa.py skills` exited `0` and
reported 330 vendor resources (165 English, 165 Chinese). No proposal/business
test/host UI operation was performed for this maintenance verification.

## Pre-edit observations

Pre-edit `qa_master/skills/codex/SKILL.md` required the work protocol but did not yet require a readable-artifacts reference before case/defect authoring or review. The protocol requires case fields/observables, but its wide case-table convention can obscure reader-facing flow. CR-037 also records requirement-shaped placeholder risk. These observations do not imply baseline failure.

## Defects

BUG-032 (P2) records the initial cached local-install delivery failure: a force
attempt exited 0 but isolated resources were stale. The initial failure is retained
in `initial-package-cache-failure-2026-10-28.md`; repaired `--reinstall` and
managed-update verification then passed with 5,891 exact source/manifest/installed
hashes. This is validation evidence, not an external defect-closure claim. The
three source-preflight P2 items were resolved instruction-review findings, not new
runtime defects. Any later failure must cite the exact synthetic artifact,
criterion and requirement without generalizing to all outputs or human acceptance.
