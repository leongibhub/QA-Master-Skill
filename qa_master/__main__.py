import argparse, json
from .core import Campaign,save,load
from .intent import plan_task
from .skill_registry import discover_skills,select_skills

def main():
    p=argparse.ArgumentParser(description='QA Master workflow guardrail CLI (no actual remote execution)')
    p.add_argument('--state',default='.qa-master/campaign.json')
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('init').add_argument('name')
    sub.add_parser('status')
    sub.add_parser('skills')
    sub.add_parser('plan').add_argument('prompt')
    a=sub.add_parser('answer');a.add_argument('key');a.add_argument('value')
    a=sub.add_parser('approve');a.add_argument('kind');a.add_argument('version')
    sub.add_parser('check').add_argument('intent',choices=('execution','regression','design','review','report'))
    sub.add_parser('invalidate').add_argument('source',choices=('requirements','code'))
    args=p.parse_args()
    if args.cmd=='skills':
        print(json.dumps(discover_skills(),ensure_ascii=False,indent=2));return
    if args.cmd=='init': obj=Campaign(args.name)
    else: obj=load(args.state)
    if args.cmd=='answer':obj.set_answer(args.key,args.value)
    if args.cmd=='approve':obj.approve(args.kind,args.version)
    if args.cmd=='invalidate':obj.invalidate(args.source)
    if args.cmd=='plan':
        known={k:(v.get('value') if isinstance(v,dict) else v) for k,v in obj.known.items()}
        if obj.status('requirements')=='CONFIRMED_NONE':known['requirements_status']='CONFIRMED_NONE'
        output=plan_task(args.prompt,known)
        output['professional_guidance']=select_skills(output['stages'])
        obj.task_contract={
            'schema_version':1,'stages':output['stages'],
            'no_execution':output['no_execution'],'no_external_writes':output['no_external_writes'],
            'capabilities':{'execute':False,'external_write':False},
            'authority':'PLANNING_ONLY'}
        output['task_contract']=obj.task_contract
    elif args.cmd=='check':
        output=obj.next_action(args.intent)
        output['mode']='PLANNING_ONLY'
        output['execution_authorized']=False
        if args.intent in ('execution','regression') and obj.task_contract.get('no_execution') is True:
            output['state']='DENIED_BY_TASK_SCOPE'
            output['question']='当前任务只允许分析或设计，不能进入测试执行。'
        if args.intent in ('execution','regression') and output['state']=='READY':
            output['state']='WAITING_TRUSTED_EXECUTOR'
            output['question']='本地规划记录不能授权执行；需要宿主核验精确审批和执行凭据。'
    else:output={'project':obj.name,'known':obj.known,'approvals':obj.approvals}
    if args.cmd not in ('status','check'):
        save(obj,args.state)
    print(json.dumps(output,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
