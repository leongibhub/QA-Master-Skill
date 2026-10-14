"""Conservative test design from explicit requirements. DRAFT only."""
from __future__ import annotations
from .core import DIMENSIONS
from .quality import review_cases

def design(requirements:list[dict],include_negative=True):
    cases=[];gaps=[]
    for req in requirements:
        rid=str(req.get('id') or '').strip()
        if not rid or not req.get('text'):
            gaps.append({'requirement':rid or '?','reason':'missing identifier or description'});continue
        acceptance=req.get('acceptance')
        if not isinstance(acceptance,str) or not acceptance.strip():
            gaps.append({'requirement':rid,'reason':'missing explicit acceptance criteria'});continue
        base={'priority':req.get('priority') if req.get('priority') in ('P0','P1','P2','P3') else 'P2',
              'trace':[rid],'preconditions':req.get('preconditions') or '待确认：测试环境及初始状态',
              'data':req.get('test_data') or '待确认：测试数据','source':req.get('source'),'approval':'DRAFT'}
        dimension=req.get('dimension','functional')
        if dimension not in DIMENSIONS:
            gaps.append({'requirement':rid,'reason':'unknown test dimension'});continue
        cases.append(dict(base,id=f'TC-{rid}-01',title=f'验证：{req["text"]}',dimension=dimension,
                          steps=[f'准备需求 {rid} 所述的前置数据',f'执行：{req["text"]}'],expected=acceptance))
        if include_negative and req.get('invalid_input') and req.get('invalid_expected'):
            cases.append(dict(base,id=f'TC-{rid}-02',title=f'拒绝非法输入：{req["text"]}',
                              dimension='negative',data=req['invalid_input'],
                              steps=['准备合法的初始环境','提交明确指定的非法输入'],expected=req['invalid_expected']))
    return {'cases':cases,'gaps':gaps,'review':review_cases(cases),'status':'DRAFT_UNAPPROVED'}

def coverage_plan(requirements:list[dict]):
    mapped={d:[] for d in DIMENSIONS}
    for req in requirements:
        dim=req.get('dimension','functional')
        if dim in mapped:mapped[dim].append(req.get('id','UNKNOWN'))
    return {d:{'status':'PROPOSED' if mapped[d] else 'UNASSESSED','requirements':mapped[d],
               'reason':'Review applicability and confirm thresholds' if not mapped[d] else ''} for d in DIMENSIONS}
