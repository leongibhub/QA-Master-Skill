"""Independent DES-040 acceptance fixtures; never invokes a model."""
import copy
import hashlib
import io
import json
import os
import platform
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from qa_master import paired_evaluation as pe
from qa_master import _paired_process as process
from qa_master._paired_contract import (PROMPT_TEMPLATE_V1, NEUTRAL_RESPONSE_SCHEMA_V1,
    DISABLED_FEATURES, ISOLATION, PairedEvaluationError, LIMIT)


def packed(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Fixture:
    def __init__(self, base):
        self.executable=Path(sys.executable).resolve(strict=True)
        self.base=Path(base); self.inputs=self.base/'inputs'; self.inputs.mkdir()
        self.manifest_path=self.inputs/'manifest.json'; self.exclusions=self.base/'excluded.json'
        exclusion={'schema_version':1,'forbidden_locators':['holdout/private.json'],'forbidden_sha256':[],'fixture_markers':['EVALUATOR_PRIVATE_12345']}
        self.exclusions.write_bytes(packed(exclusion))
        self.visible={}; participants=[]
        for arm in ('A','B'):
            asset=self.source(f'{arm}.md',f'Independent participant {arm} marker ARM_{arm}_VISIBLE_ONLY. {{'+'{VISIBLE_INPUT}} must stay literal.')
            asset.update(path='skills/entry.md',media_type='text/markdown')
            participants.append({'arm_id':arm,'participant_id':'participant-'+arm,'source':{'repository_id':'repo-'+arm,'commit':'a'*40,'tree_oid':'b'*40},'entry_asset':'skills/entry.md','assets':[asset]})
        scenarios=[]
        for number,method in enumerate(('boundary','decision_table','state_transition')):
            sid='SC-'+str(number)
            value={'schema_version':1,'scenario_id':sid,'method':method,'title':'Independent '+method,'request':'Describe test cases without execution.','known_facts':[{'id':'F-1','text':'The observable integer is seven.'}],'scope':'finite local design','checks':[{'id':'Q-1','question':'Which integer?','value_type':'INTEGER'},{'id':'Q-2','question':'Is the feature declared?','value_type':'BOOLEAN'},{'id':'Q-3','question':'What string?','value_type':'STRING'}]}
            self.visible[sid]=value
            scenarios.append({'id':sid,'method':method,'visible_input':self.source(sid+'.json',packed(value)),'oracle_commitment_sha256':sha(b'independent oracle commitment')})
        self.manifest={'schema_version':1,'run_id':'INDEPENDENT-RUN','profile':'EXPLORATORY_CONFIGURED_SAME_MODEL','created_at_utc':'2026-10-15T00:00:00Z','participants':participants,'scenarios':scenarios,'prompt_template':self.source('prompt.txt',PROMPT_TEMPLATE_V1),'response_schema':self.source('schema.json',NEUTRAL_RESPONSE_SCHEMA_V1),'evaluator_commitment_sha256':sha(packed(exclusion)),
        'runtime':{'codex':{'executable_path':str(self.executable),'executable_sha256':sha(self.executable.read_bytes()),'version':'INDEPENDENT-TEST-NATIVE-PYTHON-NOT-CODEX'},'model':{'alias':'test-model','reasoning_effort':'medium','provider_revision':{'state':'NOT_AVAILABLE','value':None,'evidence_sha256':None},'system_baseline':{'state':'UNVERIFIED','value':None,'evidence_sha256':None},'temperature_state':'NOT_AVAILABLE','seed_state':'NOT_AVAILABLE'},'policy':{'sandbox':'read-only','add_dirs':[],'ignore_user_config':True,'ephemeral':True,'skip_host_skill_discovery':True,'requested_tool_policy':'NO_TOOL_USE','disabled_features':DISABLED_FEATURES,'isolation_level':ISOLATION},'host':{'os':platform.system(),'architecture':platform.machine()},'timeout_seconds':1,'retry_count':0},
        'schedule':[{'attempt_id':'PAIR-'+str(i),'scenario_id':'SC-'+str(i),'order':['A','B'] if i!=1 else ['B','A']} for i in range(3)]}
        self.save()

    def source(self,name,raw):
        if isinstance(raw,str):raw=raw.encode('utf-8')
        (self.inputs/name).write_bytes(raw)
        return {'source_path':name,'byte_count':len(raw),'sha256':sha(raw)}

    def save(self):self.manifest_path.write_bytes(packed(self.manifest))

    def run(self,launcher,output='runs'):
        self.save();return pe._run_pair_with_ports(self.manifest_path,self.exclusions,self.base/output,launcher=launcher)

    def envelope(self,sid,**updates):
        value={'schema_version':1,'scenario_id':sid,'response_status':'COMPLETED','summary':'Independent plain-language response.','cases':[],'gaps':[],'observations':[{'check_id':'Q-1','value_type':'INTEGER','value':7,'evidence_refs':['F-1']}],'metadata':{'artifact_state':'DRAFT','execution_state':'NOT_EXECUTED'},'failure_reason':None}
        value.update(updates);return value


def trace(final,warning=True):
    rows=[{'type':'thread.started','thread_id':'independent-thread'}]
    if warning: rows.append({'type':'item.completed','item':{'id':'warn','type':'error','message':'skip_host_skill_discovery is under development'}})
    rows.extend([{'type':'turn.started'},{'type':'item.completed','item':{'id':'message','type':'agent_message','text':final.decode('utf-8')}},{'type':'turn.completed','usage':dict.fromkeys(['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens'],0)}])
    return b'\n'.join(packed(row) for row in rows)+b'\n'


def capture(final,prompt,**changes):
    value={'process_outcome':'EXITED_ZERO','termination_outcome':'NOT_REQUESTED','termination':None,'exit_code':0,'pid':987,'cleanup_outcome':'DELETED','environment':{'policy_id':'TEST_ONLY','inherited_names':[]},'duration_ms':1,'command':['TEST_DOUBLE'],'stdin_outcome':'SENT_COMPLETE','stdin_bytes_sent':len(prompt),'stream_observations':{},'stdout':trace(final),'stderr':b'PowerShell shell snapshot unavailable\n','final':final,'integrity_failure':False}
    value.update(changes);return value


class PairedRuntimeIndependent(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.f=Fixture(self.temp.name)

    def launcher(self,**kw):
        sid=next(sid for sid in self.f.visible if ('"scenario_id":"'+sid+'"').encode() in kw['prompt'])
        return capture(packed(self.f.envelope(sid)),kw['prompt'])

    def valid(self):return pe.validate_run_manifest(packed(self.f.manifest),manifest_dir=self.f.inputs)

    def test_tc_pe_201_manifest_strict_and_malformed_types_no_spawn(self):
        with patch.object(subprocess,'Popen',side_effect=AssertionError('spawn forbidden')):
            self.assertEqual(self.valid()['status'],'VALIDATED_NOT_EXECUTED')
            for raw,code in [(b'{"a":1,"a":2}','DUPLICATE_JSON_KEY'),(b'{"a":NaN}','NON_INTEGER_JSON_NUMBER'),(b'{"a":1.2}','NON_INTEGER_JSON_NUMBER'),(b'\xff','INVALID_JSON')]:
                with self.subTest(code=code),self.assertRaisesRegex(PairedEvaluationError,'^'+code+'$'):pe.load_run_manifest(raw,manifest_dir=self.f.inputs)
            original=copy.deepcopy(self.f.manifest)
            for path,val in [(('extra',),1),(('runtime','retry_count'),1),(('runtime','timeout_seconds'),0),(('runtime','timeout_seconds'),1801),(('participants',),[]),(('schedule',),{}),(('runtime','model','alias'),[])]:
                self.f.manifest=copy.deepcopy(original);obj=self.f.manifest
                for part in path[:-1]:obj=obj[part]
                obj[path[-1]]=val
                with self.subTest(path=path,val=val),self.assertRaises(PairedEvaluationError):self.valid()
            self.f.manifest=original;self.f.manifest['runtime']['timeout_seconds']=1800;self.valid()

    def test_tc_pe_202_source_drift_and_paths(self):
        with patch.object(subprocess,'Popen',side_effect=AssertionError('spawn forbidden')):
            source=self.f.inputs/'A.md';initial=source.read_bytes();source.write_bytes(initial+b'!')
            with self.assertRaisesRegex(PairedEvaluationError,'SOURCE_INTEGRITY_FAILURE'):self.valid()
            source.write_bytes(initial)
            asset=self.f.manifest['participants'][0]['assets'][0]
            for name in ('../escape','/absolute','C:/drive','a\\b','a//b','https://x','x?y','NUL','x.'):
                asset['path']=name
                with self.subTest(name=name),self.assertRaisesRegex(PairedEvaluationError,'INVALID_PATH'):self.valid()
            asset['path']='skills/entry.md'
            self.f.manifest['runtime']['codex']['executable_sha256']='0'*64
            with self.assertRaisesRegex(PairedEvaluationError,'EXECUTABLE_DRIFT'):self.valid()

    def test_tc_pe_203_counts_sizes_and_declared_capacity(self):
        p=self.f.manifest['participants'][0]; original=p['assets'][0]
        p['assets']=[dict(original,path=f'a{i:02}.md') for i in range(64)];p['entry_asset']='a00.md';self.valid()
        p['assets'].append(dict(original,path='a64.md'))
        with self.assertRaisesRegex(PairedEvaluationError,'INVALID_ARRAY'):self.valid()
        p['assets']=[dict(original,path='skills/entry.md')];p['entry_asset']='skills/entry.md'
        desc=self.f.source('large.txt',b'x'*LIMIT);desc.update(path='skills/entry.md',media_type='text/plain');p['assets']=[desc];self.valid()
        extra=self.f.source('extra.txt',b'x');extra.update(path='z.txt',media_type='text/plain');p['assets'].append(extra)
        with self.assertRaisesRegex(PairedEvaluationError,'ASSET_TOTAL_LIMIT'):self.valid()
        p['assets']=[dict(self.f.source('large.txt',b'x'*(LIMIT+1)),path='skills/entry.md',media_type='text/plain')]
        with self.assertRaises(PairedEvaluationError):self.valid()

    def test_tc_pe_204_materialization_prompt_inventory_and_noexec(self):
        with patch.object(subprocess,'Popen',side_effect=AssertionError('spawn forbidden')):
            preview=self.f.base/'preview'; result=pe.materialize_preview(self.f.manifest_path,self.f.exclusions,preview)
            self.assertEqual(result['call_count'],6);self.assertEqual(result['status'],'PREVIEW_NOT_RUN')
            for i in range(3):
                a=preview/f'calls/PAIR-{i}-A'; b=preview/f'calls/PAIR-{i}-B'
                self.assertEqual((a/'common/visible-input.json').read_bytes(),(b/'common/visible-input.json').read_bytes())
                self.assertEqual((a/'common/response.schema.json').read_bytes(),(b/'common/response.schema.json').read_bytes())
                for arm,root in [('A',a),('B',b)]:
                    prompt=(root/'stdin.txt').read_bytes();self.assertIn(('ARM_'+arm+'_VISIBLE_ONLY').encode(),prompt);self.assertNotIn(('ARM_'+('B' if arm=='A' else 'A')+'_VISIBLE_ONLY').encode(),prompt)
                    self.assertIn(b'{{VISIBLE_INPUT}} must stay literal',prompt)
                    self.assertEqual([x.relative_to(root/'assets').as_posix() for x in (root/'assets').rglob('*') if x.is_file()],['skills/entry.md'])
            self.assertEqual(pe.inspect_run(preview)['completion'],'INCOMPLETE')
            with self.assertRaisesRegex(PairedEvaluationError,'RUN_ID_EXISTS'):pe.materialize_preview(self.f.manifest_path,self.f.exclusions,preview)

    def test_tc_pe_205_evaluator_leakage_before_process_or_root(self):
        for marker in ('EVALUATOR_PRIVATE_12345','holdout/private.json'):
            self.f.manifest['participants'][0]['assets'][0].update(self.f.source('A.md',marker));self.f.save()
            with patch.object(subprocess,'Popen',side_effect=AssertionError('spawn forbidden')),self.assertRaisesRegex(PairedEvaluationError,'EVALUATOR_LEAKAGE'):
                pe.materialize_preview(self.f.manifest_path,self.f.exclusions,self.f.base/'preview')
            self.assertFalse((self.f.base/'preview').exists())

    def test_tc_pe_206_exact_six_capture_order_and_no_pilot_promotion(self):
        prompts=[]
        def launch(**kw):prompts.append(kw);return self.launcher(**kw)
        r=self.f.run(launch)
        self.assertEqual([a['call_id'] for a in r['attempts']],['PAIR-0-A','PAIR-0-B','PAIR-1-B','PAIR-1-A','PAIR-2-A','PAIR-2-B'])
        self.assertEqual(len(prompts),6);self.assertEqual((r['execution_backend'],r['evidence_class'],r['pilot_status']),('TEST_DOUBLE','TEST_DOUBLE','NOT_EXECUTED'))
        self.assertEqual({a['terminal_status'] for a in r['attempts']},{'COMPLETED_PROCESS'});self.assertEqual({a['trace_warning_count'] for a in r['attempts']},{1})
        self.assertEqual(r['claim_status'],'NOT_ASSERTED');self.assertEqual(r['human_rating_status'],'NOT_EXECUTED')
        self.assertEqual(pe.inspect_run(self.f.base/'runs/INDEPENDENT-RUN')['status'],'INTACT')
        for entry in r['ledger']:
            if entry['capture_state']=='RETAINED':
                raw=(self.f.base/'runs/INDEPENDENT-RUN'/entry['relative_path']).read_bytes();self.assertEqual((len(raw),sha(raw)),(entry['byte_count'],entry['sha256']))

    def test_tc_pe_207_failure_priority_and_schedule(self):
        variants=[('nonzero',{'process_outcome':'EXITED_NONZERO','exit_code':9},'RUN_FAILURE_UNATTRIBUTED',6),('missingfinal',{'final':None},'OUTPUT_INVALID',6),('badtrace',{'stdout':b'bad\n'},'OUTPUT_INVALID',6),('timeout',{'process_outcome':'TIMED_OUT','termination_outcome':'TERMINATION_OBSERVED','exit_code':-1},'TIMED_OUT',6),('unconfirmed',{'process_outcome':'TIMED_OUT','termination_outcome':'TERMINATION_UNCONFIRMED','exit_code':None},'TIMED_OUT',1),('spawn',{'process_outcome':'SPAWN_FAILED','stdout':None,'final':None,'exit_code':None},'INFRASTRUCTURE_FAILURE',1),('integrity',{'integrity_failure':True},'INFRASTRUCTURE_FAILURE',1)]
        for name,changes,terminal,count in variants:
            calls=[]
            def launch(**kw):
                result=self.launcher(**kw);calls.append(kw)
                if len(calls)==1:result.update(changes)
                return result
            with self.subTest(name=name):
                r=self.f.run(launch,name);a=r['attempts'][0];self.assertEqual(a['terminal_status'],terminal);self.assertEqual(len(calls),count)
                for key in ('process_outcome','termination_outcome'):
                    if key in changes:self.assertEqual(a[key],changes[key])
                if count==1:self.assertEqual([x['terminal_status'] for x in r['attempts'][1:]],['NOT_EXECUTED']*5)
                if name=='missingfinal':self.assertEqual(a['output_outcome'],'NOT_AVAILABLE')

    def test_tc_pe_208_policy_redaction_and_partial_input_stop(self):
        for name in ('tool','secret','partial'):
            calls=[]
            def launch(**kw):
                r=self.launcher(**kw);calls.append(kw)
                if name=='tool':r['stdout']=packed({'type':'item.started','item':{'type':'command_execution','command':'not-run'}})+b'\n'+r['stdout']
                elif name=='secret':r['stderr']=b'Authorization: Bearer SYNTHETIC_SECRET_123456'
                else:r['stdin_outcome']='PARTIAL';r['stdin_bytes_sent']=1
                return r
            r=self.f.run(launch,name);a=r['attempts'][0];self.assertEqual(len(calls),1)
            self.assertEqual(a['terminal_status'],'POLICY_VIOLATION' if name=='tool' else 'INFRASTRUCTURE_FAILURE')
            self.assertEqual(a['process_outcome'],'EXITED_ZERO')
            if name=='secret':
                entry=next(e for e in a['ledger'] if e['role']=='stderr');self.assertEqual(entry['capture_state'],'REDACTED');self.assertEqual(entry['redaction']['original_sha256'],sha(b'Authorization: Bearer SYNTHETIC_SECRET_123456'))
                for path in (self.f.base/name).rglob('*'):
                    if path.is_file():self.assertNotIn(b'SYNTHETIC_SECRET_123456',path.read_bytes())

    def test_tc_pe_209_typed_grade_keyword_missing_and_binding(self):
        r=self.f.run(self.launcher);root=self.f.base/'runs/INDEPENDENT-RUN'
        base={'schema_version':1,'run_manifest_sha256':r['run_manifest_sha256'],'response_schema_sha256':r['response_schema_sha256'],'assertions':[]}
        for i,expected in enumerate([{'value_type':'INTEGER','value':7},{'value_type':'BOOLEAN','value':True},{'value_type':'STRING','value':'7'}]):
            base['assertions'].append({'id':f'AS-{i}','scenario_id':'SC-0','check_id':'Q-1','expected':expected,'required_evidence_refs':['F-1'],'oracle_ref':'oracle/opaque-not-a-file'})
        base['assertions'].append({'id':'AS-MISSING','scenario_id':'SC-0','check_id':'Q-2','expected':{'value_type':'BOOLEAN','value':True},'required_evidence_refs':[],'oracle_ref':'oracle/opaque'})
        path=self.f.base/'assertions.json';path.write_bytes(packed(base))
        with patch.object(subprocess,'Popen',side_effect=AssertionError('spawn forbidden')):
            report=pe.grade_run(root,path,self.f.base/'grade.json')
        self.assertEqual([a['status'] for a in report['assertions']],['SATISFIED','VIOLATED','VIOLATED','UNSCORABLE']*2)
        base['assertions'][0]['check_id']='UNKNOWN';path.write_bytes(packed(base))
        with self.assertRaisesRegex(PairedEvaluationError,'UNKNOWN_ASSERTION_BINDING'):pe.grade_run(root,path,self.f.base/'bad-grade.json')
        self.assertFalse((self.f.base/'bad-grade.json').exists())

    def test_tc_pe_210_inspect_detects_mutation_and_undeclared(self):
        self.f.run(self.launcher);root=self.f.base/'runs/INDEPENDENT-RUN'
        extra=root/'undeclared.txt';extra.write_bytes(b'x');self.assertIn('UNDECLARED',[r['status'] for r in pe.inspect_run(root)['artifacts']]);extra.unlink()
        file=root/'calls/PAIR-0-A/assets/skills/entry.md';file.write_bytes(b'drift')
        self.assertEqual(pe.inspect_run(root)['status'],'INTEGRITY_FAILURE')

    def test_tc_pe_211_attestation_claim_and_fixed_contract_reject(self):
        original=copy.deepcopy(self.f.manifest)
        for change,code in [('strict','STRICT_PROFILE_NOT_SUPPORTED'),('verified','ATTESTATION_NOT_SUPPORTED'),('contract','COMMON_CONTRACT_MISMATCH'),('claim','INVALID_MEMBERS')]:
            self.f.manifest=copy.deepcopy(original)
            if change=='strict':self.f.manifest['profile']='STRICT_COMPARISON_CANDIDATE'
            elif change=='verified':self.f.manifest['runtime']['model']['provider_revision']['state']='VERIFIED'
            elif change=='contract':self.f.manifest['prompt_template']=self.f.source('other.txt',b'Caller-supplied prompt')
            else:self.f.manifest['winner']='A'
            with self.subTest(change=change),self.assertRaisesRegex(PairedEvaluationError,code):self.valid()

    def test_tc_pe_212_cli_nonexecute_and_no_secret_echo(self):
        with patch.object(subprocess,'Popen',side_effect=AssertionError('spawn forbidden')):
            for args in [['validate',str(self.f.manifest_path)],['materialize',str(self.f.manifest_path),'--exclusions',str(self.f.exclusions),'--output',str(self.f.base/'preview')],['inspect',str(self.f.base/'preview')]]:
                with redirect_stdout(io.StringIO()) as output:self.assertEqual(pe.main(args),0)
                self.assertNotIn('SUPER_SECRET',output.getvalue())
            self.f.manifest['token']='SUPER_SECRET';self.f.save()
            with redirect_stdout(io.StringIO()) as output:self.assertEqual(pe.main(['validate',str(self.f.manifest_path)]),2)
            self.assertNotIn('SUPER_SECRET',output.getvalue());self.assertEqual(json.loads(output.getvalue())['code'],'PROHIBITED_FIELD')

    def test_tc_pe_213_native_python_child_stream_timeout_and_command(self):
        real_popen=subprocess.Popen
        for mode in ('success','nonzero','overflow','timeout'):
            seen=[]
            script="import sys,time; from pathlib import Path; data=sys.stdin.buffer.read(); "
            if mode=='success':script+="Path(sys.argv[1]).write_bytes(b'{}');sys.stdout.buffer.write(data);sys.stderr.write('diagnostic')"
            elif mode=='nonzero':script+="sys.exit(7)"
            elif mode=='overflow':script+="sys.stdout.buffer.write(b'x'*2097153);sys.stdout.flush()"
            else:script+="time.sleep(5)"
            def launch(command,**kwargs):
                if '--output-last-message' not in command:
                    return real_popen(command,**kwargs)
                seen.append((command,dict(kwargs)))
                final=command[command.index('--output-last-message')+1]
                return real_popen([str(self.f.executable),'-c',script,final],**kwargs)
            with self.subTest(mode=mode),patch.object(process.subprocess,'Popen',side_effect=launch),patch.dict(os.environ,{'UNLISTED_PRIVATE_VALUE':'MUST_NOT_INHERIT'}):
                result=process.native_capture(executable=str(self.f.executable),model={'alias':'test-model','reasoning_effort':'medium'},features=DISABLED_FEATURES,prompt=b'fixture stdin',timeout_seconds=0.2 if mode=='timeout' else 3)
            command,kw=seen[0];self.assertFalse(kw['shell']);self.assertNotIn('--add-dir',command);self.assertIn('--ignore-user-config',command);self.assertNotIn('UNLISTED_PRIVATE_VALUE',kw['env']);self.assertFalse(Path(kw['cwd']).exists());self.assertEqual(result['cleanup_outcome'],'DELETED')
            if mode=='success':self.assertEqual(result['stdout'],b'fixture stdin');self.assertEqual(result['final'],b'{}');self.assertFalse(result['integrity_failure'])
            elif mode=='nonzero':self.assertEqual(result['exit_code'],7)
            elif mode=='overflow':self.assertTrue(result['integrity_failure']);self.assertIsNone(result['stdout']);self.assertTrue(result['stream_observations']['stdout']['overflow'])
            else:self.assertEqual(result['process_outcome'],'TIMED_OUT');self.assertIn(result['termination_outcome'],('TERMINATION_OBSERVED','TERMINATION_UNCONFIRMED'))

    def test_tc_pe_214_envelope_types_claims_and_explicit_failure(self):
        variants=[('boolean-as-integer',lambda e:e['observations'][0].update(value=True),'OUTPUT_INVALID'),('unknown-ref',lambda e:e['observations'][0].update(evidence_refs=['NOT-VISIBLE']),'OUTPUT_INVALID'),('duplicate-check',lambda e:e['observations'].append(copy.deepcopy(e['observations'][0])),'OUTPUT_INVALID'),('claim',lambda e:e.update(winner='A'),'OUTPUT_INVALID'),('explicit-failure',lambda e:e.update(response_status='PARTICIPANT_FAILURE',failure_reason='Insufficient evidence',observations=[]),'PARTICIPANT_FAILURE')]
        for name,change,status in variants:
            def launch(**kw):
                sid=next(s for s in self.f.visible if ('"scenario_id":"'+s+'"').encode() in kw['prompt']);env=self.f.envelope(sid);change(env);return capture(packed(env),kw['prompt'])
            with self.subTest(name=name):
                r=self.f.run(launch,name);self.assertEqual(len(r['attempts']),6);self.assertEqual({x['terminal_status'] for x in r['attempts']},{status})

    def test_tc_pe_215_trace_grammar_warning_and_mismatch(self):
        final=packed(self.f.envelope('SC-0'));accepted=trace(final)
        result=process.parse_trace(accepted);self.assertTrue(result['valid']);self.assertEqual(len(result['warnings']),1)
        rows=[json.loads(x) for x in accepted.splitlines()]
        variants=[accepted+b'{}\n',b'\n'.join(packed(x) for x in rows[1:]),accepted.replace(b'"thread_id":',b'"extra":'),accepted.replace(b'"output_tokens":0',b'"output_tokens":true'),b'{"type":"turn.completed","type":"other"}\n']
        for raw in variants:
            with self.subTest(raw=raw[:50]):self.assertFalse(process.parse_trace(raw)['valid'])
        def launch(**kw):
            r=self.launcher(**kw);r['stdout']=trace(packed(self.f.envelope('SC-0',summary='different')));return r
        r=self.f.run(launch);self.assertEqual(r['attempts'][0]['output_error'],'TRACE_FINAL_MISMATCH')

    def test_tc_pe_216_symlink_and_existing_root_unchanged(self):
        target=self.f.inputs/'A.md';link=self.f.inputs/'link.md'
        try:link.symlink_to(target)
        except OSError as error:self.skipTest('OS denied creating symlink fixture: '+type(error).__name__)
        self.f.manifest['participants'][0]['assets'][0]['source_path']='link.md'
        with self.assertRaisesRegex(PairedEvaluationError,'LINK_FORBIDDEN'):self.valid()
        self.f.manifest['participants'][0]['assets'][0]['source_path']='A.md'

    def test_tc_pe_220_existing_root_unchanged(self):
        self.f.run(self.launcher);root=self.f.base/'runs/INDEPENDENT-RUN';before={p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
        with self.assertRaisesRegex(PairedEvaluationError,'RUN_ID_EXISTS'):self.f.run(lambda **kw:self.fail('must not launch'))
        self.assertEqual(before,{p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()})

    def test_tc_pe_217_scenario_32_ceiling_is_disclosed(self):
        original=self.f.manifest['scenarios'][:];self.f.manifest['scenarios']=[];self.f.manifest['schedule']=[]
        for i in range(32):
            sid=f'LIMIT-{i}';v=copy.deepcopy(self.f.visible['SC-'+str(i%3)]);v['scenario_id']=sid
            self.f.manifest['scenarios'].append({'id':sid,'method':v['method'],'visible_input':self.f.source(sid+'.json',packed(v)),'oracle_commitment_sha256':'a'*64})
            self.f.manifest['schedule'].append({'attempt_id':f'P-{i}','scenario_id':sid,'order':['A','B']})
        self.valid()
        self.f.manifest['scenarios'].append(original[0])
        with self.assertRaisesRegex(PairedEvaluationError,'INVALID_ARRAY'):self.valid()
        self.f.save()
        with self.assertRaisesRegex(PairedEvaluationError,'INVALID_ARRAY'):
            pe.materialize_preview(self.f.manifest_path,self.f.exclusions,self.f.base/'over-limit')
        self.assertFalse((self.f.base/'over-limit').exists())

    def test_tc_pe_218_fault_injected_write_preserves_finalized_prefix(self):
        real_write=pe._write
        def fail_late(root,locator,raw):
            if locator=='attempts/PAIR-0-B/final.txt':raise OSError('synthetic write fault')
            return real_write(root,locator,raw)
        with patch.object(pe,'_write',side_effect=fail_late):r=self.f.run(self.launcher)
        self.assertEqual(r['attempts'][0]['terminal_status'],'COMPLETED_PROCESS');self.assertEqual(r['attempts'][1]['terminal_status'],'INFRASTRUCTURE_FAILURE');self.assertEqual([a['terminal_status'] for a in r['attempts'][2:]],['NOT_EXECUTED']*4)
        first=self.f.base/'runs/INDEPENDENT-RUN/attempts/PAIR-0-A/envelope.json';self.assertEqual(json.loads(first.read_bytes())['scenario_id'],'SC-0')

    def test_tc_pe_219_grade_missing_assertion_and_keyword_only(self):
        def launch(**kw):
            sid=next(s for s in self.f.visible if ('"scenario_id":"'+s+'"').encode() in kw['prompt']);return capture(packed(self.f.envelope(sid,summary='INTEGER seven 7 true evidence F-1',observations=[])),kw['prompt'])
        r=self.f.run(launch);root=self.f.base/'runs/INDEPENDENT-RUN';out=self.f.base/'grade.json'
        with self.assertRaises(PairedEvaluationError):pe.grade_run(root,self.f.base/'absent.json',out)
        self.assertFalse(out.exists())
        assertion={'schema_version':1,'run_manifest_sha256':r['run_manifest_sha256'],'response_schema_sha256':r['response_schema_sha256'],'assertions':[{'id':'AS-1','scenario_id':'SC-0','check_id':'Q-1','expected':{'value_type':'INTEGER','value':7},'required_evidence_refs':['F-1'],'oracle_ref':'oracle/opaque'}]}
        path=self.f.base/'assertions.json';path.write_bytes(packed(assertion));report=pe.grade_run(root,path,out);self.assertEqual([a['status'] for a in report['assertions']],['UNSCORABLE','UNSCORABLE'])

    def test_tc_pe_222_registered_native_types_observation_and_grade(self):
        values=[('BOOLEAN',True),('INTEGER',1),('DECIMAL','1'),('STRING','1'),('STRING_SET',['a','b']),('JSON',{'a':[1,True,'1']})]
        for scenario in self.f.manifest['scenarios']:
            visible=self.f.visible[scenario['id']];visible['checks']=[{'id':f'Q-{i}','question':'Independent typed check','value_type':typ} for i,(typ,val) in enumerate(values)]
            scenario['visible_input']=self.f.source(scenario['id']+'.json',packed(visible))
        def launch(**kw):
            sid=next(s for s in self.f.visible if ('"scenario_id":"'+s+'"').encode() in kw['prompt'])
            envelope=self.f.envelope(sid,observations=[{'check_id':f'Q-{i}','value_type':typ,'value':val,'evidence_refs':['F-1']} for i,(typ,val) in enumerate(values)])
            return capture(packed(envelope),kw['prompt'])
        result=self.f.run(launch);self.assertEqual({a['terminal_status'] for a in result['attempts']},{'COMPLETED_PROCESS'})
        bundle={'schema_version':1,'run_manifest_sha256':result['run_manifest_sha256'],'response_schema_sha256':result['response_schema_sha256'],'assertions':[{'id':f'AS-{i}','scenario_id':'SC-0','check_id':f'Q-{i}','expected':{'value_type':typ,'value':val},'required_evidence_refs':['F-1'],'oracle_ref':'oracle/opaque'} for i,(typ,val) in enumerate(values)]}
        path=self.f.base/'native-assertions.json';path.write_bytes(packed(bundle));report=pe.grade_run(self.f.base/'runs/INDEPENDENT-RUN',path,self.f.base/'native-grade.json');self.assertEqual([r['status'] for r in report['assertions']],['SATISFIED']*12)
        bundle['assertions'][1]['expected']['value']='1';path.write_bytes(packed(bundle))
        with self.assertRaises(PairedEvaluationError):pe.grade_run(self.f.base/'runs/INDEPENDENT-RUN',path,self.f.base/'invalid-grade.json')
        self.assertFalse((self.f.base/'invalid-grade.json').exists())

    def native_parse(self,typ,val,raw_override=None):
        from qa_master._paired_contract import parse_envelope
        visible=copy.deepcopy(self.f.visible['SC-0']);visible['checks']=[{'id':'N','question':'Typed test','value_type':typ}]
        envelope=self.f.envelope('SC-0',observations=[{'check_id':'N','value_type':typ,'value':val,'evidence_refs':['F-1']}])
        raw=packed(envelope) if raw_override is None else packed(envelope).replace(b'"value":"REPLACE_VALUE"',b'"value":'+raw_override)
        return parse_envelope(raw,visible,['skills/entry.md'])

    def test_tc_pe_223_native_no_coercion_and_set_boundaries(self):
        for typ,values in [('BOOLEAN',[0,1,'true']),('INTEGER',[True,'1',1.2]),('DECIMAL',[1,'-0','01','1.0','1e0','NaN']),('STRING',[1,True,[]]),('STRING_SET',['["a"]',['b','a'],['a','a'],[1],['']])]:
            for value in values:
                with self.subTest(typ=typ,value=value),self.assertRaises(PairedEvaluationError):self.native_parse(typ,value)
        self.native_parse('STRING_SET',[f's{i:03}' for i in range(256)])
        with self.assertRaises(PairedEvaluationError):self.native_parse('STRING_SET',[f's{i:03}' for i in range(257)])
        self.assertEqual(self.native_parse('STRING','rating score winner')['observations'][0]['value'],'rating score winner')

    def test_tc_pe_224_json_depth_nodes_recursive_keys(self):
        # Root container has depth one. Empty child containers increase depth.
        value=[]
        for _ in range(15):value=[value]
        self.native_parse('JSON',value)
        with self.assertRaises(PairedEvaluationError):self.native_parse('JSON',[value])
        self.native_parse('JSON',[0]*4095)
        with self.assertRaises(PairedEvaluationError):self.native_parse('JSON',[0]*4096)
        # Root + 2047 key/value pairs + one scalar child: 4096 nodes.
        at_limit={f'k{i}':0 for i in range(2047)};at_limit['k0']=[0]
        self.native_parse('JSON',at_limit)
        with self.assertRaises(PairedEvaluationError):self.native_parse('JSON',dict(at_limit,extra=0))
        for key in ('rating','score','winner','quality_grade','approval','execution_result','superiority','token'):
            with self.subTest(key=key),self.assertRaises(PairedEvaluationError):self.native_parse('JSON',{'nested':[{key:'synthetic'}]})

    def test_tc_pe_225_raw_integer_and_json_lexical_rejection(self):
        for raw in (b'-0',b'1e0',b'1.0',b'true',b'"1"'):
            with self.subTest(raw=raw),self.assertRaises(PairedEvaluationError):self.native_parse('INTEGER','REPLACE_VALUE',raw)
        for raw in (b'{"a":1,"a":2}',b'{"a":1.1}',b'"\\ud800"',b'NaN',b'Infinity'):
            with self.subTest(raw=raw),self.assertRaises(PairedEvaluationError):self.native_parse('JSON','REPLACE_VALUE',raw)

    def test_tc_pe_226_integer_34_digit_bound_independent_of_python_setting(self):
        get_limit=getattr(sys,'get_int_max_str_digits',None)
        set_limit=getattr(sys,'set_int_max_str_digits',None)
        prior=get_limit() if get_limit else None
        result=self.f.run(self.launcher)
        bundle={'schema_version':1,'run_manifest_sha256':result['run_manifest_sha256'],'response_schema_sha256':result['response_schema_sha256'],'assertions':[{'id':'AS-LIMIT','scenario_id':'SC-0','check_id':'Q-1','expected':{'value_type':'INTEGER','value':0},'required_evidence_refs':['F-1'],'oracle_ref':'oracle/opaque'}]}
        assertion_path=self.f.base/'integer-limit-assertions.json'
        try:
            for setting in ((640,0) if set_limit else (None,)):
                if set_limit:set_limit(setting)
                for sign in ('','-'):
                    exact=(sign+'9'*34).encode();overflow=(sign+'9'*35).encode()
                    self.native_parse('INTEGER','REPLACE_VALUE',exact)
                    self.native_parse('JSON','REPLACE_VALUE',b'{"nested":['+exact+b']}')
                    for typ,raw in [('INTEGER',overflow),('JSON',b'{"nested":['+overflow+b']}')]:
                        with self.subTest(setting=setting,sign=sign,typ=typ),self.assertRaises(PairedEvaluationError):self.native_parse(typ,'REPLACE_VALUE',raw)
                    bundle['assertions'][0]['expected']['value']=int(exact)
                    assertion_path.write_bytes(packed(bundle))
                    report=pe.grade_run(self.f.base/'runs/INDEPENDENT-RUN',assertion_path,self.f.base/f'grade-limit-{setting}-{len(sign)}.json')
                    self.assertEqual([a['status'] for a in report['assertions']],['VIOLATED','VIOLATED'])
                    bundle['assertions'][0]['expected']['value']=int(overflow)
                    assertion_path.write_bytes(packed(bundle))
                    rejected=self.f.base/f'grade-overflow-{setting}-{len(sign)}.json'
                    with self.assertRaises(PairedEvaluationError):pe.grade_run(self.f.base/'runs/INDEPENDENT-RUN',assertion_path,rejected)
                    self.assertFalse(rejected.exists())
        finally:
            if set_limit:set_limit(prior)
