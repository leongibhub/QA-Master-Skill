import argparse, json
from .core import Campaign,save,load
from .intent import plan_task

def main():
    p=argparse.ArgumentParser(description='QA Master workflow guardrail CLI (no actual remote execution)')
    p.add_argument('--state',default='.qa-master/campaign.json')
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('init').add_argument('name')
    sub.add_parser('status')
    sub.add_parser('plan').add_argument('prompt')
    a=sub.add_parser('answer');a.add_argument('key');a.add_argument('value')
    a=sub.add_parser('approve');a.add_argument('kind');a.add_argument('version')
    sub.add_parser('check').add_argument('intent',choices=('execution','regression','design','review','report'))
    sub.add_parser('invalidate').add_argument('source',choices=('requirements','code'))
    args=p.parse_args()
    if args.cmd=='init': obj=Campaign(args.name)
    else: obj=load(args.state)
    if args.cmd=='answer':obj.set_answer(args.key,args.value)
    if args.cmd=='approve':obj.approve(args.kind,args.version)
    if args.cmd=='invalidate':obj.invalidate(args.source)
    if args.cmd=='plan':
        known={k:(v.get('value') if isinstance(v,dict) else v) for k,v in obj.known.items()}
        if obj.status('requirements')=='CONFIRMED_NONE':known['requirements_status']='CONFIRMED_NONE'
        output=plan_task(args.prompt,known)
    elif args.cmd=='check':output=obj.next_action(args.intent)
    else:output={'project':obj.name,'known':obj.known,'approvals':obj.approvals}
    save(obj,args.state)
    print(json.dumps(output,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
