#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DEFAULT_CHUNKS_PATH = Path("00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl")
DEFAULT_STATEMENTS_PATH = Path("00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl")
DEFAULT_REPORT_PATH = Path("00_input/documents/electricians_knowledge_base/statements/source_coverage_report.md")
DEFAULT_OVERRIDES_PATH = Path("00_input/documents/electricians_knowledge_base/statements/source_coverage_overrides.jsonl")

MARKDOWN_RE = re.compile(r"[*_`>#\\\[\](){}]")
HTML_TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def clean_text(text: str) -> str:
    text = HTML_TAG_RE.sub(" ", text)
    text = MARKDOWN_RE.sub(" ", text)
    text = text.replace("&nbsp;", " ")
    return SPACE_RE.sub(" ", text).strip(" .:-–—\t\r\n")


def is_heading_like(chunk: dict[str, Any]) -> bool:
    text = clean_text(str(chunk.get("text", "")))
    if not text:
        return True
    if len(text) <= 100 and not re.search(r"[.!?]\s+\S", text):
        lowered = text.lower()
        heading_markers = (
            "контроль",
            "требования",
            "в папке",
            "в текстовом файле",
            "в 1с",
            "пример",
            "комментарий",
            "контрольный лист",
            "кабель-трасса",
            "особенности",
        )
        if any(marker in lowered for marker in heading_markers):
            return True
        section_path = " ".join(str(x) for x in chunk.get("section_path", []))
        if text and text in clean_text(section_path):
            return True
    return False


def source_files_from_args(chunks: list[dict[str, Any]], args: argparse.Namespace) -> set[str]:
    if args.source_file:
        return set(args.source_file)
    if args.source_document_id:
        ids = set(args.source_document_id)
        return {c["source_file"] for c in chunks if c.get("source_document_id") in ids}
    if args.topic:
        topics = set(args.topic)
        return {c["source_file"] for c in chunks if c.get("topic") in topics}
    return {c["source_file"] for c in chunks}


