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


def source_values(rows, value_key, versions):
    """兼容扁平值及显式版本来源；嵌套版本必须与来源登记一致。"""
    assert type(rows) is dict, 'source values must be an object'
    values = {}
    for source, value in rows.items():
        if isinstance(value, dict):
            equal(set(value), {'version', value_key})
            equal(value['version'], versions[source])
            value = value[value_key]
        values[source] = value
    return values


def grade(data):
    equal({(r['source_id'], r['version']) for r in data['source_register']}, {('qa-1','v1'),('tech-1','v2'),('product-1','v3')})
    equal(len(data['source_register']), 3)
    versions = {r['source_id']: r['version'] for r in data['source_register']}
    ids(data['findings'])
    equal(len(data['findings']), 2)
    merged = next(r for r in data['findings'] if set(r['input_finding_ids']) == {'F-qa','F-tech'})
    separate = next(r for r in data['findings'] if set(r['input_finding_ids']) == {'F-product'})
    equal(set(merged['sources']), {'qa-1','tech-1'})
    equal(set(separate['sources']), {'product-1'})
    equal(merged['severity'], 'P0')
    equal(source_values(merged['original_severities'], 'severity', versions), {'qa-1':'P0','tech-1':'P1'})
    equal(source_values(separate['original_severities'], 'severity', versions), {'product-1':'P2'})
    equal(source_values(merged['evidence_by_source'], 'evidence', versions), {'qa-1':['run-R1'],'tech-1':['diff-D1']})
    equal(source_values(separate['evidence_by_source'], 'evidence', versions), {'product-1':['req-Q7']})
    assert merged['id'] in data['blockers']
    assert any(set(d['sources']) == {'qa-1','tech-1'} for d in data['disagreements'])

if __name__ == '__main__':
    try:
        grade(read_result())
    except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
        print('fixture assertion failed:', exc, file=sys.stderr)
        sys.exit(1)
    print('fixture assertions passed')
