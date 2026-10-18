#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from api_case_contract import contract_errors, endpoints_from, incomplete_message, fail_incomplete

def _safe_name(method, path, i):
    return 'api_' + re.sub(r'[^a-z0-9]+', '_', f'{method}_{path}_{i}'.lower()).strip('_')

def _to_test(method, path, title, endpoint=None):
    ep = endpoint or {}
    lines = [f"test({json.dumps(title)}, async () => {{"]
    errors = contract_errors(method, path, ep)
    if errors:
        return '\n'.join(lines + [f"  throw new Error({json.dumps(incomplete_message(errors))});", '});', ''])
    call = f"request(app).{method.lower()}({json.dumps(path)})"
    for k,v in ep.get('headers',{}).items():
        call += f".set({json.dumps(k)}, {json.dumps(v)})"
    for k,v in ep.get('headers_env',{}).items():
        lines.append(f"  if (!process.env[{json.dumps(v)}]) throw new Error('Missing credential environment variable: {v}');")
        call += f".set({json.dumps(k)}, process.env[{json.dumps(v)}])"
    if 'body' in ep:
        call += f".send({json.dumps(ep['body'], ensure_ascii=False)})"
    if ep.get('max_response_ms') is not None: lines.append('  const started = Date.now();')
    lines += [f"  const res = await {call};", f"  expect({json.dumps(ep['expected_statuses'])}).toContain(res.status);"]
    if 'expected_json' in ep: lines.append(f"  expect(res.body).toEqual({json.dumps(ep['expected_json'], ensure_ascii=False)});")
    if ep.get('max_response_ms') is not None: lines.append(f"  expect(Date.now() - started).toBeLessThanOrEqual({ep['max_response_ms']});")
    return '\n'.join(lines + ['});', ''])

def main():
    parser=argparse.ArgumentParser(description='Generate contract-derived API smoke tests')
    parser.add_argument('--input',required=True,type=Path);parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args();endpoints=endpoints_from(json.loads(args.input.read_text(encoding='utf-8')))
    lines=["const request = require('supertest');", "const path = require('path');", "const app = process.env.API_BASE_URL || (process.env.SUPERTEST_APP ? require(path.resolve(process.env.SUPERTEST_APP)) : null);", "if (!app) throw new Error('Set API_BASE_URL or SUPERTEST_APP to the approved target');", "describe('Generated API smoke assertions', () => {"]
    for i,ep in enumerate(endpoints,1):
        method,path=str(ep.get('method','')),str(ep.get('path',''))
        lines.append(_to_test(method,path,_safe_name(method,path,i),ep))
    lines.append('});');args.output_dir.mkdir(parents=True,exist_ok=True)
    out=args.output_dir/'generated.api.test.js';out.write_text('\n'.join(lines)+'\n',encoding='utf-8');print(out)
    fail_incomplete(endpoints)

if __name__ == '__main__': main()
