#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import semantic_project_config as project_config


STATEMENT_ID_RE = re.compile(r"^(doc_[0-9]{3}_chunk_[0-9]{4}_stmt_[0-9]{3}|stmt_[0-9]{6})$")
DOCUMENT_ID_RE = re.compile(r"^doc_[0-9]{3}$")
CHUNK_ID_RE = re.compile(r"^doc_[0-9]{3}_chunk_[0-9]{4}$")
IMAGE_ID_RE = re.compile(r"^img_[0-9]{4}$")

REQUIRED_FIELDS = {
    "statement_id",
    "statement",
    "statement_type",
    "roles",
    "topic",
    "source_document_id",
    "source_file",
    "source_chunk_id",
    "section_path",
    "source_quote",
    "source_quote_is_exact",
    "related_image_ids",
    "visual_review_required",
    "risk_level",
    "confidence",
    "review_status",
    "scope",
    "condition",
    "action",
    "object",
    "normalized_terms",
    "extraction_notes",
}

STATEMENT_TYPES = {
    "definition",
    "requirement",
    "instruction_step",
    "checklist_item",
    "recommendation",
    "prohibition",
    "warning",
    "process_step",
    "qualification_criterion",
    "interview_signal",
    "reporting_requirement",
}

ROLES = {"installer", "electrician", "manager", "hq_engineer", "project_lead", "leader", "customer"}
TOPICS = {
    "basic_knowledge",
    "ups_components",
    "distribution_boards",
    "installation_process",
    "work_on_site",
    "service_visit",
    "photo_report",
    "installer_roles",
    "training_levels",
    "hiring_and_interview",
    "installation_request_check",
    "quality_control",
    "reporting",
    "safety",
    "unknown",
}
RISK_LEVELS = {"ordinary", "important", "safety_critical"}
CONFIDENCE = {"high", "medium", "low"}
REVIEW_STATUS = {"extracted", "review_required", "rejected"}
RESULT_REQUIRED_FIELDS = {"source_chunk_id", "coverage_summary", "skipped_source_items", "statements"}
COVERAGE_SUMMARY_REQUIRED_FIELDS = {
    "source_items_detected",
    "source_items_extracted",
    "source_items_skipped",
    "coverage_notes",
}
SKIPPED_SOURCE_ITEM_REQUIRED_FIELDS = {"source_item_quote", "source_item_type", "reason", "notes"}
SOURCE_ITEM_TYPES = {
    "heading",
    "instruction",
    "requirement",
    "table_row",
    "table_header",
    "example",
    "note",
    "empty",
    "context_only",
    "unknown",
}
SKIP_REASONS = {
    "duplicate",
    "heading",
    "not_atomic",
    "not_actionable",
    "table_header",
    "context_only",
    "image_only",
    "no_exact_quote",
    "unclear",
    "out_of_scope",
}


def load_chunks(project_root: Path, config: dict[str, str] | None = None) -> dict[str, dict[str, Any]]:
    active_config = config or project_config.load_project_config(project_root)
    chunks_path = project_config.config_path(project_root, active_config, "chunks")
    chunks: dict[str, dict[str, Any]] = {}
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            chunk = json.loads(line)
            chunks[chunk["chunk_id"]] = chunk
    return chunks


