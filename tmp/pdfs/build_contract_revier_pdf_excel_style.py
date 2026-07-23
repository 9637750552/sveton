from __future__ import annotations

import html
import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(r"C:\Users\alvad\Documents\Sveton")
SOURCE = ROOT / "01_docs" / "operations" / "contracts" / "Contract_revier.md"
OUTPUT = ROOT / "01_docs" / "operations" / "contracts" / "Contract_revier.pdf"
PARTS = ROOT / "tmp" / "pdfs" / "contract_revier_excel_style_parts"
APPENDIX5_EXCEL_PDF = ROOT / "tmp" / "pdfs" / "excel_appendix5_nextcloud" / "appendix5_excel_with_header.pdf"

DARK = colors.HexColor("#244062")
DARK2 = colors.HexColor("#1F4E78")
BLUE = colors.HexColor("#2F75B5")
MID = colors.HexColor("#5B9BD5")
LIGHT = colors.HexColor("#D9EAF7")
GRID = colors.HexColor("#B7CDE3")
TEXT = colors.HexColor("#111111")


def register_fonts() -> None:
    fonts = Path(r"C:\Windows\Fonts")
    pdfmetrics.registerFont(TTFont("DocRegular", str(fonts / "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("DocBold", str(fonts / "segoeuib.ttf")))
    pdfmetrics.registerFont(TTFont("DocItalic", str(fonts / "segoeuii.ttf")))


def make_styles():
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=9.4,
            leading=12.0,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        "center": ParagraphStyle(
            "center",
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
            leading=11.2,
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
            textColor=colors.HexColor("#17365D"),
            spaceBefore=7,
            spaceAfter=4,
        ),
        "band": ParagraphStyle(
            "band",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=14,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
        "xl_title": ParagraphStyle(
            "xl_title",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=13,
            leading=15,
            alignment=TA_CENTER,
            textColor=DARK,
            spaceAfter=5,
        ),
        "xl_subtitle": ParagraphStyle(
            "xl_subtitle",
            parent=base["Normal"],
            fontName="DocItalic",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#666666"),
            spaceAfter=6,
        ),
        "section_dark": ParagraphStyle(
            "section_dark",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=9.5,
            leading=11,
            textColor=colors.white,
        ),
        "section_light": ParagraphStyle(
            "section_light",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=8.5,
            leading=10,
            textColor=TEXT,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=7.8,
            leading=9.4,
            textColor=TEXT,
        ),
        "cell_center": ParagraphStyle(
            "cell_center",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=8,
            leading=9,
            alignment=TA_CENTER,
            textColor=TEXT,
        ),
        "cell_bold": ParagraphStyle(
            "cell_bold",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=7.8,
            leading=9.3,
            textColor=TEXT,
        ),
        "cell_head": ParagraphStyle(
            "cell_head",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=7.8,
            leading=9.3,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName="DocRegular",
            fontSize=7.1,
            leading=8.5,
            textColor=TEXT,
        ),
        "small_bold": ParagraphStyle(
            "small_bold",
            parent=base["Normal"],
            fontName="DocBold",
            fontSize=7.1,
            leading=8.5,
            textColor=TEXT,
        ),
    }


def esc(text: str | None) -> str:
    if text is None:
        return ""
    value = str(text)
    value = value.replace(r"\_", "_").replace(r"\#", "#").replace(r"\|", "|").replace("☐", "□")
    return html.escape(value)


def rich(text: str) -> str:
    parts = re.split(r"(\*\*.*?\*\*)", text)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append(f"<b>{esc(part[2:-2])}</b>")
        else:
            out.append(esc(part))
    return "".join(out)


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(rich(text), style)


def xl_p(text: str | None, style: ParagraphStyle) -> Paragraph:
    return Paragraph(esc(text), style)


def section_band(text: str, width: float, styles, *, dark: bool = True) -> Table:
    style = styles["section_dark"] if dark else styles["section_light"]
    fill = MID if dark else LIGHT
    table = Table([[xl_p(text, style)]], colWidths=[width])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.35, GRID),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def table(data, widths, styles, *, header_rows: int = 1, font_size: str = "cell", row_heights=None) -> Table:
    rows = []
    for r, row in enumerate(data):
        cells = []
        for c, value in enumerate(row):
            if r < header_rows:
                style = styles["cell_head"]
            elif value == "□" or value == "":
                style = styles["cell_center"] if value == "□" else styles[font_size]
            else:
                style = styles[font_size]
            cells.append(xl_p(value, style))
        rows.append(cells)
    t = Table(rows, colWidths=widths, rowHeights=row_heights, repeatRows=header_rows)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    if header_rows:
        commands.append(("BACKGROUND", (0, 0), (-1, header_rows - 1), BLUE))
    t.setStyle(TableStyle(commands))
    return t


def light_table(data, widths, styles, *, row_heights=None) -> Table:
    t = Table([[xl_p(cell, styles["small"]) for cell in row] for row in data], colWidths=widths, rowHeights=row_heights)
    t.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, GRID),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return t


def title_block(app_no: str, title: str, width: float, styles, *, subtitle: str | None = None):
    story = []
    band = Table([[xl_p(app_no, styles["band"])]], colWidths=[width], rowHeights=[8 * mm])
    band.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), DARK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(band)
    story.append(Spacer(1, 4))
    story.append(xl_p(title, styles["xl_title"]))
    if subtitle:
        story.append(xl_p(subtitle, styles["xl_subtitle"]))
    return story


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


