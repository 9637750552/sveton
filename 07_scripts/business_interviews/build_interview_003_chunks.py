#!/usr/bin/env python3
"""Build semantic chunks for business interview_003."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = Path("00_input/interviews/260408_sveton3_converted_t_large-v3_diar.txt")
OUTPUT_FILE = Path("00_input/interviews/chunks/interview_003_chunks.jsonl")
INTERVIEW_ID = "interview_003"


CHUNK_SPECS = [
    (1, 1, 18, "technical_explanation_needs_confirmation", "inverter_types_and_double_conversion_basics", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (2, 19, 39, "technical_explanation_needs_confirmation", "double_conversion_disadvantages_and_stabilizer_alternative", ["technical_claim_boundary", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (3, 40, 58, "technical_explanation_needs_confirmation", "instab_stabilizer_and_noise_objection", ["technical_claim_boundary", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (4, 59, 71, "operations_process", "labor_market_mobilization_and_installer_hiring", ["strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (5, 72, 95, "operations_process", "engineer_roles_technical_director_and_object_work", ["strategy_claim_review", "technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (6, 96, 115, "technical_explanation_needs_confirmation", "reserve_group_power_limit_and_load_separation", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (7, 116, 134, "sales_process", "first_call_discovery_offer_sizing_and_mounting", ["marketing_claim_review", "technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (8, 135, 154, "sales_process", "when_to_explain_wiring_complexity_and_puppy_effect", ["marketing_claim_review", "technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (9, 155, 180, "sales_process", "manager_training_base_kit_bypass_and_price_framing", ["marketing_claim_review", "technical_claim_boundary", "strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (10, 181, 193, "sales_process", "communication_channel_and_discount_framing", ["marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (11, 194, 215, "technical_explanation_needs_confirmation", "inspection_hidden_loads_and_automatic_breakers", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (12, 216, 240, "qualification_discovery", "first_call_load_estimation_and_backup_duration", ["technical_claim_boundary", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (13, 241, 264, "technical_explanation_needs_confirmation", "measuring_loads_and_shleif_wiring_limitations", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (14, 265, 305, "technical_explanation_needs_confirmation", "actual_breaker_tail_fridge_boiler_room_and_phase_constraints", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (15, 306, 324, "sales_process", "manager_ramp_complexity_and_installation_site_constraints", ["marketing_claim_review", "technical_claim_boundary", "strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (16, 325, 352, "operations_process", "manager_profile_sales_skill_a4_offer_and_retention", ["strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (17, 353, 379, "customer_segment_claim", "customer_age_gender_gas_vs_electric_heating", ["strategy_claim_review", "marketing_claim_review", "technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (18, 380, 397, "technical_explanation_needs_confirmation", "battery_capacity_cost_and_freezing_pain", ["technical_claim_boundary", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (19, 398, 421, "technical_explanation_needs_confirmation", "starting_currents_and_peak_loads", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
    (20, 422, 448, "technical_explanation_needs_confirmation", "inverter_overload_restart_and_group_shutdown_explanation", ["technical_claim_boundary", "recognition_noise"], "ready_for_extraction", ""),
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

        chunk_id = f"{INTERVIEW_ID}_chunk_{index:04d}"
        chunks.append(
            {
                "chunk_id": chunk_id,
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
                "notes": "full interview_003 chunking pass",
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
