# TASK064 independent semantic evaluator link/reparse verification

Runtime work-6aa14f5e11514574b8f8e5ff34fe7733 attempt1/version1. Product subject a9df28513d4ae808d687718bfc4f6069a32ee767, documentation HEAD at start a216475. Evaluator SHA D567D26110EACA5637F54C0DC48994E881BFEDCE69EAFD0C8AA809C41331018A. Scope is DES060 input/output/inspect parent-path link rejection only. No product edits or full local suite run.

## Windows actual execution

`python -W error::ResourceWarning -m unittest discover -s tests -p test_semantic_quality_links_independent.py -v` ran10tests in1.193s:5PASS and5skip. These are new product-specific independent tests, not existing skips from unrelated modules.

Five genuine Windows junctions were created with mklink /J and verified with the FILE_ATTRIBUTE_REPARSE_POINT bit. Each scenario tests a parent link: bundle input directory, referenced source directory, response directory, output directory, and retained inspect directory. Input paths exercise both validate and evaluate; output exercises evaluate; inspect exercises inspect_result. Every invoked path returns LINK_FORBIDDEN. Source/response bytes, unrelated sentinel, and published result bytes remain unchanged; no rejected output child is created. Link cleanup removes only the verified temporary link and never traverses target deletion.

Five real directory-symlink attempts received Windows error1314. They are NOT_EXECUTED/skipped, not PASS. Junction success does not stand in for symlink execution. Test fixtures do not mock links or error results.

## Linux actual CI readback

Tester independently fetched decoded GitHub Actions job logs and job metadata for run38739167991 after publication. Both Ubuntu jobs execute all five semantic evaluator symlink scenarios successfully, and skip five Windows-only junction scenarios as NOT_APPLICABLE. Each full suite has699tests/6skips; the sixth is the unrelated installer Windows-junction test. Ubuntu3.10 job116436073554:33.131s, success. Ubuntu3.12 job116436074129:46.754s, success.

Logs identify checkout merge53ceda1 of remote66ae928c70b94830ccbbfe1e5f2ebd47776bca85 into77e3b5d4e8be8076720ebfd2f0338db73dac2079. Root reports local40908ea is tree-equivalent to remote66ae928 (tree96fb9674e6e0e921a17626127348a62b7157019e); that equivalence is root-attributed, while tester independently read actual job/test execution. Required decoded excerpts are retained in the evidence directory.

[Ubuntu3.10 job](https://github.com/leongibhub/QA-Master-Skill/actions/runs/38739167991/job/116436073554) and [Ubuntu3.12 job](https://github.com/leongibhub/QA-Master-Skill/actions/runs/38739167991/job/116436074129). Windows CI subsequently completed and was independently read back as described below. Local Windows symlink skips remain NOT_EXECUTED and are not rewritten as successes.

## Windows CI actual execution and bounded conclusion

Tester independently fetched both Windows decoded job logs and final jobs metadata. Windows3.10 job116436073865:699tests138.763s, OK with no skips. Windows3.12 job116436073916:699tests136.580s, OK with no skips. Each explicitly reports all five semantic junction and all five semantic symlink tests `ok`; the CI hosts permit real symlink creation, unlike the local workstation. Necessary test excerpts and final summaries are preserved separately.

[Windows3.10 job](https://github.com/leongibhub/QA-Master-Skill/actions/runs/38739167991/job/116436073865) and [Windows3.12 job](https://github.com/leongibhub/QA-Master-Skill/actions/runs/38739167991/job/116436073916). Final jobs API reports success for all four jobs in run38739167991. This is live independent readback of the new tests, not prior CI inference.

Bounded verification result: PASS for the five parent-path rejection scenarios on actual Windows junctions and permitted Windows/Linux symlinks. Local symlink execution remains NOT_EXECUTED; Linux junctions remain NOT_APPLICABLE. No source change was needed or made. Governance/reviewer owns disposition; this report does not close a defect, change a Gate or establish full product acceptance.

## Evidence and limits

Test file: tests/test_semantic_quality_links_independent.py. Raw focused log: evidence/cr013-semantic-links-independent/windows-focused.txt. The evidence directory disables text/whitespace transformations. Formatting-only final newline normalization occurred after the Windows run; assertions and operations are unchanged. Existing semantic test fixture is tester-owned; developer test fixtures/oracles are not reused. Scope excludes arbitrary Windows reparse subtypes, all crash races, model calls, enterprise writes, product test execution, Gate/acceptance/release and defect closure. Historical attempts1/2/3 and final source review are preserved.
