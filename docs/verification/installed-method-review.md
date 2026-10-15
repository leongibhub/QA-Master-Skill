# TASK-058 independent review of the installed method workflow

- Artifact ID: `DOC-INSTALLED-METHOD-REVIEW-001`
- Proposed Evidence ID: `EVD-INSTALLED-METHOD-REVIEW-001`
- Change: `CR-013`
- Reviewer: `/root/workflow_review`
- Runtime work: `work-e820bc1fe844439ebfdea5ad000bc958`
- Review result: `PASS WITH P3 FOLLOW-UP`
- Finding counts: `P0=0`, `P1=0`, `P2=0`, `P3=1`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Date: 2026-10-15

This is the formal independent review of the bounded Phase 1 installed offline
design workflow. It does not decide a project Gate, approve requirements,
accept the full product, authorize product-test execution or external writes,
recommend release, or establish a quality comparison or winner.

## Frozen review subject

| Subject | Revision / SHA-256 |
|---|---|
| Product source | `8b5017af42c7675cd32f941b71c85cf79b30d499` / `CODE-INSTALLED-METHOD-WORKFLOW-001` v3 |
| DES-055 | `docs/04-design/installed-method-design.md` / `63CB5E48B0688D1DDEDFE8800C062D02F5A91DFFA244A8A2D160460E747970A5` |
| Installed dispatcher | `qa_master/__main__.py` / `283DF2A52409C537090F26BCC9EFD4418660F91368CDDAD8E3103470654D203D` |
| Installed projection | `qa_master/campaign_cli.py` / `630EAB0DB06D7C7A57A661F377E7089137353FD137872005F6B27379F3D93564` |
| Packaged method reference | `qa_master/skills/codex/references/design-methods.md` / `128DF839DA4B48DF2B40DE1B943EE0E1C1B76573FDAAAEF2717E5E8087F4265F` |
| Packaged example | `qa_master/skills/codex/examples/design-methods.json` / `3C90119659C20A35B7A9178A0224D4D3FC5AB4456E331B8A9C25E1A60FB38E64` |
| TASK-057 attempt 3 report | `docs/verification/installed-method-independent-attempt3.md` / `8B1EFB654B81BAB32D5FE98C619FFA1065E5C179938A79288C5A91FB81A386BB` |
| TASK-057 attempt 3 manifest | `docs/verification/evidence/cr013-independent-attempt3/attempt3-manifest.json` / `DAEA11DD4B941765D6094C3D5568BA9BF41DA6743C3A18CEA554F59929E54B10` |

The evidence-only repository commit at review time is `3d8dd67`; a path-scoped
comparison found no changes under `qa_master/` or `README.md` relative to the
frozen product subject. The historical attempt 2 failure and BUG-014 record
remain separate and unchanged.

## Finding

### P3 — legacy `case_review.pass` can be misread without its companion fields

The actual installed report contains `case_review.pass: true` while the same
object contains three `UNAPPROVED_TRACE` issues with severity `MAJOR`, and the
report also records `PENDING_HUMAN`, `formal_baseline_approved: false`,
`DRAFT_UNAPPROVED`, and `NOT_EXECUTED`. The packaged reference now explicitly
defines this legacy boolean as absence of a blocker-level structural finding;
it is not requirement quality, case completeness, approval, execution, or an
overall product PASS. The installed projection also keeps
`usable_case_claim` and `executable_case_claim` false.

The explicit companion fields and documentation prevent this ambiguity from
being a material correctness issue in the reviewed workflow. A consumer that
reads the boolean alone can still overstate readiness.

Recommended follow-up: if the legacy report schema is revised, add an explicit
structural-review discriminator or a versioned field with narrower naming.
Preserve the current field for backward compatibility until consumers have a
migration contract.

## Requirement and architecture conformance

The reviewed source conforms to the bounded REQ-025 Phase 1 and DES-055 path:

- `scripts/qa.py design --input --output` routes in process to the existing
  strict Campaign loader and deterministic method engine. Both global and
  subcommand parsers reject abbreviated or unknown options, and duplicate
  input/output options fail before publication.
- Installed projection is opt-in. Direct `campaign_cli` behavior keeps its
  legacy report shape when the flag is omitted, while installed output adds
  only the documented guide, source, gap and method-ID projection.
- Guide rows bind stable installed locators and exact packaged-byte hashes.
  Source rows remain `DECLARED` or `DECLARED_DIGEST`; neither status claims
  that a locator was opened, authorized, or independently verified.
- The packaged reference is sufficient to construct all three strict method
  models and now distinguishes generic requirement `text`, `source`, and
  `acceptance` from model titles, model refs and method oracles. The example is
  non-secret, covers boundary, decision-table and state-transition input, and
  keeps `approved: false`.
