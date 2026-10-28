# CR-037 strict default QA writing — independent verification

**Owner:** TASK-158 independent tester
**Basis:** strict contract `d4cdfcc`, REQ-041/042 and DES-065.
**Status:** `PASS` (bounded independent verification) — strict source wiring, three fresh probes, and repaired managed local-install verification pass. This is a bounded instruction-artifact check, not a business test, human acceptance, or external-write authorization.

## Frozen strict rubric

| ID | Contract check | Pass condition |
| --- | --- | --- |
| STRICT-WRITE-01 | Step mapping | Every numbered action, including preparation, has its own adjacent expected result. If that result is unknown, state exactly what is pending for that step; do not invent an echo, mask, message, threshold, or side effect. |
| STRICT-WRITE-02 | Human-facing default prose | Ordinary case/bug prose contains no unsolicited raw `source_role`, `direct_input`, `Trace`, or synthesized trace ID. Supplied real IDs, commands, values and human source references remain. |
| STRICT-WRITE-03 | Required machine payload | If the user/project/import schema explicitly requires raw machine fields, preserve their exact names and values in a separate machine payload/support block; do not silently drop, rename, or narrativize them. |
| STRICT-WRITE-04 | Bug readability | Symptom, setup, numbered reproduction, actual and expected appear as clear separate parts; observation attribution and unknown evidence/severity/cause remain honest. |
| STRICT-WRITE-05 | Scope | The user language and requested case/bug scope are retained; no unsolicited strategy, matrix, handoff or lifecycle payload. |
| STRICT-WRITE-06 | Boundaries | No business execution, approval, tracker write, external import or fabricated unknown fact is claimed. |

## Actual baseline findings under the new contract

Prior samples remain PASS against their earlier rubrics. They are RED only under
these new strict checks:

| Finding | Artifact / observable basis | New-criterion result |
| --- | --- | --- |
| Unpaired preparation action | `evidence/cr037/after-output.md`, TC-DEMO-001 line 21: “将数量设置为 `0`。（准备）” has no own expected result. | FAIL STRICT-WRITE-01 |
| Unsolicited raw fields | `evidence/cr037/login-explicit-output.md`, lines 9–10 add `source_role: [direct_input]` and synthesized `Trace: LOGIN-INVALID-INPUT` without a supplied schema requirement. | FAIL STRICT-WRITE-02 |

These failures do not assert bad facts, real product defects, or universal model
behavior. They establish the strict-default regression target. No fake baseline
failure is added.

## Planned independent probes

| TC | Probe | Status |
| --- | --- | --- |
| TC-STRICT-001 | Ordinary Chinese login request without explicit formatting reminder | PASS — fresh artifact `strict-login-output.md` |
| TC-STRICT-002 | Unknown preparation expectation | PASS — fresh artifact `strict-unknown-output.md` |
| TC-STRICT-003 | Explicit machine-payload request with supplied API response field and `source_role` | PASS — fresh artifact `strict-schema-output.md` |
| TC-STRICT-004 | Frozen source/reference wiring and relevant existing checks | PASS — frozen source inspection and 29 related root checks |
| TC-STRICT-005 | Repaired local install source/manifest/target hash parity | PASS — final full-map and isolated-helper readback below |

Fresh authors receive the fixture facts from the strict contract. The tester will
evaluate their actual outputs but will not author replacement artifacts. Sample
results demonstrate only bounded capability/default behavior for those facts.

## Frozen source and fresh probe results

Source `e47c0f5d031f73bd150ca7c6f88377efab4e919f` passes bounded wiring: the first-party canonical/reference, source entry, work protocol, original functional/regression guides and README require one-to-one action/expected mapping, precise pending unknowns, no unsolicited machine keys in human prose, and separately retained required payloads. Frozen diff excludes vendor/runtime/schema/adapter/packaging/permission changes. Root reported 29 relevant checks PASS in 1.966 seconds; this tester did not run a full suite.

- `strict-login-output.md` (`90d1dad68e71496c6864a930b72f927eac45feaadbfb616a8bc7b97183fa50a9`) passes STRICT-WRITE-01, 02 and 04–06: three one-action/one-expected login rows, no unsolicited raw keys, reported—not Agent-reproduced—bug actual, and pending unknowns.
- `strict-unknown-output.md` (`715ebe41c7674ea0ca722bca9d53cf361b32d8dd8fef0fdf65569bb287cd6230`) passes STRICT-WRITE-01, 02, 05 and 06; STRICT-WRITE-03/04 are not applicable. The selection preparation explicitly says its expectation is pending and identifies step 1; step 2 retains `MISSING_NAME`/no new records.
- `strict-schema-output.md` (`bd525ed02de3ad3c199ac392a4862ad5dc162c756e5654383a949218c30dddc5`) passes STRICT-WRITE-01–03, 05 and 06; STRICT-WRITE-04 is not applicable. Human expected text keeps supplied API response facts `source_role=member` and `Trace=trace-demo-01`, while separate parsed JSON exactly preserves `id`, `source_role`, `Trace`, `execution`, and `steps` values.

These samples demonstrate bounded ordinary-default capability, unknown-step honesty and machine-payload compatibility only; they do not establish universal model behavior, human acceptance, business execution or external-write authority.

## Prompt provenance and final managed-install verification

`evidence/cr037/strict-prompts.json` retains the exact three author dispatch prompts and records its limitation: it was durably transcribed after the outputs existed, rather than preregistered prompt bytes. Reading the late-captured prompts against the retained output hashes above reaffirms that the login, unknown-preparation, and required-schema probes used the stated facts and scopes. It does not alter the rubric frozen before source edits or convert the late capture into a new execution.

For TC-STRICT-005, an independent schema-1 manifest comparison after the repaired managed update reported `5891` source-bundle files, `5891` manifest files, and `5891` installed files; source-to-manifest and installed-to-manifest mappings were both exact. Six critical source/installed SHA-256 pairs also matched:

| Path | SHA-256 |
| --- | --- |
| `SKILL.md` | `4935a400a9b4f4b3317fe216de03d142f32d45f025170e01b08a80a59be8b90b` |
| `references/readable-artifacts.md` | `8beeef378e1493d0cb12357a0cb2c871726901eababc10bedca3660297356288` |
| `references/typed-observations.md` | `b0ad392cf5a8ed703abe281fa61332b2fa3aaf26286616b5c616efb3227bfcf8` |
| `references/work-protocol.md` | `521c495f53cadbc06272c34cd3a89e8e0176051a6b17d08ebbcf2a3aa7938629` |
| `scripts/qa_master/skills/professional/functional-api.md` | `ac7a7caf9d474d8d0747de91577d660c529d489e36e45dc6fa41f06526759fed` |
| `scripts/qa_master/skills/professional/regression-evidence.md` | `388e3a78738c27a13dbd05c9f770832a4fb53e212ec54912f3df44b0876cd98b` |

The managed update retained backup `qa-master.backup-afe157c111ff49fc8923e5061adada90.zip` (`6,607,992` bytes) and its matching recovery directory (`5,902` files); presence only was checked, without mutation. From a non-repository temporary directory, isolated installed helper `skills` exited `0` and reported 330 skills (165 English and 165 Chinese). No proposal, business execution, external import, or host UI interaction occurred. A separate Windows Unicode-argument harness failure remains delivery evidence outside this bounded product/Skill verdict and is not reclassified here.
