#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from api_case_contract import contract_errors, endpoints_from, incomplete_message, fail_incomplete

def _safe_slug(method,path,i):
    return re.sub(r'[^a-z0-9]+','_',f'{i:03d}_{method}_{path}'.lower()).strip('_')

def _to_bru(method,path,name,endpoint=None):
    ep=endpoint or {};errors=contract_errors(method,path,ep)
    body_mode='none' if 'body' not in ep else ('json' if ep.get('body_encoding','json')=='json' else 'text')
    safe_method=method.lower() if method.upper() in {'GET','POST','PUT','PATCH','DELETE','HEAD','OPTIONS'} else 'get'
    lines=['meta {',f'  name: {name}','  type: http','  seq: 1','}', '',safe_method+' {','  url: {{baseUrl}}'+path,f'  body: {body_mode}','}', '']
    if not errors and 'body' in ep:
        body=json.dumps(ep['body'],ensure_ascii=False,indent=2) if body_mode=='json' else ep['body']
        lines += ['body:'+body_mode+' {', '\n'.join('  ' + line for line in body.splitlines()), '}', '']
    if errors:
        lines += ['script:pre-request {', '  bru.runner.stopExecution();',f'  throw new Error({json.dumps(incomplete_message(errors))});','}', '']
        return '\n'.join(lines)
    if ep.get('headers'):
        lines+=['headers {']+[f'  {k}: {v}' for k,v in ep['headers'].items()]+['}', '']
    pre=[]
    for k,v in ep.get('headers_env',{}).items():
        pre += [f'  const {v} = bru.getProcessEnv({json.dumps(v)});',f'  if (!{v}) throw new Error("Missing credential environment variable: {v}");',f'  req.setHeader({json.dumps(k)}, {v});']
    if pre: lines += ['script:pre-request {']+pre+['}', '']
    lines+=['tests {','  test("contract status", function() {',f"    expect({json.dumps(ep['expected_statuses'])}).to.include(res.getStatus());",'  });']
    if 'expected_json' in ep: lines += ['  test("contract body", function() {',f"    expect(res.getBody()).to.deep.equal({json.dumps(ep['expected_json'],ensure_ascii=False)});",'  });']
    if ep.get('max_response_ms') is not None: lines += ['  test("supplied response limit", function() {',f"    expect(res.getResponseTime()).to.be.at.most({ep['max_response_ms']});",'  });']
    return '\n'.join(lines+['}',''])

def _bruno_json(): return json.dumps({'version':'1','name':'generated-bruno-collection','type':'collection'},indent=2)+'\n'
def _env_bru(): return 'vars {\n  baseUrl: http://127.0.0.1:8080\n}\n'

def main():
    parser=argparse.ArgumentParser(description='Generate contract-derived API smoke requests')
    parser.add_argument('--input',required=True,type=Path);parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args();endpoints=endpoints_from(json.loads(args.input.read_text(encoding='utf-8')))
    req_dir=args.output_dir/'requests';env_dir=args.output_dir/'environments'
    req_dir.mkdir(parents=True,exist_ok=True);env_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'bruno.json').write_text(_bruno_json(),encoding='utf-8');(env_dir/'staging.bru').write_text(_env_bru(),encoding='utf-8')
    for i,ep in enumerate(endpoints,1):
        method,path=str(ep.get('method','')),str(ep.get('path',''));name=_safe_slug(method,path,i)
        (req_dir/(name+'.bru')).write_text(_to_bru(method,path,name,ep),encoding='utf-8')
    print(args.output_dir);fail_incomplete(endpoints)

if __name__ == '__main__': main()