- Complete validation and report construction occur before the temporary
  output is published. Successful publication atomically replaces only the
  requested report. The command does not load Campaign state, invoke a model,
  spawn a runner, use the network, write an adapter, approve a requirement, or
  create an execution result.
- Existing method and Campaign limits bound input, model enumeration and
  projection work. No performance, throughput, remote-provider, enterprise or
  production claim is made.

No unresolved correctness, security, concurrency, data-integrity,
failure-handling, backward-compatibility or material performance finding was
observed at P0, P1 or P2 severity.

## Actual task content review

The retained attempt 3 task provides evidence beyond helper shape checks:

- three source-grounded generic requirements retain nonempty `text`, `source`
  and `acceptance`; the helper reports zero `EMPTY_REQUIREMENT`,
  `NO_PROVENANCE` or `NO_ACCEPTANCE` findings and produces three generic draft
  cases;
- all 13 deterministic candidates are linked exactly once to completed draft
  cases: boundary values/classes are exactly `1/LOWER_INVALID`, `2`, `3`, `5`,
  `6/IN_DOMAIN`, and `7/UPPER_INVALID`; the four boolean rebate assignments
  yield rebate only for `member=true, settled=true`; and the three explicit
  state rows are DRAFT/submit to REVIEW, REVIEW/publish to PUBLISHED, and
  DRAFT/publish invalid with status remaining DRAFT;
- the fourteenth draft separately covers the source-declared initial DRAFT
  state. It is not presented as a synthesized method candidate;
- the invalid publish draft does not invent an unchanged-persistence oracle,
  error code, UI or API. REVIEW/submit and terminal-state event behavior remain
  typed gaps rather than inferred denials;
- all 14 drafts remain `DRAFT_UNAPPROVED`, `NOT_EXECUTED`, and
  `INCOMPLETE_TARGET_BINDING`. The 15 typed gaps retain missing target,
  environment, setup, observable, cleanup, authorization, baseline, error,
  side-effect, representation, unspecified-transition, NFR, structural,
  recovery and regression facts;
- the task records 10 installed documents read and did not rely on the packaged
  example. This supports reference self-containment, while the recorded agent
  review remains an agent assessment rather than human acceptance.

The reviewer reconciled all 42 final manifest entries against the retained
bytes: every length and SHA-256 matched. The source facts hash
`A52B944D6A6D406C40090AED4C4E2680263D8A9BA96955571421A72631284B7C`
matches both the frozen task source and preserved copy.

## Historical findings and closure advice

| Historical severity | Observation | Resolution in reviewed subject |
|---|---|---|
| P2 | Global argparse accepted abbreviated `--sta`, allowing unintended state-option parsing. | `a6f4e33` sets `allow_abbrev=False`; attempt 3 retains strict installed CLI checks. |
| P2 | The first packaged method reference omitted enough decision/state grammar, limits and output/error detail to construct the strict three-model bundle reliably. | `f62932b` expanded the reference/example; installed and actual-task evidence exercises all three methods. |
| P2 / BUG-014 | Attempt 2 produced 18 missing semantic-field findings and zero generic cases because the installed reference did not specify legacy requirement `text`, `source`, and `acceptance`. | `8b5017a` documents the fields and updates the example; a fresh hint-free attempt produced three generic cases and none of the prior missing-field findings. |

The fresh installed attempt, actual task artifacts and this independent review
are sufficient to recommend that governance close BUG-014 for its documented
packaged-reference scope. This recommendation does not erase attempt 2, close
any broader quality gap, or constitute a Gate or acceptance decision.

## Verification evidence assessed

- TASK-057 attempt 3 records 8 focused independent tests passed and the same 8
  tests passed against a newly built wheel installed in a fresh environment.
- The tester retained the initial test-only documentation-token mismatch and
  its correction; no product file changed during that correction.
- GitHub Actions evidence for an equivalent `8b5017a` tree records 605 tests
  passing on Ubuntu and Windows with Python 3.10 and 3.12. This is observed CI
  regression evidence, separate from the independent fresh-wheel task.
- The prior attempt 2 report and manifest remain byte-addressable with their
  original FAIL/P2 result. Attempt 3 created new artifacts and did not rewrite
  the failed history.
- This reviewer performed source, document, case/gap and manifest reconciliation
  only; no product tests or model calls were rerun under TASK-058.

## Verdict boundary

The frozen installed offline method workflow passes independent review for the
bounded REQ-025 Phase 1 route, with the P3 legacy-field follow-up above. It is
reviewable evidence that a fresh installed Skill can reach deterministic method
design and support source-grounded draft/gap authoring without inventing
execution readiness.

Phase 2 semantic scoring, full REQ-025/NFR-009 acceptance, independent holdout
evaluation, human narrative review, comparison or superiority, real target
execution, enterprise integration, performance qualification, project Gate,
release readiness and deployment remain outside this verdict or
`NOT_EXECUTED`.
