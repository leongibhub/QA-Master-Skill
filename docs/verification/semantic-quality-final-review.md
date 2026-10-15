# TASK-063 independent review of the semantic-quality evaluator

- Artifact ID: `DOC-SEMANTIC-QUALITY-FINAL-REVIEW-001`
- Proposed Evidence ID: `EVD-SEMANTIC-QUALITY-REVIEW-001`
- Change: `CR-013`
- Requirements: `REQ-025` v1, `NFR-009` v1
- Reviewer: `/root/workflow_review`
- Runtime work: `work-3e45626018de452e85d3b9a92da462f1`, attempt 2 / version 22
- Review result: `PASS WITH P3 FOLLOW-UP`
- Finding counts: `P0=0`, `P1=0`, `P2=0`, `P3=1`
- Document State: `DRAFT`
- Evidence Status: `OBSERVED`
- Date: 2026-10-15

This is the formal independent review of the bounded CR-013 Phase 2 local
semantic-quality evaluator. It does not decide a project Gate, accept full
REQ-025 or the V1 product, close a defect, authorize product execution or an
external write, recommend release, provide a human rating, or establish a
comparison or quality winner.

## Frozen review subject

| Subject | Revision / SHA-256 |
|---|---|
| Product source | commit `a9df28513d4ae808d687718bfc4f6069a32ee767`; `qa_master/semantic_quality.py` `D567D26110EACA5637F54C0DC48994E881BFEDCE69EAFD0C8AA809C41331018A` |
| Requirement sub-contract | `docs/03-requirements/semantic-quality-contract.md` `C28E054C27F86F5C4C21F2892B83414C1C3CC5BE2017E80FD22A41EF28DF7FF7` |
| DES-060 v4 | `docs/04-design/semantic-quality-design.md` `4611C6C9ADD08AE913E25512361B45369C1F439715CF620FCF875D7B51148B42` |
| Independent attempt 3 report | `docs/verification/semantic-quality-independent-attempt3.md` `3DC80AEF26D7236FBFD909E0E0556A5E260D9699AB70AEB3026B3C0F77E02AC0` |
| Independent attempt 3 manifest | `docs/verification/evidence/cr013-semantic-independent-attempt3/attempt3-manifest.json` `FED86A6E446983E2437BED994AAA363A2810E3E018A65023762E26A426D353E3` |
| Independent test source | `tests/test_semantic_quality_independent.py` `68A1E704ED5FB71DF7EF3A6EBF2C4FD93FF85BCD0C7439CCCECFC98258D17195` |
| Developer test source | `tests/test_semantic_quality.py` `6FBC0A6E3C8BE265976E8112EACA1A22D4ACEB2CF9ACE0784DD0F9DF7BE484E6` |

The six registered package resources match the source constants and retained
fresh-process result: contract `EC9D6232...04A`, current projection
`25AA3F1B...C55`, legacy projection `DE207A59...8F3`, normalizer
`A3C9D024...4D9`, result schema `FD356165...EC0`, and secret scanner
`FB26EF33...176`.

The review also binds the historical evidence rather than replacing it:

- attempt 1 FAIL report `99CD6131...35C4` and manifest `CC8ECA0A...BC71`;
- attempt 2 FAIL report `1776CD8C...E624` and manifest `636B4624...5A70`;
- prefreeze findings `DOC-SEMANTIC-QUALITY-PREFREEZE-FINDINGS-001`,
  `21DF61AF...1F60`; and
- repair precheck `DOC-SEMANTIC-QUALITY-REPAIR-PRECHECK-001`,
  `44A92D2F...A2DD`.

Repository HEAD at formal review time contains later test/evidence commits, but
the product module hash remains exactly the frozen `a9df285` subject.

## Finding

### P3 — semantic evaluator link/reparse rejection lacks a task-specific executed case

DES-060's path and inspection matrix includes input/output containment and
link/reparse rejection. The implementation checks every existing path component
with `is_symlink` plus the Windows reparse-point attribute before reading or
publishing, and inspection applies the same boundary to retained children.
Static review found no bypass in the declared local, non-hostile-concurrency
scope.

The TASK-062 attempt 3 focused suite and retained semantic evaluator evidence do
not execute a link/reparse fixture for this module. The full 689-test run skipped
three Windows symlink cases because the host lacked symlink privilege; those
cases belong to the installed-skill and paired-runtime modules and therefore do
not substitute for semantic evaluator coverage.

Impact is a bounded regression-evidence gap in a defensive path boundary. It
does not demonstrate a current source failure, and it does not block the local
content-addressed evaluation scenarios exercised by TASK-062.

Recommended follow-up: on a Windows host with symlink privilege, or with a
controlled reparse-point fixture, independently exercise semantic evaluator
bundle/source input, output reservation, and result inspection paths. Verify
typed rejection, no link following, no partial publication, and preservation of
an existing destination. A POSIX symlink run is also useful for cross-platform
coverage. This follow-up must create new evidence and must not rewrite TASK-062.

## Requirement and architecture conformance

The frozen source conforms to the reviewed REQ-025/NFR-009 sub-contract and
DES-060 within the bounded Phase 2 scope:

- bundle validation binds exact registered contract, projection, normalizer,
  result-schema and scanner bytes before evaluation. Source locators are local
  controlled paths; source bytes remain opaque and content-addressed;
