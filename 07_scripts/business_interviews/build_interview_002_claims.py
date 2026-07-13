#!/usr/bin/env python3
"""Build source-backed extraction artifacts for interview_002."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = "00_input/interviews/260405_sveton_2_converted_t_large-v3_diar.txt"
SOURCE_PATH = ROOT / SOURCE_FILE
CHUNKS_PATH = ROOT / "00_input/interviews/chunks/interview_002_chunks.jsonl"
OUT_CLAIMS = ROOT / "00_input/interviews/statements/interview_002_claims.jsonl"
OUT_RESULTS = ROOT / "00_input/interviews/statements/interview_002_extraction_results.jsonl"

ROLES = {
    "SPEAKER_00": ("Дмитрий", "генеральный директор Светон"),
    "SPEAKER_01": ("Дмитрий", "генеральный директор Светон"),
    "SPEAKER_02": ("Сергей", "директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели"),
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
        "claim_id": f"interview_claim_002{seq:03d}",
        "claim": claim_text,
        "claim_type": claim_type,
        "source_interview_id": "interview_002",
        "source_file": SOURCE_FILE,
        "source_chunk_id": f"interview_002_chunk_{chunk_index:04d}",
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
    claim(1, 2, (15, 17), "SPEAKER_01", "Основной частный клиент описан как владелец частного дома, коттеджа или таунхауса с доходом выше среднего, включая верхний средний класс и нижний бизнес-класс.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training", "commercial_messaging"], "not_relevant", "source_backed", flags=["marketing_claim_review"], terms=["частный дом", "коттедж", "таунхаус", "доход выше среднего"]),
    claim(2, 2, (19, 19), "SPEAKER_01", "Средний чек проекта для частного клиента назван как 350 тысяч рублей.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review"], terms=["средний чек", "350 тысяч рублей"]),
    claim(3, 2, (21, 21), "SPEAKER_01", "Основные причины покупки: нестабильное электричество, проблемы с инженерией дома, желание повысить комфорт и обеспечить безопасность дома, включая защиту от разморозки зимой.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "sales_script", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["нестабильное электричество", "инженерия дома", "комфорт", "разморозка"]),
    claim(4, 3, (25, 28), "SPEAKER_01", "Компания не берет на себя полноценную экспертизу электропроводки, но при осмотре может заметить явные проблемы вроде короткого замыкания или плохих соединений и указать клиенту на необходимость исправления.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["электропроводка", "осмотр", "короткое замыкание", "соединения"]),
    claim(5, 3, (31, 32), "SPEAKER_01", "Если в электропроводке есть действительные проблемы, компания отказывается устанавливать систему до исправления этих проблем.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["отказ от установки", "электропроводка", "риск"]),
    claim(6, 4, (34, 35), "SPEAKER_01", "Решение о покупке обычно принимает глава семьи; это может быть мужчина, женщина, а иногда прораб.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training"], "context_only", "source_backed", flags=["marketing_claim_review"], terms=["ЛПР", "глава семьи", "прораб"]),
    claim(7, 4, (36, 39), "SPEAKER_01", "Клиенты приходят через интернет и рекомендации; рекомендации названы значительной долей, минимум около 20%.", "sales_process_claim", "sales_process", ["business_kb", "strategy", "sales_training"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["рекомендации", "интернет", "20%"]),
    claim(8, 4, (39, 39), "SPEAKER_01", "Менеджеру доплачивают фиксированную сумму за рекомендацию, чтобы он отмечал источник рекомендации в CRM на базе 1С.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["CRM", "1С", "рекомендация", "мотивация менеджера"]),
    claim(9, 4, (39, 43), "SPEAKER_01", "После одной установки в поселке может появиться 10, 20 или 30 последующих систем, а данные о существующих установках можно использовать как социальное доказательство.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "sales_script", "commercial_messaging"], "context_only", "source_backed", confidence="medium", flags=["marketing_claim_review", "price_or_guarantee_review"], terms=["поселок", "социальное доказательство", "сарафанное радио"]),
    claim(10, 4, (43, 45), "SPEAKER_01", "Компания пробовала работать с чатами поселков и просить клиентов рекомендовать установку в чате, но пока не нашла хорошую модель вознаграждения для клиентов такого уровня.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["чаты поселков", "рекомендации", "вознаграждение"]),
    claim(11, 5, (47, 47), "SPEAKER_01", "Основное возражение клиентов против ИБП: генератор кажется дешевле, сравнимым по мощности и с неограниченным сроком работы.", "objection", "objection_handling", ["business_kb", "sales_training", "objection_handling", "sales_script"], "context_only", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["генератор", "возражение", "мощность"], objection={"objection_category": "generator_cheaper", "customer_assumption": "Генератор дешевле, сравним по мощности и может работать неограниченно.", "recommended_response": "Разобрать полную стоимость качественного генератора, прерывание при запуске, обслуживание и риск отказа."}),
    claim(12, 5, (47, 47), "SPEAKER_01", "Ответ на генераторное возражение строится на том, что качественный генератор дороже, дает прерывание до запуска, требует обслуживания и имеет высокий риск отказа без обслуживания.", "recommended_response", "objection_handling", ["sales_training", "objection_handling", "sales_script", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required", "public_use_review"], terms=["генератор", "обслуживание", "отказ"]),
    claim(13, 6, (55, 64), "SPEAKER_02", "Кейс с магазином Винлаб показывает, что при отключении электричества магазин может не обслужить покупателя из-за неработающей системы и интернета, даже если часть электропитания резервируется.", "sales_case", "sales_process", ["business_kb", "sales_training", "content_bank", "commercial_messaging"], "context_only", "example_case", flags=["marketing_claim_review", "technical_confirmation_required"], sales_case={"customer_type": "розничный магазин", "problem_situation": "Отключение электричества и интернета помешало пробить товар и обслужить покупателя.", "diagnosis_path": "Проверить, какие элементы системы резервируются: касса, интернет, роутер, учетная система.", "proposed_action": "Использовать кейс как повод для холодного outreach и диагностики резервного питания.", "risk_or_caveat": "Кейс рассказан как личный эпизод и требует проверки перед публичным использованием."}, terms=["Винлаб", "розница", "интернет", "резервное питание"]),
    claim(14, 6, (64, 70), "SPEAKER_02", "Кейс Винлаб предложен как вход для тестирования холодных звонков и захода в компанию через реальную боль с резервным питанием и интернетом.", "strategy_claim", "strategy", ["business_kb", "strategy", "sales_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["холодные звонки", "корпоративный клиент", "резервное питание"]),
    claim(15, 7, (72, 79), "SPEAKER_01", "В египетских ларьках инвертор с литиевой батареей стоит потому, что при отключении света покупатели не могут рассмотреть товар, особенно вечером после выхода из отеля.", "sales_case", "sales_process", ["business_kb", "sales_training", "content_bank"], "context_only", "example_case", flags=["marketing_claim_review"], sales_case={"customer_type": "малый розничный бизнес", "problem_situation": "При отключении света покупатели не видят товар и продажи останавливаются.", "diagnosis_path": "Понять, какие часы продаж критичны и какие потребители нужно резервировать.", "proposed_action": "Позиционировать резервное питание как защиту продаж, а не только оборудования.", "risk_or_caveat": "Кейс зарубежный и используется как аналогия."}, terms=["розница", "Египет", "литиевая батарея", "потеря продаж"]),
    claim(16, 8, (83, 86), "SPEAKER_01", "Для SMB приоритетны сегменты, где при отключении электричества останавливаются деньги или клиентский поток: торговля, небольшие медицинские центры, стоматологии, ветеринарные клиники и часть небольших цехов.", "customer_segment_claim", "customer_segment", ["business_kb", "strategy", "sales_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["SMB", "торговля", "медицинский центр", "стоматология", "ветеринарная клиника"]),
    claim(17, 8, (90, 109), "SPEAKER_01", "Федеральные АЗС и крупный бизнес менее привлекательны как целевой сегмент, потому что у них зарегулированные проекты, жесткий отбор поставщиков, длинные циклы и решения закладываются проектировщиками при строительстве.", "risk_or_constraint", "strategy", ["business_kb", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["АЗС", "крупный бизнес", "тендер", "проектировщик"]),
    claim(18, 8, (111, 114), "SPEAKER_01", "Малому и среднему бизнесу нужны гибкие и недорогие решения, потому что он не готов платить большие деньги крупным производителям ИБП, а 15 минут простоя могут стоить клиентов и репутации.", "value_proposition_claim", "value_proposition", ["business_kb", "sales_training", "commercial_messaging", "website"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["SMB", "гибкое решение", "15 минут простоя", "репутация"]),
    claim(19, 9, (115, 116), "SPEAKER_01", "Ожидаемый средний чек в SMB назван в диапазоне 700 тысяч - 1,5 миллиона рублей.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["SMB", "средний чек", "700 тысяч", "1,5 миллиона"]),
    claim(20, 9, (117, 118), "SPEAKER_01", "В SMB окончательное решение принимает директор, но предварительная стадия часто идет через электрика, главного инженера, секретаря или другого сотрудника, ведущего переписку.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training", "sales_script"], "context_only", "source_backed", flags=["marketing_claim_review"], terms=["SMB", "ЛПР", "директор", "секретарь", "электрик"]),
    claim(21, 9, (119, 126), "SPEAKER_01", "Отличие SMB-продаж от частных продаж пока не проанализировано глубоко; отмечено, что у переговорщика может не быть личной заинтересованности в решении.", "open_question", "open_question", ["business_kb", "strategy", "review_only"], "not_relevant", "open_question", confidence="medium", flags=["open_question", "strategy_claim_review"], open_question={"question": "Чем продажа SMB системно отличается от продаж частным клиентам?", "why_open": "Дмитрий прямо говорит, что сильного анализа пока нет.", "needed_evidence": "Нужны интервью с менеджерами и реальные SMB сделки."}, terms=["SMB", "частные клиенты", "личная заинтересованность"]),
    claim(22, 10, (129, 131), "SPEAKER_01", "В южном регионе нужно развивать и состоятельных частных клиентов, и SMB, но частных клиентов имеет смысл искать там, где есть деньги: Сочи, Геленджик, Анапа максимум.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["южный регион", "Сочи", "Геленджик", "Анапа", "состоятельный клиент"]),
    claim(23, 10, (133, 135), "SPEAKER_01", "Региональные клиенты отличаются от московских тем, что им труднее что-либо доказать, они больше верят местным компаниям и боятся остаться с проблемами один на один.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["региональные клиенты", "доверие", "местная компания"]),
    claim(24, 10, (138, 140), "SPEAKER_01", "Для региона SMB может быть проще, потому что бизнес понимает потери, больше доверяет фирме с отзывами и проверяет репутацию в интернете.", "strategy_claim", "strategy", ["business_kb", "strategy", "sales_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["SMB", "регион", "отзывы", "репутация"]),
    claim(25, 10, (140, 140), "SPEAKER_01", "Первые 15 минут общения должны показать клиенту, что менеджер понимает его боль и четко объясняет решение.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "sales_script"], "not_relevant", "source_backed", flags=["marketing_claim_review"], terms=["первые 15 минут", "боль клиента", "менеджер"]),
    claim(26, 11, (141, 146), "SPEAKER_01", "Ключевая проблема SMB-клиента формулируется как постановка бизнеса на паузу во время отключения электроэнергии; для южного региона это связано с энергодефицитом и авариями.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["SMB", "энергодефицит", "отключение электроэнергии", "простой бизнеса"]),
    claim(27, 11, (147, 149), "SPEAKER_01", "Важный риск для удаленного клиента: оборудование может работать неправильно или ломаться, а сервисная служба находится далеко.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "strategy"], "context_only", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["удаленный клиент", "сервис", "поломка"]),
    claim(28, 11, (150, 155), "SPEAKER_01", "Покупку откладывают из-за высокой цены; иногда клиент сначала ставит генератор и возвращается к покупке ИБП после проблем с генератором.", "customer_pain", "objection_handling", ["business_kb", "sales_training", "objection_handling"], "context_only", "source_backed", flags=["marketing_claim_review", "price_or_guarantee_review"], terms=["цена", "генератор", "отложенная покупка"]),
    claim(29, 11, (152, 155), "SPEAKER_01", "У менеджеров есть аргументация экономической эффективности генератора: полная стоимость качественного генератора, площадка, установка, обслуживание и эксплуатационные проблемы.", "recommended_response", "objection_handling", ["sales_training", "objection_handling", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "price_or_guarantee_review"], terms=["генератор", "экономическая эффективность", "калькулятор"]),
    claim(30, 11, (156, 157), "SPEAKER_01", "Типовая ошибка клиента без профессионального решения - подобрать оборудование без запаса мощности или выбрать неподходящее место, что ускоряет старение электроники и аккумуляторов.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["запас мощности", "70%", "место установки", "старение аккумуляторов"]),
    claim(31, 12, (158, 159), "SPEAKER_01", "Клиент выбирает компанию из-за демонстрации экспертности, открытости по ценам и готовности отказаться от установки неподходящего оборудования.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging", "website"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["экспертность", "открытость цен", "отказ от установки"]),
    claim(32, 12, (160, 163), "SPEAKER_01", "Компания продает не оборудование, а услугу бесперебойного электроснабжения: подбор, поставку, монтаж, гарантийное и послегарантийное обслуживание.", "value_proposition_claim", "value_proposition", ["business_kb", "sales_training", "website", "brochure", "presentation", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["услуга", "бесперебойное электроснабжение", "полный цикл"]),
    claim(33, 12, (164, 165), "SPEAKER_01", "Основная прибыль формируется на продаже оборудования и монтаже; сервис является маленькой составляющей компании.", "business_model_claim", "business_model", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["прибыль", "оборудование", "монтаж", "сервис"]),
    claim(34, 12, (168, 173), "SPEAKER_01", "Продуктовые линейки включают резервирование котла, котла и водоснабжения, важных потребителей, части дома или всего дома; чаще продается резервирование части дома системой 5/10.", "product_claim", "product", ["business_kb", "sales_training", "presentation"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["котел", "водоснабжение", "часть дома", "5 кВт", "10 кВт·ч"]),
    claim(35, 12, (173, 175), "SPEAKER_01", "Компания продает только типовые решения и стандартные комплекты; сервисные контракты есть, но практически не заключаются, потому что продукт продвигается как не требующий сервиса.", "product_claim", "product", ["business_kb", "sales_training", "strategy"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "strategy_claim_review"], terms=["типовые решения", "стандартные комплекты", "сервисный контракт"]),
    claim(36, 12, (176, 183), "SPEAKER_01", "Переход от свинцово-кислотных аккумуляторов к литию снижает частоту повторных продаж и сервиса, но повышает разовый доход за счет более дорогой системы.", "business_model_claim", "business_model", ["business_kb", "strategy"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review", "strategy_claim_review"], terms=["литий", "свинцово-кислотные аккумуляторы", "повторные продажи", "one-off"]),
    claim(37, 12, (184, 186), "SPEAKER_01", "Апгрейды редки: клиент обычно закрывает критические потребности и больше не думает о системе; иногда старую систему оставляют на котел, а новую добавляют на другую часть дома.", "business_model_claim", "business_model", ["business_kb", "sales_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["апгрейд", "критические потребности", "котел"]),
    claim(38, 13, (187, 188), "SPEAKER_01", "Ключевые преимущества описаны как экспертность и надежность, которые демонстрируются менеджерами, монтажниками, брендированными машинами и одеждой.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging", "presentation"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["экспертность", "надежность", "брендирование"]),
    claim(39, 13, (189, 196), "SPEAKER_01", "Путь клиента: звонок и описание проблемы, наводящие вопросы менеджера, выявление боли, предложение вариантов, выезд, проверка реальной ситуации, подбор системы, согласование даты и монтаж.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training", "sales_script"], "context_only", "source_backed", flags=[], terms=["путь клиента", "выезд", "выявление боли", "монтаж"]),
    claim(40, 13, (197, 199), "SPEAKER_01", "Лиды приходят в основном из интернета: Директ, промо-страницы, РСЯ, прогрев через соцсети, рекомендации и потенциально чаты поселков.", "sales_process_claim", "sales_process", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["Директ", "РСЯ", "соцсети", "чаты поселков"]),
    claim(41, 14, (200, 202), "SPEAKER_01", "Поток лидов колеблется от 5 до 30 в день, что в месяц составляет примерно 500-1300 лидов.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["лиды", "500-1300", "5-30 в день"]),
    claim(42, 14, (203, 214), "SPEAKER_01", "Продажи обслуживают четыре менеджера; стоимость привлечения лида оценена от 1,5 до 3 тысяч рублей.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["4 менеджера", "стоимость лида", "1,5-3 тысячи"]),
    claim(43, 14, (221, 228), "SPEAKER_01", "Все лиды проходят консультацию; около 70% лидов доходят до КП, а продажа составляет 20-25%, максимум 27% от лидов.", "sales_process_claim", "sales_process", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["конверсия", "КП", "20-25%", "27%"]),
    claim(44, 15, (229, 234), "SPEAKER_01", "Технический расчет решения делает менеджер-специалист; предложение обычно готовится за день после консультации или бесплатного выезда.", "operational_claim", "operations", ["business_kb", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["технический расчет", "менеджер", "КП", "бесплатный выезд"]),
    claim(45, 15, (243, 248), "SPEAKER_01", "Есть дежурный менеджер и система распределения лидов; когда менеджер выезжает, он не может давать консультации, а из дома работает, если не дежурный.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["дежурный менеджер", "распределение лидов", "выезд"]),
    claim(46, 15, (248, 250), "SPEAKER_01", "Цепочка после КП: если клиента устраивает предложение, он приглашает на осмотр; выезд назван практически 100% продажей.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["КП", "осмотр", "выезд", "продажа"]),
    claim(47, 15, (256, 258), "SPEAKER_01", "Коммерческое предложение формируется быстро, потому что есть стандартные системы, подготовленная документация, схемы, листы настроек и КП по популярным комплектам.", "operational_claim", "operations", ["business_kb", "manager_training", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["КП", "стандартные системы", "схема", "лист настроек"]),
    claim(48, 16, (260, 262), "SPEAKER_01", "Схема сборки системы стандартная, а на осмотре заполняется лист осмотра с согласованием потребителей, автоматов и резервируемых цепей.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["схема сборки", "лист осмотра", "потребители", "автоматы"]),
    claim(49, 16, (262, 262), "SPEAKER_01", "Менеджер на осмотре обязан проверить соответствие мощности выбранных потребителей действительности; 2-5% накладок выясняются только на монтаже.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["осмотр", "мощность", "накладки", "2-5%"]),
    claim(50, 16, (266, 279), "SPEAKER_01", "Менеджеры работают с неравномерной нагрузкой, кучкуют выезды по поселкам, иногда есть очередь на осмотр, а при высокой нагрузке часть клиентов может недодавливаться.", "risk_or_constraint", "risk", ["business_kb", "manager_training", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["нагрузка менеджеров", "очередь", "выезды", "слив клиентов"]),
    claim(51, 16, (280, 285), "SPEAKER_01", "Монтажный ресурс описан как 8 монтажников по 2 в экипаже, то есть 4 бригады; часть систем продается без монтажа как вилка-розетка.", "operational_claim", "operations", ["business_kb", "strategy", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["монтажники", "бригады", "вилка-розетка"]),
    claim(52, 17, (288, 288), "SPEAKER_01", "В сложных случаях к техническому расчету подключаются монтажный отдел, инженер и технический директор; компания может потерять монтаж на 500-600 тысяч, если считает установку неправильной.", "risk_or_constraint", "risk", ["business_kb", "manager_training", "strategy"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review", "strategy_claim_review"], terms=["технический директор", "сложный случай", "отказ", "500-600 тысяч"]),
    claim(53, 17, (290, 292), "SPEAKER_01", "Монтаж выполняют собственные команды, а менеджер может вести одновременно 20-30 проектов, потому что это готовые решения, но важна работа по убеждению клиента.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["собственные команды", "20-30 проектов", "готовое решение"]),
    claim(54, 17, (293, 300), "SPEAKER_01", "Стандартная схема оплаты: минимальная предоплата 70% за оборудование, монтаж оплачивается после акта и ввода в эксплуатацию; без предоплаты выезжают редко и только до определенной суммы.", "business_model_claim", "business_model", ["business_kb", "manager_training", "strategy"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["предоплата", "70%", "акт", "ввод в эксплуатацию"]),
    claim(55, 18, (301, 310), "SPEAKER_01", "Основные статьи расходов - зарплата и реклама; в разговоре названы ориентиры 60-65% зарплата, 25% реклама, около 15% прочие офисные, складские и административные расходы.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["расходы", "зарплата", "реклама", "офис", "склад"]),
    claim(56, 18, (311, 324), "SPEAKER_01", "Компания живет без кредитов; инвестиционные расходы описаны как небольшие, в основном автомобили, а исследовательские разработки названы копейками.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["кредиты", "инвестиции", "автомобили", "R&D"]),
    claim(57, 19, (325, 337), "SPEAKER_01", "Главное ограничение роста сначала формулируется как качественные лиды, затем как емкость рынка, платежеспособность и осведомленность клиентов.", "strategy_claim", "strategy", ["business_kb", "strategy", "presentation"], "not_relevant", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["ограничение роста", "качественные лиды", "емкость рынка", "платежеспособность", "осведомленность"]),
    claim(58, 19, (338, 349), "SPEAKER_01", "Компания специально выбрала сегмент, где заняла доминирующее положение и отточила продукт; большой бизнес описан как кровавый океан, где компания не конкурентоспособна.", "positioning_claim", "positioning", ["business_kb", "strategy", "commercial_messaging"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["сегмент", "доминирующее положение", "кровавый океан", "большой бизнес"]),
    claim(59, 20, (350, 363), "SPEAKER_01", "Горизонтальное масштабирование в Казахстан или другие регионы упирается в филиальную модель, необходимость локального сильного руководителя и более низкую платежеспособность.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["Казахстан", "филиал", "платежеспособность", "локальный руководитель"]),
    claim(60, 20, (363, 365), "SPEAKER_01", "Компания пытается расширить свой сегмент между малым ИБП для компьютеров и крупными системами для ЦОДов, которые оба названы кровавыми океанами.", "strategy_claim", "strategy", ["business_kb", "strategy", "presentation"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["сегмент", "малые ИБП", "ЦОД", "расширение"]),
    claim(61, 21, (370, 383), "SPEAKER_01", "Основные конкуренты - около семи компаний в том же сегменте, небольшие инсталляторы и крупные дистрибьюторы, которые пробовали розницу, но уходили в дилерские продажи и маркетплейсы.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["конкуренты", "инсталляторы", "дистрибьюторы", "маркетплейсы"]),
    claim(62, 21, (384, 392), "SPEAKER_01", "Сделки у компании выигрывают либо ценой, либо умением обрабатывать богатых клиентов; конкуренты гибче и иногда ставят оборудование там, где Sveton не готов идти на риск.", "strategy_claim", "strategy", ["business_kb", "sales_training", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["конкуренты", "цена", "богатые клиенты", "гибкость", "риск"]),
    claim(63, 21, (393, 401), "SPEAKER_01", "Преимущества компании включают длительную работу, репутацию, собственную торговую марку и контроль качества поставщиков; товар низкого качества компания не продает даже при замороженном складе.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging", "presentation"], "needs_confirmation", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required", "public_use_review"], terms=["репутация", "торговая марка", "качество", "склад"]),
    claim(64, 21, (403, 405), "SPEAKER_01", "Клиенты могут выбрать конкурентов из-за задержек монтажа, низкой цены конкурента и более простых технических решений без обязательных элементов установки.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "strategy"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["задержка монтажа", "дешевле", "байпасный щит", "простое решение"]),
    claim(65, 22, (406, 412), "SPEAKER_01", "Альтернативное решение клиента - генератор; защитой бизнеса от копирования названы вложения в рекламу, которые у конкурентов в разы или на порядок меньше.", "strategy_claim", "strategy", ["business_kb", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["генератор", "копирование", "реклама", "конкуренты"]),
    claim(66, 22, (413, 420), "SPEAKER_01", "Приход конкурента с деньгами на рекламу признается риском; в ответ как защита названы репутация, собственные монтажники и переход в SMB как отдельное направление.", "risk_or_constraint", "risk", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["реклама", "репутация", "монтажники", "SMB"]),
    claim(67, 23, (421, 438), "SPEAKER_01", "SMB может быть выстроен как новый бизнес или новая компания, где прежние моральные обязательства по старой компании не распространяются автоматически.", "strategy_claim", "strategy", ["business_kb", "strategy", "review_only"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["SMB", "новая компания", "разделение бизнеса"]),
    claim(68, 23, (439, 443), "SPEAKER_01", "Вопрос, как связать регионы и филиалы с новым SMB-бизнесом, на момент интервью еще не продуман.", "open_question", "open_question", ["business_kb", "strategy", "review_only"], "not_relevant", "open_question", flags=["open_question", "strategy_claim_review"], open_question={"question": "Как регионы и филиалы должны соотноситься с новым SMB-бизнесом?", "why_open": "Дмитрий прямо говорит, что настолько не думал.", "needed_evidence": "Нужно отдельное стратегическое решение по оргструктуре и брендам."}, terms=["SMB", "регионы", "филиалы"]),
    claim(69, 24, (444, 449), "SPEAKER_01", "Оборот компании за последний год назван около 250 миллионов рублей, а маржинальность по товару - около 48%.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["оборот", "250 миллионов", "маржинальность", "48%"]),
    claim(70, 24, (451, 459), "SPEAKER_01", "Количество проектов сильно сезонно: в низкий сезон может быть один монтаж в неделю; при этом остаются сервис и внутренняя работа, но вопрос загрузки людей не решен полностью.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["сезонность", "низкий сезон", "сервис", "загрузка"]),
    claim(71, 24, (460, 466), "SPEAKER_01", "Пиковые 20 монтажей в день воспринимаются как 120% нагрузки, а задача компании - за 9 месяцев накопить запас, чтобы пройти 1-3 низких месяца.", "business_model_claim", "business_model", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["пиковая нагрузка", "120%", "жирок", "низкий сезон"]),
    claim(72, 25, (467, 472), "SPEAKER_01", "Для SMB есть надежда, что сезонность будет другой или со сдвигом, потому что бизнес может думать об улучшениях весной и переносить решения между сезонами.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "hypothesis", flags=["strategy_claim_review"], terms=["SMB", "сезонность", "поведение бизнеса"]),
    claim(73, 25, (473, 478), "SPEAKER_01", "Бизнес рос неравномерно: за последние 5 лет были годы с ростом 5% и 40%; штат примерно включает 8-9 монтажников, 3 технических специалиста, административный персонал и директоров.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["рост", "штат", "монтажники", "технические специалисты"]),
    claim(74, 26, (479, 483), "SPEAKER_01", "Через три года компания хочет быть больше, прибыльнее и развивать новые направления: регионы/филиалы, новые сегменты и новые продукты.", "strategy_claim", "strategy", ["business_kb", "strategy", "presentation"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["трехлетняя цель", "новые направления", "регионы", "продукты"]),
    claim(75, 26, (486, 488), "SPEAKER_01", "Одна из продуктовых проблем инверторов - шум вентилятора из-за отвода тепла; это важно для домов без изолированного технического помещения.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["инвертор", "шум", "вентилятор", "техническое помещение"]),
    claim(76, 26, (490, 495), "SPEAKER_01", "Помимо инверторов и аккумуляторов компания продает стабилизаторы примерно в 5% продаж; потенциальная ниша - заказное производство стабилизаторов, но для него нужны деньги и объемы от 10 тысяч единиц в год.", "strategy_claim", "strategy", ["business_kb", "strategy", "review_only"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review", "strategy_claim_review"], terms=["стабилизаторы", "5% продаж", "OEM", "10 тысяч единиц"]),
    claim(77, 27, (496, 500), "SPEAKER_01", "План по регионам осторожный: сначала один регион, возможно два; правильной точкой с точки зрения платежеспособности назван Сочи.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["регион", "Сочи", "масштабирование"]),
    claim(78, 27, (501, 508), "SPEAKER_01", "Московский сервисный радиус ограничен примерно 130 км от МКАД; дальние выезды вроде Рязани дороги, потому что два человека и машина тратят около двух дней, а сервисный выезд должен стоить минимум 20 тысяч.", "operational_claim", "operations", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["сервисный радиус", "130 км", "Рязань", "20 тысяч"]),
    claim(79, 27, (509, 516), "SPEAKER_01", "Идеальная модель масштабирования - партнеры или франшизы, но из-за технического уровня и сложности бизнеса рабочей моделью видятся филиалы.", "strategy_claim", "strategy", ["business_kb", "strategy", "presentation"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["франшиза", "партнеры", "филиал", "масштабирование"]),
    claim(80, 28, (517, 521), "SPEAKER_01", "Одна из главных задач компании - совершенствовать технический потенциал: готовить монтажников в инженера и мастера, потому что экспертность нужно поддерживать.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["технический потенциал", "инженер", "мастер", "экспертность"]),
    claim(81, 28, (522, 529), "SPEAKER_01", "После 2022 года была серьезная проблема с поиском менеджеров; текущие менеджеры работают давно, но решение о найме еще одного человека откладывается до июня из-за неопределенности малого бизнеса.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["менеджеры", "найм", "2022", "июнь", "малый бизнес"]),
    claim(82, 29, (531, 535), "SPEAKER_01", "В ближайший год желательно расширять технические и организационные решения; приоритеты развития - филиалы, продажи в регионах и продукт, который может поставить электрик под руководством компании.", "strategy_claim", "strategy", ["business_kb", "strategy", "electricians_kb"], "needs_confirmation", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["регионы", "филиалы", "электрик", "продукт как Икеа"]),
    claim(83, 30, (539, 544), "SPEAKER_01", "Одно из направлений развития - AI-агенты для прогрева аудитории на сайте или в чате, чтобы менеджеры меньше тратили время на объяснение простых вещей неподготовленным клиентам.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["AI-агенты", "прогрев аудитории", "чат", "менеджеры"]),
    claim(84, 31, (546, 551), "SPEAKER_01", "Маркетинг ведется через директ, SEO/SERM и ВКонтакте; ВКонтакте почти не дает лидов напрямую, но используется для прогрева аудитории.", "marketing_message", "marketing", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["Директ", "SEO", "SERM", "ВКонтакте", "прогрев"]),
    claim(85, 31, (548, 551), "SPEAKER_01", "Канал живого общения вокруг системы малоперспективен, потому что продукт утилитарный: клиент хочет поставить и забыть, а не долго обсуждать его в сообществе.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "strategy_claim_review"], terms=["утилитарный продукт", "поставил и забыл", "сообщество"]),
    claim(86, 31, (551, 551), "SPEAKER_01", "Ретаргетинг предлагается строить на поведении: если человек просмотрел большую часть основной страницы, его нужно преследовать промо-страницами как заинтересованного клиента.", "sales_process_claim", "sales_process", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["marketing_claim_review", "strategy_claim_review"], terms=["ретаргетинг", "промо-страницы", "80% страницы", "заинтересованный клиент"]),
    claim(87, 32, (557, 559), "SPEAKER_01", "По потенциальному лиду из окружения Сергея договорились проверить ситуацию и при наличии зацепки организовать выезд Сергея для разговора и ответов на вопросы.", "sales_process_claim", "sales_process", ["business_kb", "manager_training", "review_only"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["лид", "выезд", "проверка зацепки"]),
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

    skipped = {
        "interview_002_chunk_0001": [
            {
                "source_quote": chunk_by_id["interview_002_chunk_0001"]["text"],
                "reason": "noise",
                "notes": "Screen sharing and setup before the substantive interview.",
            }
        ]
    }

    results = []
    for chunk in chunks:
        chunk_id = chunk["chunk_id"]
        claims = by_chunk.get(chunk_id, [])
        skipped_items = skipped.get(chunk_id, [])
        results.append(
            {
                "source_chunk_id": chunk_id,
                "coverage_summary": {
                    "meaningful_items_seen": len(claims) + len(skipped_items),
                    "claims_extracted": len(claims),
                    "open_questions_found": sum(1 for item in claims if item["claim_type"] == "open_question"),
                    "noise_or_transition_items": len(skipped_items) if chunk["chunk_status"] == "excluded" else 0,
                    "coverage_notes": (
                        "Excluded setup transition."
                        if chunk["chunk_status"] == "excluded"
                        else "Full interview_002 extraction; meaningful business items extracted as source-backed claims."
                    ),
                },
                "skipped_source_items": skipped_items,
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
