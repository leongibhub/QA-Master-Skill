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
    return json.loads(blocks[0] if blocks else text, object_pairs_hook=unique_object)


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
    equal(len(data['cases']),2)
    ids(data['cases'])
    merged=next(r for r in data['cases'] if set(r['candidate_ids'])=={'C1','C2','C3','C4'})
    split=next(r for r in data['cases'] if r['candidate_ids']==['C5'])
    equal(merged['source_role'],['product','qa','ux','technical'])
    equal(merged['Trace'],['R1','AC1'])
    equal(merged['risk_tags'],['business','api','ux','consistency'])
    equal(merged['sources'],[{'source_id':'prod-1','version':'v7'},{'source_id':'qa-1','version':'v7'},{'source_id':'ux-1','version':'unknown'},{'source_id':'tech-1','version':'v7'}])
    equal(split['source_role'],['qa'])
    equal(split['Trace'],['R1','AC2'])
    equal(split['sources'],[{'source_id':'qa-2','version':'v7'}])
    equal(merged['preconditions'],{'authenticated_owner':True,'feature_enabled':True,'initial_qty':2})
    equal(split['preconditions'],{'authenticated_owner':True,'feature_enabled':False,'initial_qty':2})
    equal(merged['expected'],{'outcome':'UPDATED','qty':1})
    equal(split['expected'],{'outcome':'FEATURE_DISABLED','qty':2})
    for row in data['cases']:
        assert isinstance(row['steps'],list) and len(row['steps'])>=2
        assert all(isinstance(step,str) and step.strip() for step in row['steps'])

if __name__ == '__main__':
    try:
        grade(read_result())
    except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
        print('fixture assertion failed:', exc, file=sys.stderr)
        sys.exit(1)
    print('fixture assertions passed')
