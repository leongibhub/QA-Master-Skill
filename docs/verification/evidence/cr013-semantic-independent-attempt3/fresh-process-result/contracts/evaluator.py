"""DES-060 process-free semantic quality evaluator.

This module deliberately evaluates only published, source-bound JSON.  It has
no model, process, network, state, adapter, or legacy-grade dependency.
"""
from __future__ import annotations

import argparse
import hashlib
from importlib import resources
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
_LOCATOR = re.compile(r"^(?:[A-Za-z0-9][A-Za-z0-9_.-]*)(?:/[A-Za-z0-9][A-Za-z0-9_.-]*)*$")
_HEX = re.compile(r"^[0-9a-f]{64}$")
_SECRET = {"password", "token", "cookie", "private_key", "private-key", "privatekey"}
_CLAIMS = {"rating", "score", "winner", "quality_grade", "approval", "execution_result", "superiority"}
_CATEGORIES = ("REQUIREMENTS_CONFLICTS", "METHOD_SELECTION", "FUNCTIONAL_API_INTEGRATION",
               "SECURITY_SCOPE_AUTHORITY", "RECOVERY_REGRESSION", "NON_FUNCTIONAL",
               "DELIVERABLE_USABILITY")
_DIMENSIONS = ("SHAPE", "SEMANTIC", "USABILITY", "PROVENANCE")
_READINESS = {"DESIGN_READY", "STATIC_REVIEW", "BLOCKED_ORACLE_MISSING"}
_MAX = 2 * 1024 * 1024


class SemanticQualityError(ValueError):
    def __init__(self, code): self.code = code; super().__init__(code)


def _fail(code): raise SemanticQualityError(code)
def _sha(data): return hashlib.sha256(data).hexdigest()
def _canon(value):
    try: return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError): _fail("INVALID_BUNDLE")
def _exact(value, keys, code="INVALID_BUNDLE"):
    if not isinstance(value, dict) or set(value) != set(keys): _fail(code)
def _id(value, code="INVALID_BUNDLE"):
    if not isinstance(value, str) or not _ID.fullmatch(value): _fail(code)
    return value
def _text(value, code="INVALID_BUNDLE"):
    if not isinstance(value, str) or not value or len(value) > 20000: _fail(code)
    return value
def _digest(value, code="INVALID_BUNDLE"):
    if not isinstance(value, str) or not _HEX.fullmatch(value): _fail(code)
    return value
def _locator(value, code="INVALID_BUNDLE"):
    if not isinstance(value, str) or len(value) > 512 or not _LOCATOR.fullmatch(value): _fail(code)
    return value
def _unique(values, limit=64, code="INVALID_BUNDLE"):
    if not isinstance(values, list) or len(values) > limit or any(not isinstance(x, str) for x in values) or len(values) != len(set(values)): _fail(code)
    return sorted(values)
def _linked(path):
    return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _pairs(rows):
    value = {}
    for key, item in rows:
        if key in value:
            _fail("DUPLICATE_JSON_KEY")
        value[key] = item
    return value


SECRET_KEYS = frozenset(("password passwd token access_token refresh_token api_key authorization cookie private_key client_secret credential presigned_url").split())
def _runtime_redact(raw):
    """Withhold the entire artifact on a known sensitive pattern; never guess prose safety."""
    patterns = [
        rb'(?i)["\x27]?(?:password|passwd|access_token|refresh_token|api_key|authorization|cookie|private_key|client_secret|credential|presigned_url|token)["\x27]?\s*[:=]\s*[^\s,}]+',
        rb'(?i)\b(?:bearer|basic)\s+[A-Za-z0-9+/_.=-]{8,}',
        rb'(?i)https?://[^\s/:]+:[^\s/@]+@',
        rb'(?i)[?&](?:token|key|signature|sig|x-amz-signature|access_token)=',
        rb'\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{12,})',
        rb'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----',
    ]
    def suspicious(data, depth=0):
        if depth > 32:
            return True  # excessive encoded nesting cannot be safely retained
        # Normalize bounded JSON escapes even in malformed/mixed output, which
        # cannot safely wait for a successful JSON parser before withholding.
        normalized = data
        try:
            for _ in range(8):
                changed = re.sub(rb'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m[1], 16)).encode('utf-8'), normalized)
                changed = changed.replace(b'\\/', b'/').replace(b'\\"', b'"')
                if changed == normalized:
                    break
                normalized = changed
            else:
                return True
        except UnicodeError:
            return True
        if any(re.search(pattern, normalized) for pattern in patterns):
            return True
        if any(re.search(pattern, data) for pattern in patterns):
            return True
        def walk(value):
            if isinstance(value, dict):
                return any(key.casefold() in SECRET_KEYS or walk(child) for key, child in value.items())
            if isinstance(value, list):
                return any(walk(child) for child in value)
            if isinstance(value, str):
                return suspicious(value.encode('utf-8'), depth+1)
            return False
        # Final JSON and each JSONL event are decoded before scanning. This also
        # inspects JSON strings containing the agent's escaped final response.
        for line in [data, *data.splitlines()]:
            secret_key = False
            def pairs(rows):
                nonlocal secret_key
                secret_key |= any(key.casefold() in SECRET_KEYS for key, _ in rows)
                return dict(rows)
            try:
                decoded = json.loads(line, object_pairs_hook=pairs)
                if secret_key or walk(decoded):
                    return True
            except (ValueError, UnicodeError):
                if secret_key:
                    return True
                continue
            except RecursionError:
                return True
        return False
    if suspicious(raw):
        safe = b'{"artifact_withheld":"CONTROLLED_SECRET_PATTERN"}\n'
        return safe, {'state': 'REDACTED', 'transform_id': 'WHOLE_ARTIFACT_V1', 'original_byte_count': len(raw), 'original_sha256': _sha(raw)}
    return raw, {'state': 'UNCHANGED', 'transform_id': 'NONE', 'original_byte_count': None, 'original_sha256': None}



# Strict v4 helpers replace the initial compatibility definitions above.
def _scan(raw):
    if not isinstance(raw, bytes): _fail('INVALID_BUNDLE')
    if _runtime_redact(raw)[1]['state'] != 'UNCHANGED': _fail('PROHIBITED_INPUT_PATTERN')


def _typed_safe(value, depth=0, nodes=None):
    nodes = [0] if nodes is None else nodes
    nodes[0] += 1
    if depth > 16 or nodes[0] > 4096: _fail('COUNT_LIMIT')
    if isinstance(value, str):
        if len(value) > 20000 or any(0xD800 <= ord(c) <= 0xDFFF for c in value): _fail('INVALID_BUNDLE')
    elif type(value) is int:
        if abs(value) >= 10 ** 34: _fail('COUNT_LIMIT')
    elif isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str): _fail('INVALID_BUNDLE')
            if key.casefold() in SECRET_KEYS | _SECRET | _CLAIMS: _fail('PROHIBITED_FIELD')
            _typed_safe(key, depth + 1, nodes)
            _typed_safe(child, depth + 1, nodes)
    elif isinstance(value, list):
        for child in value: _typed_safe(child, depth + 1, nodes)
    elif value is not None and type(value) is not bool: _fail('INVALID_BUNDLE')


def _parse(raw, *, typed_bound=False, scan=True):
    if not isinstance(raw, bytes) or len(raw) > _MAX: _fail('SIZE_LIMIT')
    if scan: _scan(raw)
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs,
                           parse_float=lambda _: _fail('INVALID_BUNDLE'),
                           parse_constant=lambda _: _fail('INVALID_BUNDLE'),
                           parse_int=lambda text: _fail('INVALID_BUNDLE') if text == '-0' else int(text) if len(text.lstrip('-')) <= 34 else _fail('COUNT_LIMIT'))
    except (UnicodeError, ValueError, RecursionError) as exc:
        if isinstance(exc, SemanticQualityError): raise
        _fail('INVALID_BUNDLE')
    # Whole documents may contain 256 separately bounded typed values.
    _document_safe(value)
    if typed_bound: _typed_safe(value)
    return value


def _document_safe(value, depth=0, nodes=None):
    nodes = [0] if nodes is None else nodes
    nodes[0] += 1
    if depth > 32 or nodes[0] > 1048576: _fail('COUNT_LIMIT')
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str): _fail('INVALID_BUNDLE')
            if key.casefold() in SECRET_KEYS | _SECRET | _CLAIMS: _fail('PROHIBITED_FIELD')
            _document_safe(key, depth + 1, nodes)
            _document_safe(child, depth + 1, nodes)
    elif isinstance(value, list):
        for child in value: _document_safe(child, depth + 1, nodes)
    elif isinstance(value, str):
        if len(value) > 20000 or any(0xD800 <= ord(c) <= 0xDFFF for c in value): _fail('INVALID_BUNDLE')
    elif type(value) is int:
        if abs(value) >= 10 ** 34: _fail('COUNT_LIMIT')
    elif value is not None and type(value) is not bool: _fail('INVALID_BUNDLE')


