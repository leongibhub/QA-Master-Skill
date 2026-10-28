# CR-037 strict default rubric and baseline findings

Frozen source: `d4cdfcc`.
Evidence status: `OBSERVED` for contract/source read; fresh probe status:
`NOT_EXECUTED`.

- Old `after-output.md` line 21 has a preparation action without its own expected
  result: FAIL STRICT-WRITE-01.
- Old `login-explicit-output.md` lines 9–10 expose unsolicited `source_role`,
  `direct_input`, `Trace` and a synthesized trace ID: FAIL STRICT-WRITE-02.

The older samples retain their previous-rubric PASS results. These are new strict
criteria only, not factual, runtime, business-execution, or defect findings.
