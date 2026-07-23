import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile
import xml.etree.ElementTree as ET


WORKBOOK_PATH = Path(
    os.environ.get(
        "CONTRACT_WORKBOOK_PATH",
        r"C:\Users\alvad\Documents\Sveton\01_docs\operations\contracts\appendix_2_object_inspection_request.xlsx",
    )
)

SHEET_SETTINGS = {
    "Заявка": {
        "print_area": "'Заявка'!$A$1:$E$39",
        "orientation": "portrait",
        "fit_to_width": "1",
        "fit_to_height": "1",
    },
    "Отчет": {
        "print_area": "'Отчет'!$A$1:$J$44",
        "orientation": "landscape",
        "fit_to_width": "1",
        "fit_to_height": "1",
    },
    "Чек-лист": {
        "print_area": "'Чек-лист'!$A$1:$J$39",
        "orientation": "landscape",
        "fit_to_width": "1",
        "fit_to_height": "1",
    },
    "Подбор оборудования": {
        "print_area": "'Подбор оборудования'!$B$1:$AO$54",
        "orientation": "landscape",
        "fit_to_width": "1",
        "fit_to_height": "1",
    },
    "Чек-лист книжный": {
        "print_area": "'Чек-лист книжный'!$A$1:$D$63",
        "orientation": "portrait",
        "fit_to_width": "1",
        "fit_to_height": "0",
    },
}

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PACKAGE_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
PRINTER_SETTINGS_REL = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/printerSettings"
)

ET.register_namespace("", NS_MAIN)
ET.register_namespace("r", NS_REL)


def q(name: str) -> str:
    return f"{{{NS_MAIN}}}{name}"


def relq(name: str) -> str:
    return f"{{{NS_REL}}}{name}"


def worksheet_path_from_target(target: str) -> str:
    target = target.replace("\\", "/").lstrip("/")
    if target.startswith("xl/"):
        return target
    return f"xl/{target}".replace("xl/../", "")


def sheet_map(zip_in: ZipFile) -> dict[str, tuple[int, str]]:
    workbook_root = ET.fromstring(zip_in.read("xl/workbook.xml"))
    rels_root = ET.fromstring(zip_in.read("xl/_rels/workbook.xml.rels"))
    rel_targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels_root.findall(f"{{{NS_PACKAGE_REL}}}Relationship")
    }
    sheets = workbook_root.find(q("sheets"))
    if sheets is None:
        raise RuntimeError("Workbook has no sheets collection")

    result = {}
    for index, sheet in enumerate(sheets.findall(q("sheet"))):
        rel_id = sheet.attrib[relq("id")]
        result[sheet.attrib["name"]] = (index, worksheet_path_from_target(rel_targets[rel_id]))
    return result


def fix_sheet_xml(xml_bytes: bytes, settings: dict[str, str]) -> bytes:
    root = ET.fromstring(xml_bytes)

    sheet_pr = root.find(q("sheetPr"))
    if sheet_pr is None:
        sheet_pr = ET.Element(q("sheetPr"))
        root.insert(0, sheet_pr)

    page_setup_pr = sheet_pr.find(q("pageSetUpPr"))
    if page_setup_pr is None:
        page_setup_pr = ET.SubElement(sheet_pr, q("pageSetUpPr"))
    page_setup_pr.set("fitToPage", "1")

    for tag in ("printOptions", "pageMargins", "pageSetup"):
        for child in list(root.findall(q(tag))):
            root.remove(child)

    root.extend(
        [
            ET.Element(q("printOptions"), {"horizontalCentered": "1"}),
            ET.Element(
                q("pageMargins"),
                {
                    "left": "0.2",
                    "right": "0.2",
                    "top": "0.25",
                    "bottom": "0.25",
                    "header": "0.1",
                    "footer": "0.1",
                },
            ),
            ET.Element(
                q("pageSetup"),
                {
                    "paperSize": "9",
                    "orientation": settings["orientation"],
                    "fitToWidth": settings["fit_to_width"],
                    "fitToHeight": settings["fit_to_height"],
                },
            ),
        ]
    )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def fix_workbook_xml(xml_bytes: bytes, indexed_settings: dict[int, dict[str, str]]) -> bytes:
    root = ET.fromstring(xml_bytes)
    defined_names = root.find(q("definedNames"))
    if defined_names is None:
        defined_names = ET.Element(q("definedNames"))
        sheets = root.find(q("sheets"))
        insert_at = list(root).index(sheets) + 1 if sheets is not None else len(root)
        root.insert(insert_at, defined_names)

    target_ids = {str(index) for index in indexed_settings}
    for child in list(defined_names.findall(q("definedName"))):
        if child.attrib.get("name") == "_xlnm.Print_Area" and child.attrib.get("localSheetId") in target_ids:
            defined_names.remove(child)

    for index, settings in sorted(indexed_settings.items()):
        print_area = ET.Element(
            q("definedName"),
            {"name": "_xlnm.Print_Area", "localSheetId": str(index)},
        )
        print_area.text = settings["print_area"]
        defined_names.append(print_area)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def remove_printer_settings_content_type(xml_bytes: bytes) -> bytes:
    text = xml_bytes.decode("utf-8")
    text = re.sub(
        r"<Default\s+Extension=\"bin\"\s+ContentType=\"application/vnd\.openxmlformats-officedocument\.spreadsheetml\.printerSettings\"\s*/>",
        "",
        text,
    )
    return text.encode("utf-8")


def remove_printer_settings_rels(xml_bytes: bytes) -> bytes | None:
    root = ET.fromstring(xml_bytes)
    for child in list(root.findall(f"{{{NS_PACKAGE_REL}}}Relationship")):
        if child.attrib.get("Type") == PRINTER_SETTINGS_REL:
            root.remove(child)
    if not list(root):
        return None
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


with ZipFile(WORKBOOK_PATH, "r") as zip_in:
    sheets = sheet_map(zip_in)
    indexed_settings = {}
    replacements = {}

    for sheet_name, settings in SHEET_SETTINGS.items():
        if sheet_name not in sheets:
            raise RuntimeError(f"Sheet not found: {sheet_name}")
        index, sheet_path = sheets[sheet_name]
        indexed_settings[index] = settings
        replacements[sheet_path] = fix_sheet_xml(zip_in.read(sheet_path), settings)

    replacements["xl/workbook.xml"] = fix_workbook_xml(
        zip_in.read("xl/workbook.xml"),
        indexed_settings,
    )
    replacements["[Content_Types].xml"] = remove_printer_settings_content_type(
        zip_in.read("[Content_Types].xml")
    )
    rel_paths_to_remove = set()
    for item in zip_in.infolist():
        if item.filename.endswith(".rels") and item.filename.startswith("xl/worksheets/_rels/"):
            fixed_rels = remove_printer_settings_rels(zip_in.read(item.filename))
            if fixed_rels is None:
                rel_paths_to_remove.add(item.filename)
            else:
                replacements[item.filename] = fixed_rels

    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp_path = Path(tmp.name)

    with ZipFile(tmp_path, "w", ZIP_DEFLATED) as zip_out:
        for item in zip_in.infolist():
            if item.filename.startswith("xl/printerSettings/"):
                continue
            if item.filename in rel_paths_to_remove:
                continue
            data = replacements.get(item.filename)
            zip_out.writestr(item, data if data is not None else zip_in.read(item.filename))

tmp_path.replace(WORKBOOK_PATH)
for sheet_name, settings in SHEET_SETTINGS.items():
    print(f"{sheet_name}: {settings['print_area']}")
