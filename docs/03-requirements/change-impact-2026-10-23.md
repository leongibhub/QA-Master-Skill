# CR-034: finite-model change impact and case review proposals

- Artifact: DOC-METHOD-IMPACT-REQ-001
- Document State: DRAFT; Evaluation State: IN_REVIEW.
- Source: the user's existing improvement request, CR-033's deferred change-impact
  roadmap, and the user's instruction to continue on 2026-10-23.
- Engineering scope is authorized by continuation. Detailed requirements remain
  orchestrator-authored DRAFT; no human baseline, Gate or acceptance is implied.
- Baseline: GitHub main 90a9226.

## User outcome

When requirements/design models change, the Agent compares the saved old bundle,
new bundle and old case library. The user receives existing cases needing review,
added/removed finite scenarios, declared evidence changes and unresolved gaps.
The Agent prepares the JSON artifacts; the QA user continues to work in chat.

| ID | Requirement | Acceptance |
| --- | --- | --- |
| REQ-032 | Compare old/new finite candidates without relying on whole-model-hashed candidate IDs. | Replay both designs. Pair only identical typed formal vectors within the same model ID: method, dimension and method_data. A source-digest-only change retains vector pairs despite changed candidate IDs. Changed finite data produces removed/added vectors; model rename never auto-pairs. Ambiguous groups retain all IDs and require review. |
| REQ-033 | Produce actionable row/case review proposals. | Each existing scenario row has one action with case ID, canonical row digest and one-based occurrence. Selected case IDs are the sorted union of rows/cases needing review. Stale baseline-library digest rejects; nonconformant baseline rows and orphan/undocumented cases remain visible. No case is edited/deleted and no proposal authorizes execution or skipping tests. |
| REQ-034 | Separate formal vector identity from oracle/requirement/source context. | Same vector with changed oracle refs/descriptors, requirement bindings/records, source refs/descriptors or model metadata requires review, not a business-semantics equivalence claim. Include old/new candidate IDs and controlled reasons. Declared metadata/digests only: external source bytes are not opened. |
| REQ-035 | Preserve obligations, gaps and unmapped requirement changes. | Reconcile old/new engine obligations as PRESENT_BOTH, AFTER_ONLY, BEFORE_ONLY or AMBIGUOUS. BEFORE_ONLY never means resolved. Preserve old explicit gap followups and baseline audit findings. Changed requirements outside all finite models are explicit unknowns. New vectors request a case or declared gap. |
| REQ-036 | Deliver offline JSON/Markdown analysis through the installed Skill. | Add impact-method-cases --before --after --cases --output [--format json|markdown]. Output includes both design digests, normalized case-library identity, actionable proposals and reconciled counts; fresh wheel and installed helper work from a consumer directory without campaign initialization. |
| NFR-014 | Preserve typed, bounded, non-destructive analysis. | Standard library only; CR-033 5 MiB-per-input/depth-32/10,000-candidates-per-design/50,000-row limits. Reject duplicate keys, nonfinite values, duplicate flags, linked/reparse input ancestors and existing/colliding output. No network, model, subprocess, campaign mutation or external writes in the feature. All reports DRAFT_UNAPPROVED / NOT_EXECUTED. |

## Explicit limits

Independent review clarification: baseline MISSING/DUPLICATE/MISMATCH candidate
identities remain visible through BASELINE_NONCONFORMANT delta reasons; they are
not fabricated authored gaps. Preserve each actual gap occurrence and all
concurrent review reasons even when one action takes precedence.

An exact formal-vector pair establishes neither unchanged requirement meaning nor
correct prose/oracles. Changed oracle/requirement bindings are not inferred
renames. NO_DECLARED_IMPACT means only that this finite-model comparison found no
declared change; it never means safe to skip regression. Code-only changes and
external byte changes without refreshed descriptors are outside this analysis.
No same-model Awesome quality comparison is performed by this increment.

## Test model

TC-IMPACT-001: unchanged input; TC-IMPACT-002: source-only ID churn;
TC-IMPACT-003: typed value/bool/decimal change; TC-IMPACT-004: oracle/requirement
context; TC-IMPACT-005: model rename/add/remove; TC-IMPACT-006: stale/nonconformant
baseline and duplicate rows; TC-IMPACT-007: obligation/gap/unmodeled changes;
TC-IMPACT-008: deterministic ordering and row identity; TC-IMPACT-009: strict
parsing/limits/no-clobber/reparse; TC-IMPACT-010: isolated wheel/helper delivery.
Independent tests are authored by a distinct tester; review is a third identity.
