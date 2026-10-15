# TASK-042 independent fixture portability correction

Document State: DRAFT. Evidence Status: OBSERVED. This supplements, without rewriting, the prior independent report and CI failure.

GitHub Actions run `38717537656` at remote `7913fd6` failed on Ubuntu Python 3.10 and 3.12; Windows Python 3.10 and 3.12 passed. Direct job-log readback found the same outcome on both Ubuntu jobs: 595 tests, 5 failures, 26 errors, 1 skip (3.10: 20.018 seconds; 3.12: 19.910 seconds).

All 26 error records and four of five failure records directly contain `LINK_FORBIDDEN` from executable preflight. The fifth is the public CLI assertion expecting exit 0 but receiving 2 through the same fixture/preflight path. No separate failure cause was found in those job traces. Original Ubuntu 3.12 evidence is retained in `evidence/cr011-independent/ci-38717537656-ubuntu312-failure.txt`.

The test fixture supplied `sys.executable`, which is a symbolic link in the Ubuntu toolcache. Product policy correctly rejects executable links. The fixture now resolves the Python executable once with `Path(sys.executable).resolve(strict=True)` and consistently uses that regular-file target for manifest path, exact-byte hash, and local native Python child invocation. Product source, product `no_links`, test assertions, and expected outcomes are unchanged.

Local correction verification on Windows:

```text
python -W error::ResourceWarning -m unittest tests.test_paired_runtime_independent -v
Ran 25 tests in 36.308s
OK (skipped=1)
```

The skip remains inability to create a Windows symlink fixture. Log: `evidence/cr011-independent/portability-focused.txt`. Corrected test-source SHA-256: `35ff1d97df1c7893e42c07b703d710eb928bc3668f2306899c113ebf8017b502`.

Linux rerun after publication is still PENDING; Windows success is not presented as Linux verification. No model call, pilot, rating, comparison, release or Gate decision is made. Root independently reviewed the diff before publication.
