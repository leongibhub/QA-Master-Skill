"""Risk-aware test design from explicit reviewed requirement contracts."""
from __future__ import annotations
from .core import DIMENSIONS
from .quality import review_cases
NONFUNCTIONAL={'performance','load','stress','stability','security','compatibility','recovery'}
def design_matrix(requirements:list[dict],*,applicable:dict|None=None)->dict:
    applicable=applicable or {}
    cases=[];gaps=[];ids=set()
    for idx,req in enumerate(requirements):
        rid=str(req.get('id') or '').strip()
        if not rid or rid in ids:
            gaps.append({'requirement':rid or f'index:{idx}','code':'INVALID_OR_DUPLICATE_ID'});continue
        ids.add(rid)
        approved=req.get('approved') is True
        for dimension in req.get('dimensions',[req.get('dimension','functional')]):
            if dimension not in DIMENSIONS:
                gaps.append({'requirement':rid,'dimension':dimension,'code':'INVALID_DIMENSION'});continue
            oracle=req.get('oracles',{}).get(dimension) if isinstance(req.get('oracles'),dict) else None
            if not oracle and dimension==req.get('dimension','functional'):oracle=req.get('acceptance')
            if not approved:gaps.append({'requirement':rid,'dimension':dimension,'code':'REQUIREMENT_NOT_APPROVED'})
            if not isinstance(oracle,str) or not oracle.strip():
                gaps.append({'requirement':rid,'dimension':dimension,'code':'ORACLE_MISSING'});continue
            if dimension in NONFUNCTIONAL and not req.get('thresholds',{}).get(dimension):
                gaps.append({'requirement':rid,'dimension':dimension,'code':'THRESHOLD_UNCONFIRMED'});continue
            case={'id':f'TC-{rid}-{dimension.upper()}-001','title':f'{dimension}：{req.get("text") or rid}',
                'priority':req.get('priority') if req.get('priority') in {'P0','P1','P2','P3'} else 'P2',
                'trace':[rid],'dimension':dimension,
                'preconditions':req.get('preconditions') or '待确认：环境及初始状态',
                'data':req.get('test_data') or '待确认：测试数据',
                'steps':[f'按已确认需求 {rid} 准备场景',f'执行 {dimension} 场景并记录证据'],
                'expected':oracle.strip(),'approval':'DRAFT','source':req.get('source')}
            if dimension in NONFUNCTIONAL:case['threshold']=req['thresholds'][dimension]
            cases.append(case)
    coverage={}
    for dimension in DIMENSIONS:
        selected=[c['id'] for c in cases if c['dimension']==dimension]
        missing=[x for x in gaps if x.get('dimension')==dimension]
        if selected or missing:coverage[dimension]={'status':'BLOCKED' if missing else 'DRAFT','cases':selected,'gaps':missing}
        elif applicable.get(dimension,{}).get('status')=='N/A' and applicable[dimension].get('reason'):
            coverage[dimension]={'status':'N/A','reason':applicable[dimension]['reason'],'cases':[]}
        else:coverage[dimension]={'status':'UNASSESSED','cases':[]}
    return {'cases':cases,'gaps':gaps,'coverage':coverage,'review':review_cases(cases),'status':'DRAFT_UNAPPROVED','human_final_decision':'PENDING'}
