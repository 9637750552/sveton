#!/usr/bin/env python3
"""Build semantic chunks for business interview_002."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = Path("00_input/interviews/260405_sveton_2_converted_t_large-v3_diar.txt")
OUTPUT_FILE = Path("00_input/interviews/chunks/interview_002_chunks.jsonl")
INTERVIEW_ID = "interview_002"


CHUNK_SPECS = [
    (1, 1, 11, "noise_or_transition", "screen_share_setup", [], "excluded", "служебная настройка экрана перед началом содержательного интервью"),
    (2, 12, 21, "question_answer", "private_home_customer_profile", ["marketing_claim_review"], "ready_for_extraction", ""),
    (3, 22, 33, "technical_explanation_needs_confirmation", "electrical_safety_boundary", ["technical_claim_boundary", "marketing_claim_review"], "ready_for_extraction", ""),
    (4, 34, 45, "sales_process", "decision_makers_referrals_and_settlement_chats", ["marketing_claim_review"], "ready_for_extraction", ""),
    (5, 46, 49, "objection_response", "generator_objection", ["marketing_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (6, 50, 70, "customer_case", "winlab_outage_cold_outreach_case", ["strategy_claim_review", "recognition_noise"], "ready_for_extraction", ""),
    (7, 71, 82, "customer_case", "egypt_retail_outage_case", ["strategy_claim_review"], "ready_for_extraction", ""),
    (8, 83, 114, "market_context", "smb_segments_and_large_business_limits", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (9, 115, 126, "question_answer", "smb_ticket_decision_makers_and_sales_difference", ["strategy_claim_review"], "ready_for_extraction", ""),
    (10, 127, 140, "strategy_hypothesis", "regional_smb_focus_and_trust", ["strategy_claim_review", "marketing_claim_review"], "ready_for_extraction", ""),
    (11, 141, 157, "objection_response", "smb_pain_risks_generator_economics_and_sizing_errors", ["marketing_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (12, 158, 186, "product_explanation", "offer_service_model_product_lines_and_repeat_sales", ["marketing_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (13, 187, 199, "sales_process", "expertise_customer_journey_and_lead_channels", ["marketing_claim_review"], "ready_for_extraction", ""),
    (14, 200, 228, "sales_process", "lead_volume_conversion_and_sales_staffing", ["strategy_claim_review"], "ready_for_extraction", ""),
    (15, 229, 258, "operations_process", "manager_workload_duty_queue_and_one_click_offer", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (16, 259, 286, "operations_process", "inspection_documentation_visit_capacity_and_installation_teams", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (17, 287, 300, "operations_process", "technical_calculation_project_flow_and_payment_rules", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (18, 301, 324, "question_answer", "expense_structure_capex_and_operating_costs", ["strategy_claim_review"], "ready_for_extraction", ""),
    (19, 325, 349, "strategy_hypothesis", "growth_constraints_market_pyramid_and_segment_choice", ["strategy_claim_review"], "ready_for_extraction", ""),
    (20, 350, 365, "strategy_hypothesis", "horizontal_scaling_branches_and_adjacent_markets", ["strategy_claim_review"], "ready_for_extraction", ""),
    (21, 366, 405, "market_context", "competitors_distributors_brand_quality_and_lost_deals", ["strategy_claim_review", "marketing_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (22, 406, 420, "strategy_hypothesis", "copy_protection_advertising_reputation_and_smb_company", ["strategy_claim_review"], "ready_for_extraction", ""),
    (23, 421, 443, "strategy_hypothesis", "partner_ownership_and_new_smb_business_boundary", ["strategy_claim_review"], "ready_for_extraction", ""),
    (24, 444, 466, "question_answer", "revenue_margin_projects_low_season_and_seasonality_buffer", ["strategy_claim_review"], "ready_for_extraction", ""),
    (25, 467, 478, "strategy_hypothesis", "smb_seasonality_growth_rates_and_staff_count", ["strategy_claim_review"], "ready_for_extraction", ""),
    (26, 479, 495, "strategy_hypothesis", "three_year_vision_products_stabilizers_and_oem", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (27, 496, 516, "strategy_hypothesis", "regional_location_service_radius_and_scaling_model", ["strategy_claim_review"], "ready_for_extraction", ""),
    (28, 517, 529, "operations_process", "engineering_capacity_manager_hiring_and_june_decision", ["strategy_claim_review"], "ready_for_extraction", ""),
    (29, 530, 538, "strategy_hypothesis", "priority_development_regions_and_ikea_like_product", ["strategy_claim_review", "technical_claim_boundary"], "ready_for_extraction", ""),
    (30, 539, 545, "decision_summary", "next_interview_ai_agents_and_lead_warming", ["strategy_claim_review"], "ready_for_extraction", ""),
    (31, 546, 551, "sales_process", "vk_social_warming_and_retargeting", ["marketing_claim_review", "strategy_claim_review"], "ready_for_extraction", ""),
    (32, 552, 562, "decision_summary", "closing_and_follow_up_lead_check", [], "ready_for_extraction", ""),
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
        previous_chunk_id = f"{INTERVIEW_ID}_chunk_{index - 1:04d}" if index > 1 else None
        next_chunk_id = f"{INTERVIEW_ID}_chunk_{index + 1:04d}" if index < len(CHUNK_SPECS) else None

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
                "previous_chunk_id": previous_chunk_id,
                "next_chunk_id": next_chunk_id,
                "overlap_previous": "sequential full-transcript chunk; no duplicated source lines",
                "overlap_next": "sequential full-transcript chunk; no duplicated source lines",
                "review_flags": flags,
                "chunk_status": status,
                "exclude_reason": exclude_reason,
                "notes": "full interview_002 chunking pass",
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
