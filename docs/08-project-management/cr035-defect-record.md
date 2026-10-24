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

## Bounded repair decision

Modify the existing shared validation/write helper in case_conformance.py and
developer tests only. Do not alter the design engine, impact report schema,
valid report content, CLI flags, approval states or execution authority. Invalid
model method types consistently use INVALID_SCHEMA; invalid gap reason types
use INVALID_GAP. Preserve source/output link/reparse protections, atomic exclusive
publication and old audit/impact regressions. Do not replace precise domain
errors with a broad generic catch, or return success when writing failed.

Independent source tests precede final freeze; independently verify final wheel
and installed helper once after repair stabilization. Full Windows/Linux CI is
regression evidence, not acceptance or an application test result.