- the response normalizer preserves independent observation, case and gap
  channels. Fatal envelope failure, recoverable shape defects, semantic value
  defects, usability defects and provenance defects remain separate;
- typed comparison distinguishes booleans from integers, caps integers at 34
  magnitude digits, retains canonical decimal text, bounds string sets at 256,
  and applies controlled JSON depth/node limits without coercion;
- every obligation produces exactly four ordered rows with stable outcome,
  reason, source fact and evidence-pointer fields. The evaluator emits no score,
  aggregate, rating, approval, winner, execution, acceptance, release or Gate
  field;
- missing, conflicting and unsupported oracles remain typed gaps. A gap never
  satisfies semantic truth, and a case remains draft-only rather than being
  promoted to executable readiness;
- item-wide identity, claims, sections and serialized references are prepared
  once. Fixed-size obligation/fact/source masks and reverse indexes separate
  item-wide validity from obligation-specific checks. Each explicit mapping
  edge performs indexed membership and subset operations, while actual row and
  evidence-pointer materialization accounts for result size. This satisfies the
  design's `O(V + E + R)` bound for the reviewed joins;
- case-to-gap validity requires the referenced gap's unique identity and an
  obligation-binding intersection. Mixed known/unknown mappings invalidate only
  their known targets; unknown-only items cannot alter unrelated obligations;
- publication reserves a deterministic result identity, stages retained bytes,
  commits the manifest last, refuses overwrite and preserves unrelated data on
  injected failure. Inspection validates the strict manifest, file ledger,
  installed evaluator/assets and pure re-derivation without executing retained
  code or reaching a network target; and
- the registered legacy projection remains `UNSCORABLE` and the retained CR-011
  pilot bytes are not regraded or modified.

No unresolved correctness, security, concurrency, data-integrity,
failure-handling, backward-compatibility or material performance finding was
observed at P0, P1 or P2 severity.

## Historical findings and repair assessment

| Historical finding | Retained failure | Assessment of frozen subject |
|---|---|---|
| P2 — `STRING_SET` maximum absent | attempt 1 TC021/TC022 | Facts accept 256 and reject 257; observations classify 257 as invalid rather than mismatched. |
| P2 — malformed retained manifest misclassified | attempt 1 TC023 | Exact top-level and nested manifest validation now precedes inspection status precedence; malformed input is `INCOMPLETE`, while valid changed identity/content remains `MISMATCH`. |
| P2 — repeated case/gap joins | attempt 1 structural observation and attempt 2 TC027 FAIL | Prepared records and indexes remove repeated whole-list validation across obligation fan-out while preserving per-obligation semantics. |

These repair observations support governance disposition for the bounded
findings. They do not erase attempts 1 or 2 and are not a unilateral defect
closure decision.

## Verification evidence assessed

TASK-062 attempt 3 was performed by an independent tester and records:

- 30 focused tests passed in 23.560 seconds;
- the same 30 tests passed in 28.145 seconds against a newly built wheel in a
  fresh virtual environment, imported from `site-packages` under isolated
  Python;
- the strict full regression completed 689 tests in 151.297 seconds with three
  unrelated Windows symlink cases skipped;
- supplementary sibling-gap, duplicate-gap and mixed-known/unknown binding
  scenarios passed and preserved unrelated-obligation isolation;
- at 4, 8, 16 and 64 obligation bindings, the same mapping list was validated
  three times at every size, with 12, 24, 48 and 192 element visits. Attempt 2
  had observed 10, 18, 34 and 130 validations;
- six installed assets and the evaluator module were byte-equal across source,
  wheel, installed Skill and retained result. Two isolated processes from an
  unrelated working directory retained 13 result files byte-identically;
- prohibited-field rejection created no result root and did not echo the
  controlled fixture value; and
- the 17 retained CR-011 pilot files were unchanged. No model call, enterprise
  write, product execution or human rating occurred.

Before TASK-063 was claimable, this reviewer performed a read-only precheck on
the same frozen source. At that time it was explicitly not a formal review
conclusion. The formal review now uses it only as corroborating material bound
to the identical source hash:

- the former 64-obligation reproduction decreased from 1,217 reference-list
  calls / 9,152 element visits to 138 calls / 262 visits while retaining 256
  output rows;
- six targeted fan-out, readiness, sibling-gap, duplicate-gap, invalid-binding
  and fatal-channel tests passed in 2.872 seconds; and
- old and repaired profiles were exactly equal across 15 representative valid
  and invalid scenarios. Duplicate gap identity was separately verified as the
  intentional DES-required correction.

The structural counts establish the repaired join behavior under the finite
schema limits; they are not a timing benchmark, throughput/SLA result, or proof
for an unbounded workload.

## Verdict boundary

The frozen `a9df285` semantic-quality evaluator passes independent review for
the bounded local, process-free REQ-025 Phase 2 slice, with the P3 path-fixture
follow-up above. P0, P1 and P2 counts are zero for this subject.

The verdict does not establish full REQ-025 or V1 acceptance, a qualified
holdout, human narrative assessment, comparison fairness or superiority,
executable target readiness, enterprise/provider integration, performance or
availability qualification, hostile concurrent-filesystem security, a project
Gate, release readiness, deployment, or defect closure.