def _check_path(path):
    path = Path(os.path.abspath(path))
    for item in reversed((path, *path.parents)):
        try:
            if _linked(item): _fail('LINK_FORBIDDEN')
        except FileNotFoundError: continue
        except OSError: _fail('LOCAL_IO_FAILURE')
    return path


def _opaque(path, limit=_MAX):
    path = _check_path(path)
    try:
        with path.open('rb') as stream: raw = stream.read(limit + 1)
    except FileNotFoundError: _fail('LOCAL_INPUT_MISSING')
    except OSError: _fail('LOCAL_IO_FAILURE')
    if len(raw) > limit: _fail('SIZE_LIMIT')
    _scan(raw)
    return raw


def _load(path, limit=_MAX):
    raw = _opaque(path, limit)
    return raw, _parse(raw)


def _relative(base, locator):
    locator = _locator(locator)
    base = _check_path(base)
    candidate = _check_path(base / locator)
    if not candidate.is_relative_to(base): _fail('PATH_ESCAPE')
    return candidate


def _typed(kind, value):
    try: _typed_safe(value)
    except SemanticQualityError: return False
    if kind == 'BOOLEAN': return type(value) is bool
    if kind == 'INTEGER': return type(value) is int
    if kind == 'DECIMAL':
        return isinstance(value, str) and bool(re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]*[1-9])?', value)) and value != '-0'
    if kind == 'STRING': return isinstance(value, str) and bool(value)
    if kind == 'STRING_SET':
        return isinstance(value, list) and len(value) <= 256 and all(isinstance(x, str) and x for x in value) and value == sorted(set(value))
    return kind == 'JSON'


def _asset(name):
    try:
        entry = resources.files('qa_master').joinpath('semantic_quality_assets', name)
        if isinstance(entry, Path): _check_path(entry)
        with entry.open('rb') as stream: raw = stream.read(_MAX + 1)
    except (OSError, ModuleNotFoundError): _fail('CONTRACT_ASSET_MISSING')
    value = _parse(raw, scan=False)
    if _canon(value) + b'\n' != raw: _fail('CONTRACT_BINDING_MISMATCH')
    return raw, value


_ASSET_DIGESTS = {'contract.json': 'ec9d623230989ab75d0526a64531680280bfb38dde4e4b9f1a1c502e0433804a', 'projection.json': '25aa3f1b01dbbe36d75c3e73f73d9256ded70a1d1780804d4f8c93c217ca4c55', 'legacy-paired-projection.json': 'de207a596e3e39203a0b6fecd2955a066c68e0096897d3695caa74fbbbe1f8f3', 'normalizer.json': 'a3c9d024e130425c3bc9594e775021e06869485c1f0681655971b97527b2c2d9', 'result-schema.json': 'fd356165b1a97c7cd6f7e66aa7e326d3a427d890b5f57e4e7281e703af36247d', 'secret-scanner.json': 'fb26ef33f478e3c0340e02f70c0039cebb1b409b58991a2f68225d586fbd2176'}

def fixed_assets():
    names = {'contract': 'contract.json', 'projection': 'projection.json',
             'legacy_projection': 'legacy-paired-projection.json', 'normalizer': 'normalizer.json',
             'secret_scanner': 'secret-scanner.json', 'result_schema': 'result-schema.json'}
    result = {'raw': {}}
    for key, name in names.items():
        raw, value = _asset(name)
        if _sha(raw) != _ASSET_DIGESTS[name]:
            _fail("PROJECTION_BINDING_MISMATCH" if key in ("projection", "legacy_projection") else "CONTRACT_BINDING_MISMATCH")
        result[key] = value
        result[key + '_sha256'] = _sha(raw)
        result['raw'][name] = raw
    expected = {'contract': ('contract_id', 'semantic-quality-v1'),
                'projection': ('projection_id', 'qa-quality-case-gap-v1'),
                'legacy_projection': ('projection_id', 'paired-neutral-envelope-v1'),
                'normalizer': ('normalizer_id', 'qa-quality-normalizer-v1'),
                'secret_scanner': ('secret_scanner_id', 'qa-quality-secret-scanner-v1'),
                'result_schema': ('result_schema_id', 'semantic-quality-result-v1')}
    for name, (field, identity) in expected.items():
        value = result[name]
        if not isinstance(value, dict) or type(value.get('schema_version')) is not int or value['schema_version'] != 1 or value.get(field) != identity:
            _fail('CONTRACT_BINDING_MISMATCH')
    return result


def _refs(value, universe, code='UNKNOWN_REFERENCE'):
    refs = _unique(value, code=code)
    if any(not _ID.fullmatch(ref) or ref not in universe for ref in refs): _fail(code)
    return refs


