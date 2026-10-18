"""Deterministic evidence preparation, never semantic analysis or approval."""
import hashlib
import json
import re


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def prepare_documents(docs, prompt_text):
    if not docs:
        raise ValueError('Empty source list')
    sources=[]
    for label,text in docs:
        if not text.strip():
            raise ValueError(f'Empty required source: {label}')
        sources.append({'source':label,'source_hash':digest(text),'version':'UNKNOWN',
                        'lines':[{'line':i,'text':line} for i,line in enumerate(text.splitlines(),1)]})
    return {'artifact_mode':'evidence_preparation','analysis_status':'NOT_ASSESSED',
            'sources':sources,'prompt_hash':digest(prompt_text),
            'pending_human_decisions':['Confirm source versions, owners, and conflicts.',
                                       'Run the Skill prompt in an agent and review sourced conclusions.']}


def analysis_markdown(prompt_text, text, source_path, fmt):
    result=prepare_documents([(str(source_path),text)],prompt_text)
    fence='`' * max(3, max((len(m.group())+1 for m in re.finditer(r'`+',text)),default=3))
    return '\n'.join(['# Requirements input preparation','',
        'Analysis status: **NOT_ASSESSED**. This script preserves parsed evidence; an agent must execute the Skill prompt.',
        '',f'- Source: {source_path}',f'- Format: {fmt}',f'- Parsed text SHA-256: {result["sources"][0]["source_hash"]}',
        '- Source version: UNKNOWN (confirm with the document owner).',f'- Prompt SHA-256: {result["prompt_hash"]}',
        '', '## Complete parsed source',fence+'text',text,fence,'',
        '## Pending human decisions','- Confirm source versions and resolve conflicts.',
        '- Run the Skill prompt; provide sourced requirements, observable outcomes, risks, and open questions.',''])


def source_candidates(req_text, analysis_text):
    docs=prepare_documents([('requirement',req_text),('analysis',analysis_text)],'')
    cases=[]
    for source in docs['sources']:
        for item in source['lines']:
            if not item['text'].strip(): continue
            provenance=f"{source['source']}:{item['line']} SHA-256={source['source_hash']} version=UNKNOWN"
            cases.append({'title':f"Candidate {len(cases)+1}: {source['source']} line {item['line']}",
                'priority':'NOT_ASSESSED','type':'source candidate',
                'preconditions':'Pending agent analysis: identify the required state from the source.',
                'steps':'Pending agent analysis: derive executable actions from the source.',
                'data':'Pending agent analysis: derive input and boundary data from the source.',
                'expected':'Pending agent analysis: specify an observable business postcondition.',
                'actual':'NOT_RUN','status':'NOT_ASSESSED',
                'remark':'Evidence preparation only. '+provenance+'\n'+item['text'],
                'source_line':item['line'],'source_hash':source['source_hash'],'source_text':item['text']})
    return cases
