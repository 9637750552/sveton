#!/usr/bin/env python3
"""Build source-backed extraction artifacts for interview_005."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = "00_input/interviews/260609_sveton_converted_t_large-v3_diar.txt"
SOURCE_PATH = ROOT / SOURCE_FILE
CHUNKS_PATH = ROOT / "00_input/interviews/chunks/interview_005_chunks.jsonl"
OUT_CLAIMS = ROOT / "00_input/interviews/statements/interview_005_claims.jsonl"
OUT_RESULTS = ROOT / "00_input/interviews/statements/interview_005_extraction_results.jsonl"

ROLES = {
    "SPEAKER_00": ("Сергей", "директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели"),
    "SPEAKER_01": ("Дмитрий", "генеральный директор Светон"),
}

TS_RE = re.compile(r"^\[([0-9:]+) - ([0-9:]+)\] (SPEAKER_[0-9]{2}):")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
    )


def ts_for_lines(source_lines: list[str], start_line: int, end_line: int) -> tuple[str, str]:
    first = last = None
    for line in source_lines[start_line - 1 : end_line]:
        match = TS_RE.match(line)
        if not match:
            continue
        if first is None:
            first = match.group(1)
        last = match.group(2)
    if first is None or last is None:
        raise ValueError(f"No timestamp in lines {start_line}-{end_line}")
    return first, last


SOURCE_LINES = SOURCE_PATH.read_text(encoding="utf-8-sig").splitlines()


def claim(
    seq: int,
    chunk_index: int,
    line_range: tuple[int, int],
    speaker: str,
    claim_text: str,
    claim_type: str,
    business_area: str,
    target_outputs: list[str],
    applicability: str,
    evidence_status: str,
    confidence: str = "high",
    review_status: str = "review_required",
    flags: list[str] | None = None,
    terms: list[str] | None = None,
    objection: dict[str, str] | None = None,
    sales_case: dict[str, str] | None = None,
    discovery_question: dict[str, str] | None = None,
    open_question: dict[str, str] | None = None,
    notes: str = "",
) -> dict[str, Any]:
    start_line, end_line = line_range
    start_ts, end_ts = ts_for_lines(SOURCE_LINES, start_line, end_line)
    identity, role = ROLES[speaker]
    return {
        "claim_id": f"interview_claim_005{seq:03d}",
        "claim": claim_text,
        "claim_type": claim_type,
        "source_interview_id": "interview_005",
        "source_file": SOURCE_FILE,
        "source_chunk_id": f"interview_005_chunk_{chunk_index:04d}",
        "speaker_label": speaker,
        "speaker_identity": identity,
        "speaker_role": role,
        "speaker_mapping_confidence": "confirmed",
        "start_timestamp": start_ts,
        "end_timestamp": end_ts,
        "source_quote": "\n".join(SOURCE_LINES[start_line - 1 : end_line]),
        "business_area": business_area,
        "target_outputs": target_outputs,
        "applicability_to_electricians_kb": applicability,
        "evidence_status": evidence_status,
        "confidence": confidence,
        "review_status": review_status,
        "review_flags": flags or [],
        "related_claim_ids": [],
        "normalized_terms": terms or [],
        "objection": objection,
        "sales_case": sales_case,
        "discovery_question": discovery_question,
        "open_question": open_question,
        "notes": notes,
    }


SPECS: list[dict[str, Any]] = [
    claim(1, 1, (1, 3), "SPEAKER_00", "Сергей планирует начать региональный MVP не с прорабов, а с электриков из объявлений на Авито, потому что они ближе к людям с проблемами электроснабжения.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["MVP", "электрики", "Авито", "регион"]),
    claim(2, 1, (4, 4), "SPEAKER_01", "Дмитрий считает, что рядовой электрик обычно получает низкоуровневые задачи и редко способен провести аудит, понять решение и убедить клиента.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["электрик", "аудит", "продажа", "монтажник"]),
    claim(3, 1, (4, 5), "SPEAKER_01", "Даже среди собственных монтажников компании только два из восьми, по оценке Дмитрия, способны провести аудит и понять, что нужно ставить; при этом они не умеют продавать.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "price_or_guarantee_review", "technical_confirmation_required"], terms=["монтажники", "2 из 8", "аудит", "продажи"]),
    claim(4, 1, (5, 5), "SPEAKER_01", "Базовая модель с монтажником: он должен понять, берется ли за монтаж и сколько это будет стоить; убеждение клиента должен делать менеджер или прораб.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["монтажник", "менеджер", "прораб", "стоимость монтажа"]),
    claim(5, 1, (6, 10), "SPEAKER_00", "Сергей предлагает не решать заранее за электриков, а проверить гипотезу: электрик может быть мотивирован продать монтаж, дать контакт или использовать буклет/сайт для объяснения решения.", "strategy_claim", "strategy", ["business_kb", "strategy", "sales_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["проверка гипотезы", "электрик", "буклет", "сайт"]),
    claim(6, 2, (11, 11), "SPEAKER_00", "MVP предполагает прозвонить 72 объявления электриков за две недели и проверить, будут ли они продавать или рекомендовать решение.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["MVP", "72 объявления", "две недели", "электрики"]),
    claim(7, 2, (11, 13), "SPEAKER_00", "Для MVP нужен понятный документ или аудиоинструкция, описывающая, как проводить аудит объекта и какие вопросы задавать.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["аудит", "инструкция", "аудиозапись", "документ"]),
    claim(8, 2, (15, 16), "SPEAKER_01", "Первый шаг аудита: выяснить, какие электроприборы клиент хочет зарезервировать.", "qualification_question", "qualification", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], discovery_question={"question": "Какие электроприборы клиент хочет зарезервировать?", "why_it_matters": "Это исходная точка для расчета мощности и емкости системы.", "answer_changes": "Меняется список потребителей, тип системы и бюджет."}, terms=["аудит", "потребители", "резервирование"]),
    claim(9, 2, (16, 16), "SPEAKER_01", "Для расчета нужно оценить суммарную постоянную мощность, пиковую мощность и коэффициент использования электроприборов.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["постоянная мощность", "пиковая мощность", "коэффициент использования"]),
    claim(10, 2, (16, 16), "SPEAKER_01", "Постоянная мощность используется для подбора инвертора, пиковая мощность - для проверки способности инвертора выдержать запуск, а коэффициент использования - для расчета количества аккумуляторов.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["инвертор", "аккумуляторы", "пиковая мощность", "расчет"]),
    claim(11, 2, (16, 18), "SPEAKER_01", "Запас энергии зависит от профиля нагрузки: 5 кВт на 1 час дешевле, чем 1 кВт на 24 часа, потому что во втором случае нужен больший запас энергии.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["запас энергии", "5 кВт·ч", "24 кВт·ч", "аккумуляторы"]),
    claim(12, 2, (17, 18), "SPEAKER_01", "Коэффициент использования часто нельзя узнать у клиента точно; компания оценивает его теоретически и по опыту специалистов, примерно с погрешностью плюс-минус 10%.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["коэффициент использования", "погрешность", "10%", "предварительный расчет"]),
    claim(13, 3, (19, 20), "SPEAKER_01", "Вторая задача аудита - отсеять лишние электроприборы: например, теплый пол может быстро высосать аккумулятор и оставить без резерва котел, холодильник или насос.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["лишние нагрузки", "теплый пол", "аккумулятор", "котел"]),
    claim(14, 3, (21, 26), "SPEAKER_01", "Третья задача аудита - понять разводку по дому и можно ли выделить резервируемые приборы в отдельную линию; иначе на линии могут оказаться плита, чайник или другие мощные нагрузки.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["разводка", "отдельная линия", "кухня", "перегрузка"]),
    claim(15, 4, (27, 30), "SPEAKER_00", "Сергей формулирует простую версию аудита для электрика: спросить, какие нагрузки критичны, определить названия нагрузок и примерно оценить номинальную и пиковую мощность.", "qualification_question", "qualification", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], discovery_question={"question": "Какие нагрузки критичны и какие у них номинальные/пиковые мощности?", "why_it_matters": "Электрик должен собрать минимальные данные для предварительного расчета.", "answer_changes": "Определяет, можно ли двигаться к расчету и осмотру."}, terms=["критичные нагрузки", "номинальная мощность", "пиковая мощность", "электрик"]),
    claim(16, 4, (31, 34), "SPEAKER_01", "Дмитрий предупреждает, что нельзя переоценивать квалификацию сертифицированных электриков: многие умеют прокладывать линии и штробить, но не умеют думать в терминах системы.", "risk_or_constraint", "risk", ["business_kb", "manager_training", "electricians_kb"], "context_only", "speaker_opinion", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["сертифицированный электрик", "квалификация", "штробить", "линии"]),
    claim(17, 4, (35, 41), "SPEAKER_01", "Электрик в состоянии понять разводку, фазы, мощности и дополнительные нагрузки на линии, но работа с клиентом и убеждение остаются ролью менеджера.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["разводка", "фазы", "мощность", "роль менеджера"]),
    claim(18, 4, (41, 45), "SPEAKER_01", "На осмотре электрик может проверить щиток, распределение по фазам, мощности и наличие дополнительных потребителей на линии.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["осмотр", "щиток", "фазы", "линия"]),
    claim(19, 5, (46, 47), "SPEAKER_00", "Сергей предлагает разделить роли: он разговаривает с клиентом, а электрика отправляет на осмотр только после интереса клиента и по четкой инструкции.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["разделение ролей", "осмотр", "инструкция", "клиент"]),
    claim(20, 5, (48, 48), "SPEAKER_01", "Дмитрий оценивает, что из теплых входящих лидов реальными становятся около 25%, а в холодном обзвоне готовность к визиту может быть около 5%.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "speaker_opinion", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["лиды", "25%", "холодный обзвон", "5%"]),
    claim(21, 5, (49, 52), "SPEAKER_00", "В холодном тестировании электрик должен заинтересовать клиента решением по резервированию инженерных систем, понимать свою выгоду в монтаже и после интереса клиента передавать разговор Сергею.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "sales_script"], "context_only", "source_backed", flags=["marketing_claim_review", "strategy_claim_review"], terms=["холодное тестирование", "электрик", "монтаж", "инженерные системы"]),
    claim(22, 5, (52, 55), "SPEAKER_01", "Для Краснодарского MVP можно ориентироваться на цену монтажа около 20 тысяч рублей и один день работы, а при необходимости компенсировать выезд электрика.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["Краснодар", "20 тысяч", "один день", "компенсация выезда"]),
    claim(23, 5, (55, 61), "SPEAKER_01", "Выезд электрика должен происходить после разговора Сергея с клиентом, предварительного предложения и подтверждения, что клиенту в принципе интересно.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["выезд", "предложение", "интерес клиента", "осмотр"]),
    claim(24, 6, (62, 70), "SPEAKER_01", "В системе 3-5 первая цифра обозначает мощность инвертора в киловаттах, а вторая - запас энергии в киловатт-часах.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["3-5", "инвертор", "кВт", "кВт·ч"]),
    claim(25, 6, (71, 74), "SPEAKER_00", "Сергей выявляет риск непонимания в коммерческом описании: клиент может не понять, почему система с 2 кВт·ч обещает 6-10 часов резерва, если максимальная нагрузка 3 кВт.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "public_use_review"], terms=["коммерческое описание", "2 кВт·ч", "6-10 часов", "3 кВт"]),
    claim(26, 7, (75, 86), "SPEAKER_01", "Система 3.2 описана как кратковременный резерв для котла, холодильника и насоса; для одного котла есть отдельные меньшие системы котел.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["3.2", "котел", "холодильник", "насос", "система котел"]),
    claim(27, 7, (85, 88), "SPEAKER_01", "Пиковая мощность инвертора доступна кратковременно, примерно 2-5 секунд, и нужна для запуска нагрузок.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["пиковая мощность", "2-5 секунд", "запуск нагрузок"]),
    claim(28, 7, (89, 92), "SPEAKER_01", "Кондиционер слишком мощный для системы 3 кВт в описанном сценарии; типовой состав такой системы - холодильник, насос около 800 Вт и котел.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["кондиционер", "3 кВт", "холодильник", "насос 800 Вт", "котел"]),
]


def main() -> int:
    chunks = load_jsonl(CHUNKS_PATH)
    chunk_by_id = {chunk["chunk_id"]: chunk for chunk in chunks}
    for spec in SPECS:
        chunk = chunk_by_id[spec["source_chunk_id"]]
        if spec["source_quote"] not in chunk["text"]:
            raise SystemExit(f"{spec['claim_id']}: source quote not in chunk")

    by_chunk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for spec in SPECS:
        by_chunk[spec["source_chunk_id"]].append(spec)

    results = []
    for chunk in chunks:
        chunk_id = chunk["chunk_id"]
        claims = by_chunk.get(chunk_id, [])
        results.append(
            {
                "source_chunk_id": chunk_id,
                "coverage_summary": {
                    "meaningful_items_seen": len(claims),
                    "claims_extracted": len(claims),
                    "open_questions_found": sum(1 for item in claims if item["claim_type"] == "open_question"),
                    "noise_or_transition_items": 0,
                    "coverage_notes": "Full interview_005 extraction; regional MVP, sales-process, partner, and technical-boundary items extracted as source-backed claims.",
                },
                "skipped_source_items": [],
                "claims": claims,
            }
        )

    write_jsonl(OUT_CLAIMS, SPECS)
    write_jsonl(OUT_RESULTS, results)
    print(f"claims={len(SPECS)}")
    print(f"results={len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
