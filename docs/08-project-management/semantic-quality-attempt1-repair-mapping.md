# CR-013 semantic-quality attempt1 repair mapping

- Artifact ID: `DOC-SEMANTIC-QUALITY-ATTEMPT1-REPAIR-MAPPING-001`
- Document State: `DRAFT`
- Evaluation State: `IN_REVIEW`
- Evidence Status: `OBSERVED`
- Change: `CR-013`
- Frozen subject: `6905e0209b1159c8a8fd2b5799a74cf22adea240`
- Source: `qa_master/semantic_quality.py`, SHA-256 `65DD50954784B6EB8D632869CD95162B6F028FF6F63618DDD83739658A220295`
- Design: `DES-060` v4, SHA-256 `4611C6C9ADD08AE913E25512361B45369C1F439715CF620FCF875D7B51148B42`
- Primary evidence: `docs/verification/semantic-quality-independent-attempt1.md`, SHA-256 `99CD6131A8E137819F405801240A6DEF18B1B88CD6E54271E150D0B1581835C4`; manifest SHA-256 `CC8ECA0AE33C279F1AA23E4365E216A5027BE7A58BE763EF43E134CEC3B6BC71`
- Review input: `DOC-SEMANTIC-QUALITY-PREFREEZE-FINDINGS-001`, SHA-256 `21DF61AF29B1D2BD0AB34DFA9EFCFA93C59FA4AF8E0F65E3B889E6E2F0591F60`

This mapping corrects a post-hoc Runtime registration error without rewriting
the retained tester report, review report, command logs, or source history.
It defines the repair input for the next developer task. It is not a repair
result, an independent retest, a review conclusion, a Gate decision, or a
defect closure.

## Actual independent reproduction mapping

The retained attempt1 command ran four tests: `TC020` passed, and the tester's
`TC021`, `TC022`, and `TC023` failed. The three failures are two manifestations
of one typed-value defect plus one separate manifest-classification defect.

| Retained tester case | Actual observation | Finding / defect grouping | Repair acceptance input |
|---|---|---|---|
| `TC021` | A sorted unique `STRING_SET` with 257 fact elements was accepted although the frozen cap is 256. | `P2-1`, `STRING_SET` fact-limit manifestation. | Reject 257 while retaining valid 256, sortedness, uniqueness, nonempty values and per-value bounds. |
| `TC022` | A matching 257-element observation produced `VIOLATED/OBSERVED_VALUE_MISMATCH` instead of invalid-value handling. | `P2-1`, the *same* `STRING_SET` limit defect expressed through the observation channel. | Apply the same 256-member validation to observations and classify invalid values through the typed boundary. |
| `TC023` | A retained manifest with `evaluation_id: []` was reported `MISMATCH`, where malformed manifest input requires `INCOMPLETE`. | `P2-2`, malformed-manifest classification. | Validate the full manifest and nested rows before integrity comparison; retain the frozen precedence boundary between malformed, missing, mismatched and undeclared state. |

Therefore, an implementation repair may retain three Runtime defect records for
the two actual `STRING_SET` manifestations and the actual malformed-manifest
manifestation. It must not describe `TC021`, `TC022`, and `TC023` as three
different prefreeze P2 categories.

## Separate fanout finding

`P2-3` is distinct from the three retained tester case labels. The reviewer
found a case-by-gap rescan in the source, and the tester preserved structural
call-count evidence: four cases/four gaps caused 40 validations; eight/eight
caused 144. This is evidence for the frozen linear-work contract and repair
acceptance, but it is **not** a separately executed `TC021`/`TC022`/`TC023`
test outcome. The repair must pre-index and reuse case/gap validation, then a
new repaired-source independent attempt may execute a dedicated structural
acceptance check.

## Runtime reconciliation boundary

An earlier post-hoc Runtime registration associated `TC-SQ-023` with the
fanout observation. That association is non-authoritative for repair scope and
must remain audit-visible rather than being silently overwritten. Its linked
execution and defect are excluded from the repair input. The authoritative
mapping for this repair is the retained tester report and this document:
`TC-SQ-023` means malformed manifest; fanout is a separately traced review
finding. Any corrected late Runtime registration must state its source and
late-registration boundary explicitly; it must not claim a new test command
was executed.

The correction is now registered as `TM-SEMANTIC-QUALITY-001` v2 with
`TC-SQ-021` v2 (fact), `TC-SQ-022` v2 (observation), and `TC-SQ-023` v2
(manifest). The late records retain the original report and
`reviewer-findings-reproduction.txt` hashes, name the original execution
window `2026-10-15T12:11:21Z`, and state that registration did not run a new
command. Their resulting failure records are respectively
`BUG-783e10233d884414b0a35f61b4d4663b`, `BUG-b703e7354d6a4e528e8d7c88d0107774`,
and `BUG-1bcc4e8df00340b790cc2a148500564b`.

The obsolete v1 fanout association—`execution-20c72a693cf442d6b5b49e1973567e10`,
`BUG-b2dba0ae6e37441bb12c82fcb451cc1b`, and its completion evidence—is
superseded as a Runtime test-registration basis. It remains retained only to
explain the correction; it neither supplies a repair input nor describes a
newly executed tester case.

## Bounded repair scope and follow-up

The developer repair is limited to all three types of work:

1. enforce the `STRING_SET` member cap in fact and observation paths;
2. strictly parse/classify malformed manifests before deterministic comparison;
3. replace repeated case-by-gap validation with bounded indexed reuse.

The failed attempt1 evidence remains immutable. TASK-062 attempt3 later passed
on final `a9df285`, and TASK-063 formally reviewed that bounded subject as
`PASS WITH P3 FOLLOW-UP`; the P3 is missing semantic-evaluator-specific
executed DES link/reparse-rejection fixture evidence. The three correctly
mapped fact/observation/manifest Runtime defects remain OPEN because the
platform closure workflow requires a canonical fix/retest test-execution chain
that was not created; this is a platform-record limitation, not a claim that
the defects remain reproduced on `a9df285`. The obsolete v1 fanout association
remains non-authoritative. No human assessment, holdout, quality comparison,
overall V1, acceptance, release, or Gate conclusion is implied.