def validate_statement(statement: dict[str, Any], chunks: dict[str, dict[str, Any]], line_no: int) -> list[str]:
    errors: list[str] = []
    keys = set(statement)
    missing = REQUIRED_FIELDS - keys
    extra = keys - REQUIRED_FIELDS
    if missing:
        errors.append(f"line {line_no}: missing fields: {sorted(missing)}")
    if extra:
        errors.append(f"line {line_no}: extra fields: {sorted(extra)}")
    if missing:
        return errors

    if not isinstance(statement["statement_id"], str) or not STATEMENT_ID_RE.match(statement["statement_id"]):
        errors.append(f"line {line_no}: invalid statement_id")
    if not isinstance(statement["source_document_id"], str) or not DOCUMENT_ID_RE.match(statement["source_document_id"]):
        errors.append(f"line {line_no}: invalid source_document_id")
    if not isinstance(statement["source_chunk_id"], str) or not CHUNK_ID_RE.match(statement["source_chunk_id"]):
        errors.append(f"line {line_no}: invalid source_chunk_id")
    if statement["statement_type"] not in STATEMENT_TYPES:
        errors.append(f"line {line_no}: invalid statement_type")
    if statement["topic"] not in TOPICS:
        errors.append(f"line {line_no}: invalid topic")
    if statement["risk_level"] not in RISK_LEVELS:
        errors.append(f"line {line_no}: invalid risk_level")
    if statement["confidence"] not in CONFIDENCE:
        errors.append(f"line {line_no}: invalid confidence")
    if statement["review_status"] not in REVIEW_STATUS:
        errors.append(f"line {line_no}: invalid review_status")
    if statement["source_quote_is_exact"] is not True:
        errors.append(f"line {line_no}: source_quote_is_exact must be true")

    for field in ("statement", "source_file", "source_quote", "scope", "condition", "action", "object", "extraction_notes"):
        if not isinstance(statement[field], str):
            errors.append(f"line {line_no}: {field} must be string")
    for field in ("roles", "section_path", "related_image_ids", "normalized_terms"):
        if not isinstance(statement[field], list):
            errors.append(f"line {line_no}: {field} must be array")
    if not isinstance(statement["visual_review_required"], bool):
        errors.append(f"line {line_no}: visual_review_required must be boolean")

    roles = statement["roles"] if isinstance(statement["roles"], list) else []
    if not roles:
        errors.append(f"line {line_no}: roles must not be empty")
    for role in roles:
        if role not in ROLES:
            errors.append(f"line {line_no}: invalid role {role!r}")

    for image_id in statement["related_image_ids"] if isinstance(statement["related_image_ids"], list) else []:
        if not isinstance(image_id, str) or not IMAGE_ID_RE.match(image_id):
            errors.append(f"line {line_no}: invalid image id {image_id!r}")

    chunk = chunks.get(statement["source_chunk_id"])
    if not chunk:
        errors.append(f"line {line_no}: source_chunk_id not found")
        return errors

    if statement["source_document_id"] != chunk["source_document_id"]:
        errors.append(f"line {line_no}: source_document_id does not match chunk")
    if statement["source_file"] != chunk["source_file"]:
        errors.append(f"line {line_no}: source_file does not match chunk")

    source_quote = statement["source_quote"]
    if isinstance(source_quote, str) and source_quote not in chunk["text"]:
        errors.append(f"line {line_no}: source_quote is not an exact substring of chunk text")
    if isinstance(source_quote, str) and "[IMAGE:" in source_quote:
        errors.append(f"line {line_no}: source_quote must not be only an image marker")

    allowed_images = set(chunk.get("related_image_ids", []))
    excluded_images = set(chunk.get("excluded_image_ids", []))
    for image_id in statement["related_image_ids"]:
        if image_id not in allowed_images:
            errors.append(f"line {line_no}: related_image_id {image_id} is not allowed for chunk")
        if image_id in excluded_images:
            errors.append(f"line {line_no}: related_image_id {image_id} is excluded for chunk")

    if chunk.get("needs_review") and statement["review_status"] != "review_required":
        errors.append(f"line {line_no}: statement from review chunk must be review_required")
    if statement["risk_level"] == "safety_critical" and statement["review_status"] != "review_required":
        errors.append(f"line {line_no}: safety_critical statement must be review_required")

    return errors


