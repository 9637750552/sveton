#!/usr/bin/env python3
"""Build business-interview claim clusters and relations."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CLAIMS_PATH = ROOT / "00_input/interviews/statements/interview_corpus_claims.jsonl"
OUT_CLUSTERS = ROOT / "00_input/interviews/statements/statement_clusters.json"
OUT_CLUSTERS_MD = ROOT / "00_input/interviews/statements/statement_clusters.md"
OUT_RELATIONS = ROOT / "00_input/interviews/statements/statement_relations.jsonl"

ALLOWED_RELATIONS = {
    "duplicate_of",
    "supports",
    "refines",
    "contradicts",
    "example_of",
    "context_for",
    "requires_technical_confirmation",
    "derived_marketing_message_for",
}

CLUSTERS: list[dict[str, Any]] = [
    {
        "cluster_id": "BIC001",
        "title": "Бизнес-модель и сервисное позиционирование",
        "topic": "business_model_service_positioning",
        "primary_outputs": ["business_kb", "business_model_map", "presentation"],
        "coverage": "Что продает Светон: услуга, сервисная модель, клиентские отношения, гарантийное обслуживание, отличие от продажи железа.",
    },
    {
        "cluster_id": "BIC002",
        "title": "Клиентские сегменты и ситуации покупки",
        "topic": "customer_segments",
        "primary_outputs": ["business_kb", "sales_playbook", "website_content_bank"],
        "coverage": "Частные дома, SMB, строительные компании, прорабы, ЛПР и разные моменты возникновения потребности.",
    },
    {
        "cluster_id": "BIC003",
        "title": "Боли клиента и ценность продукта",
        "topic": "customer_pains_value_proposition",
        "primary_outputs": ["sales_playbook", "commercial_messaging", "website_content_bank"],
        "coverage": "Комфорт, безопасность, разморозка, вода, интернет, спокойствие клиента и ценностные формулировки.",
    },
    {
        "cluster_id": "BIC004",
        "title": "Продуктовая логика, мощность и резерв",
        "topic": "product_package_sizing",
        "primary_outputs": ["manager_training", "sales_training", "commercial_messaging"],
        "coverage": "Инвертор, аккумуляторы, мощность, пиковые нагрузки, время резерва, типовые потребители и подбор конфигурации.",
    },
    {
        "cluster_id": "BIC005",
        "title": "Технические edge cases и границы подтверждения",
        "topic": "technical_edge_cases_review",
        "primary_outputs": ["review_only", "links_to_electricians_kb"],
        "coverage": "Монтажные и электрические нюансы из интервью: щиты, фазы, байпас, заземление, зануление, место установки, превышение нагрузки.",
    },
    {
        "cluster_id": "BIC006",
        "title": "Генератор, стабилизатор и типы ИБП",
        "topic": "generator_stabilizer_ups_comparisons",
        "primary_outputs": ["objection_handling", "sales_training", "commercial_messaging"],
        "coverage": "Сравнения с генераторами, стабилизаторами, online/offline/line-interactive ИБП и двойным преобразованием.",
    },
    {
        "cluster_id": "BIC007",
        "title": "Продажный процесс, КП и сделка",
        "topic": "sales_process",
        "primary_outputs": ["sales_playbook", "manager_training", "commercial_messaging"],
        "coverage": "Воронка, предварительное и финальное КП, цены, скидки, договор, заказ покупателя, отправка клиенту.",
    },
    {
        "cluster_id": "BIC008",
        "title": "Квалификация и discovery-вопросы",
        "topic": "qualification_discovery",
        "primary_outputs": ["sales_script", "manager_training", "sales_playbook"],
        "coverage": "Вопросы к клиенту, косвенные признаки, сбор нагрузок, режимы работы, бюджет, решение о выезде.",
    },
    {
        "cluster_id": "BIC009",
        "title": "Возражения и рекомендуемые ответы",
        "topic": "objection_handling",
        "primary_outputs": ["objection_handling", "sales_training", "sales_script"],
        "coverage": "Возражения клиентов, ответы, спорные коммерческие тезисы и аргументация менеджера.",
    },
    {
        "cluster_id": "BIC010",
        "title": "Электрики, монтажники и партнерская модель",
        "topic": "electrician_installer_partner_model",
        "primary_outputs": ["business_kb", "manager_training", "strategy"],
        "coverage": "Роли электриков и монтажников, аудит, выезд, обучение, аутсорс, контроль, ограничения передачи клиентского разговора.",
    },
    {
        "cluster_id": "BIC011",
        "title": "Прорабы, строители и партнерские каналы",
        "topic": "foremen_builders_channels",
        "primary_outputs": ["strategy", "business_kb", "sales_playbook"],
        "coverage": "Прорабы, строительные компании, девелоперы, модульные дома и ограниченность каналов через стройку.",
    },
    {
        "cluster_id": "BIC012",
        "title": "Роли менеджера, специалиста и обучение",
        "topic": "manager_training_roles",
        "primary_outputs": ["manager_training", "sales_training"],
        "coverage": "Что должен делать менеджер/специалист, где нужен технический специалист, как обучать и заменять людей.",
    },
    {
        "cluster_id": "BIC013",
        "title": "CRM, 1C, документация и операционный учет",
        "topic": "crm_one_c_operations",
        "primary_outputs": ["manager_training", "business_kb", "operations"],
        "coverage": "1C, CRM, анкеты, нагрузки, карточки, задания, записи разговоров, документация, отчеты и материалы.",
    },
    {
        "cluster_id": "BIC014",
        "title": "Сервис, качество, мониторинг и обратная связь",
        "topic": "service_quality_monitoring",
        "primary_outputs": ["business_kb", "manager_training", "commercial_messaging"],
        "coverage": "Качество сервиса, гарантийные случаи, мониторинг, SMS, постпродажа, отзывы, репутация.",
    },
    {
        "cluster_id": "BIC015",
        "title": "Региональная экспансия и южный филиал",
        "topic": "regional_expansion",
        "primary_outputs": ["strategy", "business_model_map", "manager_training"],
        "coverage": "Южный филиал, Краснодар, Горячий Ключ, региональный MVP, Вадик, локальные электрики, первые контакты.",
    },
    {
        "cluster_id": "BIC016",
        "title": "Ограничения роста, экономика и найм",
        "topic": "growth_constraints_finance_staffing",
        "primary_outputs": ["strategy", "business_model_map"],
        "coverage": "Финансовые ограничения, маржа, склад, штат, подбор менеджеров/монтажников, масштабирование и операционные пределы.",
    },
    {
        "cluster_id": "BIC017",
        "title": "Маркетинговые формулировки и публичный контент",
        "topic": "marketing_public_content",
        "primary_outputs": ["commercial_messaging", "website_content_bank", "presentation"],
        "coverage": "Формулировки для сайта, буклетов, презентаций, публичные утверждения и материалы, требующие review.",
    },
    {
        "cluster_id": "BIC018",
        "title": "Кейсы, примеры и пилотные возможности",
        "topic": "sales_cases_examples",
        "primary_outputs": ["sales_training", "content_bank", "business_kb"],
        "coverage": "Конкретные клиентские, партнерские и внутренние кейсы, примеры продаж и пилотные региональные возможности.",
    },
    {
        "cluster_id": "BIC019",
        "title": "Открытые вопросы и блокеры",
        "topic": "open_questions_blockers",
        "primary_outputs": ["review_only", "strategy"],
        "coverage": "Вопросы, которые нельзя превращать в факты без дополнительного интервью, документов или проверки.",
    },
]

CLUSTER_BY_ID = {cluster["cluster_id"]: cluster for cluster in CLUSTERS}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
    )


def blob(claim: dict[str, Any]) -> str:
    values = [
        claim["claim"],
        claim["claim_type"],
        claim["business_area"],
        " ".join(claim.get("target_outputs", [])),
        " ".join(claim.get("normalized_terms", [])),
    ]
    return " ".join(values).lower()


def has_any(text: str, *terms: str) -> bool:
    return any(term.lower() in text for term in terms)


def assign_cluster(claim: dict[str, Any]) -> str:
    text = blob(claim)
    claim_type = claim["claim_type"]
    area = claim["business_area"]
    terms = {term.lower() for term in claim.get("normalized_terms", [])}

    if claim_type == "open_question" or area == "open_question":
        return "BIC019"
    if claim_type == "sales_case":
        return "BIC018"
    if claim_type in {"objection", "recommended_response"} or area == "objection_handling":
        return "BIC009"
    if claim_type == "qualification_question" or area == "qualification":
        return "BIC008"
    if has_any(text, "генератор", "стабилизатор", "online", "онлайн", "line interactive", "оффлайнов", "двойное преобразование"):
        return "BIC006"
    if claim_type == "technical_claim_needs_confirmation":
        if has_any(text, "байпас", "щит", "фаза", "зазем", "занул", "ноль", "место установки", "кабель", "автомат", "розет", "монтаж", "перебор"):
            return "BIC005"
        return "BIC004"
    if has_any(text, "1с", "crm", "сирем", "анкета", "карточка", "документ", "запись разговор", "отчет", "telegram", "word", "pdf", "калькулятор"):
        return "BIC013"
    if area == "customer_segment":
        return "BIC002"
    if area in {"customer_pain", "value_proposition"} or claim_type in {"customer_pain", "value_proposition_claim"}:
        return "BIC003"
    if area in {"business_model", "service_model"} or claim_type == "business_model_claim":
        if has_any(text, "регион", "краснодар", "юг", "филиал", "горячий ключ"):
            return "BIC015"
        if has_any(text, "штат", "найм", "марж", "финанс", "склад", "зарплат", "издерж", "масштаб", "рост", "средний чек"):
            return "BIC016"
        return "BIC001"
    if area == "sales_process" or claim_type == "sales_process_claim":
        return "BIC007"
    if has_any(text, "прораб", "строител", "девелоп", "дубльдом", "префаб", "модульн"):
        return "BIC011"
    if has_any(text, "электрик", "монтажник", "аутсорс", "выезд", "осмотр", "аудит", "монтаж") or area == "partner_model":
        return "BIC010"
    if has_any(text, "регион", "краснодар", "юг", "филиал", "горячий ключ", "южн"):
        return "BIC015"
    if has_any(text, "обуч", "специалист", "менеджер", "роль", "технический директор", "инженер"):
        return "BIC012"
    if has_any(text, "мониторинг", "sms", "смс", "обратная связь", "постпрод", "то", "гарант", "отзыв", "репутац"):
        return "BIC014"
    if has_any(text, "штат", "найм", "марж", "финанс", "склад", "зарплат", "издерж", "масштаб", "рост", "воронка"):
        return "BIC016"
    if claim_type == "marketing_message" or area == "marketing" or {"website", "brochure", "presentation", "commercial_messaging", "content_bank"}.intersection(claim.get("target_outputs", [])):
        return "BIC017"
    if has_any(text, "smb", "малый бизнес", "частные", "лпр", "клиентский сегмент"):
        return "BIC002"
    if has_any(text, "комфорт", "безопас", "боль клиента", "размороз", "вода", "интернет"):
        return "BIC003"
    if area in {"product", "technical_context"} or claim_type == "product_claim" or has_any(text, "инвертор", "аккумулятор", "мощность", "нагруз", "резерв", "пик", "котел", "насос", "холодильник"):
        return "BIC004"
    if area == "positioning" or claim_type == "positioning_claim":
        return "BIC001"
    if area == "operations" or claim_type == "operational_claim":
        return "BIC013"
    if area == "risk" or claim_type == "risk_or_constraint":
        return "BIC016"
    if area == "strategy" or claim_type == "strategy_claim":
        return "BIC015"
    raise ValueError(f"Cannot assign cluster for {claim['claim_id']}: {claim['claim']}")


def infer_secondary_cluster(claim: dict[str, Any], primary: str) -> str | None:
    text = blob(claim)
    candidates = [
        ("BIC003", ("комфорт", "безопас", "размороз", "вода", "интернет", "боль")),
        ("BIC010", ("электрик", "монтажник", "аутсорс", "аудит", "выезд")),
        ("BIC011", ("прораб", "строител", "девелоп")),
        ("BIC013", ("1с", "crm", "анкета", "документ", "карточка")),
        ("BIC015", ("регион", "краснодар", "юг", "горячий ключ", "вадик")),
        ("BIC004", ("инвертор", "аккумулятор", "мощность", "нагруз", "резерв")),
        ("BIC006", ("генератор", "стабилизатор", "онлайн", "ибп")),
        ("BIC001", ("услуга", "сервис", "бизнес-модель", "позиционирование")),
    ]
    for cluster_id, terms in candidates:
        if cluster_id != primary and has_any(text, *terms):
            return cluster_id
    return None


def relation_kind_for_claim(claim: dict[str, Any]) -> str:
    if claim["claim_type"] == "sales_case":
        return "example_of"
    if claim["claim_type"] in {"marketing_message", "positioning_claim", "value_proposition_claim"}:
        return "derived_marketing_message_for"
    if claim["claim_type"] == "technical_claim_needs_confirmation" or "technical_confirmation_required" in claim.get("review_flags", []):
        return "requires_technical_confirmation"
    if claim["claim_type"] in {"risk_or_constraint", "operational_claim", "open_question"}:
        return "context_for"
    return "supports"


def build_relations(claims: list[dict[str, Any]], assignments: dict[str, str]) -> list[dict[str, Any]]:
    relations: list[dict[str, Any]] = []
    relation_index = 1

    def add(source: str, relation_type: str, group_id: str, notes: str, target_claim: str | None = None, target_cluster: str | None = None) -> None:
        nonlocal relation_index
        if relation_type not in ALLOWED_RELATIONS:
            raise ValueError(f"Invalid relation type: {relation_type}")
        if not target_claim and not target_cluster:
            raise ValueError(f"Relation {source} lacks target")
        row: dict[str, Any] = {
            "relation_id": f"brel_{relation_index:04d}",
            "source_claim_id": source,
            "relation_type": relation_type,
            "group_id": group_id,
            "notes": notes,
        }
        if target_claim:
            row["target_claim_id"] = target_claim
        if target_cluster:
            row["target_cluster_id"] = target_cluster
        relations.append(row)
        relation_index += 1

    claims_by_id = {claim["claim_id"]: claim for claim in claims}
    by_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for claim in claims:
        by_cluster[assignments[claim["claim_id"]]].append(claim)

    for cluster_id, cluster_claims in by_cluster.items():
        anchors = [
            claim
            for claim in cluster_claims
            if claim["claim_type"] not in {"technical_claim_needs_confirmation", "sales_case", "open_question"}
        ]
        anchor = anchors[0] if anchors else cluster_claims[0]
        for claim in cluster_claims:
            if claim["claim_id"] == anchor["claim_id"]:
                continue
            kind = relation_kind_for_claim(claim)
            add(
                claim["claim_id"],
                kind,
                cluster_id,
                f"Primary-cluster relation to anchor claim {anchor['claim_id']} in {cluster_id}.",
                target_claim=anchor["claim_id"],
            )

    # Near-duplicate detection inside clusters. This is conservative and keeps both claims.
    for cluster_id, cluster_claims in by_cluster.items():
        sorted_claims = sorted(cluster_claims, key=lambda item: item["claim_id"])
        for index, left in enumerate(sorted_claims):
            left_text = re.sub(r"\s+", " ", left["claim"].lower())
            for right in sorted_claims[index + 1 :]:
                right_text = re.sub(r"\s+", " ", right["claim"].lower())
                if SequenceMatcher(None, left_text, right_text).ratio() >= 0.86:
                    add(
                        right["claim_id"],
                        "duplicate_of",
                        f"{cluster_id}_DUP",
                        "High lexical similarity inside the same cluster; both claims are preserved for source traceability.",
                        target_claim=left["claim_id"],
                    )

    for claim in claims:
        primary = assignments[claim["claim_id"]]
        secondary = infer_secondary_cluster(claim, primary)
        if claim["claim_type"] == "sales_case" and secondary:
            add(
                claim["claim_id"],
                "example_of",
                f"{primary}_EXAMPLES",
                f"Sales case is a concrete example relevant to {secondary}.",
                target_cluster=secondary,
            )
        if claim["claim_type"] == "open_question" and secondary:
            add(
                claim["claim_id"],
                "context_for",
                f"{primary}_OPEN",
                f"Open question may affect downstream work in {secondary}.",
                target_cluster=secondary,
            )
        if claim["claim_type"] in {"marketing_message", "positioning_claim", "value_proposition_claim"}:
            secondary = secondary or "BIC017"
            add(
                claim["claim_id"],
                "derived_marketing_message_for",
                f"{primary}_MARKETING",
                f"Candidate wording or positioning statement should be reviewed before public use in {secondary}.",
                target_cluster=secondary,
            )

    # Curated tension points that should be visible to reviewers.
    curated_pairs = [
        (
            "interview_claim_007021",
            "interview_claim_007022",
            "contradicts",
            "BIC010_TENSION",
            "Вадик notes that star electricians exist; Дмитрий counters that scalable business cannot depend on stars.",
        ),
        (
            "interview_claim_007032",
            "interview_claim_007035",
            "refines",
            "BIC011_BIC010",
            "Foremen/builders can add sales, but Sergey frames outsourced electricians as the scalable core model.",
        ),
        (
            "interview_claim_006031",
            "interview_claim_007020",
            "supports",
            "BIC010_SUPPORT",
            "Two interviews support the same concern: ordinary electricians are not expected to own complex client qualification.",
        ),
    ]
    for source, target, relation_type, group_id, notes in curated_pairs:
        if source in claims_by_id and target in claims_by_id:
            add(source, relation_type, group_id, notes, target_claim=target)

    return relations


def build_markdown(claims: list[dict[str, Any]], assignments: dict[str, str], clusters: list[dict[str, Any]], relations: list[dict[str, Any]]) -> str:
    by_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for claim in claims:
        by_cluster[assignments[claim["claim_id"]]].append(claim)

    lines = [
        "# Business interview statement clusters v1",
        "",
        f"Дата: {date.today().isoformat()}",
        "",
        "Источник:",
        "",
        "```text",
        "00_input/interviews/statements/interview_corpus_claims.jsonl",
        "```",
        "",
        "## Статус",
        "",
        "Это первичная кластеризация v1 по всем семи интервью. Она не меняет extracted claims, а группирует их для review, дедупликации, relation mapping и последующей сборки Business / Sales / Commercial KB.",
        "",
        f"- Claims total: `{len(claims)}`",
        f"- Clusters total: `{len(clusters)}`",
        f"- Relations total: `{len(relations)}`",
        f"- Technical confirmation required: `{sum('technical_confirmation_required' in claim.get('review_flags', []) for claim in claims)}`",
        "",
        "## Важные ограничения",
        "",
        "- Технические claims из интервью остаются review-required и не являются техническими правилами.",
        "- Marketing/public claims требуют отдельного review перед сайтом, КП, буклетом или презентацией.",
        "- Дубликаты не удаляются: связи фиксируются в `statement_relations.jsonl`.",
        "",
    ]

    for cluster in clusters:
        cluster_claims = sorted(by_cluster.get(cluster["cluster_id"], []), key=lambda item: item["claim_id"])
        source_counts = Counter(claim["source_interview_id"] for claim in cluster_claims)
        type_counts = Counter(claim["claim_type"] for claim in cluster_claims)
        review_flags = Counter(flag for claim in cluster_claims for flag in claim.get("review_flags", []))
        example_ids = [claim["claim_id"] for claim in cluster_claims[:8]]

        lines.extend(
            [
                f"## {cluster['cluster_id']}. {cluster['title']}",
                "",
                f"Тема: `{cluster['topic']}`",
                "",
                f"Количество claims: `{len(cluster_claims)}`",
                "",
                f"Охват: {cluster['coverage']}",
                "",
                "Основные выходы:",
                "",
            ]
        )
        lines.extend(f"- `{output}`" for output in cluster["primary_outputs"])
        lines.extend(["", "Источники:", ""])
        lines.extend([f"- `{key}`: {value}" for key, value in sorted(source_counts.items())] or ["- none"])
        lines.extend(["", "Типы claims:", ""])
        lines.extend([f"- `{key}`: {value}" for key, value in sorted(type_counts.items())] or ["- none"])
        lines.extend(["", "Review flags:", ""])
        lines.extend([f"- `{key}`: {value}" for key, value in sorted(review_flags.items())] or ["- none"])
        lines.extend(["", "Примеры claim_id:", ""])
        lines.extend([f"- `{claim_id}`" for claim_id in example_ids] or ["- none"])
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    claims = load_jsonl(CLAIMS_PATH)
    claim_ids = [claim["claim_id"] for claim in claims]
    if len(claim_ids) != len(set(claim_ids)):
        raise SystemExit("Duplicate claim_id in input")

    assignments = {claim["claim_id"]: assign_cluster(claim) for claim in claims}
    assigned_ids = set(assignments)
    if assigned_ids != set(claim_ids):
        raise SystemExit("Cluster assignment is incomplete")

    by_cluster: dict[str, list[str]] = defaultdict(list)
    for claim_id, cluster_id in assignments.items():
        if cluster_id not in CLUSTER_BY_ID:
            raise SystemExit(f"Unknown cluster_id: {cluster_id}")
        by_cluster[cluster_id].append(claim_id)

    relations = build_relations(claims, assignments)
    valid_claim_ids = set(claim_ids)
    for relation in relations:
        if relation["source_claim_id"] not in valid_claim_ids:
            raise SystemExit(f"Invalid relation source: {relation}")
        if relation.get("target_claim_id") and relation["target_claim_id"] not in valid_claim_ids:
            raise SystemExit(f"Invalid relation target claim: {relation}")
        if relation.get("target_cluster_id") and relation["target_cluster_id"] not in CLUSTER_BY_ID:
            raise SystemExit(f"Invalid relation target cluster: {relation}")

    clusters = []
    for cluster in CLUSTERS:
        claim_ids_for_cluster = sorted(by_cluster.get(cluster["cluster_id"], []))
        source_files = sorted(
            {
                claim["source_file"]
                for claim in claims
                if assignments[claim["claim_id"]] == cluster["cluster_id"]
            }
        )
        clusters.append(
            {
                **cluster,
                "source_files": source_files,
                "claim_count": len(claim_ids_for_cluster),
                "claim_ids": claim_ids_for_cluster,
            }
        )

    output = {
        "version": "v1",
        "created_at": date.today().isoformat(),
        "source": str(CLAIMS_PATH.relative_to(ROOT)),
        "canonical_claim_count": len(claims),
        "clusters": clusters,
        "next_steps": [
            "Review cluster boundaries and relation types.",
            "Use clusters as source-backed input for editorial Business / Sales / Commercial KB assembly.",
            "Do not promote technical interview claims into technical KB without external confirmation.",
        ],
        "claim_assignment_complete": True,
        "unassigned_claim_ids": [],
        "relations": {
            "source": str(OUT_RELATIONS.relative_to(ROOT)),
            "relation_count": len(relations),
            "allowed_relation_types": sorted(ALLOWED_RELATIONS),
        },
    }

    OUT_CLUSTERS.parent.mkdir(parents=True, exist_ok=True)
    OUT_CLUSTERS.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_CLUSTERS_MD.write_text(build_markdown(claims, assignments, clusters, relations), encoding="utf-8")
    write_jsonl(OUT_RELATIONS, relations)

    print(f"claims={len(claims)}")
    print(f"clusters={len(clusters)}")
    print(f"relations={len(relations)}")
    print(f"unassigned=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
