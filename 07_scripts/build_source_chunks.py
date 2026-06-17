#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


IMG_RE = re.compile(r"<img\b[^>]*\bsrc=\"(?P<src>media/image(?P<num>\d+)\.(?P<ext>[^\"]+))\"[^>]*>", re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
MAX_CHARS = 2200
OVERLAP_CHARS = 350


@dataclass
class SourceDocument:
    document_id: str
    source_file: str
    source_format: str
    document_type: str
    topic: str
    roles: str
    status: str
    extracted_path: Path


def clean_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        value = value[1:-1]
    return value.strip()


def split_markdown_table_row(line: str) -> list[str]:
    parts = [part.strip() for part in line.strip().strip("|").split("|")]
    return parts


def load_documents(project_root: Path) -> list[SourceDocument]:
    inventory_path = project_root / "00_input/documents/electricians_knowledge_base/inventory.md"
    extracted_dir = project_root / "00_input/documents/electricians_knowledge_base/extracted"

    docs: list[SourceDocument] = []
    for line in inventory_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = split_markdown_table_row(line)
        if len(cells) < 8 or not cells[0].strip().isdigit():
            continue
        number = int(cells[0])
        source_file = clean_cell(cells[1])
        stem = Path(source_file).stem
        extracted_path = extracted_dir / f"{stem}.md"
        if not extracted_path.exists():
            extracted_path = extracted_dir / f"{stem}.txt"
        if not extracted_path.exists():
            continue
        docs.append(
            SourceDocument(
                document_id=f"doc_{number:03d}",
                source_file=source_file,
                source_format=cells[2],
                document_type=cells[3],
                topic=cells[4],
                roles=cells[5],
                status=cells[6],
                extracted_path=extracted_path,
            )
        )
    return docs


def load_image_index(project_root: Path) -> dict[tuple[str, str], dict[str, str]]:
    inventory_csv = project_root / "00_input/documents/electricians_knowledge_base/images/inventory.csv"
    index: dict[tuple[str, str], dict[str, str]] = {}
    with inventory_csv.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            index[(row["source_file"], row["media_ref"])] = row
    return index


def markdown_heading(line: str) -> str | None:
    stripped = line.strip()
    if not stripped:
        return None
    if stripped.startswith("#"):
        return stripped.lstrip("#").strip()
    if stripped.startswith("|"):
        return None
    if IMG_RE.search(stripped):
        return None
    if stripped.startswith("**") and stripped.endswith("**") and len(stripped) <= 180:
        inner = stripped.strip("*").strip()
        if inner and not inner.startswith("-"):
            return inner
    if stripped.startswith("*") and stripped.endswith("*") and len(stripped) <= 160:
        return stripped.strip("*").strip()
    return None


def clean_text_for_length(text: str) -> str:
    text = HTML_TAG_RE.sub(" ", text)
    text = text.replace("\\-", "-").replace("\\[", "[").replace("\\]", "]")
    return SPACE_RE.sub(" ", text).strip()


def extract_media_refs(text: str) -> list[str]:
    refs: list[str] = []
    seen = set()
    for match in IMG_RE.finditer(text):
        ref = match.group("src")
        if ref in seen:
            continue
        seen.add(ref)
        refs.append(ref)
    return refs


def replace_images(text: str, source_file: str, image_index: dict[tuple[str, str], dict[str, str]]) -> str:
    def replacement(match: re.Match[str]) -> str:
        ref = match.group("src")
        row = image_index.get((source_file, ref))
        if not row:
            return f"[IMAGE:{ref}]"
        caption = row.get("caption", "").strip()
        bucket = row.get("linking_bucket", "").strip()
        image_id = row["image_id"]
        if caption:
            return f"[IMAGE:{image_id}|{ref}|{bucket}|{caption}]"
        return f"[IMAGE:{image_id}|{ref}|{bucket}]"

    return IMG_RE.sub(replacement, text)


def paragraph_blocks(text: str) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    section_path: list[str] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append(("\n".join(current).strip(), list(section_path)))
            current = []

    for line in text.splitlines():
        heading = markdown_heading(line)
        if heading:
            flush()
            if len(section_path) >= 3:
                section_path = section_path[:2]
            section_path.append(heading)
            current.append(line)
            continue
        if not line.strip():
            flush()
            continue
        current.append(line)
    flush()
    return [(block, path) for block, path in blocks if clean_text_for_length(block) or extract_media_refs(block)]


def line_blocks_for_pdf(text: str) -> list[tuple[str, list[str]]]:
    lines = [line.rstrip() for line in text.splitlines()]
    blocks: list[tuple[str, list[str]]] = []
    current: list[str] = []
    for line in lines:
        cleaned = clean_text_for_length(line)
        if cleaned:
            current.append(cleaned)
            if len(" ".join(current)) >= 600:
                blocks.append((" ".join(current), ["PDF text extraction"]))
                current = []
    if current:
        blocks.append((" ".join(current), ["PDF text extraction"]))
    return blocks


def merge_tiny_blocks(blocks: list[tuple[str, list[str]]]) -> list[tuple[str, list[str]]]:
    merged: list[tuple[str, list[str]]] = []
    for block, path in blocks:
        block_len = len(clean_text_for_length(block))
        has_image = bool(extract_media_refs(block))
        if merged and block_len < 120 and not has_image:
            prev_block, prev_path = merged[-1]
            if prev_path == path:
                merged[-1] = (f"{prev_block}\n\n{block}", prev_path)
                continue
        merged.append((block, path))

    result: list[tuple[str, list[str]]] = []
    idx = 0
    while idx < len(merged):
        block, path = merged[idx]
        block_len = len(clean_text_for_length(block))
        has_image = bool(extract_media_refs(block))
        if block_len < 120 and not has_image and idx + 1 < len(merged):
            next_block, next_path = merged[idx + 1]
            if next_path == path:
                result.append((f"{block}\n\n{next_block}", path))
                idx += 2
                continue
        result.append((block, path))
        idx += 1
    return result


def split_long_block(block: str, max_chars: int) -> list[str]:
    if len(block) <= max_chars:
        return [block]
    sentences = re.split(r"(?<=[.!?。])\s+", block)
    parts: list[str] = []
    current = ""
    for sentence in sentences:
        if not sentence:
            continue
        if len(current) + len(sentence) + 1 > max_chars and current:
            parts.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        parts.append(current.strip())
    return parts or [block]


def make_chunks_for_document(
    doc: SourceDocument,
    image_index: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, object]]:
    raw_text = doc.extracted_path.read_text(encoding="utf-8", errors="replace")
    blocks = line_blocks_for_pdf(raw_text) if doc.extracted_path.suffix == ".txt" else paragraph_blocks(raw_text)
    blocks = merge_tiny_blocks(blocks)

    expanded_blocks: list[tuple[str, list[str]]] = []
    for block, path in blocks:
        for part in split_long_block(block, MAX_CHARS):
            expanded_blocks.append((part, path))

    chunks: list[dict[str, object]] = []
    current_blocks: list[str] = []
    current_path: list[str] = []
    char_cursor = 0
    chunk_start = 0

    def flush() -> None:
        nonlocal current_blocks, current_path, chunk_start, char_cursor
        if not current_blocks:
            return
        raw_chunk_text = "\n\n".join(current_blocks).strip()
        media_refs = extract_media_refs(raw_chunk_text)
        related_image_ids: list[str] = []
        excluded_image_ids: list[str] = []
        review_image_ids: list[str] = []
        for ref in media_refs:
            row = image_index.get((doc.source_file, ref))
            if not row:
                continue
            bucket = row["linking_bucket"]
            if bucket == "exclude_candidate":
                excluded_image_ids.append(row["image_id"])
            elif bucket == "manual_pdf_review":
                review_image_ids.append(row["image_id"])
            else:
                related_image_ids.append(row["image_id"])

        chunk_text = replace_images(raw_chunk_text, doc.source_file, image_index)
        review_reasons: list[str] = []
        if "review_required" in doc.status:
            review_reasons.append("source_document_review_required")
        if review_image_ids:
            review_reasons.append("manual_image_review_required")
        if doc.extracted_path.suffix == ".txt":
            review_reasons.append("pdf_text_layout_review_required")

        chunks.append(
            {
                "chunk_id": "",
                "source_document_id": doc.document_id,
                "source_file": doc.source_file,
                "source_format": doc.source_format,
                "source_type": doc.document_type,
                "topic": doc.topic,
                "roles": [role.strip() for role in doc.roles.split(",")],
                "source_status": [status.strip() for status in doc.status.split(",")],
                "extracted_path": str(doc.extracted_path),
                "section_path": current_path or [Path(doc.source_file).stem],
                "page_start": None,
                "page_end": None,
                "text": chunk_text,
                "text_char_count": len(clean_text_for_length(chunk_text)),
                "media_refs": media_refs,
                "related_image_ids": related_image_ids,
                "excluded_image_ids": excluded_image_ids,
                "review_image_ids": review_image_ids,
                "previous_chunk_id": None,
                "next_chunk_id": None,
                "previous_context": "",
                "next_context": "",
                "overlap_group_id": "",
                "needs_review": bool(review_reasons),
                "review_reasons": review_reasons,
                "char_start_approx": chunk_start,
                "char_end_approx": chunk_start + len(raw_chunk_text),
            }
        )
        char_cursor = chunk_start + len(raw_chunk_text)
        chunk_start = char_cursor
        current_blocks = []
        current_path = []

    for block, path in expanded_blocks:
        block_len = len(clean_text_for_length(block))
        current_len = len(clean_text_for_length("\n\n".join(current_blocks)))
        path_changed = bool(current_path and path != current_path)
        if current_blocks and (current_len + block_len > MAX_CHARS or path_changed):
            flush()
        if not current_blocks:
            current_path = path
        current_blocks.append(block)

    flush()

    for idx, chunk in enumerate(chunks, start=1):
        chunk_id = f"{doc.document_id}_chunk_{idx:04d}"
        chunk["chunk_id"] = chunk_id
        chunk["overlap_group_id"] = f"{doc.document_id}_overlap_{idx:04d}"
    for idx, chunk in enumerate(chunks):
        if idx > 0:
            chunk["previous_chunk_id"] = chunks[idx - 1]["chunk_id"]
            chunk["previous_context"] = clean_text_for_length(str(chunks[idx - 1]["text"]))[-OVERLAP_CHARS:]
        if idx + 1 < len(chunks):
            chunk["next_chunk_id"] = chunks[idx + 1]["chunk_id"]
            chunk["next_context"] = clean_text_for_length(str(chunks[idx + 1]["text"]))[:OVERLAP_CHARS]
    return chunks


