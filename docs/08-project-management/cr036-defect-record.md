# CR-036 prototype review and repair record

Document State:DRAFT; Evidence Status:OBSERVED. These findings concern the
unreleased TASK-148 working prototype after fb5e4be, before its first product
freeze. No immutable pre-repair product commit is claimed. Reviewer public
reproductions, static source review and developer regressions are retained in
the separate TASK-151 report; all fixes precede final installed verification.

| ID | Severity | Observed issue / root cause | Repair and bounded disposition |
| --- | --- | --- | --- |
| BUG-027 | P2 | Missing-vector followups inherited held-row reasons but lost the full case's causal reasons; removing one model from a shared case omitted FINITE_VECTOR_REMOVED on a retained point held by whole-case atomicity. | Index and union held-row AND matching case-decision reasons; independently reproduced and retested. |
| BUG-028 | P2 | Otherwise uncaught writer RuntimeError/OSError could escape with raw path text instead of OUTPUT_IO_ERROR. | File-wrapper error boundary preserves own/known domain errors and maps raw I/O/runtime errors value-free; injected failure regression passes. |
| BUG-029 | P2 | Per-row full finding scans and per-missing-vector full held-row/gap scans violated the indexed-work contract. | Preindex finding codes and held-source reasons by case/candidate/after ID; no quadratic repeated global scans remain in reviewed paths. |
| BUG-030 | P2 | Defense gap: an injected inconsistent fresh impact action was accepted; post-audit/source-row/count/hash guards were incomplete. This was not a normal-input upstream failure. | Validate unique mapping/formal identity, post candidate set/list/count/hash and source/locator/decision accounting; targeted injected-inconsistency regressions pass. |
| BUG-031 | P3 | Held gaps were initially built in canonical projection order but then reordered by SHA digest, contradicting DES-064. | Keep canonical gap order and duplicate occurrence numbering; eight-gap regression checks canonical versus digest ordering. |

Source checks before freeze: developer9 + independent11 + old audit13/impact10
=43 tests PASS (installed branch still freeze-gated). Existing three protected
core modules retain their baseline content. Final source/package/CI identities
and verdicts are recorded only after observation in the delivery/test/review
reports. No external defect closure, human acceptance, Gate or release follows.

Preimplementation schema/reason/order/privacy ambiguities and the inherited
argparse syntax-error ruling are design decisions in DES-064, not fabricated
executed defects. The preliminary uninstalled `python -I -m qa_master` consumer
test failure was a test-environment mistake, retained as harness history and
corrected before the installed fixture; no product fix was attributed to it.
