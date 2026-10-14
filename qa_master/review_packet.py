"""Create traceable review questions from source observations; no implicit approval."""
from __future__ import annotations
from hashlib import sha256
import json

def create_review_packet(inspection:dict)->dict:
    if not isinstance(inspection,dict) or not isinstance(inspection.get('candidates'),list):
        raise ValueError('Inspection candidates list required')
    observations=[];findings=[];seen=set()
    for index,c in enumerate(inspection['candidates']):
        if not isinstance(c,dict):
            findings.append({'severity':'BLOCKER','code':'INVALID_CANDIDATE','index':index});continue
        src=c.get('source')
        if not isinstance(src,dict) or not src.get('path') or type(src.get('line')) is not int or src['line']<1:
            findings.append({'severity':'BLOCKER','code':'MISSING_SOURCE','index':index});continue
        key=(src['path'],src['line'],src.get('symbol',''))
        if key in seen:
            findings.append({'severity':'MAJOR','code':'DUPLICATE_OBSERVATION','index':index});continue
        seen.add(key)
        oid='OBS-'+sha256(json.dumps(key,ensure_ascii=False).encode()).hexdigest()[:12]
        risks=sorted(set(c.get('risk_hints') or []))
        observations.append({'id':oid,'source':src,'observed':c.get('observed',''),'risks':risks,
                             'status':'UNCONFIRMED','testable_oracle':False})
        findings.append({'severity':'REVIEW','code':'BUSINESS_INTENT_UNKNOWN','observation_id':oid,
                         'question':'该代码行为是否符合预期业务需求？对应验收标准是什么？'})
        if 'BRANCHES' in risks:
            findings.append({'severity':'REVIEW','code':'BRANCH_BOUNDARIES','observation_id':oid,
                             'question':'各分支的触发条件、边界值和预期结果是什么？'})
        if 'EXCEPTIONS' in risks:
            findings.append({'severity':'REVIEW','code':'ERROR_CONTRACT','observation_id':oid,
                             'question':'错误返回、异常回滚和恢复要求是什么？'})
    for gap in inspection.get('gaps',[]):
        findings.append({'severity':'MAJOR','code':'INSPECTION_GAP','detail':gap})
    return {'kind':'CODE_DERIVED_REQUIREMENT_REVIEW','approval':'PENDING_HUMAN',
            'observations':observations,'findings':findings,
            'statistics':{'observations':len(observations),'review_items':len(findings)},
            'limitations':['Static code observations do not establish correct requirements',
                           'Acceptance criteria must be confirmed by a human']}

def build_requirement_drafts(packet:dict,decisions:dict)->dict:
    if packet.get('kind')!='CODE_DERIVED_REQUIREMENT_REVIEW':raise ValueError('Invalid packet')
    result=[];rejected=[];unresolved=[]
    for obs in packet['observations']:
        choice=decisions.get(obs['id'])
        if choice is None:unresolved.append(obs['id']);continue
        if choice.get('decision')=='reject':rejected.append(obs['id']);continue
        if (choice.get('decision')!='accept' or not str(choice.get('requirement','')).strip()
                or not str(choice.get('acceptance','')).strip()):
            unresolved.append(obs['id']);continue
        result.append({'id':'REQ-'+obs['id'][4:],'text':choice['requirement'].strip(),
                       'acceptance':choice['acceptance'].strip(),'source':obs['source'],
                       'origin':'code','approved':False,'approval':'DRAFT_PENDING_HUMAN_BASELINE'})
    return {'requirements':result,'rejected':rejected,'unresolved':unresolved,'baseline_approved':False}
