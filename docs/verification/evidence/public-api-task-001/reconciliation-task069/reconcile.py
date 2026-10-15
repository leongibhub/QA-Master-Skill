"""Read-only TASK069 byte/boundary reconciliation. Does not assess case quality."""
import hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,'D:/QA-Master-PR2')
from qa_master.codex_skill import skill_bundle
repo=Path('D:/QA-Master-PR2');retained=repo/'docs/verification/evidence/public-api-task-001/attempt1';out=repo/'docs/verification/evidence/public-api-task-001/reconciliation-task069'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=repo)
def read(p):return json.loads(p.read_bytes())
def record(p):return {'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
manifest_path=retained/'manifest.json';manifest=read(manifest_path)
assert sha(manifest_path.read_bytes())=='503717dcbd6a5c123f461f479870a4f83a9b32366e7e4853f8dc2ee91a781021'
assert manifest_path.read_bytes()==blob('52bff0397336fe27ead11053e2798294234a8b40',manifest_path.relative_to(repo).as_posix())
verified=[]
for row in manifest['files']:
 p=retained/row['path'];assert p.resolve().is_relative_to(retained.resolve());raw=p.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'];assert raw==blob('52bff0397336fe27ead11053e2798294234a8b40',p.relative_to(repo).as_posix());verified.append(record(p))
assert {p.name for p in retained.iterdir() if p.is_file()}=={r['path'] for r in manifest['files']}|{'manifest.json','.gitattributes'}
prep=read(retained/'preparation.json');copies=read(retained/'input-copy.json');post=read(retained/'postcheck.json');handoff=read(retained/'handoff.json');skill=Path(prep['skill_root']);install_manifest=skill/'.qa-master-install.json';inventory=read(install_manifest)['files'];expected=skill_bundle()
assert sha(install_manifest.read_bytes())==prep['manifest_sha256'];assert len(inventory)==prep['installed_file_count']==59;assert set(inventory)==set(expected)
installed=[]
for name,digest in inventory.items():
 p=skill/name;raw=p.read_bytes();assert sha(raw)==digest and raw==expected[name];installed.append(record(p))
actual={p.relative_to(skill).as_posix() for p in skill.rglob('*') if p.is_file()}
assert actual==set(inventory)|{'.qa-master-install.json'}
product_delta=subprocess.check_output(['git','diff','--name-only',manifest['product_source'],'HEAD','--','qa_master','pyproject.toml'],cwd=repo).decode();assert not product_delta.strip()
source_dir=repo/'benchmarks/public-development/PD-API-COLLAB-001';allowed={'requirements.md','openapi.yaml','participant-task.md'};assert {Path(row['path']).name for row in copies}==allowed
sources=[]
for row in copies:
 p=Path(row['path']);src=source_dir/p.name;raw=p.read_bytes();frozen=blob(manifest['source_freeze_commit'],src.relative_to(repo).as_posix());assert raw==frozen==src.read_bytes();assert sha(raw)==row['sha256'] and len(raw)==row['bytes'];sources.append(record(p))
input_root=Path(copies[0]['path']).parent;assert {p.name for p in input_root.iterdir()}==allowed
freeze=(source_dir/'source-freeze.md').read_text(encoding='utf-8');assert (source_dir/'source-freeze.md').read_bytes()==blob(manifest['source_freeze_commit'],(source_dir/'source-freeze.md').relative_to(repo).as_posix())
for row in sources:assert row['sha256'].upper() in freeze
# Hashes in declared read audit are verified, without treating it as a host access log.
read_rows=re.findall(r'^\| (D:.*?) \| ([A-Fa-f0-9]{64}) \|$',(retained/'read-audit.md').read_text(encoding='utf-8'),re.M)
assert len(read_rows)==12
allowed_paths={str(Path(r['path'])) for r in copies};audits=[]
for path,digest in read_rows:
 p=Path(path);assert str(p) in allowed_paths or p.is_relative_to(skill);assert sha(p.read_bytes())==digest.lower();audits.append(record(p))
assert {r['path'] for r in handoff['sources']}=={p for p,_ in read_rows}
for row in handoff['sources']:assert sha(Path(row['path']).read_bytes())==row['sha256'].lower()
for row in handoff['artifacts']:
 p=Path(row['path']);assert sha(p.read_bytes())==row['sha256'].lower();assert p.read_bytes()==(retained/p.name).read_bytes()
assert post['sources_unchanged'] and post['installed_bundle_unchanged'] and post['checked_installed_files']==59
assert manifest['status']=='OUTPUT_RETAINED_NOT_ASSESSED';assert manifest['isolation']=='PROMPT_SCOPED_NOT_OS_ENFORCED';assert manifest['read_audit']=='PARTICIPANT_DECLARED_NOT_HOST_ACCESS_ATTESTATION'
wheels=[]
for p in (repo/'.qa-master').rglob('*.whl'):
 if sha(p.read_bytes())==prep['wheel_sha256']:wheels.append(p)
assert len(wheels)==1
wheel=wheels[0]
with zipfile.ZipFile(wheel) as z:
 for name,data in expected.items():
  if name.startswith('scripts/qa_master/'):
   assert z.read('qa_master/'+name[len('scripts/qa_master/'):])==data
  elif name!='scripts/qa.py':assert z.read('qa_master/skills/codex/'+name)==data
result={'work':'TASK-069','result':'BYTE_AND_DECLARED_BOUNDARY_RECONCILED','participant_quality_status':'OUTPUT_RETAINED_NOT_ASSESSED','retained_manifest':record(manifest_path),'retained_files':verified,'installed_manifest':record(install_manifest),'installed_inventory':installed,'wheel':record(wheel),'sources':sources,'declared_read_audit':audits,'source_freeze_commit':manifest['source_freeze_commit'],'product_source':manifest['product_source'],'postcheck_claims_match_current_bytes':True,'only_three_files_in_input_directory':True,'installed_inventory_matches_frozen_product_and_wheel':True,'limits':['No participant rerun or output edit','Fresh-install chronology is preparation-owner provenance, not independently observed here','Read audit is participant declaration, not host/OS isolation or comprehensive access proof','Before/after records corroborated by frozen/current bytes; no continuous write-monitoring claim','Withheld ledger/checklist content not read or used as a conformance or scoring oracle','No quality score/comparison/acceptance/Gate/release/product-validity conclusion']}
(out/'reconciliation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'result':result['result'],'retained_files':len(verified),'installed_files':len(installed),'allowed_inputs':len(sources),'declared_read_files':len(audits),'matched_wheel':str(wheel),'quality_status':result['participant_quality_status']},indent=2))
