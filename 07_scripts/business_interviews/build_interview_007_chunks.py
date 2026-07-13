#!/usr/bin/env python3
"""Build semantic chunks for business interview_007."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = Path("00_input/interviews/260610_sveton_converted_t_large-v3_diar.txt")
OUTPUT_FILE = Path("00_input/interviews/chunks/interview_007_chunks.jsonl")
INTERVIEW_ID = "interview_007"


CHUNK_SPECS = [
    (1, 1, 35, "technical_explanation_needs_confirmation", "inverter_overload_and_bypass_question", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (2, 36, 64, "technical_explanation_needs_confirmation", "manual_bypass_inverter_battery_matching_and_voltage_limits", ["technical_claim_boundary", "price_or_guarantee_review"], "ready_for_extraction", ""),
    (3, 65, 87, "technical_explanation_needs_confirmation", "high_power_system_buses_and_70_percent_rule", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (4, 88, 113, "sales_explanation", "power_confusion_customer_language_and_indirect_discovery", ["technical_claim_boundary", "marketing_claim_review"], "ready_for_extraction", ""),
    (5, 114, 145, "qualification_discovery", "remote_estimate_before_site_visit_and_load_discovery", ["technical_claim_boundary", "strategy_claim_review"], "ready_for_extraction", ""),
    (6, 146, 188, "strategy_discussion", "electricians_stars_vs_conveyor_and_service_client_ownership", ["strategy_claim_review"], "ready_for_extraction", ""),
    (7, 189, 229, "strategy_discussion", "crm_documentation_broken_telephone_and_foreman_channel_limits", ["strategy_claim_review", "marketing_claim_review"], "ready_for_extraction", ""),
    (8, 230, 264, "strategy_discussion", "scale_construction_companies_foremen_and_outsourced_electricians", ["strategy_claim_review"], "ready_for_extraction", ""),
    (9, 265, 273, "strategy_hypothesis", "uberized_pool_of_orders_and_electricians", ["strategy_claim_review"], "ready_for_extraction", ""),
    (10, 274, 302, "technical_explanation_needs_confirmation", "boiler_transfer_delay_grounding_and_neutral_specifics", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (11, 303, 342, "customer_pain", "comfort_security_monitoring_and_real_buying_motivation", ["marketing_claim_review"], "ready_for_extraction", ""),
    (12, 343, 361, "product_operations", "technical_documentation_instructions_and_engineering_role", ["technical_claim_boundary"], "ready_for_extraction", ""),
    (13, 362, 389, "business_context", "installed_base_presentations_finmodels_and_generator_argument", ["strategy_claim_review", "price_or_guarantee_review"], "ready_for_extraction", ""),
    (14, 390, 420, "business_context", "b2b_materials_documentation_package_and_call_closing", ["strategy_claim_review", "marketing_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (15, 421, 436, "next_steps", "telegram_group_materials_and_first_regional_contact", ["strategy_claim_review"], "ready_for_extraction", ""),
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
                "notes": "full interview_007 chunking pass",
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
