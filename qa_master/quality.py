"""Original dependency-free QA artifact validation and traceability."""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
import re

CASE_FIELDS=('id','title','priority','trace','dimension','preconditions','data','steps','expected')
PRIORITIES={'P0','P1','P2','P3'}
VAGUE=('系统正常','符合预期','工作正常','正常即可','should work','works correctly')
@dataclass(frozen=True)
class Finding:
    severity:str
    code:str
    subject:str
    message:str

def analyze_requirements(requirements:list[dict])->dict:
    findings=[];ids=[]
    for index,requirement in enumerate(requirements):
        identifier=str(requirement.get('id') or f'item:{index+1}');ids.append(identifier)
        content=str(requirement.get('text') or '').strip()
        if not content:findings.append(Finding('BLOCKER','EMPTY_REQUIREMENT',identifier,'需求内容为空'))
        if not requirement.get('source'):findings.append(Finding('MAJOR','NO_PROVENANCE',identifier,'缺少来源和版本'))
        if any(x in content.lower() for x in ('尽快','适当','友好','快速','高性能','若干','as fast as possible','user friendly')):
            findings.append(Finding('MAJOR','AMBIGUOUS',identifier,'验收描述模糊'))
        if not requirement.get('acceptance'):findings.append(Finding('MAJOR','NO_ACCEPTANCE',identifier,'缺少验收标准'))
        if requirement.get('origin')=='code' and requirement.get('approved') is not True:
            findings.append(Finding('BLOCKER','CODE_UNCONFIRMED',identifier,'代码行为不是已批准需求'))
    for identifier,count in Counter(ids).items():
        if count>1:findings.append(Finding('BLOCKER','DUPLICATE_REQUIREMENT_ID',identifier,'需求 ID 重复'))
    return {'findings':[asdict(f) for f in findings],'approval':'PENDING_HUMAN','count':len(requirements)}

def review_cases(cases:list[dict],approved_requirement_ids:set[str]|None=None)->dict:
    issues=[];seen_ids=set();signatures=set();trace_map=defaultdict(list)
    for n,case in enumerate(cases):
        subject=str(case.get('id') or f'case:{n+1}')
        for field in CASE_FIELDS:
            value=case.get(field)
            if value is None or value=='' or value==[]:issues.append(Finding('BLOCKER','MISSING_FIELD',subject,f'缺少 {field}'))
        if subject in seen_ids:issues.append(Finding('BLOCKER','DUPLICATE_ID',subject,'用例 ID 重复'))
        seen_ids.add(subject)
        if case.get('priority') not in PRIORITIES:issues.append(Finding('MAJOR','BAD_PRIORITY',subject,'优先级应为 P0-P3'))
        if any(x in str(case.get('expected') or '').lower() for x in VAGUE):
            issues.append(Finding('BLOCKER','WEAK_ORACLE',subject,'预期结果不可判定'))
        if isinstance(case.get('steps'),list) and any(not str(x).strip() for x in case['steps']):
            issues.append(Finding('MAJOR','EMPTY_STEP',subject,'存在空步骤'))
        traces=case.get('trace') or []
        if isinstance(traces,str):traces=[x.strip() for x in re.split('[;,，；]',traces) if x.strip()]
        for req in traces:
            trace_map[req].append(subject)
            if approved_requirement_ids is not None and req not in approved_requirement_ids:
                issues.append(Finding('MAJOR','UNAPPROVED_TRACE',subject,f'未批准需求 {req}'))
        if not traces:issues.append(Finding('BLOCKER','NO_TRACE',subject,'没有需求或风险引用'))
        signature=(str(case.get('title','')).strip().lower(),tuple(map(str,traces)))
        if signature in signatures:issues.append(Finding('MAJOR','POSSIBLE_DUPLICATE',subject,'用例内容疑似重复'))
        signatures.add(signature)
    if approved_requirement_ids is not None:
        for req in sorted(approved_requirement_ids-set(trace_map)):
            issues.append(Finding('MAJOR','UNCOVERED_REQUIREMENT',req,'批准需求未关联用例'))
    return {'pass':not any(x.severity=='BLOCKER' for x in issues),'issues':[asdict(x) for x in issues],
            'trace_matrix':dict(sorted(trace_map.items())),'case_count':len(cases),'human_final_decision':'PENDING'}

def execution_report(runs:list[dict],defects:list[dict]|None=None)->dict:
    valid={'PASS','FAIL','BLOCKED','NOT_RUN','RUNNING'}
    findings=[];counts=Counter()
    for n,run in enumerate(runs):
        state=run.get('status','NOT_RUN')
        if state not in valid:findings.append({'code':'INVALID_STATUS','run':n});continue
        if state in ('PASS','FAIL') and not run.get('evidence'):
            findings.append({'code':'MISSING_EVIDENCE','run':n});state='BLOCKED'
        counts[state]+=1
    executed=counts['PASS']+counts['FAIL']
    return {'status':'EVIDENCE_REVIEW_REQUIRED' if findings else ('NOT_EXECUTED' if not executed else 'RESULTS_AVAILABLE'),
            'counts':{s:counts[s] for s in sorted(valid)},'defect_count':len(defects) if defects is not None else None,
            'findings':findings,'release_approved':False}
