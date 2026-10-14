"""Dependency-aware persistent QA workflow planner. Planning has no side effects."""
from dataclasses import dataclass,field,asdict
from pathlib import Path
import json
@dataclass
class Step:
    id:str
    depends_on:list[str]=field(default_factory=list)
    required:list[str]=field(default_factory=list)
    approvals:list[str]=field(default_factory=list)
    side_effect:bool=False
    status:str='PENDING'
    result_ref:str|None=None
STEPS={
 'requirements':Step('requirements',required=['source']),
 'review':Step('review',['requirements']),
 'baseline':Step('baseline',['review'],approvals=['requirements']),
 'design':Step('design',['baseline']),
 'case_review':Step('case_review',['design'],approvals=['cases']),
 'code_refinement':Step('code_refinement',['case_review'],required=['git_ref']),
 'test_plan':Step('test_plan',['case_review'],required=['jira_project','plan_name','cycle_name'],approvals=['test_plan'],side_effect=True),
 'execution':Step('execution',['case_review','test_plan'],required=['build_ref','environment'],approvals=['execution'],side_effect=True),
 'regression':Step('regression',['execution'],required=['fix_ref'],approvals=['regression'],side_effect=True),
 'report':Step('report',['execution'])
}
@dataclass
class Workflow:
    project:str
    steps:dict[str,Step]=field(default_factory=dict)
    answers:dict=field(default_factory=dict)
    approvals:dict=field(default_factory=dict)
    events:list=field(default_factory=list)
    def request(self,targets):
        def include(s):
            if s not in STEPS:raise ValueError('Unknown step')
            if s in self.steps:return
            definition=STEPS[s]
            for dep in definition.depends_on:include(dep)
            self.steps[s]=Step(s,list(definition.depends_on),list(definition.required),list(definition.approvals),definition.side_effect)
        for s in targets:include(s)
        self.events.append({'action':'request','targets':targets})
    def answer(self,name,value):
        val=value.strip() if isinstance(value,str) else value
        state='CONFIRMED_NONE' if val is None or (isinstance(val,str) and val.lower() in ('没有','无','none','no')) else 'PROVIDED'
        self.answers[name]={'state':state,'value':None if state=='CONFIRMED_NONE' else val}
        self.events.append({'action':'answer','key':name,'state':state})
    def approve(self,kind,version,scope):
        if kind not in {a for s in STEPS.values() for a in s.approvals}:raise ValueError('Unknown approval')
        if not version or not scope:raise ValueError('Version and scope required')
        self.approvals[kind]={'version':version,'scope':scope}
        self.events.append({'action':'approve','kind':kind,'version':version,'scope':scope})
    def evaluate(self,step):
        x=self.steps[step]
        if x.status=='DONE':return 'DONE'
        if any(self.steps[d].status!='DONE' for d in x.depends_on):return 'PENDING'
        for req in x.required:
            if req not in self.answers:return 'WAITING_INPUT'
            if self.answers[req]['state']=='CONFIRMED_NONE':return 'BLOCKED'
        if any(a not in self.approvals for a in x.approvals):return 'WAITING_APPROVAL'
        return 'READY'
    def complete(self,step,result_ref):
        if step not in self.steps or self.evaluate(step)!='READY':raise ValueError('Step not ready')
        if not result_ref:raise ValueError('Result/evidence reference required')
        self.steps[step].status='DONE';self.steps[step].result_ref=result_ref
        self.events.append({'action':'complete','step':step,'result_ref':result_ref})
    def next_actions(self):
        return [{'step':k,'state':self.evaluate(k)} for k in self.steps if self.steps[k].status!='DONE']
    def invalidate(self,step):
        if step not in self.steps:raise ValueError('Unknown step')
        affected={step}
        while True:
            old=len(affected)
            affected.update(k for k,v in self.steps.items() if any(d in affected for d in v.depends_on))
            if len(affected)==old:break
        for name in affected:
            self.steps[name].status='PENDING';self.steps[name].result_ref=None
            for approval in self.steps[name].approvals:self.approvals.pop(approval,None)
        self.events.append({'action':'invalidate','affected':sorted(affected)})
        return sorted(affected)
    def save(self,path):
        p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
        tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(asdict(self),ensure_ascii=False,indent=2),encoding='utf8');tmp.replace(p)
    @classmethod
    def load(cls,path):
        raw=json.loads(Path(path).read_text(encoding='utf8'))
        raw['steps']={k:Step(**v) for k,v in raw['steps'].items()}
        return cls(**raw)
