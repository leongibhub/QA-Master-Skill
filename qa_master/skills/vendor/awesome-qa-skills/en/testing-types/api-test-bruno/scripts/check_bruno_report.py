#!/usr/bin/env python3
"""Require executed requests and assertions in a Bruno 4.x JSON report."""
import argparse
import json
from pathlib import Path


def validate_report(report):
    if not isinstance(report,list) or not report:
        raise ValueError('Empty or unsupported Bruno report')
    for iteration in report:
        results=iteration.get('results')
        summary=iteration.get('summary',{})
        if not isinstance(results,list) or not results:
            raise ValueError('No executed requests')
        if summary.get('totalRequests')!=len(results) or summary.get('skippedRequests')!=0:
            raise ValueError('Skipped or missing requests cannot pass')
        if any(summary.get(key,0)!=0 for key in ('failedRequests','errorRequests','failedTests','failedAssertions','failedPreRequestTests','failedPostResponseTests')):
            raise ValueError('Bruno reported failures')
        checked=0
        for result in results:
            response = result.get('response', {})
            if result.get('skipped') or result.get('error') or type(response.get('status')) is not int or not 100 <= response['status'] <= 599:
                raise ValueError('Request was skipped or has no response')
            checks=[]
            for key in ('testResults','assertionResults','preRequestTestResults','postResponseTestResults'):
                values=result.get(key,[])
                if not isinstance(values,list):raise ValueError('Invalid assertion report')
                checks.extend(values)
            if not checks or any(check.get('status')!='pass' for check in checks):
                raise ValueError('Each request needs executed, passing assertions')
            checked+=len(checks)
        declared=sum(summary.get(k,0) for k in ('totalTests','totalAssertions','totalPreRequestTests','totalPostResponseTests'))
        if declared!=checked:
            raise ValueError('Assertion summary does not match executed checks')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report',type=Path)
    args=parser.parse_args()
    validate_report(json.loads(args.report.read_text(encoding='utf-8')))
    print('Bruno requests and assertions executed without skips or failures')


if __name__=='__main__':main()