def generic_table(raw_rows: list[str], width: float, styles) -> Table | None:
    rows = [split_table_row(row) for row in raw_rows if not is_table_separator(row)]
    if not rows:
        return None
    max_cols = max(len(row) for row in rows)
    for row in rows:
        row.extend([""] * (max_cols - len(row)))
    return table(rows, [width / max_cols] * max_cols, styles, header_rows=1)


def blank_box(width: float, height: float) -> Table:
    t = Table([[""]], colWidths=[width], rowHeights=[height])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, GRID), ("BACKGROUND", (0, 0), (-1, -1), colors.white)]))
    return t


def combine_city_date_lines(lines: list[str]) -> list[str]:
    combined: list[str] = []
    i = 0
    while i < len(lines):
        current = lines[i].strip()
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if current.startswith("г. ") and nxt.startswith('"'):
            combined.append(f"{current}    {nxt}")
            i += 2
            continue
        combined.append(lines[i])
        i += 1
    return combined


def appendix_1_signature_block(width: float, styles):
    rows = [["Заказчик: __________________ /________________/", "Исполнитель: __________________ /________________/"]]
    block = light_table(rows, [width / 2, width / 2], styles, row_heights=[9 * mm])
    block.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return [
        Spacer(1, 10),
        p("Подписи Сторон:", styles["h2"]),
        block,
    ]


def generic_flowables(lines: list[str], width: float, styles):
    story = []
    table_buffer: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush():
        nonlocal table_buffer
        if table_buffer:
            t = generic_table(table_buffer, width, styles)
            if t is not None:
                story.append(t)
                story.append(Spacer(1, 5))
            table_buffer = []

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                story.append(blank_box(width, 30 * mm) if not any(x.strip() for x in code_lines) else p("<br/>".join(code_lines), styles["small"]))
                story.append(Spacer(1, 6))
                code_lines = []
                in_code = False
            else:
                flush()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if stripped.startswith("|"):
            table_buffer.append(line)
            continue
        flush()
        if not stripped:
            continue
        if stripped == "---":
            story.append(Spacer(1, 6))
            continue
        if stripped.startswith(r"\# "):
            story.append(p(stripped[3:].strip(), styles["h1"]))
            continue
        if stripped.startswith("# "):
            text = stripped[2:].strip()
            if text.startswith("Приложение N "):
                story.append(PageBreak())
            story.append(p(text, styles["h1"]))
            continue
        if stripped.startswith("## "):
            story.append(p(stripped[3:].strip(), styles["h2"]))
            continue
        if stripped.startswith("- "):
            story.append(p("- " + stripped[2:].strip(), styles["bullet"]))
            continue
        style = styles["center"] if stripped.startswith("г. ") or stripped.startswith('"') or stripped.startswith("к договору") else styles["body"]
        story.append(p(stripped, style))
    flush()
    return story


