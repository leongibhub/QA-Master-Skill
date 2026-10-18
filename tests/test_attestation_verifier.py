"""Developer verification for TASK-077 (DES-061 attestation verifier).

All signatures and keys here are synthetic test doubles. Nothing in this file
is provider evidence or pilot evidence of any kind.
"""
import json
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from qa_master import paired_evaluation as pe
from qa_master._paired_contract import canonical, digest, PairedEvaluationError

from tests.test_paired_evaluation import fixture, capture


# Retained run roots from the CR-011 verification exercise. These live under
# the git-ignored `.qa-master/` working directory and are absent in a clean
# checkout, so the retained-roots check skips when they are not present.
RETAINED_ROOTS = [
    Path(__file__).resolve().parents[1] / '.qa-master/paired-pilot/observed-v4-final-freeze/CR011-EXPLORATORY-PUBLIC-DEV-001',
    Path(__file__).resolve().parents[1] / '.qa-master/cr011-independent/preview',
    Path(__file__).resolve().parents[1] / '.qa-master/cr011-independent/final-installed/preview',
    Path(__file__).resolve().parents[1] / '.qa-master/cr011-independent/repaired-installed/preview',
]


def registry_for(root, keys):
    """Write a trust registry naming each (issuer, subject) with a hex key."""
    issuers = []
    for issuer_id, subject, public_hex in keys:
        issuers.append({'issuer_id': issuer_id, 'subject': subject,
                        'algorithm': 'ED25519', 'public_key_multibase': public_hex})
    registry = {'schema_version': 1, 'registry_id': 'REG-TEST-001',
                'created_at_utc': '2026-10-16T00:00:00Z', 'issuers': issuers}
    path = root/'registry.json'
    path.write_bytes(canonical(registry))
    return path


def attestations_for(root, issuer_key, manifest_created='2026-10-15T00:00:00Z'):
    """Write four provider-signed attestation document/sig pairs."""
    directory = root/'attestations'
    directory.mkdir(exist_ok=True)
    for arm in ('A', 'B'):
        for subject in pe.ATTESTATION_SUBJECTS:
            document = {'schema_version': 1, 'subject': subject, 'arm_id': arm,
                        'value': subject + '-value',
                        'observed_at_utc': '2026-10-14T00:00:00Z',
                        'issuer_id': 'ISSUER-TEST-001',
                        'statement': 'Synthetic test attestation.'}
            raw = canonical(document)
            signature = issuer_key.sign(raw)
            (directory/(subject + '-' + arm + '.json')).write_bytes(raw)
            (directory/(subject + '-' + arm + '.sig')).write_bytes(signature)
    return directory


class AttestationVerifierDeveloperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path, self.excluded, self.manifest = fixture(self.root)
        self.issuer = Ed25519PrivateKey.generate()
        self.public_hex = self.issuer.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
        self.registry = registry_for(self.root, [
            ('ISSUER-TEST-001', 'provider_revision', self.public_hex),
            ('ISSUER-TEST-001', 'system_baseline', self.public_hex),
        ])
        self.attestations = attestations_for(self.root, self.issuer)
        self.manifest['profile'] = pe.STRICT_PROFILE
        # Strict candidates need both orders across at least two rows.
        self.manifest['schedule'][1]['order'] = ['B', 'A']
        self.manifest['schedule'][2]['order'] = ['B', 'A']
        self.path.write_bytes(canonical(self.manifest))

    def run_strict_fake(self):
        return pe._run_pair_with_ports(self.path, self.excluded, self.root/'output',
                                       launcher=capture,
                                       trust_registry_path=self.registry,
                                       evidence_dir=self.attestations)

    def code_of(self, call):
        try:
            call()
        except PairedEvaluationError as exc:
            return exc.code
        raise AssertionError('expected PairedEvaluationError')

    # TC-SV-1: registry validation

    def test_registry_invalid_grammar(self):
        bad = json.loads(self.registry.read_text())
        bad['issuers'][0]['algorithm'] = 'RSA'
        self.registry.write_bytes(canonical(bad))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'TRUST_REGISTRY_INVALID')

    def test_registry_secret_pattern_rejected(self):
        bad = json.loads(self.registry.read_text())
        bad['issuers'][0]['public_key_multibase'] = 'password=secret-value'
        self.registry.write_bytes(canonical(bad))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'TRUST_REGISTRY_INVALID')

    # TC-SV-4: preflight fail-closed combinations

    def test_strict_without_registry_fails(self):
        self.manifest['profile'] = pe.STRICT_PROFILE
        self.path.write_bytes(canonical(self.manifest))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent))
        self.assertEqual(code, 'STRICT_PROFILE_NOT_SUPPORTED')

    def test_exploratory_with_registry_fails(self):
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'STRICT_PROFILE_MISMATCH')

    def test_declared_verified_without_verifier_fails(self):
        self.manifest['runtime']['model']['provider_revision'] = {
            'state': 'VERIFIED', 'value': 'x', 'evidence_sha256': '4'*64}
        self.path.write_bytes(canonical(self.manifest))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'ATTESTATION_NOT_SUPPORTED')

    # TC-SV-7: DES-061 v2 NR-1 equality clause

    def test_differing_arm_values_fail(self):
        # Re-sign arm B provider_revision with a different value.
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        document = json.loads((self.attestations/'provider_revision-B.json').read_text())
        document['value'] = 'different-revision-for-B'
        raw = canonical(document)
        (self.attestations/'provider_revision-B.json').write_bytes(raw)
        (self.attestations/'provider_revision-B.sig').write_bytes(self.issuer.sign(raw))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'STRICT_ATTESTATION_VALUE_MISMATCH')

    def test_declared_value_mismatch_fails(self):
        self.manifest['runtime']['model']['provider_revision'] = {
            'state': 'UNVERIFIED', 'value': 'declared-other-revision', 'evidence_sha256': None}
        self.path.write_bytes(canonical(self.manifest))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'STRICT_ATTESTATION_VALUE_MISMATCH')

    def test_declared_value_matching_passes(self):
        value = json.loads((self.attestations/'provider_revision-A.json').read_text())['value']
        self.manifest['runtime']['model']['provider_revision'] = {
            'state': 'UNVERIFIED', 'value': value, 'evidence_sha256': None}
        self.path.write_bytes(canonical(self.manifest))
        outcome = pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations)
        self.assertEqual(outcome['status'], 'VALIDATED_NOT_EXECUTED')

    def test_strict_single_order_schedule_fails(self):
        self.manifest['schedule'][1]['order'] = ['A', 'B']
        self.manifest['schedule'][2]['order'] = ['A', 'B']
        self.path.write_bytes(canonical(self.manifest))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'INVALID_SCHEDULE')

    def test_missing_attestation_fails(self):
        (self.attestations/'provider_revision-A.json').unlink()
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'ATTESTATION_MISSING')

    def test_tampered_document_fails(self):
        document = json.loads((self.attestations/'provider_revision-A.json').read_text())
        document['value'] = 'tampered'
        (self.attestations/'provider_revision-A.json').write_bytes(canonical(document))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'ATTESTATION_SIGNATURE_INVALID')

    def test_wrong_key_fails(self):
        other = Ed25519PrivateKey.generate()
        self.attestations = attestations_for(self.root, other)
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'ATTESTATION_SIGNATURE_INVALID')

    def test_unknown_issuer_fails(self):
        registry = registry_for(self.root, [
            ('ISSUER-OTHER-001', 'provider_revision', self.public_hex),
            ('ISSUER-OTHER-001', 'system_baseline', self.public_hex),
        ])
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'ATTESTATION_ISSUER_UNKNOWN')

    def test_future_attestation_fails(self):
        document = json.loads((self.attestations/'provider_revision-A.json').read_text())
        document['observed_at_utc'] = '2027-01-01T00:00:00Z'
        raw = canonical(document)
        (self.attestations/'provider_revision-A.json').write_bytes(raw)
        (self.attestations/'provider_revision-A.sig').write_bytes(self.issuer.sign(raw))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'ATTESTATION_TIME_INVALID')

    def test_subject_filename_mismatch_fails(self):
        document = json.loads((self.attestations/'provider_revision-A.json').read_text())
        document['subject'] = 'system_baseline'
        raw = canonical(document)
        (self.attestations/'provider_revision-A.json').write_bytes(raw)
        (self.attestations/'provider_revision-A.sig').write_bytes(self.issuer.sign(raw))
        code = self.code_of(lambda: pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations))
        self.assertEqual(code, 'ATTESTATION_INVALID')

    def test_registry_drift_fails_run(self):
        # A registry that changes between preflight and the first call stops
        # the run; existing attempts record the drift as infrastructure failure.
        def launch(**kwargs):
            bad = json.loads(self.registry.read_text())
            bad['issuers'][0]['issuer_id'] = 'ISSUER-TEST-002'
            self.registry.write_bytes(canonical(bad))
            return capture(**kwargs)
        result = pe._run_pair_with_ports(self.path, self.excluded, self.root/'output', launcher=launch,
                                         trust_registry_path=self.registry, evidence_dir=self.attestations)
        stopped = [row for row in result['attempts'] if row['terminal_status'] == 'INFRASTRUCTURE_FAILURE']
        self.assertTrue(stopped)
        self.assertTrue(all(row['infrastructure_error'] == 'TRUST_REGISTRY_DRIFT' for row in stopped))
        # Once the registry drifted, no later call may proceed.
        self.assertTrue(all(row['process_outcome'] in ('NOT_STARTED', 'EXITED_ZERO') for row in result['attempts']))
        self.assertEqual(result['evidence_class'], 'TEST_DOUBLE')

    # TC-SV-5: run-result derivation

    def test_strict_run_derives_verdicts_and_test_double_boundary(self):
        result = self.run_strict_fake()
        # TEST_DOUBLE backend can never claim strict evidence class.
        self.assertEqual(result['execution_backend'], 'TEST_DOUBLE')
        self.assertEqual(result['evidence_class'], 'TEST_DOUBLE')
        self.assertEqual(len(result['attestation_verdicts']), 4)
        self.assertEqual(result['strict_eligibility'], 'HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY')
        # R-01 repair: a TEST_DOUBLE run records verdicts but presents no
        # promoted model record.
        self.assertNotIn('model', result)
        self.assertEqual(result['claim_status'], 'NOT_ASSERTED')
        self.assertEqual(result['human_rating_status'], 'NOT_EXECUTED')
        # Manifest-declared UNVERIFIED records are preserved in runtime.
        self.assertEqual(result['runtime']['model']['provider_revision']['state'], 'NOT_AVAILABLE')

    def test_strict_test_double_root_passes_own_inspect(self):
        # R-01 repair regression: the written run root of a strict TEST_DOUBLE
        # run must pass inspect_run (it previously failed INVALID_RESULT).
        result = self.run_strict_fake()
        run_root = self.root/'output'/self.manifest['run_id']
        outcome = pe.inspect_run(run_root)
        self.assertEqual(outcome['status'], 'INTACT')
        # The written result still records TEST_DOUBLE evidence class.
        from qa_master._paired_contract import strict_json
        written = strict_json((run_root/'result.json').read_bytes())
        self.assertEqual(written['evidence_class'], 'TEST_DOUBLE')
        self.assertNotIn('model', written)

    @unittest.skipUnless(all((p/'preflight.json').is_file() for p in RETAINED_ROOTS),
                         'retained roots absent in clean checkout')
    def test_historical_preflight_without_registry_member_inspects(self):
        # R-02 repair regression: retained pre-CR-015 run roots (no
        # trust_registry_sha256 member) must remain inspectable. The retained
        # TASK-044 pilot root is the authoritative instance; a missing member
        # in a ledger-listed file cannot be simulated without breaking the
        # ledger digest, so this checks the real retained roots.
        existing = [path for path in RETAINED_ROOTS if (path/'preflight.json').is_file()]
        self.assertTrue(existing, 'retained run roots must exist in the repository checkout')
        for run_root in existing:
            preflight = json.loads((run_root/'preflight.json').read_bytes())
            self.assertNotIn('trust_registry_sha256', preflight)
            outcome = pe.inspect_run(run_root)
            self.assertEqual(outcome['status'], 'INTACT', run_root)

    def test_strict_validate_passes_with_all_verdicts(self):
        outcome = pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations)
        self.assertEqual(outcome['status'], 'VALIDATED_NOT_EXECUTED')
        self.assertEqual(outcome['claim_status'], 'NOT_ASSERTED')

    # TC-SV-6: exploratory path unchanged

    def test_exploratory_validate_unchanged_without_flags(self):
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        outcome = pe.validate_run_manifest(self.path.read_bytes(), manifest_dir=self.path.parent)
        self.assertEqual(outcome['status'], 'VALIDATED_NOT_EXECUTED')
        result = pe._run_pair_with_ports(self.path, self.excluded, self.root/'output2', launcher=capture)
        self.assertNotIn('attestation_verdicts', result)
        self.assertNotIn('strict_eligibility', result)
        self.assertEqual(result['evidence_class'], 'TEST_DOUBLE')

    def test_cli_flags_wired_and_exploratory_default_unchanged(self):
        import subprocess
        import sys as _sys
        # Default CLI: exploratory manifest validates without new flags.
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        done = subprocess.run([_sys.executable, '-m', 'qa_master.paired_evaluation', 'validate', str(self.path)],
                              capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[1]))
        self.assertEqual(done.returncode, 0)
        self.assertIn('VALIDATED_NOT_EXECUTED', done.stdout)
        # CLI with registry on an exploratory manifest fails with the mismatch code.
        done = subprocess.run([_sys.executable, '-m', 'qa_master.paired_evaluation', 'validate', str(self.path),
                               '--trust-registry', str(self.registry), '--attestations', str(self.attestations)],
                              capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[1]))
        self.assertEqual(done.returncode, 2)
        self.assertIn('STRICT_PROFILE_MISMATCH', done.stdout)
        # CLI strict without registry fails with the fail-closed code.
        self.manifest['profile'] = pe.STRICT_PROFILE
        self.path.write_bytes(canonical(self.manifest))
        done = subprocess.run([_sys.executable, '-m', 'qa_master.paired_evaluation', 'validate', str(self.path)],
                              capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[1]))
        self.assertEqual(done.returncode, 2)
        self.assertIn('STRICT_PROFILE_NOT_SUPPORTED', done.stdout)
        # CLI strict with registry and attestations validates.
        done = subprocess.run([_sys.executable, '-m', 'qa_master.paired_evaluation', 'validate', str(self.path),
                               '--trust-registry', str(self.registry), '--attestations', str(self.attestations)],
                              capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[1]))
        self.assertEqual(done.returncode, 0)
        self.assertIn('VALIDATED_NOT_EXECUTED', done.stdout)


if __name__ == '__main__':
    unittest.main()
