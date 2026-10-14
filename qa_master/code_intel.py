"""Read-only Python AST inventory; observed code is NOT an approved requirement."""
from __future__ import annotations
import ast
from pathlib import Path

def inventory_python(root:str,max_files:int=1000):
    base=Path(root).resolve()
    if not base.is_dir():raise ValueError('Repository root must be a directory')
    results=[];problems=[]
    paths=sorted(p for p in base.rglob('*.py') if '.git' not in p.parts and '.venv' not in p.parts and 'venv' not in p.parts and '__pycache__' not in p.parts)
    if len(paths)>max_files:raise ValueError('Repository exceeds file inspection limit')
    for path in paths:
        try:tree=ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path))
        except (SyntaxError,UnicodeError) as exc:
            problems.append({'file':str(path.relative_to(base)),'error':type(exc).__name__});continue
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                branches=sum(isinstance(x,(ast.If,ast.IfExp,ast.For,ast.AsyncFor,ast.While,ast.Try,ast.Match)) for x in ast.walk(node))
                raises=sum(isinstance(x,ast.Raise) for x in ast.walk(node))
                results.append({'file':str(path.relative_to(base)),'function':node.name,'line':node.lineno,
                                'is_async':isinstance(node,ast.AsyncFunctionDef),'branch_points':branches,'raise_points':raises,
                                'kind':'CODE_OBSERVATION','requirement_approval':'NOT_APPROVED'})
    return {'functions':results,'parse_problems':problems,'files_scanned':len(paths),'scope':'python_ast_static_only'}