def build_simple_pdf(path: Path, pagesize, flowables) -> None:
    doc = SimpleDocTemplate(
        str(path),
        pagesize=pagesize,
        leftMargin=11 * mm,
        rightMargin=11 * mm,
        topMargin=9 * mm,
        bottomMargin=10 * mm,
        title="Contract_revier",
        author="Sveton",
    )
    doc.build(flowables)


def appendix_2(styles):
    width = A4[0] - 22 * mm
    story = title_block("Приложение N 2", "Заявка на осмотр объекта", width, styles, subtitle='к договору N ____ от "___" ____________ 20__ г.')
    story.append(section_band("1. Данные по заявке", width, styles))
    fields = [
        ["Поле", "Значение"],
        ["Заказчик / ответственное лицо Светон", ""],
        ["Клиент - Ф.И.О. или наименование организации", ""],
        ["Контакты клиента", ""],
        ["Адрес объекта", ""],
        ["Срок исполнения заявки", ""],
        ["Стоимость выезда / услуг Исполнителя", ""],
    ]
    story.append(table(fields, [50 * mm, width - 50 * mm], styles, row_heights=[5.5 * mm] + [9.2 * mm] * 6))
    story.append(Spacer(1, 4))
    story.append(section_band("2. Что передано исполнителю", width, styles))
    materials = [
        ["Отметка", "Материал", "Комментарий"],
        ["□", "Фото щита от клиента", ""],
        ["□", "Фото места установки ИБП от клиента", ""],
        ["□", "Фото предполагаемой трассы от клиента", ""],
        ["□", "Схема / план помещений от клиента", ""],
        ["□", "Электрическая схема энергоснабжения объекта от клиента", ""],
        ["□", "Предварительный список нагрузок, устанавливаемых в резерв", ""],
        ["□", "Особые условия объекта от клиента", ""],
        ["□", "Иное", ""],
    ]
    story.append(table(materials, [30 * mm, 80 * mm, width - 110 * mm], styles, row_heights=[5.5 * mm] + [6.6 * mm] * 8))
    story.append(Spacer(1, 4))
    story.append(section_band("3. Что нужно проверить/измерить", width, styles))
    checks = [
        ["Отметка", "Проверка", "Комментарий"],
        ["□", "3.1. Проверить состояние электросети.", ""],
        ["□", "3.2. Проверить возможность установки ИБП, инвертора и АКБ.", ""],
        ["□", "3.3. Проверить состояние щита клиента.", ""],
        ["□", "3.4. Определить состав и мощности нагрузок, устанавливаемых в резерв.", ""],
        ["□", "3.5. Определить автоматы резервной группы.", ""],
        ["□", "3.6. Проверить возможность прокладки кабельной трассы.", ""],
    ]
    story.append(table(checks, [30 * mm, 80 * mm, width - 110 * mm], styles, row_heights=[5.5 * mm] + [6.6 * mm] * 6))
    story.append(Spacer(1, 12))
    story.append(light_table([["Исполнитель / монтажник", "", "Подпись", ""], ["Ответственное лицо Светон", "", "Подпись", ""], ["Дата", "", "", ""]], [50 * mm, 95 * mm, 25 * mm, width - 170 * mm], styles, row_heights=[8 * mm] * 3))
    return story


