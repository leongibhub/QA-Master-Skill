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
    equal(ids(data["traces"]), {"T0","T1","T2","T3","T4"})
    rows = {r["id"]:r for r in data["traces"]}
    expected = [{'id': 'T0', 'selection': 'valid', 'arguments': 'valid', 'authorization': 'allowed', 'side_effects': 0, 'duplicate': False}, {'id': 'T1', 'selection': 'wrong', 'arguments': 'valid', 'authorization': 'denied', 'side_effects': 0, 'duplicate': False}, {'id': 'T2', 'selection': 'valid', 'arguments': 'invalid', 'authorization': 'allowed', 'side_effects': 0, 'duplicate': False}, {'id': 'T3', 'selection': 'valid', 'arguments': 'valid', 'authorization': 'allowed', 'side_effects': 1, 'duplicate': False}, {'id': 'T4', 'selection': 'valid', 'arguments': 'valid', 'authorization': 'allowed', 'side_effects': 2, 'duplicate': True}]
    for row in expected:
        for key, value in row.items():
            equal(rows[row["id"]][key], value)

if __name__ == '__main__':
    try:
        grade(read_result())
    except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
        print('fixture assertion failed:', exc, file=sys.stderr)
        sys.exit(1)
    print('fixture assertions passed')