def validate_state(raw, bundle, response_raw, source_raw, assets):
    """Validate retained bytes and derive indexes without reading any local path."""
    parsed = _parse(raw)
    if _canon(parsed) != _canon(bundle): _fail('BUNDLE_INTEGRITY_FAILURE')
    _exact(bundle, {'schema_version', 'evaluation_id', 'fixture_class', 'created_at_utc', 'contract', 'response', 'sources', 'facts', 'category_applicability', 'obligations'})
    if type(bundle['schema_version']) is not int or bundle['schema_version'] != 1 or bundle['fixture_class'] not in ('PUBLIC_DEVELOPMENT', 'INDEPENDENT_HOLDOUT', 'PRODUCT_TEST'): _fail('INVALID_BUNDLE')
    from datetime import datetime
    stamp = bundle['created_at_utc']
    if not isinstance(stamp, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', stamp): _fail('INVALID_BUNDLE')
    try: datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError: _fail('INVALID_BUNDLE')
    _id(bundle['evaluation_id'])
    contract = bundle['contract']
    _exact(contract, {name + suffix for name in ('contract', 'projection', 'normalizer', 'result_schema', 'secret_scanner') for suffix in ('_id', '_sha256')})
    for name in ('contract', 'normalizer', 'result_schema', 'secret_scanner'):
        if contract[name + '_id'] != assets[name][name + '_id'] or contract[name + '_sha256'] != assets[name + '_sha256']: _fail('CONTRACT_BINDING_MISMATCH')
    registry = {assets[name]['projection_id']: assets[name + '_sha256'] for name in ('projection', 'legacy_projection')}
    projection = _id(contract['projection_id'])
    if projection not in registry: _fail('UNKNOWN_PROJECTION')
    if contract['projection_sha256'] != registry[projection]: _fail('PROJECTION_BINDING_MISMATCH')
    response = bundle['response']
    _exact(response, {'state', 'source_path', 'byte_count', 'sha256', 'declared_projection_id'})
    declared = _id(response['declared_projection_id'])
    if declared not in registry: _fail('UNKNOWN_PROJECTION')
    if declared != projection: _fail('PROJECTION_BINDING_MISMATCH')
    if response['state'] == 'PRESENT':
        _locator(response['source_path']); _digest(response['sha256'])
        if type(response['byte_count']) is not int or not 0 <= response['byte_count'] <= _MAX: _fail('INVALID_BUNDLE')
        if not isinstance(response_raw, bytes) or len(response_raw) != response['byte_count'] or _sha(response_raw) != response['sha256']: _fail('RESPONSE_INTEGRITY_FAILURE')
        _scan(response_raw)
        _response_policy(response_raw)
    elif response['state'] == 'ABSENT':
        if response_raw is not None or any(response[key] is not None for key in ('source_path', 'byte_count', 'sha256')): _fail('INVALID_BUNDLE')
    else: _fail('INVALID_BUNDLE')
    for field in ('sources', 'facts', 'obligations'):
        if not isinstance(bundle[field], list) or len(bundle[field]) > 256: _fail('COUNT_LIMIT')
    sources = {}
    if not isinstance(source_raw, dict): _fail('INVALID_BUNDLE')
    total = 0
    for source in bundle['sources']:
        _exact(source, {'id', 'kind', 'state', 'locator', 'sha256'})
        sid = _id(source['id'])
        if sid in sources or source['kind'] not in ('requirement', 'risk', 'contract', 'model', 'guard', 'effect', 'change', 'defect', 'evidence', 'other'): _fail('INVALID_BUNDLE')
        if source['state'] == 'AVAILABLE':
            _locator(source['locator']); _digest(source['sha256'])
            data = source_raw.get(sid)
            if not isinstance(data, bytes) or _sha(data) != source['sha256']: _fail('SOURCE_INTEGRITY_FAILURE')
            total += len(data)
            if len(data) > _MAX or total > 4 * 1024 * 1024: _fail('SIZE_LIMIT')
            _scan(data)
        elif source['state'] != 'NOT_AVAILABLE' or source['locator'] is not None or source['sha256'] is not None: _fail('INVALID_BUNDLE')
        sources[sid] = source
    if set(source_raw) != {sid for sid, row in sources.items() if row['state'] == 'AVAILABLE'}: _fail('SOURCE_INTEGRITY_FAILURE')
    facts = {}
    for fact in bundle['facts']:
        _exact(fact, {'id', 'source_ids', 'category', 'value_type', 'value', 'scope'})
        fid = _id(fact['id'])
        if fid in facts or fact['category'] not in _CATEGORIES or not _typed(fact['value_type'], fact['value']): _fail('INVALID_BUNDLE')
        refs = _refs(fact['source_ids'], sources)
        if not refs or any(sources[x]['state'] != 'AVAILABLE' for x in refs): _fail('UNKNOWN_REFERENCE')
        _text(fact['scope']); facts[fid] = fact
    obligations, checks = {}, set()
    by_category = {category: [] for category in _CATEGORIES}
    for item in bundle['obligations']:
        _exact(item, {'id', 'category', 'interpretation', 'source_ids', 'source_fact_ids', 'oracle_state', 'required_gap_reason', 'check_id', 'operator', 'expected_fact_ids', 'allowed_readiness', 'case_required'})
        oid = _id(item['id'])
        if oid in obligations or item['category'] not in _CATEGORIES or type(item['case_required']) is not bool: _fail('INVALID_ORACLE_STATE')
        _text(item['interpretation'])
        src = _refs(item['source_ids'], sources, 'INVALID_ORACLE_STATE')
        refs = _refs(item['source_fact_ids'], facts, 'INVALID_ORACLE_STATE')
        expected = _refs(item['expected_fact_ids'], facts, 'INVALID_ORACLE_STATE')
        allfacts = set(refs) | set(expected)
        if not src or any(facts[x]['category'] != item['category'] or not set(facts[x]['source_ids']) <= set(src) for x in allfacts): _fail('INVALID_ORACLE_STATE')
        readiness = _unique(item['allowed_readiness'])
        if not readiness or set(readiness) - _READINESS: _fail('INVALID_ORACLE_STATE')
        oracle = item['oracle_state']
        available = all(sources[x]['state'] == 'AVAILABLE' for x in src)
        values = {_canon([facts[x]['value_type'], facts[x]['value']]) for x in expected}
        types = {facts[x]['value_type'] for x in expected}
        if oracle == 'DETERMINATE':
            check = _id(item['check_id'], 'INVALID_ORACLE_STATE')
            if check in checks or not available or item['required_gap_reason'] is not None: _fail('INVALID_ORACLE_STATE')
            checks.add(check)
            if item['operator'] not in ('EQUALS', 'ONE_OF') or not expected or len(types) != 1: _fail('INVALID_OPERATOR')
            if item['operator'] == 'EQUALS' and len(expected) != 1 or item['operator'] == 'ONE_OF' and len(expected) > 16: _fail('INVALID_OPERATOR')
            if len(values) != len(expected): _fail('DUPLICATE_EXPECTED_VALUE')
        else:
            if item['check_id'] is not None or item['operator'] is not None: _fail('INVALID_ORACLE_STATE')
            reason = item['required_gap_reason']
            if oracle == 'ORACLE_MISSING':
                if not available or expected or reason != 'ORACLE_MISSING' or set(readiness) != {'BLOCKED_ORACLE_MISSING'}: _fail('INVALID_ORACLE_STATE')
            elif oracle == 'CONFLICT':
                fact_sources = {sid for fid in expected for sid in facts[fid]['source_ids']}
                if not available or len(src) < 2 or len(expected) < 2 or len(values) < 2 or len(types) != 1 or len(fact_sources) < 2 or reason != 'CONFLICT': _fail('INVALID_ORACLE_STATE')
            elif oracle == 'UNSCORABLE':
                if expected or reason not in ('SOURCE_MISSING', 'UNSUPPORTED_CATEGORY') or reason == 'SOURCE_MISSING' and available: _fail('INVALID_ORACLE_STATE')
            else: _fail('INVALID_ORACLE_STATE')
        obligations[oid] = item
        by_category[item['category']].append(item)
    cats = bundle['category_applicability']
    code = 'CATEGORY_OBLIGATION_MISMATCH'
    if not isinstance(cats, list) or len(cats) != len(_CATEGORIES) or any(not isinstance(row, dict) for row in cats) or [row.get('category') for row in cats] != list(_CATEGORIES): _fail(code)
    for row in cats:
        _exact(row, {'category', 'state', 'reason', 'source_ids', 'fact_ids'}, code)
        src = _refs(row['source_ids'], sources, code)
        refs = _refs(row['fact_ids'], facts, code)
        if not src or any(facts[x]['category'] != row['category'] or not set(facts[x]['source_ids']) <= set(src) for x in refs): _fail(code)
        items = by_category[row['category']]
        states = {item['oracle_state'] for item in items}
        if items:
            if row['source_ids'] != sorted({x for item in items for x in item['source_ids']}) or row['fact_ids'] != sorted({x for item in items for x in item['source_fact_ids'] + item['expected_fact_ids']}): _fail(code)
        state = row['state']
        if state == 'APPLICABLE':
            if 'DETERMINATE' not in states or row['reason'] is not None: _fail(code)
        else:
            _text(row['reason'], code)
            if state == 'NOT_APPLICABLE':
                if items: _fail(code)
            elif state == 'ORACLE_MISSING':
                if states != {'ORACLE_MISSING'}: _fail(code)
            elif state == 'UNSCORABLE':
                if 'DETERMINATE' in states or not states & {'CONFLICT', 'UNSCORABLE'}: _fail(code)
            else: _fail(code)
    return {'raw': raw, 'bundle': bundle, 'assets': assets, 'facts': facts, 'obligations': obligations, 'sources': sources, 'source_raw': source_raw, 'response_raw': response_raw, 'supported': projection == assets['projection']['projection_id']}


def _validate_bundle(path):
    path = _check_path(path)
    raw, bundle = _load(path)
    base = path.parent
    # Validate descriptor shapes before indexing or doing any input read.
    if not isinstance(bundle, dict): _fail('INVALID_BUNDLE')
    response = bundle.get('response')
    _exact(response, {'state', 'source_path', 'byte_count', 'sha256', 'declared_projection_id'})
    paths = [path]
    response_raw = None
    if response['state'] == 'PRESENT':
        item = _relative(base, response['source_path']); paths.append(item)
        response_raw = _opaque(item)
    rows = bundle.get('sources')
    if not isinstance(rows, list) or len(rows) > 256: _fail('COUNT_LIMIT')
    source_raw, total = {}, 0
    for source in rows:
        _exact(source, {'id', 'kind', 'state', 'locator', 'sha256'})
        sid = _id(source['id'])
        if source['state'] == 'AVAILABLE':
            item = _relative(base, source['locator']); paths.append(item)
            data = _opaque(item)
            total += len(data)
            if total > 4 * 1024 * 1024: _fail('SIZE_LIMIT')
            source_raw[sid] = data
    state = validate_state(raw, bundle, response_raw, source_raw, fixed_assets())
    state.update(base=base, input_paths=paths)
    return state


def _walk_safe(value, depth=0, nodes=None):
    """Whole-envelope security checks; typed values have separate bounds."""
    return _document_safe(value, depth, nodes)


def _response_policy(raw):
    """Reject controlled claim keys without classifying malformed JSON as input failure."""
    try: value = json.loads(raw.decode('utf-8'))
    except (ValueError, UnicodeError, RecursionError): return
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            if any(key.casefold() in SECRET_KEYS | _SECRET | _CLAIMS for key in item): _fail('PROHIBITED_FIELD')
            pending.extend(item.values())
        elif isinstance(item, list): pending.extend(item)

# TASK061 derivation fragment, integrated before freeze.
_MISSING_FIELDS = {'SOURCE','SETUP','DATA','EXPECTED_ORACLE','TARGET_INTERFACE','OBSERVABLE_LOCATOR','CLEANUP_INVENTORY','NON_FUNCTIONAL_THRESHOLD'}
_CASE_KEYS = {'case_id','obligation_ids','category','readiness','setup','preconditions','data','actions','expected_oracle','cleanup','source_fact_ids','gap_ids','missing_fields','extensions'}
_GAP_KEYS = {'gap_id','obligation_ids','reason','fact_ids','source_ids','needed_evidence','evidence_pointer'}
_OBS_KEYS = {'check_id','value_type','value','source_fact_ids'}


def _valid_id(value):
    return isinstance(value, str) and bool(_ID.fullmatch(value))


def _valid_refs(value):
    return isinstance(value,list) and len(value)<=64 and all(_valid_id(x) for x in value) and len(value)==len(set(value))


def _binding(value, known, required=()):
    return _valid_refs(value) and all(ref in known for ref in value) and set(required)<=set(value)


def _diagnostic(code, channel='root', index=None, item_id=None, member=None):
    return dict(code=code,channel=channel,index=index,item_id=item_id if _valid_id(item_id) else None,member=member)


def _diag_key(d):
    return d['code'],d['channel'], -1 if d['index'] is None else d['index'],d['item_id'] or '', d['member'] or ''


def _normalize(state):
    normal={'fatal':False,'shape':[],'items':[],'channels':{},'observations':{},'cases':{},'gaps':{},'value':None}
    bundle=state['bundle']
    check_ids={o['check_id'] for o in state['obligations'].values()}
    if bundle['response']['state']=='ABSENT' or not state['supported']:
        return normal
    try:
        value=_parse(state['response_raw'])
        if not isinstance(value,dict) or type(value.get('schema_version')) is not int or value['schema_version']!=1 or not _valid_id(value.get('artifact_id')):
            raise ValueError()
    except (ValueError,UnicodeError,RecursionError) as error:
        if isinstance(error,SemanticQualityError) and error.code in {'PROHIBITED_FIELD','PROHIBITED_INPUT_PATTERN'}: raise
        normal['fatal']=True
        normal['shape'].append(_diagnostic('MALFORMED_KNOWN_RESPONSE_FATAL'))
        return normal
    normal['value']=value
    outer={'schema_version','artifact_id','artifact_state','execution_state','summary','observations','cases','gaps','extensions'}
    if set(value)-outer: normal['shape'].append(_diagnostic('UNKNOWN_MEMBER'))
    for member in ('summary','artifact_state','execution_state','extensions'):
        v=value.get(member)
        valid=isinstance(v,dict) if member=='extensions' else isinstance(v,str) and bool(v)
        if member=='artifact_state': valid=v=='DRAFT_UNAPPROVED'
        if member=='execution_state': valid=v=='NOT_EXECUTED'
        if not valid: normal['shape'].append(_diagnostic('INVALID_ENVELOPE_MEMBER',member=member))
    for channel,keys,identity in [('observations',_OBS_KEYS,'check_id'),('cases',_CASE_KEYS,'case_id'),('gaps',_GAP_KEYS,'gap_id')]:
        rows=value.get(channel)
        if not isinstance(rows,list):
            normal['channels'][channel]=False
            normal['shape'].append(_diagnostic('CHANNEL_UNAVAILABLE',channel))
            continue
        if len(rows)>256:
            normal['fatal']=True; normal['shape']=[_diagnostic('MALFORMED_KNOWN_RESPONSE_FATAL')];normal['value']=None
            return normal
        normal['channels'][channel]=True
        identities={}
        for index,row in enumerate(rows):
            if not isinstance(row,dict):
                normal['shape'].append(_diagnostic('ITEM_NOT_OBJECT',channel,index)); continue
            item_id=row.get(identity)
            if set(row)-keys: normal['shape'].append(_diagnostic('UNKNOWN_ITEM_MEMBER',channel,index,item_id))
            if not _valid_id(item_id): normal['items'].append(_diagnostic('INVALID_ITEM_ID',channel,index,None,identity))
            else: identities.setdefault(item_id,[]).append(index)
            for member in keys-set(row): normal['items'].append(_diagnostic('MISSING_ITEM_MEMBER',channel,index,item_id,member))
            if channel=='cases':
                for section_name in ('setup','data','cleanup','expected_oracle'):
                    section=row.get(section_name)
                    allowed={'state','items','reason','oracle_fact_ids'} if section_name=='expected_oracle' else {'state','items','reason'}
                    if isinstance(section,dict) and set(section)-allowed:
                        normal['shape'].append(_diagnostic('UNKNOWN_ITEM_MEMBER',channel,index,item_id,section_name))
                for section_name in ('setup','data','cleanup','expected_oracle','preconditions','actions'):
                    section=row.get(section_name)
                    claims=section.get('items') if isinstance(section,dict) else section
                    if isinstance(claims,list) and any(isinstance(c,dict) and set(c)-{'text','source_fact_ids'} for c in claims):
                        normal['shape'].append(_diagnostic('UNKNOWN_ITEM_MEMBER',channel,index,item_id,section_name))
            wrapped=(index,row)
            if channel=='observations':
                if _valid_id(item_id):
                    normal['observations'].setdefault(item_id,[]).append(wrapped)
                    if item_id not in check_ids:
                        normal['items'].append(_diagnostic('UNBOUND_OBSERVATION',channel,index,item_id))
                if not _binding(row.get('source_fact_ids'),state['facts']): normal['items'].append(_diagnostic('SOURCE_BINDING_INVALID',channel,index,item_id,'source_fact_ids'))
                try: valid=_typed(row.get('value_type'),row.get('value'))
                except (TypeError,ValueError): valid=False
                if not valid: normal['items'].append(_diagnostic('OBSERVED_VALUE_INVALID',channel,index,item_id,'value'))
            else:
                refs=row.get('obligation_ids')
                if not _valid_refs(refs) or not refs or any(ref not in state['obligations'] for ref in refs): normal['items'].append(_diagnostic('INVALID_OBLIGATION_BINDING',channel,index,item_id,'obligation_ids'))
                if isinstance(refs,list):
                    for ref in set(x for x in refs if isinstance(x,str) and x in state['obligations']): normal[channel].setdefault(ref,[]).append(wrapped)
        normal[channel+'_ids']=identities
        for item_id,indexes in identities.items():
            if len(indexes)>1:
                for index in indexes: normal['items'].append(_diagnostic('AMBIGUOUS_ITEM_ID',channel,index,item_id,identity))
    normal['shape'].sort(key=_diag_key)
    return normal


def _claims_valid(items,state):
    return isinstance(items,list) and len(items)<=64 and all(isinstance(x,dict) and set(x)=={'text','source_fact_ids'} and isinstance(x['text'],str) and 0<len(x['text'])<=20000 and _valid_refs(x['source_fact_ids']) and bool(x['source_fact_ids']) for x in items)


def _indexed_refs(value, universe):
    """Read one serialized reference list once; masks have at most 256 bits."""
    syntax=_valid_refs(value)
    mask=0
    known=syntax
    if syntax:
        for ref in value:
            bit=universe.get(ref)
            if bit is None: known=False
            else: mask |= bit
    return {'syntax':syntax,'known':known,'mask':mask,'nonempty':syntax and bool(value)}


def _mask_contains(actual, required):
    return actual & required == required


def _prepare_items(state, normal):
    """Index item-wide shape/binding once; edge validators only read these records."""
    facts={key:1<<index for index,key in enumerate(state['facts'])}
    sources={key:1<<index for index,key in enumerate(state['sources'])}
    obligations={key:1<<index for index,key in enumerate(state['obligations'])}
    all_obligations=(1<<len(obligations))-1
    normal['obligation_index']={}
    for oid,ob in state['obligations'].items():
        normal['obligation_index'][oid]={
            'bit':obligations[oid],
            'required':sum(facts[ref] for ref in set(ob['source_fact_ids'])|set(ob['expected_fact_ids'])),
            'expected':sum(facts[ref] for ref in ob['expected_fact_ids']),
            'sources':sum(sources[ref] for ref in ob['source_ids']),
        }
    unavailable=sum(sources[sid] for sid,row in state['sources'].items() if row['state']!='AVAILABLE')
    prepared={channel:{} for channel in ('observations','cases','gaps')}
    normal['prepared']=prepared
    raw=normal.get('value') or {}
    def items(channel):
        return [row for row in raw.get(channel,[]) if isinstance(row,dict)] if normal['channels'].get(channel) else []
    gap_membership={}
    for row in items('gaps'):
        bindings=_indexed_refs(row.get('obligation_ids'),obligations)
        # Even a malformed item can have valid partial mappings; these match
        # the normalizer's retained, un-repaired binding edges.
        partial=0
        if isinstance(row.get('obligation_ids'),list):
            for oid in row['obligation_ids']:
                if isinstance(oid,str): partial |= obligations.get(oid,0)
        gid=row.get('gap_id')
        if _valid_id(gid): gap_membership[gid]=gap_membership.get(gid,0)|partial
        fact_refs=_indexed_refs(row.get('fact_ids'),facts)
        source_refs=_indexed_refs(row.get('source_ids'),sources)
        reason=row.get('reason')
        agreement=bindings['known'] and all(state['obligations'][oid]['required_gap_reason']==reason for oid in row['obligation_ids'])
        available=reason=='SOURCE_MISSING' or not(source_refs['mask'] & unavailable)
        pointer=row.get('evidence_pointer')
        content=(set(row)==_GAP_KEYS and _valid_id(gid) and len(normal.get('gaps_ids',{}).get(gid,[]))==1
                 and bindings['nonempty'] and agreement and fact_refs['known'] and source_refs['known'] and available
                 and isinstance(row.get('needed_evidence'),str) and 0<len(row['needed_evidence'])<=20000
                 and isinstance(pointer,str) and 0<len(pointer)<=512 and not any(c in pointer for c in ('\\','\n','\r')) and not pointer.startswith('/') and '..' not in pointer.split('/'))
        prepared['gaps'][id(row)]={'content':content,'provenance':bindings['known'] and bindings['nonempty'] and fact_refs['known'] and source_refs['known'] and available,
                                  'facts':fact_refs['mask'],'sources':source_refs['mask'],'reason':reason}
    gap_ids={key:1<<index for index,key in enumerate(normal.get('gaps_ids',{}))}
    for row in items('observations'):
        refs=_indexed_refs(row.get('source_fact_ids'),facts)
        prepared['observations'][id(row)]={'provenance':refs['known'],'facts':refs['mask']}
    for row in items('cases'):
        bindings=_indexed_refs(row.get('obligation_ids'),obligations)
        fact_refs=_indexed_refs(row.get('source_fact_ids'),facts)
        gap_refs=_indexed_refs(row.get('gap_ids'),gap_ids)
        missing=row.get('missing_fields')
        missing_valid=_valid_refs(missing) and missing==sorted(missing) and not(set(missing)-_MISSING_FIELDS)
        category=row.get('category')
        agreement=bindings['known'] and all(state['obligations'][oid]['category']==category for oid in row['obligation_ids'])
        cid=row.get('case_id')
        content=(set(row)==_CASE_KEYS and _valid_id(cid) and len(normal.get('cases_ids',{}).get(cid,[]))==1
                 and bindings['nonempty'] and agreement and isinstance(row.get('extensions'),dict)
                 and fact_refs['syntax'] and gap_refs['syntax'] and missing_valid)
        provenance=bindings['known'] and bindings['nonempty'] and fact_refs['known'] and gap_refs['known']
        def claims(value):
            good=isinstance(value,list) and len(value)<=64
            honest=True
            if isinstance(value,list):
                for claim in value:
                    if not isinstance(claim,dict): good=False;continue
                    refs=_indexed_refs(claim.get('source_fact_ids'),facts)
                    good=good and set(claim)=={'text','source_fact_ids'} and isinstance(claim.get('text'),str) and 0<len(claim['text'])<=20000 and refs['syntax'] and refs['nonempty']
                    honest=honest and refs['known'] and refs['nonempty']
            return good,honest
        needs_gap=False
        source_missing=False
        for name in ('preconditions','actions','setup','data','cleanup','expected_oracle'):
            section=row.get(name)
            section_items=section.get('items') if isinstance(section,dict) else section
            good,honest=claims(section_items)
            provenance=provenance and honest
            if name in ('preconditions','actions'):
                content=content and good and (name!='actions' or bool(section_items))
                continue
            allowed={'state','items','reason','oracle_fact_ids'} if name=='expected_oracle' else {'state','items','reason'}
            section_shape=isinstance(section,dict) and set(section)==allowed
            if not section_shape:
                content=False
                continue
            section_state=section.get('state')
            if section_state=='DEFINED':
                content=content and good and bool(section_items) and section.get('reason') is None
            elif section_state in (('ORACLE_MISSING','CONFLICT') if name=='expected_oracle' else ('NOT_APPLICABLE','SOURCE_MISSING')):
                content=content and section_items==[] and isinstance(section.get('reason'),str) and bool(section['reason'])
                if name!='expected_oracle': needs_gap=needs_gap or not fact_refs['nonempty']
            else: content=False
            if name!='expected_oracle' and section_state=='SOURCE_MISSING': source_missing=True
        oracle=row.get('expected_oracle')
        oracle_refs=_indexed_refs(oracle.get('oracle_fact_ids') if isinstance(oracle,dict) else None,facts)
        oracle_defined=isinstance(oracle,dict) and oracle.get('state')=='DEFINED'
        content=content and oracle_refs['syntax'] and (not oracle_defined or oracle_refs['nonempty'])
        if isinstance(oracle,dict): provenance=provenance and oracle_refs['known']
        readiness=row.get('readiness')
        if readiness=='DESIGN_READY':
            content=content and oracle_defined and not source_missing and missing_valid and not(set(missing)&{'SOURCE','SETUP','DATA','EXPECTED_ORACLE','CLEANUP_INVENTORY','NON_FUNCTIONAL_THRESHOLD'})
        if readiness=='BLOCKED_ORACLE_MISSING':
            content=content and missing_valid and bool(missing)
            needs_gap=True
        gap_mapping=all_obligations
        if gap_refs['syntax']:
            for gid in row['gap_ids']:
                if len(normal.get('gaps_ids',{}).get(gid,[]))!=1:
                    gap_mapping=0
                    provenance=False
                else: gap_mapping &= gap_membership.get(gid,0)
        else: gap_mapping=0
        prepared['cases'][id(row)]={'content':content,'provenance':provenance,'facts':fact_refs['mask'],
                                    'oracle':oracle_refs['mask'],'oracle_defined':oracle_defined,
                                    'category':category,'readiness':readiness,'needs_gap':needs_gap,'gap_mapping':gap_mapping}


def _gap_valid(gap,ob,state,normal):
    item=normal['prepared']['gaps'][id(gap)]
    binding=normal['obligation_index'][ob['id']]
    return item['content'] and _mask_contains(item['facts'],binding['required']) and _mask_contains(item['sources'],binding['sources'])


def _case_valid(case,ob,state,normal):
    item=normal['prepared']['cases'][id(case)]
    return (item['content'] and item['readiness'] in ob['allowed_readiness']
            and (not item['needs_gap'] or normal['exact_gap'][ob['id']])
            and bool(item['gap_mapping'] & normal['obligation_index'][ob['id']]['bit']))


def _artifact_provenance(row,channel,ob,state,normal):
    item=normal['prepared'][channel][id(row)]
    binding=normal['obligation_index'][ob['id']]
    if not item['provenance'] or not _mask_contains(item['facts'],binding['required']): return False
    if channel=='observations': return True
    if channel=='gaps': return item['reason']==ob['required_gap_reason'] and _mask_contains(item['sources'],binding['sources'])
    return item['category']==ob['category'] and (not item['oracle_defined'] or ob['oracle_state']=='DETERMINATE' and _mask_contains(item['oracle'],binding['expected']))


def derive_profile(state):
    """Pure deterministic profile derivation: no I/O and no retained code execution."""
    normal=_normalize(state); bundle=state['bundle']; rows=[]
    # Item-wide work is independent of mapping fan-out.
    _prepare_items(state,normal)
    normal['exact_gap']={}
    gap_validity={}
    case_validity={}
    for oid,ob in (state['obligations'].items() if not normal['fatal'] else ()):
        mapped_gaps=normal['gaps'].get(oid,[])
        for index,gap in mapped_gaps:
            gap_validity[oid,index]=_gap_valid(gap,ob,state,normal)
        normal['exact_gap'][oid]=any(gap_validity[oid,index] for index,_ in mapped_gaps)
        for index,case in normal['cases'].get(oid,[]):
            case_validity[oid,index]=_case_valid(case,ob,state,normal)
    result_id='SQ-'+_identity(state)[:32]
    response_mode='ABSENT' if bundle['response']['state']=='ABSENT' else 'SUPPORTED' if state['supported'] else 'LEGACY_UNSUPPORTED'
    for oid,ob in sorted(state['obligations'].items()):
        obs=normal['observations'].get(ob['check_id'],[]); cases=normal['cases'].get(oid,[]); gaps=normal['gaps'].get(oid,[])
        pointers=['bundle:obligation/'+oid]+['bundle:fact/'+fid for fid in sorted(set(ob['source_fact_ids'])|set(ob['expected_fact_ids']))]
        def emit(dimension,outcome,reason):
            evidence=list(pointers)
            channels= [('observation',obs)] if dimension=='SEMANTIC' else [('case',cases),('gap',gaps)] if dimension=='USABILITY' else [('observation',obs),('case',cases),('gap',gaps)] if dimension=='PROVENANCE' else []
            for channel,items in channels: evidence.extend('response:'+channel+'/'+str(i) for i,_ in items)
            if dimension=='SHAPE': evidence.extend('diagnostic:'+d['code']+'/'+d['channel']+'/'+('root' if d['index'] is None else str(d['index'])) for d in normal['shape'])
            if len(evidence)==len(pointers): evidence.append('diagnostic:'+reason+'/root/root')
            rows.append(dict(obligation_id=oid,category=ob['category'],dimension=dimension,outcome=outcome,reason_code=reason,source_fact_ids=sorted(ob['source_fact_ids']),evidence_pointers=sorted(set(evidence))))
        if response_mode!='SUPPORTED':
            for d in _DIMENSIONS: emit(d,'UNSCORABLE','RESPONSE_ABSENT' if response_mode=='ABSENT' else 'LEGACY_PROJECTION_UNSUPPORTED')
            continue
        if normal['fatal']:
            emit('SHAPE','VIOLATED','MALFORMED_KNOWN_RESPONSE_FATAL')
            for d in _DIMENSIONS[1:]: emit(d,'UNSCORABLE','RESPONSE_SHAPE_DEPENDENCY')
            continue
        emit('SHAPE','VIOLATED' if normal['shape'] else 'SATISFIED','MALFORMED_KNOWN_RESPONSE_RECOVERABLE' if normal['shape'] else 'PROJECTED_SHAPE_VALID')
        oracle=ob['oracle_state']
        if oracle!='DETERMINATE':
            emit('SEMANTIC','ORACLE_MISSING' if oracle=='ORACLE_MISSING' else 'UNSCORABLE',{'ORACLE_MISSING':'SOURCE_ORACLE_MISSING','CONFLICT':'SOURCE_FACT_CONFLICT','UNSCORABLE':'SEMANTIC_RULE_UNAVAILABLE'}[oracle])
            emit('USABILITY','ORACLE_MISSING' if oracle=='ORACLE_MISSING' else 'UNSCORABLE',{'ORACLE_MISSING':'USABLE_ORACLE_UNAVAILABLE','CONFLICT':'USABLE_OUTCOME_CONFLICTING','UNSCORABLE':'USABILITY_RULE_UNAVAILABLE'}[oracle])
        else:
            if not normal['channels'].get('observations'): emit('SEMANTIC','UNSCORABLE','OBSERVATIONS_CHANNEL_UNAVAILABLE')
            elif len(obs)>1: emit('SEMANTIC','VIOLATED','OBSERVATION_AMBIGUOUS')
            elif not obs: emit('SEMANTIC','VIOLATED','OBSERVATION_MISSING')
            else:
                row=obs[0][1]; expected=[state['facts'][x] for x in ob['expected_fact_ids']]
                try: valid=row.get('value_type')==expected[0]['value_type'] and _typed(row.get('value_type'),row.get('value'))
                except (TypeError,ValueError): valid=False
                if not valid: emit('SEMANTIC','VIOLATED','OBSERVED_VALUE_INVALID')
                elif any(_canon(row['value'])==_canon(f['value']) for f in expected): emit('SEMANTIC','SATISFIED','SOURCE_BOUND_VALUE_MATCH')
                else: emit('SEMANTIC','VIOLATED','OBSERVED_VALUE_MISMATCH')
            if not ob['case_required'] and not cases: emit('USABILITY','SATISFIED','CASE_NOT_REQUIRED')
            elif not normal['channels'].get('cases'): emit('USABILITY','UNSCORABLE','CASES_CHANNEL_UNAVAILABLE')
            elif not cases: emit('USABILITY','VIOLATED','REQUIRED_CASE_MISSING')
            elif any(not case_validity[oid,index] for index,_ in cases): emit('USABILITY','VIOLATED','MAPPED_CASE_INVALID' if ob['case_required'] else 'OPTIONAL_CASE_INVALID')
            else: emit('USABILITY','SATISFIED','USABLE_DRAFT_ARTIFACT_PRESENT')
        bad=False
        for channel,items in [('observations',obs),('cases',cases),('gaps',gaps)]:
            for index,row in items:
                if not _artifact_provenance(row,channel,ob,state,normal):
                    bad=True; normal['items'].append(_diagnostic('SOURCE_BINDING_INVALID',channel,index,row.get({'observations':'check_id','cases':'case_id','gaps':'gap_id'}[channel])))
                if channel=='cases' and not case_validity[oid,index]: normal['items'].append(_diagnostic('MAPPED_CASE_INVALID',channel,index,row.get('case_id')))
                if channel=='gaps' and not gap_validity[oid,index]: normal['items'].append(_diagnostic('MAPPED_GAP_INVALID',channel,index,row.get('gap_id')))
        exact=normal['exact_gap'][oid]
        if bad: emit('PROVENANCE','VIOLATED','SOURCE_BINDING_INVALID')
        elif oracle!='DETERMINATE' and normal['channels'].get('gaps') and not exact: emit('PROVENANCE','VIOLATED','REQUIRED_GAP_MISSING')
        elif (oracle=='DETERMINATE' and not normal['channels'].get('observations')) or (ob['case_required'] and not normal['channels'].get('cases')) or (oracle!='DETERMINATE' and not normal['channels'].get('gaps')): emit('PROVENANCE','UNSCORABLE','PROVENANCE_CHANNEL_UNAVAILABLE')
        else: emit('PROVENANCE','SATISFIED',{'ORACLE_MISSING':'MISSING_ORACLE_HONESTLY_REPORTED','CONFLICT':'CONFLICT_HONESTLY_REPORTED','UNSCORABLE':'UNSCORABLE_GAP_HONESTLY_REPORTED','DETERMINATE':'SOURCE_BINDING_COMPLETE'}[oracle])
    unique={_canon(d):d for d in normal['items']}
    return dict(schema_version=1,result_id=result_id,evaluation_id=bundle['evaluation_id'],fixture_class=bundle['fixture_class'],evaluation_state='EVALUATED_DRAFT_ONLY',execution_state='NOT_EXECUTED',claim_status='NOT_ASSERTED',human_rating_status='NOT_EXECUTED',legacy_grade_changed=False,response_mode=response_mode,category_applicability=bundle['category_applicability'],shape_diagnostics=normal['shape'],item_diagnostics=sorted(unique.values(),key=_diag_key),rows=rows,limitations=['DRAFT_ONLY','NO_AGGREGATE','NO_HUMAN_RATING'])

"""Publication/inspection fragment; integrated into semantic_quality.py."""
import uuid

_SQ_ASSETS = {"contract_sha256": "contract.json", "projection_sha256": "projection.json",
              "normalizer_sha256": "normalizer.json", "result_schema_sha256": "result-schema.json",
              "secret_scanner_sha256": "secret-scanner.json"}
_SQ_ROLES = {"bundle.source.json": "BUNDLE_SOURCE", "bundle.canonical.json": "BUNDLE_CANONICAL",
             "response.source.json": "RESPONSE_SOURCE", "response.normalized.json": "RESPONSE_NORMALIZED",
             "profile.json": "PROFILE", "contracts/evaluator.py": "EVALUATOR_IMPLEMENTATION"}
_SQ_ROLES.update({"contracts/" + name: "CONTRACT_ASSET" for name in _SQ_ASSETS.values()})
_SQ_LIMIT = 16 * 1024 * 1024


def _sq_asset_digests(state):
    digests = {key: state["assets"][key] for key in _SQ_ASSETS}
    if state["bundle"]["contract"]["projection_id"] == "paired-neutral-envelope-v1":
        digests["projection_sha256"] = state["assets"]["legacy_projection_sha256"]
    return digests


def _identity(state):
    return _sha(_canon({"bundle_sha256": _sha(state["raw"]),
        "canonical_bundle_sha256": _sha(_canon(state["bundle"])),
        "response_state": state["bundle"]["response"]["state"],
        "response_sha256": None if state["response_raw"] is None else _sha(state["response_raw"]),
        "sources": sorted((key, _sha(value)) for key, value in state["source_raw"].items()),
        "assets": _sq_asset_digests(state),
        "implementation_sha256": _sha(state["implementation_raw"])}))


def _sq_check_path(value):
    path = Path(value)
    if ".." in path.parts:
        _fail("PATH_ESCAPE")
    path = path.absolute()
    for component in reversed((path, *path.parents)):
        try:
            if component.exists() or component.is_symlink():
                if _linked(component):
                    _fail("LINK_FORBIDDEN")
        except OSError:
            _fail("LOCAL_IO_FAILURE")
    return path


def _sq_read(path):
    try:
        with path.open("rb") as stream:
            data = stream.read(_SQ_LIMIT + 1)
        return data
    except OSError:
        _fail("LOCAL_IO_FAILURE")


def _sq_json(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate")
            out[key] = value
        return out
    def constant(value):
        raise ValueError("constant")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)


def _sq_role(name):
    if re.fullmatch(r"sources/[0-9a-f]{64}\.source", name):
        return "SOURCE_BYTES"
    return _SQ_ROLES.get(name)


def _sq_selected_assets(assets, bundle):
    raw = assets["raw"]
    projection = ("legacy-paired-projection.json" if bundle["contract"]["projection_id"] ==
                  "paired-neutral-envelope-v1" else "projection.json")
    return {"contracts/" + name: raw[projection if name == "projection.json" else name]
            for name in _SQ_ASSETS.values()}


def _sq_manifest(state, profile, files):
    return {"schema_version": 1, "result_id": profile["result_id"], "identity_sha256": _identity(state),
        "evaluation_id": state["bundle"]["evaluation_id"], "fixture_class": profile["fixture_class"],
        "bundle_sha256": _sha(state["raw"]), "canonical_bundle_sha256": _sha(files["bundle.canonical.json"]),
        "response_sha256": None if state["response_raw"] is None else _sha(state["response_raw"]),
        "normalized_response_sha256": _sha(files["response.normalized.json"]) if "response.normalized.json" in files else None,
        "profile_sha256": _sha(files["profile.json"]), "contract": state["bundle"]["contract"],
        "asset_sha256": _sq_asset_digests(state),
        "implementation_sha256": _sha(state["implementation_raw"]),
        "files": [{"path": name, "sha256": _sha(data), "byte_count": len(data), "role": _sq_role(name)}
                  for name, data in sorted(files.items())],
        "profile_row_count": len(profile["rows"]), "category_applicability": profile["category_applicability"],
        "shape_diagnostics": profile["shape_diagnostics"], "item_diagnostics": profile["item_diagnostics"],
        "rows": profile["rows"], "limitations": profile["limitations"]}


def _sq_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if _sq_read(path) != data:
        _fail("LOCAL_IO_FAILURE")


def evaluate_state(state, output_root, derive_profile, normalize, implementation_bytes):
    state = dict(state, implementation_raw=implementation_bytes)
    root = _sq_check_path(output_root)
    if root.exists() and not root.is_dir():
        _fail("OUTPUT_PATH_CONFLICT")
    for supplied in state.get("input_paths", []):
        path = _sq_check_path(supplied)
        if root == path or root.is_relative_to(path) or path.is_relative_to(root):
            _fail("OUTPUT_PATH_CONFLICT")
    # Keep outputs away from the input bundle tree, including CR-011 evidence.
    if state.get("base") is not None:
        base = _sq_check_path(state["base"])
        if root == base or root.is_relative_to(base) or base.is_relative_to(root):
            _fail("OUTPUT_PATH_CONFLICT")
    profile = derive_profile(state)
    normal = normalize(state)
    result_id = "SQ-" + _identity(state)[:32]
    target = root / result_id
    _sq_check_path(target)
    if target.exists():
        _fail("RESULT_EXISTS")
    files = {"bundle.source.json": state["raw"], "bundle.canonical.json": _canon(state["bundle"]),
             "profile.json": _canon(profile), "contracts/evaluator.py": implementation_bytes}
    files.update(_sq_selected_assets(state["assets"], state["bundle"]))
    if state["response_raw"] is not None:
        files["response.source.json"] = state["response_raw"]
    if normal is not None and normal.get("value") is not None:
        files["response.normalized.json"] = _canon(normal["value"])
    for data in state["source_raw"].values():
        files["sources/" + _sha(data) + ".source"] = data
    manifest_raw = _canon(_sq_manifest(state, profile, files))
    if sum(map(len, files.values())) + len(manifest_raw) > _SQ_LIMIT:
        _fail("RESULT_SIZE_LIMIT")
    nonce = uuid.uuid4().hex
    reservation = _canon({"result_id": result_id, "owner_nonce": nonce})
    owned = False
    owner_directory = None
    committed = False
    stage = None
    try:
        root.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix=".semantic-quality-", dir=root))
        for name, data in files.items():
            _sq_write(stage / name, data)
        _sq_write(stage / "manifest.json", manifest_raw)
        try:
            target.mkdir()
        except FileExistsError:
            _fail("RESULT_EXISTS")
        info = target.stat()
        owner_directory = (info.st_dev, info.st_ino)
        owned = True
        _sq_write(target / "reservation.json", reservation)
        for name, data in files.items():
            _sq_write(target / name, _sq_read(stage / name))
        _sq_write(target / ".manifest.json", manifest_raw)
        if _sq_read(target / "reservation.json") != reservation:
            _fail("LOCAL_IO_FAILURE")
        (target / "reservation.json").unlink()
        os.replace(target / ".manifest.json", target / "manifest.json")
        committed = True
    except OSError:
        _fail("LOCAL_IO_FAILURE")
    finally:
        if owned and not committed:
            # Missing reservation is legitimate only in our short commit window.
            marker = target / "reservation.json"
            try:
                same_owner = (marker.is_file() and not _linked(marker) and marker.read_bytes() == reservation)
                if not marker.exists():
                    same_owner = (target / ".manifest.json").is_file() and not (target / "manifest.json").exists()
                info = target.lstat()
                same_directory = (info.st_dev, info.st_ino) == owner_directory and not _linked(target)
                if same_owner and same_directory:
                    shutil.rmtree(target)
            except OSError:
                pass
        if stage is not None:
            shutil.rmtree(stage, ignore_errors=True)
    return {"status": "EVALUATED_DRAFT_ONLY", "result_id": result_id,
            "evaluation_id": profile["evaluation_id"], "profile_path": str(target / "profile.json"),
            "row_count": len(profile["rows"])}


