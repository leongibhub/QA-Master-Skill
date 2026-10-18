#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

from common_formatter import (
    format_excel_tsv,
    format_json,
    format_markdown,
    write_output,
    write_word_docx,
)
from common_parser import PARSERS, detect_format
from evidence_scaffold import prepare_documents, source_candidates, analysis_markdown


def _load_doc(path: Path, label: str) -> Tuple[str, str]:
    fmt = detect_format(path)
    text = PARSERS[fmt](path)
    return (label, text)











def build_review(prompt_text, docs):
    result = prepare_documents(docs, prompt_text)
    result["next_action"] = "Run prompts/test-case-reviewer-plus.md in an agent. No review findings or coverage conclusion have been produced."
    return result


def _default_output_path(testcase_file: Path, output_format: str) -> Path:
    suffix_map = {
        "markdown": ".review.md",
        "word": ".review.docx",
        "json": ".review.json",
        "excel": ".review.tsv",
    }
    return testcase_file.with_name(testcase_file.stem + suffix_map[output_format])


def main() -> None:
    parser = argparse.ArgumentParser(description="Test-Case-Reviewer Plus input preparation (NOT_ASSESSED)")
    parser.add_argument("--requirement", required=True, type=Path, help="Requirement document file path")
    parser.add_argument("--analysis", type=Path, help="Requirement analysis result file path")
    parser.add_argument("--tech", type=Path, help="Technical document file path")
    parser.add_argument("--plan", type=Path, help="Project plan document file path")
    parser.add_argument("--strategy", type=Path, help="Test strategy document file path")
    parser.add_argument("--testcase", required=True, type=Path, help="Test case document file path")
    parser.add_argument("--other", action="append", type=Path, default=[], help="Other document path, repeatable")
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
        default=Path(__file__).resolve().parents[1] / "prompts" / "test-case-reviewer-plus.md",
        help="Prompt file path",
    )
    args = parser.parse_args()

    docs: List[Tuple[str, str]] = []
    docs.append(_load_doc(args.requirement, "需求文档"))
    docs.append(_load_doc(args.testcase, "测试用例文档"))

    optional_inputs = [
        ("需求分析结果", args.analysis),
        ("技术文档", args.tech),
        ("项目计划", args.plan),
        ("测试策略文档", args.strategy),
    ]
    for label, path in optional_inputs:
        if path:
            docs.append(_load_doc(path, label))

    for idx, p in enumerate(args.other, start=1):
        docs.append(_load_doc(p, f"其他文档{idx}"))

    prompt_text = args.prompt.read_text(encoding="utf-8", errors="strict")
    review = build_review(prompt_text, docs)
    output_path = args.output or _default_output_path(args.testcase, args.output_format)

    if args.output_format == "word":
        write_word_docx(review, output_path)
    elif args.output_format == "markdown":
        write_output(format_markdown(review), output_path)
    elif args.output_format == "json":
        write_output(format_json(review), output_path)
    elif args.output_format == "excel":
        write_output(format_excel_tsv(review), output_path)
    else:
        raise ValueError(f"Unsupported output format: {args.output_format}")

    print(str(output_path))


if __name__ == "__main__":
    main()
