"""Independent re-test of TASK-084 (NR-1 equality implementation) at 547c6e6.

Authored by the independent tester. Synthetic keys only; no provider
evidence, model call, pair run or holdout material.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from qa_master import paired_evaluation as pe
from qa_master._paired_contract import canonical, PairedEvaluationError

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from tests.test_paired_evaluation import fixture, capture  # noqa: E402


class EqualityReTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path, self.excluded, self.manifest = fixture(self.root)
        self.issuer = Ed25519PrivateKey.generate()
        self.public_hex = self.issuer.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
        self.registry = self._registry()
        self.attestations = self._attestations()
        self.manifest['profile'] = pe.STRICT_PROFILE
        self.manifest['schedule'][1]['order'] = ['B', 'A']
        self.manifest['schedule'][2]['order'] = ['B', 'A']
        self.path.write_bytes(canonical(self.manifest))

    def _registry(self):
        registry = {'schema_version': 1, 'registry_id': 'REG-EQ-001',
                    'created_at_utc': '2026-10-16T00:00:00Z',
                    'issuers': [{'issuer_id': 'ISSUER-EQ-001', 'subject': subject,
                                 'algorithm': 'ED25519', 'public_key_multibase': self.public_hex}
                                for subject in pe.ATTESTATION_SUBJECTS]}
        path = self.root/'registry-eq.json'
        path.write_bytes(canonical(registry))
        return path

    def _attestations(self, per_arm_values=None):
        per_arm_values = per_arm_values or {}
        directory = self.root/'attestations-eq'
        directory.mkdir(exist_ok=True)
        for arm in ('A', 'B'):
            for subject in pe.ATTESTATION_SUBJECTS:
                value = per_arm_values.get((arm, subject), subject + '/shared')
                document = {'schema_version': 1, 'subject': subject, 'arm_id': arm,
                            'value': value, 'observed_at_utc': '2026-10-14T00:00:00Z',
                            'issuer_id': 'ISSUER-EQ-001',
                            'statement': 'Independent equality re-test.'}
                raw = canonical(document)
                (directory/(subject + '-' + arm + '.json')).write_bytes(raw)
                (directory/(subject + '-' + arm + '.sig')).write_bytes(self.issuer.sign(raw))
        return directory

    def code_of(self, call):
        try:
            call()
        except PairedEvaluationError as exc:
            return exc.code
        raise AssertionError('expected PairedEvaluationError')

    def validate(self, attestations=None):
        return pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=attestations or self.attestations)

    def test_differing_provider_revision_across_arms_rejected(self):
        att = self._attestations({('B', 'provider_revision'): 'other-revision'})
        self.assertEqual(self.code_of(lambda: self.validate(att)),
                         'STRICT_ATTESTATION_VALUE_MISMATCH')

    def test_differing_system_baseline_across_arms_rejected(self):
        att = self._attestations({('A', 'system_baseline'): 'other-baseline'})
        self.assertEqual(self.code_of(lambda: self.validate(att)),
                         'STRICT_ATTESTATION_VALUE_MISMATCH')

    def test_declared_mismatch_rejected_and_declared_match_passes(self):
        attested = 'provider_revision/shared'
        self.manifest['runtime']['model']['provider_revision'] = {
            'state': 'UNVERIFIED', 'value': 'not-the-attested-value', 'evidence_sha256': None}
        self.path.write_bytes(canonical(self.manifest))
        self.assertEqual(self.code_of(self.validate), 'STRICT_ATTESTATION_VALUE_MISMATCH')
        self.manifest['runtime']['model']['provider_revision'] = {
            'state': 'UNVERIFIED', 'value': attested, 'evidence_sha256': None}
        self.path.write_bytes(canonical(self.manifest))
        self.assertEqual(self.validate()['status'], 'VALIDATED_NOT_EXECUTED')

    def test_declared_verified_keeps_dedicated_code(self):
        self.manifest['runtime']['model']['provider_revision'] = {
            'state': 'VERIFIED', 'value': 'whatever', 'evidence_sha256': '5'*64}
        self.path.write_bytes(canonical(self.manifest))
        self.assertEqual(self.code_of(self.validate), 'ATTESTATION_NOT_SUPPORTED')

    def test_equal_values_strict_test_double_run_still_bounded(self):
        result = pe._run_pair_with_ports(self.path, self.excluded, self.root/'out-eq', launcher=capture,
                                         trust_registry_path=self.registry, evidence_dir=self.attestations)
        self.assertEqual(result['evidence_class'], 'TEST_DOUBLE')
        self.assertNotIn('model', result)
        self.assertEqual(result['strict_eligibility'], 'HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY')
        self.assertEqual(pe.inspect_run(self.root/'out-eq'/self.manifest['run_id'])['status'], 'INTACT')

    def test_exploratory_default_unchanged_after_equality(self):
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        outcome = pe.validate_run_manifest(self.path.read_bytes(), manifest_dir=self.path.parent)
        self.assertEqual(outcome['status'], 'VALIDATED_NOT_EXECUTED')


if __name__ == '__main__':
    unittest.main()
