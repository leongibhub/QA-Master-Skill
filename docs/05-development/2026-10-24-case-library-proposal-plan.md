# Case Library Proposal Implementation Plan

> Execute through separate developer, independent tester and reviewer owners;
> use subagent-driven-development for the scoped implementation/review loop.

**Goal:** prepare a reviewable after-version case library without applying it.
**Architecture:** additive pure JSON overlay; impact + after replay + post-audit,
indexed exact matching, case atomicity, held gaps and mandatory review.
**Tech Stack:** Python3.10+, stdlib/unittest; Windows and Linux.
**Spec:** DES-064 / DOC-CASE-LIBRARY-PROPOSAL-REQ-001; CR-036.

## Global constraints

Input5MiB/depth32; existing replay budget10000; cases10000; rows+gaps50000.
Exact compact output+newline <=5MiB. No source/network/model/subprocess/state/
external operation in feature. Existing core modules unchanged. Always draft,
nonexecuted, nonapplied; no apply or arbitrary-report rendering API.

## TASK-147 — orchestrator scope/design/traceability

- [x] Read current Git/history, instructions, lifecycle and existing contracts.
- [x] Obtain read-only requirement/architecture options and choose fixed DES-064.
- [x] Record CR/RTM and actual assignments; commit design before implementation.

Actual owners: TASK-147 /root; TASK-148 developer /root/rebind_developer;
TASK-149 documentation_manager /root/rebind_docs; TASK-150 tester
/root/rebind_tester; TASK-151 reviewer /root/rebind_reviewer. Requirements and
architecture investigations /root/rebind_requirements and /root/rebind_architecture
were read-only advisory inputs, not implementation or acceptance evidence.
Runtime registration NOT_AVAILABLE; no lease/Gate result is invented.

## TASK-148 — developer module/CLI/unit regressions

Own qa_master/case_library_proposal.py, additive qa_master/__main__.py and
tests/test_case_library_proposal.py. Do not touch existing audit/impact/engine.

- [x] Write/run RED teaching example before implementation; retain actual output.
- [x] Implement exact schemas/indexes, eligibility, whole-case holds, gap holds,
  review-reason union, exact followups and after-audit/count/hash invariants.
- [x] Add safe JSON-only CLI and bounded serializer/error adapter; duplicate flags,
  stdout privacy/no campaign loading; existing file helper behavior preserved.
- [x] Run developer and relevant old regression checks; no local full discovery.

## TASK-149 — bundled chat guidance

Own concise README addition, both Skill entries, new bundled
references/case-library-proposal.md. Reuse existing before/after/library example;
no redundant example files or install/catalogue churn.

- [x] Explain ordinary chat use and Agent-prepared structured inputs.
- [x] Show real source/installed paths; teaching example9 proposed,1 missing.
- [x] Explain nested strict library, mandatory review, held cases/gaps and no
  apply/execution; output-size and post-publication cleanup boundaries.

## TASK-150 — independent QA and installed delivery

Own tests/test_case_library_proposal_independent.py and its verification/evidence.

- [x] Independently author TC-PROP-001–011 plus adversarial variants, preserving
  RED/fix history; verify schema, cases/rows/gaps accounting, types and no mutation.
- [x] Test context changes, model obligations, all baseline faults/empty cases,
  partial-case deletion/ambiguity,2old1new, orphan/duplicate gaps, exact missing
  contexts, order/occurrences, strict parser/limits/I/O/error values.
- [x] On final frozen SHA build one clean archive/wheel, offline consumer install,
  module CLI and installed helper; same fixture, recorded subprocess bytes/exits.
  Run via exec session and poll SAME returned session; no detached second writer.
  Save exit after fixture cleanup. Independent evidence directory per attempt.
- [x] Preserve permissions skips and raw logs; root runs full cross-platform CI.

## TASK-151 — independent source/contract/evidence review

Own the independent review report only; read-only product access.

- [x] Preflight fixed contract before developer source freeze.
- [x] Review exact eligibility/whole-case atomicity/held work; no fabricated
  prose/gap reasons, arbitrary mapping, approval or hidden application path.
- [x] Verify typed projection, provenance, invariants, limits/I/O, package evidence
  and claim boundaries. Batch findings, repair, retest and re-review before merge.

## Delivery

- [x] Persist actual evidence/RTM/change/work records; all project Gates unchanged.
- [ ] Push PR to existing repository; inspect final-source CI; merge and read back.
- [x] Explain chat invocation and first-slice limits to the user (Agent-prepared inputs, mandatory review, whole-case holds).


## Observed implementation and verification

Product freeze ddb2fc2 implements TASK-148/149. TASK-150 completed one frozen
archive/wheel installed attempt (session66660, exit0,11/11); full command
identities/hashes are in EVD-CR036-DELIVERY-001 and its independent record.
TASK-151 final evidence review recorded in the independent review report. Prototype BUG-027–031 repaired before freeze. Later83afa58 changes
only an independent symlink assertion and adds a separate input-link check;
local11/11PASS. Initial CI40079455590 failed fixture retained; fresh
CI40080022358 all4PASS (910 tests each, no failures/errors, skips retained).
The merge checklist remains open at this premerge snapshot; the actual receipt
follows Git/PR history and final user readback.
