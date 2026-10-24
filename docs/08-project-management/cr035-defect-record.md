# CR-035 finite API rejection defects

Document State: DRAFT. Baseline main `8fcaba9`, runtime `c2e7957`.
Existing contracts: REQ-029–031 / NFR-013 (DES-062), REQ-032–036 /
NFR-014 (DES-063). Independent tester TASK-142 and reviewer TASK-143 reproduced
the following before any production repair. All are local engineering findings;
no enterprise issue, human approval or external defect closure is implied.

| ID | Severity | Input / observed behavior | Root cause | Required repair / acceptance | Current state |
| --- | --- | --- | --- | --- | --- |
| BUG-021 | P2 | Valid bundle/library, but a gap reason_code is JSON object or list: audit Python API leaks TypeError, CLI falls back to generic COMMAND_REJECTED. | Membership test in a set precedes reason string validation. | Require string before membership, reject INVALID_GAP; API and CLI exact-code regressions. | REPRODUCED; repair NOT_EXECUTED |
| BUG-022 | P2 | Model method is JSON object/list: audit API leaks unhashable TypeError from _preflight. | Preflight asks set membership before authoritative engine validation/adaptation. | Non-string method rejects stable INVALID_SCHEMA before membership; all valid methods retain existing replay bounds/behavior. | REPRODUCED; repair NOT_EXECUTED |
| BUG-023 | P2 | Output parent is an existing regular file: audit and impact file APIs leak FileExistsError; both CLIs exit1 with traceback/path. | Parent mkdir and temporary-file creation are outside the shared writer's OSError boundary. | Wrap writer preparation in OUTPUT_IO_ERROR adaptation, retain OUTPUT_EXISTS/no-clobber and cleanup semantics. Both APIs/CLIs reject with exit2/value-free JSON; sentinel parent/inputs unchanged. Also independently check temporary-file creation failure. | REPRODUCED; repair NOT_EXECUTED |
| BUG-024 | P3 | Direct file API format={} raises raw unhashable TypeError in audit and impact, rather than INVALID_FORMAT. | Format set membership precedes string validation. | Validate string type before supported-format membership; no writes on rejection. | REPRODUCED; repair NOT_EXECUTED |
| BUG-025 | P2 | Valid open-world state model with128 states,100 triggers,1 explicit transition yields1 candidate/1 logical row in design engine, but audit/impact reject CANDIDATE_LIMIT_EXCEEDED. | Preflight charges full state-trigger product even though open-world engine enumerates only explicit records. | Open-world replay bound uses explicit-transition count; closed-world and other method bounds stay intact. Valid low-work publicAPI example succeeds; aggregate over-limit replay still rejects before enumeration. | REPRODUCED; repair NOT_EXECUTED |
| BUG-026 | P2 | Public renderer accepts impossible MISMATCH with GAP_DUPLICATE and no cases/gaps; also ORPHAN_CASE with candidate_id instead of case_id. | Validator checks generic known codes/key shapes without state-code/variant coherence. | Enforce exact emitter-supported MISMATCH branches and code-specific finding shapes; malformed reports reject INVALID_REPORT while all genuine audit variants render. | REPRODUCED; repair NOT_EXECUTED |

## Bounded repair decision

Modify existing shared validation/write helpers in case_conformance.py,
the impact file API format guard, and developer tests only. Do not alter the design engine, impact report schema,
valid report content, CLI flags, approval states or execution authority. Invalid
model method types consistently use INVALID_SCHEMA; invalid gap reason types
use INVALID_GAP. Preserve source/output link/reparse protections, atomic exclusive
publication and old audit/impact regressions. Do not replace precise domain
errors with a broad generic catch, or return success when writing failed.

Open-world estimate uses explicit transition records when closed_world is
exactly False, retaining conservative existing bounds for closed/invalid modes.
Report validation is structural coherence, not source authenticity: enforce the
actual audit emitter's two MISMATCH variants (gap/case conflict, or one authored
case with nonempty data/reference/documentation diagnostics), and code-specific
finding shapes, preserving root and candidate documentation findings.

BUG-023 follow-up before freeze: independent fault injection also reproduced
cleanup PermissionError escaping from the writer's finally block. The bounded
decision retains the cleanup attempt and preserves any in-flight domain error
(including OUTPUT_EXISTS); otherwise cleanup OSError rejects OUTPUT_IO_ERROR.
After successful atomic publication, that rejection may coexist with an already
published valid report and a remaining temporary file. Do not invent rollback,
delete the published report, overwrite on retry, or silently report complete
success. Caller should inspect the requested destination before retrying.

Independent source tests precede final freeze; independently verify final wheel
and installed helper once after repair stabilization. Full Windows/Linux CI is
regression evidence, not acceptance or an application test result.
