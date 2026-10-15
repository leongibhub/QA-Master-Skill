"""Independent DES-055 installed workflow tests, no model or product execution."""
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from qa_master.codex_skill import install_skill
from qa_master.campaign_cli import prepare_campaign


def bundle():
    base={'id':'R-1','text':'Finite policy','source':'sources/facts.md','dimension':'functional','approved':False,'priority':'P1'}
    refs=[{'id':'S','kind':'requirement','locator':'sources/facts.md'},{'id':'E','kind':'effect','locator':'sources/effect.md'}]
    oracles=[{'id':i,'kind':kind,'locator':'oracles/'+i} for i,kind in [('V','valid'),('I','invalid'),('O','outcome'),('T','transition'),('D','denial')]]
    def model(i,method,spec):return {'id':i,'method':method,'title':i,'dimension':'functional','requirement_ids':['R-1'],'source_refs':['S'],'spec':spec}
    models=[model('B','boundary',{'numeric_type':'integer','origin':0,'step':1,'lower':{'value':2,'inclusive':True},'upper':{'value':6,'inclusive':True},'oracle_by_class':{'IN_DOMAIN':'V','LOWER_INVALID':'I','UPPER_INVALID':'I','BOTH_INVALID':'I'}}),model('D','decision_table',{'conditions':[{'id':'member','values':[False,True]}],'constraints':[],'rules':[{'id':'yes','when':{'member':True},'outcome_id':'allowed','source_refs':['S'],'oracle_ref':'O'},{'id':'no','when':{'member':False},'outcome_id':'denied','source_refs':['S'],'oracle_ref':'O'}]}),model('S','state_transition',{'states':[{'id':'draft','terminal':False,'source_refs':['S']},{'id':'done','terminal':True,'source_refs':['S']}],'initial_state':'draft','triggers':['submit'],'transitions':[{'id':'submit','validity':'valid','from_state':'draft','to_state':'done','trigger':'submit','guard_refs':[],'effect_refs':['E'],'source_refs':['S'],'oracle_ref':'T'}],'closed_world':False,'closed_world_deny_oracle_ref':None})]
    return {'project':'Independent installed task','requirements':[base],'design_models':{'schema_version':1,'source_refs':refs,'oracle_refs':oracles,'models':models}}


