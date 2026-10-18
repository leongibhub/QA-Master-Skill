#!/usr/bin/env python3
"""Check the appended fixture-decision table, not other scenario tables."""
import os,re,sys
EXPECTED = {'F1': 'FAIL', 'F2': 'PASS', 'F3': 'FAIL'}

def grade(text,exit_code):
    if str(exit_code) != '0': raise ValueError('engine did not exit successfully')
    lines=text.splitlines()
    headers=[]
    for index,line in enumerate(lines):
        if '|' not in line: continue
        cells=[cell.strip() for cell in line.strip().strip('|').split('|')]
        if [cell.upper() for cell in cells] == ['ID','DECISION','EVIDENCE']:
            headers.append(index)
    if len(headers)!=1:
        raise ValueError('exactly one appended ID/DECISION/Evidence table is required')
    rows=[]
    for line in lines[headers[0]+1:]:
        if not line.strip():
            if rows: break
            continue
        if '|' not in line: break
        cells=[cell.strip() for cell in line.strip().strip('|').split('|')]
        if cells and all(re.fullmatch(r':?-{3,}:?',cell.replace(' ','')) for cell in cells):
            continue
        if len(cells)!=3:
            raise ValueError('each appended decision row must contain exactly three cells')
        rows.append(cells)
    found={}
    for key,decision,evidence in rows:
        if key not in EXPECTED:
            raise ValueError('unknown decision ID: '+key)
        if key in found:
            raise ValueError('duplicate decision ID: '+key)
        if decision!=EXPECTED[key] or not evidence or evidence in ('-','--','TODO'):
            raise ValueError('incorrect or unsourced decision: '+key)
        found[key]=decision
    for key,expected in EXPECTED.items():
        if key not in found:
            raise ValueError('missing decision: '+key)

if __name__=='__main__':
    try:grade(os.environ.get('EVAL_FINAL_MESSAGE',''),os.environ.get('EVAL_EXIT_CODE',''))
    except ValueError as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
    print('Exact fixture decisions passed; semantic explanation remains separately reviewable')
