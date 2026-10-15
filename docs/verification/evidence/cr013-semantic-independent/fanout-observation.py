import importlib.util,json
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('independent','D:/QA-Master-PR2/tests/test_semantic_quality_independent.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
records=[]
for n in (4,8):
 t=m.SemanticIndependent();t.setUp()
 try:
  original=t.r['cases'][0];t.r['cases']=[]
  for i in range(n):
   c=m.copy.deepcopy(original);c['case_id']='CX'+str(i);t.r['cases'].append(c)
  t.r['gaps']=[dict(gap_id='G'+str(i),obligation_ids=['O0'],reason='ORACLE_MISSING',fact_ids=['F0'],source_ids=['S'],needed_evidence='Review gap',evidence_pointer='source:scope') for i in range(n)]
  with patch.object(m.sq,'_gap_valid',wraps=m.sq._gap_valid) as observed:t.run_profile()
  records.append(dict(mapped_cases=n,mapped_gaps=n,gap_validation_calls=observed.call_count))
 finally:t.doCleanups()
print(json.dumps({'scope':'Structural call-count observation, not runtime benchmark or acceptance threshold','rows':records},indent=2))
