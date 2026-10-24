# Non-applied after-change case-library proposal

Use this only when a saved finite model changed and the user wants a reviewable
draft of its after-version case library. The QA user stays in ordinary chat:
ask the Agent to prepare the before bundle, after bundle and before-bound case
library JSON. The user does not hand-fill JSON.

This is CR-036 DRAFT guidance, not a lifecycle Gate decision or Gate evidence.

The command produces a draft proposal, not a case-library update. It makes no
campaign or external-system change, runs no test, grants no approval and never
authorizes regression to be skipped. `DRAFT_UNAPPROVED`, `NOT_EXECUTED`, and
`NOT_APPLIED` describe its proposal state; they are not a test or quality
result.

## Agent workflow

1. Keep the old bundle and strict v1 case library together; the library must
   bind to the before design digest. Create the after bundle from declared
   facts, including refreshed source/oracle descriptors when known.
2. Run the proposal command. It freshens finite-model impact and the after
   audit; do not supply a prior impact report as a substitute.
3. Review every emitted case and row decision against the real sources and
   case prose, even when its formal vector is unchanged. Also review held gaps,
   missing-vector followups, baseline findings, obligation deltas and unknowns.
4. After human review, an Agent may extract only the nested
   `proposed_case_library` into a **new** case-library file and audit that file
   against the after bundle. The proposal envelope itself is never valid
   `--cases` input. There is no apply command.

From a source checkout:

```text
python -m qa_master propose-method-case-library --before old-bundle.json --after new-bundle.json --cases old-cases.json --output proposal.json
```

From an installed Skill, resolve the Skill directory and use its helper:

```text
python -I "<skill>/scripts/qa.py" propose-method-case-library --before old-bundle.json --after new-bundle.json --cases old-cases.json --output proposal.json
```

Each of `--before`, `--after`, `--cases`, and `--output` is required exactly
once. The only format is JSON. Choose a new output path: inputs and existing
outputs are never overwritten. Exit 0 means only that the draft was created;
parsed artifact, domain, or I/O rejection returns exit 2 with its stable JSON
error code and is not a quality result. Syntax, missing/duplicate-option, and
unknown-option errors retain inherited `argparse` usage on stderr and exit 2;
they do not read an artifact.

## What the draft contains

The fixed root envelope includes state and input digests, a nested strict v1
`proposed_case_library`, candidate deltas, case and row decisions, held gaps,
missing-vector followups, baseline audit/findings, obligation deltas,
unknowns, post-proposal audit, summary, and limitations. The nested library
has only ordinary v1 library keys: `schema_version`, after
`design_input_sha256`, `cases`, and `gaps`. Its `gaps` is empty in this slice;
proposal state, approval, and execution fields are never placed inside it.

Every source case has one case decision retaining a detached original and a
source hash; an empty case still receives that case decision. Every original
scenario occurrence has one row decision, including duplicate normalized
occurrences. Case and row review is always required where the corresponding
case or row exists. Decisions preserve applicable baseline, ambiguity,
removal, context and obligation reason codes; ambiguous possible after IDs are
listed, never guessed. A proposed scenario projects the after candidate's ID,
typed method data and requirement/source/oracle ID sets only. It preserves case
ID, title, preconditions, steps, expected prose and scenario order.

Whole-case atomicity is mandatory. A case is proposed only when all its rows
have a conformant baseline, a unique retained mapping and no unresolved model
obligation. Otherwise every row and the case are held, including otherwise
eligible rows, rather than partially migrating the case. An unresolved
obligation holds affected work. Every old explicit gap is held verbatim for
reason review; no gap is copied to the nested library or silently treated as
current. Each after-audit missing vector gets a followup with its exact
after-candidate binding and source/oracle descriptors, so new points and points
excluded by held cases remain visible. Review requirement and model business
context against the after bundle identified by its digest; the followup does
not copy complete requirement records or model metadata.

Formal retention is not semantic equivalence. Context or binding changes still
need human review, and neither the strict projection nor copied prose proves
that a case is correct, executable, approved, or executed.

## Packaged teaching example

The existing files are the complete teaching set; do not create a duplicate:

```text
qa_master/skills/codex/examples/design-methods.json
qa_master/skills/codex/examples/design-methods-after.json
qa_master/skills/codex/examples/method-cases.json
```

From a source checkout:

```text
python -m qa_master propose-method-case-library --before qa_master/skills/codex/examples/design-methods.json --after qa_master/skills/codex/examples/design-methods-after.json --cases qa_master/skills/codex/examples/method-cases.json --output .qa-master/case-library-proposal.json
```

From an installed Skill, the same bundled assets are relative to the resolved
Skill directory:

```text
python -I "<skill>/scripts/qa.py" propose-method-case-library --before "<skill>/examples/design-methods.json" --after "<skill>/examples/design-methods-after.json" --cases "<skill>/examples/method-cases.json" --output proposal.json
```

The before library represents nine of ten candidates and records no gap. This
example therefore produces nine proposed cases and one missing-vector followup.
That finding is instructional only; it is not an executed defect, approval, or
permission to skip regression.

## Limits and retry boundary

Inputs use the existing strict local JSON, depth, replay, case and row/gap
limits. The generated compact UTF-8 JSON plus newline is at most 5 MiB;
otherwise the command rejects with `OUTPUT_TOO_LARGE` before publication. It
does not read locators, invoke a model or subprocess, mutate inputs, or write
outside the requested output.

The proposal repeats original case prose and declared descriptors, so it has
the same confidentiality sensitivity as its inputs. Keep real credentials out
of shared artifacts. The command has no automatic arbitrary-prose credential
detector or redactor; normal CLI stdout and artifact/domain/I/O errors do not
echo artifact prose or input values.

For malformed artifacts, correct the declared JSON and retry with a new output
path. `OUTPUT_IO_ERROR` covers output preparation, writing, or cleanup. If
cleanup fails after atomic publication, the requested output may already exist:
inspect it before retrying. Do not assume silent rollback or success.
