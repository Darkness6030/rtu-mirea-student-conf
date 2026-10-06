"""Собрать отчёт ПР5 из образца без изменения стилей и других частей DOCX.

Запуск: python scripts/build_report.py (только стандартная библиотека).
После сборки требуется визуальная проверка результата в Word или рендерере.
"""

import json
from pathlib import Path
from xml.dom import minidom
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def build():
    replacements = json.loads((ROOT / "scripts/report_content.json").read_text(encoding="utf-8"))
    source = ROOT / "docs/Отчет_ПР3_Кирьянов.docx"
    target = ROOT / "results/Отчет_ПР5_Кирьянов.docx"
    with ZipFile(source) as archive:
        document = minidom.parseString(archive.read("word/document.xml"))
        body = document.getElementsByTagNameNS(NS, "body")[0]
        paragraphs = [node for node in body.childNodes if node.localName == "p"]
        if len(paragraphs) != 29:
            raise ValueError("Структура образца изменилась")
        for index, value in replacements.items():
            paragraph = paragraphs[int(index)]
            runs = paragraph.getElementsByTagNameNS(NS, "r")
            properties = runs[0].getElementsByTagNameNS(NS, "rPr")
            properties = properties[0].cloneNode(True) if properties else None
            for node in list(paragraph.childNodes):
                if node.localName != "pPr":
                    paragraph.removeChild(node)
            run = document.createElementNS(NS, "w:r")
            if properties is not None:
                run.appendChild(properties)
            for line_index, line in enumerate(value.split("\n")):
                if line_index:
                    run.appendChild(document.createElementNS(NS, "w:br"))
                text = document.createElementNS(NS, "w:t")
                text.setAttribute("xml:space", "preserve")
                text.appendChild(document.createTextNode(line))
                run.appendChild(text)
            paragraph.appendChild(run)
        target.parent.mkdir(exist_ok=True)
        with ZipFile(target, "w") as output:
            for entry in archive.infolist():
                content = (
                    document.toxml(encoding="UTF-8")
                    if entry.filename == "word/document.xml"
                    else archive.read(entry.filename)
                )
                output.writestr(entry, content)
    print(target)


if __name__ == "__main__":
    build()
