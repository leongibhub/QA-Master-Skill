#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from typing import List, Dict

from common_formatter import (
    format_excel_tsv,
    format_json,
    format_markdown,
    write_word_docx,
    write_output,
)
from common_parser import PARSERS, detect_format
from evidence_scaffold import prepare_documents, source_candidates, analysis_markdown











def generate_test_cases(req_text, ana_text):
    return source_candidates(req_text, ana_text)


def _render(content_cases: List[Dict], output_format: str) -> str:
    if output_format == "markdown":
        return format_markdown(content_cases)
    if output_format == "json":
        return format_json(content_cases)
    if output_format == "excel":
        return format_excel_tsv(content_cases)
    raise ValueError(f"Unsupported output format: {output_format}")


def _default_output_path(requirement_file: Path, output_format: str) -> Path:
    suffix_map = {
        "markdown": ".testcases.md",
        "word": ".testcases.docx",
        "json": ".testcases.json",
        "excel": ".testcases.tsv",
    }
    return requirement_file.with_name(requirement_file.stem + suffix_map[output_format])


def main() -> None:
    parser = argparse.ArgumentParser(description="TestcaseWriter Plus input preparation (NOT_ASSESSED)")
    parser.add_argument("--requirement", required=True, type=Path, help="Requirement document file path")
    parser.add_argument("--analysis", required=True, type=Path, help="Requirement analysis result file path")
    parser.add_argument(
        "--output-format",
        default="markdown",
        choices=["markdown", "word", "json", "excel"],
        help="Output format, default is markdown",
    )
    parser.add_argument("--output", type=Path, help="Output file path")
    parser.add_argument(
        "--prompt",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "prompts" / "testcase-writer-plus.md",
        help="Prompt file path",
    )
    args = parser.parse_args()

    req_fmt = detect_format(args.requirement)
    ana_fmt = detect_format(args.analysis)
    req_text = PARSERS[req_fmt](args.requirement)
    ana_text = PARSERS[ana_fmt](args.analysis)

    # Reading the prompt checks its presence; this deterministic script does not execute it.
    prompt_text = args.prompt.read_text(encoding="utf-8", errors="strict")

    cases = generate_test_cases(req_text, ana_text)
    import hashlib
    for candidate in cases:
        candidate["prompt_hash"] = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    output_path = args.output or _default_output_path(args.requirement, args.output_format)
    if args.output_format == "word":
        write_word_docx(cases, output_path)
    else:
        rendered = _render(cases, args.output_format)
        write_output(rendered, output_path)
    print(str(output_path))


if __name__ == "__main__":
    main()
