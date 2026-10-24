import argparse
import json
from .application import CampaignApplicationService
from .design_methods import DesignMethodError
from .skill_registry import discover_skills, discover_vendor_skills
from .state_store import StateConflictError


def main():
    p = argparse.ArgumentParser(description='QA Master local workflow CLI (planning only)', allow_abbrev=False)
    p.add_argument('--state', default='.qa-master/campaign.json')
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('init').add_argument('name')
    sub.add_parser('status')
    sub.add_parser('skills')
    install = sub.add_parser('install-codex', help='Install the self-contained Codex skill')
    destination = install.add_mutually_exclusive_group()
    destination.add_argument('--user', action='store_true', help='Install under ~/.agents/skills')
    destination.add_argument('--project', help='Install under PROJECT/.agents/skills')
    destination.add_argument('--target', help='Explicit skill directory')
    install.add_argument('--update', action='store_true', help='Update an unchanged managed install; keep backup')
    design = sub.add_parser('design', help='Generate an offline draft from a strict campaign bundle', allow_abbrev=False)
    # append lets us reject duplicate options instead of silently accepting the last one.
    design.add_argument('--input', action='append', required=True)
    design.add_argument('--output', action='append', required=True)
    audit = sub.add_parser('audit-method-cases', help='Audit explicit case rows against finite design candidates', allow_abbrev=False)
    audit.add_argument('--input', action='append', required=True)
    audit.add_argument('--cases', action='append', required=True)
    audit.add_argument('--output', action='append', required=True)
    audit.add_argument('--format', action='append', choices=('json', 'markdown'), default=[])
    impact = sub.add_parser('impact-method-cases', help='Propose case review after finite design changes', allow_abbrev=False)
    impact.add_argument('--before', action='append', required=True)
    impact.add_argument('--after', action='append', required=True)
    impact.add_argument('--cases', action='append', required=True)
    impact.add_argument('--output', action='append', required=True)
    impact.add_argument('--format', action='append', choices=('json', 'markdown'), default=[])
    proposal = sub.add_parser('propose-method-case-library', help='Draft a non-applied after-design case library', allow_abbrev=False)
    proposal.add_argument('--before', action='append', required=True)
    proposal.add_argument('--after', action='append', required=True)
    proposal.add_argument('--cases', action='append', required=True)
    proposal.add_argument('--output', action='append', required=True)
    sub.add_parser('plan').add_argument('prompt')
    a = sub.add_parser('answer'); a.add_argument('key'); a.add_argument('value')
    a = sub.add_parser('approve'); a.add_argument('kind'); a.add_argument('version')
    sub.add_parser('check').add_argument('intent', choices=('execution','regression','design','review','report'))
    sub.add_parser('invalidate').add_argument('source', choices=('requirements','code'))
    sub.add_parser('pause').add_argument('reason')
    sub.add_parser('resume')
    args = p.parse_args()
    if args.cmd == 'design' and (len(args.input) != 1 or len(args.output) != 1):
        p.error('design requires exactly one --input and one --output')
    if args.cmd == 'audit-method-cases' and (len(args.input) != 1 or len(args.cases) != 1 or len(args.output) != 1 or len(args.format) > 1):
        p.error('audit-method-cases requires exactly one --input, --cases, --output, and optional --format')
    if args.cmd == 'impact-method-cases' and (len(args.before) != 1 or len(args.after) != 1 or len(args.cases) != 1 or len(args.output) != 1 or len(args.format) > 1):
        p.error('impact-method-cases requires exactly one --before, --after, --cases, --output, and optional --format')
    if args.cmd == 'propose-method-case-library' and (len(args.before) != 1 or len(args.after) != 1 or len(args.cases) != 1 or len(args.output) != 1):
        p.error('propose-method-case-library requires exactly one --before, --after, --cases, and --output')
    try:
        if args.cmd == 'design':
            from .campaign_cli import write_campaign
            try:
                report = write_campaign(args.input[0], args.output[0], installed_projection=True)
            except DesignMethodError as error:
                print(json.dumps({'status': 'REJECTED', 'error': error.code}, ensure_ascii=True))
                return 2
            except (ValueError, TypeError, KeyError):
                print(json.dumps({'status': 'REJECTED', 'error': 'INVALID_CAMPAIGN_INPUT'}, ensure_ascii=True))
                return 2
            except OSError:
                print(json.dumps({'status': 'REJECTED', 'error': 'CAMPAIGN_IO_ERROR'}, ensure_ascii=True))
                return 2
            output = {
                'project': report['project'],
                'counts': {
                    'test_cases': len(report['test_cases']),
                    'requirement_findings': len(report['requirement_review']['findings']),
                    'unresolved_design': len(report['unresolved']['design_gaps']),
                    'method_candidates': len(report.get('method_design', {}).get('candidates', [])),
                    'method_obligations': len(report.get('method_design', {}).get('obligations', [])),
                },
                'status': 'DRAFT_UNAPPROVED', 'execution': 'NOT_EXECUTED', 'output': args.output[0],
            }
        elif args.cmd == 'audit-method-cases':
            from .case_conformance import write_case_audit, CaseConformanceError
            try:
                report = write_case_audit(args.input[0], args.cases[0], args.output[0],
                                          format=args.format[0] if args.format else 'json')
            except CaseConformanceError as error:
                print(json.dumps({'status': 'REJECTED', 'error': error.code}, ensure_ascii=True))
                return 2
            output = {'status': report['status'], 'execution': report['execution'],
                      'candidate_denominator': report['summary']['candidate_denominator'],
                      'output': args.output[0]}
        elif args.cmd == 'impact-method-cases':
            from .method_impact import write_method_impact, MethodImpactError
            try:
                report = write_method_impact(args.before[0], args.after[0], args.cases[0], args.output[0],
                                             format=args.format[0] if args.format else 'json')
            except MethodImpactError as error:
                print(json.dumps({'status': 'REJECTED', 'error': error.code}, ensure_ascii=True))
                return 2
            output = {'status': report['status'], 'execution': report['execution'],
                      'review_case_count': report['summary']['review_case_count'], 'output': args.output[0]}
        elif args.cmd == 'propose-method-case-library':
            from .case_library_proposal import write_method_case_library_proposal, CaseLibraryProposalError
            try:
                report = write_method_case_library_proposal(args.before[0], args.after[0], args.cases[0], args.output[0])
            except CaseLibraryProposalError as error:
                print(json.dumps({'status': 'REJECTED', 'error': error.code}, ensure_ascii=True))
                return 2
            output = {'status': report['status'], 'execution': report['execution'], 'application_state': report['application_state'],
                      'proposed_case_count': report['summary']['proposed_case_count'], 'held_case_count': report['summary']['held_case_count'],
                      'missing_vector_count': report['summary']['missing_after_candidate_count'], 'output': args.output[0]}
        elif args.cmd == 'install-codex':
            from .codex_skill import install_skill, SkillInstallError
            try:
                output = install_skill(args.target, user=args.user, project=args.project, update=args.update)
            except SkillInstallError as error:
                print(json.dumps({'error': str(error)}, ensure_ascii=True))
                return 2
            except OSError:
                print(json.dumps({'error': 'SKILL_INSTALL_IO_ERROR'}, ensure_ascii=True))
                return 2
        elif args.cmd == 'skills':
            output = discover_skills()
            vendor = discover_vendor_skills()
            output['vendor'] = {
                'count': vendor['count'],
                'status': vendor['status'],
                'languages': {lang: sum(1 for s in vendor['skills'] if s['language'] == lang) for lang in ('en', 'zh')},
                'categories': {cat: sum(1 for s in vendor['skills'] if s['category'] == cat)
                               for cat in ('testing-workflows', 'testing-types', 'skill-engineering')},
            }
        elif args.cmd == 'init':
            output = CampaignApplicationService.initialize(args.state, args.name).status()
        else:
            service = CampaignApplicationService.load(args.state)
            if args.cmd == 'status':
                output = service.status()
            elif args.cmd == 'check':
                output = service.check(args.intent)
            else:
                payload = {key: value for key, value in vars(args).items() if key not in ('state', 'cmd')}
                output = service.mutate(args.cmd, **payload)
    except (ValueError, TypeError, PermissionError, StateConflictError) as error:
        # Exception text is deliberately fixed by our domain, never raw payloads.
        code = 'STATE_CONFLICT' if isinstance(error, StateConflictError) else 'COMMAND_REJECTED'
        if str(error) in ('CAMPAIGN_PAUSED', 'UNSUPPORTED_SCHEMA', 'AMBIGUOUS_SCHEMA'):
            code = str(error)
        print(json.dumps({'error': code}, ensure_ascii=True))
        return 2
    print(json.dumps(output, ensure_ascii=True, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
