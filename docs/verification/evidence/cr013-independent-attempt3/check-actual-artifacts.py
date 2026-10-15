from pathlib import Path
import json,hashlib
p=Path(__file__).parent/'actual-task'
r=json.loads((p/'report-original.json').read_bytes());cases=json.loads((p/'final-cases.json').read_bytes());gaps=json.loads((p/'typed-gaps.json').read_bytes())
assert len(cases)==14 and len(gaps)==15
assert not r['requirement_review']['findings'] and r['case_review']['case_count']==3
assert {x['code'] for x in r['case_review']['issues']}=={'UNAPPROVED_TRACE'}
assert not r['formal_baseline_approved']
b={c['input']['value']:c['input']['class'] for c in cases if c['type']=='boundary'}
assert b=={'1':'LOWER_INVALID','2':'IN_DOMAIN','3':'IN_DOMAIN','5':'IN_DOMAIN','6':'IN_DOMAIN','7':'UPPER_INVALID'}
d={(c['input']['assignment']['member'],c['input']['assignment']['settled']):c['input']['outcome_id'] for c in cases if c['type']=='decision_table'}
assert d=={(False,False):'NO_REBATE',(False,True):'NO_REBATE',(True,False):'NO_REBATE',(True,True):'REBATE'}
s={(c['input']['from_state'],c['input']['trigger'],c['input']['to_state'],c['input']['validity']) for c in cases if c['type']=='state_transition'}
assert s=={('DRAFT','submit','REVIEW','valid'),('REVIEW','publish','PUBLISHED','valid'),('DRAFT','publish',None,'invalid')}
assert len({c['id'] for c in cases})==14
ids=[c['helper_candidate_id'] for c in cases if c.get('helper_candidate_id')]
assert len(ids)==len(set(ids))==13
assert set(ids)=={c['id'] for c in r['method_design']['candidates']}
for c in cases:
 assert c['approval']=='DRAFT_UNAPPROVED' and c['execution']=='NOT_EXECUTED'
 assert set(c['gap_ids']) <= {g['id'] for g in gaps}
 assert set(c['source_ids']) <= {'F-01','F-02','F-03','F-04','F-05','F-06','F-07'}
 assert c['preconditions'] and c['actions'] and c['expected'] and c['cleanup']
assert hashlib.sha256((p/'source-facts-preserved.md').read_bytes()).hexdigest()=='a52b944d6a6d406c40090aed4c4e2680263d8a9ba96955571421a72631284b7c'
print('Independent artifact checks PASS: 3 generic drafts; 13 exact method bindings; 14 completed policy drafts; 15 linked gaps; no approval/execution promotion.')
