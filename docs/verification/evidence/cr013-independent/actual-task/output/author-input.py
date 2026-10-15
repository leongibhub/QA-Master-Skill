import json
from pathlib import Path
root=Path(r'C:\Users\LEON~1.WAN\AppData\Local\Temp\qa-master-cr013-acceptance-b8wwvs6j')
out=root/'task-output'
refs=[{'id':f'F-{i:02}','kind':'requirement','locator':f'source-facts/F-{i:02}'} for i in range(1,8)]
refs += [{'id':'EFF-04','kind':'effect','locator':'source-facts/F-04/status-REVIEW'},{'id':'EFF-05','kind':'effect','locator':'source-facts/F-05/status-PUBLISHED'}]
oracles=[{'id':i,'kind':k,'locator':loc} for i,k,loc in [('O-valid','valid','source-facts/F-01/in-range'),('O-invalid','invalid','source-facts/F-01/out-of-range'),('O-allow','outcome','source-facts/F-02/both-true'),('O-no','outcome','source-facts/F-02/otherwise'),('O-review','transition','source-facts/F-04/status-REVIEW'),('O-published','transition','source-facts/F-05/status-PUBLISHED'),('O-deny','denial','source-facts/F-06/stays-DRAFT')]]
models=[{'id':'M-boundary','method':'boundary','title':'Batch integer range','dimension':'functional','requirement_ids':['REQ-001'],'source_refs':['F-01'],'spec':{'numeric_type':'integer','origin':0,'step':1,'lower':{'value':2,'inclusive':True},'upper':{'value':6,'inclusive':True},'oracle_by_class':{'IN_DOMAIN':'O-valid','LOWER_INVALID':'O-invalid','UPPER_INVALID':'O-invalid'}}}]
rules=[]
for m,s in [(False,False),(False,True),(True,False),(True,True)]:
 rules.append({'id':f'R-{int(m)}{int(s)}','when':{'member':m,'settled':s},'outcome_id':'REBATE_ALLOWED' if m and s else 'NO_REBATE','source_refs':['F-02'],'oracle_ref':'O-allow' if m and s else 'O-no'})
models.append({'id':'M-decision','method':'decision_table','title':'Member and settled rebate decision','dimension':'functional','requirement_ids':['REQ-002'],'source_refs':['F-02'],'spec':{'conditions':[{'id':'member','values':[False,True]},{'id':'settled','values':[False,True]}],'constraints':[],'rules':rules}})
transitions=[]
for id,frm,to,event,valid,source,effect,oracle in [('T-submit','DRAFT','REVIEW','submit','valid','F-04','EFF-04','O-review'),('T-publish','REVIEW','PUBLISHED','publish','valid','F-05','EFF-05','O-published'),('T-invalid','DRAFT',None,'publish','invalid','F-06',None,'O-deny')]:
 transitions.append({'id':id,'validity':valid,'from_state':frm,'to_state':to,'trigger':event,'guard_refs':[],'effect_refs':[effect] if effect else [],'source_refs':[source],'oracle_ref':oracle})
models.append({'id':'M-state','method':'state_transition','title':'Document lifecycle, explicit transitions only','dimension':'functional','requirement_ids':['REQ-003','REQ-004','REQ-005','REQ-006'],'source_refs':['F-03','F-04','F-05','F-06'],'spec':{'states':[{'id':s,'terminal':s=='PUBLISHED','source_refs':['F-03']} for s in ['DRAFT','REVIEW','PUBLISHED']],'initial_state':'DRAFT','triggers':['submit','publish'],'transitions':transitions,'closed_world':False,'closed_world_deny_oracle_ref':None}})
statements=['Strict integer batch size 2 through 6 inclusive, step 1 origin 0.','Rebate allowed exactly when member and settled are true.','DRAFT initial; REVIEW; PUBLISHED terminal.','submit in DRAFT changes status to REVIEW, no guard declared.','publish in REVIEW changes status to PUBLISHED, no guard declared.','publish in DRAFT invalid; stays DRAFT. Other combinations unspecified.']
bundle={'project':'Document release policy offline draft','requirements':[{'id':f'REQ-{i:03}','title':s,'dimension':'functional','approved':False} for i,s in enumerate(statements,1)],'design_models':{'schema_version':1,'source_refs':refs,'oracle_refs':oracles,'models':models}}
(out/'design-input.json').write_text(json.dumps(bundle,indent=2),encoding='utf-8')
