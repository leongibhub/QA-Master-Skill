"""Bounded source inspection: code observations are not approved requirements."""
from __future__ import annotations
import ast,hashlib
from pathlib import PurePosixPath
SUFFIXES={'.py','.js','.jsx','.ts','.tsx','.java','.go','.rs','.cs','.vue'}
SKIP={'node_modules','.git','vendor','dist','build','target','.venv','venv','__pycache__','coverage'}
SENSITIVE=('secret','.env','credential','private','password','id_rsa','.pem','.key')
def eligible(path):
    if not isinstance(path,str) or not path or path.startswith('/') or '\\' in path:return False
    parts=PurePosixPath(path).parts
    if '..' in parts or any(x in SKIP for x in parts):return False
    if any(x in parts[-1].lower() for x in SENSITIVE):return False
    return PurePosixPath(path).suffix.lower() in SUFFIXES
def analyze_source(path,content,*,blob_id=None,ref='HEAD'):
    if not eligible(path) or not path.endswith('.py'):return []
    try:tree=ast.parse(content,filename=path)
    except SyntaxError:return []
    digest=hashlib.sha256(content.encode()).hexdigest();out=[]
    for node in ast.walk(tree):
        if not isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
        branches=sum(isinstance(x,(ast.If,ast.IfExp,ast.While,ast.For,ast.AsyncFor,ast.Try,ast.Match)) for x in ast.walk(node))
        raises=sum(isinstance(x,ast.Raise) for x in ast.walk(node))
        source_key=f'{path}:{node.lineno}:{node.name}'
        out.append({'id':'CAND-'+hashlib.sha256(source_key.encode()).hexdigest()[:12],
          'title':f'需要核实函数 {node.name} 的业务行为',
          'observed':f'发现函数 {node.name}，静态分支节点 {branches} 个，显式抛出异常节点 {raises} 个',
          'source':{'path':path,'line':node.lineno,'symbol':node.name,'blob_id':blob_id,'ref':ref,'sha256':digest},
          'status':'NEEDS_HUMAN_CONFIRMATION','confidence':'STATIC_OBSERVATION_ONLY','acceptance':None,
          'risk_hints':(['BRANCHES'] if branches else [])+(['EXCEPTIONS'] if raises else [])})
    return out
def inspect_repository(reader,project,ref='HEAD',max_files=80,max_total_chars=1_000_000):
    if not 1<=max_files<=1000 or not 1<=max_total_chars<=10_000_000:raise ValueError('Invalid crawl limits')
    metadata=reader.project(project);entries=reader.tree(project,ref)
    paths=sorted({e['path'] for e in entries if e.get('type')=='blob' and eligible(e.get('path'))})
    candidates=[];problems=[];scanned=[];total=0
    if len(paths)>max_files:problems.append({'kind':'FILE_LIMIT','skipped':len(paths)-max_files})
    for path in paths[:max_files]:
        try:
            obj=reader.file(project,path,ref);content=obj['content'];total+=len(content)
            if total>max_total_chars:
                problems.append({'kind':'CHAR_LIMIT','path':path});break
            scanned.append(path)
            if not path.endswith('.py'):problems.append({'kind':'LANGUAGE_ANALYSIS_UNSUPPORTED','path':path})
            candidates.extend(analyze_source(path,content,blob_id=obj.get('blob_id'),ref=ref))
        except Exception as exc:problems.append({'kind':'READ_FAILED','path':path,'error_type':type(exc).__name__})
    return {'project':metadata,'requested_ref':ref,'files_seen':len(entries),'scanned_files':scanned,
      'candidates':candidates,'gaps':problems,'approval':'PENDING_HUMAN',
      'completeness':'PARTIAL_STATIC_ANALYSIS',
      'next_action':'Review evidence and verify business intent before approving a requirement baseline'}
