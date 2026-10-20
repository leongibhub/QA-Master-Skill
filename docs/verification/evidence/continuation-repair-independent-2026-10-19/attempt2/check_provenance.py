import json
from pathlib import Path
import subprocess

evidence = Path(__file__).resolve().parent
summary = json.loads((evidence / 'delivery-summary.json').read_text())
scratch = Path(summary['scratch'])
python = str(scratch / 'venv/Scripts/python.exe')
consumer = scratch / 'consumer project'
scripts = consumer / '.agents/skills/qa-master/scripts'
code = "import qa_master,json; from qa_master.skill_registry import discover_vendor_skills; d=discover_vendor_skills(); print(json.dumps(dict(module=qa_master.__file__,count=d['count'],paths=[x['path'] for x in d['skills']])))"
results = {}
for label, prefix in [('wheel', ''), ('standalone', 'import sys; sys.path.insert(0,' + repr(str(scripts)) + '); ')]:
    results[label] = json.loads(subprocess.check_output([python, '-I', '-c', prefix + code], cwd=consumer, text=True))
assert all(Path(p).is_relative_to(scripts) for p in results['standalone']['paths'])
assert all(Path(p).is_relative_to(scratch / 'venv') for p in results['wheel']['paths'])
(evidence / 'import-and-route-provenance.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print({k: {'module': v['module'], 'count': v['count']} for k, v in results.items()})
