"""Independent public-development fixtures from DES060v4, not developer tests."""
import copy
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from qa_master import semantic_quality as sq

CATEGORIES=['REQUIREMENTS_CONFLICTS','METHOD_SELECTION','FUNCTIONAL_API_INTEGRATION','SECURITY_SCOPE_AUTHORITY','RECOVERY_REGRESSION','NON_FUNCTIONAL','DELIVERABLE_USABILITY']
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x): return hashlib.sha256(x).hexdigest()

def fixture():
    assets=Path(sq.__file__).parent/'semantic_quality_assets'
    contract={}
    for key,name,ident in [('contract','contract.json','semantic-quality-v1'),('projection','projection.json','qa-quality-case-gap-v1'),('normalizer','normalizer.json','qa-quality-normalizer-v1'),('result_schema','result-schema.json','semantic-quality-result-v1'),('secret_scanner','secret-scanner.json','qa-quality-secret-scanner-v1')]:
        contract[key+'_id']=ident;contract[key+'_sha256']=sha((assets/name).read_bytes())
    facts=[];obs=[];cases=[];obligations=[];cats=[]
    # Visible domain rules beyond finite-method coverage: authority, recovery, SLA, deliverable policy.
    values=[('STRING','conflict recorded'),('STRING_SET',['boundary','decision']),('INTEGER',204),('BOOLEAN',False),('JSON',{'rollback':'previous','retain_data':True}),('DECIMAL','1.5'),('STRING','traceable draft')]
    for i,(category,(kind,value)) in enumerate(zip(CATEGORIES,values)):
        fid='F'+str(i);oid='O'+str(i);check='Q'+str(i)
        facts.append(dict(id=fid,source_ids=['S'],category=category,value_type=kind,value=value,scope='Published '+category+' policy'))
        obligations.append(dict(id=oid,category=category,interpretation='Compare published policy',source_ids=['S'],source_fact_ids=[fid],oracle_state='DETERMINATE',required_gap_reason=None,check_id=check,operator='EQUALS',expected_fact_ids=[fid],allowed_readiness=['DESIGN_READY'],case_required=True))
        cats.append(dict(category=category,state='APPLICABLE',reason=None,source_ids=['S'],fact_ids=[fid]))
        obs.append(dict(check_id=check,value_type=kind,value=value,source_fact_ids=[fid]))
        item=dict(text='Apply and inspect published policy',source_fact_ids=[fid])
        section=dict(state='DEFINED',items=[item],reason=None)
        cases.append(dict(case_id='C'+str(i),obligation_ids=[oid],category=category,readiness='DESIGN_READY',setup=copy.deepcopy(section),preconditions=[item],data=copy.deepcopy(section),actions=[item],expected_oracle=dict(state='DEFINED',items=[item],oracle_fact_ids=[fid],reason=None),cleanup=copy.deepcopy(section),source_fact_ids=[fid],gap_ids=[],missing_fields=['OBSERVABLE_LOCATOR','TARGET_INTERFACE'],extensions={}))
    response=dict(schema_version=1,artifact_id='A',artifact_state='DRAFT_UNAPPROVED',execution_state='NOT_EXECUTED',summary='Public development fixture',observations=obs,cases=cases,gaps=[],extensions={})
    bundle=dict(schema_version=1,evaluation_id='SQ-INDEPENDENT',fixture_class='PUBLIC_DEVELOPMENT',created_at_utc='2026-10-15T00:00:00Z',contract=contract,response={},sources=[dict(id='S',kind='requirement',state='AVAILABLE',locator='facts.txt',sha256=sha(b'Published policies; evaluator-authored development facts.'))],facts=facts,category_applicability=cats,obligations=obligations)
    return bundle,response

