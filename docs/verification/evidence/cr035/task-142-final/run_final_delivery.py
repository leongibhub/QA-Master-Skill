"""One clean archive/wheel/install/installed-helper verification for TASK-142."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


SHA = "8fc8533d4ec533bc5ba1ea66e6f24ef51a92f0f6"
EVIDENCE = Path(__file__).resolve().parent
REPO = EVIDENCE.parents[4]
COMMANDS = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def persist():
    (EVIDENCE / "delivery-commands.json").write_text(
        json.dumps(COMMANDS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run(label, command, cwd):
    completed = subprocess.run(command, cwd=cwd, capture_output=True)
    item = {
        "label": label,
        "command": command,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout": completed.stdout.decode("utf-8", "replace"),
        "stderr": completed.stderr.decode("utf-8", "replace"),
    }
    COMMANDS.append(item)
    persist()
    if completed.returncode:
        raise RuntimeError(label)
    return item


def assert_rejected(label, command, cwd, code, private_root):
    completed = subprocess.run(command, cwd=cwd, capture_output=True)
    stdout = completed.stdout.decode("utf-8", "replace")
    stderr = completed.stderr.decode("utf-8", "replace")
    COMMANDS.append({"label": label, "command": command, "cwd": str(cwd), "returncode": completed.returncode,
                     "stdout": stdout, "stderr": stderr})
    persist()
    if completed.returncode != 2 or stderr or json.loads(stdout) != {"status": "REJECTED", "error": code}:
        raise AssertionError(label + " rejected contract")
    if str(private_root) in stdout or str(private_root) in stderr or "Traceback" in stdout or "Traceback" in stderr:
        raise AssertionError(label + " leaked path or traceback")


def main():
    with tempfile.TemporaryDirectory(prefix="t142-") as temporary:
        root = Path(temporary)
        archive, source, wheel_dir, venv, consumer = root / "source.zip", root / "source", root / "wheel", root / "venv", root / "consumer"
        wheel_dir.mkdir(); consumer.mkdir()
        run("source_freeze", ["git", "rev-parse", SHA], REPO)
        run("archive", ["git", "archive", "--format=zip", "--output", str(archive), SHA], REPO)
        with zipfile.ZipFile(archive) as payload:
            payload.extractall(source)
        run("wheel_build", [sys.executable, "-m", "pip", "wheel", str(source), "--no-deps", "--no-build-isolation", "-w", str(wheel_dir)], consumer)
        wheel = next(wheel_dir.glob("*.whl"))
        run("venv_create", [sys.executable, "-m", "venv", str(venv)], consumer)
        python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        run("wheel_install", [str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)], consumer)
        skill = consumer / "skill"
        run("skill_install", [str(python), "-I", "-m", "qa_master", "install-codex", "--target", str(skill)], consumer)

        for name in ("design-methods.json", "design-methods-after.json", "method-cases.json"):
            shutil.copy2(skill / "examples" / name, consumer / name)
        before, after, cases = (consumer / "design-methods.json", consumer / "design-methods-after.json", consumer / "method-cases.json")
        module_json, module_md = consumer / "module-audit.json", consumer / "module-audit.md"
        helper_json, helper_md = consumer / "helper-audit.json", consumer / "helper-audit.md"
        run("module_audit_json", [str(python), "-I", "-m", "qa_master", "audit-method-cases", "--input", str(before), "--cases", str(cases), "--output", str(module_json)], consumer)
        run("module_audit_markdown", [str(python), "-I", "-m", "qa_master", "audit-method-cases", "--input", str(before), "--cases", str(cases), "--output", str(module_md), "--format", "markdown"], consumer)
        run("helper_audit_json", [str(python), "-I", str(skill / "scripts" / "qa.py"), "audit-method-cases", "--input", str(before), "--cases", str(cases), "--output", str(helper_json)], consumer)
        run("helper_audit_markdown", [str(python), "-I", str(skill / "scripts" / "qa.py"), "audit-method-cases", "--input", str(before), "--cases", str(cases), "--output", str(helper_md), "--format", "markdown"], consumer)

        impact_json, impact_md = consumer / "module-impact.json", consumer / "module-impact.md"
        run("module_impact_json", [str(python), "-I", "-m", "qa_master", "impact-method-cases", "--before", str(before), "--after", str(after), "--cases", str(cases), "--output", str(impact_json)], consumer)
        run("module_impact_markdown", [str(python), "-I", "-m", "qa_master", "impact-method-cases", "--before", str(before), "--after", str(after), "--cases", str(cases), "--output", str(impact_md), "--format", "markdown"], consumer)

        source_data = json.loads(before.read_text(encoding="utf-8"))
        case_data = json.loads(cases.read_text(encoding="utf-8"))
        candidate_id = case_data["cases"][0]["scenarios"][0]["candidate_id"]
        malformed_gap = dict(case_data)
        malformed_gap["gaps"] = [{"candidate_id": candidate_id, "reason_code": {}}]
        malformed_gap_path = consumer / "bad-gap.json"
        malformed_gap_path.write_text(json.dumps(malformed_gap), encoding="utf-8")
        malformed_method = json.loads(before.read_text(encoding="utf-8"))
        malformed_method["design_models"]["models"][0]["method"] = {}
        malformed_method_path = consumer / "bad-method.json"
        malformed_method_path.write_text(json.dumps(malformed_method), encoding="utf-8")
        rejected = consumer / "rejected.json"
        assert_rejected("audit_bad_gap", [str(python), "-I", "-m", "qa_master", "audit-method-cases", "--input", str(before), "--cases", str(malformed_gap_path), "--output", str(rejected)], consumer, "INVALID_GAP", root)
        assert_rejected("impact_bad_gap", [str(python), "-I", "-m", "qa_master", "impact-method-cases", "--before", str(before), "--after", str(before), "--cases", str(malformed_gap_path), "--output", str(rejected)], consumer, "INVALID_GAP", root)
        assert_rejected("audit_bad_method", [str(python), "-I", "-m", "qa_master", "audit-method-cases", "--input", str(malformed_method_path), "--cases", str(cases), "--output", str(rejected)], consumer, "INVALID_SCHEMA", root)
        assert_rejected("impact_bad_method", [str(python), "-I", "-m", "qa_master", "impact-method-cases", "--before", str(malformed_method_path), "--after", str(before), "--cases", str(cases), "--output", str(rejected)], consumer, "INVALID_SCHEMA", root)

        blocker, blocked = consumer / "blocker", consumer / "blocker" / "report.json"
        blocker.write_bytes(b"must-remain")
        assert_rejected("audit_blocked_parent", [str(python), "-I", "-m", "qa_master", "audit-method-cases", "--input", str(before), "--cases", str(cases), "--output", str(blocked)], consumer, "OUTPUT_IO_ERROR", root)
        assert_rejected("impact_blocked_parent", [str(python), "-I", "-m", "qa_master", "impact-method-cases", "--before", str(before), "--after", str(before), "--cases", str(cases), "--output", str(blocked)], consumer, "OUTPUT_IO_ERROR", root)
        if blocker.read_bytes() != b"must-remain" or blocked.exists():
            raise AssertionError("blocked parent safety")

        probe = consumer / "format-probe.py"
        probe.write_text(
            "import json, sys\n"
            "from qa_master.case_conformance import CaseConformanceError, write_case_audit\n"
            "from qa_master.method_impact import MethodImpactError, write_method_impact\n"
            "before, cases, out = map(__import__('pathlib').Path, sys.argv[1:])\n"
            "result = {}\n"
            "try: write_case_audit(before, cases, out, format={})\n"
            "except CaseConformanceError as error: result['audit'] = error.code\n"
            "try: write_method_impact(before, before, cases, out, format={})\n"
            "except MethodImpactError as error: result['impact'] = error.code\n"
            "print(json.dumps(result, sort_keys=True))\n", encoding="utf-8"
        )
        completed = subprocess.run([str(python), "-I", str(probe), str(before), str(cases), str(consumer / "format-output.json")], cwd=consumer, capture_output=True)
        stdout, stderr = completed.stdout.decode("utf-8", "replace"), completed.stderr.decode("utf-8", "replace")
        COMMANDS.append({"label": "direct_format_type", "command": [str(python), "-I", str(probe), "<before>", "<cases>", "<output>"], "cwd": str(consumer), "returncode": completed.returncode, "stdout": stdout, "stderr": stderr})
        persist()
        if completed.returncode or stderr or json.loads(stdout) != {"audit": "INVALID_FORMAT", "impact": "INVALID_FORMAT"}:
            raise AssertionError("format type contract")

        normal = json.loads(module_json.read_text(encoding="utf-8"))
        impact = json.loads(impact_json.read_text(encoding="utf-8"))
        manifest = {
            "source_freeze_sha": SHA,
            "archive_sha256": digest(archive),
            "wheel": {"name": wheel.name, "bytes": wheel.stat().st_size, "sha256": digest(wheel)},
            "installed_skill_file_count": sum(1 for item in skill.rglob("*") if item.is_file()),
            "outputs": {name: {"bytes": path.stat().st_size, "sha256": digest(path)} for name, path in {
                "module_audit_json": module_json, "module_audit_markdown": module_md, "helper_audit_json": helper_json,
                "helper_audit_markdown": helper_md, "module_impact_json": impact_json, "module_impact_markdown": impact_md,
            }.items()},
            "audit": {"status": normal["status"], "execution": normal["execution"], "candidate_denominator": normal["summary"]["candidate_denominator"]},
            "impact": {"status": impact["status"], "execution": impact["execution"], "review_case_count": impact["summary"]["review_case_count"]},
            "rejections": {"bad_gap": "INVALID_GAP", "bad_method": "INVALID_SCHEMA", "blocked_parent": "OUTPUT_IO_ERROR", "format": "INVALID_FORMAT"},
        }
        (EVIDENCE / "delivery-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        (EVIDENCE / "delivery-script-error.txt").write_text(
            f"{type(error).__name__}: {error}\n", encoding="utf-8"
        )
        (EVIDENCE / "delivery-script-exit.txt").write_text("1\n", encoding="utf-8")
        raise
    else:
        (EVIDENCE / "delivery-script-exit.txt").write_text("0\n", encoding="utf-8")
