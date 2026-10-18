#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

from common_parser import PARSERS, detect_format
from evidence_scaffold import prepare_documents, source_candidates, analysis_markdown











def build_analysis(prompt_text, source_text, source_path, fmt):
    return analysis_markdown(prompt_text, source_text, source_path, fmt)


def main() -> None:
    parser = argparse.ArgumentParser(description="Requirements Analysis Plus input preparation (NOT_ASSESSED)")
    parser.add_argument("--input", required=True, type=Path, help="Requirement document path")
    parser.add_argument(
        "--format",
        choices=["auto", "word", "html", "json", "markdown", "excel"],
        default="auto",
        help="Input format. auto means detect by extension.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output markdown path. Default: <input>.analysis.md",
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "prompts" / "requirements-analysis-plus.md",
        help="Prompt template path",
    )
    args = parser.parse_args()

    fmt = detect_format(args.input) if args.format == "auto" else args.format
    parser_fn = PARSERS[fmt]
    parsed_text = parser_fn(args.input)
    prompt_text = args.prompt.read_text(encoding="utf-8", errors="strict")
    analysis = build_analysis(prompt_text, parsed_text, args.input, fmt)

    out = args.output or args.input.with_name(args.input.stem + ".analysis.md")
    out.write_text(analysis, encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
