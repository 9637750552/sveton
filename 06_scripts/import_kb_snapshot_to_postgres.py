from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import semantic_project_config as project_config


PROJECT_NAME = "Sveton"
CORPUS_NAME = "Electricians Knowledge Base"
SCHEMA_VERSION = "001_create_kb_review_schema"

STATEMENT_CLUSTERS_FILE = "statement_clusters.json"
STATEMENT_RELATIONS_FILE = "statement_relations.jsonl"
STATEMENT_IMAGES_FILE = "statement_images.jsonl"
SOURCE_COVERAGE_REPORT_FILE = "source_coverage_report.jsonl"

REVIEW_FILE_PATTERNS = [
    "statements/review/*.md",
    "statements/safety_review_queue.md",
    "statements/safety_review_c009_installation_process.md",
    "statements/source_quality_issues.md",
    "statements/batch_*.md",
]

STATEMENT_RISK_LEVELS = {"ordinary", "important", "safety_critical"}
STATEMENT_CONFIDENCE = {"high", "medium", "low"}
STATEMENT_REVIEW_STATUSES = {"extracted", "review_required", "rejected"}


@dataclass(frozen=True)
class ImportPaths:
    config_path: Path
    inventory_path: Path
    chunks_path: Path
    statements_path: Path
    statements_dir: Path
    clusters_path: Path
    relations_path: Path
    images_path: Path
    statement_images_path: Path
    coverage_report_path: Path
    coverage_overrides_path: Path
    extraction_errors_path: Path
    coverage_warnings_path: Path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            rows.append(row)
    return rows


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_markdown_table_row(line: str) -> list[str]:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return [cell.strip("`").strip() for cell in cells]


