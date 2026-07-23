from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile
import xml.etree.ElementTree as ET


WORKBOOK_PATH = Path(
    r"C:\Users\alvad\Documents\Sveton\01_docs\operations\contracts\appendix_2_object_inspection_request.xlsx"
)
SHEET_NAME = "Отчет"
PRINT_AREA = f"'{SHEET_NAME}'!$A$1:$J$44"

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PACKAGE_REL = "http://schemas.openxmlformats.org/package/2006/relationships"

ET.register_namespace("", NS_MAIN)
ET.register_namespace("r", NS_REL)


def q(name: str) -> str:
    return f"{{{NS_MAIN}}}{name}"


def relq(name: str) -> str:
    return f"{{{NS_REL}}}{name}"


def package_relq(name: str) -> str:
    return f"{{{NS_PACKAGE_REL}}}{name}"


def worksheet_path_from_target(target: str) -> str:
    target = target.replace("\\", "/")
    if target.startswith("/"):
        return target.lstrip("/")
    return f"xl/{target}".replace("xl/../", "")


def find_report_sheet(zip_in: ZipFile) -> tuple[int, str]:
    workbook_root = ET.fromstring(zip_in.read("xl/workbook.xml"))
    rels_root = ET.fromstring(zip_in.read("xl/_rels/workbook.xml.rels"))
    rel_targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels_root.findall(f"{{{NS_PACKAGE_REL}}}Relationship")
    }

    sheets = workbook_root.find(q("sheets"))
    if sheets is None:
        raise RuntimeError("Workbook has no sheets collection")

    for index, sheet in enumerate(sheets.findall(q("sheet"))):
        if sheet.attrib.get("name") == SHEET_NAME:
            rel_id = sheet.attrib[relq("id")]
            return index, worksheet_path_from_target(rel_targets[rel_id])

    raise RuntimeError(f"Sheet not found: {SHEET_NAME}")


def fix_sheet_xml(xml_bytes: bytes) -> bytes:
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

    print_options = ET.Element(q("printOptions"), {"horizontalCentered": "1"})
    page_margins = ET.Element(
        q("pageMargins"),
        {
            "left": "0.2",
            "right": "0.2",
            "top": "0.25",
            "bottom": "0.25",
            "header": "0.1",
            "footer": "0.1",
        },
    )
    page_setup = ET.Element(
        q("pageSetup"),
        {
            "paperSize": "9",
            "orientation": "landscape",
            "fitToWidth": "1",
            "fitToHeight": "1",
        },
    )
    root.extend([print_options, page_margins, page_setup])
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def fix_workbook_xml(xml_bytes: bytes, sheet_index: int) -> bytes:
    root = ET.fromstring(xml_bytes)
    local_sheet_id = str(sheet_index)

    defined_names = root.find(q("definedNames"))
    if defined_names is None:
        defined_names = ET.Element(q("definedNames"))
        sheets = root.find(q("sheets"))
        insert_at = list(root).index(sheets) + 1 if sheets is not None else len(root)
        root.insert(insert_at, defined_names)

    for child in list(defined_names.findall(q("definedName"))):
        if (
            child.attrib.get("name") == "_xlnm.Print_Area"
            and child.attrib.get("localSheetId") == local_sheet_id
        ):
            defined_names.remove(child)

    print_area = ET.Element(
        q("definedName"),
        {"name": "_xlnm.Print_Area", "localSheetId": local_sheet_id},
    )
    print_area.text = PRINT_AREA
    defined_names.append(print_area)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


with ZipFile(WORKBOOK_PATH, "r") as zip_in:
    sheet_index, report_sheet_path = find_report_sheet(zip_in)
    replacements = {
        report_sheet_path: fix_sheet_xml(zip_in.read(report_sheet_path)),
        "xl/workbook.xml": fix_workbook_xml(zip_in.read("xl/workbook.xml"), sheet_index),
    }

    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp_path = Path(tmp.name)

    with ZipFile(tmp_path, "w", ZIP_DEFLATED) as zip_out:
        for item in zip_in.infolist():
            data = replacements.get(item.filename)
            zip_out.writestr(item, data if data is not None else zip_in.read(item.filename))

tmp_path.replace(WORKBOOK_PATH)
print(f"updated:{WORKBOOK_PATH}")
print(f"sheet:{report_sheet_path}")
print(f"print_area:{PRINT_AREA}")
