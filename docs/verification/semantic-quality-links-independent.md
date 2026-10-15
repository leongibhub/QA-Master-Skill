# TASK064 independent semantic evaluator link/reparse verification

Runtime work-6aa14f5e11514574b8f8e5ff34fe7733 attempt1/version1. Product subject a9df28513d4ae808d687718bfc4f6069a32ee767, documentation HEAD at start a216475. Evaluator SHA D567D26110EACA5637F54C0DC48994E881BFEDCE69EAFD0C8AA809C41331018A. Scope is DES060 input/output/inspect parent-path link rejection only. No product edits or full local suite run.

## Windows actual execution

`python -W error::ResourceWarning -m unittest discover -s tests -p test_semantic_quality_links_independent.py -v` ran10tests in1.193s:5PASS and5skip. These are new product-specific independent tests, not existing skips from unrelated modules.

Five genuine Windows junctions were created with mklink /J and verified with the FILE_ATTRIBUTE_REPARSE_POINT bit. Each scenario tests a parent link: bundle input directory, referenced source directory, response directory, output directory, and retained inspect directory. Input paths exercise both validate and evaluate; output exercises evaluate; inspect exercises inspect_result. Every invoked path returns LINK_FORBIDDEN. Source/response bytes, unrelated sentinel, and published result bytes remain unchanged; no rejected output child is created. Link cleanup removes only the verified temporary link and never traverses target deletion.

Five real directory-symlink attempts received Windows error1314. They are NOT_EXECUTED/skipped, not PASS. Junction success does not stand in for symlink execution. Test fixtures do not mock links or error results.

## Linux boundary

Linux CI actual execution/readback is PENDING until these tests are published. Linux should skip the five Windows-specific junction scenarios as NOT_APPLICABLE and execute the five actual symlink scenarios. No earlier CI run is claimed as evidence for this new test file.

## Evidence and limits

Test file: tests/test_semantic_quality_links_independent.py. Raw focused log: evidence/cr013-semantic-links-independent/windows-focused.txt. The evidence directory disables text/whitespace transformations. Formatting-only final newline normalization occurred after the Windows run; assertions and operations are unchanged. Existing semantic test fixture is tester-owned; developer test fixtures/oracles are not reused. Scope excludes arbitrary Windows reparse subtypes, all crash races, model calls, enterprise writes, product test execution, Gate/acceptance/release and defect closure. Historical attempts1/2/3 and final source review are preserved.
