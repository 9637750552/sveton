#!/usr/bin/env python3
"""Build semantic chunks for business interview_004."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = Path("00_input/interviews/260408_sveton4_converted_t_large-v3_diar.txt")
OUTPUT_FILE = Path("00_input/interviews/chunks/interview_004_chunks.jsonl")
INTERVIEW_ID = "interview_004"


CHUNK_SPECS = [
    (1, 1, 10, "noise_or_transition", "schedule_and_session_continuation_setup", [], "excluded", "служебное обсуждение продолжительности разговора"),
    (2, 11, 30, "strategy_hypothesis", "regional_market_test_first_contact_and_handoff", ["strategy_claim_review", "marketing_claim_review", "technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (3, 31, 49, "strategy_hypothesis", "audience_diversification_intermediaries_and_local_staff_gap", ["strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (4, 50, 80, "customer_case", "smb_private_testing_stomatology_tea_line_and_pellet_case", ["strategy_claim_review", "marketing_claim_review", "technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (5, 81, 112, "technical_explanation_needs_confirmation", "pellet_boiler_small_systems_bms_market_reputation_and_ventilation", ["technical_claim_boundary", "marketing_claim_review", "strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (6, 113, 132, "strategy_hypothesis", "priority_segments_private_smb_and_intermediaries", ["strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (7, 133, 139, "noise_or_transition", "time_transition_before_final_topic", [], "excluded", "служебный переход"),
    (8, 140, 155, "risk_or_constraint", "critical_medical_infrastructure_no_go_boundary", ["technical_claim_boundary", "strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (9, 156, 199, "product_explanation", "server_backup_double_conversion_and_shutdown_protocol", ["technical_claim_boundary", "marketing_claim_review", "strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (10, 200, 210, "strategy_hypothesis", "market_potential_test_and_agent_relationship", ["strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (11, 211, 224, "partner_workflow", "krasnodar_regional_intermediaries_and_agent_contract", ["strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (12, 225, 236, "business_model_claim", "discounts_lithium_margin_and_price_positioning", ["strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (13, 237, 270, "operations_process", "regional_installer_training_documentation_logistics_and_stand", ["technical_claim_boundary", "strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (14, 271, 307, "partner_workflow", "regional_electricians_contractors_staff_installers_and_quality_risk", ["technical_claim_boundary", "strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (15, 308, 348, "operations_process", "foreman_electrician_model_quality_control_and_visual_instruction", ["technical_claim_boundary", "strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (16, 349, 419, "mixed", "offtopic_camping_business_model_and_possible_electrician_overlap", ["mixed_topics", "manual_split_recommended", "strategy_claim_review", "recognition_noise"], "needs_review", "off-topic camping business discussion with minor possible electrician-staffing overlap"),
    (17, 420, 496, "noise_or_transition", "offtopic_camping_rules_market_history_and_close", [], "excluded", "отдельная тема кемпинга, не источник для Sveton Business KB"),
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
                "notes": "full interview_004 chunking pass",
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