def appendix_3(styles):
    page = landscape(A4)
    width = page[0] - 22 * mm
    story = title_block("Отчет об осмотре", "", width, styles, subtitle='Приложение N 3 к договору N ____ от "___" ____________ 20__ г.')
    story.append(section_band("1. Данные отчета", width, styles, dark=False))
    story.append(light_table(
        [
            ["Дата осмотра", "", "Исполнитель", ""],
            ["Объект / адрес объекта", "", "Дата отправки отчета Заказчику", ""],
            ["□", "Заявка на подбор оборудования заполнена и подписана Клиентом", "□ да / □ нет / □ клиент отказался / □ подпись невозможно получить", ""],
            ["□", "Чек-лист осмотра места монтажа ИБП приложен", "□ да / □ нет / □ не требуется", ""],
            ["□", "Фотоотчет приложен", "□ да / □ нет / □ не требуется", ""],
        ],
        [22 * mm, 90 * mm, 74 * mm, width - 186 * mm],
        styles,
        row_heights=[6 * mm, 6.5 * mm, 5.5 * mm, 5.5 * mm, 5.5 * mm],
    ))
    story.append(Spacer(1, 5))
    story.append(section_band("2. Раскладка автоматов по щитам", width, styles, dark=False))
    story.append(xl_p("Перечислить по каждому щиту только автоматы резервной группы. Нумерация: слева направо и сверху вниз; первый автомат - верхний левый, последний - нижний правый.", styles["small"]))
    breaker = [["Щит / место", "N", "Что фактически питает", "УЗО/диф", "Фаза", "Комментарий"]] + [["", "", "", "", "", ""] for _ in range(10)]
    story.append(table(breaker, [30 * mm, 14 * mm, 86 * mm, 25 * mm, 22 * mm, width - 177 * mm], styles, row_heights=[5.4 * mm] + [4.8 * mm] * 10))
    story.append(xl_p("Если автоматов больше, чем строк в таблице, зарисовать схему щита вручную и приложить фото схемы.", styles["small"]))
    story.append(Spacer(1, 4))
    story.append(section_band("3. Непроверенные или спорные вопросы", width, styles, dark=False))
    dispute_rows = [
        ["", "Вопрос / ограничение", "Описание"],
        ["□", "Что не удалось проверить на объекте", ""],
        ["□", "Выявлены ограничения по месту установки ИБП", ""],
        ["□", "Выявлены ограничения по прокладке кабельной трассы", ""],
        ["□", "Есть опасные или непонятные места в щитах", ""],
        ["□", "Есть сложности с выделением резервных автоматов", ""],
        ["□", "Есть расхождения с данными из Заявки", ""],
        ["□", "Дальнейшие работы невозможны без уточнений", ""],
        ["□", "Требуется решение Заказчика для продолжения", ""],
    ]
    story.append(table(dispute_rows, [24 * mm, 90 * mm, width - 114 * mm], styles, row_heights=[5.2 * mm] + [4.8 * mm] * 8))
    story.append(xl_p("Исполнитель подтверждает, что отчет заполнен по результатам осмотра Объекта и содержит сведения, материалы, ограничения и выводы в пределах фактически выполненных действий.", styles["small"]))
    story.append(Spacer(1, 8))
    story.append(light_table([['Исполнитель: __________________ /________________/ "__" ____________ 20__ г.', 'Ответственное лицо Заказчика: __________________ /________________/ "__" ____________ 20__ г.']], [width / 2, width / 2], styles))
    return story


