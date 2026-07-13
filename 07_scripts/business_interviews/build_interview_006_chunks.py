#!/usr/bin/env python3
"""Build semantic chunks for business interview_006."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = Path("00_input/interviews/260609_sveton_2_converted_t_large-v3_diar.txt")
OUTPUT_FILE = Path("00_input/interviews/chunks/interview_006_chunks.jsonl")
INTERVIEW_ID = "interview_006"


CHUNK_SPECS = [
    (1, 1, 5, "marketing_message", "upsell_from_3_4_to_5_4_and_reserve_wording", ["marketing_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (2, 6, 24, "technical_explanation_needs_confirmation", "appliance_peak_power_and_70_percent_nominal_rule", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (3, 25, 34, "technical_explanation_needs_confirmation", "offline_ups_relay_switching", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (4, 35, 45, "technical_explanation_needs_confirmation", "online_vs_offline_ups_tradeoffs", ["technical_claim_boundary", "price_or_guarantee_review"], "ready_for_extraction", ""),
    (5, 46, 81, "technical_explanation_needs_confirmation", "simultaneous_start_and_peak_capacity", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (6, 82, 105, "operational_walkthrough", "load_tab_auto_calculation_and_reference_database_idea", ["technical_claim_boundary", "strategy_claim_review"], "ready_for_extraction", ""),
    (7, 106, 160, "operational_walkthrough", "one_c_access_and_load_print_navigation", ["recognition_noise"], "ready_for_extraction", ""),
    (8, 161, 199, "operational_walkthrough", "finding_customer_questionnaire_in_one_c", ["recognition_noise"], "ready_for_extraction", ""),
    (9, 200, 238, "operational_walkthrough", "load_table_fields_and_auto_calculated_system_parameters", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (10, 239, 261, "operational_walkthrough", "device_names_are_generic_and_audit_corrects_client_words", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (11, 262, 320, "sales_process_walkthrough", "commercial_offer_variants_and_create_cp_flow", ["marketing_claim_review"], "ready_for_extraction", ""),
    (12, 321, 360, "sales_process_walkthrough", "preliminary_cp_before_audit_and_manager_role", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (13, 361, 395, "operational_walkthrough", "electrician_inspection_photos_and_installation_place", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (14, 396, 440, "operational_walkthrough", "final_cp_customer_order_contract_and_installer_task", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (15, 441, 486, "partner_workflow", "installer_card_training_and_no_client_talk_rule", ["technical_claim_boundary", "strategy_claim_review"], "ready_for_extraction", ""),
    (16, 487, 506, "operational_walkthrough", "safe_navigation_in_live_one_c_and_sergey_next_steps", ["strategy_claim_review"], "ready_for_extraction", ""),
    (17, 507, 538, "strategy_hypothesis", "regional_specialist_model_vadik_and_next_action", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
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
                "notes": "full interview_006 chunking pass",
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
