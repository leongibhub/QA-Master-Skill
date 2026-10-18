#!/usr/bin/env python3
import json
import re
import zipfile
from pathlib import Path
from html.parser import HTMLParser
from typing import Callable, Dict
from xml.etree import ElementTree as ET
from xlsx_reader import read_workbook


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self._parts.append(text)

    def get_text(self) -> str:
        return "\n".join(self._parts)


def parse_word(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as f:
            root = ET.fromstring(f.read())
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    lines = []
    for p in root.findall(".//w:p", ns):
        texts = [t.text for t in p.findall(".//w:t", ns) if t.text]
        line = "".join(texts).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def parse_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    parser = _HTMLTextExtractor()
    parser.feed(raw)
    return parser.get_text()


def _flatten_json(prefix: str, value, out: list) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            _flatten_json(key, v, out)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            key = f"{prefix}[{i}]"
            _flatten_json(key, v, out)
    else:
        out.append(f"{prefix}: {value}")


def parse_json(path: Path) -> str:
    obj = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    out = []
    _flatten_json("", obj, out)
    return "\n".join(out)


def parse_markdown(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _read_shared_strings(zf: zipfile.ZipFile) -> list:
    try:
        with zf.open("xl/sharedStrings.xml") as f:
            root = ET.fromstring(f.read())
    except KeyError:
        return []
    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    strings = []
    for si in root.findall(".//a:si", ns):
        parts = [t.text or "" for t in si.findall(".//a:t", ns)]
        strings.append("".join(parts))
    return strings


def parse_excel(path: Path) -> str:
    sheets = read_workbook(path)
    lines = []
    for sheet in sheets:
        lines.append("## Worksheet: " + sheet["name"])
        for number, row in zip(sheet["row_numbers"], sheet["rows"]):
            lines.append(f"row {number}: " + json.dumps(row, ensure_ascii=False))
    return "\n".join(lines)


PARSERS: Dict[str, Callable[[Path], str]] = {
    "word": parse_word,
    "html": parse_html,
    "json": parse_json,
    "markdown": parse_markdown,
    "excel": parse_excel,
}


def detect_format(path: Path) -> str:
    ext = path.suffix.lower()
    mapping = {
        ".docx": "word",
        ".html": "html",
        ".htm": "html",
        ".json": "json",
        ".md": "markdown",
        ".markdown": "markdown",
        ".xlsx": "excel",
        ".xlsm": "excel",
    }
    if ext not in mapping:
        raise ValueError(f"Unsupported file extension: {ext}")
    return mapping[ext]