def appendix_4(styles):
    page = landscape(A4)
    width = page[0] - 22 * mm
    story = title_block("Приложение N 4", "Чек-лист осмотра места монтажа ИБП", width, styles)
    left_sections = [
        ("1. До начала осмотра", ["Разместить термометр в предполагаемом месте установки АКБ.", "Уточнить у Клиента, какие помещения, щиты и трассы можно фотографировать."]),
        ("2. Щит и электросеть", ['Фото открытого щита "на столбе".', "Фото основного щита до снятия защитной крышки.", "Фото списка потребителей, если он прилагается к щиту.", "Снять защитную крышку щита.", "Фото открытого щита полностью.", "Фото щита и номиналов каждого ряда со всех сторон.", "Проверить РЕ/N шины.", "Измерить напряжение на каждой фазе.", "Установить соответствие автоматов и нагрузок, планируемых в резерв.", "Заполнить в Отчете информацию по автоматам и нагрузкам из резервной группы.", "Проверить наличие дополнительных щитов."]),
        ("3. Потребители и оборудование", ["Измерить или уточнить номинальную и пиковую мощность погружного насоса или другого оборудования.", "Фото шильдиков циркуляционных насосов и другого резервируемого оборудования.", "Проверить, все ли заявленные потребители установлены фактически.", "Отметить в Отчете все спорные или непонятные нагрузки."]),
    ]
    right_sections = [
        ("5. Обязательно проверить", ["Проверить наличие газового отсекателя для газового котла.", "Уточнить у Клиента, есть ли трехфазные нагрузки.", "Проверить, нет ли радиатора отопления рядом с местом установки ИБП.", "Уточнить состав и толщину стены, если потребуются проходы."]),
        ("6. Заявка на подбор оборудования", ["Заполнить Заявку на подбор оборудования.", "Организовать подписание Заявки на подбор оборудования у Клиента либо зафиксировать отказ/невозможность получения подписи."]),
        ("7. Материалы для отправки Заказчику", ["Фото или скан подписанной заявки на подбор оборудования либо фиксация отказа/невозможности получения подписи.", "Полностью заполненный Отчет об осмотре.", "Настоящий заполненный чек-лист.", "Скриншот координат Объекта.", "Фотоотчет."]),
        ("8. Завершение", ["Проверено, что все действия по чек-листу выполнены или отмечены как невыполнимые.", "В Отчете об осмотре указано, что не удалось проверить и почему.", "Комплект материалов передан Заказчику."]),
        ("4. Место установки ИБП и трасса", ["Сфотографировать место установки ИБП, инвертора или АКБ по кругу.", "Записать размеры помещения, если это нужно для монтажа.", "Осмотреть предполагаемую трассу кабеля.", "Фото трассы на всем протяжении.", "Фото мест проходов через стены или перекрытия."]),
    ]
    right_sections.sort(key=lambda section: int(section[0].split(".", 1)[0]))
    rows = []
    max_rows = max(sum(len(items) + 1 for _, items in left_sections), sum(len(items) + 1 for _, items in right_sections))
    left_flat = []
    right_flat = []
    for title, items in left_sections:
        left_flat.append(("section", title))
        left_flat.extend(("item", item) for item in items)
    for title, items in right_sections:
        right_flat.append(("section", title))
        right_flat.extend(("item", item) for item in items)
    for i in range(max_rows):
        l = left_flat[i] if i < len(left_flat) else ("blank", "")
        r = right_flat[i] if i < len(right_flat) else ("blank", "")
        left_mark = "□" if l[0] == "item" else (l[1] if l[0] == "section" else "")
        left_text = l[1] if l[0] == "item" else ""
        right_mark = "□" if r[0] == "item" else (r[1] if r[0] == "section" else "")
        right_text = r[1] if r[0] == "item" else ""
        rows.append([left_mark, left_text, right_mark, right_text])
    t = light_table(rows, [18 * mm, (width / 2) - 18 * mm, 18 * mm, (width / 2) - 18 * mm], styles, row_heights=[5.4 * mm] * len(rows))
    commands = []
    for idx, (l, r) in enumerate(zip(left_flat + [("blank", "")] * max_rows, right_flat + [("blank", "")] * max_rows)):
        if idx >= len(rows):
            break
        if l[0] == "section":
            commands += [("BACKGROUND", (0, idx), (1, idx), LIGHT), ("FONTNAME", (0, idx), (1, idx), "DocBold"), ("SPAN", (0, idx), (1, idx))]
        if r[0] == "section":
            commands += [("BACKGROUND", (2, idx), (3, idx), LIGHT), ("FONTNAME", (2, idx), (3, idx), "DocBold"), ("SPAN", (2, idx), (3, idx))]
    t.setStyle(TableStyle(commands))
    story.append(t)
    story.append(Spacer(1, 4))
    story.append(light_table([["Что не удалось выполнить по чек-листу и почему:", ""], ['Исполнитель: __________________ /________________/ "__" ____________ 20__ г.', 'Ответственное лицо Заказчика: __________________ /________________/ "__" ____________ 20__ г.']], [width / 2, width / 2], styles, row_heights=[7 * mm, 7 * mm]))
    return story


