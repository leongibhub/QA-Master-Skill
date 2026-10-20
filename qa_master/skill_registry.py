"""Discover and route QA Master's bundled professional guidance.

This module only selects instructional files.  It neither invokes an agent nor
executes a test, so callers must preserve the returned planning-only state.
"""
from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Iterable
import re
from .intent import mention_states

from .core import DIMENSIONS, SKILLS, DIMENSION_SKILLS

_GUIDE_FILES = (
    "requirements-review.md",
    "functional-api.md",
    "structural-integration.md",
    "nonfunctional-compatibility.md",
    "security-recovery.md",
    "regression-evidence.md",
)
_VALID_RISKS = {"low", "medium", "high"}
_REQUIRED_FIELDS = {"id", "title", "dimensions", "intents", "risks", "artifacts"}


def bundled_skill_root():
    """Return the package-resource directory holding the canonical guides.

    ``Traversable`` is deliberately returned instead of assuming resources are
    ordinary filesystem files; installed zip-compatible packages can therefore
    still be inspected through the resource API.
    """
    return resources.files("qa_master").joinpath("skills", "professional")


def _values(value: object) -> tuple[str, ...]:
    if not isinstance(value, str):
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _metadata(text: str) -> dict[str, object] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    result: dict[str, object] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key or not value or key in result:
            return None
        result[key] = _values(value) if key in {"dimensions", "intents", "risks", "artifacts"} else value
    else:
        return None
    return result


def _iter_files(root) -> Iterable[object]:
    try:
        return sorted(root.iterdir(), key=lambda item: item.name)
    except (FileNotFoundError, NotADirectoryError, AttributeError):
        return ()


