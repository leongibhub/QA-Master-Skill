import sys,importlib.util,json,copy
from unittest.mock import patch
sys.path.insert(0,'D:/QA-Master-PR2')
spec=importlib.util.spec_from_file_location('independent','D:/QA-Master-PR2/tests/test_semantic_quality_independent.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
records=[]
for n in (4,8,16,64):
 t=m.SemanticIndependent();t.setUp()
 try:
  template=t.b['obligations'].pop(0);obs=t.r['observations'].pop(0);ids=['X'+str(i).zfill(2) for i in range(n)]
  for i,oid in enumerate(ids):
   ob=copy.deepcopy(template);ob.update(id=oid,check_id='CHECK'+str(i));t.b['obligations'].append(ob)
   observation=copy.deepcopy(obs);observation['check_id']='CHECK'+str(i);t.r['observations'].append(observation)
  t.r['cases'][0]['obligation_ids']=ids
  counts={'all_calls':0,'all_reference_elements':0,'same_mapping_list_calls':0,'same_mapping_element_visits':0}
  original=m.sq._valid_refs
  def observe(value):
   counts['all_calls']+=1
   if isinstance(value,list):counts['all_reference_elements']+=len(value)
   if value==ids:counts['same_mapping_list_calls']+=1;counts['same_mapping_element_visits']+=len(value)
   return original(value)
  with patch.object(m.sq,'_valid_refs',side_effect=observe):t.run_profile()
  records.append({'obligations_for_one_case':n,**counts})
 finally:t.doCleanups()
print(json.dumps({'scope':'Structural repeated reference validation; no timing benchmark. Six unrelated category cases held fixed.','records':records},indent=2))
