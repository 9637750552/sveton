#!/usr/bin/env python3
"""Build semantic chunks for business interview_005."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = Path("00_input/interviews/260609_sveton_converted_t_large-v3_diar.txt")
OUTPUT_FILE = Path("00_input/interviews/chunks/interview_005_chunks.jsonl")
INTERVIEW_ID = "interview_005"


CHUNK_SPECS = [
    (1, 1, 10, "partner_workflow", "electrician_outreach_vs_foreman_sales_role", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (2, 11, 18, "qualification_discovery", "audit_instruction_prompt_and_power_calculation_basics", ["technical_claim_boundary", "strategy_claim_review"], "ready_for_extraction", ""),
    (3, 19, 26, "technical_explanation_needs_confirmation", "exclude_noncritical_loads_and_separate_reserve_lines", ["technical_claim_boundary", "marketing_claim_review"], "ready_for_extraction", ""),
    (4, 27, 45, "disagreement_clarification", "sergey_restates_audit_flow_and_manager_vs_electrician_roles", ["technical_claim_boundary", "strategy_claim_review"], "ready_for_extraction", ""),
    (5, 46, 61, "strategy_hypothesis", "cold_mvp_conversion_expectations_and_paid_inspection", ["strategy_claim_review", "marketing_claim_review"], "ready_for_extraction", ""),
    (6, 62, 74, "technical_explanation_needs_confirmation", "offer_after_interest_and_3_5_system_naming_confusion", ["technical_claim_boundary", "price_or_guarantee_review"], "ready_for_extraction", ""),
    (7, 75, 92, "technical_explanation_needs_confirmation", "nominal_power_peak_power_and_small_boiler_systems", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
]


TIMESTAMP_RE = re.compile(r"^\[(\d\d:\d\d:\d\d) - (\d\d:\d\d:\d\d)\]")
SPEAKER_RE = re.compile(r"\bSPEAKER_\d\d\b")


def parse_timestamp(line: str) -> tuple[str, str]:
    match = TIMESTAMP_RE.match(line)
    if not match:
        raise ValueError(f"Cannot parse timestamp from line: {line!r}")
    return match.group(1), match.group(2)


def build_chunks() -> list[dict]:
    source_path = ROOT / SOURCE_FILE
    lines = source_path.read_text(encoding="utf-8-sig").splitlines()
    chunks: list[dict] = []
    expected_start = 1

    for spec in CHUNK_SPECS:
        index, start_line, end_line, episode_type, topic, flags, status, exclude_reason = spec
        if start_line != expected_start:
            raise ValueError(f"Non-contiguous chunk at {index}: expected line {expected_start}, got {start_line}")
        if end_line > len(lines):
            raise ValueError(f"Chunk {index} ends at {end_line}, but source has {len(lines)} lines")

        selected = lines[start_line - 1 : end_line]
        start_timestamp, _ = parse_timestamp(selected[0])
        _, end_timestamp = parse_timestamp(selected[-1])
        speakers = sorted({speaker for line in selected for speaker in SPEAKER_RE.findall(line)})
        if not speakers:
            raise ValueError(f"Chunk {index} has no speaker labels")

        chunks.append(
            {
                "chunk_id": f"{INTERVIEW_ID}_chunk_{index:04d}",
                "source_interview_id": INTERVIEW_ID,
                "source_file": str(SOURCE_FILE),
                "chunk_index": index,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "start_line": start_line,
                "end_line": end_line,
                "speakers": speakers,
                "speaker_mapping_status": "confirmed",
                "episode_type": episode_type,
                "primary_topic": topic,
                "text": "\n".join(selected),
                "previous_chunk_id": f"{INTERVIEW_ID}_chunk_{index - 1:04d}" if index > 1 else None,
                "next_chunk_id": f"{INTERVIEW_ID}_chunk_{index + 1:04d}" if index < len(CHUNK_SPECS) else None,
                "overlap_previous": "sequential full-transcript chunk; no duplicated source lines",
                "overlap_next": "sequential full-transcript chunk; no duplicated source lines",
                "review_flags": flags,
                "chunk_status": status,
                "exclude_reason": exclude_reason,
                "notes": "full interview_005 chunking pass",
            }
        )
        expected_start = end_line + 1

    if expected_start != len(lines) + 1:
        raise ValueError(f"Uncovered tail: expected next line {expected_start}, source has {len(lines)} lines")
    return chunks


def main() -> None:
    output_path = ROOT / OUTPUT_FILE
    output_path.parent.mkdir(parents=True, exist_ok=True)
    chunks = build_chunks()
    with output_path.open("w", encoding="utf-8") as output:
        for chunk in chunks:
            output.write(json.dumps(chunk, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(chunks)} chunks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
