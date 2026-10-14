"""Conservative Python control-flow candidate analysis. No actual coverage execution."""
from __future__ import annotations
import ast, hashlib
from pathlib import PurePosixPath
BRANCH=(ast.If,ast.IfExp,ast.For,ast.AsyncFor,ast.While,ast.Try,ast.Match)
def inspect_python(source:str,path:str,*,commit_sha=None):
    p=PurePosixPath(path)
    if not isinstance(path,str) or not path or p.is_absolute() or '..' in p.parts or '\\' in path or p.suffix!='.py':
        raise ValueError('Safe relative Python path required')
    try: tree=ast.parse(source,filename=path)
    except SyntaxError as e:return {'status':'PARSE_ERROR','line':e.lineno,'candidates':[]}
    digest=hashlib.sha256(source.encode()).hexdigest()
    found=[]
    for func in ast.walk(tree):
        if not isinstance(func,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
        stack=list(reversed(func.body))
        while stack:
            node=stack.pop()
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef,ast.Lambda)):continue
            stack.extend(reversed(list(ast.iter_child_nodes(node))))
            if not isinstance(node,BRANCH+(ast.Raise,)):continue
            kind=type(node).__name__
            key=f'{path}:{func.name}:{node.lineno}:{kind}'
            cases=(['condition_true','condition_false'] if isinstance(node,(ast.If,ast.IfExp))
                   else ['zero_iterations','one_or_more_iterations'] if isinstance(node,(ast.For,ast.AsyncFor,ast.While))
                   else ['normal_path','handled_exception_path'] if isinstance(node,ast.Try)
                   else ['each_match_arm','unmatched_input'] if isinstance(node,ast.Match)
                   else ['exception_raised'])
            found.append({'id':'WB-'+hashlib.sha256(key.encode()).hexdigest()[:14],
                          'source':{'path':path,'line':node.lineno,'function':func.name,'commit':commit_sha,'sha256':digest},
                          'kind':kind,'scenarios':cases,'expected':None,'test_data':None,
                          'status':'NEEDS_SPECIFICATION','execution':'NOT_RUN','branch_coverage':'NOT_MEASURED'})
    return {'status':'REVIEW_REQUIRED','source':path,'sha256':digest,'approved':False,'candidates':found}
def review_readiness(result):
    gaps=[]
    for item in result.get('candidates',[]):
        for field in ('expected','test_data'):
            if not item.get(field):gaps.append({'id':item['id'],'code':field.upper()+'_UNCONFIRMED'})
    return {'ready':bool(result.get('approved')) and not gaps,'gaps':gaps}
