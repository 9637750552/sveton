#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path
from zipfile import ZipFile
import subprocess
import re

import semantic_project_config as project_config


DOCX_MEDIA_PREFIX = "word/media/"
MEDIA_IMAGE_RE = re.compile(r"image(?P<num>\d+)$", re.IGNORECASE)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def sanitize_stem(path: Path) -> str:
    return path.stem.replace(" ", "_")


def extract_docx_images(input_file: Path, raw_dir: Path) -> int:
    extracted = 0
    source_stem = sanitize_stem(input_file)
    with ZipFile(input_file) as archive:
        for member in archive.infolist():
            if not member.filename.startswith(DOCX_MEDIA_PREFIX):
                continue
            if member.is_dir():
                continue
            suffix = Path(member.filename).suffix.lower()
            if suffix not in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".wmf", ".emf"}:
                continue
            media_stem = Path(member.filename).stem
            media_match = MEDIA_IMAGE_RE.match(media_stem)
            if media_match:
                image_number = int(media_match.group("num"))
            else:
                image_number = extracted + 1
            target = raw_dir / f"{source_stem}__img_{image_number:03d}{suffix}"
            with archive.open(member) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted += 1
    return extracted


def render_pdf_pages(input_file: Path, raw_dir: Path) -> int:
    source_stem = sanitize_stem(input_file)
    prefix = raw_dir / f"{source_stem}__page"
    command = [
        "gs",
        "-q",
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=png16m",
        "-r144",
        f"-sOutputFile={prefix}_%03d.png",
        str(input_file),
    ]
    subprocess.run(command, check=True)
    return len(list(raw_dir.glob(f"{source_stem}__page_*.png")))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: extract_source_images.py <project_root> [raw_dir] [image_raw_dir] [normalized_dir] [config_path]", file=sys.stderr)
        return 1

    project_root = Path(argv[1]).resolve()
    config = project_config.load_project_config(project_root, argv[5] if len(argv) > 5 else None)
    raw_input_dir = project_root / (argv[2] if len(argv) > 2 else config["raw_sources"])
    image_raw_dir = project_root / (argv[3] if len(argv) > 3 else config["images_raw"])
    image_normalized_dir = project_root / (argv[4] if len(argv) > 4 else config["images_normalized"])

    if not raw_input_dir.is_dir():
        print(f"Raw directory not found: {raw_input_dir}", file=sys.stderr)
        return 1

    ensure_dir(image_raw_dir)
    ensure_dir(image_normalized_dir)

    total_images = 0
    for input_file in sorted(raw_input_dir.iterdir()):
        if not input_file.is_file():
            continue
        suffix = input_file.suffix.lower()
        if suffix == ".docx":
            count = extract_docx_images(input_file, image_raw_dir)
            print(f"{input_file.name}: extracted {count} embedded images")
            total_images += count
        elif suffix == ".pdf":
            count = render_pdf_pages(input_file, image_raw_dir)
            print(f"{input_file.name}: rendered {count} pages")
            total_images += count

    print(f"Total visual artifacts: {total_images}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