def small_choice_table(title, rows, width, styles):
    data = [[title, ""]] + [[item, "□"] for item in rows]
    t = light_table(data, [width - 9 * mm, 9 * mm], styles, row_heights=[4.1 * mm] * len(data))
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, 0), "DocBold"), ("ALIGN", (1, 1), (1, -1), "CENTER")]))
    return t


def appendix_5(styles):
    page = landscape(A4)
    width = page[0] - 22 * mm
    story = title_block("Приложение N 5", "Заявка на подбор оборудования", width, styles, subtitle='к договору N ____ от "___" ____________ 20__ г.')
    story.append(light_table([["Контрагент", ""], ["Адрес", ""]], [36 * mm, width - 36 * mm], styles, row_heights=[6 * mm, 6 * mm]))
    story.append(Spacer(1, 2))
    block_w = (width - 8 * mm) / 3
    blocks = Table(
        [[
            small_choice_table("Типы нагрузки", ["Освещение", "Котел", "Насосы", "Бытовые приборы"], block_w, styles),
            small_choice_table("Требуется", ["Установка ИБП", "Установка АСЭС", "Установка стабилизатора"], block_w, styles),
            small_choice_table("Условия установки", ["Ведется строительство", "Помещение готово", "Помещение теплое", "Часть потребителей не установлены", "Все потребители установлены"], block_w, styles),
        ]],
        colWidths=[block_w, block_w, block_w],
    )
    blocks.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story.append(blocks)
    story.append(Spacer(1, 2))
    story.append(light_table([["Тип объекта", "Частный дом □", "Предприятие □", "Офис □"]], [35 * mm, 55 * mm, 55 * mm, width - 145 * mm], styles, row_heights=[4.5 * mm]))
    story.append(Spacer(1, 2))
    left_w = width * 0.58
    right_w = width - left_w - 5 * mm
    reserve = [["Потребитель", "кВт", "ч"]] + [[name, "", ""] for name in ["Освещение", "Котел", "Насосы отопления", "Насос на воду", "Холодильник", "Септик", "Насос сброса", "Водоочистка", "Телевизор", "Компьютер", "Видеонаблюдение", "Иное"]]
    external = [["Проверка", "Значение / отметка"], ["Номинал вводного автомата в щите дома", "___ А"], ["Номинал автомата на вводе / столбе", "___ А"], ["Трехфазный ввод", "□ да / □ нет"], ["Однофазный ввод", "□ да / □ нет"], ["На шинах нуля и земли нет напряжения", "□ да / □ нет / □ не проверялось"], ["На планке заземления нет напряжения", "□ да / □ нет / □ не проверялось"]]
    combined = Table(
        [[
            table(reserve, [left_w * 0.52, left_w * 0.22, left_w * 0.26], styles, row_heights=[3.85 * mm] * len(reserve)),
            table(external, [right_w * 0.58, right_w * 0.42], styles, row_heights=[3.85 * mm] * len(external)),
        ]],
        colWidths=[left_w, right_w],
    )
    combined.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story.append(section_band("4. Потребители, устанавливаемые в резерв / 5. Анализ внешней сети", width, styles, dark=False))
    story.append(combined)
    story.append(Spacer(1, 2))
    story.append(section_band("6. Комментарий", width, styles, dark=False))
    story.append(light_table([["Комментарий Исполнителя: ____________________________________________________________________________________"], ["____________________________________________________________________________________________________________"]], [width], styles, row_heights=[4.0 * mm] * 2))
    story.append(Spacer(1, 1))
    story.append(section_band("7. Особенности и ограничения", width, styles, dark=False))
    story.append(table([["Условие", "Значение / комментарий"], ["Трехфазное подключение в резерве", ""], ["Общая мощность приборов не превышает", "___ кВт"], ["При превышении мощности резервной группы более", "___ кВт"], ["Температура в помещении не превышает", "28 °C"], ["Температура в помещении не опускается ниже", "5 °C"]], [width * 0.5, width * 0.5], styles, row_heights=[4.0 * mm] * 6))
    story.append(Spacer(1, 1))
    story.append(section_band("8. Подтверждение", width, styles, dark=False))
    story.append(xl_p("Исполнитель подтверждает, что настоящая Заявка заполнена по результатам осмотра Объекта и предназначена для подбора оборудования Заказчиком.", styles["small"]))
    story.append(light_table([['Исполнитель: __________________ /________________/ "__" ____________ 20__ г.', 'Клиент: __________________ /________________/ "__" ____________ 20__ г.', 'Ответственное лицо Заказчика: __________________ /________________/ "__" ____________ 20__ г.']], [width / 3, width / 3, width / 3], styles, row_heights=[6 * mm]))
    return story


