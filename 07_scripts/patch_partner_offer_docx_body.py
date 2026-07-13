from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = ROOT / "01_docs/legal/Коммерческое_предложение_партнерам_Светон.docx"

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP = {"w": NS_W}

ROLE_ROW_NEW = "Проводит технический осмотр объекта, проверяет условия подключения, щиты, ввод, место установки, нагрузки и ограничения, делает фото/видео и фиксирует результаты осмотра."
ROLE_PAY_NEW = "Светон выплачивает вознаграждение за технический осмотр объекта и отчет по результатам осмотра."
EXCLUSIVE_RULE = "По одному клиенту Светон выплачивает вознаграждение только одному партнеру. Одновременное применение форматов Тип А и Тип Б к одному клиенту не допускается."
MONTAGE_RULE = "Если по объекту возникает необходимость монтажа, подготовительных или иных работ, такие работы согласуются между клиентом и партнером отдельно и оплачиваются клиентом напрямую партнеру."
EXCLUSIVE_MARKER = "По одному клиенту Светон выплачивает вознаграждение только одному партнеру."
MONTAGE_MARKER = "Если по объекту возникает необходимость монтажа"


def w_tag(name: str) -> str:
    return f"{{{NS_W}}}{name}"


def paragraph_text(p) -> str:
    return "".join(p.itertext()).strip()


def build_paragraph(text: str):
    p = etree.Element(w_tag("p"))
    p_pr = etree.SubElement(p, w_tag("pPr"))
    spacing = etree.SubElement(p_pr, w_tag("spacing"))
    spacing.set(w_tag("before"), "0")
    spacing.set(w_tag("after"), "140")
    spacing.set(w_tag("line"), "259")
    spacing.set(w_tag("lineRule"), "auto")

    r = etree.SubElement(p, w_tag("r"))
    r_pr = etree.SubElement(r, w_tag("rPr"))
    r_fonts = etree.SubElement(r_pr, w_tag("rFonts"))
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        r_fonts.set(w_tag(key), "Calibri")
    color = etree.SubElement(r_pr, w_tag("color"))
    color.set(w_tag("val"), "000000")
    sz = etree.SubElement(r_pr, w_tag("sz"))
    sz.set(w_tag("val"), "25")
    sz_cs = etree.SubElement(r_pr, w_tag("szCs"))
    sz_cs.set(w_tag("val"), "25")
    t = etree.SubElement(r, w_tag("t"))
    t.text = text
    return p


def main() -> None:
    with ZipFile(DOCX_PATH, "r") as zin:
        xml = zin.read("word/document.xml")
        root = etree.fromstring(xml)
        body = root.find("w:body", namespaces=NSMAP)
        if body is None:
            raise RuntimeError("document.xml has no body")

        # Update the roles table wording.
        tables = body.findall("w:tbl", namespaces=NSMAP)
        if len(tables) < 3:
            raise RuntimeError("Expected at least 3 tables in document body")

        roles_tbl = tables[1]
        rows = roles_tbl.findall("w:tr", namespaces=NSMAP)
        for row in rows[1:]:
            cells = row.findall("w:tc", namespaces=NSMAP)
            if len(cells) < 3:
                continue
            role_name = paragraph_text(cells[0])
            if role_name == "Технический осмотр и сбор исходных данных":
                for cell, text in ((cells[1], ROLE_ROW_NEW), (cells[2], ROLE_PAY_NEW)):
                    for child in list(cell):
                        cell.remove(child)
                    p = build_paragraph(text)
                    cell.append(p)
                break

        # Remove all existing copies of the exclusivity and montage paragraphs.
        to_remove = []
        for child in list(body):
            if child.tag != w_tag("p"):
                continue
            text = paragraph_text(child)
            if EXCLUSIVE_MARKER in text or MONTAGE_MARKER in text:
                to_remove.append(child)
        for child in to_remove:
            body.remove(child)

        # Insert the two paragraphs right after the formats table.
        formats_tbl = body.findall("w:tbl", namespaces=NSMAP)[2]
        exclusive_p = build_paragraph(EXCLUSIVE_RULE)
        montage_p = build_paragraph(MONTAGE_RULE)
        formats_tbl.addnext(exclusive_p)
        exclusive_p.addnext(montage_p)

        new_xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

        tmp_path = DOCX_PATH.with_name(DOCX_PATH.stem + ".__tmp__.docx")

        with ZipFile(DOCX_PATH, "r") as zin2, ZipFile(tmp_path, "w", compression=ZIP_DEFLATED) as zout:
            for item in zin2.infolist():
                data = new_xml if item.filename == "word/document.xml" else zin2.read(item.filename)
                zout.writestr(item, data)

    tmp_path.replace(DOCX_PATH)


if __name__ == "__main__":
    main()
