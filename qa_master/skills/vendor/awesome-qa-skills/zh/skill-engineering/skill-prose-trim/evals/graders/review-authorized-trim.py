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
    from pathlib import Path
    equal(data["mode"], "edited")
    # 可编辑文档保留每行内容；末尾换行不是判定规则。
    equal(Path("contract.md").read_text().splitlines(), '# Safe review\nNever send production writes.\nMeasured limit: one local fixture; runtime effectiveness is UNASSESSED.\nHistory: 2026-09-18, issue #42 recorded the schema change.\nFormal reference: https://example.test/spec/v1'.splitlines())
    # YAML |- 不提供末尾换行；禁止编辑的 fixture 必须保留原始字节。
    equal(Path("fixtures/recorded.json").read_bytes(), b'{"recorded_at":"2026-09-18","expected":"This PR is fixture payload"}')

if __name__ == '__main__':
    try:
        grade(read_result())
    except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
        print('fixture assertion failed:', exc, file=sys.stderr)
        sys.exit(1)
    print('fixture assertions passed')