def build_report(
    chunks: list[dict[str, Any]],
    statements: list[dict[str, Any]],
    source_files: set[str],
    overrides: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    statements_by_chunk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for statement in statements:
        statements_by_chunk[statement["source_chunk_id"]].append(statement)

    rows: list[dict[str, Any]] = []
    for chunk in chunks:
        if chunk["source_file"] not in source_files:
            continue
        chunk_statements = statements_by_chunk.get(chunk["chunk_id"], [])
        if chunk_statements:
            status = "covered"
            reason = "has_statements"
        elif chunk["chunk_id"] in overrides:
            override = overrides[chunk["chunk_id"]]
            status = override.get("status", "ignored")
            reason = override.get("reason", "coverage_override")
        elif is_heading_like(chunk):
            status = "ignored"
            reason = "heading_or_context"
        elif chunk.get("needs_review"):
            status = "needs_review"
            reason = ",".join(chunk.get("review_reasons", [])) or "chunk_needs_review"
        else:
            status = "uncovered_content"
            reason = "no_canonical_statement_for_content_chunk"

        rows.append(
            {
                "source_document_id": chunk["source_document_id"],
                "source_file": chunk["source_file"],
                "chunk_id": chunk["chunk_id"],
                "status": status,
                "reason": reason,
                "statement_count": len(chunk_statements),
                "statement_ids": [s["statement_id"] for s in chunk_statements],
                "covered_by_statement_ids": overrides.get(chunk["chunk_id"], {}).get("covered_by_statement_ids", []),
                "override_notes": overrides.get(chunk["chunk_id"], {}).get("notes", ""),
                "text_preview": clean_text(str(chunk.get("text", "")))[:180],
            }
        )

    totals = Counter(row["status"] for row in rows)
    by_file: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        by_file[row["source_file"]][row["status"]] += 1

    summary = {
        "source_files_checked": len(source_files),
        "chunks_checked": len(rows),
        "status_totals": dict(totals),
        "by_file": {source_file: dict(counter) for source_file, counter in sorted(by_file.items())},
    }
    return rows, summary


def render_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# Source Coverage Report",
        "",
        "## Summary",
        "",
        f"- Source files checked: `{summary['source_files_checked']}`",
        f"- Chunks checked: `{summary['chunks_checked']}`",
    ]
    for status, count in sorted(summary["status_totals"].items()):
        lines.append(f"- `{status}`: `{count}`")

    lines.extend(["", "## By File", ""])
    for source_file, counts in summary["by_file"].items():
        count_text = ", ".join(f"`{status}`: `{count}`" for status, count in sorted(counts.items()))
        lines.append(f"- `{source_file}`: {count_text}")

    uncovered = [row for row in rows if row["status"] == "uncovered_content"]
    if uncovered:
        lines.extend(["", "## Uncovered Content Chunks", ""])
        for row in uncovered:
            lines.extend(
                [
                    f"### `{row['chunk_id']}`",
                    "",
                    f"- Source: `{row['source_file']}`",
                    f"- Reason: `{row['reason']}`",
                    f"- Preview: {row['text_preview']}",
                    "",
                ]
            )

    override_rows = [row for row in rows if row["covered_by_statement_ids"] and row["status"] == "ignored"]
    if override_rows:
        lines.extend(["", "## Coverage Overrides", ""])
        for row in override_rows:
            covered_by = ", ".join(f"`{statement_id}`" for statement_id in row["covered_by_statement_ids"])
            lines.extend(
                [
                    f"### `{row['chunk_id']}`",
                    "",
                    f"- Source: `{row['source_file']}`",
                    f"- Reason: `{row['reason']}`",
                    f"- Covered by: {covered_by}",
                    f"- Notes: {row['override_notes']}",
                    "",
                ]
            )

    review = [row for row in rows if row["status"] == "needs_review"]
    if review:
        lines.extend(["", "## Review Chunks", ""])
        for row in review:
            lines.extend(
                [
                    f"- `{row['chunk_id']}` / `{row['source_file']}`: {row['reason']}",
                ]
            )

    lines.extend(["", "## Machine Rows", "", "See JSONL companion if generated by caller."])
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check source chunk coverage by canonical atomic statements.")
    parser.add_argument("project_root")
    parser.add_argument("--source-file", action="append", help="Limit check to a source file. Can be repeated.")
    parser.add_argument("--source-document-id", action="append", help="Limit check to a source document id. Can be repeated.")
    parser.add_argument("--topic", action="append", help="Limit check to a chunk topic. Can be repeated.")
    parser.add_argument("--statements", default=str(DEFAULT_STATEMENTS_PATH), help="Statements JSONL path relative to project root.")
    parser.add_argument("--chunks", default=str(DEFAULT_CHUNKS_PATH), help="Chunks JSONL path relative to project root.")
    parser.add_argument("--output-md", default=str(DEFAULT_REPORT_PATH), help="Markdown report path relative to project root.")
    parser.add_argument("--output-jsonl", help="Optional JSONL detail report path relative to project root.")
    parser.add_argument("--overrides", default=str(DEFAULT_OVERRIDES_PATH), help="Coverage overrides JSONL path relative to project root.")
    parser.add_argument("--fail-on-uncovered", action="store_true", help="Exit non-zero when content chunks lack statements.")
    args = parser.parse_args(argv[1:])

    project_root = Path(args.project_root).resolve()
    chunks = load_jsonl(project_root / args.chunks)
    statements = load_jsonl(project_root / args.statements)
    overrides_path = project_root / args.overrides
    overrides = {
        row["chunk_id"]: row
        for row in load_jsonl(overrides_path)
    } if overrides_path.exists() else {}
    source_files = source_files_from_args(chunks, args)
    rows, summary = build_report(chunks, statements, source_files, overrides)

    output_md = project_root / args.output_md
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(rows, summary), encoding="utf-8")

    if args.output_jsonl:
        output_jsonl = project_root / args.output_jsonl
        output_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with output_jsonl.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    uncovered_count = summary["status_totals"].get("uncovered_content", 0)
    if uncovered_count and args.fail_on_uncovered:
        print(f"Source coverage failed: {uncovered_count} content chunks are not covered.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
