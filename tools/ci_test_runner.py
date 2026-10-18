"""CI runner: run unittest and emit GitHub Actions ``::error::`` annotations.

Runs the full suite with ResourceWarning promoted to error (matching the strict
CI command) so any failing or erroring test surfaces as a machine-readable
annotation that is visible in the Actions UI and via the checks API.
"""
import sys
import unittest
import warnings
from pathlib import Path

warnings.simplefilter("error", ResourceWarning)

ROOT = Path(__file__).resolve().parent.parent
suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
result = unittest.TextTestRunner(verbosity=1).run(suite)

for test, tb in result.failures + result.errors:
    tail = tb.strip().splitlines()[-1] if tb.strip() else "(no traceback)"
    print(f"::error::{test.id()}: {tail}")

print(
    f"::notice::ran={result.testsRun} failures={len(result.failures)} "
    f"errors={len(result.errors)} skipped={len(result.skipped)}"
)
sys.exit(0 if result.wasSuccessful() else 1)