def _sq_manifest_structure(manifest):
    """Validate types and controlled shapes before inspecting retained evidence."""
    def require(condition):
        if not condition:
            raise ValueError()
    def digest(value):
        return isinstance(value,str) and bool(_HEX.fullmatch(value))
    def sequence(value, maximum):
        require(isinstance(value,list) and len(value)<=maximum)
    try:
        _document_safe(manifest)
        require(_valid_id(manifest['evaluation_id']))
        require(manifest['fixture_class'] in ('PUBLIC_DEVELOPMENT','INDEPENDENT_HOLDOUT','PRODUCT_TEST'))
        for key in ('identity_sha256','bundle_sha256','canonical_bundle_sha256','profile_sha256','implementation_sha256'):
            require(digest(manifest[key]))
        for key in ('response_sha256','normalized_response_sha256'):
            require(manifest[key] is None or digest(manifest[key]))
        contract=manifest['contract']
        require(isinstance(contract,dict) and set(contract)=={name+suffix for name in ('contract','projection','normalizer','result_schema','secret_scanner') for suffix in ('_id','_sha256')})
        for key,value in contract.items():
            require(digest(value) if key.endswith('_sha256') else _valid_id(value))
        assets=manifest['asset_sha256']
        require(isinstance(assets,dict) and set(assets)==set(_SQ_ASSETS))
        require(all(digest(value) for value in assets.values()))
        count=manifest['profile_row_count']
        require(type(count) is int and 0<=count<=1024)
        categories=manifest['category_applicability']
        sequence(categories,7)
        require(len(categories)==7)
        for row in categories:
            require(isinstance(row,dict) and set(row)=={'category','state','reason','source_ids','fact_ids'})
            require(row['category'] in _CATEGORIES and row['state'] in ('APPLICABLE','NOT_APPLICABLE','ORACLE_MISSING','UNSCORABLE'))
            require(row['reason'] is None or isinstance(row['reason'],str) and 0<len(row['reason'])<=20000)
            require(_valid_refs(row['source_ids']) and _valid_refs(row['fact_ids']))
        for key in ('shape_diagnostics','item_diagnostics'):
            sequence(manifest[key],65536)
            for row in manifest[key]:
                require(isinstance(row,dict) and set(row)=={'code','channel','index','item_id','member'})
                require(_valid_id(row['code']) and row['channel'] in ('root','observations','cases','gaps'))
                require(row['index'] is None or type(row['index']) is int and 0<=row['index']<256)
                require(row['item_id'] is None or _valid_id(row['item_id']))
                require(row['member'] is None or _valid_id(row['member']))
        sequence(manifest['rows'],1024)
        for row in manifest['rows']:
            require(isinstance(row,dict) and set(row)=={'obligation_id','category','dimension','outcome','reason_code','source_fact_ids','evidence_pointers'})
            require(_valid_id(row['obligation_id']) and row['category'] in _CATEGORIES and row['dimension'] in _DIMENSIONS)
            require(row['outcome'] in ('SATISFIED','VIOLATED','ORACLE_MISSING','UNSCORABLE') and _valid_id(row['reason_code']))
            require(_valid_refs(row['source_fact_ids']))
            sequence(row['evidence_pointers'],4096)
            require(bool(row['evidence_pointers']) and all(isinstance(v,str) and 0<len(v)<=512 for v in row['evidence_pointers']))
        sequence(manifest['limitations'],64)
        require(all(_valid_id(value) for value in manifest['limitations']))
        for row in manifest['files']:
            require(isinstance(row,dict) and isinstance(row.get('role'),str) and row['role'] in set(_SQ_ROLES.values())|{'SOURCE_BYTES'})
        return True
    except (ValueError,TypeError,KeyError,RecursionError):
        return False