class InstalledMethodIndependent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='qa-installed-independent-');cls.base=Path(cls.temp.name)
        cls.skill=cls.base/'project/.agents/skills/qa-master';install_skill(cls.skill)
        cls.cwd=cls.base/'unrelated';cls.cwd.mkdir();cls.wrapper=cls.skill/'scripts/qa.py'
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def setUp(self):
        self.area=self.base/self._testMethodName;self.area.mkdir();self.input=self.area/'input.json';self.output=self.area/'output.json';self.state=self.area/'state-sentinel.json';self.state.write_bytes(b'STATE_UNTOUCHED')
    def invoke(self,b,extra=None,raw=None):
        self.input.write_bytes(raw if raw is not None else json.dumps(b).encode())
        args=[sys.executable,'-I',str(self.wrapper),'--state',str(self.state),'design','--input',str(self.input),'--output',str(self.output)]
        if extra:args.extend(extra)
        return subprocess.run(args,cwd=self.cwd,capture_output=True,text=True,encoding='utf-8',env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'})
    def report(self,b):
        result=self.invoke(b);self.assertEqual(result.returncode,0,result.stderr+result.stdout);return json.loads(self.output.read_bytes()),json.loads(result.stdout)

    def test_tc_imd_001_002_isolated_three_methods_equivalence(self):
        b=bundle();r,summary=self.report(b);direct=prepare_campaign(b)
        self.assertEqual(r['method_design'],direct['method_design'])
        self.assertEqual({m['method'] for m in r['method_design']['model_results']},{'boundary','decision_table','state_transition'})
        self.assertEqual([p['value'] for p in next(m for m in r['method_design']['model_results'] if m['model_id']=='B')['analysis']['points']],['1','2','3','5','6','7'])
        for key in direct:self.assertEqual(r[key],direct[key])
        self.assertEqual(set(r)-set(direct),{'installed_design'});self.assertEqual(summary['execution'],'NOT_EXECUTED')
        self.assertFalse(r['installed_design']['method_output']['usable_case_claim']);self.assertFalse(r['installed_design']['method_output']['executable_case_claim'])

    def test_tc_imd_003_004_missing_models_sources_dimensions_honest(self):
        b=bundle();del b['design_models'];del b['requirements'][0]['source'];del b['requirements'][0]['dimension']
        r,_=self.report(b);codes={g['code'] for g in r['installed_design']['gaps']}
        self.assertTrue({'METHOD_MODELS_NOT_SUPPLIED','SOURCE_NOT_SUPPLIED','GUIDE_DIMENSION_NOT_SUPPLIED'}<=codes)
        self.assertFalse(r['formal_baseline_approved']);self.assertFalse(r['installed_design']['method_output']['present'])
        b=bundle();b['design_models']['models']=[];r,_=self.report(b);self.assertIn('METHOD_MODELS_EMPTY',[g['code'] for g in r['installed_design']['gaps']])
        b=bundle();del b['design_models']['models'][0]['spec']['oracle_by_class']['IN_DOMAIN'];r,_=self.report(b)
        self.assertIn('BOUNDARY_ORACLE_MISSING',[g['code'] for g in r['method_design']['obligations']]);self.assertFalse(r['formal_baseline_approved'])
        self.assertFalse(json.loads(self.input.read_bytes())['requirements'][0]['approved'])

    def test_tc_imd_005_008_guide_source_binding_determinism(self):
        b=bundle();r,_=self.report(b);first=self.output.read_bytes();self.report(b);self.assertEqual(self.output.read_bytes(),first)
        projection=r['installed_design'];self.assertTrue(projection['guides'])
        for guide in projection['guides']:
            self.assertEqual(guide['sha256'],hashlib.sha256((self.skill/guide['locator']).read_bytes()).hexdigest());self.assertEqual(guide['requirement_ids'],['R-1']);self.assertEqual(guide['model_ids'],['B','D','S']);self.assertFalse(Path(guide['locator']).is_absolute())
        row=next(x for x in projection['source_mapping'] if x['origin']=='DESIGN_MODEL_SOURCE' and x['source_id']=='S')
        self.assertEqual(row['model_ids'],['B','D','S']);self.assertEqual(row['binding_state'],'DECLARED');self.assertEqual(set(row['candidate_ids']),{c['id'] for c in r['method_design']['candidates']})
        guidepath=self.skill/projection['guides'][0]['locator'];old=guidepath.read_bytes()
        try:
            guidepath.write_bytes(old+b'\nIndependent mutation fixture.\n');changed,_=self.report(b);self.assertNotEqual(changed['installed_design']['guides'][0]['sha256'],projection['guides'][0]['sha256'])
        finally:guidepath.write_bytes(old)

    def test_tc_imd_006_invalid_preserves_output_and_state(self):
        invalid=[b'{"project":"x","project":"y"}',b'{"x":NaN}',b'\xff',b'x'*5000001]
        for raw in invalid:
            self.output.write_bytes(b'OUTPUT_SENTINEL');result=self.invoke(None,raw=raw);self.assertEqual(result.returncode,2);self.assertEqual(self.output.read_bytes(),b'OUTPUT_SENTINEL');self.assertEqual(self.state.read_bytes(),b'STATE_UNTOUCHED');self.assertFalse(list(self.area.glob('.qa-master-*')))
        for mutate in (lambda b:b['design_models']['models'][0]['source_refs'].append('MISSING'),lambda b:b['design_models']['oracle_refs'][0].update(kind='outcome')):
            b=bundle();mutate(b);self.output.write_bytes(b'OUTPUT_SENTINEL');self.assertEqual(self.invoke(b).returncode,2);self.assertEqual(self.output.read_bytes(),b'OUTPUT_SENTINEL')

    def test_tc_imd_006_cli_exact_options_samepath_io(self):
        for extra in (['--input',str(self.input)],['--output',str(self.output)],['--unknown'],['--out',str(self.output)]):
            self.output.write_bytes(b'SENTINEL');self.assertEqual(self.invoke(bundle(),extra=extra).returncode,2);self.assertEqual(self.output.read_bytes(),b'SENTINEL')
        self.input.write_text(json.dumps(bundle()),encoding='utf-8');original=self.input.read_bytes()
        for args in ([ '--sta',str(self.state),'design','--input',str(self.input),'--output',str(self.output)],['design','--input',str(self.input),'--output',str(self.input)],['design','--input',str(self.area/'absent'),'--output',str(self.output)],['design','--input',str(self.input),'--output',str(self.cwd)]):
            self.assertEqual(subprocess.run([sys.executable,'-I',str(self.wrapper),*args],cwd=self.cwd,capture_output=True).returncode,2)
        self.assertEqual(self.input.read_bytes(),original)

    def test_tc_imd_007_no_state_network_process_adapter(self):
        self.input.write_text(json.dumps(bundle()),encoding='utf-8')
        script='''import sys,runpy,socket,subprocess,os
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
wrapper,input_path,output_path,state=sys.argv[1:]
sys.path.insert(0,str(Path(wrapper).parent))
from qa_master.application import CampaignApplicationService
original_import=__import__
def guarded_import(name,*args,**kwargs):
 if name.startswith(('qa_master.adapters','qa_master.runners')): raise AssertionError('adapter import')
 return original_import(name,*args,**kwargs)
def audit(event,args):
 if event=='open' and str(args[0])==state: raise AssertionError('state read/write')
sys.addaudithook(audit)
sys.argv=[wrapper,'--state',state,'design','--input',input_path,'--output',output_path]
with patch.object(socket,'socket',side_effect=AssertionError('network')),patch.object(subprocess,'Popen',side_effect=AssertionError('process')),patch.object(os,'system',side_effect=AssertionError('process')),patch.object(CampaignApplicationService,'load',side_effect=AssertionError('state')),patch.object(CampaignApplicationService,'initialize',side_effect=AssertionError('state')),patch.object(CampaignApplicationService,'mutate',side_effect=AssertionError('approval')),patch('builtins.__import__',side_effect=guarded_import):
 runpy.run_path(wrapper,run_name='__main__')
'''
        proc=subprocess.run([sys.executable,'-I','-c',script,str(self.wrapper),str(self.input),str(self.output),str(self.state)],cwd=self.cwd,capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr);self.assertEqual(self.state.read_bytes(),b'STATE_UNTOUCHED');self.assertFalse((self.cwd/'.qa-master').exists())

    def test_tc_imd_009_012_reference_example_and_claim_boundaries(self):
        ref=(self.skill/'references/design-methods.md').read_text(encoding='utf-8');example=json.loads((self.skill/'examples/design-methods.json').read_bytes())
        for token in ('decision_table','state_transition','closed_world','oracle_by_class','DRAFT_UNAPPROVED'):self.assertIn(token,ref)
        self.assertEqual({m['method'] for m in example['design_models']['models']},{'boundary','decision_table','state_transition'});self.assertTrue(all(r.get('approved') is False for r in example['requirements']))
        r,_=self.report(example);self.assertEqual(r['installed_design']['execution'],'NOT_EXECUTED');self.assertEqual(r['installed_design']['state_access'],'NONE');self.assertFalse(r['formal_baseline_approved'])
        for c in r['method_design']['candidates']:self.assertEqual((c['approval'],c['evidence_state'],c['validation_action']),('DRAFT','PENDING','NOT_EXECUTED'))
        for b in (bundle(),{'project':'legacy','requirements':bundle()['requirements']}):
            self.input.write_text(json.dumps(b),encoding='utf-8')
            script="import sys,json;sys.path.insert(0,sys.argv[1]);from qa_master.campaign_cli import write_campaign;write_campaign(sys.argv[2],sys.argv[3])"
            out=self.area/'direct.json';p=subprocess.run([sys.executable,'-I','-c',script,str(self.skill/'scripts'),str(self.input),str(out)],cwd=self.cwd,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(out.read_bytes()),prepare_campaign(b));self.assertNotIn('installed_design',json.loads(out.read_bytes()))

    def test_tc_imd_013_legacy_semantics_documented_and_observable(self):
        ref=(self.skill/'references/design-methods.md').read_text(encoding='utf-8')
        for token in ('`text`','`source`','`acceptance`','NO_PROVENANCE','NO_ACCEPTANCE','declared provenance'):
            self.assertIn(token,ref)
        b=bundle();b['requirements'][0]['acceptance']='The finite policy outcome is observable.'
        r,_=self.report(b)
        self.assertEqual(r['requirement_review']['findings'],[])
        self.assertEqual(r['case_review']['case_count'],1)
        self.assertFalse(r['formal_baseline_approved'])
        for field,code in [('text','EMPTY_REQUIREMENT'),('source','NO_PROVENANCE'),('acceptance','NO_ACCEPTANCE')]:
            with self.subTest(field=field):
                absent=copy.deepcopy(b);del absent['requirements'][0][field]
                observed,_=self.report(absent)
                self.assertIn(code,{f['code'] for f in observed['requirement_review']['findings']})
                self.assertFalse(observed['formal_baseline_approved'])
        example=json.loads((self.skill/'examples/design-methods.json').read_bytes())
        r,_=self.report(example)
        self.assertEqual(r['requirement_review']['findings'],[])
        self.assertEqual(r['case_review']['case_count'],len(example['requirements']))
        self.assertTrue(all(req['approved'] is False for req in example['requirements']))
        self.assertFalse(r['formal_baseline_approved'])
