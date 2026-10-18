#!/usr/bin/env python3
import argparse
import json
import re
from decimal import Decimal
from pathlib import Path
from api_case_contract import contract_errors, endpoints_from, incomplete_message, fail_incomplete

def _safe_name(method,path,idx):
    return re.sub(r'[^a-z0-9]+','_',f'{idx}_{method}_{path}'.lower()).strip('_')

def _invoke_line(method,path,ep=None):
    ep=ep or {};errors=contract_errors(method,path,ep)
    if errors: return f"org.junit.jupiter.api.Assertions.fail({json.dumps(incomplete_message(errors))});"
    call='given().spec(requestSpec)'
    for k,v in ep.get('headers',{}).items(): call+=f".header({json.dumps(k)}, {json.dumps(v)})"
    for k,v in ep.get('headers_env',{}).items(): call+=f".header({json.dumps(k)}, requiredEnv({json.dumps(v)}))"
    if 'body' in ep:
        body=json.dumps(ep['body'],ensure_ascii=False) if ep.get('body_encoding','json')=='json' else ep['body']
        call+=f".body({json.dumps(body)})"
    call+=f".when().{method.lower()}({json.dumps(path)}).then().statusCode(anyOf("+', '.join(f'is({s})' for s in ep['expected_statuses'])+'))'
    if ep.get('max_response_ms') is not None:
        max_nanos = min(int(Decimal(str(ep['max_response_ms'])) * Decimal(1_000_000)), (1 << 63) - 1)
        call+=f".time(lessThanOrEqualTo({max_nanos}L), java.util.concurrent.TimeUnit.NANOSECONDS)"
    if 'expected_json' not in ep: return call+';'
    return ('String actual = '+call+'.extract().asString();\n        '+
        'org.junit.jupiter.api.Assertions.assertEquals(new com.fasterxml.jackson.databind.ObjectMapper().readTree('+json.dumps(json.dumps(ep['expected_json'],ensure_ascii=False))+'), new com.fasterxml.jackson.databind.ObjectMapper().readTree(actual));')

def build_java_class(endpoints):
    endpoints=endpoints_from({'endpoints':endpoints})
    lines=['package com.example.api;','import org.junit.jupiter.api.Test;','import static io.restassured.RestAssured.given;','import static org.hamcrest.Matchers.*;','public class GeneratedApiTest extends BaseApiTest {']
    for i,ep in enumerate(endpoints,1):
        method,path=str(ep.get('method','')),str(ep.get('path',''))
        lines+=['    @Test',f'    void test_{_safe_name(method,path,i)}() throws Exception {{','        '+_invoke_line(method,path,ep),'    }']
    return '\n'.join(lines+['}',''])

def main():
    parser=argparse.ArgumentParser(description='Generate contract-derived API smoke tests')
    parser.add_argument('--input',required=True,type=Path);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();endpoints=endpoints_from(json.loads(args.input.read_text(encoding='utf-8')))
    code=build_java_class(endpoints);args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(code,encoding='utf-8');print(args.output);fail_incomplete(endpoints)

if __name__ == '__main__': main()
