#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

import semantic_project_config as project_config


FILE_DIM_RE = re.compile(r"(?P<width>\d+)\s*x\s*(?P<height>\d+)")

SOURCE_DEFAULTS = {
    "Правила_фотосъемки_монтажа_Чек_лист_ред1": {
        "source_file": "Правила_фотосъемки_монтажа_Чек_лист_ред1.docx",
        "topic": "photo_report",
        "image_type": "photo_example",
        "roles": "installer|hq_engineer",
        "status": "raw_extracted|ready_for_linking",
        "notes": "Photo examples for montage photo checklist.",
    },
    "ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1": {
        "source_file": "ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1.docx",
        "topic": "basic_knowledge",
        "image_type": "diagram",
        "roles": "installer|electrician",
        "status": "raw_extracted|ready_for_linking",
        "notes": "Basic explanatory visual.",
    },
    "ЭЛК_2_1_техн.карты_изделий.": {
        "source_file": "ЭЛК_2_1 техн.карты изделий..docx",
        "topic": "ups_components",
        "image_type": "diagram",
        "roles": "installer|electrician|hq_engineer",
        "status": "raw_extracted|needs_classification",
        "notes": "Technical cards and assembly visuals.",
    },
    "ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5": {
        "source_file": "ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5.docx",
        "topic": "ups_components",
        "image_type": "diagram",
        "roles": "installer|electrician",
        "status": "raw_extracted|needs_classification",
        "notes": "UPS component visuals.",
    },
    "ЭЛК_3_1процесс_монтажа": {
        "source_file": "ЭЛК_3_1процесс монтажа.pdf",
        "topic": "installation_process",
        "image_type": "pdf_page_render",
        "roles": "installer|electrician",
        "status": "raw_extracted|review_required",
        "notes": "Rendered PDF page. Needs page-level review before linking.",
    },
    "ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9": {
        "source_file": "ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx",
        "topic": "installation_process",
        "image_type": "diagram",
        "roles": "installer|electrician",
        "status": "raw_extracted|needs_classification",
        "notes": "Installation process visuals.",
    },
    "ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1": {
        "source_file": "ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1.docx",
        "topic": "distribution_boards",
        "image_type": "diagram",
        "roles": "installer|electrician",
        "status": "raw_extracted|needs_classification",
        "notes": "Distribution board element visuals.",
    },
    "ЭЛК_5_-_Переборка_щитов_1.0": {
        "source_file": "ЭЛК_5 - Переборка щитов_1.0.pdf",
        "topic": "distribution_boards",
        "image_type": "pdf_page_render",
        "roles": "installer|electrician|hq_engineer",
        "status": "raw_extracted|review_required",
        "notes": "Rendered PDF page. Needs page-level review before linking.",
    },
}


def parse_dimensions(image_path: Path) -> tuple[int, int]:
    result = subprocess.run(["file", str(image_path)], check=True, capture_output=True, text=True)
    matches = list(FILE_DIM_RE.finditer(result.stdout))
    if not matches:
        return 0, 0
    match = matches[-1]
    return int(match.group("width")), int(match.group("height"))


def split_source_and_suffix(filename: str) -> tuple[str, str]:
    if "__img_" in filename:
        base, suffix = filename.split("__img_", 1)
        return base, f"img_{suffix.rsplit('.', 1)[0]}"
    if "__page_" in filename:
        base, suffix = filename.split("__page_", 1)
        return base, f"page_{suffix.rsplit('.', 1)[0]}"
    return Path(filename).stem, "unknown"


def classify_entry(source_key: str, suffix_key: str, width: int, height: int) -> tuple[str, str, str]:
    defaults = SOURCE_DEFAULTS[source_key]
    image_type = defaults["image_type"]
    status = defaults["status"]
    caption = ""

    is_page_render = suffix_key.startswith("page_")
    if is_page_render:
        page_no = int(suffix_key.split("_", 1)[1])
        caption = f"Rendered PDF page {page_no}"
        return image_type, status, caption

    if width <= 140 or height <= 90:
        return "decorative_or_unclear", "raw_extracted|exclude_candidate|needs_classification", "Small icon or fragment"

    if height >= width * 2 and width < 700:
        return "decorative_or_unclear", "raw_extracted|exclude_candidate|needs_classification", "Tall cropped fragment"

    if source_key == "Правила_фотосъемки_монтажа_Чек_лист_ред1":
        return "photo_example", status, "Photo example for montage framing"
    if source_key == "ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1":
        return "diagram", status, "Battery connection scheme"
    if source_key in {
        "ЭЛК_2_1_техн.карты_изделий.",
        "ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5",
        "ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9",
        "ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1",
    }:
        return "diagram", status, "Technical visual pending detailed caption"

    return image_type, status, caption


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: build_image_inventory.py <project_root> [images_raw_dir] [inventory_csv] [config_path]", file=sys.stderr)
        return 1

    project_root = Path(argv[1]).resolve()
    config = project_config.load_project_config(project_root, argv[4] if len(argv) > 4 else None)
    images_raw_dir = project_root / (argv[2] if len(argv) > 2 else config["images_raw"])
    inventory_csv = project_root / (argv[3] if len(argv) > 3 else config["images_inventory"])

    if not images_raw_dir.is_dir():
        print(f"Images directory not found: {images_raw_dir}", file=sys.stderr)
        return 1

    rows: list[dict[str, str]] = []
    for idx, image_path in enumerate(sorted(images_raw_dir.iterdir()), start=1):
        if not image_path.is_file():
            continue
        source_key, suffix_key = split_source_and_suffix(image_path.name)
        defaults = SOURCE_DEFAULTS.get(source_key)
        if defaults is None:
            continue
        width, height = parse_dimensions(image_path)
        image_type, status, caption = classify_entry(source_key, suffix_key, width, height)
        rows.append(
            {
                "image_id": f"img_{idx:04d}",
                "file_name": image_path.name,
                "source_key": source_key,
                "source_file": defaults["source_file"],
                "topic": defaults["topic"],
                "image_type": image_type,
                "roles": defaults["roles"],
                "status": status,
                "width": str(width),
                "height": str(height),
                "caption": caption,
                "nearby_text": "",
                "notes": defaults["notes"],
            }
        )

    inventory_csv.parent.mkdir(parents=True, exist_ok=True)
    with inventory_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "image_id",
                "file_name",
                "source_key",
                "source_file",
                "topic",
                "image_type",
                "roles",
                "status",
                "width",
                "height",
                "caption",
                "nearby_text",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {inventory_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