def split_csv_like(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def split_pipe_like(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def read_inventory(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = parse_markdown_table_row(stripped)
        if len(cells) < 8:
            continue
        if cells[0] == "№":
            header = cells
            continue
        if cells[0].replace(":", "").replace("-", "") == "":
            continue
        if header is None or cells[0].startswith("---"):
            continue
        try:
            doc_no = int(cells[0])
        except ValueError:
            continue
        raw = dict(zip(header, cells, strict=False))
        rows.append(
            {
                "source_document_id": f"doc_{doc_no:03d}",
                "source_file": raw.get("Файл", ""),
                "source_format": raw.get("Формат") or None,
                "document_type": raw.get("Тип") or None,
                "topic": raw.get("Основная тема") or None,
                "roles": split_csv_like(raw.get("Роли")),
                "status": raw.get("Статус") or None,
                "metadata": {
                    "document_number": doc_no,
                    "status_values": split_csv_like(raw.get("Статус")),
                    "comment": raw.get("Комментарий") or "",
                    "raw_row": raw,
                },
            }
        )
    return rows


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def as_text_list(value: Any) -> list[str]:
    return [str(item) for item in as_list(value) if item not in (None, "")]


def as_bool(value: Any) -> bool:
    return bool(value)


def as_int_or_none(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def relpath(project_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(project_root))
    except ValueError:
        return str(path)


def file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=str):
        digest.update(str(path).encode("utf-8"))
        digest.update(b"\0")
        if path.exists():
            digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_commit(project_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def sql_literal(value: Any) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def sql_bool(value: bool) -> str:
    return "TRUE" if value else "FALSE"


def sql_int(value: int | None) -> str:
    return "NULL" if value is None else str(value)


def sql_text_array(values: list[Any]) -> str:
    if not values:
        return "ARRAY[]::text[]"
    return "ARRAY[" + ", ".join(sql_literal(str(value)) for value in values) + "]::text[]"


def sql_jsonb(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return sql_literal(text) + "::jsonb"


def project_id_sql(project_key: str) -> str:
    return f"(SELECT id FROM kb.projects WHERE project_key = {sql_literal(project_key)})"


def corpus_id_sql(project_key: str, corpus_key: str) -> str:
    return (
        "(SELECT c.id FROM kb.corpora c "
        "JOIN kb.projects p ON p.id = c.project_id "
        f"WHERE p.project_key = {sql_literal(project_key)} "
        f"AND c.corpus_key = {sql_literal(corpus_key)})"
    )


def source_id_sql(project_key: str, corpus_key: str, source_document_id: str) -> str:
    return (
        "(SELECT s.id FROM kb.sources s "
        "JOIN kb.projects p ON p.id = s.project_id "
        "JOIN kb.corpora c ON c.id = s.corpus_id "
        f"WHERE p.project_key = {sql_literal(project_key)} "
        f"AND c.corpus_key = {sql_literal(corpus_key)} "
        f"AND s.source_document_id = {sql_literal(source_document_id)})"
    )


def chunk_db_id_sql(project_key: str, corpus_key: str, chunk_id: str) -> str:
    return (
        "(SELECT ch.id FROM kb.chunks ch "
        "JOIN kb.projects p ON p.id = ch.project_id "
        "JOIN kb.corpora c ON c.id = ch.corpus_id "
        f"WHERE p.project_key = {sql_literal(project_key)} "
        f"AND c.corpus_key = {sql_literal(corpus_key)} "
        f"AND ch.chunk_id = {sql_literal(chunk_id)})"
    )


def statement_db_id_sql(project_key: str, corpus_key: str, statement_id: str) -> str:
    return (
        "(SELECT st.id FROM kb.statements st "
        "JOIN kb.projects p ON p.id = st.project_id "
        "JOIN kb.corpora c ON c.id = st.corpus_id "
        f"WHERE p.project_key = {sql_literal(project_key)} "
        f"AND c.corpus_key = {sql_literal(corpus_key)} "
        f"AND st.statement_id = {sql_literal(statement_id)})"
    )


def image_db_id_sql(project_key: str, corpus_key: str, image_id: str) -> str:
    return (
        "(SELECT im.id FROM kb.images im "
        "JOIN kb.projects p ON p.id = im.project_id "
        "JOIN kb.corpora c ON c.id = im.corpus_id "
        f"WHERE p.project_key = {sql_literal(project_key)} "
        f"AND c.corpus_key = {sql_literal(corpus_key)} "
        f"AND im.image_id = {sql_literal(image_id)})"
    )


def cluster_db_id_sql(project_key: str, corpus_key: str, cluster_id: str) -> str:
    return (
        "(SELECT cl.id FROM kb.clusters cl "
        "JOIN kb.projects p ON p.id = cl.project_id "
        "JOIN kb.corpora c ON c.id = cl.corpus_id "
        f"WHERE p.project_key = {sql_literal(project_key)} "
        f"AND c.corpus_key = {sql_literal(corpus_key)} "
        f"AND cl.cluster_id = {sql_literal(cluster_id)})"
    )


def discrepancy(
    severity: str,
    artifact: str,
    row_id: str,
    check: str,
    message: str,
    related_ids: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "severity": severity,
        "artifact": artifact,
        "row_id": row_id,
        "check": check,
        "message": message,
        "related_ids": related_ids or [],
    }


def duplicate_values(rows: list[dict[str, Any]], key: str) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        value = str(row.get(key) or "")
        if not value:
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def build_paths(project_root: Path, config_path_arg: str | None) -> tuple[dict[str, str], ImportPaths]:
    config = project_config.load_project_config(project_root, config_path_arg)
    config_path = project_root / (config_path_arg or project_config.DEFAULT_CONFIG_PATH)
    statements_dir = project_config.config_path(project_root, config, "statements_dir")
    paths = ImportPaths(
        config_path=config_path,
        inventory_path=project_config.config_path(project_root, config, "source_inventory"),
        chunks_path=project_config.config_path(project_root, config, "chunks"),
        statements_path=project_config.config_path(project_root, config, "statements"),
        statements_dir=statements_dir,
        clusters_path=statements_dir / STATEMENT_CLUSTERS_FILE,
        relations_path=statements_dir / STATEMENT_RELATIONS_FILE,
        images_path=project_config.config_path(project_root, config, "images_inventory"),
        statement_images_path=statements_dir / STATEMENT_IMAGES_FILE,
        coverage_report_path=statements_dir / SOURCE_COVERAGE_REPORT_FILE,
        coverage_overrides_path=project_config.config_path(project_root, config, "coverage_overrides"),
        extraction_errors_path=project_config.config_path(project_root, config, "extraction_errors"),
        coverage_warnings_path=project_config.config_path(project_root, config, "coverage_warnings"),
    )
    return config, paths


def load_snapshot(project_root: Path, paths: ImportPaths) -> dict[str, Any]:
    clusters = read_json(paths.clusters_path)
    return {
        "sources": read_inventory(paths.inventory_path),
        "chunks": read_jsonl(paths.chunks_path),
        "statements": read_jsonl(paths.statements_path),
        "clusters": clusters.get("clusters", []),
        "clusters_raw": clusters,
        "relations": read_jsonl(paths.relations_path),
        "images": read_csv(paths.images_path),
        "statement_images": read_jsonl(paths.statement_images_path),
        "coverage_report": read_jsonl(paths.coverage_report_path),
        "coverage_overrides": read_jsonl(paths.coverage_overrides_path),
        "extraction_errors": read_jsonl(paths.extraction_errors_path),
        "coverage_warnings": read_jsonl(paths.coverage_warnings_path),
        "review_files": find_review_files(project_root, paths.statements_dir),
    }


def find_review_files(project_root: Path, statements_dir: Path) -> list[str]:
    base = statements_dir.parent
    found: set[str] = set()
    for pattern in REVIEW_FILE_PATTERNS:
        for path in base.glob(pattern):
            if path.is_file():
                found.add(relpath(project_root, path))
    return sorted(found)


def validate_snapshot(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    discrepancies: list[dict[str, Any]] = []

    sources = snapshot["sources"]
    chunks = snapshot["chunks"]
    statements = snapshot["statements"]
    clusters = snapshot["clusters"]
    relations = snapshot["relations"]
    images = snapshot["images"]
    statement_images = snapshot["statement_images"]

    source_ids = {row["source_document_id"] for row in sources}
    source_files = {row["source_file"] for row in sources}
    chunk_ids = {row["chunk_id"] for row in chunks}
    statement_ids = {row["statement_id"] for row in statements}
    image_ids = {row["image_id"] for row in images}

    for artifact, rows, key in [
        ("inventory.md", sources, "source_document_id"),
        ("inventory.md", sources, "source_file"),
        ("source_chunks.jsonl", chunks, "chunk_id"),
        ("atomic_statements.jsonl", statements, "statement_id"),
        ("images/inventory.csv", images, "image_id"),
        ("statement_relations.jsonl", relations, "relation_id"),
    ]:
        for value in sorted(duplicate_values(rows, key)):
            discrepancies.append(
                discrepancy("error", artifact, value, "duplicate_id", f"Duplicate {key}: {value}", [value])
            )

    for row in chunks:
        chunk_id = row.get("chunk_id", "")
        if row.get("source_document_id") not in source_ids:
            discrepancies.append(
                discrepancy(
                    "error",
                    "source_chunks.jsonl",
                    chunk_id,
                    "missing_source_document",
                    "chunk source_document_id does not resolve to inventory.md",
                    [str(row.get("source_document_id") or "")],
                )
            )
        if row.get("source_file") not in source_files:
            discrepancies.append(
                discrepancy(
                    "error",
                    "source_chunks.jsonl",
                    chunk_id,
                    "missing_source_file",
                    "chunk source_file does not resolve to inventory.md",
                    [str(row.get("source_file") or "")],
                )
            )
        for link_key in ("previous_chunk_id", "next_chunk_id"):
            linked = row.get(link_key)
            if linked and linked not in chunk_ids:
                discrepancies.append(
                    discrepancy(
                        "error",
                        "source_chunks.jsonl",
                        chunk_id,
                        f"missing_{link_key}",
                        f"{link_key} does not resolve inside source_chunks.jsonl",
                        [str(linked)],
                    )
                )
        for image_key in ("related_image_ids", "excluded_image_ids", "review_image_ids"):
            for image_id in as_text_list(row.get(image_key)):
                if image_id not in image_ids:
                    discrepancies.append(
                        discrepancy(
                            "warning",
                            "source_chunks.jsonl",
                            chunk_id,
                            f"unresolved_{image_key}",
                            f"{image_key} contains image id not present in images/inventory.csv",
                            [image_id],
                        )
                    )

    chunks_by_id = {row["chunk_id"]: row for row in chunks}
    for row in statements:
        statement_id = row.get("statement_id", "")
        source_chunk_id = row.get("source_chunk_id")
        chunk = chunks_by_id.get(source_chunk_id)
        if row.get("source_document_id") not in source_ids:
            discrepancies.append(
                discrepancy("error", "atomic_statements.jsonl", statement_id, "missing_source_document", "statement source_document_id does not resolve", [str(row.get("source_document_id") or "")])
            )
        if row.get("source_file") not in source_files:
            discrepancies.append(
                discrepancy("error", "atomic_statements.jsonl", statement_id, "missing_source_file", "statement source_file does not resolve", [str(row.get("source_file") or "")])
            )
        if chunk is None:
            discrepancies.append(
                discrepancy("error", "atomic_statements.jsonl", statement_id, "missing_chunk", "source_chunk_id does not resolve to source_chunks.jsonl", [str(source_chunk_id or "")])
            )
        elif chunk.get("source_document_id") != row.get("source_document_id") or chunk.get("source_file") != row.get("source_file"):
            discrepancies.append(
                discrepancy(
                    "error",
                    "atomic_statements.jsonl",
                    statement_id,
                    "source_chunk_mismatch",
                    "statement source_document_id/source_file does not match referenced chunk",
                    [str(source_chunk_id or "")],
                )
            )
        for field, allowed in [
            ("risk_level", STATEMENT_RISK_LEVELS),
            ("confidence", STATEMENT_CONFIDENCE),
            ("review_status", STATEMENT_REVIEW_STATUSES),
        ]:
            if row.get(field) not in allowed:
                discrepancies.append(
                    discrepancy("error", "atomic_statements.jsonl", statement_id, f"invalid_{field}", f"{field} is outside DB constraint values", [str(row.get(field) or "")])
                )
        if not row.get("source_quote_is_exact", False):
            discrepancies.append(
                discrepancy("warning", "atomic_statements.jsonl", statement_id, "inexact_source_quote", "source_quote_is_exact is false", [statement_id])
            )
        for image_id in as_text_list(row.get("related_image_ids")):
            if image_id not in image_ids:
                discrepancies.append(
                    discrepancy("warning", "atomic_statements.jsonl", statement_id, "unresolved_related_image", "related_image_ids contains image id not present in images/inventory.csv", [image_id])
                )

    assigned_statement_ids: list[str] = []
    cluster_ids: set[str] = set()
    for cluster in clusters:
        cluster_id = str(cluster.get("cluster_id") or "")
        if cluster_id in cluster_ids:
            discrepancies.append(discrepancy("error", "statement_clusters.json", cluster_id, "duplicate_cluster_id", "Duplicate cluster_id", [cluster_id]))
        cluster_ids.add(cluster_id)
        member_ids = as_text_list(cluster.get("statement_ids"))
        assigned_statement_ids.extend(member_ids)
        if cluster.get("statement_count") != len(member_ids):
            discrepancies.append(
                discrepancy("error", "statement_clusters.json", cluster_id, "cluster_count_mismatch", "statement_count does not equal statement_ids length", [cluster_id])
            )
        for statement_id in member_ids:
            if statement_id not in statement_ids:
                discrepancies.append(
                    discrepancy("error", "statement_clusters.json", cluster_id, "missing_statement", "cluster statement id does not resolve to atomic_statements.jsonl", [statement_id])
                )
    duplicate_assignments = {sid for sid in assigned_statement_ids if assigned_statement_ids.count(sid) > 1}
    for statement_id in sorted(duplicate_assignments):
        discrepancies.append(
            discrepancy("error", "statement_clusters.json", statement_id, "duplicate_cluster_assignment", "statement id appears in multiple cluster assignments", [statement_id])
        )
    for statement_id in sorted(statement_ids - set(assigned_statement_ids)):
        discrepancies.append(
            discrepancy("error", "statement_clusters.json", statement_id, "unassigned_statement", "statement id is not assigned to any cluster", [statement_id])
        )

    for row in relations:
        row_id = str(row.get("relation_id") or row.get("group_id") or "")
        source_statement_id = row.get("source_statement_id")
        target_statement_id = row.get("target_statement_id")
        if source_statement_id not in statement_ids:
            discrepancies.append(discrepancy("error", "statement_relations.jsonl", row_id, "missing_source_statement", "source_statement_id does not resolve", [str(source_statement_id or "")]))
        if target_statement_id not in statement_ids:
            discrepancies.append(discrepancy("error", "statement_relations.jsonl", row_id, "missing_target_statement", "target_statement_id does not resolve", [str(target_statement_id or "")]))
        if source_statement_id and source_statement_id == target_statement_id:
            discrepancies.append(discrepancy("error", "statement_relations.jsonl", row_id, "self_relation", "source and target statements are identical", [str(source_statement_id)]))

    for row in images:
        image_id = row.get("image_id", "")
        if row.get("source_file") and row.get("source_file") not in source_files:
            discrepancies.append(
                discrepancy("warning", "images/inventory.csv", image_id, "unresolved_source_file", "image source_file does not resolve to inventory.md", [row.get("source_file", "")])
            )
        for field in ("width", "height"):
            try:
                as_int_or_none(row.get(field))
            except ValueError:
                discrepancies.append(
                    discrepancy("error", "images/inventory.csv", image_id, f"invalid_{field}", f"{field} must be integer or null", [str(row.get(field) or "")])
                )

    for row in statement_images:
        row_id = f"{row.get('statement_id', '')}:{row.get('image_id', '')}:{row.get('link_type', '')}"
        if row.get("statement_id") not in statement_ids:
            discrepancies.append(discrepancy("error", "statement_images.jsonl", row_id, "missing_statement", "statement_id does not resolve", [str(row.get("statement_id") or "")]))
        if row.get("image_id") not in image_ids:
            discrepancies.append(discrepancy("error", "statement_images.jsonl", row_id, "missing_image", "image_id does not resolve", [str(row.get("image_id") or "")]))

    return discrepancies


def build_source_summary(
    project_root: Path,
    paths: ImportPaths,
    snapshot: dict[str, Any],
    discrepancies: list[dict[str, Any]],
    import_run_key: str,
    source_git_commit: str | None,
) -> dict[str, Any]:
    artifact_paths = [
        paths.config_path,
        paths.inventory_path,
        paths.chunks_path,
        paths.statements_path,
        paths.clusters_path,
        paths.relations_path,
        paths.images_path,
        paths.statement_images_path,
        paths.coverage_report_path,
        paths.coverage_overrides_path,
        paths.extraction_errors_path,
        paths.coverage_warnings_path,
    ]
    counts = {
        "sources": len(snapshot["sources"]),
        "chunks": len(snapshot["chunks"]),
        "statements": len(snapshot["statements"]),
        "clusters": len(snapshot["clusters"]),
        "relations": len(snapshot["relations"]),
        "images": len(snapshot["images"]),
        "statement_images": len(snapshot["statement_images"]),
        "coverage_report": len(snapshot["coverage_report"]),
        "coverage_overrides": len(snapshot["coverage_overrides"]),
        "extraction_errors": len(snapshot["extraction_errors"]),
        "coverage_warnings": len(snapshot["coverage_warnings"]),
        "discrepancy_errors": sum(1 for row in discrepancies if row["severity"] == "error"),
        "discrepancy_warnings": sum(1 for row in discrepancies if row["severity"] == "warning"),
    }
    return {
        "import_run_key": import_run_key,
        "source_git_commit": source_git_commit,
        "schema_version": SCHEMA_VERSION,
        "artifact_paths": {path.name: relpath(project_root, path) for path in artifact_paths},
        "artifact_hashes": {relpath(project_root, path): file_sha256(path) for path in artifact_paths},
        "counts": counts,
        "coverage_report": {
            "rows": len(snapshot["coverage_report"]),
            "path": relpath(project_root, paths.coverage_report_path),
        },
        "coverage_overrides": {
            "rows": len(snapshot["coverage_overrides"]),
            "path": relpath(project_root, paths.coverage_overrides_path),
        },
        "file_only_review_evidence": snapshot["review_files"],
    }


def append_project_sql(sql: list[str], project_key: str, corpus_key: str, source_summary: dict[str, Any], config_path: str, import_run_key: str, source_git_commit: str | None) -> None:
    project_id = project_id_sql(project_key)
    corpus_id = corpus_id_sql(project_key, corpus_key)
    sql.append(
        "INSERT INTO kb.projects(project_key, name) "
        f"VALUES ({sql_literal(project_key)}, {sql_literal(PROJECT_NAME)}) "
        "ON CONFLICT (project_key) DO UPDATE SET name = EXCLUDED.name;"
    )
    sql.append(
        "INSERT INTO kb.corpora(project_id, corpus_key, name) "
        f"VALUES ({project_id}, {sql_literal(corpus_key)}, {sql_literal(CORPUS_NAME)}) "
        "ON CONFLICT (project_id, corpus_key) DO UPDATE SET name = EXCLUDED.name;"
    )
    sql.append(
        "INSERT INTO kb.import_runs(project_id, corpus_id, import_run_key, source_git_commit, engine_git_commit, schema_version, config_path, source_summary) "
        f"VALUES ({project_id}, {corpus_id}, {sql_literal(import_run_key)}, {sql_literal(source_git_commit)}, NULL, "
        f"{sql_literal(SCHEMA_VERSION)}, {sql_literal(config_path)}, {sql_jsonb(source_summary)}) "
        "ON CONFLICT (project_id, corpus_id, import_run_key) DO UPDATE SET "
        "source_git_commit = EXCLUDED.source_git_commit, "
        "engine_git_commit = EXCLUDED.engine_git_commit, "
        "schema_version = EXCLUDED.schema_version, "
        "config_path = EXCLUDED.config_path, "
        "source_summary = EXCLUDED.source_summary;"
    )


def append_sources_sql(sql: list[str], project_key: str, corpus_key: str, sources: list[dict[str, Any]]) -> None:
    project_id = project_id_sql(project_key)
    corpus_id = corpus_id_sql(project_key, corpus_key)
    for row in sources:
        sql.append(
            "INSERT INTO kb.sources(project_id, corpus_id, source_document_id, source_file, source_format, document_type, topic, roles, status, metadata) "
            f"VALUES ({project_id}, {corpus_id}, {sql_literal(row['source_document_id'])}, {sql_literal(row['source_file'])}, "
            f"{sql_literal(row.get('source_format'))}, {sql_literal(row.get('document_type'))}, {sql_literal(row.get('topic'))}, "
            f"{sql_text_array(row.get('roles', []))}, {sql_literal(row.get('status'))}, {sql_jsonb(row.get('metadata', {}))}) "
            "ON CONFLICT (project_id, corpus_id, source_document_id) DO UPDATE SET "
            "source_file = EXCLUDED.source_file, source_format = EXCLUDED.source_format, document_type = EXCLUDED.document_type, "
            "topic = EXCLUDED.topic, roles = EXCLUDED.roles, status = EXCLUDED.status, metadata = EXCLUDED.metadata;"
        )


def append_chunks_sql(sql: list[str], project_key: str, corpus_key: str, chunks: list[dict[str, Any]]) -> None:
    project_id = project_id_sql(project_key)
    corpus_id = corpus_id_sql(project_key, corpus_key)
    for row in chunks:
        source_document_id = str(row.get("source_document_id") or "")
        sql.append(
            "INSERT INTO kb.chunks(project_id, corpus_id, source_id, chunk_id, source_document_id, source_file, topic, roles, section_path, chunk_text, "
            "related_image_ids, excluded_image_ids, review_image_ids, previous_chunk_id, next_chunk_id, previous_context, next_context, needs_review, review_reasons, raw_payload) "
            f"VALUES ({project_id}, {corpus_id}, {source_id_sql(project_key, corpus_key, source_document_id)}, "
            f"{sql_literal(row.get('chunk_id'))}, {sql_literal(source_document_id)}, {sql_literal(row.get('source_file'))}, "
            f"{sql_literal(row.get('topic'))}, {sql_text_array(as_text_list(row.get('roles')))}, {sql_text_array(as_text_list(row.get('section_path')))}, "
            f"{sql_literal(row.get('text') or '')}, {sql_text_array(as_text_list(row.get('related_image_ids')))}, "
            f"{sql_text_array(as_text_list(row.get('excluded_image_ids')))}, {sql_text_array(as_text_list(row.get('review_image_ids')))}, "
            f"{sql_literal(row.get('previous_chunk_id'))}, {sql_literal(row.get('next_chunk_id'))}, {sql_literal(row.get('previous_context'))}, "
            f"{sql_literal(row.get('next_context'))}, {sql_bool(as_bool(row.get('needs_review')))}, {sql_text_array(as_text_list(row.get('review_reasons')))}, {sql_jsonb(row)}) "
            "ON CONFLICT (project_id, corpus_id, chunk_id) DO UPDATE SET "
            "source_id = EXCLUDED.source_id, source_document_id = EXCLUDED.source_document_id, source_file = EXCLUDED.source_file, "
            "topic = EXCLUDED.topic, roles = EXCLUDED.roles, section_path = EXCLUDED.section_path, chunk_text = EXCLUDED.chunk_text, "
            "related_image_ids = EXCLUDED.related_image_ids, excluded_image_ids = EXCLUDED.excluded_image_ids, review_image_ids = EXCLUDED.review_image_ids, "
            "previous_chunk_id = EXCLUDED.previous_chunk_id, next_chunk_id = EXCLUDED.next_chunk_id, previous_context = EXCLUDED.previous_context, "
            "next_context = EXCLUDED.next_context, needs_review = EXCLUDED.needs_review, review_reasons = EXCLUDED.review_reasons, raw_payload = EXCLUDED.raw_payload;"
        )


def append_images_sql(sql: list[str], project_key: str, corpus_key: str, images: list[dict[str, str]]) -> None:
    project_id = project_id_sql(project_key)
    corpus_id = corpus_id_sql(project_key, corpus_key)
    for row in images:
        sql.append(
            "INSERT INTO kb.images(project_id, corpus_id, image_id, source_file, file_name, media_ref, image_type, topic, roles, status, width, height, caption, source_anchor, nearby_text, linking_bucket, raw_payload) "
            f"VALUES ({project_id}, {corpus_id}, {sql_literal(row.get('image_id'))}, {sql_literal(row.get('source_file'))}, "
            f"{sql_literal(row.get('file_name'))}, {sql_literal(row.get('media_ref'))}, {sql_literal(row.get('image_type'))}, "
            f"{sql_literal(row.get('topic'))}, {sql_text_array(split_pipe_like(row.get('roles')))}, {sql_literal(row.get('status'))}, "
            f"{sql_int(as_int_or_none(row.get('width')))}, {sql_int(as_int_or_none(row.get('height')))}, {sql_literal(row.get('caption'))}, "
            f"{sql_literal(row.get('source_anchor'))}, {sql_literal(row.get('nearby_text'))}, {sql_literal(row.get('linking_bucket'))}, {sql_jsonb(row)}) "
            "ON CONFLICT (project_id, corpus_id, image_id) DO UPDATE SET "
            "source_file = EXCLUDED.source_file, file_name = EXCLUDED.file_name, media_ref = EXCLUDED.media_ref, image_type = EXCLUDED.image_type, "
            "topic = EXCLUDED.topic, roles = EXCLUDED.roles, status = EXCLUDED.status, width = EXCLUDED.width, height = EXCLUDED.height, "
            "caption = EXCLUDED.caption, source_anchor = EXCLUDED.source_anchor, nearby_text = EXCLUDED.nearby_text, linking_bucket = EXCLUDED.linking_bucket, raw_payload = EXCLUDED.raw_payload;"
        )


def append_statements_sql(sql: list[str], project_key: str, corpus_key: str, statements: list[dict[str, Any]]) -> None:
    project_id = project_id_sql(project_key)
    corpus_id = corpus_id_sql(project_key, corpus_key)
    for row in statements:
        source_document_id = str(row.get("source_document_id") or "")
        source_chunk_id = str(row.get("source_chunk_id") or "")
        sql.append(
            "INSERT INTO kb.statements(project_id, corpus_id, source_id, chunk_db_id, statement_id, statement_text, statement_type, topic, roles, "
            "source_document_id, source_file, source_chunk_id, section_path, source_quote, source_quote_is_exact, related_image_ids, visual_review_required, "
            "risk_level, confidence, review_status, scope, condition, action, object, normalized_terms, extraction_notes, downstream_status, raw_payload) "
            f"VALUES ({project_id}, {corpus_id}, {source_id_sql(project_key, corpus_key, source_document_id)}, {chunk_db_id_sql(project_key, corpus_key, source_chunk_id)}, "
            f"{sql_literal(row.get('statement_id'))}, {sql_literal(row.get('statement') or '')}, {sql_literal(row.get('statement_type') or '')}, "
            f"{sql_literal(row.get('topic'))}, {sql_text_array(as_text_list(row.get('roles')))}, {sql_literal(source_document_id)}, {sql_literal(row.get('source_file'))}, "
            f"{sql_literal(source_chunk_id)}, {sql_text_array(as_text_list(row.get('section_path')))}, {sql_literal(row.get('source_quote') or '')}, "
            f"{sql_bool(as_bool(row.get('source_quote_is_exact')))}, {sql_text_array(as_text_list(row.get('related_image_ids')))}, "
            f"{sql_bool(as_bool(row.get('visual_review_required')))}, {sql_literal(row.get('risk_level'))}, {sql_literal(row.get('confidence'))}, "
            f"{sql_literal(row.get('review_status'))}, {sql_literal(row.get('scope'))}, {sql_literal(row.get('condition'))}, {sql_literal(row.get('action'))}, "
            f"{sql_literal(row.get('object'))}, {sql_text_array(as_text_list(row.get('normalized_terms')))}, {sql_literal(row.get('extraction_notes'))}, "
            f"{sql_literal('draft')}, {sql_jsonb(row)}) "
            "ON CONFLICT (project_id, corpus_id, statement_id) DO UPDATE SET "
            "source_id = EXCLUDED.source_id, chunk_db_id = EXCLUDED.chunk_db_id, statement_type = EXCLUDED.statement_type, topic = EXCLUDED.topic, roles = EXCLUDED.roles, "
            "section_path = EXCLUDED.section_path, related_image_ids = EXCLUDED.related_image_ids, visual_review_required = EXCLUDED.visual_review_required, "
            "risk_level = EXCLUDED.risk_level, confidence = EXCLUDED.confidence, review_status = EXCLUDED.review_status, scope = EXCLUDED.scope, condition = EXCLUDED.condition, "
            "action = EXCLUDED.action, object = EXCLUDED.object, normalized_terms = EXCLUDED.normalized_terms, extraction_notes = EXCLUDED.extraction_notes, raw_payload = EXCLUDED.raw_payload "
            "WHERE kb.statements.statement_text = EXCLUDED.statement_text "
            "AND kb.statements.source_quote = EXCLUDED.source_quote "
            "AND kb.statements.source_chunk_id = EXCLUDED.source_chunk_id "
            "AND kb.statements.source_document_id = EXCLUDED.source_document_id "
            "AND kb.statements.source_file = EXCLUDED.source_file;"
        )


def append_clusters_sql(sql: list[str], project_key: str, corpus_key: str, clusters: list[dict[str, Any]]) -> None:
    project_id = project_id_sql(project_key)
    corpus_id = corpus_id_sql(project_key, corpus_key)
    for row in clusters:
        cluster_id = str(row.get("cluster_id") or "")
        sql.append(
            "INSERT INTO kb.clusters(project_id, corpus_id, cluster_id, title, topic, summary, raw_payload) "
            f"VALUES ({project_id}, {corpus_id}, {sql_literal(cluster_id)}, {sql_literal(row.get('title'))}, {sql_literal(row.get('topic'))}, {sql_literal(row.get('notes'))}, {sql_jsonb(row)}) "
            "ON CONFLICT (project_id, corpus_id, cluster_id) DO UPDATE SET "
            "title = EXCLUDED.title, topic = EXCLUDED.topic, summary = EXCLUDED.summary, raw_payload = EXCLUDED.raw_payload;"
        )
        for statement_id in as_text_list(row.get("statement_ids")):
            sql.append(
                "INSERT INTO kb.statement_clusters(statement_id, cluster_id, relation_type) "
                f"VALUES ({statement_db_id_sql(project_key, corpus_key, statement_id)}, {cluster_db_id_sql(project_key, corpus_key, cluster_id)}, 'member') "
                "ON CONFLICT (statement_id, cluster_id, relation_type) DO NOTHING;"
            )


def append_relations_sql(sql: list[str], project_key: str, corpus_key: str, relations: list[dict[str, Any]]) -> None:
    project_id = project_id_sql(project_key)
    corpus_id = corpus_id_sql(project_key, corpus_key)
    for row in relations:
        source_statement_id = str(row.get("source_statement_id") or "")
        target_statement_id = str(row.get("target_statement_id") or "")
        sql.append(
            "INSERT INTO kb.statement_relations(project_id, corpus_id, source_statement_id, target_statement_id, relation_type, confidence, notes, raw_payload) "
            f"VALUES ({project_id}, {corpus_id}, {statement_db_id_sql(project_key, corpus_key, source_statement_id)}, "
            f"{statement_db_id_sql(project_key, corpus_key, target_statement_id)}, {sql_literal(row.get('relation_type'))}, NULL, {sql_literal(row.get('notes'))}, {sql_jsonb(row)}) "
            "ON CONFLICT (source_statement_id, target_statement_id, relation_type) DO UPDATE SET "
            "notes = EXCLUDED.notes, raw_payload = EXCLUDED.raw_payload;"
        )


def append_statement_images_sql(sql: list[str], project_key: str, corpus_key: str, statement_images: list[dict[str, Any]]) -> None:
    for row in statement_images:
        statement_id = str(row.get("statement_id") or "")
        image_id = str(row.get("image_id") or "")
        sql.append(
            "INSERT INTO kb.statement_images(statement_id, image_id, link_type, review_status, notes, raw_payload) "
            f"VALUES ({statement_db_id_sql(project_key, corpus_key, statement_id)}, {image_db_id_sql(project_key, corpus_key, image_id)}, "
            f"{sql_literal(row.get('link_type') or 'illustrates')}, {sql_literal(row.get('status'))}, {sql_literal(row.get('rationale'))}, {sql_jsonb(row)}) "
            "ON CONFLICT (statement_id, image_id, link_type) DO UPDATE SET "
            "review_status = EXCLUDED.review_status, notes = EXCLUDED.notes, raw_payload = EXCLUDED.raw_payload;"
        )


def build_sql(config: dict[str, str], source_summary: dict[str, Any], snapshot: dict[str, Any], config_path: str, import_run_key: str, source_git_commit: str | None) -> str:
    project_key = config["project_id"]
    corpus_key = config["corpus_id"]
    sql: list[str] = [
        "\\set ON_ERROR_STOP on",
        "BEGIN;",
    ]
    append_project_sql(sql, project_key, corpus_key, source_summary, config_path, import_run_key, source_git_commit)
    append_sources_sql(sql, project_key, corpus_key, snapshot["sources"])
    append_chunks_sql(sql, project_key, corpus_key, snapshot["chunks"])
    append_images_sql(sql, project_key, corpus_key, snapshot["images"])
    append_statements_sql(sql, project_key, corpus_key, snapshot["statements"])
    append_clusters_sql(sql, project_key, corpus_key, snapshot["clusters"])
    append_relations_sql(sql, project_key, corpus_key, snapshot["relations"])
    append_statement_images_sql(sql, project_key, corpus_key, snapshot["statement_images"])
    sql.append("COMMIT;")
    return "\n".join(sql) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def apply_sql(sql_text: str, command: str) -> None:
    args = shlex.split(command)
    if not args:
        raise ValueError("empty apply command")
    result = subprocess.run(args, input=sql_text, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"apply command failed with exit code {result.returncode}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import the current Sveton semantic extraction snapshot into the Postgres KB schema.")
    parser.add_argument("--project-root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--config", default=None, help="Path to semantic_project.yml, relative to project root.")
    parser.add_argument("--out-dir", default="99_tmp/kb_import", help="Dry-run output directory, relative to project root.")
    parser.add_argument("--sql-output", default=None, help="Optional SQL output path, relative to project root.")
    parser.add_argument("--apply", action="store_true", help="Execute generated SQL through --apply-command or SVETON_KB_PSQL_COMMAND.")
    parser.add_argument("--apply-command", default=os.environ.get("SVETON_KB_PSQL_COMMAND"), help="Command that reads SQL from stdin and executes it.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    project_root = Path(args.project_root).resolve()
    config, paths = build_paths(project_root, args.config)

    required_paths = [
        paths.config_path,
        paths.inventory_path,
        paths.chunks_path,
        paths.statements_path,
        paths.clusters_path,
        paths.relations_path,
        paths.images_path,
        paths.statement_images_path,
        paths.coverage_report_path,
        paths.coverage_overrides_path,
    ]
    missing = [relpath(project_root, path) for path in required_paths if not path.exists()]
    if missing:
        for path in missing:
            print(f"Missing required artifact: {path}", file=sys.stderr)
        return 2

    snapshot = load_snapshot(project_root, paths)
    discrepancies = validate_snapshot(snapshot)
    source_git_commit = git_commit(project_root)
    hash_paths = [
        paths.inventory_path,
        paths.chunks_path,
        paths.statements_path,
        paths.clusters_path,
        paths.relations_path,
        paths.images_path,
        paths.statement_images_path,
        paths.coverage_report_path,
        paths.coverage_overrides_path,
    ]
    import_hash = artifact_hash(hash_paths)[:12]
    import_run_key = f"{config['corpus_id']}_{import_hash}"
    source_summary = build_source_summary(project_root, paths, snapshot, discrepancies, import_run_key, source_git_commit)

    out_dir = project_root / args.out_dir
    summary_path = out_dir / "import_summary.json"
    discrepancies_path = out_dir / "discrepancies.jsonl"
    sql_path = project_root / args.sql_output if args.sql_output else out_dir / "import.sql"

    write_json(summary_path, source_summary)
    write_jsonl(discrepancies_path, discrepancies)

    sql_text = build_sql(config, source_summary, snapshot, relpath(project_root, paths.config_path), import_run_key, source_git_commit)
    sql_path.parent.mkdir(parents=True, exist_ok=True)
    sql_path.write_text(sql_text, encoding="utf-8")

    error_count = sum(1 for row in discrepancies if row["severity"] == "error")
    warning_count = sum(1 for row in discrepancies if row["severity"] == "warning")
    print(f"Import run key: {import_run_key}")
    print(f"Summary: {relpath(project_root, summary_path)}")
    print(f"Discrepancies: {relpath(project_root, discrepancies_path)}")
    print(f"SQL: {relpath(project_root, sql_path)}")
    print(f"Rows: sources={len(snapshot['sources'])}, chunks={len(snapshot['chunks'])}, statements={len(snapshot['statements'])}, clusters={len(snapshot['clusters'])}, relations={len(snapshot['relations'])}, images={len(snapshot['images'])}, statement_images={len(snapshot['statement_images'])}")
    print(f"Discrepancies: errors={error_count}, warnings={warning_count}")

    if error_count:
        print("Import blocked because hard validation errors exist.", file=sys.stderr)
        return 1

    if args.apply:
        if not args.apply_command:
            print("--apply requires --apply-command or SVETON_KB_PSQL_COMMAND.", file=sys.stderr)
            return 2
        apply_sql(sql_text, args.apply_command)
        print("Applied SQL successfully.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
