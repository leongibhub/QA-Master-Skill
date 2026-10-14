"""OpenAPI inventory and conservative draft; never claim execution."""
from __future__ import annotations

def draft_openapi(spec:dict):
    if not isinstance(spec,dict) or not isinstance(spec.get('paths'),dict):raise ValueError('OpenAPI paths map required')
    cases=[];gaps=[]
    for path,methods in sorted(spec['paths'].items()):
        if not isinstance(methods,dict):continue
        for method,operation in sorted(methods.items()):
            if method.lower() not in ('get','post','put','patch','delete','head','options','trace') or not isinstance(operation,dict):continue
            responses=operation.get('responses',{})
            expected=[str(s) for s in responses if str(s).isdigit() and 200<=int(s)<300]
            if not expected:
                gaps.append({'method':method.upper(),'path':path,'reason':'no documented 2xx response'});continue
            cases.append({'id':f'API-{len(cases)+1:04d}','title':f'{method.upper()} {path}',
                          'method':method.upper(),'path':path,'expected_statuses':expected,
                          'trace':[operation.get('operationId') or f'{method.upper()} {path}'],
                          'status':'DRAFT','execution':'NOT_RUN','test_data':'REQUIRES_CONFIRMATION'})
    return {'cases':cases,'gaps':gaps,'status':'DRAFT_UNAPPROVED'}
