import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import shutil
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor

from qa_master.semantic_quality import (SemanticQualityError, evaluate_bundle,
                                        fixed_assets, inspect_result, validate_bundle)


def canon(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


class SemanticQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); (self.root / 'inputs').mkdir(); (self.root / 'source').mkdir()
        self.source = b'published source bytes'; (self.root / 'source' / 'rule.txt').write_bytes(self.source)
        self.response = {"schema_version": 1, "artifact_id": "ART-1", "artifact_state": "DRAFT_UNAPPROVED", "execution_state": "NOT_EXECUTED", "summary": "draft", "extensions": {}, "observations": [{"check_id":"CHECK-1","value_type":"STRING","value":"yes","source_fact_ids":["F-1"]}], "cases": [], "gaps": []}
        raw=canon(self.response); (self.root/'inputs'/'response.json').write_bytes(raw)
        a=fixed_assets(); contract={k:a[k] for k in ('contract_sha256','projection_sha256','normalizer_sha256','result_schema_sha256','secret_scanner_sha256')}
        contract.update(contract_id=a['contract']['contract_id'], projection_id=a['projection']['projection_id'], normalizer_id=a['normalizer']['normalizer_id'], result_schema_id=a['result_schema']['result_schema_id'], secret_scanner_id=a['secret_scanner']['secret_scanner_id'])
        cats=[]
        for category in ('REQUIREMENTS_CONFLICTS','METHOD_SELECTION','FUNCTIONAL_API_INTEGRATION','SECURITY_SCOPE_AUTHORITY','RECOVERY_REGRESSION','NON_FUNCTIONAL','DELIVERABLE_USABILITY'):
            cats.append({'category':category,'state':'APPLICABLE' if category=='METHOD_SELECTION' else 'NOT_APPLICABLE','reason':None if category=='METHOD_SELECTION' else 'not applicable','source_ids':['SRC-1'],'fact_ids':['F-1'] if category=='METHOD_SELECTION' else []})
        self.bundle={"schema_version":1,"evaluation_id":"SQE-1","fixture_class":"PUBLIC_DEVELOPMENT","created_at_utc":"2026-10-15T00:00:00Z","contract":contract,"response":{"state":"PRESENT","source_path":"inputs/response.json","byte_count":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"declared_projection_id":a['projection']['projection_id']},"sources":[{"id":"SRC-1","kind":"requirement","state":"AVAILABLE","locator":"source/rule.txt","sha256":hashlib.sha256(self.source).hexdigest()}],"facts":[{"id":"F-1","source_ids":["SRC-1"],"category":"METHOD_SELECTION","value_type":"STRING","value":"yes","scope":"published"}],"category_applicability":cats,"obligations":[{"id":"OB-1","category":"METHOD_SELECTION","interpretation":"rule","source_ids":["SRC-1"],"required_gap_reason":None,"source_fact_ids":["F-1"],"oracle_state":"DETERMINATE","check_id":"CHECK-1","operator":"EQUALS","expected_fact_ids":["F-1"],"allowed_readiness":["DESIGN_READY"],"case_required":False}]}

        self.addCleanup(lambda: shutil.rmtree(self.output(), ignore_errors=True))

    def update_response(self):
        raw = canon(self.response)
        (self.root / 'inputs' / 'response.json').write_bytes(raw)
        self.bundle['response'].update(byte_count=len(raw), sha256=hashlib.sha256(raw).hexdigest())

    def profile(self):
        result = evaluate_bundle(self.write_bundle(), self.output())
        return json.loads(Path(result['profile_path']).read_bytes())

    def write_bundle(self):
        path=self.root/'bundle.json'; path.write_bytes(canon(self.bundle)); return path

    def output(self):
        return self.root.parent / ('semantic-out-' + self.root.name)

    def test_validates_evaluates_and_inspects(self):
        path=self.write_bundle(); self.assertEqual(validate_bundle(path)['status'],'VALIDATED_NOT_EVALUATED')
        result=evaluate_bundle(path,self.output()); self.assertEqual(result['status'],'EVALUATED_DRAFT_ONLY')
        self.assertEqual(inspect_result(Path(result['profile_path']).parent)['status'],'INTACT')

    def test_hash_drift_rejects_without_output(self):
        self.bundle['response']['sha256']='0'*64
        with self.assertRaisesRegex(SemanticQualityError,'RESPONSE_INTEGRITY_FAILURE'):
            evaluate_bundle(self.write_bundle(),self.root/'out')
        self.assertFalse((self.root/'out').exists())

    def test_one_of_duplicate_canonical_value_rejected(self):
        self.bundle['facts'].append(dict(self.bundle['facts'][0],id='F-2'))
        ob=self.bundle['obligations'][0]; ob['operator']='ONE_OF'; ob['expected_fact_ids']=['F-1','F-2']
        with self.assertRaises(SemanticQualityError): validate_bundle(self.write_bundle())

    def test_inspect_detects_tampered_retained_profile(self):
        result=evaluate_bundle(self.write_bundle(),self.output())
        profile=Path(result['profile_path']); profile.write_bytes(b'{"rows":[]}')
        self.assertEqual(inspect_result(profile.parent)['status'],'MISMATCH')

    def test_identical_result_id_is_not_overwritten(self):
        output=self.output()
        evaluate_bundle(self.write_bundle(),output)
        with self.assertRaisesRegex(SemanticQualityError,'RESULT_EXISTS'):
            evaluate_bundle(self.write_bundle(),output)

    def test_inspect_rejects_joint_profile_and_manifest_rewrite(self):
        result=evaluate_bundle(self.write_bundle(),self.output()); root=Path(result['profile_path']).parent
        profile=json.loads((root/'profile.json').read_text()); profile['rows'][0]['outcome']='VIOLATED'; raw=canon(profile); (root/'profile.json').write_bytes(raw)
        manifest=json.loads((root/'manifest.json').read_text())
        for row in manifest['files']:
            if row['path']=='profile.json': row.update(sha256=hashlib.sha256(raw).hexdigest(),byte_count=len(raw))
        (root/'manifest.json').write_bytes(canon(manifest))
        self.assertEqual(inspect_result(root)['status'],'MISMATCH')


    def test_inspect_missing_precedes_undeclared(self):
        result = evaluate_bundle(self.write_bundle(), self.output())
        root = Path(result['profile_path']).parent
        (root / 'profile.json').unlink()
        (root / 'extra.txt').write_bytes(b'extra')
        self.assertEqual(inspect_result(root)['status'], 'MISSING')

    def test_inspect_mismatch_precedes_undeclared(self):
        result = evaluate_bundle(self.write_bundle(), self.output())
        root = Path(result['profile_path']).parent
        (root / 'profile.json').write_bytes(b'{}')
        (root / 'extra.txt').write_bytes(b'extra')
        self.assertEqual(inspect_result(root)['status'], 'MISMATCH')

    def test_inspect_reservation_precedes_missing(self):
        result = evaluate_bundle(self.write_bundle(), self.output())
        root = Path(result['profile_path']).parent
        (root / 'profile.json').unlink()
        (root / 'reservation.json').write_bytes(b'{}')
        self.assertEqual(inspect_result(root)['status'], 'INCOMPLETE')

    def test_inspect_extra_directory_is_undeclared(self):
        result = evaluate_bundle(self.write_bundle(), self.output())
        root = Path(result['profile_path']).parent
        (root / 'extra').mkdir()
        self.assertEqual(inspect_result(root)['status'], 'UNDECLARED')

    def test_inspect_wrong_role_is_mismatch(self):
        result = evaluate_bundle(self.write_bundle(), self.output())
        root = Path(result['profile_path']).parent
        manifest = json.loads((root / 'manifest.json').read_bytes())
        manifest['files'][0]['role'] = 'PROFILE'
        (root / 'manifest.json').write_bytes(canon(manifest))
        self.assertEqual(inspect_result(root)['status'], 'MISMATCH')

    def test_inspect_is_read_only(self):
        result = evaluate_bundle(self.write_bundle(), self.output())
        root = Path(result['profile_path']).parent
        before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        with patch('qa_master.semantic_quality.tempfile.mkdtemp', side_effect=AssertionError('no temp')):
            self.assertEqual(inspect_result(root)['status'], 'INTACT')
        after = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_publication_commit_failure_cleans_own_reservation(self):
        with patch('qa_master.semantic_quality.os.replace', side_effect=OSError('injected')):
            with self.assertRaisesRegex(SemanticQualityError, 'LOCAL_IO_FAILURE'):
                evaluate_bundle(self.write_bundle(), self.output())
        self.assertEqual(list(self.output().iterdir()), [])

    def test_competing_publishers_preserve_one_winner(self):
        bundle = self.write_bundle()
        def publish(_):
            try:
                return evaluate_bundle(bundle, self.output())['status']
            except SemanticQualityError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(publish, range(2)))
        self.assertCountEqual(outcomes, ['EVALUATED_DRAFT_ONLY', 'RESULT_EXISTS'])
        roots = list(self.output().iterdir())
        self.assertEqual(len(roots), 1)
        self.assertEqual(inspect_result(roots[0])['status'], 'INTACT')

    def test_bad_summary_preserves_semantic_channel(self):
        self.response.pop('summary')
        self.update_response()
        rows = {row['dimension']: row for row in self.profile()['rows']}
        self.assertEqual(rows['SHAPE']['outcome'], 'VIOLATED')
        self.assertEqual(rows['SEMANTIC']['outcome'], 'SATISFIED')

    def test_unknown_fact_reference_does_not_change_typed_truth(self):
        self.response['observations'][0]['source_fact_ids'] = ['UNKNOWN']
        self.update_response()
        rows = {row['dimension']: row for row in self.profile()['rows']}
        self.assertEqual(rows['SEMANTIC']['outcome'], 'SATISFIED')
        self.assertEqual(rows['PROVENANCE']['outcome'], 'VIOLATED')

    def test_boolean_is_not_integer_json_value(self):
        self.bundle['facts'][0].update(value_type='JSON', value={'x': 1})
        self.response['observations'][0].update(value_type='JSON', value={'x': True})
        self.update_response()
        rows = {row['dimension']: row for row in self.profile()['rows']}
        self.assertEqual(rows['SEMANTIC']['outcome'], 'VIOLATED')

    def test_absent_response_omits_retained_response_files(self):
        self.bundle['response'] = dict(state='ABSENT', source_path=None, byte_count=None,
                                       sha256=None, declared_projection_id="qa-quality-case-gap-v1")
        result = evaluate_bundle(self.write_bundle(), self.output())
        root = Path(result['profile_path']).parent
        self.assertFalse((root / 'response.source.json').exists())
        self.assertFalse((root / 'response.normalized.json').exists())
        self.assertEqual(inspect_result(root)['status'], 'INTACT')
    def complete_case(self):
        claim={'text':'review visible rule','source_fact_ids':['F-1']}
        section={'state':'DEFINED','items':[claim],'reason':None}
        return {'case_id':'CASE-1','obligation_ids':['OB-1'],'category':'METHOD_SELECTION','readiness':'DESIGN_READY','setup':section,'preconditions':[],'data':section,'actions':[claim],'expected_oracle':dict(section,oracle_fact_ids=['F-1']),'cleanup':{'state':'NOT_APPLICABLE','items':[],'reason':'read-only review'},'source_fact_ids':['F-1'],'gap_ids':[],'missing_fields':[],'extensions':{}}

    def dimensions(self):
        self.update_response()
        return {r['dimension']:r for r in self.profile()['rows']}

    def test_complete_case_and_duplicate_identity(self):
        self.bundle['obligations'][0]['case_required']=True
        self.response['cases']=[self.complete_case()]
        self.assertEqual(self.dimensions()['USABILITY']['outcome'],'SATISFIED')
        self.response['cases'].append(self.complete_case())
        rows=self.dimensions()
        self.assertEqual(rows['USABILITY']['reason_code'],'MAPPED_CASE_INVALID')
        self.assertEqual(rows['PROVENANCE']['outcome'],'SATISFIED')

    def test_invalid_optional_case_not_ignored(self):
        case=self.complete_case();case['actions']=[]
        self.response['cases']=[case]
        self.assertEqual(self.dimensions()['USABILITY']['reason_code'],'OPTIONAL_CASE_INVALID')

    def test_invalid_readiness_keeps_reference_honesty(self):
        case=self.complete_case();case['readiness']='EXECUTABLE';self.response['cases']=[case]
        rows=self.dimensions()
        self.assertEqual(rows['USABILITY']['outcome'],'VIOLATED')
        self.assertEqual(rows['PROVENANCE']['outcome'],'SATISFIED')

    def test_unavailable_observations_preserve_case_usability(self):
        self.response['cases']=[self.complete_case()];self.response['observations']=None
        rows=self.dimensions()
        self.assertEqual(rows['SEMANTIC']['reason_code'],'OBSERVATIONS_CHANNEL_UNAVAILABLE')
        self.assertEqual(rows['USABILITY']['outcome'],'SATISFIED')
        self.assertEqual(rows['PROVENANCE']['outcome'],'UNSCORABLE')

    def test_definite_provenance_defect_precedes_missing_channel(self):
        self.response['observations']=None
        case=self.complete_case();case['source_fact_ids']=['UNKNOWN'];self.response['cases']=[case]
        self.assertEqual(self.dimensions()['PROVENANCE']['outcome'],'VIOLATED')

    def test_unknown_only_observation_is_isolated(self):
        self.response['observations'].append({'check_id':'OTHER','value_type':'STRING','value':'extra','source_fact_ids':['UNKNOWN']})
        rows=self.dimensions()
        self.assertEqual(rows['PROVENANCE']['outcome'],'SATISFIED')
        self.assertEqual(rows['SHAPE']['outcome'],'SATISFIED')

    def missing_oracle(self):
        self.bundle['obligations'][0].update(oracle_state='ORACLE_MISSING',required_gap_reason='ORACLE_MISSING',check_id=None,operator=None,expected_fact_ids=[],allowed_readiness=['BLOCKED_ORACLE_MISSING'])
        self.bundle['category_applicability'][1].update(state='ORACLE_MISSING',reason='no threshold in inspected source')
        self.response['observations']=[]
        return {'gap_id':'GAP-1','obligation_ids':['OB-1'],'reason':'ORACLE_MISSING','fact_ids':['F-1'],'source_ids':['SRC-1'],'needed_evidence':'approved threshold','evidence_pointer':'source/rule.txt'}

    def test_missing_oracle_exact_gap_provenance(self):
        gap=self.missing_oracle()
        rows=self.dimensions()
        self.assertEqual(rows['SEMANTIC']['outcome'],'ORACLE_MISSING')
        self.assertEqual(rows['USABILITY']['outcome'],'ORACLE_MISSING')
        self.assertEqual(rows['PROVENANCE']['reason_code'],'REQUIRED_GAP_MISSING')
        self.response['gaps']=[gap]
        self.assertEqual(self.dimensions()['PROVENANCE']['reason_code'],'MISSING_ORACLE_HONESTLY_REPORTED')

    def test_unavailable_gap_keeps_oracle_missing(self):
        self.missing_oracle();self.response['gaps']=None
        rows=self.dimensions()
        self.assertEqual(rows['SEMANTIC']['outcome'],'ORACLE_MISSING')
        self.assertEqual(rows['PROVENANCE']['outcome'],'UNSCORABLE')

    def test_source_missing_honest_gap(self):
        self.bundle['sources'].append({'id':'SRC-2','kind':'contract','state':'NOT_AVAILABLE','locator':None,'sha256':None})
        ob=self.bundle['obligations'][0]
        ob.update(source_ids=['SRC-1','SRC-2'],oracle_state='UNSCORABLE',required_gap_reason='SOURCE_MISSING',check_id=None,operator=None,expected_fact_ids=[])
        self.bundle['category_applicability'][1].update(source_ids=['SRC-1','SRC-2'],state='UNSCORABLE',reason='contract unavailable')
        self.response['observations']=[]
        self.response['gaps']=[{'gap_id':'GAP-1','obligation_ids':['OB-1'],'reason':'SOURCE_MISSING','fact_ids':['F-1'],'source_ids':['SRC-1','SRC-2'],'needed_evidence':'contract','evidence_pointer':'missing:contract'}]
        rows=self.dimensions()
        self.assertEqual(rows['SEMANTIC']['outcome'],'UNSCORABLE')
        self.assertEqual(rows['PROVENANCE']['outcome'],'SATISFIED')

    def test_registered_legacy_is_unscorable_and_intact(self):
        assets=fixed_assets()
        self.bundle['contract'].update(projection_id='paired-neutral-envelope-v1',projection_sha256=assets['legacy_projection_sha256'])
        self.bundle['response']['declared_projection_id']='paired-neutral-envelope-v1'
        result=evaluate_bundle(self.write_bundle(),self.output())
        profile=json.loads(Path(result['profile_path']).read_bytes())
        self.assertEqual({r['reason_code'] for r in profile['rows']},{'LEGACY_PROJECTION_UNSUPPORTED'})
        self.assertEqual(inspect_result(Path(result['profile_path']).parent)['status'],'INTACT')

    def test_global_invalid_identity_keeps_total_four_rows(self):
        self.response['artifact_id']=[]
        rows=self.dimensions()
        self.assertEqual(rows['SHAPE']['outcome'],'VIOLATED')
        self.assertEqual({rows[x]['outcome'] for x in ('SEMANTIC','USABILITY','PROVENANCE')},{'UNSCORABLE'})

    def test_claim_policy_does_not_change_semantic_truth(self):
        self.response['execution_state']='PASSED'
        rows=self.dimensions()
        self.assertEqual(rows['SHAPE']['outcome'],'VIOLATED')
        self.assertEqual(rows['SEMANTIC']['outcome'],'SATISFIED')

    def test_boundary_references_and_claims(self):
        import qa_master.semantic_quality as sq
        self.assertTrue(sq._valid_refs(['F'+str(i) for i in range(64)]))
        self.assertFalse(sq._valid_refs(['F'+str(i) for i in range(65)]))
        claim={'text':'x','source_fact_ids':['F-1']}
        self.assertTrue(sq._claims_valid([claim]*64,{}))
        self.assertFalse(sq._claims_valid([claim]*65,{}))

    def test_typed_bounds_and_decimal(self):
        import qa_master.semantic_quality as sq
        self.assertTrue(sq._typed('INTEGER',10**34-1))
        self.assertFalse(sq._typed('INTEGER',10**34))
        self.assertTrue(sq._typed('STRING','x'*20000))
        self.assertFalse(sq._typed('STRING','x'*20001))
        self.assertTrue(sq._typed('DECIMAL','-0.1'))
        self.assertFalse(sq._typed('DECIMAL','-0'))
        self.assertTrue(sq._typed('JSON',[None]*4095))
        self.assertFalse(sq._typed('JSON',[None]*4096))
        value=None
        for _ in range(16):value=[value]
        self.assertTrue(sq._typed('JSON',value))
        self.assertFalse(sq._typed('JSON',[value]))

    def test_256_observations_and_over_limit(self):
        self.response['observations'] += [{'check_id':'EXTRA-'+str(i),'value_type':'STRING','value':'x','source_fact_ids':['F-1']} for i in range(255)]
        self.assertEqual(self.dimensions()['SEMANTIC']['outcome'],'SATISFIED')
        self.response['observations'].append({'check_id':'EXTRA-END'})
        self.assertEqual(self.dimensions()['SEMANTIC']['outcome'],'UNSCORABLE')

    def test_security_pattern_rejects_without_publishing(self):
        self.response['extensions']={'authorization':'Bearer nonsecretfixture123'};self.update_response()
        with self.assertRaisesRegex(SemanticQualityError,'PROHIBITED_INPUT_PATTERN'):
            evaluate_bundle(self.write_bundle(),self.output())
        self.assertFalse(self.output().exists())

    def test_category_cross_link_rejected(self):
        self.bundle['category_applicability'][0]['fact_ids']=['F-1']
        with self.assertRaisesRegex(SemanticQualityError,'CATEGORY_OBLIGATION_MISMATCH'):
            validate_bundle(self.write_bundle())
    def test_conflicting_sources_require_honest_gap(self):
        self.bundle['sources'].append(dict(self.bundle['sources'][0],id='SRC-2'))
        self.bundle['facts'].append(dict(self.bundle['facts'][0],id='F-2',source_ids=['SRC-2'],value='no'))
        self.bundle['obligations'][0].update(source_ids=['SRC-1','SRC-2'],source_fact_ids=['F-1','F-2'],oracle_state='CONFLICT',required_gap_reason='CONFLICT',check_id=None,operator=None,expected_fact_ids=['F-1','F-2'],allowed_readiness=['STATIC_REVIEW'])
        self.bundle['category_applicability'][1].update(source_ids=['SRC-1','SRC-2'],fact_ids=['F-1','F-2'],state='UNSCORABLE',reason='sources disagree')
        self.response['observations']=[]
        self.response['gaps']=[{'gap_id':'GAP-1','obligation_ids':['OB-1'],'reason':'CONFLICT','fact_ids':['F-1','F-2'],'source_ids':['SRC-1','SRC-2'],'needed_evidence':'resolve rule','evidence_pointer':'source/rule.txt'}]
        rows=self.dimensions()
        self.assertEqual(rows['SEMANTIC']['reason_code'],'SOURCE_FACT_CONFLICT')
        self.assertEqual(rows['PROVENANCE']['reason_code'],'CONFLICT_HONESTLY_REPORTED')

    def test_obligations_256_and_257_boundary(self):
        self.bundle['obligations']=[dict(self.bundle['obligations'][0],id='OB-'+str(i),check_id='CHECK-'+str(i)) for i in range(256)]
        self.assertEqual(validate_bundle(self.write_bundle())['obligation_count'],256)
        self.assertEqual(len(self.profile()['rows']),1024)
        self.bundle['obligations'].append(dict(self.bundle['obligations'][0],id='EXCESS',check_id='EXCESS'))
        with self.assertRaisesRegex(SemanticQualityError,'COUNT_LIMIT'): validate_bundle(self.write_bundle())

    def test_sources_and_facts_256_capacity(self):
        self.bundle['sources']=[dict(self.bundle['sources'][0],id='SRC-'+str(i+1)) for i in range(256)]
        self.bundle['facts']=[dict(self.bundle['facts'][0],id='F-'+str(i+1)) for i in range(256)]
        validate_bundle(self.write_bundle())
        self.bundle['facts'].append(dict(self.bundle['facts'][0],id='EXCESS'))
        with self.assertRaisesRegex(SemanticQualityError,'COUNT_LIMIT'):validate_bundle(self.write_bundle())

    def test_opaque_source_byte_limit(self):
        source=self.root/'source'/'rule.txt'
        data=b'x'*(2*1024*1024)
        source.write_bytes(data);self.bundle['sources'][0]['sha256']=hashlib.sha256(data).hexdigest()
        validate_bundle(self.write_bundle())
        source.write_bytes(data+b'x');self.bundle['sources'][0]['sha256']=hashlib.sha256(data+b'x').hexdigest()
        with self.assertRaisesRegex(SemanticQualityError,'SIZE_LIMIT'):validate_bundle(self.write_bundle())

    def test_security_claim_key_rejects_validate(self):
        self.response['extensions']={'score':3};self.update_response()
        with self.assertRaisesRegex(SemanticQualityError,'PROHIBITED_FIELD'):validate_bundle(self.write_bundle())

    def test_extension_detail_preserves_four_outcomes(self):
        before=[(r['dimension'],r['outcome'],r['reason_code']) for r in self.profile()['rows']]
        self.response['extensions']={'helpful_detail':{'unrelated':['extra','visible']}}
        self.update_response()
        self.assertEqual(before,[(r['dimension'],r['outcome'],r['reason_code']) for r in self.profile()['rows']])

    def test_process_network_side_effect_sentinels(self):
        import socket, subprocess
        with patch.object(socket,'socket',side_effect=AssertionError('network forbidden')), patch.object(subprocess,'Popen',side_effect=AssertionError('process forbidden')):
            result=evaluate_bundle(self.write_bundle(),self.output())
            self.assertEqual(inspect_result(Path(result['profile_path']).parent)['status'],'INTACT')
    def test_repair_string_set_256_fact_and_observation_boundary(self):
        values=['value-%03d'%i for i in range(256)]
        self.bundle['facts'][0].update(value_type='STRING_SET',value=values)
        self.response['observations'][0].update(value_type='STRING_SET',value=values)
        self.assertEqual(self.dimensions()['SEMANTIC']['outcome'],'SATISFIED')
        self.response['observations'][0]['value']=values+['value-256']
        self.assertEqual(self.dimensions()['SEMANTIC']['reason_code'],'OBSERVED_VALUE_INVALID')
        self.bundle['facts'][0]['value']=values+['value-256']
        with self.assertRaisesRegex(SemanticQualityError,'INVALID_BUNDLE'):
            validate_bundle(self.write_bundle())

    def test_repair_manifest_nested_types_are_incomplete_before_missing(self):
        from copy import deepcopy
        result=evaluate_bundle(self.write_bundle(),self.output())
        root=Path(result['profile_path']).parent
        original=json.loads((root/'manifest.json').read_bytes())
        (root/'profile.json').unlink()
        changes=[('evaluation_id',[]),('fixture_class',None),('identity_sha256',17),('profile_row_count',True),('contract',[]),('asset_sha256',{}),('category_applicability',[]),('shape_diagnostics',[{'code':'x'}]),('rows',[{'dimension':'SEMANTIC'}]),('limitations',{})]
        for key,value in changes:
            with self.subTest(key=key):
                manifest=deepcopy(original);manifest[key]=value
                (root/'manifest.json').write_bytes(canon(manifest))
                self.assertEqual(inspect_result(root)['status'],'INCOMPLETE')
        manifest=deepcopy(original);manifest['rows'][0]['evidence_pointers']=[3]
        (root/'manifest.json').write_bytes(canon(manifest))
        self.assertEqual(inspect_result(root)['status'],'INCOMPLETE')
        (root/'manifest.json').write_bytes(canon(original))
        self.assertEqual(inspect_result(root)['status'],'MISSING')

    def test_repair_manifest_valid_but_changed_metadata_remains_mismatch(self):
        result=evaluate_bundle(self.write_bundle(),self.output());root=Path(result['profile_path']).parent
        manifest=json.loads((root/'manifest.json').read_bytes())
        manifest['evaluation_id']='ANOTHER-VALID-ID'
        (root/'manifest.json').write_bytes(canon(manifest))
        self.assertEqual(inspect_result(root)['status'],'MISMATCH')

    def test_repair_case_gap_validation_visits_each_mapping_once(self):
        import qa_master.semantic_quality as sq
        for count in (16,32,256):
            with self.subTest(count=count):
                self.response['cases']=[dict(self.complete_case(),case_id='CASE-'+str(i)) for i in range(count)]
                self.response['gaps']=[{'gap_id':'GAP-'+str(i),'obligation_ids':['OB-1'],'reason':'ORACLE_MISSING','fact_ids':['F-1'],'source_ids':['SRC-1'],'needed_evidence':'context','evidence_pointer':'source/rule.txt'} for i in range(count)]
                self.update_response();state=sq._validate_bundle(self.write_bundle());state['implementation_raw']=Path(sq.__file__).read_bytes()
                with patch.object(sq,'_gap_valid',wraps=sq._gap_valid) as gap_check, patch.object(sq,'_case_valid',wraps=sq._case_valid) as case_check:
                    profile=sq.derive_profile(state)
                self.assertEqual(gap_check.call_count,count)
                self.assertEqual(case_check.call_count,count)
                rows={r['dimension']:r for r in profile['rows']}
                self.assertEqual(rows['USABILITY']['outcome'],'SATISFIED')
                self.assertEqual(rows['PROVENANCE']['reason_code'],'SOURCE_BINDING_INVALID')
    def test_repair_installed_asset_failure_has_deriver_reason(self):
        result=evaluate_bundle(self.write_bundle(),self.output());root=Path(result['profile_path']).parent
        for code in ('CONTRACT_ASSET_MISSING','CONTRACT_BINDING_MISMATCH','INVALID_BUNDLE','DUPLICATE_JSON_KEY'):
            with self.subTest(code=code), patch('qa_master.semantic_quality.fixed_assets',side_effect=SemanticQualityError(code)):
                self.assertEqual(inspect_result(root),{'status':'MISMATCH','reason':'INSTALLED_DERIVER_MISMATCH'})
    def test_residual_fanout_item_lists_visited_once_independent_of_edges(self):
        import qa_master.semantic_quality as sq
        from copy import deepcopy
        original_ob=deepcopy(self.bundle['obligations'][0])
        normalizer=sq._normalize
        observations=[]
        for mode in ('case','gap_and_case'):
            counts=[]
            for count in (1,16,64):
                ids=['OB-'+str(i) for i in range(count)]
                self.bundle['obligations']=[dict(original_ob,id=oid,check_id='CHECK-'+str(i)) for i,oid in enumerate(ids)]
                self.response['observations']=[{'check_id':'CHECK-'+str(i),'value_type':'STRING','value':'yes','source_fact_ids':['F-1']} for i in range(count)]
                case=self.complete_case();case['obligation_ids']=ids
                self.response['cases']=[case];self.response['gaps']=[]
                if mode=='gap_and_case':
                    for ob in self.bundle['obligations']:
                        ob.update(oracle_state='ORACLE_MISSING',check_id=None,operator=None,expected_fact_ids=[],required_gap_reason='ORACLE_MISSING',allowed_readiness=['BLOCKED_ORACLE_MISSING'])
                    self.bundle['category_applicability'][1].update(state='ORACLE_MISSING',reason='missing oracle')
                    self.response['observations']=[]
                    case.update(readiness='BLOCKED_ORACLE_MISSING',missing_fields=['EXPECTED_ORACLE'],gap_ids=['GAP-MULTI'],expected_oracle={'state':'ORACLE_MISSING','items':[],'oracle_fact_ids':[],'reason':'oracle absent'})
                    self.response['gaps']=[{'gap_id':'GAP-MULTI','obligation_ids':ids,'reason':'ORACLE_MISSING','fact_ids':['F-1'],'source_ids':['SRC-1'],'needed_evidence':'oracle','evidence_pointer':'source/rule.txt'}]
                else:self.bundle['category_applicability'][1].update(state='APPLICABLE',reason=None)
                self.update_response();state=sq._validate_bundle(self.write_bundle());state['implementation_raw']=Path(sq.__file__).read_bytes()
                traversals=[]
                class WatchedList(list):
                    def __init__(self,values,label):super().__init__(values);self.label=label;self.visits=0;traversals.append(self)
                    def __iter__(self):self.visits+=len(self);return super().__iter__()
                def watch(value,label):
                    if isinstance(value,dict):
                        for key,child in list(value.items()):value[key]=watch(child,key)
                    elif isinstance(value,list):return WatchedList([watch(child,label) for child in value],label)
                    return value
                def normalized(value):
                    result=normalizer(value)
                    for channel in ('cases','gaps'):
                        for row in result['value'][channel]:watch(row,channel)
                    return result
                def edge_guard(function):
                    def guarded(*args):
                        before=[item.visits for item in traversals]
                        result=function(*args)
                        self.assertEqual(before,[item.visits for item in traversals],'edge traversed serialized item list')
                        return result
                    return guarded
                with patch.object(sq,'_normalize',side_effect=normalized), patch.object(sq,'_case_valid',side_effect=edge_guard(sq._case_valid)), patch.object(sq,'_gap_valid',side_effect=edge_guard(sq._gap_valid)), patch.object(sq,'_artifact_provenance',side_effect=edge_guard(sq._artifact_provenance)):
                    profile=sq.derive_profile(state)
                mapping_visits=sum(item.visits for item in traversals if item.label=='obligation_ids')
                other_visits=sum(item.visits for item in traversals if item.label!='obligation_ids')
                counts.append((count,mapping_visits,other_visits))
                self.assertEqual(len(profile['rows']),4*count)
                self.assertTrue(all(row['outcome']=='SATISFIED' for row in profile['rows'] if row['dimension']=='PROVENANCE'))
            self.assertEqual(len({visits//count for count,visits,_ in counts}),1)
            self.assertEqual(len({other for _,_,other in counts}),1)
            observations.append((mode,counts))
        print('ITEM_FANOUT_VISITS',observations)

    def test_residual_fanout_keeps_readiness_and_reference_dimensions_separate(self):
        from copy import deepcopy
        base=deepcopy(self.bundle['obligations'][0])
        self.bundle['obligations']=[dict(base,id='OB-'+str(i),check_id='CHECK-'+str(i),allowed_readiness=['STATIC_REVIEW'] if i==0 else ['DESIGN_READY']) for i in range(16)]
        self.response['observations']=[{'check_id':'CHECK-'+str(i),'value_type':'STRING','value':'yes','source_fact_ids':['F-1']} for i in range(16)]
        case=self.complete_case();case['obligation_ids']=['OB-'+str(i) for i in range(16)];self.response['cases']=[case]
        self.update_response();profile=self.profile()
        rows={(row['obligation_id'],row['dimension']):row for row in profile['rows']}
        self.assertEqual(rows['OB-0','USABILITY']['outcome'],'VIOLATED')
        self.assertEqual(rows['OB-1','USABILITY']['outcome'],'SATISFIED')
        self.assertTrue(all(row['outcome']=='SATISFIED' for row in profile['rows'] if row['dimension']=='PROVENANCE'))
        case['actions'][0]['source_fact_ids']=['UNKNOWN'];self.update_response();profile=self.profile()
        self.assertTrue(all(row['outcome']=='VIOLATED' for row in profile['rows'] if row['dimension']=='PROVENANCE'))
        self.assertTrue(all(row['outcome']=='SATISFIED' for row in profile['rows'] if row['dimension']=='SEMANTIC'))
    def test_residual_fanout_sibling_gap_binding_and_unknown_binding_isolation(self):
        base=dict(self.bundle['obligations'][0])
        self.bundle['obligations']=[dict(base,id='OB-0',check_id='CHECK-0'),dict(base,id='OB-1',check_id='CHECK-1')]
        self.response['observations']=[{'check_id':'CHECK-'+str(i),'value_type':'STRING','value':'yes','source_fact_ids':['F-1']} for i in range(2)]
        case=self.complete_case();case.update(obligation_ids=['OB-0','OB-1'],gap_ids=['GAP-0'])
        self.response['cases']=[case]
        self.response['gaps']=[{'gap_id':'GAP-0','obligation_ids':['OB-0'],'reason':'ORACLE_MISSING','fact_ids':['F-1'],'source_ids':['SRC-1'],'needed_evidence':'context','evidence_pointer':'source/rule.txt'}]
        self.update_response();rows={(r['obligation_id'],r['dimension']):r for r in self.profile()['rows']}
        self.assertEqual(rows['OB-0','USABILITY']['outcome'],'SATISFIED')
        self.assertEqual(rows['OB-1','USABILITY']['outcome'],'VIOLATED')
        case.update(obligation_ids=['OB-0','UNKNOWN'],gap_ids=[]);self.response['gaps']=[]
        self.update_response();rows={(r['obligation_id'],r['dimension']):r for r in self.profile()['rows']}
        self.assertEqual(rows['OB-0','PROVENANCE']['outcome'],'VIOLATED')
        self.assertEqual(rows['OB-1','PROVENANCE']['outcome'],'SATISFIED')
        self.assertEqual(rows['OB-1','USABILITY']['reason_code'],'CASE_NOT_REQUIRED')

    def test_residual_fanout_mixed_gap_reasons_preserve_global_content_rule(self):
        gap=self.missing_oracle();base=dict(self.bundle['obligations'][0])
        self.bundle['obligations']=[dict(base,id='OB-0'),dict(base,id='OB-1',oracle_state='UNSCORABLE',required_gap_reason='UNSUPPORTED_CATEGORY',allowed_readiness=['STATIC_REVIEW'])]
        self.bundle['category_applicability'][1].update(state='UNSCORABLE',reason='mixed source limits')
        gap['obligation_ids']=['OB-0','OB-1'];self.response['gaps']=[gap]
        self.update_response();rows={(r['obligation_id'],r['dimension']):r for r in self.profile()['rows']}
        self.assertEqual(rows['OB-0','PROVENANCE']['reason_code'],'REQUIRED_GAP_MISSING')
        self.assertEqual(rows['OB-1','PROVENANCE']['reason_code'],'SOURCE_BINDING_INVALID')
    def test_residual_fanout_duplicate_gap_cannot_bind_case(self):
        base=dict(self.bundle['obligations'][0]);self.bundle['obligations'].append(dict(base,id='OB-OTHER',check_id='CHECK-OTHER'))
        self.response['observations'].append({'check_id':'CHECK-OTHER','value_type':'STRING','value':'yes','source_fact_ids':['F-1']})
        case=self.complete_case();case['gap_ids']=['DUPLICATE'];self.response['cases']=[case]
        gap={'gap_id':'DUPLICATE','obligation_ids':['OB-1'],'reason':'ORACLE_MISSING','fact_ids':['F-1'],'source_ids':['SRC-1'],'needed_evidence':'context','evidence_pointer':'source/rule.txt'}
        self.response['gaps']=[gap,dict(gap)]
        self.update_response();rows={(r['obligation_id'],r['dimension']):r for r in self.profile()['rows']}
        self.assertEqual(rows['OB-1','USABILITY']['reason_code'],'OPTIONAL_CASE_INVALID')
        self.assertEqual(rows['OB-1','PROVENANCE']['outcome'],'VIOLATED')
        self.assertEqual(rows['OB-OTHER','PROVENANCE']['outcome'],'SATISFIED')

    def test_residual_preparation_does_not_assess_partial_fatal_channels(self):
        self.response['cases']=[self.complete_case()]
        self.response['gaps']=[{}]*257
        rows=self.dimensions()
        self.assertEqual(rows['SHAPE']['reason_code'],'MALFORMED_KNOWN_RESPONSE_FATAL')
        self.assertEqual(rows['USABILITY']['outcome'],'UNSCORABLE')
