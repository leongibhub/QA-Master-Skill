"""Independent re-test of TASK-080 (CODE-ATTESTATION-VERIFIER-REPAIR-001) at 362d9c1.

Authored by the independent tester. Verifies the R-01/R-02/R-03 and F-01..F-03
repairs behave per DES-061, on fresh fixtures and the retained roots. Synthetic
keys only; no provider evidence, model call, pair run or holdout material.
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

# Retained run roots from the CR-011 verification exercise. These live under
# the git-ignored `.qa-master/` working directory and are absent in a clean
# checkout, so the retained-roots checks skip when they are not present.
RETAINED_ROOTS = [
    REPO/'.qa-master/paired-pilot/observed-v4-final-freeze/CR011-EXPLORATORY-PUBLIC-DEV-001',
    REPO/'.qa-master/cr011-independent/preview',
    REPO/'.qa-master/cr011-independent/final-installed/preview',
    REPO/'.qa-master/cr011-independent/repaired-installed/preview',
]


class RepairReTest(unittest.TestCase):
    """Independent verification that each repair does what the review asked."""

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
        registry = {'schema_version': 1, 'registry_id': 'REG-RE-001',
                    'created_at_utc': '2026-10-16T00:00:00Z',
                    'issuers': [{'issuer_id': 'ISSUER-RE-001', 'subject': subject,
                                 'algorithm': 'ED25519', 'public_key_multibase': self.public_hex}
                                for subject in pe.ATTESTATION_SUBJECTS]}
        path = self.root/'registry-re.json'
        path.write_bytes(canonical(registry))
        return path

    def _attestations(self):
        directory = self.root/'attestations-re'
        directory.mkdir(exist_ok=True)
        for arm in ('A', 'B'):
            for subject in pe.ATTESTATION_SUBJECTS:
                document = {'schema_version': 1, 'subject': subject, 'arm_id': arm,
                            'value': subject + '/shared',
                            'observed_at_utc': '2026-10-14T00:00:00Z',
                            'issuer_id': 'ISSUER-RE-001',
                            'statement': 'Independent re-test synthetic.'}
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

    def validate(self):
        return pe.validate_run_manifest(
            self.path.read_bytes(), manifest_dir=self.path.parent,
            trust_registry_path=self.registry, evidence_dir=self.attestations)

    def run_strict(self, output='output-re'):
        return pe._run_pair_with_ports(self.path, self.excluded, self.root/output, launcher=capture,
                                       trust_registry_path=self.registry, evidence_dir=self.attestations)

    # RT-1: R-02 repair on the real retained roots (fresh process, real files)

    @unittest.skipUnless(all((p/'preflight.json').is_file() for p in RETAINED_ROOTS),
                         'retained roots absent in clean checkout')
    def test_retained_roots_inspect_intact(self):
        existing = [p for p in RETAINED_ROOTS if (p/'preflight.json').is_file()]
        self.assertEqual(len(existing), 4)
        for run_root in existing:
            self.assertEqual(pe.inspect_run(run_root)['status'], 'INTACT', run_root)

    @unittest.skipUnless((RETAINED_ROOTS[0]/'result.json').is_file(),
                         'retained pilot root absent in clean checkout')
    def test_retained_pilot_root_gradable(self):
        # Full grade chain on the retained pilot root with a machine-fact bundle.
        from qa_master._paired_contract import read_bytes, strict_json, contained
        root = RETAINED_ROOTS[0]
        result = json.loads((root/'result.json').read_bytes())
        attempt = result['attempts'][0]
        visible = strict_json(read_bytes(contained(root, 'calls/'+attempt['call_id']+'/common/visible-input.json')))
        env_rows = [e for e in attempt['ledger'] if e['role'] == 'envelope']
        envelope = strict_json(read_bytes(contained(root, env_rows[0]['relative_path'])))
        obs = envelope['observations'][0]
        bundle = {'schema_version': 1, 'run_manifest_sha256': result['run_manifest_sha256'],
                  'response_schema_sha256': result['response_schema_sha256'],
                  'assertions': [{'id': 'RT1-GRADE-001', 'scenario_id': attempt['scenario_id'],
                                  'check_id': obs['check_id'],
                                  'expected': {'value_type': obs['value_type'], 'value': obs['value']},
                                  'required_evidence_refs': sorted(obs['evidence_refs'])[:1],
                                  'oracle_ref': 'oracle/committed.md'}]}
        src = self.root/'assertions-re.json'; src.write_bytes(canonical(bundle))
        out = self.root/'grade-re.json'
        report = pe.grade_run(root, src, out)
        self.assertEqual(report['assertions'][0]['status'], 'SATISFIED')

    # RT-2: R-01 repair end-to-end on a fresh strict TEST_DOUBLE run

    def test_strict_test_double_run_root_intact_and_unpromoted(self):
        result = self.run_strict()
        self.assertEqual(result['evidence_class'], 'TEST_DOUBLE')
        self.assertNotIn('model', result)
        run_root = self.root/'output-re'/self.manifest['run_id']
        self.assertEqual(pe.inspect_run(run_root)['status'], 'INTACT')
        written = json.loads((run_root/'result.json').read_bytes())
        self.assertNotIn('model', written)
        self.assertEqual(written['strict_eligibility'], 'HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY')
        # A tampered model member must now be rejected (R-03).
        written2 = dict(written)
        written2['model'] = {'provider_revision': {'state': 'VERIFIED', 'value': 'fake',
                                                    'evidence_sha256': '0'*64},
                             'system_baseline': {'state': 'VERIFIED', 'value': 'fake',
                                                 'evidence_sha256': '0'*64}}
        tampered = run_root/'../tampered-run'
        tampered.mkdir(exist_ok=True)
        import shutil
        shutil.copytree(run_root, tampered, dirs_exist_ok=True)
        (tampered/'result.json').write_bytes(canonical(written2)+b'\n')
        # inspect_run wraps every _inspect rejection as RUN_INTEGRITY_FAILURE;
        # the tampered model member must be rejected (R-03 rebinding inside).
        code = self.code_of(lambda: pe.inspect_run(tampered))
        self.assertEqual(code, 'RUN_INTEGRITY_FAILURE')

    # RT-3: F-01/F-02 dedicated codes (fresh negative probes)

    def test_registry_bad_grammar_maps_to_dedicated_code(self):
        for mutate in (
            lambda reg: reg.update(issuers=[]),
            lambda reg: reg.update(extra=1),
            lambda reg: reg['issuers'][0].update(subject='other'),
            lambda reg: reg['issuers'][0].update(algorithm='RSA'),
            lambda reg: reg['issuers'][0].update(public_key_multibase='short'),
            lambda reg: reg['issuers'].append(dict(reg['issuers'][0])),
            lambda reg: reg.update(created_at_utc='not-a-time'),
        ):
            registry = json.loads(self.registry.read_text())
            mutate(registry)
            self.registry.write_bytes(canonical(registry))
            self.assertEqual(self.code_of(self.validate), 'TRUST_REGISTRY_INVALID', mutate)
            self.registry.write_bytes(canonical(json.loads(
                '{"schema_version":1,"registry_id":"REG-RE-001","created_at_utc":"2026-10-16T00:00:00Z",'
                '"issuers":[{"issuer_id":"ISSUER-RE-001","subject":"provider_revision","algorithm":"ED25519",'
                '"public_key_multibase":"%s"},'
                '{"issuer_id":"ISSUER-RE-001","subject":"system_baseline","algorithm":"ED25519",'
                '"public_key_multibase":"%s"}]}' % (self.public_hex, self.public_hex))))

    def test_attestation_bad_grammar_maps_to_dedicated_code(self):
        for name, mutate in (
            ('empty value', lambda d: d.update(value='')),
            ('string schema_version', lambda d: d.update(schema_version='1')),
            ('bad arm', lambda d: d.update(arm_id='C')),
            ('bad time', lambda d: d.update(observed_at_utc='2026-13-40T00:00:00Z')),
        ):
            document = json.loads((self.attestations/'provider_revision-A.json').read_text())
            mutate(document)
            raw = canonical(document)
            (self.attestations/'provider_revision-A.json').write_bytes(raw)
            (self.attestations/'provider_revision-A.sig').write_bytes(self.issuer.sign(raw))
            self.assertEqual(self.code_of(self.validate), 'ATTESTATION_INVALID', name)

    # RT-4: F-03 canonical-bytes enforcement (leading whitespace too)

    def test_noncanonical_document_bytes_rejected_both_sides(self):
        raw = (self.attestations/'system_baseline-B.json').read_bytes()
        for mutated in (raw + b' ', b' ' + raw, b'\n' + raw):
            (self.attestations/'system_baseline-B.json').write_bytes(mutated)
            self.assertEqual(self.code_of(self.validate), 'ATTESTATION_INVALID')
        (self.attestations/'system_baseline-B.json').write_bytes(raw)

    # RT-5: exploratory default path still untouched

    def test_exploratory_default_unchanged(self):
        self.manifest['profile'] = pe.PROFILE
        self.path.write_bytes(canonical(self.manifest))
        outcome = pe.validate_run_manifest(self.path.read_bytes(), manifest_dir=self.path.parent)
        self.assertEqual(outcome['status'], 'VALIDATED_NOT_EXECUTED')
        result = pe._run_pair_with_ports(self.path, self.excluded, self.root/'out-exp', launcher=capture)
        self.assertEqual(result['evidence_class'], 'TEST_DOUBLE')
        self.assertNotIn('attestation_verdicts', result)
        self.assertNotIn('strict_eligibility', result)
        self.assertNotIn('model', result)

    # RT-6: CLI wiring still correct after the repair

    def test_cli_repair_unchanged(self):
        done = subprocess.run([sys.executable, '-m', 'qa_master.paired_evaluation', 'validate', str(self.path),
                               '--trust-registry', str(self.registry), '--attestations', str(self.attestations)],
                              capture_output=True, text=True, cwd=str(REPO))
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn('VALIDATED_NOT_EXECUTED', done.stdout)


if __name__ == '__main__':
    unittest.main()
