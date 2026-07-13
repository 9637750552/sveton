#!/usr/bin/env python3
"""Render a human-readable grouped review for interview claims."""

from __future__ import annotations

import json
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLAIMS_PATH = ROOT / "00_input/interviews/statements/interview_001_claims.jsonl"
OUT_PATH = ROOT / "00_input/interviews/review/interview_001_claims_review.md"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def short_quote(text: str, limit: int = 260) -> str:
    text = text.replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "..."


def reasons(claim: dict) -> str:
    return ", ".join(claim["review_flags"]) if claim["review_flags"] else claim["review_status"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", type=Path, default=CLAIMS_PATH)
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--title", default="Interview 001 claims review")
    parser.add_argument("--interview-id", default="interview_001")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    claims_path = args.claims if args.claims.is_absolute() else ROOT / args.claims
    out_path = args.out if args.out.is_absolute() else ROOT / args.out
    claims = load_jsonl(claims_path)

    groups = [
        (
            "Филиалы и стратегия",
            {
                "interview_claim_001001",
                "interview_claim_001002",
                "interview_claim_001003",
                "interview_claim_001015",
                "interview_claim_001016",
                "interview_claim_001017",
                "interview_claim_001018",
                "interview_claim_001028",
                "interview_claim_001033",
                "interview_claim_001057",
                "interview_claim_001062",
                "interview_claim_001088",
            },
        ),
        ("Прорабы и партнерский канал", None),
        ("Боли клиента и ценность", None),
        ("Генератор и возражения", None),
        (
            "Мониторинг и обратная связь",
            {
                "interview_claim_001046",
                "interview_claim_001047",
                "interview_claim_001048",
                "interview_claim_001049",
                "interview_claim_001050",
                "interview_claim_001051",
                "interview_claim_001052",
                "interview_claim_001053",
                "interview_claim_001057",
                "interview_claim_001058",
                "interview_claim_001059",
                "interview_claim_001060",
                "interview_claim_001061",
                "interview_claim_001062",
                "interview_claim_001063",
                "interview_claim_001064",
                "interview_claim_001065",
                "interview_claim_001066",
            },
        ),
        ("Продажи, pitch и позиционирование", None),
        (
            "Операции, 1С и Planada",
            {
                "interview_claim_001076",
                "interview_claim_001077",
                "interview_claim_001078",
                "interview_claim_001079",
                "interview_claim_001080",
            },
        ),
        (
            "Разработки и техграница",
            {
                "interview_claim_001024",
                "interview_claim_001025",
                "interview_claim_001026",
                "interview_claim_001040",
                "interview_claim_001045",
                "interview_claim_001069",
                "interview_claim_001070",
                "interview_claim_001071",
                "interview_claim_001072",
                "interview_claim_001081",
                "interview_claim_001082",
                "interview_claim_001083",
                "interview_claim_001084",
                "interview_claim_001085",
                "interview_claim_001086",
                "interview_claim_001087",
            },
        ),
    ]

    area_groups = {
        "Прорабы и партнерский канал": {"partner_model"},
        "Боли клиента и ценность": {"customer_pain", "value_proposition", "customer_segment"},
        "Генератор и возражения": {"objection_handling"},
        "Продажи, pitch и позиционирование": {"sales_process", "positioning", "qualification"},
    }

    assigned: set[str] = set()
    sections: list[tuple[str, list[dict]]] = []

    for title, ids in groups:
        if ids is not None:
            items = [claim for claim in claims if claim["claim_id"] in ids]
        else:
            areas = area_groups[title]
            items = [claim for claim in claims if claim["business_area"] in areas and claim["claim_id"] not in assigned]
        items = sorted(items, key=lambda claim: claim["claim_id"])
        if not items:
            continue
        assigned.update(claim["claim_id"] for claim in items)
        sections.append((title, items))

    rest = sorted([claim for claim in claims if claim["claim_id"] not in assigned], key=lambda claim: claim["claim_id"])
    if rest:
        sections.append(("Остальное", rest))

    lines = [
        f"# {args.title}",
        "",
        f"Всего claims: {len(claims)}",
        "",
        f"> Это человекочитаемое представление полного прогона `{args.interview_id}`. Источник истины для дальнейшей обработки — `{claims_path.name}`.",
        "",
        "## Как смотреть",
        "",
        "1. Сначала прочитать тематические блоки ниже.",
        "2. Если claim выглядит спорным, открыть `claim_id` в `interview_001_review_queue.md`.",
        "3. Полный JSON нужен только для машинной обработки и последующего clustering.",
        "",
    ]

    for title, items in sections:
        lines.append(f"## {title}")
        lines.append("")
        for claim in items:
            lines.append(f"### {claim['claim_id']}")
            lines.append("")
            lines.append(f"- Тип: `{claim['claim_type']}`")
            lines.append(f"- Chunk: `{claim['source_chunk_id']}`")
            lines.append(f"- Review: {reasons(claim)}")
            lines.append(f"- Claim: {claim['claim']}")
            lines.append(f"- Цитата: {short_quote(claim['source_quote'])}")
            lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
