"""Independent CR028 delivery/README verification; run only after source freeze."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote
import zipfile

ROOT = Path(r'D:\QA-Master-PR2')
EVIDENCE = Path(__file__).resolve().parent
BUILD_PYTHON = r'C:\Program Files\Python\python.exe'
records = []

def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    records.append({'args': list(map(str, args)), 'cwd': str(cwd), 'returncode': result.returncode,
                    'stdout': result.stdout, 'stderr': result.stderr})
    (EVIDENCE / 'delivery-commands.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'command failed: {args}: {result.stderr}')
    return result.stdout

def digest(data):
    return hashlib.sha256(data).hexdigest()

scratch = Path(tempfile.mkdtemp(prefix='qa-cr028-independent-'))
source = scratch / 'source'
source.mkdir()
paths = run(['git', 'ls-files', '-z'], ROOT).split('\0')
for name in filter(None, paths):
    path = ROOT / name
    if path.is_file():
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
wheels = scratch / 'wheels'
wheels.mkdir()
run([BUILD_PYTHON, '-m', 'pip', 'wheel', '--no-deps', '--no-build-isolation', '--no-index', '--wheel-dir', str(wheels), '.'], source)
wheel = next(wheels.glob('*.whl'))
venv = scratch / 'venv'
run([BUILD_PYTHON, '-m', 'venv', str(venv)], scratch)
python = str(venv / 'Scripts/python.exe')
run([python, '-m', 'pip', 'install', '--no-index', '--no-deps', str(wheel)], scratch)
project = scratch / 'consumer project'
project.mkdir()
run([python, '-I', '-m', 'qa_master', 'install-codex', '--project', str(project)], project)
installed = project / '.agents/skills/qa-master'
vendor_prefix = 'qa_master/skills/vendor/'
expected = {name: (ROOT / name).read_bytes() for name in paths if name.startswith(vendor_prefix) and (ROOT / name).is_file()}
assert expected
with zipfile.ZipFile(wheel) as archive:
    wheel_vendor = {name: archive.read(name) for name in archive.namelist() if name.startswith(vendor_prefix) and not name.endswith('/')}
assert set(expected) == set(wheel_vendor), (set(expected) - set(wheel_vendor), set(wheel_vendor) - set(expected))
installed_vendor = {p.relative_to(installed / 'scripts').as_posix(): p.read_bytes()
                    for p in (installed / 'scripts/qa_master/skills/vendor').rglob('*') if p.is_file()}
assert set(expected) == set(installed_vendor)
manifest = []
for name, data in expected.items():
    assert data == wheel_vendor[name] == installed_vendor[name], name
    manifest.append({'path': name, 'bytes': len(data), 'sha256': digest(data)})
(EVIDENCE / 'vendor-equivalence.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
helper = str(installed / 'scripts/qa.py')
skills = json.loads(run([python, '-I', helper, 'skills'], project))
assert skills['vendor']['count'] == 330
assert skills['vendor']['languages'] == {'en': 165, 'zh': 165}
# Execute the independently authored behavioral suite against wheel and standalone imports.
testfile = ROOT / 'tests/test_continuation_repair_independent.py'
load_test = "import importlib.util,unittest; s=importlib.util.spec_from_file_location('independent'," + repr(str(testfile)) + "); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(m)); raise SystemExit(not r.wasSuccessful())"
run([python, '-I', '-c', load_test], project)
run([python, '-I', '-c', 'import sys; sys.path.insert(0,' + repr(str(installed / 'scripts')) + '); ' + load_test], project)
# README CLI examples use the documented repository teaching input copied to a separate consumer.
shutil.copytree(ROOT / 'examples', project / 'examples')
run([python, '-I', '-m', 'qa_master', 'init', 'demo-login'], project)
plan = json.loads(run([python, '-I', '-m', 'qa_master', 'plan', '需求评审 + 测试计划 + 编写用例，不执行测试'], project))
assert plan['no_execution']
assert plan['stages'] == ['review', 'test_plan', 'design']
design = json.loads(run([python, '-I', '-m', 'qa_master', 'design', '--input', 'examples/design-methods.json', '--output', '.qa-master/methods.json'], project))
assert design['status'] == 'DRAFT_UNAPPROVED' and design['execution'] == 'NOT_EXECUTED'
run([python, '-I', '-m', 'qa_master', 'status'], project)
run([python, '-I', helper, 'plan', '只评审用例，不要提交缺陷'], project)
run([python, '-I', helper, 'pause', '等待可测试构建'], project)
run([python, '-I', helper, 'resume'], project)
run([python, '-I', '-m', 'qa_master', 'install-codex', '--project', str(project), '--update'], project)
links = []
for filename in ('README.md', 'docs/GETTING_STARTED.md', 'docs/SKILL_CATALOG.md'):
    path = ROOT / filename
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if '://' in target or target.startswith('#'):
            continue
        relative = unquote(target.split('#')[0])
        resolved = path.parent / relative
        links.append({'file': filename, 'target': target, 'exists': resolved.exists()})
assert all(item['exists'] for item in links), [item for item in links if not item['exists']]
(EVIDENCE / 'readme-local-links.json').write_text(json.dumps(links, ensure_ascii=False, indent=2), encoding='utf-8')
summary = {'source_commit': run(['git', 'rev-parse', 'HEAD'], ROOT).strip(), 'scratch': str(scratch),
           'wheel': wheel.name, 'wheel_sha256': digest(wheel.read_bytes()), 'vendor_files_equal': len(manifest),
           'wheel_and_standalone_independent_suite': 'PASS', 'readme_local_links': len(links),
           'readme_commands': 'PASS', 'upstream_network_execution': 'NOT_EXECUTED'}
(EVIDENCE / 'delivery-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