def inspect_result_state(result_root, derive_profile, normalize, implementation_bytes):
    root = _sq_check_path(result_root)
    if not root.exists() or not root.is_dir():
        return {"status": "MISSING"}
    # Walk explicitly without following links; links outrank every integrity status.
    actual = {}
    directories = set()
    pending = [root]
    retained_size = 0
    while pending:
        parent = pending.pop()
        try:
            children = list(parent.iterdir())
        except OSError:
            _fail("LOCAL_IO_FAILURE")
        for path in children:
            _sq_check_path(path)
            name = path.relative_to(root).as_posix()
            if len(actual) + len(directories) >= 1024:
                return {"status": "MISMATCH", "reason": "RESULT_SIZE_LIMIT"}
            if path.is_dir():
                directories.add(name)
                pending.append(path)
            elif path.is_file():
                actual[name] = _sq_read(path)
                retained_size += len(actual[name])
                if retained_size > _SQ_LIMIT:
                    return {"status": "MISMATCH", "reason": "RESULT_SIZE_LIMIT"}
            else:
                actual[name] = b""
    if "reservation.json" in actual or "manifest.json" not in actual:
        return {"status": "INCOMPLETE"}
    try:
        manifest = _sq_json(actual["manifest.json"])
        required = {"schema_version", "result_id", "identity_sha256", "evaluation_id", "fixture_class",
                    "bundle_sha256", "canonical_bundle_sha256", "response_sha256", "normalized_response_sha256",
                    "profile_sha256", "contract", "asset_sha256", "implementation_sha256", "files",
                    "profile_row_count", "category_applicability", "shape_diagnostics", "item_diagnostics", "rows", "limitations"}
        if not isinstance(manifest, dict) or set(manifest) != required or type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
            raise ValueError()
        if not isinstance(manifest["result_id"], str) or not re.fullmatch(r"SQ-[0-9a-f]{32}", manifest["result_id"]):
            raise ValueError()
        if not isinstance(manifest["files"], list) or len(manifest["files"]) > 1024:
            raise ValueError()
        if not _sq_manifest_structure(manifest):
            raise ValueError()
        declared = {}
        for row in manifest["files"]:
            if not isinstance(row, dict) or set(row) != {"path", "sha256", "byte_count", "role"}:
                raise ValueError()
            name = row["path"]
            if not isinstance(name, str) or name in declared:
                raise ValueError()
            if ".." in name.split("/") or name.startswith(("/", "\\")) or "\\" in name or ":" in name:
                _fail("PATH_ESCAPE")
            if _sq_role(name) is None or not isinstance(row["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) or type(row["byte_count"]) is not int or row["byte_count"] < 0:
                raise ValueError()
            declared[name] = row
        mandatory = {"bundle.source.json", "bundle.canonical.json", "profile.json", "contracts/evaluator.py"} | {"contracts/" + name for name in _SQ_ASSETS.values()}
        if not mandatory <= declared.keys():
            raise ValueError()
    except SemanticQualityError:
        raise
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError):
        return {"status": "INCOMPLETE"}
    if set(declared) - set(actual):
        return {"status": "MISSING"}
    def mismatch(reason):
        return {"status": "MISMATCH", "reason": reason}
    for name, row in declared.items():
        if len(actual[name]) != row["byte_count"] or _sha(actual[name]) != row["sha256"] or row["role"] != _sq_role(name):
            return mismatch("FILE_INTEGRITY_MISMATCH")
    if sum(len(data) for data in actual.values()) > _SQ_LIMIT:
        return mismatch("RESULT_SIZE_LIMIT")
    try:
        bundle = _sq_json(actual["bundle.source.json"])
        canonical = _sq_json(actual["bundle.canonical.json"])
        profile = _sq_json(actual["profile.json"])
        if canonical != bundle or actual["bundle.canonical.json"] != _canon(bundle):
            return mismatch("CANONICAL_BUNDLE_MISMATCH")
        try:
            installed = fixed_assets()
        except SemanticQualityError as error:
            if error.code not in {'LINK_FORBIDDEN','PATH_ESCAPE','LOCAL_IO_FAILURE'}:
                return mismatch("INSTALLED_DERIVER_MISMATCH")
            raise
        selected = _sq_selected_assets(installed, bundle)
        if actual["contracts/evaluator.py"] != implementation_bytes or any(actual[name] != data for name, data in selected.items()):
            return mismatch("INSTALLED_DERIVER_MISMATCH")
        assets = dict(installed)
        source_raw = {row["id"]: actual["sources/" + row["sha256"] + ".source"]
                      for row in bundle["sources"] if row["state"] == "AVAILABLE"}
        replay = validate_state(actual["bundle.source.json"], bundle, actual.get("response.source.json"), source_raw, assets)
        replay["implementation_raw"] = actual["contracts/evaluator.py"]
        identity = _identity(replay)
        if manifest["identity_sha256"] != identity or root.name != manifest["result_id"] or manifest["result_id"] != "SQ-" + identity[:32]:
            return mismatch("IDENTITY_MISMATCH")
        expected_profile = derive_profile(replay)
        if actual["profile.json"] != _canon(expected_profile):
            return mismatch("PROFILE_DERIVATION_MISMATCH")
        normal = normalize(replay)
        normalized = _canon(normal["value"]) if normal is not None and normal.get("value") is not None else None
        if actual.get("response.normalized.json") != normalized:
            return mismatch("PROFILE_DERIVATION_MISMATCH")
        expected_files = {name: actual[name] for name in mandatory}
        expected_files.update({"sources/" + _sha(data) + ".source": data for data in source_raw.values()})
        if replay["response_raw"] is not None:
            expected_files["response.source.json"] = replay["response_raw"]
        if normalized is not None:
            expected_files["response.normalized.json"] = normalized
        if manifest != _sq_manifest(replay, expected_profile, expected_files):
            return mismatch("PROFILE_DERIVATION_MISMATCH")
    except SemanticQualityError as error:
        if error.code in {'LINK_FORBIDDEN','PATH_ESCAPE','LOCAL_IO_FAILURE'}:
            raise
        return mismatch("PROFILE_DERIVATION_MISMATCH")
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError):
        return mismatch("PROFILE_DERIVATION_MISMATCH")
    expected_directories = {str(Path(name).parent).replace("\\", "/") for name in declared if "/" in name}
    if set(actual) - set(declared) - {"manifest.json"} or directories - expected_directories:
        return {"status": "UNDECLARED"}
    return {"status": "INTACT", "result_id": manifest["result_id"], "profile_row_count": len(profile["rows"])}

