#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

import semantic_project_config as project_config


IMG_RE = re.compile(r"<img\b[^>]*\bsrc=\"media/image(?P<num>\d+)\.(?P<ext>[^\"]+)\"[^>]*>", re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
MARKDOWN_RE = re.compile(r"[*_`>]+")
SPACE_RE = re.compile(r"\s+")

TOPIC_TO_SECTION = {
    "photo_report": "photo_report",
    "basic_knowledge": "basic_knowledge",
    "ups_components": "ups_components",
    "installation_process": "installation_process",
    "distribution_boards": "distribution_boards",
}

GENERIC_CAPTIONS = {
    "",
    "Technical visual pending detailed caption",
    "Photo example for montage framing",
    "Battery connection scheme",
}


def clean_text(value: str) -> str:
    value = IMG_RE.sub(" ", value)
    value = HTML_TAG_RE.sub(" ", value)
    value = html.unescape(value)
    value = value.replace("\\-", "-").replace("\\>", ">").replace("\\[", "[").replace("\\]", "]")
    value = value.replace("|", " ")
    value = MARKDOWN_RE.sub("", value)
    value = SPACE_RE.sub(" ", value)
    return value.strip(" -\t\r\n")


def significant_line(value: str) -> bool:
    if not value:
        return False
    if set(value) <= {"-", ":"}:
        return False
    if value.lower() in {"см. изображение ниже", "смотрите изображение ниже"}:
        return False
    return len(value) >= 4


def short(value: str, limit: int = 700) -> str:
    value = SPACE_RE.sub(" ", value).strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def media_ref_from_filename(file_name: str) -> str:
    match = re.search(r"__img_(?P<num>\d+)\.(?P<ext>[^.]+)$", file_name)
    if match:
        return f"media/image{int(match.group('num'))}.{match.group('ext')}"
    match = re.search(r"__page_(?P<num>\d+)\.", file_name)
    if match:
        return f"page_{int(match.group('num')):03d}"
    return ""


def extracted_path(project_root: Path, config: dict[str, str], source_file: str) -> Path | None:
    extracted = project_config.config_path(project_root, config, "extracted_texts")
    stem = Path(source_file).stem
    for suffix in (".md", ".txt"):
        path = extracted / f"{stem}{suffix}"
        if path.exists():
            return path
    return None


def build_markdown_context(path: Path) -> dict[str, dict[str, str]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    contexts: dict[str, list[str]] = {}
    anchors: dict[str, str] = {}

    for idx, line in enumerate(lines):
        for match in IMG_RE.finditer(line):
            ref = f"media/image{int(match.group('num'))}.{match.group('ext')}"

            before: list[str] = []
            for prev in range(idx - 1, max(-1, idx - 18), -1):
                cleaned = clean_text(lines[prev])
                if significant_line(cleaned):
                    before.append(cleaned)
                if len(before) >= 3:
                    break

            after: list[str] = []
            for nxt in range(idx + 1, min(len(lines), idx + 24)):
                cleaned = clean_text(lines[nxt])
                if significant_line(cleaned):
                    after.append(cleaned)
                if len(after) >= 3:
                    break

            current = clean_text(line)
            parts = list(reversed(before))
            if significant_line(current):
                parts.append(current)
            parts.extend(after)
            snippet = short(" ".join(parts))
            if snippet:
                contexts.setdefault(ref, []).append(snippet)

            anchor = first_anchor(before, after, current)
            if anchor and ref not in anchors:
                anchors[ref] = short(anchor, 140)

    result: dict[str, dict[str, str]] = {}
    for ref, snippets in contexts.items():
        merged: list[str] = []
        seen = set()
        for snippet in snippets:
            if snippet in seen:
                continue
            seen.add(snippet)
            merged.append(snippet)
        result[ref] = {
            "nearby_text": short(" || ".join(merged), 900),
            "source_anchor": anchors.get(ref, ""),
        }
    return result


def first_anchor(before: list[str], after: list[str], current: str) -> str:
    candidates = list(before)
    if significant_line(current):
        candidates.append(current)
    candidates.extend(after[:1])

    for candidate in reversed(candidates):
        lower = candidate.lower()
        if "см. изображение" in lower or "смотрите изображение" in lower:
            continue
        if len(candidate) > 180:
            continue
        return candidate
    return ""


def linking_bucket(row: dict[str, str]) -> str:
    status = row.get("status", "")
    image_type = row.get("image_type", "")
    if "exclude_candidate" in status:
        return "exclude_candidate"
    if image_type == "pdf_page_render":
        return "manual_pdf_review"
    if "ready_for_linking" in status:
        return "ready_for_linking"
    if image_type in {"diagram", "photo_example"}:
        return "candidate_for_linking"
    return "needs_review"


def caption_for(row: dict[str, str]) -> str:
    caption = row.get("caption", "").strip()
    anchor = row.get("source_anchor", "").strip()
    image_type = row.get("image_type", "")

    if caption and caption not in GENERIC_CAPTIONS:
        return caption
    if anchor:
        return short(anchor, 180)
    if image_type == "pdf_page_render":
        return f"Rendered PDF page from {row['source_file']}"
    if image_type == "decorative_or_unclear":
        return "Small icon or unclear fragment"
    return caption or "Technical visual pending detailed caption"


def enrich_rows(project_root: Path, config: dict[str, str], rows: list[dict[str, str]]) -> list[dict[str, str]]:
    context_cache: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        source_file = row["source_file"]
        if source_file not in context_cache:
            path = extracted_path(project_root, config, source_file)
            context_cache[source_file] = build_markdown_context(path) if path and path.suffix == ".md" else {}

        media_ref = media_ref_from_filename(row["file_name"])
        row["media_ref"] = media_ref
        row["related_section"] = TOPIC_TO_SECTION.get(row["topic"], row["topic"])
        row["linking_bucket"] = linking_bucket(row)

        context = context_cache[source_file].get(media_ref, {})
        row["source_anchor"] = context.get("source_anchor", "")
        row["nearby_text"] = context.get("nearby_text", row.get("nearby_text", ""))

        if row["image_type"] == "pdf_page_render":
            row["source_anchor"] = Path(source_file).stem
            row["nearby_text"] = (
                "PDF page render. Page-level text is not reliably available in the extracted text; "
                "manual visual review is required before linking this image to statements."
            )

        row["caption"] = caption_for(row)

    return rows


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: enrich_image_inventory.py <project_root> [inventory_csv] [config_path]", file=sys.stderr)
        return 1

    project_root = Path(argv[1]).resolve()
    config = project_config.load_project_config(project_root, argv[3] if len(argv) > 3 else None)
    inventory_csv = project_root / (argv[2] if len(argv) > 2 else config["images_inventory"])

    with inventory_csv.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    rows = enrich_rows(project_root, config, rows)
    fieldnames = [
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
        "media_ref",
        "source_anchor",
        "caption",
        "nearby_text",
        "linking_bucket",
        "related_section",
        "notes",
    ]

    with inventory_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Enriched {len(rows)} image inventory rows in {inventory_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
