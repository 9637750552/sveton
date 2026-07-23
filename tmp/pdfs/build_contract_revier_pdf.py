from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\alvad\Documents\Sveton")
SOURCE = ROOT / "01_docs" / "operations" / "contracts" / "Contract_revier.md"
OUTPUT = ROOT / "01_docs" / "operations" / "contracts" / "Contract_revier.pdf"


PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 18 * mm
RIGHT_MARGIN = 16 * mm
TOP_MARGIN = 16 * mm
BOTTOM_MARGIN = 16 * mm
AVAILABLE_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN


def register_fonts() -> None:
    fonts = Path(r"C:\Windows\Fonts")
    pdfmetrics.registerFont(TTFont("DocRegular", str(fonts / "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("DocBold", str(fonts / "segoeuib.ttf")))


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=9.4,
            leading=12.0,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        "body_center": ParagraphStyle(
            "body_center",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=9.4,
            leading=12.0,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=9.1,
            leading=11.3,
            alignment=TA_LEFT,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="DocBold",
            fontSize=14,
            leading=17,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#17365D"),
            spaceBefore=8,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="DocBold",
            fontSize=11.3,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#17365D"),
            spaceBefore=7,
            spaceAfter=4,
        ),
        "table": ParagraphStyle(
            "table",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=7.8,
            leading=9.2,
            alignment=TA_LEFT,
        ),
        "table_head": ParagraphStyle(
            "table_head",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=7.8,
            leading=9.2,
            alignment=TA_LEFT,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=8.4,
            leading=10.2,
            alignment=TA_JUSTIFY,
            spaceAfter=3,
        ),
    }
    return styles


def unescape_markdown(text: str) -> str:
    text = text.replace(r"\_", "_")
    text = text.replace(r"\#", "#")
    text = text.replace(r"\|", "|")
    text = text.replace("☐", "□")
    return text


def rich_text(text: str) -> str:
    text = unescape_markdown(text)
    parts = re.split(r"(\*\*.*?\*\*)", text)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append(f"<b>{html.escape(part[2:-2])}</b>")
        else:
            out.append(html.escape(part))
    return "".join(out)


def is_table_separator(line: str) -> bool:
    stripped = line.strip().strip("|").strip()
    return bool(stripped) and all(ch in "-:| " for ch in stripped)


def split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def col_widths(col_count: int) -> list[float]:
    if col_count == 2:
        return [AVAILABLE_WIDTH * 0.5, AVAILABLE_WIDTH * 0.5]
    if col_count == 4:
        return [AVAILABLE_WIDTH * 0.28, AVAILABLE_WIDTH * 0.18, AVAILABLE_WIDTH * 0.20, AVAILABLE_WIDTH * 0.34]
    if col_count == 6:
        return [
            AVAILABLE_WIDTH * 0.14,
            AVAILABLE_WIDTH * 0.09,
            AVAILABLE_WIDTH * 0.34,
            AVAILABLE_WIDTH * 0.09,
            AVAILABLE_WIDTH * 0.08,
            AVAILABLE_WIDTH * 0.26,
        ]
    return [AVAILABLE_WIDTH / col_count] * col_count


def table_from_rows(raw_rows: list[str], styles) -> Table | None:
    rows = [split_table_row(row) for row in raw_rows if not is_table_separator(row)]
    if not rows:
        return None
    max_cols = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (max_cols - len(row)))

    data = []
    for row_index, row in enumerate(rows):
        style_name = "table_head" if row_index == 0 else "table"
        data.append([Paragraph(rich_text(cell), styles[style_name]) for cell in row])

    table = Table(data, colWidths=col_widths(max_cols), repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "DocRegular"),
                ("FONTNAME", (0, 0), (-1, 0), "DocBold"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F243E")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#6F8FAF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def blank_box(height: float = 34 * mm) -> Table:
    table = Table([[""]], colWidths=[AVAILABLE_WIDTH], rowHeights=[height])
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#6F8FAF")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ]
        )
    )
    return table


def page_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("DocRegular", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 9 * mm, str(canvas.getPageNumber()))
    canvas.restoreState()


def flush_table(story, table_buffer: list[str], styles) -> None:
    if not table_buffer:
        return
    table = table_from_rows(table_buffer, styles)
    if table is not None:
        story.append(table)
        story.append(Spacer(1, 5))


def build_pdf() -> None:
    register_fonts()
    styles = make_styles()

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []
    table_buffer: list[str] = []
    in_code = False
    code_lines: list[str] = []

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                if code_lines and any(item.strip() for item in code_lines):
                    code_text = "<br/>".join(html.escape(unescape_markdown(item)) for item in code_lines)
                    story.append(Paragraph(code_text, styles["small"]))
                else:
                    story.append(blank_box())
                story.append(Spacer(1, 6))
                code_lines = []
                in_code = False
            else:
                flush_table(story, table_buffer, styles)
                table_buffer.clear()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if stripped.startswith("|"):
            table_buffer.append(line)
            continue
        if table_buffer:
            flush_table(story, table_buffer, styles)
            table_buffer.clear()

        if not stripped:
            continue

        if stripped == "---":
            story.append(Spacer(1, 6))
            continue

        heading_line = stripped
        if heading_line.startswith(r"\# "):
            text = heading_line[3:].strip()
            story.append(Paragraph(rich_text(text), styles["h1"]))
            continue

        if heading_line.startswith("# "):
            text = heading_line[2:].strip()
            if text.startswith("Приложение N "):
                story.append(PageBreak())
            story.append(Paragraph(rich_text(text), styles["h1"]))
            continue

        if heading_line.startswith("## "):
            text = heading_line[3:].strip()
            story.append(Paragraph(rich_text(text), styles["h2"]))
            continue

        if stripped.startswith("- "):
            bullet_text = stripped[2:].strip()
            story.append(Paragraph("- " + rich_text(bullet_text), styles["bullet"]))
            continue

        paragraph_style = styles["body_center"] if (
            stripped.startswith("г. ") or stripped.startswith('"') or stripped.startswith("к договору")
        ) else styles["body"]
        story.append(Paragraph(rich_text(stripped), paragraph_style))

    if table_buffer:
        flush_table(story, table_buffer, styles)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="Contract_revier",
        author="Sveton",
    )
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