def validate_bundle(bundle_path):
    state=_validate_bundle(bundle_path)
    return {'status':'VALIDATED_NOT_EVALUATED','evaluation_id':state['bundle']['evaluation_id'],'bundle_sha256':_sha(state['raw']),'obligation_count':len(state['obligations']),'fixture_class':state['bundle']['fixture_class']}


def evaluate_bundle(bundle_path,output_root):
    try:
        return evaluate_state(_validate_bundle(bundle_path),output_root,derive_profile,_normalize,Path(__file__).read_bytes())
    except OSError: _fail('LOCAL_IO_FAILURE')


def inspect_result(result_root):
    try:
        return inspect_result_state(result_root,derive_profile,_normalize,Path(__file__).read_bytes())
    except OSError: _fail('LOCAL_IO_FAILURE')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    sub=parser.add_subparsers(dest='command',required=True)
    validate=sub.add_parser('validate',allow_abbrev=False);validate.add_argument('--bundle',required=True)
    evaluate=sub.add_parser('evaluate',allow_abbrev=False);evaluate.add_argument('--bundle',required=True);evaluate.add_argument('--output-root',required=True)
    inspect=sub.add_parser('inspect',allow_abbrev=False);inspect.add_argument('--result-root',required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='validate': result=validate_bundle(args.bundle)
        elif args.command=='evaluate': result=evaluate_bundle(args.bundle,args.output_root)
        else: result=inspect_result(args.result_root)
    except SemanticQualityError as error:
        print(json.dumps({'status':'REJECTED','error':error.code},ensure_ascii=True));return 2
    print(json.dumps(result,ensure_ascii=True,sort_keys=True));return 0


if __name__=='__main__': raise SystemExit(main())
