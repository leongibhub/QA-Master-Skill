# Initial CI fixture failure

Frozen product source: `ddb2fc2665b2b6f044eba9bf56a70de69211db7e`.
GitHub Actions run: `40079455590`.

Ubuntu Python 3.10 job `120829761677` and Ubuntu Python 3.12 job
`120829761824` each reported 910 tests, 1 failure, 0 errors, 12 skips.
The failure was in `test_tc_prop_010_strict_parse_limits_io_and_cli_contract`:
an existing output leaf symlink returned `OUTPUT_EXISTS`, while the fixture
expected `LINK_PATH_REJECTED`. The protected target remained unchanged.

The test now expects the existing-output collision code and separately asserts
that a symlinked input returns `LINK_PATH_REJECTED`. No product or protected-core
change was required. These failed results remain failed; a fresh CI run is needed
to validate the corrected fixture across the matrix. The frozen installed-package
evidence remains attributed to the product source above.
