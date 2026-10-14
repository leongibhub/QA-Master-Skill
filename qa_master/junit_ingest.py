"""Import bounded JUnit XML as unapproved, evidence-linked raw test outcomes."""
from __future__ import annotations
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET

class JUnitImportError(ValueError):
    pass

def ingest_junit(path, case_map, *, max_bytes=5_000_000):
    """case_map maps (classname,name) tuples to official IDs. Provenance remains unverified."""
    source=Path(path)
    if source.stat().st_size>max_bytes:raise JUnitImportError('JUnit file exceeds limit')
    payload=source.read_bytes()
    if b'<!DOCTYPE' in payload.upper() or b'<!ENTITY' in payload.upper():
        raise JUnitImportError('DTD/entity declarations forbidden')
    try:root=ET.fromstring(payload)
    except ET.ParseError as exc:raise JUnitImportError('Malformed JUnit XML') from exc
    if root.tag not in ('testsuite','testsuites'):raise JUnitImportError('Unexpected XML root')
    nodes=root.findall('.//testcase')
    if not nodes:raise JUnitImportError('No testcases')
    if len(nodes)>10000:raise JUnitImportError('Too many tests')
    if not isinstance(case_map,dict):raise JUnitImportError('Case map required')
    digest=hashlib.sha256(payload).hexdigest()
    seen=set();runs=[]
    for node in nodes:
        key=(node.get('classname') or '',node.get('name') or '')
        if not key[1] or key in seen:raise JUnitImportError('Missing or duplicate testcase identity')
        seen.add(key)
        case_id=case_map.get(key)
        if not isinstance(case_id,str) or not case_id.strip():raise JUnitImportError('Unmapped test '+repr(key))
        children=[x for x in node if x.tag in ('failure','error','skipped')]
        if len(children)>1:raise JUnitImportError('Conflicting outcomes')
        status=({'failure':'FAIL','error':'BLOCKED','skipped':'SKIPPED'}.get(children[0].tag) if children else 'PASS')
        runs.append({'case_id':case_id,'status':status,
                     'evidence':f'junit-sha256:{digest}#{len(runs)}',
                     'raw_outcome':children[0].tag if children else 'success',
                     'provenance':'UNVERIFIED_EXTERNAL_ARTIFACT'})
    if len({r['case_id'] for r in runs})!=len(runs):raise JUnitImportError('Multiple JUnit tests mapped to one case ID')
    return {'source_sha256':digest,'runs':runs,'source_verified':False,'execution_authorized':False}
