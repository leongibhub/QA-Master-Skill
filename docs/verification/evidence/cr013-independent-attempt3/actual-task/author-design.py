import json, hashlib, pathlib, subprocess, sys, datetime
base=pathlib.Path(r'C:\Users\LEON~1.WAN\AppData\Local\Temp\qa-master-cr013-attempt3-2fjk27p3')
out=base/'task-output'; out.mkdir(exist_ok=True)
skill=base/'project/.agents/skills/qa-master'
read=['SKILL.md','references/work-protocol.md','references/domains.md','references/design-methods.md']+['scripts/qa_master/skills/professional/'+n+'.md' for n in ['requirements-review','functional-api','structural-integration','nonfunctional-compatibility','security-recovery','regression-evidence']]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v): (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
source=base/'source-facts.md'; digest=sha(source)
save('read-documents.json',[{'path':str(skill/p),'sha256':sha(skill/p),'read':True,'scope':'full document'} for p in read])
(out/'source-facts-preserved.md').write_bytes(source.read_bytes())
refs=[{'id':f'F-{i:02}','kind':'requirement','locator':'source-facts.md','sha256':digest} for i in range(1,8)]
refs += [{'id':'E-REVIEW','kind':'effect','locator':'source-facts.md','sha256':digest},{'id':'E-PUBLISHED','kind':'effect','locator':'source-facts.md','sha256':digest}]
oracles=[{'id':i,'kind':k,'locator':'source-facts.md','sha256':digest} for i,k in [('O-VALID','valid'),('O-INVALID','invalid'),('O-REBATE','outcome'),('O-NOREBATE','outcome'),('O-REVIEW','transition'),('O-PUBLISHED','transition'),('O-DENY','denial')]]
reqs=[]
for i,text,accept in [('REQ-B','Batch size is strict integer on origin 0 step 1 with inclusive bounds 2 and 6.','Integers 2 through 6 are accepted; below 2 or above 6 invalid (F-01).'),('REQ-D','Rebate depends on independent booleans member and settled.','Rebate only for both true; all other combinations no rebate (F-02).'),('REQ-S','Initial DRAFT; submit reaches REVIEW, publish from REVIEW reaches terminal PUBLISHED; publish from DRAFT invalid.','Status follows F-03 through F-06; unspecified pairs remain unspecified.')]:
 reqs.append({'id':i,'text':text,'acceptance':accept,'source':'source-facts.md','dimension':'functional','approved':False,'priority':'P1'})
models=[{'id':'M-B','method':'boundary','title':'Batch integer limits','dimension':'functional','requirement_ids':['REQ-B'],'source_refs':['F-01'],'spec':{'numeric_type':'integer','origin':0,'step':1,'lower':{'value':2,'inclusive':True},'upper':{'value':6,'inclusive':True},'oracle_by_class':{'IN_DOMAIN':'O-VALID','LOWER_INVALID':'O-INVALID','UPPER_INVALID':'O-INVALID'}}}]
rules=[]
for m in [False,True]:
 for s in [False,True]:
  rules.append({'id':f'R-{int(m)}{int(s)}','when':{'member':m,'settled':s},'outcome_id':'REBATE' if m and s else 'NO_REBATE','source_refs':['F-02'],'oracle_ref':'O-REBATE' if m and s else 'O-NOREBATE'})
models.append({'id':'M-D','method':'decision_table','title':'Rebate complete boolean table','dimension':'functional','requirement_ids':['REQ-D'],'source_refs':['F-02'],'spec':{'conditions':[{'id':n,'values':[False,True]} for n in ['member','settled']],'constraints':[],'rules':rules}})
trans=[]
for i,fr,to,tr,e,o,f in [('T-SUBMIT','DRAFT','REVIEW','submit','E-REVIEW','O-REVIEW','F-04'),('T-PUBLISH','REVIEW','PUBLISHED','publish','E-PUBLISHED','O-PUBLISHED','F-05'),('T-DENY','DRAFT',None,'publish',None,'O-DENY','F-06')]:
 trans.append({'id':i,'validity':'valid' if to else 'invalid','from_state':fr,'to_state':to,'trigger':tr,'guard_refs':[],'effect_refs':[e] if e else [],'source_refs':[f],'oracle_ref':o})
models.append({'id':'M-S','method':'state_transition','title':'Declared lifecycle only','dimension':'functional','requirement_ids':['REQ-S'],'source_refs':['F-03','F-04','F-05','F-06'],'spec':{'states':[{'id':s,'terminal':s=='PUBLISHED','source_refs':['F-03']} for s in ['DRAFT','REVIEW','PUBLISHED']],'initial_state':'DRAFT','triggers':['submit','publish'],'transitions':trans,'closed_world':False,'closed_world_deny_oracle_ref':None}})
save('input-original.json',{'project':'Document release policy offline draft','requirements':reqs,'design_models':{'schema_version':1,'source_refs':refs,'oracle_refs':oracles,'models':models}})
cmd=[sys.executable,'-I',str(skill/'scripts/qa.py'),'design','--input',str(out/'input-original.json'),'--output',str(out/'report-original.json')]
r=subprocess.run(cmd,cwd=base/'unrelated-cwd',capture_output=True)
(out/'stdout.txt').write_text(r.stdout.decode('utf-8'),encoding='utf-8'); (out/'stderr.txt').write_text(r.stderr.decode('utf-8'),encoding='utf-8')
save('command-evidence.json',{'argv':cmd,'cwd':str(base/'unrelated-cwd'),'exit_code':r.returncode,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_sha256':sha(out/'input-original.json'),'report_sha256':sha(out/'report-original.json') if (out/'report-original.json').exists() else None,'meaning':'Offline helper invocation only; product tests NOT_EXECUTED'})
print(r.returncode); print(r.stdout.decode('utf-8')); print(r.stderr.decode('utf-8'))
