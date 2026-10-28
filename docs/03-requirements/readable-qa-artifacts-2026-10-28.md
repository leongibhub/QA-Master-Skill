# CR-037 — readable test cases and defect drafts

Document State: DRAFT. User authorizes a writing-quality repair to QA Master.
Baseline: main `8a22a9f45f514c4cebd7be67317ed5044bc4cc28`.

## Problem and scope

The user reports that generated cases and bug reports are often difficult for
people to understand. Source inspection confirms that the mandatory entry lacks
a concrete reader-facing writing contract. The work protocol puts many metadata
fields in one case table; the conservative generator can emit requirement-shaped
placeholder steps. Those outputs are candidates, not usable authored cases.

This change repairs first-party instructions/templates and documentation. It does
not change generator algorithms, audit schemas, tracker adapters or execution
permissions. Existing source values, formal IDs and machine-readable fields must
remain intact. User-provided real unreadable examples are NOT_AVAILABLE; synthetic
fixtures and their limitations must be labeled. No existing remote issue or case
will be edited merely because this writing rule changes.

## Requirements and acceptance

| ID | Requirement | Observable acceptance |
| --- | --- | --- |
| REQ-041 | Default authored cases and bug drafts use the user's language and can be understood without prior chat. | Cases have a concrete scenario title, explicit known setup/data, numbered actions with observable expected results, and cleanup where needed. Bug drafts have a symptom title, environment/setup, numbered minimal repro, separate expected/actual results, known impact and locatable supplied evidence. Bulk lists may use a summary table plus case detail rather than an unreadably wide table. |
| REQ-042 | Readability preserves facts and permission boundaries. | Retain exact commands, API/error names, values/units, constraints, sources and machine IDs; explain essential jargon on first use. Do not invent UI paths, thresholds, messages, credentials, evidence, frequency, severity policy or root causes. Missing execution information stays a plain-language question and affected draft remains unexecuted. No external write/execution is authorized by drafting or rewriting. |

Acceptance examples cover a Web negative case and matching observed-defect
fixture, an API validation case, and an incomplete performance requirement.
Synthetic observed facts are fixtures, never actual business executions. No
universal readability, model-quality, human acceptance or competitor claim follows
from these examples.

## DES-065 / implementation plan

Add an original bundled `references/readable-artifacts.md` with compact Chinese
templates, worked synthetic examples and a pre-delivery reader check. The canonical
Skill must require reading it before authoring/reviewing cases or defect drafts,
including specialist-selected work and tracker packets. Wire the source entry,
work protocol and original functional/regression guides to that rule. Keep raw
technical evidence in a supporting section, not as a substitute for a plain-language
explanation. Existing format/project fields remain compatible. Do not alter
vendored specialist files or license attribution.

| Task | Actual owner | Responsibility |
| --- | --- | --- |
| TASK-154 | /root; implementation delegated to /root/rebind_docs | Requirements/CR/RTM; first-party writing instructions/templates and README. |
| TASK-155 | /root/readability_baseline and /root/rebind_tester | Unchanged baseline authored samples, independent evaluation and post-change fresh samples; managed installed-bundle verification. |
| TASK-156 | /root/rebind_reviewer | Independent scope/consistency/factuality review and issue readback. |

Sequence: freeze baseline outputs and evaluation rubric before editing instructions;
implement the bounded repair; independently inspect source/packaged asset wiring,
evaluate fresh outputs without claiming a human study; review; update the managed
local installation and verify; publish through a branch/PR with actual readback.
Do not fabricate a failing baseline if the baseline author already writes clearly.
Record any baseline PASS and the confirmed instruction gap separately.

## Evidence and governance

Current stage: scoped development and verification of a writing-quality repair.
All project Gates remain unchanged; Runtime registration and human acceptance are
NOT_AVAILABLE. Results are PENDING until recorded in verification documents.
Company knowledge-base guidance was consulted read-only; internal documents,
product data, identifiers and examples must not be copied into the public bundle.

Delivery-method follow-up: local same-path uv refresh reused an old cached wheel.
BUG-032 is recorded in the delivery report; existing-user update instructions
add `--reinstall`, with fresh-build/resource verification. This is propagation of
the same authorized instruction repair, not a runtime or permission change.