def validate_chunk_result(result: dict[str, Any], chunks: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    keys = set(result)
    missing = RESULT_REQUIRED_FIELDS - keys
    extra = keys - RESULT_REQUIRED_FIELDS
    chunk_id = result.get("source_chunk_id", "<unknown>")
    prefix = f"chunk {chunk_id}:"

    if missing:
        errors.append(f"{prefix} missing result fields: {sorted(missing)}")
    if extra:
        errors.append(f"{prefix} extra result fields: {sorted(extra)}")
    if missing:
        return errors

    if not isinstance(result["source_chunk_id"], str) or not CHUNK_ID_RE.match(result["source_chunk_id"]):
        errors.append(f"{prefix} invalid source_chunk_id")
    chunk = chunks.get(result["source_chunk_id"])
    if not chunk:
        errors.append(f"{prefix} source_chunk_id not found")
        return errors

    statements = result["statements"]
    if not isinstance(statements, list):
        errors.append(f"{prefix} statements must be an array")
        statements = []

    coverage_summary = result["coverage_summary"]
    if not isinstance(coverage_summary, dict):
        errors.append(f"{prefix} coverage_summary must be an object")
        coverage_summary = {}
    else:
        coverage_keys = set(coverage_summary)
        coverage_missing = COVERAGE_SUMMARY_REQUIRED_FIELDS - coverage_keys
        coverage_extra = coverage_keys - COVERAGE_SUMMARY_REQUIRED_FIELDS
        if coverage_missing:
            errors.append(f"{prefix} missing coverage_summary fields: {sorted(coverage_missing)}")
        if coverage_extra:
            errors.append(f"{prefix} extra coverage_summary fields: {sorted(coverage_extra)}")

    for field in ("source_items_detected", "source_items_extracted", "source_items_skipped"):
        value = coverage_summary.get(field)
        if not isinstance(value, int) or value < 0:
            errors.append(f"{prefix} coverage_summary.{field} must be a non-negative integer")
    if not isinstance(coverage_summary.get("coverage_notes"), str):
        errors.append(f"{prefix} coverage_summary.coverage_notes must be a string")

    skipped_source_items = result["skipped_source_items"]
    if not isinstance(skipped_source_items, list):
        errors.append(f"{prefix} skipped_source_items must be an array")
        skipped_source_items = []

    for idx, item in enumerate(skipped_source_items, start=1):
        item_prefix = f"{prefix} skipped_source_items[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{item_prefix} must be an object")
            continue
        item_keys = set(item)
        item_missing = SKIPPED_SOURCE_ITEM_REQUIRED_FIELDS - item_keys
        item_extra = item_keys - SKIPPED_SOURCE_ITEM_REQUIRED_FIELDS
        if item_missing:
            errors.append(f"{item_prefix} missing fields: {sorted(item_missing)}")
        if item_extra:
            errors.append(f"{item_prefix} extra fields: {sorted(item_extra)}")
        if item_missing:
            continue

        source_item_quote = item["source_item_quote"]
        if not isinstance(source_item_quote, str) or not source_item_quote:
            errors.append(f"{item_prefix}.source_item_quote must be a non-empty string")
        elif source_item_quote not in chunk["text"]:
            errors.append(f"{item_prefix}.source_item_quote is not an exact substring of chunk text")
        if isinstance(source_item_quote, str) and "[IMAGE:" in source_item_quote:
            errors.append(f"{item_prefix}.source_item_quote must not be only an image marker")

        if item["source_item_type"] not in SOURCE_ITEM_TYPES:
            errors.append(f"{item_prefix}.source_item_type is invalid")
        if item["reason"] not in SKIP_REASONS:
            errors.append(f"{item_prefix}.reason is invalid")
        if not isinstance(item["notes"], str):
            errors.append(f"{item_prefix}.notes must be a string")

    detected = coverage_summary.get("source_items_detected")
    extracted = coverage_summary.get("source_items_extracted")
    skipped = coverage_summary.get("source_items_skipped")
    if isinstance(extracted, int) and extracted != len(statements):
        errors.append(f"{prefix} coverage_summary.source_items_extracted must equal statements count")
    if isinstance(skipped, int) and skipped != len(skipped_source_items):
        errors.append(f"{prefix} coverage_summary.source_items_skipped must equal skipped_source_items count")
    if isinstance(detected, int) and isinstance(extracted, int) and isinstance(skipped, int):
        if detected < extracted + skipped:
            errors.append(f"{prefix} coverage_summary.source_items_detected must be >= extracted + skipped")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: validate_atomic_statements.py <project_root> <statements_jsonl> [config_path]", file=sys.stderr)
        return 1

    project_root = Path(argv[1]).resolve()
    statements_path = (project_root / argv[2]).resolve()
    config = project_config.load_project_config(project_root, argv[3] if len(argv) > 3 else None)
    chunks = load_chunks(project_root, config)

    total = 0
    errors: list[str] = []
    seen_ids: set[str] = set()
    with statements_path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            total += 1
            try:
                statement = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc}")
                continue
            statement_id = statement.get("statement_id")
            if statement_id in seen_ids:
                errors.append(f"line {line_no}: duplicate statement_id {statement_id}")
            seen_ids.add(statement_id)
            errors.extend(validate_statement(statement, chunks, line_no))

    if errors:
        print(f"INVALID: {len(errors)} errors in {total} statements")
        for error in errors:
            print(error)
        return 1

    print(f"VALID: {total} statements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
