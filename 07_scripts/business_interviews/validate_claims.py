#!/usr/bin/env python3
"""Validate business interview claims and build review/coverage reports."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CLAIM_SCHEMA = ROOT / "00_input/interviews/statements/interview_claim.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows)
    path.write_text(text + ("\n" if text else ""), encoding="utf-8")


def enum(schema: dict[str, Any], field: str) -> set[str]:
    return set(schema["properties"][field]["enum"])


def item_enum(schema: dict[str, Any], field: str) -> set[str]:
    return set(schema["properties"][field]["items"]["enum"])


def validate_claims(
    claims: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
    extraction_results: list[dict[str, Any]],
    schema: dict[str, Any],
) -> tuple[list[str], list[str], list[dict[str, Any]], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    review_items: list[dict[str, Any]] = []

    chunks_by_id = {chunk["chunk_id"]: chunk for chunk in chunks}
    claim_required = set(schema["required"])
    allowed_claim_type = enum(schema, "claim_type")
    allowed_business_area = enum(schema, "business_area")
    allowed_mapping = enum(schema, "speaker_mapping_confidence")
    allowed_evidence = enum(schema, "evidence_status")
    allowed_confidence = enum(schema, "confidence")
    allowed_review_status = enum(schema, "review_status")
    allowed_target_outputs = item_enum(schema, "target_outputs")
    allowed_review_flags = item_enum(schema, "review_flags")
    allowed_electricians = enum(schema, "applicability_to_electricians_kb")
    schema_fields = set(schema["properties"])

    claim_ids = [claim.get("claim_id", "") for claim in claims]
    for claim_id, count in Counter(claim_ids).items():
        if count > 1:
            errors.append(f"duplicate claim_id: {claim_id}")

    id_pattern = re.compile(r"^interview_claim_[0-9]{6}$")
    chunk_pattern = re.compile(r"^interview_[0-9]{3}_chunk_[0-9]{4}$")
    speaker_pattern = re.compile(r"^SPEAKER_[0-9]{2}$")
    timestamp_pattern = re.compile(r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$")

    result_chunks = {result["source_chunk_id"] for result in extraction_results}

    for index, claim in enumerate(claims, 1):
        claim_id = claim.get("claim_id", f"row_{index}")
        missing = sorted(claim_required - set(claim))
        if missing:
            errors.append(f"{claim_id}: missing required fields: {', '.join(missing)}")

        extra = sorted(set(claim) - schema_fields)
        if extra:
            errors.append(f"{claim_id}: unknown fields: {', '.join(extra)}")

        if not id_pattern.match(str(claim.get("claim_id", ""))):
            errors.append(f"{claim_id}: invalid claim_id")
        if not chunk_pattern.match(str(claim.get("source_chunk_id", ""))):
            errors.append(f"{claim_id}: invalid source_chunk_id")
        if not speaker_pattern.match(str(claim.get("speaker_label", ""))):
            errors.append(f"{claim_id}: invalid speaker_label")
        if not timestamp_pattern.match(str(claim.get("start_timestamp", ""))):
            errors.append(f"{claim_id}: invalid start_timestamp")
        if not timestamp_pattern.match(str(claim.get("end_timestamp", ""))):
            errors.append(f"{claim_id}: invalid end_timestamp")

        scalar_checks = {
            "claim_type": allowed_claim_type,
            "business_area": allowed_business_area,
            "speaker_mapping_confidence": allowed_mapping,
            "applicability_to_electricians_kb": allowed_electricians,
            "evidence_status": allowed_evidence,
            "confidence": allowed_confidence,
            "review_status": allowed_review_status,
        }
        for field, allowed in scalar_checks.items():
            if claim.get(field) not in allowed:
                errors.append(f"{claim_id}: invalid {field}: {claim.get(field)}")

        for output in claim.get("target_outputs", []):
            if output not in allowed_target_outputs:
                errors.append(f"{claim_id}: invalid target_output: {output}")
        if len(claim.get("target_outputs", [])) != len(set(claim.get("target_outputs", []))):
            errors.append(f"{claim_id}: duplicate target_outputs")

        for flag in claim.get("review_flags", []):
            if flag not in allowed_review_flags:
                errors.append(f"{claim_id}: invalid review_flag: {flag}")
        if len(claim.get("review_flags", [])) != len(set(claim.get("review_flags", []))):
            errors.append(f"{claim_id}: duplicate review_flags")

        source_chunk_id = claim.get("source_chunk_id")
        source_chunk = chunks_by_id.get(source_chunk_id)
        if not source_chunk:
            errors.append(f"{claim_id}: source chunk not found: {source_chunk_id}")
        elif claim.get("source_quote", "") not in source_chunk.get("text", ""):
            errors.append(f"{claim_id}: source_quote is not an exact contiguous fragment of source chunk")

        if source_chunk_id not in result_chunks:
            warnings.append(f"{claim_id}: source chunk has no extraction result record")

        if claim.get("speaker_identity") == "needs_mapping" or claim.get("speaker_role") == "needs_mapping":
            if claim.get("review_status") != "review_required":
                errors.append(f"{claim_id}: needs_mapping speaker must be review_required")
            if "speaker_mapping_required" not in claim.get("review_flags", []):
                errors.append(f"{claim_id}: needs_mapping speaker must carry speaker_mapping_required")

        if claim.get("claim_type") == "technical_claim_needs_confirmation":
            if claim.get("applicability_to_electricians_kb") != "needs_confirmation":
                errors.append(f"{claim_id}: technical claim must set applicability_to_electricians_kb=needs_confirmation")
            if "technical_confirmation_required" not in claim.get("review_flags", []):
                errors.append(f"{claim_id}: technical claim must carry technical_confirmation_required")
            if claim.get("review_status") != "review_required":
                errors.append(f"{claim_id}: technical claim must be review_required")

        if claim.get("applicability_to_electricians_kb") == "needs_confirmation":
            if "technical_confirmation_required" not in claim.get("review_flags", []):
                errors.append(f"{claim_id}: electricians needs_confirmation must carry technical_confirmation_required")

        if claim.get("claim_type") == "objection" and not claim.get("objection"):
            errors.append(f"{claim_id}: objection claim must fill objection object")
        if claim.get("claim_type") == "sales_case" and not claim.get("sales_case"):
            errors.append(f"{claim_id}: sales_case claim must fill sales_case object")
        if claim.get("claim_type") == "qualification_question" and not claim.get("discovery_question"):
            errors.append(f"{claim_id}: qualification_question must fill discovery_question object")
        if claim.get("claim_type") == "open_question":
            if not claim.get("open_question"):
                errors.append(f"{claim_id}: open_question claim must fill open_question object")
            if claim.get("evidence_status") != "open_question":
                errors.append(f"{claim_id}: open_question claim must set evidence_status=open_question")

        public_outputs = {"website", "brochure", "presentation", "commercial_messaging", "content_bank"}
        public_flags = {"marketing_claim_review", "public_use_review"}
        if public_outputs.intersection(claim.get("target_outputs", [])) and not public_flags.intersection(claim.get("review_flags", [])):
            warnings.append(f"{claim_id}: public/commercial output without marketing/public review flag")

        review_reasons = sorted(set(claim.get("review_flags", [])))
        if claim.get("review_status") == "review_required" and not review_reasons:
            review_reasons.append("review_status_required")
        if claim.get("confidence") == "low" and "low_confidence" not in review_reasons:
            review_reasons.append("low_confidence")
        if claim.get("speaker_identity") == "needs_mapping" and "speaker_mapping_required" not in review_reasons:
            review_reasons.append("speaker_mapping_required")
        if claim.get("claim_type") == "technical_claim_needs_confirmation" and "technical_confirmation_required" not in review_reasons:
            review_reasons.append("technical_confirmation_required")
        if claim.get("applicability_to_electricians_kb") == "needs_confirmation" and "technical_confirmation_required" not in review_reasons:
            review_reasons.append("technical_confirmation_required")

        if review_reasons:
            review_items.append(
                {
                    "claim_id": claim_id,
                    "source_interview_id": claim.get("source_interview_id", ""),
                    "source_chunk_id": claim.get("source_chunk_id", ""),
                    "review_reasons": review_reasons,
                    "claim": claim.get("claim", ""),
                    "source_quote": claim.get("source_quote", ""),
                    "review_owner": "business_owner",
                    "decision_status": "pending",
                    "decision_notes": "",
                }
            )

    chunk_ids_with_claims = {claim.get("source_chunk_id") for claim in claims}
    skipped_reason_counter: Counter[str] = Counter()
    for result in extraction_results:
        for skipped in result.get("skipped_source_items", []):
            skipped_reason_counter[skipped.get("reason", "unknown")] += 1

    coverage = {
        "run_id": "business_interviews_validation",
        "interviews": sorted({claim.get("source_interview_id", "") for claim in claims if claim.get("source_interview_id")}),
        "chunks_total": len(chunks),
        "chunks_with_claims": len(chunk_ids_with_claims),
        "claims_total": len(claims),
        "claims_by_type": dict(sorted(Counter(claim.get("claim_type", "") for claim in claims).items())),
        "claims_by_business_area": dict(sorted(Counter(claim.get("business_area", "") for claim in claims).items())),
        "claims_by_review_status": dict(sorted(Counter(claim.get("review_status", "") for claim in claims).items())),
        "review_flags": dict(sorted(Counter(flag for claim in claims for flag in claim.get("review_flags", [])).items())),
        "technical_confirmation_required": sum(
            "technical_confirmation_required" in claim.get("review_flags", []) for claim in claims
        ),
        "electricians_kb_relevant": sum(
            claim.get("applicability_to_electricians_kb") in {"directly_relevant", "needs_confirmation"}
            or "electricians_kb" in claim.get("target_outputs", [])
            for claim in claims
        ),
        "chunks_with_zero_claims": sorted(set(chunks_by_id) - chunk_ids_with_claims),
        "skipped_items_by_reason": dict(sorted(skipped_reason_counter.items())),
        "validation_errors": errors,
        "validation_warnings": warnings,
    }
    return errors, warnings, review_items, coverage


def write_review_queue(path: Path, review_items: list[dict[str, Any]]) -> None:
    lines = ["# Business interview review queue", ""]
    lines.append(f"Items: {len(review_items)}")
    lines.append("")
    for item in review_items:
        lines.extend(
            [
                f"## {item['claim_id']}",
                "",
                f"- Source: `{item['source_interview_id']}` / `{item['source_chunk_id']}`",
                f"- Reasons: {', '.join(item['review_reasons'])}",
                f"- Decision: `{item['decision_status']}`",
                "",
                f"Claim: {item['claim']}",
                "",
                "Source quote:",
                "",
                "```text",
                item["source_quote"],
                "```",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_coverage_report(path: Path, coverage: dict[str, Any]) -> None:
    def table(counter: dict[str, int]) -> list[str]:
        if not counter:
            return ["- none"]
        return [f"- `{key}`: {value}" for key, value in counter.items()]

    zero_claim_chunks = [f"- `{chunk_id}`" for chunk_id in coverage["chunks_with_zero_claims"]] or ["- none"]
    validation_errors = [f"- {error}" for error in coverage["validation_errors"]] or ["- none"]
    validation_warnings = [f"- {warning}" for warning in coverage["validation_warnings"]] or ["- none"]

    lines = [
        "# Business interview coverage report",
        "",
        f"- Interviews: {', '.join(coverage['interviews']) or 'none'}",
        f"- Chunks total: {coverage['chunks_total']}",
        f"- Chunks with claims: {coverage['chunks_with_claims']}",
        f"- Claims total: {coverage['claims_total']}",
        f"- Technical confirmation required: {coverage['technical_confirmation_required']}",
        f"- Electricians KB relevant/needs confirmation: {coverage['electricians_kb_relevant']}",
        f"- Validation errors: {len(coverage['validation_errors'])}",
        f"- Validation warnings: {len(coverage['validation_warnings'])}",
        "",
        "## Claims By Type",
        "",
        *table(coverage["claims_by_type"]),
        "",
        "## Claims By Business Area",
        "",
        *table(coverage["claims_by_business_area"]),
        "",
        "## Review Status",
        "",
        *table(coverage["claims_by_review_status"]),
        "",
        "## Review Flags",
        "",
        *table(coverage["review_flags"]),
        "",
        "## Skipped Items",
        "",
        *table(coverage["skipped_items_by_reason"]),
        "",
        "## Chunks With Zero Claims",
        "",
        *zero_claim_chunks,
        "",
        "## Validation Errors",
        "",
        *validation_errors,
        "",
        "## Validation Warnings",
        "",
        *validation_warnings,
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", required=True, type=Path)
    parser.add_argument("--chunks", required=True, type=Path)
    parser.add_argument("--extraction-results", required=True, type=Path)
    parser.add_argument("--review-queue-md", required=True, type=Path)
    parser.add_argument("--review-queue-jsonl", required=True, type=Path)
    parser.add_argument("--coverage-md", required=True, type=Path)
    parser.add_argument("--coverage-json", required=True, type=Path)
    args = parser.parse_args()

    schema = load_json(CLAIM_SCHEMA)
    claims = load_jsonl(args.claims)
    chunks = load_jsonl(args.chunks)
    extraction_results = load_jsonl(args.extraction_results)

    errors, warnings, review_items, coverage = validate_claims(claims, chunks, extraction_results, schema)
    coverage["source_claims_file"] = str(args.claims)
    coverage["source_chunks_file"] = str(args.chunks)

    write_jsonl(args.review_queue_jsonl, review_items)
    write_review_queue(args.review_queue_md, review_items)
    args.coverage_json.parent.mkdir(parents=True, exist_ok=True)
    args.coverage_json.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_coverage_report(args.coverage_md, coverage)

    print(f"claims={len(claims)}")
    print(f"review_items={len(review_items)}")
    print(f"errors={len(errors)}")
    print(f"warnings={len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
