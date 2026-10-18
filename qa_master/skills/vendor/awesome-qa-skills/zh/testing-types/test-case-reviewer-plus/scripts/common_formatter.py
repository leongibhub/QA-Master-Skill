#!/usr/bin/env python3
import json
import zipfile
from xml.sax.saxutils import escape
from pathlib import Path
from typing import Dict


ORDERED_KEYS = ["artifact_mode", "analysis_status", "sources", "prompt_hash", "pending_human_decisions", "next_action"]


def review_to_lines(artifact):
    return ["Evidence preparation — NOT_ASSESSED", ""] + [key + ": " + json.dumps(artifact.get(key), ensure_ascii=False) for key in ORDERED_KEYS]


def format_markdown(artifact):
    lines = ["# Evidence preparation — NOT_ASSESSED", ""]
    for key in ORDERED_KEYS:
        lines += ["## " + key, "", "~~~~json", json.dumps(artifact.get(key), ensure_ascii=False, indent=2), "~~~~", ""]
    return "\n".join(lines)


def format_json(review: Dict[str, str]) -> str:
    return json.dumps(review, ensure_ascii=False, indent=2) + "\n"


def format_excel_tsv(artifact):
    rows = ["field\tvalue"]
    for key in ORDERED_KEYS:
        value = json.dumps(artifact.get(key), ensure_ascii=False).replace("\t", " ").replace("\n", " ")
        rows.append(key + "\t" + value)
    return "\n".join(rows) + "\n"


def _paragraph_xml(text: str) -> str:
    return (
        "<w:p>"
        "<w:r>"
        "<w:t xml:space=\"preserve\">"
        f"{escape(text)}"
        "</w:t>"
        "</w:r>"
        "</w:p>"
    )


def _build_docx_xml(review: Dict[str, str]) -> str:
    body = "".join(_paragraph_xml(x) for x in review_to_lines(review))
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
        "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
        "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
        "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
        "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
        "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
        "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
        "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
        "xmlns:wne=\"http://schemas.microsoft.com/office/word/2006/wordml\" "
        "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
        "mc:Ignorable=\"w14 wp14\">"
        "<w:body>"
        f"{body}"
        "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
        "</w:body>"
        "</w:document>"
    )


def write_word_docx(review: Dict[str, str], path: Path) -> None:
    content_types = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
        "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
        "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
        "<Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>"
        "</Types>"
    )
    rels = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
        "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>"
        "</Relationships>"
    )
    document_xml = _build_docx_xml(review)

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", document_xml)


def write_output(content: str, path: Path) -> None:
    path.write_text(content, encoding="utf-8")
