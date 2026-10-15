# Test harness correction

focused-first.txt preserves 7 passing tests and one new TC-IMD013 failure: an assertion required literal `case_count` wording in installed reference. DES055/BUG014 did not require that spelling, so this was an over-specific tester assertion, not a product defect. Removed only that token check; behavioral generic case counts remain asserted for tester-owned input and installed example. Focused retest: 8 PASS. Fresh wheel: 8 PASS. No product edits or original log replacement.
