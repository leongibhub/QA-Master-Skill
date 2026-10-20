import json
from pathlib import Path
import subprocess

evidence = Path(__file__).resolve().parent
scratch = Path(json.loads((evidence / 'delivery-summary.json').read_text())['scratch'])
consumer = scratch / 'consumer project'
scripts = consumer / '.agents/skills/qa-master/scripts'
python = str(scratch / 'venv/Scripts/python.exe')
code = '''
import json
from qa_master.intent import plan_task
from qa_master.skill_registry import select_vendor_skills
prompts = ["不要 chaos-testing，只评审用例", "Do not use property-based-testing; only write test reports", "only unlisted-specialist-xyz"]
results = []
for prompt in prompts:
    route = select_vendor_skills(prompt=prompt)
    plan = plan_task(prompt)
    assert not route['selected'], (prompt, route)
    assert any(g['code'] == 'NO_MATCHING_VENDOR_SKILL' for g in route['gaps'])
    assert route['execution'] == 'NOT_EXECUTED'
    assert plan['no_execution']
    results.append({'prompt': prompt, 'route': route, 'plan': plan})
print(json.dumps(results))
'''
prefix = 'import sys; sys.path.insert(0,' + repr(str(scripts)) + ');\n'
result = subprocess.run([python, '-I', '-c', prefix + code], cwd=consumer, capture_output=True, text=True)
(evidence / 'route-edges.json').write_text(json.dumps({'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}, indent=2), encoding='utf-8')
assert result.returncode == 0, result.stderr
print('PASS: 2 negated canonical requests and 1 unknown request remain unresolved without execution')
