# CR-037 strict default QA writing — independent review

- Artifact: `DOC-CR037-STRICT-INDEPENDENT-REVIEW-001`
- Owner: TASK-159 reviewer `/root/rebind_reviewer`
- Product baseline: `aaf8b1c215a9cc84834668b42f72d3a9304a4fde`
- Fixed acceptance: `d4cdfcc`
- Final instruction freeze: `e47c0f5d031f73bd150ca7c6f88377efab4e919f`
- Review state: `DECIDED`
- Evidence status: independent source and installed-byte review `VERIFIED`;
  model-authored samples and recorded command observations remain `OBSERVED`.
- Final bounded verdict: `PASS`; unresolved P0/P1/P2/P3: `0/0/0/0`.
- Gate, release, human acceptance and external-write effect: none.

## Finding history

The pre-freeze review found two P2 wording ambiguities in the professional
guides. The first drafts could be read as permitting explicitly required raw
artifact/import metadata to re-enter human prose. Both guides now distinguish
actual supplied API/domain/response fields, which remain beside the relevant
step or expected result, from artifact/import metadata, which remains exact only
in a separate payload or support block when a user, project or schema requires
it. The repaired wording is consistent with the canonical entry and readable
artifact reference.

The final evidence review found a further P2 provenance gap: the three fresh
outputs were retained, but their actual dispatched input facts were not. The only
then-durable login input described the older `demo-login-1` fixture, so the review
could not establish whether the new output's username echo and password masking
were supplied facts or invented expectations. The three original task prompts
were subsequently transcribed verbatim from the dispatch calls into
`evidence/cr037/strict-prompts.json`. That file honestly identifies itself as a
late capture made after the outputs, not a preregistered prompt hash or a new run.
Reading it against the retained outputs resolves the factuality issue: echo and
masking were supplied, the file-selection result was explicitly absent, and the
API/schema keys and values were supplied exactly. This resolution supports the
bounded result but does not turn the late capture into stronger provenance.

A final P3 documentation inconsistency marked installed parity `PENDING` after
the independent installed check had passed. The delivery record now reports the
actual 5,891-file equality, helper result and retained backup/recovery evidence.
No unresolved finding remains.

## Requirements and architecture conformance

The final first-party instruction set conforms to the CR-037 clarification of
REQ-041/042 and DES-065:

- default human-facing cases use `步骤 | 操作步骤 | 预期结果`, or an explicitly
  required equivalent, with one fact-grounded expected-result slot for every
  numbered case action, including preparation;
- an unknown step result names the missing observable and affected step instead
  of inventing an echo, mask, UI message, threshold or side effect;
- ordinary prose omits unsolicited `source_role`, `direct_input`, `Trace` and
  synthesized trace IDs, while actual supplied IDs, commands, response fields
  and other technical literals remain exact and locally relevant;
- explicitly required machine fields remain exact in a separate payload/support
  block rather than being dropped, renamed or substituted with prose;
- bug drafts separate setup, numbered reproduction, attributed actual result and
  expected result, and leave unknown evidence, severity, frequency and root cause
  pending;
- requested language and narrow case/bug scope are preserved. Drafting does not
  authorize business execution, tracker/import writes, approval or modification
  of existing cases.

The typed-observation reference now states its activation boundary without
weakening the existing literal-token, synthesized-label or declared-precision
rules. The source-tree entry, canonical installed entry, readable reference,
work protocol and both original professional guides resolve consistently.
Python runtime, generator/validator contracts, audit/impact/proposal schemas,
tracker adapters, permissions and vendored specialist content are unchanged.
No private company knowledge-base body, URL or product detail appears in the
reviewed public source diff.

## Evidence readback

- The strict contract and RED criteria were recorded before the instruction
  changes. Older samples retain their original-rubric PASS results; under the
  new rubric they expose one unpaired preparation action and unsolicited machine
  fields without being relabelled as real product defects.
- Frozen source `e47c0f5` changes eight first-party documentation/instruction
  assets only. `git diff --check` passes; Python and vendored-skill diffs from the
  fixed-acceptance revision are empty.
- `strict-login-output.md` SHA-256
  `90d1dad68e71496c6864a930b72f927eac45feaadbfb616a8bc7b97183fa50a9`
  has three paired case rows, no unsolicited machine fields, and an attributed
  reported actual distinct from the expected result.
- `strict-unknown-output.md` SHA-256
  `715ebe41c7674ea0ca722bca9d53cf361b32d8dd8fef0fdf65569bb287cd6230`
  identifies the missing observable for step 1 and preserves `MISSING_NAME` plus
  the no-new-record rule for step 2.
- `strict-schema-output.md` SHA-256
  `bd525ed02de3ad3c199ac392a4862ad5dc162c756e5654383a949218c30dddc5`
  keeps the supplied response fields in the human expected result and preserves
  every explicitly required key/value in a separate parsed JSON payload.
- The owning tester classified TC-STRICT-001–005 PASS. Root's related source and
  catalogue/document checks ran 29 tests, exit zero, in 1.966 seconds; this was a
  focused run, not a full-suite claim.
- After the managed update, reviewer readback independently compared every source
  bundle, schema-1 manifest and installed file hash: all three maps contain 5,891
  entries and are exactly equal. Critical matches include `SKILL.md`
  (`4935a400a9b4f4b3317fe216de03d142f32d45f025170e01b08a80a59be8b90b`),
  readable-artifacts
  (`8beeef378e1493d0cb12357a0cb2c871726901eababc10bedca3660297356288`),
  functional-api
  (`ac7a7caf9d474d8d0747de91577d660c529d489e36e45dc6fa41f06526759fed`)
  and regression-evidence
  (`388e3a78738c27a13dbd05c9f770832a4fb53e212ec54912f3df44b0876cd98b`).
- The independent tester also observed the isolated installed helper exit zero
  with 330 resources (165 English and 165 Chinese). The delivery record retains
  the managed `UPDATED` result, backup ZIP, recovery tree and final root
  `UNCHANGED` repeat without converting installation into host discovery.

## Limits

All three authoring probes use explicitly synthetic facts. They demonstrate the
bounded default behavior exercised here, not universal future model quality or
human readability acceptance. Prompt inputs were captured late and are therefore
weaker provenance than preregistered bytes despite matching the retained outputs.
No real login, import or API call ran; no bug was submitted, case imported, old
case modified, host UI discovery observed or external system written. No full
suite, production deployment, Gate decision, release approval or human acceptance
is inferred. Git publication, PR merge and final main-branch identity require
separate later readback.
