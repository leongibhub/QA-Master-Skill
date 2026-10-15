"""One-command offline campaign draft. Never executes tests or approves requirements."""
from __future__ import annotations
import argparse,hashlib,json,os,tempfile
from pathlib import Path
from .quality import analyze_requirements,review_cases
from .coverage_design import design_matrix
from .design_methods import DesignMethodError, design_methods, load_bundle_json
from .skill_registry import select_skills


def _ids(values):
    """Return stable unique IDs or reject an ambiguous installed projection."""
    if any(not isinstance(value, str) or not value for value in values):
        raise ValueError("INVALID_INSTALLED_PROJECTION")
    result = sorted(values)
    if len(result) != len(set(result)):
        raise ValueError("INVALID_INSTALLED_PROJECTION")
    return result


def _installed_design(bundle, report):
    """Add the DES-055 installed-workflow metadata without changing design output."""
    requirements = bundle["requirements"]
    requirement_ids = _ids([item.get("id") for item in requirements])
    requirement_by_id = {item["id"]: item for item in requirements}
    methods = report.get("method_design")
    models = bundle.get("design_models", {}).get("models", []) if methods is not None else []
    candidates = methods["candidates"] if methods is not None else []
    obligations = methods["obligations"] if methods is not None else []
    candidate_by_id = {item["id"]: item for item in candidates}
    obligation_by_id = {item["id"]: item for item in obligations}
    if len(candidate_by_id) != len(candidates) or len(obligation_by_id) != len(obligations):
        raise ValueError("INVALID_INSTALLED_PROJECTION")
    source_refs = bundle.get("design_models", {}).get("source_refs", [])
    source_ids = _ids([item["id"] for item in source_refs]) if methods is not None else []
    source_by_id = {item["id"]: item for item in source_refs}
    requirement_models = {item: set() for item in requirement_ids}
    requirement_candidates = {item: set() for item in requirement_ids}
    requirement_obligations = {item: set() for item in requirement_ids}
    source_models = {item: set() for item in source_ids}
    source_candidates = {item: set() for item in source_ids}
    source_obligations = {item: set() for item in source_ids}
    source_requirements = {item: set() for item in source_ids}
    for model in models:
        for requirement_id in model["requirement_ids"]:
            requirement_models[requirement_id].add(model["id"])
        for source_id in model["source_refs"]:
            source_models[source_id].add(model["id"])
            source_requirements[source_id].update(model["requirement_ids"])
    for candidate in candidates:
        for requirement_id in candidate["trace"]:
            requirement_candidates[requirement_id].add(candidate["id"])
        for source in candidate["source_refs"]:
            source_candidates[source["id"]].add(candidate["id"])
            source_models[source["id"]].add(candidate["model_id"])
            source_requirements[source["id"]].update(candidate["trace"])
    for obligation in obligations:
        for requirement_id in obligation["requirement_ids"]:
            requirement_obligations[requirement_id].add(obligation["id"])
        for source in obligation["source_refs"]:
            source_obligations[source["id"]].add(obligation["id"])
            source_models[source["id"]].add(obligation["model_id"])
            source_requirements[source["id"]].update(obligation["requirement_ids"])

    dimensions = sorted({item.get("dimension") for item in requirements
                         if isinstance(item.get("dimension"), str) and item["dimension"]})
    selected = select_skills(intent="design", dimensions=dimensions, risk=None) if dimensions else {
        "selected": [], "gaps": []
    }
    guides = []
    for guide in selected["selected"]:
        guide_path = Path(guide["path"])
        guide_dimensions = set(guide["dimensions"])
        guides.append({
            "id": guide["id"], "file": guide["file"],
            "locator": "scripts/qa_master/skills/professional/" + guide["file"],
            "sha256": hashlib.sha256(guide_path.read_bytes()).hexdigest(),
            "requirement_ids": sorted(item["id"] for item in requirements
                                      if item.get("dimension") in guide_dimensions),
            "model_ids": sorted(item["id"] for item in models
                                if item.get("dimension") in guide_dimensions),
        })
    guides.sort(key=lambda item: item["id"])

    source_rows = []
    for requirement_id in requirement_ids:
        requirement = requirement_by_id[requirement_id]
        source = requirement.get("source")
        if isinstance(source, str) and source:
            source_rows.append({
                "origin": "REQUIREMENT_SOURCE", "source_id": requirement_id,
                "kind": "requirement", "locator": source, "sha256": None,
                "binding_state": "DECLARED", "requirement_ids": [requirement_id],
                "model_ids": sorted(requirement_models[requirement_id]),
                "candidate_ids": sorted(requirement_candidates[requirement_id]),
                "obligation_ids": sorted(requirement_obligations[requirement_id]),
            })
    for source_id in source_ids:
        source = source_by_id[source_id]
        linked_candidates = source_candidates[source_id]
        linked_obligations = source_obligations[source_id]
        source_rows.append({
            "origin": "DESIGN_MODEL_SOURCE", "source_id": source_id,
            "kind": source["kind"], "locator": source["locator"],
            "sha256": source.get("sha256"),
            "binding_state": "DECLARED_DIGEST" if "sha256" in source else "DECLARED",
            "requirement_ids": sorted(source_requirements[source_id]),
            "model_ids": sorted(source_models[source_id]),
            "candidate_ids": sorted(linked_candidates),
            "obligation_ids": sorted(linked_obligations),
        })
    source_rows.sort(key=lambda item: (item["origin"], item["source_id"]))
    if len({(item["origin"], item["source_id"]) for item in source_rows}) != len(source_rows):
        raise ValueError("INVALID_INSTALLED_PROJECTION")

    gaps = list(selected["gaps"])
    if not dimensions:
        gaps.append({"code": "GUIDE_DIMENSION_NOT_SUPPLIED"})
    if methods is None:
        gaps.append({"code": "METHOD_MODELS_NOT_SUPPLIED"})
    elif not models:
        gaps.append({"code": "METHOD_MODELS_EMPTY"})
    for requirement_id in requirement_ids:
        requirement = requirement_by_id[requirement_id]
        if not (isinstance(requirement.get("source"), str) and requirement["source"]) and not requirement_models[requirement_id]:
            gaps.append({"code": "SOURCE_NOT_SUPPLIED", "requirement_id": requirement_id})
    if candidates or obligations:
        gaps.append({"code": "METHOD_OUTPUT_REQUIRES_CASE_COMPLETION"})
    gaps.sort(key=lambda item: (item["code"], item.get("requirement_id", "")))
    report["installed_design"] = {
        "schema_version": 1, "entry_point": "scripts/qa.py design",
        "status": "DRAFT_UNAPPROVED", "execution": "NOT_EXECUTED",
        "state_access": "NONE", "external_writes": "REQUESTED_OUTPUT_ONLY",
        "guides": guides, "source_mapping": source_rows, "gaps": gaps,
        "method_output": {
            "present": methods is not None,
            "candidate_ids": _ids(list(candidate_by_id)),
            "obligation_ids": _ids(list(obligation_by_id)),
            "usable_case_claim": False, "executable_case_claim": False,
        },
    }
    return report