def add_page_numbers(input_pdf: Path, output_pdf: Path, skip_from_page: int | None = None) -> None:
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages, start=1):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        if skip_from_page is None or i < skip_from_page:
            overlay_path = PARTS / f"num_{i}.pdf"
            c = canvas.Canvas(str(overlay_path), pagesize=(w, h))
            c.setFont("DocRegular", 8)
            c.setFillColor(colors.HexColor("#666666"))
            c.drawRightString(w - 10 * mm, 7 * mm, str(i))
            c.save()
            overlay = PdfReader(str(overlay_path)).pages[0]
            page.merge_page(overlay)
        writer.add_page(page)
    with output_pdf.open("wb") as f:
        writer.write(f)


def build() -> None:
    register_fonts()
    styles = make_styles()
    PARTS.mkdir(parents=True, exist_ok=True)
    for old in PARTS.glob("*.pdf"):
        old.unlink()

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    contract_index = next(i for i, line in enumerate(lines) if line.strip() == "# ДОГОВОР N \\__\\_")
    app2_index = next(i for i, line in enumerate(lines) if line.strip() == "# Приложение N 2")
    main_lines = combine_city_date_lines(lines[contract_index:app2_index])

    parts = []
    main_pdf = PARTS / "01_main_app1.pdf"
    main_width = A4[0] - 22 * mm
    main_story = generic_flowables(main_lines, main_width, styles)
    build_simple_pdf(main_pdf, A4, main_story)
    parts.append(main_pdf)

    builders = [
        ("02_appendix_2.pdf", A4, appendix_2(styles)),
        ("03_appendix_3.pdf", landscape(A4), appendix_3(styles)),
        ("04_appendix_4.pdf", landscape(A4), appendix_4(styles)),
    ]
    for name, page_size, story in builders:
        part = PARTS / name
        build_simple_pdf(part, page_size, story)
        parts.append(part)

    if not APPENDIX5_EXCEL_PDF.exists():
        raise FileNotFoundError(f"Excel-rendered Appendix 5 is missing: {APPENDIX5_EXCEL_PDF}")
    appendix5_start_page = sum(len(PdfReader(str(part)).pages) for part in parts) + 1
    parts.append(APPENDIX5_EXCEL_PDF)

    merged = PARTS / "merged_no_numbers.pdf"
    writer = PdfWriter()
    for part in parts:
        for page in PdfReader(str(part)).pages:
            writer.add_page(page)
    with merged.open("wb") as f:
        writer.write(f)
    add_page_numbers(merged, OUTPUT, skip_from_page=appendix5_start_page)
    print(OUTPUT)


if __name__ == "__main__":
    build()