def write_outputs(project_root: Path, chunks: list[dict[str, object]]) -> None:
    chunks_dir = project_root / "00_input/documents/electricians_knowledge_base/chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = chunks_dir / "source_chunks.jsonl"
    summary_path = chunks_dir / "summary.md"

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    by_doc: dict[str, list[dict[str, object]]] = {}
    for chunk in chunks:
        by_doc.setdefault(str(chunk["source_file"]), []).append(chunk)

    all_related_image_ids = [image_id for chunk in chunks for image_id in chunk["related_image_ids"]]
    all_excluded_image_ids = [image_id for chunk in chunks for image_id in chunk["excluded_image_ids"]]
    all_review_image_ids = [image_id for chunk in chunks for image_id in chunk["review_image_ids"]]

    lines = [
        "# Инвентаризация чанков базы знаний электриков",
        "",
        "Дата создания: 2026-06-16",
        "",
        "## Назначение",
        "",
        "Этот файл фиксирует результат структурного разбиения извлеченных документов на чанки для semantic extraction.",
        "",
        "Основной машинный файл: `source_chunks.jsonl`.",
        "",
        "## Формат",
        "",
        "- `chunk_id`: стабильный идентификатор чанка;",
        "- `source_document_id`: идентификатор документа из корпуса;",
        "- `section_path`: ближайший путь раздела;",
        "- `text`: текст чанка с заменой картинок на маркеры `[IMAGE:...]`;",
        "- `media_refs`: исходные ссылки `media/imageN.ext`;",
        "- `related_image_ids`: картинки, которые можно передать в semantic extraction как визуальную опору;",
        "- `excluded_image_ids`: картинки, которые не надо автоматически связывать с утверждениями;",
        "- `review_image_ids`: картинки, требующие ручного просмотра;",
        "- `previous_chunk_id` / `next_chunk_id`: порядок внутри документа;",
        "- `previous_context` / `next_context`: overlap-контекст соседних чанков без дублирования основного текста;",
        "- `needs_review` / `review_reasons`: причины ручной проверки.",
        "",
        "## Итог",
        "",
        f"- Всего чанков: `{len(chunks)}`.",
        f"- Документов с чанками: `{len(by_doc)}`.",
        f"- Чанков с изображениями: `{sum(bool(c['media_refs']) for c in chunks)}`.",
        f"- Чанков с `related_image_ids`: `{sum(bool(c['related_image_ids']) for c in chunks)}`.",
        f"- Уникальных `related_image_ids`: `{len(set(all_related_image_ids))}`.",
        f"- Уникальных `excluded_image_ids`: `{len(set(all_excluded_image_ids))}`.",
        f"- Уникальных `review_image_ids`: `{len(set(all_review_image_ids))}`.",
        f"- Чанков с `needs_review`: `{sum(bool(c['needs_review']) for c in chunks)}`.",
        "",
        "## По документам",
        "",
        "| Документ | Чанков | С изображениями | На ревью |",
        "|---|---:|---:|---:|",
    ]
    for source_file, doc_chunks in by_doc.items():
        lines.append(
            "| `{}` | {} | {} | {} |".format(
                source_file,
                len(doc_chunks),
                sum(bool(c["media_refs"]) for c in doc_chunks),
                sum(bool(c["needs_review"]) for c in doc_chunks),
            )
        )
    lines.extend(
        [
            "",
            "## Ограничения",
            "",
            "- PDF-документы размечены как `pdf_text_layout_review_required`, потому что текущий текст извлечен с layout-артефактами.",
            "- `related_image_ids` не означает, что картинка сама является источником утверждения; утверждение должно подтверждаться текстом чанка.",
            "- `excluded_image_ids` не передаются в автоматическое извлечение утверждений без ручного переопределения.",
        ]
    )
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: build_source_chunks.py <project_root>", file=sys.stderr)
        return 1
    project_root = Path(argv[1]).resolve()
    image_index = load_image_index(project_root)
    docs = load_documents(project_root)
    chunks: list[dict[str, object]] = []
    for doc in docs:
        chunks.extend(make_chunks_for_document(doc, image_index))
    write_outputs(project_root, chunks)
    print(f"Wrote {len(chunks)} chunks for {len(docs)} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
