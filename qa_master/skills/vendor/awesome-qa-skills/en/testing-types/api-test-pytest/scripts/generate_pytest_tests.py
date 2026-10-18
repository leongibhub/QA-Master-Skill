#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from api_case_contract import contract_errors, endpoints_from, incomplete_message, fail_incomplete

def _safe_name(method, path, idx):
    return re.sub(r"[^a-z0-9]+", "_", f"{method}_{path}_{idx}".lower()).strip("_")

def _case_block(method, path, name, endpoint=None):
    ep = endpoint or {}
    lines = [f"def test_{name}(api_client):"]
    errors = contract_errors(method, path, ep)
    if errors:
        return "\n".join(lines + ["    import pytest", f"    pytest.fail({incomplete_message(errors)!r})", ""])
    kwargs = []
    if ep.get('headers'):
        kwargs.append(f"headers={ep['headers']!r}")
    if ep.get('headers_env'):
        lines.append("    import os")
        lines.append(f"    env_headers = {{k: os.environ[v] for k, v in {ep['headers_env']!r}.items()}}")
        lines.append(f"    env_headers.update({ep.get('headers', {})!r})")
        kwargs = ["headers=env_headers"]
    if 'body' in ep:
        key = 'json' if ep.get('body_encoding', 'json') == 'json' else 'data'
        kwargs.append(f"{key}={ep['body']!r}")
    suffix = ', ' + ', '.join(kwargs) if kwargs else ''
    lines.append(f"    resp = api_client.request({method.upper()!r}, {path!r}{suffix})")
    lines.append(f"    assert resp.status_code in {ep['expected_statuses']!r}")
    if 'expected_json' in ep:
        lines.append(f"    assert resp.json() == {ep['expected_json']!r}")
    if ep.get('max_response_ms') is not None:
        lines.append(f"    assert resp.elapsed.total_seconds() * 1000 <= {ep['max_response_ms']!r}")
    return "\n".join(lines) + "\n\n"

def main():
    parser = argparse.ArgumentParser(description="Generate contract-derived API smoke tests; incomplete scaffolds exit nonzero")
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    endpoints = endpoints_from(json.loads(args.input.read_text(encoding='utf-8')))
    lines = ['"""Generated smoke assertions; add reviewed business/schema checks as required."""', '']
    for i, ep in enumerate(endpoints, 1):
        method, path = str(ep.get('method', '')), str(ep.get('path', ''))
        lines.append(_case_block(method, path, _safe_name(method, path, i), ep))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(args.output)
    fail_incomplete(endpoints)

if __name__ == '__main__': main()
