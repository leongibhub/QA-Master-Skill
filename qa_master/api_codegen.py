"""Generate guarded pytest API tests from approved, fully specified scenarios."""
from __future__ import annotations
import ast,json,re
from pathlib import Path

SAFE={'GET','HEAD','OPTIONS'}
METHODS=SAFE|{'POST','PUT','PATCH','DELETE'}
PATH=re.compile(r'^/[A-Za-z0-9_./~%?=&+:-]*$')

def validate_scenarios(scenarios):
    if not isinstance(scenarios,list) or not scenarios:raise ValueError('Non-empty scenarios required')
    result=[]
    for i,s in enumerate(scenarios):
        if not isinstance(s,dict):raise ValueError('Invalid scenario')
        m=str(s.get('method','')).upper();p=s.get('path');statuses=s.get('expected_statuses')
        if m not in METHODS:raise ValueError('Unsupported method')
        if not isinstance(p,str) or not PATH.fullmatch(p) or '..' in p or '{' in p:raise ValueError('Unresolved/unsafe path')
        if not isinstance(statuses,list) or not statuses or any(type(x)!=int or not 100<=x<=599 for x in statuses):raise ValueError('Explicit status oracle required')
        if not s.get('approved'):raise ValueError('Case approval required')
        if m not in SAFE and not s.get('allow_mutation'):raise ValueError('Mutation approval required')
        if 'json_body' in s and not isinstance(s['json_body'],(dict,list)):raise ValueError('Invalid body')
        result.append({'method':m,'path':p,'expected_statuses':statuses,'json_body':s.get('json_body'),
          'has_body':'json_body' in s,'expected_json':s.get('expected_json'),
          'check_json':'expected_json' in s,'mutating':m not in SAFE})
    return result

def generate_pytest(scenarios):
    payload=repr(json.dumps(validate_scenarios(scenarios),ensure_ascii=False))
    code='''# GENERATED PYTEST FILE: never embed credentials
import json,os
from urllib.parse import urlsplit
import pytest,requests
SCENARIOS=json.loads(__PAYLOAD__)
@pytest.mark.parametrize("case",SCENARIOS)
def test_approved_api_scenario(case):
    assert os.environ.get("QA_EXECUTION_APPROVED")=="YES", "Explicit approval required"
    base=os.environ.get("QA_TARGET_URL","")
    parsed=urlsplit(base)
    assert parsed.scheme in ("http","https") and parsed.netloc and not parsed.username and not parsed.password, "Valid origin required"
    assert parsed.path in ("","/") and not parsed.query and not parsed.fragment, "Origin only"
    if case["mutating"]:
        assert os.environ.get("QA_MUTATION_APPROVED")=="YES", "Mutation approval required"
    headers={}
    token=os.environ.get("QA_API_TOKEN")
    if token:headers["Authorization"]="Bearer "+token
    kwargs={"headers":headers,"timeout":20,"allow_redirects":False}
    if case["has_body"]:kwargs["json"]=case["json_body"]
    response=requests.request(case["method"],base.rstrip("/")+case["path"],**kwargs)
    assert response.status_code in case["expected_statuses"],(response.status_code,case["expected_statuses"])
    if case["check_json"]:assert response.json()==case["expected_json"]
'''
    code=code.replace('__PAYLOAD__',payload)
    ast.parse(code)
    return code

def write_pytest(scenarios,output_path):
    p=Path(output_path)
    if p.suffix!='.py':raise ValueError('Expected .py file')
    code=generate_pytest(scenarios)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(code,encoding='utf8')
    return str(p)
