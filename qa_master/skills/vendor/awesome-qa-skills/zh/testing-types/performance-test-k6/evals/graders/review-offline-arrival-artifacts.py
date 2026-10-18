#!/usr/bin/env python3
"""Package-local skill-up assertion: validates one declared fixture result only."""
import json
import os
import re
import sys


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key: ' + key)
        out[key] = value
    return out


def read_result():
    if os.environ.get('EVAL_EXIT_CODE') != '0':
        raise ValueError('agent exit code must be zero')
    text = os.environ.get('EVAL_FINAL_MESSAGE', '').strip()
    blocks = re.findall(r'```json\s*([\s\S]*?)```', text)
    if len(blocks) > 1:
        raise ValueError('expected one JSON result')
    decoder=json.JSONDecoder(object_pairs_hook=unique_object)
    if blocks:
        return decoder.decode(blocks[0].strip())
    values=[]
    offset=0
    while True:
        start=text.find('{',offset)
        if start<0: break
        try:
            value,end=decoder.raw_decode(text,start)
        except json.JSONDecodeError:
            offset=start+1
            continue
        if isinstance(value,dict) and 'execution_status' in value:
            values.append(value)
        offset=end
    if len(values)!=1:
        raise ValueError('expected one JSON result')
    return values[0]


def equal(actual, expected):
    if type(expected) in (dict, list):
        assert type(actual) is type(expected), (type(actual), type(expected))
        if isinstance(expected, dict):
            assert set(actual) == set(expected), (actual, expected)
            for key in expected: equal(actual[key], expected[key])
        else:
            assert len(actual) == len(expected), (actual, expected)
            for left, right in zip(actual, expected): equal(left, right)
    else:
        if isinstance(expected, bool) or isinstance(actual, bool):
            assert type(actual) is type(expected), 'boolean cannot represent a count'
        assert actual == expected, (actual, expected)


def ids(rows, key='id'):
    values = [row[key] for row in rows]
    assert len(values) == len(set(values)), 'duplicate row identity'
    return set(values)


def grade(data):
    from pathlib import Path
    import subprocess
    equal(data['execution_status'], 'NOT_RUN')
    options=json.loads(Path('perf/options.json').read_text())
    scenarios=options['scenarios']
    assert isinstance(scenarios,dict) and len(scenarios)==1, 'expected one target scenario'
    scenario=next(iter(scenarios.values()))
    equal(scenario['executor'], 'constant-arrival-rate')
    for key,value in {'rate':100,'timeUnit':'1s','duration':'1m','preAllocatedVUs':20,'maxVUs':50}.items():
        equal(scenario[key],value)
    for key,value in {'http_req_duration':['p(95)<300'],'http_req_failed':['rate<0.01'],'dropped_iterations':['count==0']}.items():
        equal(options['thresholds'][key],value)
    source=Path('perf/scripts/order.js').read_text()
    business_thresholds=[key for key in ('checks','business_checks') if key in options['thresholds']]
    assert len(business_thresholds)==1, 'one unfiltered business-check threshold is required'
    equal(options['thresholds'][business_thresholds[0]],['rate==1'])
    if business_thresholds[0]=='business_checks':
        rate=re.search(r'\b(?:const|let)\s+(\w+)\s*=\s*new\s+Rate\s*\(\s*[\'\"]business_checks[\'\"]\s*\)',source)
        result=re.search(r'\b(?:const|let)\s+(\w+)\s*=\s*check\s*\(',source)
        assert rate and result, 'custom business-check rate must be declared and derive from check()'
        assert re.search(r'\b'+re.escape(rate.group(1))+r'\.add\(\s*'+re.escape(result.group(1))+r'\s*\)',source), 'every iteration must record the combined business-check result'
    entry=re.search(r'\bexport\s+(?:default\b|function\b)',source)
    assert entry, 'an exported k6 entry point is required'
    assert 'open(' in source[:entry.start()], 'options read must be init-only'
    assert 'open(' not in source[entry.start():], 'no per-iteration open'
    assert '__ENV.BASE_URL' in source and '__ENV.API_TOKEN' in source
    assert '/orders' in source and 'http.post' in source
    assert re.search(r"JSON\.stringify\(\{\s*sku\s*:\s*['\"]SKU-1['\"],\s*qty\s*:\s*1\s*\}\)",source)
    assert re.search(r'\.status\s*===\s*201',source)
    assert re.search(r"typeof\s+body\.id\s*===\s*['\"]string['\"]",source)
    assert re.search(r"body\.state\s*===\s*['\"]CREATED['\"]",source)
    assert re.search(r"body\.sku\s*===\s*['\"]SKU-1['\"]",source)
    assert re.search(r'body\.qty\s*===\s*1',source)
    assert subprocess.run(['node','--check','perf/scripts/order.js'],capture_output=True).returncode == 0

if __name__ == '__main__':
    try:
        grade(read_result())
    except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
        print('fixture assertion failed:', exc, file=sys.stderr)
        sys.exit(1)
    print('fixture assertions passed')
