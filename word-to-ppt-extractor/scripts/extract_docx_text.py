#!/usr/bin/env python3
import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def text_from_node(node):
    parts = []
    for item in node.iter():
        if item.tag == f"{{{NS['w']}}}t":
            parts.append(item.text or "")
        elif item.tag == f"{{{NS['w']}}}tab":
            parts.append("\t")
        elif item.tag == f"{{{NS['w']}}}br":
            parts.append("\n")
    return "".join(parts).strip()


def paragraph_style(paragraph):
    style = paragraph.find("./w:pPr/w:pStyle", NS)
    if style is None:
        return ""
    return style.attrib.get(f"{{{NS['w']}}}val", "")


def extract_docx(path):
    path = Path(path)
    with zipfile.ZipFile(path) as docx:
        document_xml = docx.read("word/document.xml")
        root = ET.fromstring(document_xml)

        blocks = []
        for child in root.findall(".//w:body/*", NS):
            if child.tag == f"{{{NS['w']}}}p":
                text = text_from_node(child)
                if not text:
                    continue
                style = paragraph_style(child)
                level = None
                match = re.search(r"Heading([1-6])|标题([1-6])", style, re.I)
                if match:
                    level = int(match.group(1) or match.group(2))
                blocks.append({"type": "paragraph", "style": style, "level": level, "text": text})
            elif child.tag == f"{{{NS['w']}}}tbl":
                rows = []
                for tr in child.findall(".//w:tr", NS):
                    cells = [text_from_node(tc) for tc in tr.findall("./w:tc", NS)]
                    if any(cells):
                        rows.append(cells)
                if rows:
                    blocks.append({"type": "table", "rows": rows})

        media = []
        for name in docx.namelist():
            if name.startswith("word/media/"):
                info = docx.getinfo(name)
                media.append({"path": name, "bytes": info.file_size})

    plain_parts = []
    for block in blocks:
        if block["type"] == "paragraph":
            prefix = "#" * block["level"] + " " if block.get("level") else ""
            plain_parts.append(prefix + block["text"])
        elif block["type"] == "table":
            for row in block["rows"]:
                plain_parts.append(" | ".join(row))

    return {
        "source": str(path),
        "word_count_estimate": len(re.findall(r"\w+|[\u4e00-\u9fff]", "\n".join(plain_parts))),
        "blocks": blocks,
        "media": media,
        "plain_text": "\n\n".join(plain_parts),
    }


def main():
    parser = argparse.ArgumentParser(description="Extract structured text from a .docx file.")
    parser.add_argument("docx")
    parser.add_argument("-o", "--output", help="Write JSON result to this path.")
    args = parser.parse_args()

    result = extract_docx(args.docx)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
