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
    equal(set(data['selected']), {'T0','T1','T2'})
    equal(len(data['selected']),3)
    equal(set(data['execution_order']),set(data['selected']))
    equal(len(data['execution_order']),3)
    assert data['execution_order'].index('T0') < data['execution_order'].index('T1')
    assert data['execution_order'].index('T0') < data['execution_order'].index('T2')
    equal(data['total_minutes'],11)
    assert data['total_minutes'] <= 12
    equal(data['budget_status'],'FEASIBLE')
    equal(set(data['deferred']), {'T3','T4'})
    equal(data['uncovered_risks'],[])

if __name__ == '__main__':
    try:
        grade(read_result())
    except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
        print('fixture assertion failed:', exc, file=sys.stderr)
        sys.exit(1)
    print('fixture assertions passed')
