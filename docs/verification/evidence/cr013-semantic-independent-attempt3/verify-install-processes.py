import sys,json,hashlib,importlib.util,tempfile,subprocess,shutil
from pathlib import Path
import qa_master
from qa_master.codex_skill import install_skill
from qa_master import semantic_quality as sq
assert 'site-packages' in qa_master.__file__
ev=Path('D:/QA-Master-PR2/docs/verification/evidence/cr013-semantic-independent-attempt3')
spec=importlib.util.spec_from_file_location('independent','D:/QA-Master-PR2/tests/test_semantic_quality_independent.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root=Path(tempfile.mkdtemp(prefix='sq-independent-final-'));skill=root/'project/.agents/skills/qa-master';install_skill(skill);cwd=root/'unrelated';cwd.mkdir();inputs=root/'inputs';inputs.mkdir()
assets=Path(sq.__file__).parent/'semantic_quality_assets';installed=skill/'scripts/qa_master/semantic_quality_assets';resources=[]
for p in sorted(assets.iterdir()):
 if p.is_file():
  a=p.read_bytes();b=(installed/p.name).read_bytes();c=(Path('D:/QA-Master-PR2/qa_master/semantic_quality_assets')/p.name).read_bytes();assert a==b==c
  resources.append({'path':p.name,'sha256':m.sha(a),'bytes':len(a)})
assert len(resources)==6
assert Path(sq.__file__).read_bytes()==(skill/'scripts/qa_master/semantic_quality.py').read_bytes()==Path('D:/QA-Master-PR2/qa_master/semantic_quality.py').read_bytes()
b,r=m.fixture();raw=m.canonical(r);(inputs/'response.json').write_bytes(raw);(inputs/'facts.txt').write_bytes(b'Published policies; evaluator-authored development facts.');b['response']=dict(state='PRESENT',source_path='response.json',byte_count=len(raw),sha256=m.sha(raw),declared_projection_id=b['contract']['projection_id']);bundle=inputs/'bundle.json';bundle.write_bytes(m.canonical(b))
boot="import sys;sys.path.insert(0,sys.argv.pop(1));from qa_master.semantic_quality import main;raise SystemExit(main())"
records=[];resultdirs=[]
for n in (1,2):
 argv=[sys.executable,'-I','-c',boot,str(skill/'scripts'),'evaluate','--bundle',str(bundle),'--output-root',str(root/f'output{n}')]
 run=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,run.stderr+run.stdout
 result=json.loads(run.stdout);resultdirs.append(Path(result['profile_path']).parent);records.append({'argv':argv,'cwd':str(cwd),'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
files=lambda p:{str(x.relative_to(p)):x.read_bytes() for x in p.rglob('*') if x.is_file()}
left,right=map(files,resultdirs);assert left==right
shutil.copytree(inputs,ev/'fresh-process-inputs');shutil.copytree(resultdirs[0],ev/'fresh-process-result')
# Stable public CLI rejection; source value must not be echoed.
r['extensions']={'password':'public-fixture-not-a-credential'};raw=m.canonical(r);(inputs/'response.json').write_bytes(raw);b['response'].update(byte_count=len(raw),sha256=m.sha(raw));bundle.write_bytes(m.canonical(b))
run=subprocess.run([sys.executable,'-I','-c',boot,str(skill/'scripts'),'evaluate','--bundle',str(bundle),'--output-root',str(root/'rejected')],cwd=cwd,capture_output=True,text=True,encoding='utf-8');assert run.returncode==2
error=json.loads(run.stdout);assert set(error)=={'status','error'} and error['status']=='REJECTED' and error['error'] in ('PROHIBITED_FIELD','PROHIBITED_INPUT_PATTERN');assert 'public-fixture-not-a-credential' not in run.stdout+run.stderr;assert not (root/'rejected').exists()
(ev/'fresh-process-record.json').write_text(json.dumps({'root':str(root),'module_sha256':m.sha(Path(sq.__file__).read_bytes()),'resources':resources,'runs':records,'identical_retained_files':len(left),'result_id':resultdirs[0].name,'rejection':error,'scope':'Fresh independent Python processes, installed local helper only; no model/product execution'},indent=2),encoding='utf-8')
print(json.dumps({'resource_bytes_equal':len(resources),'module_equal':True,'fresh_processes':2,'all_retained_bytes_equal':True,'retained_files':len(left),'secret_field_atomic_rejection':error},indent=2))