class SemanticIndependent(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='sq-independent-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.inputs=self.root/'inputs';self.inputs.mkdir();self.out=self.root/'outputs';self.n=0
        self.b,self.r=fixture();(self.inputs/'facts.txt').write_bytes(b'Published policies; evaluator-authored development facts.')
    def write(self,raw=None):
        raw=canonical(self.r) if raw is None else raw
        (self.inputs/'response.json').write_bytes(raw)
        self.b['response']=dict(state='PRESENT',source_path='response.json',byte_count=len(raw),sha256=sha(raw),declared_projection_id=self.b['contract']['projection_id'])
        p=self.inputs/'bundle.json';p.write_bytes(canonical(self.b));return p
    def run_profile(self,raw=None):
        self.n+=1;result=sq.evaluate_bundle(self.write(raw),self.out/str(self.n))
        p=Path(result['profile_path']);return json.loads(p.read_bytes()),p.parent
    def row(self,p,o,d):return next(x for x in p['rows'] if x['obligation_id']==o and x['dimension']==d)
    def expected(self,p,o,d,outcome,reason):
        row=self.row(p,o,d);self.assertEqual((row['outcome'],row['reason_code']),(outcome,reason));self.assertTrue(row['evidence_pointers'])
    def reject(self,code):
        rejected_output=self.root/'rejected-output'
        with self.assertRaises(sq.SemanticQualityError) as cm:sq.evaluate_bundle(self.inputs/'bundle.json',rejected_output)
        self.assertEqual(cm.exception.code,code);self.assertFalse(rejected_output.exists())
    def test_001_public_categories_four_rows(self):
        p,d=self.run_profile();self.assertEqual(len(p['rows']),28)
        self.assertEqual([(x['obligation_id'],x['dimension']) for x in p['rows']],[(f'O{i}',dim) for i in range(7) for dim in ['SHAPE','SEMANTIC','USABILITY','PROVENANCE']])
        self.assertTrue(all(x['outcome']=='SATISFIED' for x in p['rows']));self.assertEqual(sq.inspect_result(d)['status'],'INTACT')
    def test_002_cross_dimension_independence(self):
        self.r['observations'][0]['source_fact_ids']=['UNKNOWN'];p,_=self.run_profile()
        self.expected(p,'O0','SEMANTIC','SATISFIED','SOURCE_BOUND_VALUE_MATCH');self.expected(p,'O0','PROVENANCE','VIOLATED','SOURCE_BINDING_INVALID')
        self.r['observations'][0]['source_fact_ids']=['F0'];self.r['observations'][0]['value']='different';p,_=self.run_profile()
        self.expected(p,'O0','SEMANTIC','VIOLATED','OBSERVED_VALUE_MISMATCH');self.expected(p,'O0','PROVENANCE','SATISFIED','SOURCE_BINDING_COMPLETE')
        self.r['cases'][0]['readiness']='EXECUTABLE';p,_=self.run_profile();self.expected(p,'O0','USABILITY','VIOLATED','MAPPED_CASE_INVALID');self.expected(p,'O0','PROVENANCE','SATISFIED','SOURCE_BINDING_COMPLETE')
    def test_003_channels_are_independent(self):
        for channel,dim,reason in [('observations','SEMANTIC','OBSERVATIONS_CHANNEL_UNAVAILABLE'),('cases','USABILITY','CASES_CHANNEL_UNAVAILABLE')]:
            with self.subTest(channel=channel):
                self.b,self.r=fixture();self.r[channel]=None;p,_=self.run_profile()
                self.expected(p,'O0','SHAPE','VIOLATED','MALFORMED_KNOWN_RESPONSE_RECOVERABLE');self.expected(p,'O0',dim,'UNSCORABLE',reason)
                other='USABILITY' if dim=='SEMANTIC' else 'SEMANTIC';self.assertEqual(self.row(p,'O0',other)['outcome'],'SATISFIED')
    def test_004_fatal_recoverable_and_extensions(self):
        p,_=self.run_profile(b'{');self.expected(p,'O0','SHAPE','VIOLATED','MALFORMED_KNOWN_RESPONSE_FATAL');self.expected(p,'O0','SEMANTIC','UNSCORABLE','RESPONSE_SHAPE_DEPENDENCY')
        self.r['observations'][0]['extra']='detail';p,_=self.run_profile();self.expected(p,'O0','SHAPE','VIOLATED','MALFORMED_KNOWN_RESPONSE_RECOVERABLE');self.assertEqual(self.row(p,'O0','SEMANTIC')['outcome'],'SATISFIED')
        del self.r['observations'][0]['extra'];self.r['extensions']={'detail':['more','context']};p,_=self.run_profile();self.assertTrue(all(x['outcome']=='SATISFIED' for x in p['rows']))
    def test_005_duplicate_unknown_and_missing_observations(self):
        self.r['observations'].append(copy.deepcopy(self.r['observations'][0]));p,_=self.run_profile();self.expected(p,'O0','SEMANTIC','VIOLATED','OBSERVATION_AMBIGUOUS');self.assertEqual(self.row(p,'O1','SEMANTIC')['outcome'],'SATISFIED')
        self.r['observations']=[x for x in self.r['observations'] if x['check_id']!='Q0'];self.r['observations'].append(dict(check_id='UNKNOWN',value_type='BOOLEAN',value=True,source_fact_ids=['UNKNOWN']));p,_=self.run_profile();self.expected(p,'O0','SEMANTIC','VIOLATED','OBSERVATION_MISSING');self.assertEqual(self.row(p,'O1','PROVENANCE')['outcome'],'SATISFIED')
    def test_006_native_type_mismatch(self):
        self.r['observations'][3]['value']=0;p,_=self.run_profile();self.expected(p,'O3','SEMANTIC','VIOLATED','OBSERVED_VALUE_INVALID');self.assertEqual(self.row(p,'O3','PROVENANCE')['outcome'],'SATISFIED')
    def test_007_case_missing_content_and_optional(self):
        self.r['cases']=[];p,_=self.run_profile();self.expected(p,'O0','USABILITY','VIOLATED','REQUIRED_CASE_MISSING')
        self.b['obligations'][0]['case_required']=False;p,_=self.run_profile();self.expected(p,'O0','USABILITY','SATISFIED','CASE_NOT_REQUIRED')
        _,original=fixture();self.r['cases']=[original['cases'][0]];del self.r['cases'][0]['cleanup'];p,_=self.run_profile();self.expected(p,'O0','USABILITY','VIOLATED','OPTIONAL_CASE_INVALID');self.assertEqual(self.row(p,'O0','SHAPE')['outcome'],'SATISFIED')
    def missing_oracle(self):
        o=self.b['obligations'][5];o.update(oracle_state='ORACLE_MISSING',required_gap_reason='ORACLE_MISSING',check_id=None,operator=None,expected_fact_ids=[],allowed_readiness=['BLOCKED_ORACLE_MISSING'])
        self.b['category_applicability'][5].update(state='ORACLE_MISSING',reason='Inspected SLA scope lacks threshold')
        self.r['observations']=[x for x in self.r['observations'] if x['check_id']!='Q5'];self.r['cases']=[x for x in self.r['cases'] if x['case_id']!='C5']
        self.r['gaps']=[dict(gap_id='G5',obligation_ids=['O5'],reason='ORACLE_MISSING',fact_ids=['F5'],source_ids=['S'],needed_evidence='Published threshold',evidence_pointer='source:scope')]
    def test_008_missing_threshold_gap_honesty(self):
        self.missing_oracle();p,_=self.run_profile();self.expected(p,'O5','SEMANTIC','ORACLE_MISSING','SOURCE_ORACLE_MISSING');self.expected(p,'O5','USABILITY','ORACLE_MISSING','USABLE_ORACLE_UNAVAILABLE');self.expected(p,'O5','PROVENANCE','SATISFIED','MISSING_ORACLE_HONESTLY_REPORTED')
        self.r['gaps']=[];p,_=self.run_profile();self.expected(p,'O5','PROVENANCE','VIOLATED','REQUIRED_GAP_MISSING')
        self.r['gaps']=None;p,_=self.run_profile();self.expected(p,'O5','PROVENANCE','UNSCORABLE','PROVENANCE_CHANNEL_UNAVAILABLE')
    def test_009_oneof_duplicate_oracles_and_unknown_projection(self):
        f=copy.deepcopy(self.b['facts'][0]);f['id']='FX';self.b['facts'].append(f);self.b['obligations'][0].update(operator='ONE_OF',expected_fact_ids=['F0','FX']);self.write();self.reject('DUPLICATE_EXPECTED_VALUE')
        self.b,self.r=fixture();self.b['contract']['projection_id']='unknown';self.write();self.reject('UNKNOWN_PROJECTION')
    def test_010_input_drift_atomic(self):
        self.write();(self.inputs/'facts.txt').write_bytes(b'changed');
        with self.assertRaises(sq.SemanticQualityError):sq.evaluate_bundle(self.inputs/'bundle.json',self.out)
        self.assertFalse(self.out.exists())
    def test_011_inspect_mixed_precedence_and_readonly(self):
        p,d=self.run_profile();before={x.name:x.read_bytes() for x in d.iterdir() if x.is_file()};self.assertEqual(sq.inspect_result(d)['status'],'INTACT');self.assertEqual(before,{x.name:x.read_bytes() for x in d.iterdir() if x.is_file()})
        (d/'unexpected').write_text('extra');self.assertEqual(sq.inspect_result(d)['status'],'UNDECLARED')
        (d/'profile.json').write_bytes(b'{}');self.assertEqual(sq.inspect_result(d)['status'],'MISMATCH')
        (d/'profile.json').unlink();self.assertEqual(sq.inspect_result(d)['status'],'MISSING')
        (d/'reservation.json').write_bytes(b'{}');self.assertEqual(sq.inspect_result(d)['status'],'INCOMPLETE')
    def test_012_single_reservation_winner(self):
        path=self.write()
        def run(_):
            try:return sq.evaluate_bundle(path,self.out)['status']
            except sq.SemanticQualityError as e:return e.code
        with ThreadPoolExecutor(2) as pool:result=list(pool.map(run,range(2)))
        self.assertEqual(sorted(result),['EVALUATED_DRAFT_ONLY','RESULT_EXISTS']);dirs=[x for x in self.out.iterdir() if x.name.startswith('SQ-')];self.assertEqual(len(dirs),1);self.assertEqual(sq.inspect_result(dirs[0])['status'],'INTACT')
    def test_013_no_network_process_state(self):
        path=self.write();sentinel=self.root/'state.json';sentinel.write_bytes(b'UNTOUCHED')
        with patch.object(socket,'socket',side_effect=AssertionError('network')),patch.object(subprocess,'Popen',side_effect=AssertionError('process')),patch.object(os,'system',side_effect=AssertionError('shell')):
            sq.validate_bundle(path);result=sq.evaluate_bundle(path,self.out);sq.inspect_result(Path(result['profile_path']).parent)
        self.assertEqual(sentinel.read_bytes(),b'UNTOUCHED')
    def test_014_known_legacy_and_absent(self):
        assets=Path(sq.__file__).parent/'semantic_quality_assets';self.b['contract'].update(projection_id='paired-neutral-envelope-v1',projection_sha256=sha((assets/'legacy-paired-projection.json').read_bytes()));p,_=self.run_profile();self.assertTrue(all(x['outcome']=='UNSCORABLE' and x['reason_code']=='LEGACY_PROJECTION_UNSUPPORTED' for x in p['rows']))
        self.b,self.r=fixture();self.write();self.b['response'].update(state='ABSENT',source_path=None,byte_count=None,sha256=None);(self.inputs/'bundle.json').write_bytes(canonical(self.b));result=sq.evaluate_bundle(self.inputs/'bundle.json',self.out/'absent');p=json.loads(Path(result['profile_path']).read_bytes());self.assertTrue(all(x['reason_code']=='RESPONSE_ABSENT' for x in p['rows']))

    def test_015_oneof_success_and_nonapplicable(self):
        f=copy.deepcopy(self.b['facts'][0]);f.update(id='FX',value='alternate');self.b['facts'].append(f);self.b['obligations'][0].update(operator='ONE_OF',expected_fact_ids=['F0','FX']);self.b['category_applicability'][0]['fact_ids']=['F0','FX'];self.r['observations'][0]['value']='alternate';p,_=self.run_profile();self.expected(p,'O0','SEMANTIC','SATISFIED','SOURCE_BOUND_VALUE_MATCH')
        self.b,self.r=fixture();self.b['obligations'].pop();self.b['category_applicability'][-1].update(state='NOT_APPLICABLE',reason='No deliverable contract requested');self.r['observations'].pop();self.r['cases'].pop();p,_=self.run_profile();self.assertEqual(len(p['rows']),24);self.assertEqual(p['category_applicability'][-1]['state'],'NOT_APPLICABLE')
    def test_016_conflict_and_unavailable_source(self):
        o=self.b['obligations'][0];f=copy.deepcopy(self.b['facts'][0]);f.update(id='FX',value='contradiction',source_ids=['S2']);self.b['facts'].append(f)
        self.b['sources'].append(dict(id='S2',kind='requirement',state='AVAILABLE',locator='facts.txt',sha256=self.b['sources'][0]['sha256']))
        o.update(oracle_state='CONFLICT',required_gap_reason='CONFLICT',source_ids=['S','S2'],source_fact_ids=['F0','FX'],expected_fact_ids=['F0','FX'],check_id=None,operator=None)
        self.b['category_applicability'][0].update(state='UNSCORABLE',reason='Sources disagree',source_ids=['S','S2'],fact_ids=['F0','FX'])
        self.r['cases'].pop(0);self.r['observations'].pop(0);self.r['gaps']=[dict(gap_id='G',obligation_ids=['O0'],reason='CONFLICT',fact_ids=['F0','FX'],source_ids=['S','S2'],needed_evidence='Resolve conflict',evidence_pointer='source:conflict')]
        p,_=self.run_profile();self.expected(p,'O0','SEMANTIC','UNSCORABLE','SOURCE_FACT_CONFLICT');self.expected(p,'O0','PROVENANCE','SATISFIED','CONFLICT_HONESTLY_REPORTED')
        self.b,self.r=fixture();self.b['sources'].append(dict(id='M',kind='requirement',state='NOT_AVAILABLE',locator=None,sha256=None));self.b['obligations'][0].update(oracle_state='UNSCORABLE',required_gap_reason='SOURCE_MISSING',source_ids=['M','S'],check_id=None,operator=None,expected_fact_ids=[]);self.b['category_applicability'][0].update(state='UNSCORABLE',reason='Source unavailable',source_ids=['M','S']);self.r['cases'].pop(0);self.r['observations'].pop(0);self.r['gaps']=[dict(gap_id='G',obligation_ids=['O0'],reason='SOURCE_MISSING',fact_ids=['F0'],source_ids=['M','S'],needed_evidence='Missing source',evidence_pointer='source:missing')]
        p,_=self.run_profile();self.expected(p,'O0','PROVENANCE','SATISFIED','UNSCORABLE_GAP_HONESTLY_REPORTED')
    def test_017_typed_and_document_limits(self):
        self.b['facts'][2]['value']=10**34-1;self.r['observations'][2]['value']=10**34-1;p,_=self.run_profile();self.assertEqual(self.row(p,'O2','SEMANTIC')['outcome'],'SATISFIED')
        self.b['facts'][2]['value']=10**34;self.write();self.reject('COUNT_LIMIT')
        self.b,self.r=fixture()
        for i in range(7,256):
            f=copy.deepcopy(self.b['facts'][0]);f['id']='F'+str(i);self.b['facts'].append(f)
        sq.validate_bundle(self.write());f=copy.deepcopy(self.b['facts'][0]);f['id']='F256';self.b['facts'].append(f);self.write();self.reject('COUNT_LIMIT')
        self.b,self.r=fixture();path=self.write();path.write_bytes(b' '*(2*1024*1024+1));self.reject('SIZE_LIMIT')
    def test_018_joint_profile_manifest_forgery(self):
        p,d=self.run_profile();p['rows'][0]['outcome']='VIOLATED';raw=canonical(p);(d/'profile.json').write_bytes(raw)
        m=json.loads((d/'manifest.json').read_bytes());m['rows']=p['rows'];m['profile_sha256']=sha(raw)
        for f in m['files']:
            if f['path']=='profile.json':f.update(sha256=sha(raw),byte_count=len(raw))
        (d/'manifest.json').write_bytes(canonical(m));result=sq.inspect_result(d);self.assertEqual(result['status'],'MISMATCH');self.assertIn('PROFILE_DERIVATION_MISMATCH',json.dumps(result))
    def test_019_publish_failure_preserves_unrelated(self):
        path=self.write();self.out.mkdir();(self.out/'unrelated').write_bytes(b'KEEP')
        with patch.object(os,'replace',side_effect=OSError('injected commit fault')):
            with self.assertRaises(sq.SemanticQualityError) as cm:sq.evaluate_bundle(path,self.out)
        self.assertEqual(cm.exception.code,'LOCAL_IO_FAILURE');self.assertEqual((self.out/'unrelated').read_bytes(),b'KEEP');self.assertFalse(any(x.name.startswith('SQ-') for x in self.out.iterdir()))

    def test_020_json_depth_nodes_and_case_limit(self):
        for depth,ok in [(16,True),(17,False)]:
            self.b,self.r=fixture();v=0
            for _ in range(depth):v=[v]
            self.b['facts'][4]['value']=v;self.r['observations'][4]['value']=v
            if ok:sq.validate_bundle(self.write())
            else:self.write();self.reject('INVALID_BUNDLE')
        for nodes,ok in [(4096,True),(4097,False)]:
            self.b,self.r=fixture();self.b['facts'][4]['value']=[0]*(nodes-1);self.r['observations'][4]['value']=[0]*(nodes-1)
            if ok:sq.validate_bundle(self.write())
            else:self.write();self.reject('INVALID_BUNDLE')
        self.b,self.r=fixture()
        for i in range(7,256):
            c=copy.deepcopy(self.r['cases'][0]);c['case_id']='C'+str(i);self.r['cases'].append(c)
        p,_=self.run_profile();self.assertEqual(self.row(p,'O0','USABILITY')['outcome'],'SATISFIED')
        c=copy.deepcopy(self.r['cases'][0]);c['case_id']='C256';self.r['cases'].append(c);p,_=self.run_profile();self.expected(p,'O0','SHAPE','VIOLATED','MALFORMED_KNOWN_RESPONSE_FATAL')

    def test_021_string_set_fact_256_257(self):
        self.b['facts'][1]['value']=[f'v{i:03}' for i in range(256)];self.r['observations'][1]['value']=self.b['facts'][1]['value'];sq.validate_bundle(self.write())
        self.b['facts'][1]['value']=[f'v{i:03}' for i in range(257)];self.write()
        with self.assertRaises(sq.SemanticQualityError):sq.validate_bundle(self.inputs/'bundle.json')
    def test_022_string_set_observation_257_invalid(self):
        self.r['observations'][1]['value']=[f'v{i:03}' for i in range(257)];p,_=self.run_profile();self.expected(p,'O1','SEMANTIC','VIOLATED','OBSERVED_VALUE_INVALID')
    def test_023_malformed_manifest_is_incomplete(self):
        _,d=self.run_profile();m=json.loads((d/'manifest.json').read_bytes());m['evaluation_id']=[];(d/'manifest.json').write_bytes(canonical(m));self.assertEqual(sq.inspect_result(d)['status'],'INCOMPLETE')

    def test_024_fanout_validation_once_per_mapped_artifact(self):
        counts=[]
        for n in (4,8,16):
            self.b,self.r=fixture();original=self.r['cases'][0];self.r['cases']=[]
            for i in range(n):
                c=copy.deepcopy(original);c['case_id']='CX'+str(i);self.r['cases'].append(c)
            self.r['gaps']=[dict(gap_id='G'+str(i),obligation_ids=['O0'],reason='ORACLE_MISSING',fact_ids=['F0'],source_ids=['S'],needed_evidence='Review gap',evidence_pointer='source:scope') for i in range(n)]
            with patch.object(sq,'_gap_valid',wraps=sq._gap_valid) as gaps,patch.object(sq,'_case_valid',wraps=sq._case_valid) as cases:self.run_profile()
            counts.append((n,gaps.call_count,cases.call_count));self.assertEqual((gaps.call_count,cases.call_count),(n,n))
        self.assertEqual(counts,[(4,4,4),(8,8,8),(16,16,16)])
    def test_025_manifest_types_enums_and_precedence(self):
        _,d=self.run_profile();original=json.loads((d/'manifest.json').read_bytes())
        edits=[lambda m:m.update(evaluation_id=[]),lambda m:m.update(profile_row_count=True),lambda m:m['contract'].update(contract_sha256=[]),lambda m:m['rows'][0].update(outcome='PASS'),lambda m:m['rows'][0].update(evidence_pointers=None),lambda m:m['category_applicability'][0].update(state='UNKNOWN'),lambda m:m['files'][0].update(role='UNKNOWN'),lambda m:m.update(limitations={}),lambda m:m.pop('contract')]
        for i,edit in enumerate(edits):
            with self.subTest(mutation=i):
                m=copy.deepcopy(original);edit(m);(d/'manifest.json').write_bytes(canonical(m));self.assertEqual(sq.inspect_result(d)['status'],'INCOMPLETE')
        (d/'unexpected').write_bytes(b'extra');(d/'profile.json').unlink();m=copy.deepcopy(original);m['evaluation_id']=[];(d/'manifest.json').write_bytes(canonical(m));self.assertEqual(sq.inspect_result(d)['status'],'INCOMPLETE')
    def test_026_installed_deriver_mismatch(self):
        _,d=self.run_profile();altered=self.root/'other-evaluator.py';altered.write_bytes(Path(sq.__file__).read_bytes()+b'\n# different bytes\n')
        with patch.object(sq,'__file__',str(altered)):
            result=sq.inspect_result(d)
        self.assertEqual(result['status'],'MISMATCH');self.assertIn('INSTALLED_DERIVER_MISMATCH',json.dumps(result))

    def test_027_case_wide_reference_validation_independent_of_mapping_count(self):
        visits=[]
        for n in (4,64):
            self.b,self.r=fixture();base=self.b['obligations'].pop(0);observation=self.r['observations'].pop(0);ids=[f'X{i:02}' for i in range(n)]
            for i,oid in enumerate(ids):
                ob=copy.deepcopy(base);ob.update(id=oid,check_id='CHECK'+str(i));self.b['obligations'].append(ob)
                obs=copy.deepcopy(observation);obs['check_id']='CHECK'+str(i);self.r['observations'].append(obs)
            self.r['cases'][0]['obligation_ids']=ids
            original=sq._valid_refs;count=[0]
            def observe(value):
                if value==ids:count[0]+=1
                return original(value)
            with patch.object(sq,'_valid_refs',side_effect=observe):self.run_profile()
            visits.append(count[0])
        self.assertEqual(visits[0],visits[1], 'Case-wide list validity must be cached independently of mapping count')
