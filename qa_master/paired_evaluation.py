"""Explicit local exploratory paired evaluation (TASK-041, DES-040).

Only ``run_pair`` invokes a model. Validation, preview, inspection and grading
are process-free. Existing benchmark submissions remain a separate contract.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import re
from pathlib import Path

from ._paired_contract import (
    LIMIT, PROMPT_LIMIT, PROFILE, ISOLATION, DISABLED_FEATURES, VALUE_TYPES,
    PROMPT_TEMPLATE_V1, NEUTRAL_RESPONSE_SCHEMA_V1, PairedEvaluationError,
    array, canonical, check_keys, contained, digest, exact, fail, file_digest,
    hash_value, identifier, integer, no_links, parse_envelope, read_bytes,
    relative, strict_json, text, typed, unique,
)
from ._paired_process import native_capture, parse_trace, redact

MAX_SCENARIOS = 32
MAX_MATERIALIZED_BYTES = 64 * 1024 * 1024
STRICT_PROFILE = 'STRICT_COMPARISON_CANDIDATE'
ATTESTATION_SUBJECTS = ('provider_revision', 'system_baseline')


def _utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def _utf8(raw):
    try:
        return raw.decode('utf-8')
    except UnicodeError:
        fail('INVALID_UTF8')


def _source(descriptor, base, *, asset=False):
    exact(descriptor, 'path source_path media_type byte_count sha256' if asset else 'source_path byte_count sha256')
    integer(descriptor['byte_count'], 0, LIMIT)
    hash_value(descriptor['sha256'])
    raw = read_bytes(contained(base, descriptor['source_path']))
    if len(raw) != descriptor['byte_count'] or digest(raw) != descriptor['sha256']:
        fail('SOURCE_INTEGRITY_FAILURE')
    _utf8(raw)
    if asset:
        relative(descriptor['path'])
        if descriptor['media_type'] not in ('text/plain', 'text/markdown', 'application/json'):
            fail('UNSUPPORTED_MEDIA_TYPE')
        if descriptor['media_type'] == 'application/json':
            strict_json(raw)
    # Known secret patterns are rejected in inputs as well as withheld in output.
    if redact(raw)[1]['state'] != 'UNCHANGED':
        fail('PROHIBITED_INPUT_PATTERN')
    return raw


def _visible(raw, scenario):
    value = strict_json(raw)
    exact(value, 'schema_version scenario_id method title request known_facts scope checks')
    integer(value['schema_version'], 1, 1)
    check_keys(value, {'oracle', 'expected', 'answer', 'rating', 'score', 'winner'})
    if value['scenario_id'] != scenario['id'] or value['method'] != scenario['method']:
        fail('SCENARIO_MISMATCH')
    for key in ('title', 'request', 'scope'):
        text(value[key])
    for fact in array(value['known_facts'], 256, 1):
        exact(fact, 'id text'); identifier(fact['id']); text(fact['text'])
    unique([fact['id'] for fact in value['known_facts']])
    for check in array(value['checks'], 256):
        exact(check, 'id question value_type'); identifier(check['id']); text(check['question'])
        if check['value_type'] not in VALUE_TYPES:
            fail('UNKNOWN_VALUE_TYPE')
    unique([check['id'] for check in value['checks']])
    return value


def _runtime(value):
    exact(value, 'codex model policy host timeout_seconds retry_count')
    codex = exact(value['codex'], 'executable_path executable_sha256 version')
    name = text(codex['executable_path'], 4096)
    exe = Path(name)
    if not exe.is_absolute() or '..' in exe.parts or '\x00' in name:
        fail('INVALID_EXECUTABLE_PATH')
    exe = no_links(exe)
    try:
        with exe.open('rb') as stream:
            magic = stream.read(4)
    except OSError:
        fail('MISSING_EXECUTABLE')
    valid = exe.suffix.lower() == '.exe' and magic[:2] == b'MZ' if os.name == 'nt' else (
        os.access(exe, os.X_OK) and magic in (b'\x7fELF', b'\xfe\xed\xfa\xce', b'\xce\xfa\xed\xfe', b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe', b'\xca\xfe\xba\xbe'))
    if not valid:
        fail('NATIVE_EXECUTABLE_REQUIRED')
    if file_digest(exe) != hash_value(codex['executable_sha256']):
        fail('EXECUTABLE_DRIFT')
    text(codex['version'], 128)
    model = exact(value['model'], 'alias reasoning_effort provider_revision system_baseline temperature_state seed_state')
    identifier(model['alias'])
    if model['reasoning_effort'] not in ('none', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra'):
        fail('INVALID_REASONING_EFFORT')
    for name in ('provider_revision', 'system_baseline'):
        record = exact(model[name], 'state value evidence_sha256')
        if record['state'] == 'VERIFIED':
            # Only the verifier port may produce VERIFIED; a manifest that
            # merely claims it never passes (DES-061 §6 keeps this code).
            fail('ATTESTATION_NOT_SUPPORTED')
        if record['state'] not in ('NOT_AVAILABLE', 'UNVERIFIED'):
            fail('INVALID_ATTESTATION_STATE')
        if record['state'] == 'NOT_AVAILABLE' and (record['value'] is not None or record['evidence_sha256'] is not None):
            fail('INVALID_ATTESTATION_STATE')
        if record['value'] is not None:
            text(record['value'])
        if record['evidence_sha256'] is not None:
            hash_value(record['evidence_sha256'])
    if model['temperature_state'] != 'NOT_AVAILABLE' or model['seed_state'] != 'NOT_AVAILABLE':
        fail('UNSUPPORTED_MODEL_SETTING')
    expected_policy = {'sandbox': 'read-only', 'add_dirs': [], 'ignore_user_config': True,
                       'ephemeral': True, 'skip_host_skill_discovery': True, 'requested_tool_policy': 'NO_TOOL_USE',
                       'disabled_features': DISABLED_FEATURES, 'isolation_level': ISOLATION}
    if canonical(value['policy']) != canonical(expected_policy):
        fail('POLICY_MISMATCH')
    if value['host'] != {'os': platform.system(), 'architecture': platform.machine()}:
        fail('HOST_MISMATCH')
    integer(value['timeout_seconds'], 1, 1800)
    integer(value['retry_count'], 0, 0)


ATTESTATION_SUBJECTS = ('provider_revision', 'system_baseline')
VERIFIER_ID = 'ATTESTATION_VERIFIER_V1'


def _load_trust_registry(path):
    """Load and validate the administrator-controlled trust registry (DES-061 §2)."""
    path = no_links(Path(path))
    raw = read_bytes(path)
    if redact(raw)[1]['state'] != 'UNCHANGED':
        fail('TRUST_REGISTRY_INVALID')
    registry = strict_json(raw)
    try:
        exact(registry, 'schema_version registry_id created_at_utc issuers')
        integer(registry['schema_version'], 1, 1)
        identifier(registry['registry_id'])
        dt.datetime.strptime(registry['created_at_utc'], '%Y-%m-%dT%H:%M:%SZ')
        issuers_raw = array(registry['issuers'], 64, 1)
    except (PairedEvaluationError, TypeError, ValueError):
        # F-01 repair: registry grammar failures surface the DES-061 §6 code.
        fail('TRUST_REGISTRY_INVALID')
    issuers = {}
    for issuer in issuers_raw:
        try:
            exact(issuer, 'issuer_id subject algorithm public_key_multibase')
            identifier(issuer['issuer_id'])
            text(issuer['public_key_multibase'], 512)
        except PairedEvaluationError:
            fail('TRUST_REGISTRY_INVALID')
        if issuer['subject'] not in ATTESTATION_SUBJECTS:
            fail('TRUST_REGISTRY_INVALID')
        if issuer['algorithm'] != 'ED25519':
            fail('TRUST_REGISTRY_INVALID')
        if len(issuer['public_key_multibase']) < 8:
            fail('TRUST_REGISTRY_INVALID')
        key = (issuer['issuer_id'], issuer['subject'])
        if key in issuers:
            fail('TRUST_REGISTRY_INVALID')
        issuers[key] = issuer['public_key_multibase']
    return {'registry': registry, 'digest': digest(raw), 'keys': issuers}


def _registry_drift(path, expected_digest):
    path = no_links(Path(path))
    if file_digest(path) != expected_digest:
        fail('TRUST_REGISTRY_DRIFT')


def _verify_attestations(trust_registry_path, evidence_dir, manifest):
    """Verify provider-signed attestations for both arms and both subjects (DES-061 §3-4)."""
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        fail('ATTESTATION_VERIFIER_UNAVAILABLE')
    loaded = _load_trust_registry(trust_registry_path)
    evidence_dir = no_links(Path(evidence_dir))
    manifest_created = dt.datetime.strptime(manifest['created_at_utc'], '%Y-%m-%dT%H:%M:%SZ')
    verdicts = []
    for arm in ('A', 'B'):
        for subject in ATTESTATION_SUBJECTS:
            document_path = contained(evidence_dir, subject + '-' + arm + '.json')
            signature_path = contained(evidence_dir, subject + '-' + arm + '.sig')
            try:
                document_raw = read_bytes(document_path)
            except PairedEvaluationError as exc:
                if exc.code == 'MISSING_FILE':
                    fail('ATTESTATION_MISSING')
                raise
            try:
                signature_raw = read_bytes(signature_path, 1024)
            except PairedEvaluationError as exc:
                if exc.code == 'MISSING_FILE':
                    fail('ATTESTATION_MISSING')
                raise
            if redact(document_raw)[1]['state'] != 'UNCHANGED':
                fail('ATTESTATION_INVALID')
            document = strict_json(document_raw)
            # F-03 repair: the signature covers the canonical bytes, so the
            # on-disk bytes must be exactly canonical — no tolerated variants.
            if document_raw != canonical(document):
                fail('ATTESTATION_INVALID')
            try:
                exact(document, 'schema_version subject arm_id value observed_at_utc issuer_id statement')
                integer(document['schema_version'], 1, 1)
                if document['subject'] != subject or document['arm_id'] != arm:
                    fail('ATTESTATION_INVALID')
                text(document['value'], 20000)
                text(document['statement'], 20000)
                identifier(document['issuer_id'])
            except PairedEvaluationError:
                # F-02 repair: grammar failures inside the shared helpers
                # surface the DES-061 §6 code, not contract-layer codes.
                fail('ATTESTATION_INVALID')
            try:
                observed = dt.datetime.strptime(document['observed_at_utc'], '%Y-%m-%dT%H:%M:%SZ')
            except (TypeError, ValueError):
                fail('ATTESTATION_INVALID')
            if observed > manifest_created:
                fail('ATTESTATION_TIME_INVALID')
            key = (document['issuer_id'], subject)
            if key not in loaded['keys']:
                fail('ATTESTATION_ISSUER_UNKNOWN')
            try:
                public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(loaded['keys'][key]))
            except ValueError:
                fail('TRUST_REGISTRY_INVALID')
            try:
                public_key.verify(signature_raw, canonical(document))
            except Exception:
                fail('ATTESTATION_SIGNATURE_INVALID')
            verdicts.append({'subject': subject, 'arm_id': arm, 'state': 'VERIFIED',
                             'value': document['value'], 'issuer_id': document['issuer_id'],
                             'observed_at_utc': document['observed_at_utc'],
                             'evidence_sha256': digest(document_raw), 'verifier_id': VERIFIER_ID,
                             'verification': 'SIGNATURE_VALID'})
    if len(verdicts) != 4:
        fail('STRICT_ATTESTATION_INCOMPLETE')
    return {'registry_digest': loaded['digest'], 'verdicts': verdicts}


def _strict_preflight(manifest, trust_registry_path, evidence_dir):
    """Fail-closed strict-profile gate (DES-061 §5). Returns verdicts or None."""
    if manifest['profile'] == STRICT_PROFILE:
        if trust_registry_path is None or evidence_dir is None:
            fail('STRICT_PROFILE_NOT_SUPPORTED')
        result = _verify_attestations(trust_registry_path, evidence_dir, manifest)
        return result
    if trust_registry_path is not None:
        # An exploratory manifest never consumes a registry; it cannot silently upgrade.
        fail('STRICT_PROFILE_MISMATCH')
    return None


def _prepare_unchecked(payload, manifest_dir, trust_registry_path=None, evidence_dir=None):
    manifest = strict_json(payload)
    if redact(payload)[1]['state'] != 'UNCHANGED':
        fail('PROHIBITED_INPUT_PATTERN')
    exact(manifest, 'schema_version run_id profile created_at_utc participants scenarios prompt_template response_schema evaluator_commitment_sha256 runtime schedule')
    integer(manifest['schema_version'], 1, 1)
    identifier(manifest['run_id'])
    # Run/attempt IDs become path components and must also satisfy the path grammar.
    relative(manifest['run_id'])
    if manifest['profile'] not in (PROFILE, STRICT_PROFILE):
        fail('INVALID_PROFILE')
    try:
        dt.datetime.strptime(manifest['created_at_utc'], '%Y-%m-%dT%H:%M:%SZ')
    except (TypeError, ValueError):
        fail('INVALID_TIMESTAMP')
    attestation = _strict_preflight(manifest, trust_registry_path, evidence_dir)
    hash_value(manifest['evaluator_commitment_sha256'])
    _runtime(manifest['runtime'])
    participants = array(manifest['participants'], 2, 2)
    if [p.get('arm_id') if isinstance(p, dict) else None for p in participants] != ['A', 'B']:
        fail('INVALID_ARMS')
    assets = {}
    for participant in participants:
        exact(participant, 'arm_id participant_id source entry_asset assets')
        identifier(participant['participant_id'])
        source = exact(participant['source'], 'repository_id commit tree_oid')
        identifier(source['repository_id']); hash_value(source['commit'], git=True); hash_value(source['tree_oid'], git=True)
        rows = array(participant['assets'], 64, 1)
        copied = {}
        for row in rows:
            raw = _source(row, manifest_dir, asset=True)
            key = row['path']
            if key.casefold() in {p.casefold() for p in copied}:
                fail('DUPLICATE_ASSET')
            copied[key] = raw
        if list(copied) != sorted(copied) or participant['entry_asset'] not in copied:
            fail('INVALID_ASSET_INVENTORY')
        if sum(map(len, copied.values())) > LIMIT:
            fail('ASSET_TOTAL_LIMIT')
        assets[participant['arm_id']] = copied
    unique([p['participant_id'] for p in participants])
    scenarios = array(manifest['scenarios'], MAX_SCENARIOS, 3)
    visible = {}; input_bytes = {}
    for scenario in scenarios:
        exact(scenario, 'id method visible_input oracle_commitment_sha256')
        identifier(scenario['id']); hash_value(scenario['oracle_commitment_sha256'])
        if scenario['method'] not in ('boundary', 'decision_table', 'state_transition'):
            fail('INVALID_METHOD')
        raw = _source(scenario['visible_input'], manifest_dir)
        input_bytes[scenario['id']] = raw
        visible[scenario['id']] = _visible(raw, scenario)
    unique([row['id'] for row in scenarios])
    if {row['method'] for row in scenarios} != {'boundary', 'decision_table', 'state_transition'}:
        fail('PILOT_METHODS_INCOMPLETE')
    template = _source(manifest['prompt_template'], manifest_dir)
    schema = _source(manifest['response_schema'], manifest_dir)
    if template != PROMPT_TEMPLATE_V1 or schema != NEUTRAL_RESPONSE_SCHEMA_V1:
        fail('COMMON_CONTRACT_MISMATCH')
    schedule = array(manifest['schedule'], MAX_SCENARIOS, 3)
    for row in schedule:
        exact(row, 'attempt_id scenario_id order')
        identifier(row['attempt_id']); relative(row['attempt_id'])
        if row['scenario_id'] not in visible or row['order'] not in (['A', 'B'], ['B', 'A']):
            fail('INVALID_SCHEDULE')
    unique([row['attempt_id'].casefold() for row in schedule])
    if sorted(row['scenario_id'] for row in schedule) != sorted(visible):
        fail('INVALID_SCHEDULE')
    if manifest['profile'] == STRICT_PROFILE:
        # A strict candidate needs at least two completed schedule rows with both
        # orders represented (DES-040 §4.2); preflight derives it, never trusts it.
        orders = {tuple(row['order']) for row in schedule}
        if len(schedule) < 2 or orders != {('A', 'B'), ('B', 'A')}:
            fail('INVALID_SCHEDULE')
    return {'manifest': manifest, 'assets': assets, 'inputs': input_bytes, 'visible': visible,
            'attestation': attestation}


def _prepare(payload, manifest_dir, trust_registry_path=None, evidence_dir=None):
    try:
        return _prepare_unchecked(payload, manifest_dir, trust_registry_path, evidence_dir)
    except (TypeError, KeyError, AttributeError, RecursionError):
        fail('INVALID_SCHEMA')
    except OSError:
        fail('LOCAL_IO_FAILURE')


def load_run_manifest(payload, *, manifest_dir):
    return _prepare(payload, manifest_dir)['manifest']


def validate_run_manifest(payload, *, manifest_dir, trust_registry_path=None, evidence_dir=None):
    prepared = _prepare(payload, manifest_dir, trust_registry_path, evidence_dir)
    return {'status': 'VALIDATED_NOT_EXECUTED', 'run_manifest_sha256': digest(canonical(prepared['manifest'])),
            'claim_status': 'NOT_ASSERTED', 'human_rating_status': 'NOT_EXECUTED'}


def _projection(assets):
    chunks = [b'PARTICIPANT_CONTEXT_V1\n']
    for path, raw in assets.items():
        path_bytes = path.encode('utf-8')
        chunks.extend([f'ASSET {len(path_bytes)} {len(raw)} {digest(raw)}\n'.encode('ascii'),
                       path_bytes, b'\n', raw, b'\nEND_ASSET\n'])
    return b''.join(chunks) + b'END_PARTICIPANT_CONTEXT\n'


def _prompt(context, visible):
    blocks = {b'{{PARTICIPANT_CONTEXT}}': context, b'{{VISIBLE_INPUT}}': visible,
              b'{{RESPONSE_CONTRACT}}': NEUTRAL_RESPONSE_SCHEMA_V1}
    # Callback visits only tokens in the original template, never inserted data.
    result = re.sub(rb'\{\{[A-Z_]+\}\}', lambda match: blocks[match[0]], PROMPT_TEMPLATE_V1)
    if len(result) > PROMPT_LIMIT:
        fail('PROMPT_SIZE_LIMIT')
    return result


def _exclusions(path, prepared, manifest_dir, output_root):
    path = no_links(path)
    if path.is_relative_to(no_links(manifest_dir)) or path.is_relative_to(no_links(output_root)):
        fail('EVALUATOR_PATH_NOT_SEPARATE')
    value = strict_json(read_bytes(path))
    exact(value, 'schema_version forbidden_locators forbidden_sha256 fixture_markers')
    integer(value['schema_version'], 1, 1)
    for name in ('forbidden_locators', 'forbidden_sha256', 'fixture_markers'):
        array(value[name], 256); unique(value[name])
    for locator in value['forbidden_locators']:
        relative(locator)
    for hashed in value['forbidden_sha256']:
        hash_value(hashed)
    for marker in value['fixture_markers']:
        if not isinstance(marker, str) or not re.fullmatch(r'[\x20-\x7e]{16,128}', marker):
            fail('INVALID_FIXTURE_MARKER')
    if digest(canonical(value)) != prepared['manifest']['evaluator_commitment_sha256']:
        fail('EVALUATOR_COMMITMENT_MISMATCH')
    return value


def _leak(raw, locator, exclusions):
    needles = exclusions['forbidden_locators'] + exclusions['fixture_markers']
    if digest(raw) in exclusions['forbidden_sha256'] or any(n.encode('utf-8') in raw or n in locator for n in needles):
        fail('EVALUATOR_LEAKAGE')


def _write(root, locator, raw):
    path = contained(root, locator)
    path.parent.mkdir(parents=True, exist_ok=True)
    no_links(path.parent)
    try:
        with path.open('xb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        if read_bytes(path, max(LIMIT, PROMPT_LIMIT)) != raw:
            fail('ARTIFACT_WRITE_FAILURE')
    except FileExistsError:
        fail('ARTIFACT_EXISTS')
    except OSError:
        fail('ARTIFACT_WRITE_FAILURE')


def _ledger_write(root, locator, raw, role):
    if raw is None:
        return {'role': role, 'relative_path': locator, 'capture_state': 'ABSENT', 'byte_count': None, 'sha256': None,
                'redaction': {'state': 'UNCHANGED', 'transform_id': 'NONE', 'original_byte_count': None, 'original_sha256': None}}
    safe, transformation = redact(raw)
    _write(root, locator, safe)
    return {'role': role, 'relative_path': locator, 'capture_state': 'REDACTED' if transformation['state'] == 'REDACTED' else 'RETAINED',
            'byte_count': len(safe), 'sha256': digest(safe), 'redaction': transformation}


def _materialize(manifest_path, exclusions_path, output_root, preview=False,
                 trust_registry_path=None, evidence_dir=None):
    manifest_path = no_links(manifest_path)
    # Snapshot the registry digest before preparation; the verifier reloads it
    # during preparation and both digests must match, then every materialized
    # call rechecks the live file (DES-061 §2 drift boundary).
    registry_before = _load_trust_registry(trust_registry_path)['digest'] if trust_registry_path is not None else None
    prepared = _prepare(read_bytes(manifest_path), manifest_path.parent,
                        trust_registry_path, evidence_dir)
    manifest = prepared['manifest']
    if trust_registry_path is not None:
        if registry_before != prepared['attestation']['registry_digest']:
            fail('TRUST_REGISTRY_DRIFT')
        _registry_drift(trust_registry_path, prepared['attestation']['registry_digest'])
    outer = no_links(output_root)
    exclusions = _exclusions(exclusions_path, prepared, manifest_path.parent, outer)
    root = outer if preview else contained(outer, manifest['run_id'])
    if root.is_relative_to(manifest_path.parent):
        fail('OUTPUT_NOT_SEPARATE')
    plans = []
    materialized_bytes = len(canonical(manifest)) + 1
    for row in manifest['schedule']:
        for arm in row['order']:
            context = _projection(prepared['assets'][arm])
            visible = prepared['inputs'][row['scenario_id']]
            prompt = _prompt(context, visible)
            call_id = row['attempt_id'] + '-' + arm
            files = {'common/visible-input.json': visible, 'common/response.schema.json': NEUTRAL_RESPONSE_SCHEMA_V1}
            files.update({'assets/' + path: raw for path, raw in prepared['assets'][arm].items()})
            for locator, raw in files.items():
                _leak(raw, locator, exclusions)
            _leak(prompt, 'stdin.txt', exclusions)
            materialized_bytes += sum(map(len, files.values())) + len(prompt)
            if materialized_bytes > MAX_MATERIALIZED_BYTES:
                fail('MATERIALIZATION_CAPACITY_LIMIT')
            plans.append({'call_id': call_id, 'attempt_id': row['attempt_id'], 'scenario_id': row['scenario_id'],
                          'arm_id': arm, 'files': files, 'prompt': prompt, 'participant_context_sha256': digest(context),
                          'common_request_sha256': digest(canonical({'template_sha256': digest(PROMPT_TEMPLATE_V1),
                              'visible_input_sha256': digest(visible), 'response_schema_sha256': digest(NEUTRAL_RESPONSE_SCHEMA_V1)}))})
    writes = [('manifest.json', canonical(manifest)+b'\n', 'manifest')]
    for plan in plans:
        for locator, raw in plan['files'].items():
            writes.append(('calls/'+plan['call_id']+'/'+locator, raw, 'materialized_input'))
        writes.append(('calls/'+plan['call_id']+'/stdin.txt', plan['prompt'], 'stdin'))
    for locator, raw, role in writes:
        if redact(raw)[1]['state'] != 'UNCHANGED':
            fail('PROHIBITED_INPUT_PATTERN')
    ledger = [{'role': role, 'relative_path': locator, 'capture_state': 'RETAINED', 'byte_count': len(raw), 'sha256': digest(raw),
               'redaction': {'state': 'UNCHANGED', 'transform_id': 'NONE', 'original_byte_count': None, 'original_sha256': None}}
              for locator, raw, role in writes]
    preflight = {'schema_version': 1, 'status': 'PREVIEW_NOT_RUN' if preview else 'SEALED', 'created_at_utc': _utc(),
                 'run_manifest_sha256': digest(canonical(manifest)), 'runtime': manifest['runtime'],
                 'settings_canonical_sha256': digest(canonical(manifest['runtime'])),
                 'evaluator_commitment_sha256': manifest['evaluator_commitment_sha256'], 'leakage_matches': 0,
                 'trust_registry_sha256': prepared['attestation']['registry_digest'] if prepared['attestation'] else None,
                 'ledger': ledger, 'planned_calls': [{key: value for key, value in plan.items() if key not in ('files', 'prompt')} for plan in plans]}
    preflight_bytes = canonical(preflight)+b'\n'
    if len(preflight_bytes) > LIMIT//2 or len(preflight_bytes)+len(plans)*10240 > LIMIT:
        fail('CONTROL_RECORD_CAPACITY_LIMIT')
    if materialized_bytes+len(preflight_bytes) > MAX_MATERIALIZED_BYTES:
        fail('MATERIALIZATION_CAPACITY_LIMIT')
    try:
        root.parent.mkdir(parents=True, exist_ok=True)
        no_links(root.parent)
        root.mkdir(mode=0o700)
    except FileExistsError:
        fail('RUN_ID_EXISTS')
    except OSError:
        fail('RUN_RESERVATION_FAILED')
    for locator, raw, role in writes:
        _write(root, locator, raw)
    _write(root, 'preflight.json', preflight_bytes)
    return root, prepared, plans, preflight


def materialize_preview(manifest_path, evaluator_exclusions_path, preview_root,
                        trust_registry_path=None, evidence_dir=None):
    root, prepared, plans, preflight = _materialize(manifest_path, evaluator_exclusions_path, preview_root, True,
                                                    trust_registry_path, evidence_dir)
    return {'status': 'PREVIEW_NOT_RUN', 'run_manifest_sha256': preflight['run_manifest_sha256'], 'call_count': len(plans)}


def _terminal(record, participant_failure=False):
    if record['process_outcome'] == 'SPAWN_FAILED' or record['output_outcome'] == 'INTEGRITY_FAILURE':
        return 'INFRASTRUCTURE_FAILURE'
    if record['process_outcome'] == 'TIMED_OUT':
        return 'TIMED_OUT'
    if record['policy_outcome'] == 'POLICY_VIOLATION_OBSERVED':
        return 'POLICY_VIOLATION'
    if record['output_outcome'] in ('NOT_AVAILABLE', 'OUTPUT_INVALID'):
        return 'OUTPUT_INVALID'
    if participant_failure:
        return 'PARTICIPANT_FAILURE'
    if record['process_outcome'] != 'EXITED_ZERO':
        return 'RUN_FAILURE_UNATTRIBUTED'
    return 'COMPLETED_PROCESS'


def _run(manifest_path, exclusions_path, output_root, launcher, backend,
         trust_registry_path=None, evidence_dir=None):
    root, prepared, plans, preflight = _materialize(manifest_path, exclusions_path, output_root,
                                                    False, trust_registry_path, evidence_dir)
    manifest = prepared['manifest']; runtime = manifest['runtime']
    attempts = []; stop = None
    ledger = list(preflight['ledger'])
    ledger.append({'role': 'preflight', 'relative_path': 'preflight.json', 'capture_state': 'RETAINED',
                   'byte_count': len(read_bytes(root/'preflight.json')), 'sha256': file_digest(root/'preflight.json'),
                   'redaction': {'state': 'UNCHANGED', 'transform_id': 'NONE', 'original_byte_count': None, 'original_sha256': None}})
    for ordinal, plan in enumerate(plans):
        record = {key: plan[key] for key in ('call_id', 'attempt_id', 'scenario_id', 'arm_id', 'participant_context_sha256', 'common_request_sha256')}
        record.update({'ordinal': ordinal, 'stdin_sha256': digest(plan['prompt']), 'response_schema_sha256': digest(NEUTRAL_RESPONSE_SCHEMA_V1),
                       'started_at_utc': None, 'ended_at_utc': None, 'process_outcome': 'NOT_STARTED',
                       'termination_outcome': 'NOT_REQUESTED', 'output_outcome': 'NOT_AVAILABLE', 'policy_outcome': 'NOT_EVALUATED',
                       'terminal_status': 'NOT_EXECUTED', 'stop_reason': stop, 'ledger': []})
        prefix = 'attempts/' + plan['call_id'] + '/'
        if stop is None:
            record['started_at_utc'] = _utc()
            try:
                # Recheck executable, registry and every materialized byte immediately before launch.
                if file_digest(runtime['codex']['executable_path']) != runtime['codex']['executable_sha256']:
                    fail('EXECUTABLE_DRIFT')
                if trust_registry_path is not None:
                    _registry_drift(trust_registry_path, prepared['attestation']['registry_digest'])
                for entry in preflight['ledger']:
                    path = contained(root, entry['relative_path'])
                    if file_digest(path) != entry['sha256']:
                        fail('MATERIALIZED_DRIFT')
                capture = launcher(executable=runtime['codex']['executable_path'], model=runtime['model'],
                                   features=runtime['policy']['disabled_features'], prompt=plan['prompt'], timeout_seconds=runtime['timeout_seconds'])
                record.update({key: capture[key] for key in ('process_outcome', 'termination_outcome', 'termination',
                    'exit_code', 'pid', 'cleanup_outcome', 'environment', 'duration_ms', 'command')})
                record.update({key: capture[key] for key in ('stdin_outcome', 'stdin_bytes_sent', 'stream_observations')})
                for role in ('stdout', 'stderr', 'final'):
                    raw = capture[role]
                    if raw is not None and (not isinstance(raw, bytes) or len(raw) > LIMIT):
                        fail('CAPTURE_LIMIT')
                    record['ledger'].append(_ledger_write(root, prefix+role+('.jsonl' if role == 'stdout' else '.txt'), raw, role))
                trace = parse_trace(capture['stdout'] or b'')
                record.update({'policy_outcome': trace['policy_outcome'], 'trace_error': trace['error'], 'usage': trace['usage']})
                # Warning text is already in the redacted stream; never duplicate unfiltered text.
                record['trace_warning_count'] = len(trace['warnings'])
                envelope = None
                if (capture['integrity_failure'] or capture['stdin_outcome'] != 'SENT_COMPLETE'
                    or capture['stdin_bytes_sent'] != len(plan['prompt'])
                    or any(item['capture_state'] == 'REDACTED' for item in record['ledger'])):
                    record['output_outcome'] = 'INTEGRITY_FAILURE'
                elif not capture['final'] or not capture['stdout']:
                    record['output_outcome'] = 'NOT_AVAILABLE'
                else:
                    try:
                        envelope = parse_envelope(capture['final'], prepared['visible'][plan['scenario_id']], prepared['assets'][plan['arm_id']])
                        if not trace['valid'] or canonical(strict_json(trace['agent_text'].encode('utf-8'))) != canonical(envelope):
                            fail('TRACE_FINAL_MISMATCH')
                        record['output_outcome'] = 'COMPLETE'
                        record['ledger'].append(_ledger_write(root, prefix+'envelope.json', canonical(envelope)+b'\n', 'envelope'))
                    except PairedEvaluationError as exc:
                        envelope = None; record['output_outcome'] = 'OUTPUT_INVALID'; record['output_error'] = exc.code
                record['terminal_status'] = _terminal(record, bool(envelope and envelope['response_status'] == 'PARTICIPANT_FAILURE'))
            except (PairedEvaluationError, OSError) as exc:
                record['output_outcome'] = 'INTEGRITY_FAILURE'
                record['terminal_status'] = 'INFRASTRUCTURE_FAILURE'
                record['infrastructure_error'] = exc.code if isinstance(exc, PairedEvaluationError) else 'LOCAL_IO_FAILURE'
            record['ended_at_utc'] = _utc()
            if (record['process_outcome'] == 'SPAWN_FAILED' or record['output_outcome'] == 'INTEGRITY_FAILURE'
                or record['policy_outcome'] == 'POLICY_VIOLATION_OBSERVED' or record['termination_outcome'] == 'TERMINATION_UNCONFIRMED'):
                stop = 'RUN_STOP_' + record['terminal_status'] + '_' + plan['attempt_id']
        record_ledger = _ledger_write(root, prefix+'record.json', canonical(record)+b'\n', 'attempt_record')
        ledger.extend(record['ledger']); ledger.append(record_ledger)
        attempts.append(record)
    complete = all(row['terminal_status'] == 'COMPLETED_PROCESS' for row in attempts)
    started = any(row['process_outcome'] not in ('NOT_STARTED', 'SPAWN_FAILED') for row in attempts)
    attestation = prepared['attestation']
    strict_eligible = (attestation is not None and backend == 'NATIVE_CODEX'
                       and manifest['profile'] == STRICT_PROFILE)
    evidence_class = 'STRICT_COMPARABILITY_CANDIDATE' if strict_eligible else (PROFILE if backend == 'NATIVE_CODEX' else 'TEST_DOUBLE')
    result = {'schema_version': 1, 'run_id': manifest['run_id'], 'created_at_utc': _utc(),
              'run_manifest_sha256': preflight['run_manifest_sha256'], 'response_schema_sha256': digest(NEUTRAL_RESPONSE_SCHEMA_V1),
              'execution_backend': backend, 'evidence_class': evidence_class,
              'pilot_status': ('COMPLETE' if complete else 'PARTIAL' if started else 'FAILED') if backend == 'NATIVE_CODEX' else 'NOT_EXECUTED',
              'claim_status': 'NOT_ASSERTED', 'human_rating_status': 'NOT_EXECUTED', 'runtime': runtime,
              'attempts': attempts, 'ledger': ledger}
    if attestation is not None:
        # Preserve the manifest's declared records; verdicts are separate derived facts.
        result['attestation_verdicts'] = attestation['verdicts']
        result['strict_eligibility'] = 'HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY'
        if strict_eligible:
            # The promoted model record exists only on a native strict-eligible
            # run; a TEST_DOUBLE run records verdicts but presents no model.
            result['model'] = dict(runtime['model'])
            for verdict in attestation['verdicts']:
                record = result['model'].get(verdict['subject'])
                if isinstance(record, dict):
                    record = dict(record, state='VERIFIED', value=verdict['value'],
                                  evidence_sha256=verdict['evidence_sha256'])
                    result['model'][verdict['subject']] = record
    result_bytes = canonical(result)+b'\n'
    if len(result_bytes) > LIMIT:
        fail('CONTROL_RECORD_CAPACITY_LIMIT')
    _write(root, 'result.json', result_bytes)
    return result


def run_pair(manifest_path, evaluator_exclusions_path, output_root,
             trust_registry_path=None, evidence_dir=None):
    return _run(manifest_path, evaluator_exclusions_path, output_root, native_capture, 'NATIVE_CODEX',
                trust_registry_path, evidence_dir)


def _run_pair_with_ports(manifest_path, evaluator_exclusions_path, output_root, *, launcher,
                        trust_registry_path=None, evidence_dir=None):
    """Private deterministic test port. Never produces native pilot evidence."""
    return _run(manifest_path, evaluator_exclusions_path, output_root, launcher, 'TEST_DOUBLE',
                trust_registry_path, evidence_dir)


def _check_ledger(entries):
    locators = []
    for item in array(entries, 20000):
        exact(item, 'role relative_path capture_state byte_count sha256 redaction')
        text(item['role'], 64); relative(item['relative_path'])
        locators.append(item['relative_path'].casefold())
        if item['capture_state'] not in ('RETAINED', 'ABSENT', 'REDACTED'):
            fail('INVALID_LEDGER')
        if item['capture_state'] == 'ABSENT':
            if item['byte_count'] is not None or item['sha256'] is not None:
                fail('INVALID_LEDGER')
        else:
            integer(item['byte_count'], 0, PROMPT_LIMIT); hash_value(item['sha256'])
        transform = exact(item['redaction'], 'state transform_id original_byte_count original_sha256')
        if transform['state'] not in ('UNCHANGED', 'REDACTED'):
            fail('INVALID_LEDGER')
        if transform['state'] == 'UNCHANGED':
            if transform != {'state': 'UNCHANGED', 'transform_id': 'NONE', 'original_byte_count': None, 'original_sha256': None}:
                fail('INVALID_LEDGER')
        else:
            if item['capture_state'] != 'REDACTED' or transform['transform_id'] != 'WHOLE_ARTIFACT_V1':
                fail('INVALID_LEDGER')
            integer(transform['original_byte_count'], 0, LIMIT); hash_value(transform['original_sha256'])
    unique(locators)


def _inspect(run_root):
    root = no_links(run_root)
    result_file = root/'result.json'
    preflight = strict_json(read_bytes(root/'preflight.json'))
    # R-02 repair: pre-CR-015 run roots have no trust_registry_sha256 member;
    # retained evidence must stay inspectable, so the member is optional-absent
    # for those roots and required for strict-profile runs (which always have one).
    required_preflight = 'schema_version status created_at_utc run_manifest_sha256 runtime settings_canonical_sha256 evaluator_commitment_sha256 leakage_matches ledger planned_calls'
    optional_preflight = {'trust_registry_sha256'}
    if not isinstance(preflight, dict) or not set(required_preflight.split()).issubset(preflight):
        fail('INVALID_PREFLIGHT')
    if set(preflight) - set(required_preflight.split()) - optional_preflight:
        fail('INVALID_PREFLIGHT')
    if 'trust_registry_sha256' in preflight and preflight['trust_registry_sha256'] is not None:
        hash_value(preflight['trust_registry_sha256'])
    if preflight['status'] not in ('SEALED', 'PREVIEW_NOT_RUN'):
        fail('INVALID_PREFLIGHT')
    manifest = strict_json(read_bytes(root/'manifest.json'))
    if digest(canonical(manifest)) != preflight['run_manifest_sha256'] or canonical(manifest['runtime']) != canonical(preflight['runtime']):
        fail('INVALID_PREFLIGHT')
    if digest(canonical(preflight['runtime'])) != preflight['settings_canonical_sha256']:
        fail('INVALID_PREFLIGHT')
    if manifest.get('profile') == STRICT_PROFILE and preflight.get('trust_registry_sha256') is None:
        # A strict run always passed the verifier and must record the registry digest.
        fail('INVALID_PREFLIGHT')
    _check_ledger(preflight['ledger'])
    planned = preflight['planned_calls']
    for plan in array(planned, 512):
        exact(plan, 'call_id attempt_id scenario_id arm_id participant_context_sha256 common_request_sha256')
        relative(plan['call_id']); identifier(plan['attempt_id']); identifier(plan['scenario_id'])
        hash_value(plan['participant_context_sha256']); hash_value(plan['common_request_sha256'])
        if plan['arm_id'] not in ('A', 'B'):
            fail('INVALID_PLAN')
    unique([row['call_id'].casefold() for row in planned])
    document = strict_json(read_bytes(result_file)) if result_file.exists() else preflight
    _check_ledger(document['ledger'])
    if result_file.exists():
        required_result = 'schema_version run_id created_at_utc run_manifest_sha256 response_schema_sha256 execution_backend evidence_class pilot_status claim_status human_rating_status runtime attempts ledger'
        if not isinstance(document, dict) or not set(required_result.split()).issubset(document):
            fail('INVALID_RESULT')
        optional_result = set('attestation_verdicts strict_eligibility model'.split())
        if set(document) - set(required_result.split()) - optional_result:
            fail('INVALID_RESULT')
        integer(document['schema_version'], 1, 1)
        if (preflight['status'] != 'SEALED' or document['run_id'] != manifest['run_id']
            or document['run_manifest_sha256'] != preflight['run_manifest_sha256']
            or document['response_schema_sha256'] != digest(NEUTRAL_RESPONSE_SCHEMA_V1)
            or canonical(document['runtime']) != canonical(preflight['runtime'])
            or document['claim_status'] != 'NOT_ASSERTED' or document['human_rating_status'] != 'NOT_EXECUTED'):
            fail('INVALID_RESULT')
        if document['execution_backend'] not in ('NATIVE_CODEX', 'TEST_DOUBLE'):
            fail('INVALID_RESULT')
        strict_candidate = (document['evidence_class'] == 'STRICT_COMPARABILITY_CANDIDATE')
        expected_class = ('STRICT_COMPARABILITY_CANDIDATE' if strict_candidate else
                          (PROFILE if document['execution_backend'] == 'NATIVE_CODEX' else 'TEST_DOUBLE'))
        if document['evidence_class'] != expected_class:
            fail('INVALID_RESULT')
        has_strict_members = 'attestation_verdicts' in document or 'strict_eligibility' in document
        if strict_candidate:
            # Strict-eligible results must carry the verifier verdicts, the
            # holdout-protocol-only marker, and no claim/rating promotion.
            verdicts = document.get('attestation_verdicts')
            if (not isinstance(verdicts, list) or len(verdicts) != 4
                    or document.get('strict_eligibility') != 'HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY'
                    or document['claim_status'] != 'NOT_ASSERTED'
                    or document['human_rating_status'] != 'NOT_EXECUTED'):
                fail('INVALID_RESULT')
            if document['execution_backend'] != 'NATIVE_CODEX':
                # Only a native run may carry the strict evidence class.
                fail('INVALID_RESULT')
        elif has_strict_members and document['execution_backend'] != 'TEST_DOUBLE':
            # Strict members on a non-strict NATIVE result would be a silent upgrade.
            fail('INVALID_RESULT')
        if has_strict_members:
            # R-01 repair: strict TEST_DOUBLE runs record their verification facts,
            # but they are never strict candidates and claim nothing.
            if document.get('strict_eligibility') != 'HOLDS_FOR_HOLDOUT_PROTOCOL_ONLY':
                fail('INVALID_RESULT')
            if document['evidence_class'] != 'TEST_DOUBLE' and not strict_candidate:
                fail('INVALID_RESULT')
            if 'model' in document and document['execution_backend'] != 'NATIVE_CODEX':
                # A TEST_DOUBLE run must not present a promoted model record.
                fail('INVALID_RESULT')
            if 'model' in document:
                # R-03 repair: validate the promoted model record shape and
                # rebind every VERIFIED member to the verdict list.
                model = document['model']
                if not isinstance(model, dict) or not {'provider_revision', 'system_baseline'}.issubset(model):
                    fail('INVALID_RESULT')
                verdicts = document.get('attestation_verdicts') or []
                for name in ('provider_revision', 'system_baseline'):
                    record = model.get(name)
                    if not isinstance(record, dict):
                        fail('INVALID_RESULT')
                    exact(record, 'state value evidence_sha256')
                    if record['state'] != 'VERIFIED':
                        fail('INVALID_RESULT')
                    match = [v for v in verdicts if v.get('subject') == name and v.get('arm_id') == 'A']
                    if len(match) != 1 or match[0].get('value') != record['value'] or match[0].get('evidence_sha256') != record['evidence_sha256']:
                        fail('INVALID_RESULT')
            if 'attestation_verdicts' in document:
                verdicts = document['attestation_verdicts']
                if not isinstance(verdicts, list):
                    fail('INVALID_RESULT')
                for verdict in verdicts:
                    exact(verdict, 'subject arm_id state value issuer_id observed_at_utc evidence_sha256 verifier_id verification')
                    if (verdict['state'] != 'VERIFIED' or verdict['verification'] != 'SIGNATURE_VALID'
                            or verdict['verifier_id'] != VERIFIER_ID or verdict['arm_id'] not in ('A', 'B')
                            or verdict['subject'] not in ATTESTATION_SUBJECTS):
                        fail('INVALID_RESULT')
                if [(v['arm_id'], v['subject']) for v in verdicts] != [('A', 'provider_revision'), ('A', 'system_baseline'), ('B', 'provider_revision'), ('B', 'system_baseline')]:
                    fail('INVALID_RESULT')
        attempts = array(document['attempts'], 512)
        if len(attempts) != len(planned):
            fail('ATTEMPT_INVENTORY_MISMATCH')
        global_entries = {item['relative_path']: item for item in document['ledger']}
        for item in preflight['ledger']:
            if global_entries.get(item['relative_path']) != item:
                fail('LEDGER_MISMATCH')
        expected_stop = None
        for ordinal, (record, plan) in enumerate(zip(attempts, planned)):
            required = set('call_id attempt_id scenario_id arm_id participant_context_sha256 common_request_sha256 ordinal stdin_sha256 response_schema_sha256 started_at_utc ended_at_utc process_outcome termination_outcome output_outcome policy_outcome terminal_status stop_reason ledger'.split())
            optional = set('termination exit_code pid cleanup_outcome environment duration_ms command stdin_outcome stdin_bytes_sent stream_observations trace_error usage trace_warning_count output_error infrastructure_error'.split())
            if not isinstance(record, dict) or not required.issubset(record) or set(record)-required-optional:
                fail('INVALID_ATTEMPT')
            if record['ordinal'] != ordinal or any(record[key] != value for key, value in plan.items()):
                fail('ATTEMPT_INVENTORY_MISMATCH')
            if (record['process_outcome'] not in ('NOT_STARTED', 'SPAWN_FAILED', 'EXITED_ZERO', 'EXITED_NONZERO', 'TIMED_OUT')
                or record['termination_outcome'] not in ('NOT_REQUESTED', 'TERMINATION_OBSERVED', 'TERMINATION_UNCONFIRMED')
                or record['output_outcome'] not in ('NOT_AVAILABLE', 'COMPLETE', 'OUTPUT_INVALID', 'INTEGRITY_FAILURE')
                or record['policy_outcome'] not in ('NOT_EVALUATED', 'POLICY_VIOLATION_OBSERVED', 'NO_VIOLATION_OBSERVED')
                or record['terminal_status'] not in ('NOT_EXECUTED', 'PRECHECK_REJECTED', 'INFRASTRUCTURE_FAILURE', 'TIMED_OUT', 'POLICY_VIOLATION', 'OUTPUT_INVALID', 'PARTICIPANT_FAILURE', 'RUN_FAILURE_UNATTRIBUTED', 'COMPLETED_PROCESS')):
                fail('INVALID_ATTEMPT')
            _check_ledger(record['ledger'])
            unique([entry['role'] for entry in record['ledger']])
            roles = {entry['role']: entry for entry in record['ledger']}
            if set(roles)-{'stdout', 'stderr', 'final', 'envelope'}:
                fail('INVALID_ATTEMPT_ROLE')
            for item in record['ledger']:
                if global_entries.get(item['relative_path']) != item or not item['relative_path'].startswith('attempts/'+plan['call_id']+'/'):
                    fail('LEDGER_MISMATCH')
            record_path = 'attempts/'+plan['call_id']+'/record.json'
            if record_path not in global_entries or canonical(strict_json(read_bytes(contained(root, record_path)))) != canonical(record):
                fail('ATTEMPT_RECORD_MISMATCH')
            stdin_entry = global_entries.get('calls/'+plan['call_id']+'/stdin.txt')
            if (stdin_entry is None or record['stdin_sha256'] != stdin_entry['sha256']
                or record['response_schema_sha256'] != digest(NEUTRAL_RESPONSE_SCHEMA_V1)):
                fail('ATTEMPT_INPUT_MISMATCH')
            if any(item['capture_state'] == 'REDACTED' for item in roles.values()) and record['output_outcome'] != 'INTEGRITY_FAILURE':
                fail('REDACTION_OUTCOME_MISMATCH')
            if record.get('cleanup_outcome') == 'DELETE_FAILED' and record['output_outcome'] != 'INTEGRITY_FAILURE':
                fail('CLEANUP_OUTCOME_MISMATCH')
            if record['process_outcome'] in ('EXITED_ZERO', 'EXITED_NONZERO', 'TIMED_OUT'):
                if ((record.get('stdin_outcome') != 'SENT_COMPLETE' or record.get('stdin_bytes_sent') != stdin_entry['byte_count'])
                    and record['output_outcome'] != 'INTEGRITY_FAILURE'):
                    fail('STDIN_OUTCOME_MISMATCH')
            envelope = None
            if record['output_outcome'] == 'COMPLETE':
                if set(roles) != {'stdout', 'stderr', 'final', 'envelope'} or any(item['capture_state'] != 'RETAINED' for item in roles.values()):
                    fail('ATTEMPT_OUTPUT_MISMATCH')
                visible = strict_json(read_bytes(contained(root, 'calls/'+plan['call_id']+'/common/visible-input.json')))
                participant = next(p for p in manifest['participants'] if p['arm_id'] == plan['arm_id'])
                envelope = parse_envelope(read_bytes(contained(root, roles['envelope']['relative_path'])), visible, [a['path'] for a in participant['assets']])
                final = strict_json(read_bytes(contained(root, roles['final']['relative_path'])))
                trace = parse_trace(read_bytes(contained(root, roles['stdout']['relative_path'])))
                if (canonical(final) != canonical(envelope) or not trace['valid']
                    or canonical(strict_json(trace['agent_text'].encode('utf-8'))) != canonical(envelope)
                    or record['policy_outcome'] != trace['policy_outcome']
                    or record.get('stdin_outcome') != 'SENT_COMPLETE'
                    or record.get('stdin_bytes_sent') != stdin_entry['byte_count']):
                    fail('ATTEMPT_OUTPUT_MISMATCH')
            elif 'envelope' in roles:
                fail('ATTEMPT_OUTPUT_MISMATCH')
            for role, observation in record.get('stream_observations', {}).items():
                if role not in ('stdout', 'stderr') or not isinstance(observation, dict):
                    fail('INVALID_STREAM_OBSERVATION')
                exact(observation, 'observed_byte_count observed_sha256 eof_observed overflow')
                integer(observation['observed_byte_count'], 0, 2**63-1)
                if observation['observed_sha256'] is not None:
                    hash_value(observation['observed_sha256'])
                if type(observation['eof_observed']) is not bool or type(observation['overflow']) is not bool:
                    fail('INVALID_STREAM_OBSERVATION')
                if observation['overflow'] and (roles.get(role, {}).get('capture_state') != 'ABSENT' or record['output_outcome'] != 'INTEGRITY_FAILURE'):
                    fail('INVALID_STREAM_OBSERVATION')
            if record['terminal_status'] == 'NOT_EXECUTED':
                if (record['process_outcome'] != 'NOT_STARTED' or record['output_outcome'] != 'NOT_AVAILABLE'
                    or record['ledger'] or record['started_at_utc'] is not None or record['ended_at_utc'] is not None
                    or expected_stop is None or record['stop_reason'] != expected_stop):
                    fail('INVALID_UNEXECUTED_ATTEMPT')
            else:
                if expected_stop is not None or record['stop_reason'] is not None:
                    fail('STOP_CHAIN_MISMATCH')
                if record['terminal_status'] != _terminal(record, bool(envelope and envelope['response_status'] == 'PARTICIPANT_FAILURE')):
                    fail('ATTEMPT_TERMINAL_MISMATCH')
                if (record['process_outcome'] == 'SPAWN_FAILED' or record['output_outcome'] == 'INTEGRITY_FAILURE'
                    or record['policy_outcome'] == 'POLICY_VIOLATION_OBSERVED' or record['termination_outcome'] == 'TERMINATION_UNCONFIRMED'):
                    expected_stop = 'RUN_STOP_'+record['terminal_status']+'_'+record['attempt_id']
        complete = all(row['terminal_status'] == 'COMPLETED_PROCESS' for row in attempts)
        started = any(row['process_outcome'] not in ('NOT_STARTED', 'SPAWN_FAILED') for row in attempts)
        expected_status = ('COMPLETE' if complete else 'PARTIAL' if started else 'FAILED') if document['execution_backend'] == 'NATIVE_CODEX' else 'NOT_EXECUTED'
        if document['pilot_status'] != expected_status:
            fail('INVALID_RESULT')
    rows = []; known = {'result.json', 'preflight.json'}
    for item in document['ledger']:
        locator = relative(item['relative_path']); known.add(locator)
        path = contained(root, locator)
        if item['capture_state'] == 'ABSENT':
            status = 'MISMATCH' if path.exists() else 'INTACT'
        elif not path.exists():
            status = 'MISSING'
        else:
            status = 'INTACT' if path.stat().st_size == item['byte_count'] and file_digest(path) == item['sha256'] else 'MISMATCH'
        rows.append({'relative_path': locator, 'status': status})
    for path in root.rglob('*'):
        no_links(path)
        if path.is_file() and path.relative_to(root).as_posix() not in known:
            rows.append({'relative_path': path.relative_to(root).as_posix(), 'status': 'UNDECLARED'})
    return {'status': 'INTACT' if all(row['status'] == 'INTACT' for row in rows) else 'INTEGRITY_FAILURE',
            'completion': 'RECORDED' if result_file.exists() else 'INCOMPLETE', 'artifacts': rows,
            'claim_status': 'NOT_ASSERTED', 'human_rating_status': 'NOT_EXECUTED'}


def inspect_run(run_root):
    try:
        return _inspect(run_root)
    except (PairedEvaluationError, OSError, KeyError, TypeError, AttributeError, RecursionError):
        raise PairedEvaluationError('RUN_INTEGRITY_FAILURE') from None


def _grade_run(run_root, assertions_path, output_path):
    root = no_links(run_root); output = no_links(output_path); source = no_links(assertions_path)
    if output.is_relative_to(root) or source.is_relative_to(root):
        fail('GRADING_PATH_NOT_SEPARATE')
    if output.exists():
        fail('ARTIFACT_EXISTS')
    inspection = inspect_run(root)
    if inspection['status'] != 'INTACT' or inspection['completion'] != 'RECORDED':
        fail('RUN_INTEGRITY_FAILURE')
    result = strict_json(read_bytes(root/'result.json'))
    manifest = strict_json(read_bytes(root/'manifest.json'))
    scenario_ids = {row['id'] for row in manifest['scenarios']}
    check_ids = {}
    for attempt in result['attempts']:
        visible = strict_json(read_bytes(contained(root, 'calls/'+attempt['call_id']+'/common/visible-input.json')))
        check_ids[attempt['scenario_id']] = {row['id'] for row in visible['checks']}
    bundle = strict_json(read_bytes(source))
    exact(bundle, 'schema_version run_manifest_sha256 response_schema_sha256 assertions')
    integer(bundle['schema_version'], 1, 1)
    for key in ('run_manifest_sha256', 'response_schema_sha256'):
        if bundle[key] != result[key]:
            fail('GRADER_BINDING_MISMATCH')
    assertions = array(bundle['assertions'], 1024)
    for assertion in assertions:
        exact(assertion, 'id scenario_id check_id expected required_evidence_refs oracle_ref')
        identifier(assertion['id']); identifier(assertion['scenario_id']); identifier(assertion['check_id'])
        if assertion['scenario_id'] not in scenario_ids or assertion['check_id'] not in check_ids[assertion['scenario_id']]:
            fail('UNKNOWN_ASSERTION_BINDING')
        expected = exact(assertion['expected'], 'value_type value'); typed(expected['value_type'], expected['value'])
        for ref in array(assertion['required_evidence_refs'], 64):
            text(ref)
        unique(assertion['required_evidence_refs']); relative(assertion['oracle_ref'])
    unique([row['id'] for row in assertions])
    rows = []
    for attempt in result['attempts']:
        envelope_rows = [entry for entry in attempt['ledger'] if entry['role'] == 'envelope' and entry['capture_state'] == 'RETAINED']
        envelope = strict_json(read_bytes(contained(root, envelope_rows[0]['relative_path']))) if len(envelope_rows) == 1 else None
        for assertion in assertions:
            if assertion['scenario_id'] != attempt['scenario_id']:
                continue
            observations = [item for item in envelope['observations'] if item['check_id'] == assertion['check_id']] if envelope else []
            status = 'UNSCORABLE'
            if len(observations) == 1:
                observed = observations[0]
                equivalent = canonical({'value_type': observed['value_type'], 'value': observed['value']}) == canonical(assertion['expected'])
                equivalent &= set(assertion['required_evidence_refs']).issubset(observed['evidence_refs'])
                status = 'SATISFIED' if equivalent else 'VIOLATED'
            rows.append({'assertion_id': assertion['id'], 'call_id': attempt['call_id'], 'arm_id': attempt['arm_id'],
                         'status': status, 'evidence_pointer': envelope_rows[0]['relative_path']+'#/observations' if envelope_rows else None,
                         'oracle_ref': assertion['oracle_ref']})
    report = {'schema_version': 1, 'run_manifest_sha256': result['run_manifest_sha256'], 'assertions_sha256': digest(canonical(bundle)),
              'execution_backend': result['execution_backend'], 'assertions': rows, 'claim_status': 'NOT_ASSERTED', 'human_rating_status': 'NOT_EXECUTED',
              'parser': {'version': 1, 'implementation_sha256': file_digest(__file__)}}
    _write(output.parent, output.name, canonical(report)+b'\n')
    return report


def grade_run(run_root, assertions_path, output_path):
    try:
        return _grade_run(run_root, assertions_path, output_path)
    except (KeyError, TypeError, AttributeError, RecursionError):
        raise PairedEvaluationError('INVALID_ASSERTION_SCHEMA') from None
    except OSError:
        raise PairedEvaluationError('LOCAL_IO_FAILURE') from None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    validate = subs.add_parser('validate'); validate.add_argument('manifest')
    validate.add_argument('--trust-registry'); validate.add_argument('--attestations')
    for name in ('materialize', 'run'):
        command = subs.add_parser(name); command.add_argument('manifest'); command.add_argument('--exclusions', required=True); command.add_argument('--output', required=True)
        command.add_argument('--trust-registry'); command.add_argument('--attestations')
    inspect = subs.add_parser('inspect'); inspect.add_argument('run_root')
    grade = subs.add_parser('grade'); grade.add_argument('run_root'); grade.add_argument('--assertions', required=True); grade.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate':
            result = validate_run_manifest(read_bytes(args.manifest), manifest_dir=Path(args.manifest).absolute().parent,
                                           trust_registry_path=args.trust_registry, evidence_dir=args.attestations)
        elif args.command == 'materialize':
            result = materialize_preview(args.manifest, args.exclusions, args.output,
                                         args.trust_registry, args.attestations)
        elif args.command == 'run':
            result = run_pair(args.manifest, args.exclusions, args.output,
                              args.trust_registry, args.attestations)
        elif args.command == 'inspect':
            result = inspect_run(args.run_root)
        else:
            result = grade_run(args.run_root, args.assertions, args.output)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 0
    except (PairedEvaluationError, OSError) as exc:
        print(json.dumps({'status': 'FAILED', 'code': exc.code if isinstance(exc, PairedEvaluationError) else 'LOCAL_IO_FAILURE', 'claim_status': 'NOT_ASSERTED'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
