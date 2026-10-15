import sys,importlib.util,json,copy
sys.path.insert(0,'D:/QA-Master-PR2')
spec=importlib.util.spec_from_file_location('independent','D:/QA-Master-PR2/tests/test_semantic_quality_independent.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]
def run(label,mutate,check):
 t=m.SemanticIndependent();t.setUp()
 try:
  t.missing_oracle();mutate(t);p,_=t.run_profile();check(t,p);results.append({'scenario':label,'result':'PASS','rows':p['rows']})
 finally:t.doCleanups()
def duplicate(t):t.r['gaps'].append(copy.deepcopy(t.r['gaps'][0]))
def check_duplicate(t,p):
 t.expected(p,'O5','PROVENANCE','VIOLATED','REQUIRED_GAP_MISSING');t.expected(p,'O1','PROVENANCE','SATISFIED','SOURCE_BINDING_COMPLETE')
run('duplicate-gap ambiguity isolated',duplicate,check_duplicate)
def sibling(t):
 g=copy.deepcopy(t.r['gaps'][0]);g.update(gap_id='SIBLING',obligation_ids=['UNKNOWN']);t.r['gaps'].append(g)
def check_sibling(t,p):t.expected(p,'O5','PROVENANCE','SATISFIED','MISSING_ORACLE_HONESTLY_REPORTED')
run('unknown-only sibling gap does not poison valid gap',sibling,check_sibling)
def mixed(t):t.r['gaps'][0]['obligation_ids']=['O5','UNKNOWN']
def check_mixed(t,p):
 t.expected(p,'O5','PROVENANCE','VIOLATED','SOURCE_BINDING_INVALID');t.expected(p,'O1','PROVENANCE','SATISFIED','SOURCE_BINDING_COMPLETE')
run('mixed known-unknown binding affects mapped obligation only',mixed,check_mixed)
print(json.dumps(results,indent=2))
