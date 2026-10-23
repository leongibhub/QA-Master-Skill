"""Reproduce the public CR-033 example; no model or real-system test runs."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--subject", required=True, help="Frozen product Git SHA recorded by the host")
args = parser.parse_args()
if len(args.subject) != 40 or any(char not in "0123456789abcdef" for char in args.subject):
    parser.error("subject must be a full lowercase Git SHA")
sys.path.insert(0, str(ROOT))
from qa_master.case_conformance import audit_method_cases
from qa_master.quality import review_cases

assets = ROOT / "qa_master/skills/codex/examples"
bundle = json.loads((assets / "design-methods.json").read_text(encoding="utf-8"))
library = json.loads((assets / "method-cases.json").read_text(encoding="utf-8"))
legacy_cases = []
for case in library["cases"]:
    requirements = sorted({rid for row in case["scenarios"] for rid in row["requirement_ids"]})
    legacy_cases.append({
        "id": case["id"], "title": case["title"], "priority": "P1",
        "trace": requirements, "dimension": "functional",
        "preconditions": case["preconditions"], "data": case["scenarios"],
        "steps": case["steps"], "expected": case["expected"],
    })
# This set is a demonstration input to the existing link checker, not approval.
requirement_ids = {row["id"] for row in bundle["requirements"]}
old = review_cases(legacy_cases, requirement_ids)
new = audit_method_cases(bundle, library)
result = {
    "subject_commit": args.subject,
    "scope": "Preexisting QA Master requirement-link check versus new finite-scenario audit on the same public scenario rows; not an Awesome/model-quality comparison.",
    "design_input_sha256": new["design_input_sha256"],
    "case_library_sha256": new["case_library_sha256"],
    "preexisting_uncovered_requirement_ids": [
        row["subject"] for row in old["issues"] if row["code"] == "UNCOVERED_REQUIREMENT"
    ],
    "new_audit_summary": new["summary"],
    "new_missing_candidate_ids": [row["id"] for row in new["candidates"] if row["state"] == "MISSING"],
    "artifact_status": new["status"], "product_execution": new["execution"],
    "human_approval": "NOT_AVAILABLE",
}
destination = Path(__file__).with_name("example-comparison-" + args.subject[:7] + ".json")
with destination.open("x", encoding="utf-8") as stream:
    stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=True))
