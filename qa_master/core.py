"""QA Master v0.1: deterministic guardrails for AI-assisted testing.
No external side effect is performed by this module.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

DIMENSIONS = ('functional','api','whitebox','integration','performance','load','stress','stability','compatibility','negative','security','recovery','regression')
STAGES = ('discovery','requirements','review','baseline','design','case_review','code_refinement','execution','regression','report')
SKILLS = {
 'requirements': ['requirements-analysis'], 'review':['requirements-analysis'],
 'design':['test-strategy','test-case-writing','test-case-reviewer'],
 'code_refinement':['code-review','api-testing','test-case-writing'],
 'execution':['automation-testing','functional-testing','api-testing'],
 'regression':['regression-testing'], 'report':['test-reporting'],
}
DIMENSION_SKILLS = {
 'functional':'functional-testing','api':'api-testing','whitebox':'code-review',
 'integration':'api-testing','performance':'performance-testing','load':'performance-testing',
 'stress':'performance-testing','stability':'reliability-testing',
 'compatibility':'compatibility-testing','negative':'test-case-writing',
 'security':'security-testing','recovery':'reliability-testing','regression':'regression-testing',
}

@dataclass
class Campaign:
    name: str
    known: dict = field(default_factory=dict)
    approvals: dict = field(default_factory=dict)
    artifacts: dict = field(default_factory=dict)
    questions: dict = field(default_factory=dict)
    history: list = field(default_factory=list)
    run_ids: list = field(default_factory=list)

    def set_answer(self, key, value):
        if value is None or (isinstance(value,str) and value.strip().lower() in ('没有','无','none','no')):
            self.known[key] = {'status':'CONFIRMED_NONE','value':None}
        else:
            self.known[key] = {'status':'PROVIDED','value':value}
        self.history.append({'event':'answer','field':key,'status':self.known[key]['status']})

    def has(self,key):
        return bool(self.known.get(key,{}).get('value'))

    def status(self,key):
        return self.known.get(key,{}).get('status','UNKNOWN')

    def approve(self, kind, artifact_version):
        if kind not in ('requirements','cases','execution','report','plan','cycle','bug'):
            raise ValueError('Unknown approval')
        if not artifact_version: raise ValueError('Approval requires version or scoped identifier')
        self.approvals[kind] = artifact_version
        self.history.append({'event':'approval','kind':kind,'version':artifact_version})

    def invalidate(self, changed):
        if changed == 'requirements':
            for k in ('requirements','cases','execution','report'):self.approvals.pop(k,None)
        elif changed == 'code':
            for k in ('cases','execution','report'):self.approvals.pop(k,None)
        self.history.append({'event':'invalidate','source':changed})

    def need_question(self,key):
        return self.status(key)=='UNKNOWN'

    def plan(self, prompt):
        """Conservative deterministic intent routing; an LLM can propose but never bypass gates."""
        p=prompt.lower()
        limited = any(x in p for x in ('只','仅','先','only','just'))
        intents=[]
        if any(x in p for x in ('评审需求','review requirements','需求评审')): intents.append('review')
        if any(x in p for x in ('用例','test case','测试设计')): intents.append('design')
        if any(x in p for x in ('回归','regression')): intents.append('regression')
        if any(x in p for x in ('报告','report')): intents.append('report')
        denied_execution = any(x in p for x in ('不执行测试','不要执行测试','无需执行','不开始测试','do not run','without executing'))
        if not denied_execution and any(x in p for x in ('执行测试','开始测试','run tests','完整测试','从头到尾','全流程')): intents.append('execution')
        if any(x in p for x in ('源码','代码','gitlab','github','仓库')): intents.append('code_refinement')
        if not intents: intents=['discovery']
        if 'execution' in intents and not limited:
            intents=['requirements','review','design','case_review','code_refinement','execution','regression','report']
        ordered=[s for s in STAGES if s in intents]
        return {'intent':ordered,'scope_limited':limited, 'skills':sorted({k for s in ordered for k in SKILLS.get(s,[])})}

    def next_action(self, intent):
        if not self.has('requirements') and not self.has('gitlab') and not self.has('web_url'):
            return {'state':'NEEDS_INPUT','question':'请提供需求文档/Wiki、GitLab 仓库或已部署系统地址（任选一种）。'}
        if self.has('gitlab') and not self.has('requirements') and self.need_question('requirements'):
            return {'state':'NEEDS_INPUT','question':'有正式需求文档或 Wiki 链接吗？没有请回答“没有”，我会从源码整理候选需求供评审。'}
        if intent in ('execution','regression'):
            for key,question in [('requirements','请先建立并确认需求基线。'),('cases','请先完成并确认测试用例。')]:
                if key not in self.approvals:return {'state':'WAITING_APPROVAL','question':question}
            if not self.has('build'):return {'state':'WAITING_FOR_BUILD','question':'请提供可测试版本及构建标识。'}
            if not self.has('environment'):return {'state':'WAITING_ENVIRONMENT','question':'请确认隔离测试环境和目标测试机。'}
            for key,question in [('jira_project','选择 Jira/SynapseRT 项目。'),('plan_name','填写/确认 Test Plan 名称。'),('cycle_name','填写/确认 Test Cycle 名称。'),('bug_assignee','确认 Bug 负责人或分配规则。')]:
                if not self.has(key):return {'state':'NEEDS_INPUT','question':question}
            if 'execution' not in self.approvals:return {'state':'WAITING_APPROVAL','question':'请批准本次测试范围、目标环境及测试执行。'}
        return {'state':'READY','question':None}

    def coverage(self, entries):
        """Explicit N/A accepted only with reason; uncovered dimensions surfaced."""
        issues=[]
        for dim in DIMENSIONS:
            row=entries.get(dim)
            if not row: issues.append(f'{dim}: missing coverage decision');continue
            if row.get('status')=='N/A' and not row.get('reason'):issues.append(f'{dim}: N/A missing reason')
            elif row.get('status')=='COVERED' and not row.get('cases'):issues.append(f'{dim}: no cases')
            elif row.get('status') not in ('COVERED','N/A','BLOCKED'):issues.append(f'{dim}: invalid status')
        return {'pass':not issues,'issues':issues}

def save(campaign,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(asdict(campaign),ensure_ascii=False,indent=2),encoding='utf8')
    tmp.replace(path)

def load(path):
    return Campaign(**json.loads(Path(path).read_text(encoding='utf8')))