def prepare_campaign(bundle):
    if not isinstance(bundle,dict):raise ValueError("Expected JSON object")
    project=bundle.get("project");requirements=bundle.get("requirements")
    if not isinstance(project,str) or not project.strip():raise ValueError("Project required")
    if not isinstance(requirements,list) or len(requirements)>10000 or not all(isinstance(r,dict) for r in requirements):
        raise ValueError("requirements must be <=10000 objects")
    method_design = design_methods(bundle) if 'design_models' in bundle else None
    requirements_review=analyze_requirements(requirements)
    design=design_matrix(requirements,applicable=bundle.get("applicability"))
    approved={str(r["id"]) for r in requirements if r.get("approved") is True and r.get("id")}
    case_review=review_cases(design["cases"],approved)
    digest=hashlib.sha256(json.dumps(bundle,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    report = {"schema_version":1,"project":project.strip(),"input_sha256":digest,
            "requirement_review":requirements_review,"test_cases":design["cases"],
            "coverage":design["coverage"],"case_review":case_review,
            "unresolved":{"requirement_blockers":[f for f in requirements_review["findings"] if f["severity"]=="BLOCKER"],
                          "design_gaps":design["gaps"]},
            "workflow":{"requirements_review":"WAITING_HUMAN_APPROVAL",
                        "test_design":"DRAFT_ONLY","execution":"NOT_AUTHORIZED","synapsert":"NOT_WRITTEN"},
            "formal_baseline_approved":False}
    if method_design is not None:
        report['method_design'] = method_design
    return report

def write_campaign(bundle_path,output_path, *, installed_projection=False):
    source=Path(bundle_path).resolve(strict=True);destination=Path(output_path).resolve()
    if destination==source:raise ValueError("Output must not overwrite input")
    if source.stat().st_size>5_000_000:raise ValueError("Input too large")
    payload=source.read_bytes()
    if len(payload)>5_000_000:raise ValueError("Input too large")
    bundle = load_bundle_json(payload)
    result=prepare_campaign(bundle)
    if installed_projection:
        _installed_design(bundle, result)
    destination.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=".qa-master-",suffix=".json",dir=destination.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as out:
            json.dump(result,out,ensure_ascii=False,indent=2);out.write("\n")
        os.replace(tmp,destination)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return result

def main(argv=None):
    p=argparse.ArgumentParser(description="Generate offline QA design and review draft")
    p.add_argument("--input",required=True);p.add_argument("--output",required=True)
    a=p.parse_args(argv)
    try:
        report=write_campaign(a.input,a.output)
    except DesignMethodError as error:
        print(json.dumps({'status':'REJECTED','error':error.code},ensure_ascii=True))
        return 2
    except (ValueError,TypeError,KeyError):
        print(json.dumps({'status':'REJECTED','error':'INVALID_CAMPAIGN_INPUT'},ensure_ascii=True))
        return 2
    except OSError:
        print(json.dumps({'status':'REJECTED','error':'CAMPAIGN_IO_ERROR'},ensure_ascii=True))
        return 2
    summary={"project":report["project"],"cases":len(report["test_cases"]),
      "requirement_findings":len(report["requirement_review"]["findings"]),
      "unresolved_design":len(report["unresolved"]["design_gaps"]),"status":"DRAFT_UNAPPROVED",
      "output":a.output}
    if 'method_design' in report:
        summary.update(method_candidates=report['method_design']['summary']['candidate_count'],
                       method_obligations=report['method_design']['summary']['obligation_count'],
                       execution='NOT_AUTHORIZED')
    print(json.dumps(summary,ensure_ascii=True))
    return 0
if __name__=="__main__":raise SystemExit(main())
