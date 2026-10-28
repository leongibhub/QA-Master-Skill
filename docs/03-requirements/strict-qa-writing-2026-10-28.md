# CR-037 follow-up — strict human-facing case and bug writing

Document State: DRAFT. User explicitly requests tightening the two findings from
the login-writing audit at `477ffe4`; product baseline is main `aaf8b1c`.
This clarifies REQ-041/042 and DES-065 without changing runtime/schema/permissions.

## Fixed acceptance before instruction changes

1. Default human-facing cases use a step / operation / expected-result table,
   or preserve an explicitly required project format with the same one-to-one
   mapping. Every numbered action, including preparation, has its own expected
   result. Unknown expectations say exactly what is pending for that step; no
   invented input echo, password masking, message, threshold or side effect.
2. Ordinary case/bug prose does not expose unsolicited machine field names,
   `source_role`, `direct_input`, `Trace` labels or synthesized trace IDs. Preserve
   supplied real IDs, exact technical commands/values and human source references.
   If an explicit user/project/import schema requires raw fields, preserve them
   exactly in a separate machine payload/support block; do not drop/rename them.
3. Bug drafts lead with symptom, setup, reproduction steps, actual result and
   expected result in clear separate parts. Supplied observations retain source
   attribution; missing evidence and unknown severity/root causes remain pending.
4. Keep the user's language and requested scope. This is authoring guidance,
   not authority to execute a business test, submit a bug or modify old cases.

## Tasks and independent checks

- TASK-157: `/root/rebind_docs` owns first-party entry/reference/professional
  instruction changes and a concise README update; `/root` owns traceability,
  managed propagation and Git publication.
- TASK-158: `/root/rebind_tester` independently checks baseline findings, final
  fresh outputs, required-field preservation and installed source/manifest parity.
- TASK-159: `/root/rebind_reviewer` independently reviews wording, exceptions,
  evidence integrity and compatibility.

Baseline RED evidence is retained: the prior explicit author exposed unsolicited
machine fields; source reference line 39 explicitly allowed unpaired preparation
actions. Prior samples that passed the older rubric remain PASS on that rubric.
Use fresh ordinary login, unknown-preparation-expectation and explicit-machine-
schema probes; do not force a fake failing baseline or claim universal model
reliability from samples. Existing relevant instruction/catalogue/doc checks run
after editing. Final propagation uses uv `--reinstall`, the managed installer
with backup, and independently checked file hashes.

Actual host owners are not Runtime leases. All project Gates remain unchanged;
human acceptance and business execution remain NOT_AVAILABLE/NOT_EXECUTED.
Company bug-format guidance was consulted read-only; internal contents/URLs are
not copied into public instructions or examples.
