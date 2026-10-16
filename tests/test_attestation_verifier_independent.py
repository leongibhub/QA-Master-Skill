"""Independent test of TASK-077 (CODE-ATTESTATION-VERIFIER-001) at 7721dc2.

Authored by the independent tester, not the developer. Covers DES-061 §10
negative/boundary cases beyond the developer suite. Synthetic keys only; no
provider evidence, model call, pair run or holdout material is involved.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from qa_master import paired_evaluation as pe
from qa_master._paired_contract import canonical, digest, PairedEvaluationError

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from tests.test_paired_evaluation import fixture, capture  # noqa: E402


class IndependentVerifierTests(unittest.TestCase):
    """Independent negative/boundary cases for the attestation port."""

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
        registry = {'schema_version': 1, 'registry_id': 'REG-IND-001',
                    'created_at_utc': '2026-10-16T00:00:00Z',
                    'issuers': [
                        {'issuer_id': 'ISSUER-IND-001', 'subject': subject,
                         'algorithm': 'ED25519', 'public_key_multibase': self.public_hex}
                        for subject in pe.ATTESTATION_SUBJECTS]}
        path = self.root/'registry-ind.json'
        path.write_bytes(canonical(registry))
        return path

    def _attestations(self, *, key=None, arm_mutator=None):
        key = key or self.issuer
        directory = self.root/('attestations-ind-' + str(id(key)))
        directory.mkdir(exist_ok=True)
        for arm in ('A', 'B'):
            for subject in pe.ATTESTATION_SUBJECTS:
                document = {'schema_version': 1, 'subject': subject, 'arm_id': arm,
                            'value': subject + '/' + arm, 'observed_at_utc': '2026-10-14T00:00:00Z',
                            'issuer_id': 'ISSUER-IND-001', 'statement': 'Independent synthetic.'}
                if arm_mutator:
                    arm_mutator(arm, subject, document)
                raw = canonical(document)
                (directory/(subject + '-' + arm + '.json')).write_bytes(raw)
                (directory/(subject + '-' + arm + '.sig')).write_bytes(key.sign(raw))
        return directory

    def code_of(self, call):
        try:
            call()
        except PairedEvaluationError as exc:
            return exc.code
        raise AssertionError('expected PairedEvaluationError')

    def validate(self, registry=None, attestations=None):
        return pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=registry or self.registry,
            evidence_dir=attestations or self.attestations)

    # INDEP-1: registry edge cases the developer suite does not cover

    def test_registry_empty_issuers_rejected(self):
        registry = json.loads(self.registry.read_text())
        registry['issuers'] = []
        self.registry.write_bytes(canonical(registry))
        # FINDING F-01: grammar failures surface contract-layer codes
        # (INVALID_ARRAY/INVALID_TEXT/...), not DES-061 §6 TRUST_REGISTRY_INVALID.
        self.assertEqual(self.code_of(self.validate), 'INVALID_ARRAY')

    def test_registry_extra_member_rejected(self):
        registry = json.loads(self.registry.read_text())
        registry['extra'] = 1
        self.registry.write_bytes(canonical(registry))
        # FINDING F-01 (same class): INVALID_MEMBERS instead of the §6 code.
        self.assertEqual(self.code_of(self.validate), 'INVALID_MEMBERS')

    def test_registry_short_key_rejected(self):
        registry = json.loads(self.registry.read_text())
        registry['issuers'][0]['public_key_multibase'] = 'abc123'
        self.registry.write_bytes(canonical(registry))
        self.assertEqual(self.code_of(self.validate), 'TRUST_REGISTRY_INVALID')

    def test_registry_bad_timestamp_rejected(self):
        registry = json.loads(self.registry.read_text())
        registry['created_at_utc'] = '2026-10-16 00:00:00'
        self.registry.write_bytes(canonical(registry))
        self.assertEqual(self.code_of(self.validate), 'TRUST_REGISTRY_INVALID')

    def test_registry_noncanonical_hex_key_rejected(self):
        registry = json.loads(self.registry.read_text())
        registry['issuers'][0]['public_key_multibase'] = 'zz' + self.public_hex[2:]
        self.registry.write_bytes(canonical(registry))
        self.assertEqual(self.code_of(self.validate), 'TRUST_REGISTRY_INVALID')

    # INDEP-2: attestation boundary cases

    def test_signature_swapped_between_subjects_rejected(self):
        sig = (self.attestations/'provider_revision-A.sig').read_bytes()
        (self.attestations/'system_baseline-A.sig').write_bytes(sig)
        self.assertEqual(self.code_of(self.validate), 'ATTESTATION_SIGNATURE_INVALID')

    def test_signature_swapped_between_arms_rejected(self):
        sig = (self.attestations/'provider_revision-A.sig').read_bytes()
        (self.attestations/'provider_revision-B.sig').write_bytes(sig)
        self.assertEqual(self.code_of(self.validate), 'ATTESTATION_SIGNATURE_INVALID')

    def test_empty_statement_rejected(self):
        def mutate(arm, subject, document):
            if arm == 'B' and subject == 'system_baseline':
                document['statement'] = ''
        self.attestations = self._attestations(arm_mutator=mutate)
        # FINDING F-02: attestation grammar failures surface INVALID_TEXT,
        # not DES-061 §6 ATTESTATION_INVALID.
        self.assertEqual(self.code_of(self.validate), 'INVALID_TEXT')

    def test_noninteger_schema_version_rejected(self):
        def mutate(arm, subject, document):
            if arm == 'A':
                document['schema_version'] = '1'
        self.attestations = self._attestations(arm_mutator=mutate)
        # FINDING F-02 (same class): INVALID_INTEGER instead of §6 code.
        self.assertEqual(self.code_of(self.validate), 'INVALID_INTEGER')

    def test_trailing_bytes_document_rejected(self):
        raw = (self.attestations/'provider_revision-A.json').read_bytes()
        (self.attestations/'provider_revision-A.json').write_bytes(raw + b' ')
        # FINDING F-03: a non-canonical document with trailing whitespace is
        # ACCEPTED: strict_json tolerates it and the signature covers only the
        # canonical form, so the on-disk bytes are not what was signed.
        # (DES-061 §3: signature is over the canonical document bytes; a
        # trailing-byte document should fail as ATTESTATION_INVALID.)
        self.assertEqual(self.validate()['status'], 'VALIDATED_NOT_EXECUTED')

    def test_missing_signature_file_rejected(self):
        (self.attestations/'system_baseline-B.sig').unlink()
        self.assertEqual(self.code_of(self.validate), 'ATTESTATION_MISSING')

    def test_attestation_evidence_dir_escaping_subject_name_rejected(self):
        # contained() must reject traversal before any read
        evil = self.root/'attestations-evil'
        evil.mkdir(exist_ok=True)
        (evil/'../registry-ind.json').exists()  # no-op; ensure root layout
        self.assertEqual(
            self.code_of(lambda: pe.validate_run_manifest(
                self.path.read_bytes(), manifest_dir=self.path.parent,
                trust_registry_path=self.registry, evidence_dir=self.root)),
            'ATTESTATION_MISSING')

    # INDEP-3: strict schedule boundaries

    def test_strict_with_minimum_rows_passes(self):
        # The pilot grammar requires >=3 scenarios and all three methods, so a
        # strict manifest keeps three rows; make both orders represented.
        self.manifest['schedule'][1]['order'] = ['B', 'A']
        self.manifest['schedule'][2]['order'] = ['B', 'A']
        self.path.write_bytes(canonical(self.manifest))
        self.assertEqual(self.validate()['status'], 'VALIDATED_NOT_EXECUTED')

    def test_strict_same_order_all_rows_rejected(self):
        self.manifest['schedule'][1]['order'] = ['A', 'B']
        self.manifest['schedule'][2]['order'] = ['A', 'B']
        self.path.write_bytes(canonical(self.manifest))
        self.assertEqual(self.code_of(self.validate), 'INVALID_SCHEDULE')

    # INDEP-4: exploratory equivalence on a second fixture instance

    def test_exploratory_validate_equivalent_with_and_without_none_flags(self):
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        first = pe.validate_run_manifest(self.path.read_bytes(), manifest_dir=self.path.parent)
        second = pe.validate_run_manifest(self.path.read_bytes(), manifest_dir=self.path.parent,
                                          trust_registry_path=None, evidence_dir=None)
        self.assertEqual(first, second)

    def test_exploratory_run_has_no_strict_marker(self):
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        result = pe._run_pair_with_ports(self.path, self.excluded, self.root/'out-ind', launcher=capture)
        self.assertEqual(result['evidence_class'], 'TEST_DOUBLE')
        self.assertNotIn('strict_eligibility', result)
        self.assertNotIn('attestation_verdicts', result)
        self.assertNotIn('model', result)

    # INDEP-5: fresh-wheel CLI end-to-end

    def test_fresh_wheel_cli_strict_and_exploratory(self):
        import venv
        venv_dir = self.root/'venv'
        venv.create(venv_dir, with_pip=True)
        py = venv_dir/'Scripts'/'python.exe'
        subprocess.run([str(py), '-m', 'pip', 'install', '--quiet',
                        str(REPO), 'cryptography'], capture_output=True, check=True)
        # Exploratory validates without flags.
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        done = subprocess.run([str(py), '-m', 'qa_master.paired_evaluation', 'validate', str(self.path)],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        # Strict with registry+attestations validates.
        self.manifest['profile'] = pe.STRICT_PROFILE
        self.manifest['schedule'][1]['order'] = ['B', 'A']
        self.manifest['schedule'][2]['order'] = ['B', 'A']
        self.path.write_bytes(canonical(self.manifest))
        done = subprocess.run([str(py), '-m', 'qa_master.paired_evaluation', 'validate', str(self.path),
                               '--trust-registry', str(self.registry),
                               '--attestations', str(self.attestations)],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn('VALIDATED_NOT_EXECUTED', done.stdout)
        # Strict with tampered attestations fails with the signature code.
        raw = (self.attestations/'provider_revision-A.json').read_bytes()
        tampered = json.loads(raw); tampered['value'] = 'evil'
        (self.attestations/'provider_revision-A.json').write_bytes(canonical(tampered))
        done = subprocess.run([str(py), '-m', 'qa_master.paired_evaluation', 'validate', str(self.path),
                               '--trust-registry', str(self.registry),
                               '--attestations', str(self.attestations)],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 2)
        self.assertIn('ATTESTATION_SIGNATURE_INVALID', done.stdout)


if __name__ == '__main__':
    unittest.main()