def discover_skills(root=None, *, required_files: Iterable[str] = _GUIDE_FILES) -> dict:
    """Return only valid guides physically present under *root*.

    Invalid, unreadable and missing required guides are explicit gaps.  A
    caller may pass a temporary ``Path`` in tests; normal operation reads the
    installed package resource directory.
    """
    root = bundled_skill_root() if root is None else root
    files = {item.name: item for item in _iter_files(root) if getattr(item, "is_file", lambda: False)()}
    guides, gaps, seen_ids = [], [], set()
    for expected in required_files:
        if expected not in files:
            gaps.append({"code": "GUIDE_FILE_MISSING", "file": expected})
    for name, item in sorted(files.items()):
        if not name.endswith(".md"):
            continue
        try:
            parsed = _metadata(item.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            gaps.append({"code": "GUIDE_FILE_UNREADABLE", "file": name})
            continue
        if not parsed or _REQUIRED_FIELDS - set(parsed):
            gaps.append({"code": "GUIDE_METADATA_INVALID", "file": name})
            continue
        invalid_dimensions = set(parsed["dimensions"]) - set(DIMENSIONS)
        invalid_risks = set(parsed["risks"]) - _VALID_RISKS
        if invalid_dimensions:
            gaps.append({"code": "GUIDE_DIMENSION_INVALID", "file": name, "dimensions": sorted(invalid_dimensions)})
            continue
        if invalid_risks or not parsed["intents"] or not parsed["artifacts"]:
            gaps.append({"code": "GUIDE_METADATA_INVALID", "file": name})
            continue
        if parsed["id"] in seen_ids:
            gaps.append({"code": "GUIDE_ID_DUPLICATE", "file": name, "id": parsed["id"]})
            continue
        seen_ids.add(parsed["id"])
        guides.append({**parsed, "file": name, "path": str(item)})
    return {"guides": guides, "gaps": gaps, "status": "DISCOVERED" if guides else "NO_GUIDES_AVAILABLE"}


def _requested(value: str | Iterable[str] | None) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def select_skills(intent: str | Iterable[str] | None = None, dimensions: Iterable[str] | None = None,
                  risk: str | None = None, *, root=None) -> dict:
    """Select verified instructional artifacts for the requested planning work."""
    requested_intents = _requested(intent)
    requested_dimensions = _requested(dimensions)
    found = discover_skills(root)
    gaps = list(found["gaps"])
    unknown = sorted(set(requested_dimensions) - set(DIMENSIONS))
    if unknown:
        gaps.append({"code": "UNKNOWN_DIMENSION", "dimensions": unknown})
    if risk is not None and risk not in _VALID_RISKS:
        gaps.append({"code": "UNKNOWN_RISK", "risk": risk})
    selected = []
    for guide in found["guides"]:
        if requested_intents and not set(requested_intents).intersection(guide["intents"]):
            continue
        if requested_dimensions and not set(requested_dimensions).intersection(guide["dimensions"]):
            continue
        if risk and risk in _VALID_RISKS and risk not in guide["risks"]:
            continue
        selected.append(guide)
    if not selected and not unknown:
        gaps.append({"code": "NO_MATCHING_BUNDLED_GUIDE", "intent": list(requested_intents),
                     "dimensions": list(requested_dimensions), "risk": risk})
    return {
        "status": "PLANNING_ONLY",
        "execution": "NOT_EXECUTED",
        "requested": {"intent": list(requested_intents), "dimensions": list(requested_dimensions), "risk": risk},
        "selected": selected,
        "gaps": gaps,
    }


_VENDOR_LANGS = ("en", "zh")
_VENDOR_CATEGORIES = ("testing-workflows", "testing-types", "skill-engineering")


def vendor_skill_root():
    """Return the package-resource directory holding vendored breadth skills."""
    return resources.files("qa_master").joinpath("skills", "vendor", "awesome-qa-skills")


def _vendor_metadata(text: str) -> dict[str, str] | None:
    """Parse a vendored ``SKILL.md`` frontmatter into its name/description map."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    result: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key or not value or key in result:
            return None
        result[key] = value
    if "name" not in result or "description" not in result:
        return None
    return result


def discover_vendor_skills(root=None) -> dict:
    """Discover vendored awesome-qa-skills breadth leaves (en + zh).

    Vendored skills are Markdown prompt workflows without QA Master's
    deterministic engine; QA Master only discovers and routes them and never
    executes their content locally.
    """
    root = vendor_skill_root() if root is None else root
    skills, gaps = [], []
    for lang in _VENDOR_LANGS:
        for category in _VENDOR_CATEGORIES:
            category_root = root.joinpath(lang).joinpath(category)
            for skill_dir in _iter_files(category_root):
                if not getattr(skill_dir, "is_dir", lambda: False)():
                    continue
                skill_file = skill_dir.joinpath("SKILL.md")
                try:
                    metadata = _vendor_metadata(skill_file.read_text(encoding="utf-8"))
                except (OSError, UnicodeError):
                    gaps.append({"code": "VENDOR_SKILL_UNREADABLE", "path": str(skill_file)})
                    continue
                if not metadata:
                    gaps.append({"code": "VENDOR_SKILL_METADATA_INVALID", "path": str(skill_file)})
                    continue
                skills.append({
                    "name": metadata["name"],
                    "description": metadata["description"],
                    "language": lang,
                    "category": category,
                    "path": str(skill_file),
                })
    return {
        "skills": skills,
        "gaps": gaps,
        "count": len(skills),
        "status": "DISCOVERED" if skills else "NO_VENDOR_SKILLS_AVAILABLE",
    }


def select_vendor_skills(stages=None, dimensions=None, *, root=None, prompt=None, language=None, names=None) -> dict:
    """Route planning stages/dimensions to matching vendored breadth skills.

    Stages/dimensions, explicit catalog names and a small documented bilingual
    alias set are deterministic selectors, not arbitrary language understanding.
    Missing names and ambiguous aliases are reported as gaps. Prompt calls prefer
    Chinese for Chinese text and English otherwise; stage-only calls retain both
    languages for compatibility. This never authorizes or executes a workflow.
    """
    requested_stages = _requested(stages)
    requested_dimensions = _requested(dimensions)
    discovered = discover_vendor_skills(root)
    by_name: dict[str, list] = {}
    for skill in discovered["skills"]:
        by_name.setdefault(skill["name"], []).append(skill)
    wanted = set()
    for stage in requested_stages:
        wanted.update(SKILLS.get(stage, ()))
    for dimension in requested_dimensions:
        name = DIMENSION_SKILLS.get(dimension)
        if name:
            wanted.add(name)
    gaps = list(discovered["gaps"])
    matches = []
    text = prompt.casefold() if isinstance(prompt, str) else ""
    preferred = language
    if preferred is None and prompt is not None:
        preferred = "zh" if re.search(r"[\u3400-\u9fff]", text) else "en"
    if preferred not in (None, "zh", "en"):
        raise ValueError("language must be en or zh")
    explicit = set(_requested(names))
    excluded = set()
    for name in by_name:
        positive, negative = mention_states(text, (name,))
        if negative: excluded.add(name)
        elif positive:
            explicit.add(name)
            matches.append({"term": name, "names": [name], "basis": "CANONICAL_NAME"})
    aliases = {
        "property based testing": ("property-based-testing",),
        "property-based testing": ("property-based-testing",),
        "属性测试": ("property-based-testing",),
        "基于属性的测试": ("property-based-testing",),
        "chaos engineering": ("chaos-testing",),
        "chaos testing": ("chaos-testing",),
        "混沌测试": ("chaos-testing",),
        "混沌工程": ("chaos-testing",),
        "playwright": ("ui-test-playwright",),
        "rag testing": ("rag-quality-testing", "rag-retrieval-testing"),
        "rag 测试": ("rag-quality-testing", "rag-retrieval-testing"),
        "rag测试": ("rag-quality-testing", "rag-retrieval-testing"),
    }
    for term, targets in aliases.items():
        positive, negative = mention_states(text, (term,))
        if negative: excluded.update(targets)
        elif positive:
            explicit.update(targets)
            matches.append({"term": term, "names": list(targets), "basis": "CURATED_ALIAS"})
            if len(targets) > 1:
                gaps.append({"code": "AMBIGUOUS_SPECIALIST_REQUEST", "term": term,
                             "candidates": list(targets)})
    wanted.update(explicit)
    wanted.difference_update(excluded)
    selected = []
    for name in sorted(wanted):
        candidates = by_name.get(name, ())
        if not candidates:
            gaps.append({"code": "REQUESTED_VENDOR_SKILL_UNAVAILABLE", "name": name})
            continue
        localized = [item for item in candidates if item["language"] == preferred]
        selected.extend(localized if preferred and localized else candidates)
        if preferred and not localized:
            gaps.append({"code": "PREFERRED_LANGUAGE_UNAVAILABLE", "name": name, "language": preferred})
    if not selected:
        gaps.append({"code": "NO_MATCHING_VENDOR_SKILL", "routing": "canonical names or curated aliases or stage/dimension mappings"})
    return {
        "status": "PLANNING_ONLY",
        "execution": "NOT_EXECUTED",
        "requested": {"stages": list(requested_stages), "dimensions": list(requested_dimensions), "language": preferred, "names": list(_requested(names))},
        "matches": matches,
        "wanted": sorted(wanted),
        "selected": selected,
        "count": len(selected),
        "vendor_skill_count": discovered["count"],
        "gaps": gaps,
    }
