#!/usr/bin/env python3
"""Build full-control extraction artifacts for interview_001.

The claim specs below intentionally reference transcript line ranges instead of
copying quotes by hand. This keeps source_quote exact and auditable.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = "00_input/interviews/260405_sveton_converted_t_large-v3_diar.txt"
SOURCE_PATH = ROOT / SOURCE_FILE
CHUNKS_PATH = ROOT / "00_input/interviews/chunks/interview_001_chunks.jsonl"
OUT_CLAIMS = ROOT / "00_input/interviews/statements/interview_001_claims.jsonl"
OUT_RESULTS = ROOT / "00_input/interviews/statements/interview_001_extraction_results.jsonl"

ROLES = {
    "SPEAKER_00": ("Дмитрий", "генеральный директор Светон"),
    "SPEAKER_01": ("Дмитрий", "генеральный директор Светон"),
    "SPEAKER_02": ("Сергей", "директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели"),
    "SPEAKER_03": ("Сергей", "директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели"),
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
    source_lines = SOURCE_LINES
    start_line, end_line = line_range
    start_ts, end_ts = ts_for_lines(source_lines, start_line, end_line)
    identity, role = ROLES[speaker]
    return {
        "claim_id": f"interview_claim_001{seq:03d}",
        "claim": claim_text,
        "claim_type": claim_type,
        "source_interview_id": "interview_001",
        "source_file": SOURCE_FILE,
        "source_chunk_id": f"interview_001_chunk_{chunk_index:04d}",
        "speaker_label": speaker,
        "speaker_identity": identity,
        "speaker_role": role,
        "speaker_mapping_confidence": "confirmed",
        "start_timestamp": start_ts,
        "end_timestamp": end_ts,
        "source_quote": "\n".join(source_lines[start_line - 1 : end_line]),
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


SOURCE_LINES = SOURCE_PATH.read_text(encoding="utf-8-sig").splitlines()

SPECS: list[dict[str, Any]] = [
    # 0001: branch strategy
    claim(1, 1, (2, 4), "SPEAKER_01", "В начале интервью выделены три направления: E-agent, развитие ИВП для малого и среднего бизнеса, и филиальная тема.", "strategy_claim", "strategy", ["business_kb", "strategy", "presentation"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["E-agent", "ИВП", "малый бизнес", "средний бизнес", "филиал"]),
    claim(2, 1, (5, 8), "SPEAKER_01", "Для запуска филиала важны платежеспособный спрос, особенности ведения бизнеса и невозможность дотянуться до удаленного рынка из центра.", "strategy_claim", "strategy", ["business_kb", "strategy"], "context_only", "source_backed", confidence="medium", flags=["strategy_claim_review", "recognition_noise"], terms=["филиал", "платежеспособный спрос", "региональный рынок"]),
    claim(3, 1, (9, 13), "SPEAKER_01", "Одна продажа в месяц может считаться хорошим стартовым результатом для филиала.", "business_model_claim", "business_model", ["business_kb", "strategy", "manager_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["филиал", "одна продажа в месяц", "масштабируемая модель"]),
    claim(4, 1, (15, 16), "SPEAKER_01", "Потенциальный региональный партнер часто уже занимается электрикой или монтажом и выходит на самостоятельную работу, включая продажи.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "manager_training"], "directly_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["региональный партнер", "электрик", "монтажник"]),

    # 0002: foreman channel
    claim(5, 2, (17, 18), "SPEAKER_01", "Прораб является потенциальным каналом, потому что он координирует стройку и знает поставщиков/монтажников по инженерным системам.", "partner_model_claim", "partner_model", ["business_kb", "sales_training", "strategy"], "context_only", "source_backed", review_status="extracted", terms=["прораб", "инженерные системы", "партнерский канал"]),
    claim(6, 2, (18, 20), "SPEAKER_01", "Инженерные системы для прораба являются дополнительным заработком, даже если он не специалист по каждой системе.", "partner_model_claim", "partner_model", ["business_kb", "sales_training", "manager_training"], "context_only", "source_backed", review_status="extracted", terms=["прораб", "дополнительный заработок", "инженерия"]),
    claim(7, 2, (21, 21), "SPEAKER_01", "Компания хочет находить прорабов, которые могут предлагать клиенту систему бесперебойного электроснабжения.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["прораб", "система бесперебойного электроснабжения", "канал продаж"]),
    claim(8, 2, (23, 27), "SPEAKER_01", "Партнер может работать по агентской схеме: передавать клиента компании, получать меньший процент и не выполнять операционную работу.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "sales_training"], "context_only", "example_case", flags=["strategy_claim_review"], terms=["агентская схема", "прораб", "партнерский процент"]),
    claim(9, 2, (28, 30), "SPEAKER_01", "Осведомленность о бесперебойном электроснабжении значительно ниже, чем о септиках и очистке воды; в интервью названа оценка около 5%.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "commercial_messaging", "strategy"], "context_only", "speaker_opinion", confidence="medium", flags=["strategy_claim_review", "price_or_guarantee_review", "marketing_claim_review"], terms=["осведомленность", "бесперебойка", "септик", "очистка воды"], notes="Процент является оценкой из интервью."),

    # 0003: modern home and foreman influence
    claim(10, 3, (31, 35), "SPEAKER_01", "Современный загородный дом зависит от электричества: септик, котел, насос, вода и бытовой комфорт перестают работать при отключении.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["современный дом", "септик", "котел", "насос", "отключение электричества"]),
    claim(11, 3, (34, 36), "SPEAKER_01", "Клиентская боль может отличаться: для одних важна защита от разморозки, для других вода, насос или туалет при гостях.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "sales_script"], "context_only", "speaker_opinion", flags=["marketing_claim_review"], terms=["клиентская боль", "разморозка", "вода", "насос"]),
    claim(12, 3, (41, 43), "SPEAKER_01", "Если клиент доверяет прорабу выбор монтажников и материалов, прораб может предложить один-два варианта или конкретное решение.", "partner_model_claim", "partner_model", ["business_kb", "sales_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["прораб", "доверие клиента", "выбор решения"]),
    claim(13, 3, (44, 50), "SPEAKER_01", "Для клиента инженерные системы могут выглядеть одинаково, поэтому выбор сильно зависит от прораба, который знает клиента и его бюджет.", "partner_model_claim", "partner_model", ["business_kb", "sales_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["прораб", "бюджет клиента", "выбор клиента"]),
    claim(14, 3, (50, 50), "SPEAKER_01", "Возможны две рабочие схемы продажи через прораба: прораб договаривается и передает параметры, либо клиент договаривается сам, а установка согласуется с прорабом.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "sales_script"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["прораб", "схема продажи", "монтаж"]),

    # 0004: market context and channel goal
    claim(15, 4, (54, 60), "SPEAKER_01", "В регионах есть компании, связанные с бесперебойкой, но их мало; солнечные компании обычно не предлагают чистую бесперебойку.", "strategy_claim", "strategy", ["business_kb", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["региональный рынок", "солнечная энергетика", "чистая бесперебойка"]),
    claim(16, 4, (61, 66), "SPEAKER_01", "Рынок очистки воды в разговоре оценивается как в 5-10 раз больше домашнего ИБП, потому что проблему воды клиенты воспринимают как более неизбежную.", "strategy_claim", "strategy", ["business_kb", "strategy"], "context_only", "speaker_opinion", confidence="medium", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["рынок очистки воды", "ИБП для дома", "размер рынка"]),
    claim(17, 4, (68, 75), "SPEAKER_02", "Для южного филиала сформулированы две разные задачи: создать масштабируемую модель филиалов и найти более эффективный канал выхода на новый сегмент.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["масштабируемая модель", "канал продаж", "новый сегмент"]),
    claim(18, 4, (71, 72), "SPEAKER_01", "Канал через прорабов точнее описан не как прямой канал продаж, а как канал, который подталкивает клиента обратиться в компанию.", "partner_model_claim", "partner_model", ["business_kb", "sales_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["канал обращения", "прораб", "лидогенерация"]),

    # 0005: training and red book
    claim(19, 5, (84, 85), "SPEAKER_01", "В компании существует закрытая управленческая система работы менеджера, называемая «Красная книга».", "operational_claim", "operations", ["business_kb", "manager_training", "review_only"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["Красная книга", "система работы менеджера"]),
    claim(20, 5, (86, 93), "SPEAKER_01", "Для разговора с людьми в филиальной модели новому сотруднику не нужно недельное глубокое обучение, но нужна достаточная техническая грамотность и понимание темы.", "operational_claim", "operations", ["business_kb", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["обучение", "филиал", "техническая грамотность"]),
    claim(21, 5, (93, 93), "SPEAKER_01", "Базовый бытовой опыт с электрикой воспринимается как полезный признак при обучении менеджера.", "qualification_question", "qualification", ["manager_training", "sales_training"], "directly_relevant", "speaker_opinion", flags=[], discovery_question={"question": "Есть ли у кандидата базовый бытовой опыт с электрикой?", "why_it_matters": "Это показывает стартовый уровень технической грамотности.", "answer_changes": "При наличии опыта можно быстрее переходить к продуктовым и монтажным нюансам."}, terms=["кандидат", "техническая грамотность", "обучение"]),
    claim(22, 5, (95, 101), "SPEAKER_01", "Для партнера-прораба одна продажа требует не только монтажного времени, но и звонков/убеждения; это влияет на оценку нагрузки.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["прораб", "нагрузка", "звонки", "убеждение"]),

    # 0006: installer competence
    claim(23, 6, (102, 106), "SPEAKER_01", "Даже если монтаж кажется простым, нельзя постоянно делать все самому; нужен обученный монтажник или партнер.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["монтажник", "обучение", "масштабирование"]),
    claim(24, 6, (107, 112), "SPEAKER_01", "Монтаж содержит практические нюансы: сверление, крошение материала, скрытые трубы и электричество в стене.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "recognition_noise"], terms=["монтаж", "сверление", "скрытые коммуникации"]),
    claim(25, 6, (121, 127), "SPEAKER_01", "Переборка щита названа примерно 30% работы по инсталляции системы.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", confidence="medium", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["переборка щита", "инсталляция", "30%"]),
    claim(26, 6, (129, 132), "SPEAKER_01", "При однофазной системе 5 кВт в трехфазном доме монтажник должен перераспределить нагрузки и сбалансировать фазы.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["3 фазы", "5 кВт", "балансировка фаз"]),
    claim(27, 6, (133, 133), "SPEAKER_01", "Нового монтажника отправляют на один-два монтажа, чтобы он сначала наблюдал процесс.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "context_only", "source_backed", flags=[], terms=["обучение монтажника", "полевое обучение"]),

    # 0007: discovery and generator objection
    claim(28, 7, (135, 140), "SPEAKER_01", "Для этой тематики нужно искать человека с реальной болью; большинство знает не о системах, а о своей проблеме.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "sales_script"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["поиск клиента", "боль клиента", "осведомленность"]),
    claim(29, 7, (141, 144), "SPEAKER_01", "Возражение про генератор требует учитывать, кто в доме реально сможет запускать и обслуживать генератор.", "objection", "objection_handling", ["sales_training", "objection_handling", "sales_script"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "public_use_review"], objection={"objection_category": "generator_alternative", "customer_assumption": "Генератор может быть простой заменой бесперебойной системе.", "recommended_response": "Уточнить, кто будет запускать, контролировать и обслуживать генератор при отключениях."}, terms=["генератор", "возражение", "эксплуатация"]),
    claim(30, 7, (146, 151), "SPEAKER_01", "Хорошие китайские генераторы в разговоре описаны как редкие и стоящие на уровне хороших европейских или японских.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "objection_handling"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["генератор", "китайские генераторы", "цена"]),
    claim(31, 7, (153, 157), "SPEAKER_01", "Дешевый бензиновый генератор может иметь ограниченный ресурс и требовать обслуживания, включая замену масла.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "objection_handling"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["генератор", "ресурс", "ТО", "масло"]),
    claim(32, 7, (158, 158), "SPEAKER_01", "Генератор признается хорошим решением при качественном оборудовании и наличии механика/обслуживания.", "recommended_response", "objection_handling", ["sales_training", "objection_handling", "sales_script"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "price_or_guarantee_review"], objection={"objection_category": "generator_alternative", "customer_assumption": "Генератора достаточно вместо ИБП.", "recommended_response": "Согласиться, что генератор подходит при качественном оборудовании, регулярном обслуживании и готовности платить за ТО."}, terms=["генератор", "ТО", "обслуживание"]),

    # 0009-0012: positioning and differentiators
    claim(33, 9, (176, 187), "SPEAKER_02", "Переход к бесперебойным электрическим решениям сравнивается с переходом от ДВС к электромобилям: люди готовы платить за удобство и комфорт, но автономные сценарии требуют генератора, солнца, ветра или ДВС.", "strategy_claim", "strategy", ["business_kb", "commercial_messaging", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review", "technical_confirmation_required"], terms=["удобство", "комфорт", "автономка", "генератор"]),
    claim(34, 9, (188, 194), "SPEAKER_02", "Для продаж нужна лаконичная elevator pitch формулировка: аудитория, проблема, технология и секретный соус в одном абзаце.", "sales_process_claim", "sales_process", ["sales_training", "sales_script", "presentation"], "not_relevant", "speaker_opinion", flags=["marketing_claim_review"], terms=["elevator pitch", "позиционирование", "секретный соус"]),
    claim(35, 10, (195, 202), "SPEAKER_01", "Компания продает услугу бесперебойного электроснабжения, а не просто товар или систему.", "positioning_claim", "positioning", ["business_kb", "sales_training", "website", "brochure", "presentation", "commercial_messaging"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "public_use_review"], terms=["услуга", "бесперебойное электроснабжение", "позиционирование"]),
    claim(36, 10, (197, 200), "SPEAKER_01", "Целевой сегмент описан как верхний уровень среднего класса, нижний уровень бизнес-класса, владельцы домов/дач и верх малого бизнеса.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training", "strategy", "commercial_messaging"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["средний класс", "бизнес-класс", "владельцы домов", "малый бизнес"]),
    claim(37, 10, (199, 202), "SPEAKER_01", "Решаемая проблема сформулирована как кратковременные перерывы электроснабжения до 10-12 часов.", "value_proposition_claim", "value_proposition", ["business_kb", "sales_training", "commercial_messaging"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "marketing_claim_review", "price_or_guarantee_review"], terms=["перерывы электроснабжения", "10-12 часов", "резерв"]),
    claim(38, 10, (202, 202), "SPEAKER_01", "Сервисная ценность включает расчет ровно того, что нужно клиенту, потому что клиент сам может неправильно оценить потребность.", "value_proposition_claim", "value_proposition", ["business_kb", "sales_training", "sales_script"], "context_only", "speaker_opinion", flags=["marketing_claim_review"], terms=["расчет системы", "потребность клиента", "сервис"]),
    claim(39, 10, (205, 206), "SPEAKER_01", "Дом описан как сложное инженерное сооружение, которому требуется постоянное электроснабжение для мониторинга, видеонаблюдения, отопления, септика, скважины и охраны.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["инженерный дом", "видеонаблюдение", "отопление", "септик", "скважина"]),
    claim(40, 10, (208, 209), "SPEAKER_01", "Инверторная технология описана как запасание энергии в аккумуляторах при наличии сети и бесшовная выдача потребителям при отсутствии сети.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["инверторная технология", "аккумуляторы", "бесшовная работа"]),
    claim(41, 11, (210, 213), "SPEAKER_01", "Секретный соус не в самой технологии, а в том, как система собирается, из каких элементов и с каким качеством исполнения.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging", "presentation"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "public_use_review"], terms=["секретный соус", "сборка", "качество"]),
    claim(42, 11, (214, 220), "SPEAKER_01", "Отличие компании формулируется как гарантия качества, надежности и того, что клиента не бросят.", "positioning_claim", "positioning", ["business_kb", "sales_training", "website", "brochure", "commercial_messaging"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "public_use_review", "price_or_guarantee_review"], terms=["качество", "надежность", "не бросим клиента"]),
    claim(43, 11, (221, 227), "SPEAKER_01", "Грамотное объяснение за 15 минут может сформировать доверие и снизить мотивацию клиента искать другие предложения.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "sales_script"], "not_relevant", "speaker_opinion", flags=["marketing_claim_review", "recognition_noise"], terms=["доверие", "объяснение", "продажа"]),
    claim(44, 12, (228, 235), "SPEAKER_01", "Собственные стеллажи, аккуратная компоновка, кабели и эстетика используются как продуктовая дифференциация.", "product_claim", "product", ["business_kb", "sales_training", "presentation", "commercial_messaging"], "needs_confirmation", "speaker_opinion", confidence="medium", flags=["technical_confirmation_required", "marketing_claim_review", "recognition_noise"], terms=["стеллаж", "эстетика", "компоновка", "кабели"]),
    claim(45, 12, (235, 236), "SPEAKER_01", "Желание клиента закрыть систему красивым шкафом может конфликтовать с вентиляцией и отводом тепла.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "sales_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["закрытый шкаф", "вентиляция", "отвод тепла", "перегрев"]),

    # 0013-0018: monitoring and feedback
    claim(46, 13, (237, 241), "SPEAKER_01", "В компании был собственный проект мониторинга инверторов на базе протокола и Wi-Fi чипа; он дошел примерно до 80% готовности и был заброшен.", "product_claim", "product", ["business_kb", "strategy", "review_only"], "needs_confirmation", "source_backed", confidence="medium", flags=["technical_confirmation_required", "strategy_claim_review", "recognition_noise"], terms=["мониторинг", "инвертор", "Wi-Fi чип", "протокол"]),
    claim(47, 13, (250, 256), "SPEAKER_01", "Китайские системы мониторинга дают приложения, но могут не отвечать на конкретно нужные клиенту сценарии, например уведомление об отключении электричества.", "product_claim", "product", ["business_kb", "strategy", "sales_training"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "marketing_claim_review", "recognition_noise"], terms=["китайские приложения", "мониторинг", "уведомление"]),
    claim(48, 13, (258, 266), "SPEAKER_01", "Инверторный протокол может быть доступен, но данные через Wi-Fi коробочку и китайский сервер создают проблему доступа к информации.", "technical_claim_needs_confirmation", "technical_context", ["review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "recognition_noise"], terms=["протокол", "Wi-Fi коробочка", "китайский сервер"]),
    claim(49, 14, (267, 269), "SPEAKER_01", "Клиенту в мониторинге прежде всего нужны два ответа: есть ли внешнее электричество и сколько осталось энергии в аккумуляторах.", "value_proposition_claim", "value_proposition", ["business_kb", "sales_training", "commercial_messaging", "content_bank"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "public_use_review"], terms=["мониторинг", "электричество", "остаток энергии"]),
    claim(50, 14, (271, 273), "SPEAKER_01", "Простая SMS/GPRS-розетка с уведомлением о пропаже электричества описана как решение основной клиентской потребности.", "product_claim", "product", ["business_kb", "strategy", "review_only"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "price_or_guarantee_review", "marketing_claim_review"], terms=["SMS-розетка", "GPRS", "уведомление"]),
    claim(51, 14, (274, 276), "SPEAKER_01", "Продукт может быть технически хорошим, но не нужен клиенту, если опережает его реальную потребность.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["потребность клиента", "стартап", "product-market fit"]),
    claim(52, 14, (287, 293), "SPEAKER_01", "Компания не может отдавать клиентам сырой мониторинг, потому что сбой вызывает недовольство и противоречит позиционированию надежности.", "risk_or_constraint", "risk", ["business_kb", "manager_training", "strategy", "review_only"], "needs_confirmation", "source_backed", confidence="medium", flags=["recognition_noise", "technical_confirmation_required", "marketing_claim_review"], terms=["сырой продукт", "мониторинг", "надежность", "репутация"]),
    claim(53, 14, (295, 297), "SPEAKER_01", "Собственный проект мониторинга был закрыт в 2021 году, а спустя несколько лет китайские приложения стали лучше.", "strategy_claim", "strategy", ["business_kb", "strategy", "review_only"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["мониторинг", "2021", "китайские приложения"]),
    claim(54, 15, (298, 306), "SPEAKER_01", "В приложениях инверторов много данных, но для клиента и сервиса важнее фиксировать ошибки и события в момент проблемы, а не просто показывать текущую картинку.", "product_claim", "product", ["business_kb", "manager_training", "strategy"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["приложение инвертора", "ошибки", "события", "мониторинг"]),
    claim(55, 15, (319, 326), "SPEAKER_01", "Модели прямых сделок энергией внутри сети обсуждаются как интересные, но в российских условиях ограничены старыми сетями и юридическими проблемами.", "strategy_claim", "strategy", ["business_kb", "strategy", "review_only"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["энергосети", "прямые сделки", "юридические проблемы"]),
    claim(56, 16, (330, 331), "SPEAKER_01", "Компания раньше поставляла комплекты качественного оборудования в удаленные регионы и собирала системы до последнего элемента для отправки.", "operational_claim", "operations", ["business_kb", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["удаленные регионы", "комплект оборудования", "отправка"]),
    claim(57, 16, (333, 340), "SPEAKER_01", "Потребность в SMS-уведомлениях сформулирована как гипотеза, основанная на опыте менеджеров и надежности канала, но без достаточной статистики опросов.", "strategy_claim", "strategy", ["business_kb", "strategy", "review_only"], "context_only", "speaker_opinion", confidence="medium", flags=["strategy_claim_review", "marketing_claim_review", "recognition_noise"], terms=["SMS", "гипотеза", "опрос клиентов", "менеджеры"]),
    claim(58, 16, (342, 348), "SPEAKER_01", "После монтажа есть обязательный контрольный звонок примерно через неделю, но регулярные опросы клиентов после продажи не ведутся.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["контрольный звонок", "опрос клиентов", "постпродажа"]),
    claim(59, 17, (349, 356), "SPEAKER_01", "Компания работала через ВК и email-рассылки, но не использовала холодные личные сообщения клиентам.", "operational_claim", "operations", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["ВК", "email", "клиентские коммуникации"]),
    claim(60, 17, (357, 362), "SPEAKER_02", "Опрос клиентов можно строить не как генерацию негатива, а как короткие вопросы для понимания потребностей и проверки идей продукта.", "qualification_question", "qualification", ["business_kb", "manager_training", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], discovery_question={"question": "Что клиенту не хватает и нужны ли ему новые функции вроде мобильного приложения?", "why_it_matters": "Без обратной связи продуктовые идеи остаются гипотезами.", "answer_changes": "Ответы помогают решить, развивать ли приложение, SMS или другие постпродажные функции."}, terms=["опрос клиентов", "обратная связь", "мобильное приложение"]),
    claim(61, 17, (363, 369), "SPEAKER_01", "Wi-Fi мониторинг вызывает сервисные проблемы: клиенты меняют роутер или пароль, сигнал не добивает до технического помещения, а дисклеймеры не решают ожидание «чтобы работало».", "risk_or_constraint", "risk", ["business_kb", "manager_training", "review_only"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["Wi-Fi мониторинг", "роутер", "дисклеймер", "техническое помещение"]),
    claim(62, 18, (370, 375), "SPEAKER_01", "Модель мониторинга рассматривалась как год бесплатного использования и затем 500 рублей в год, но разработка и сопровождение оценивались примерно в 2,5 млн рублей за полтора года.", "strategy_claim", "strategy", ["business_kb", "strategy", "review_only"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["мониторинг", "абонентка", "2,5 млн", "500 рублей"]),
    claim(63, 18, (376, 379), "SPEAKER_02", "Мониторинг может быть не прямой болью клиента, а способом компании доказать ценность после продажи и повысить лояльность.", "value_proposition_claim", "value_proposition", ["business_kb", "sales_training", "manager_training", "commercial_messaging"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "public_use_review"], terms=["постпродажа", "лояльность", "доказательство ценности"]),
    claim(64, 18, (383, 385), "SPEAKER_02", "Китайские приложения не позволяют персональные коммуникации от компании, опросы или сервисные сообщения поверх базового функционала.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["китайские приложения", "персональные коммуникации", "опросы"]),
    claim(65, 19, (388, 391), "SPEAKER_01", "Зависимость от внешних приложений несет риск блокировки: приведен пример китайского приложения, которое перестало работать на мобильных сетях после блокировки РКН.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["РКН", "блокировка", "мобильные сети", "загородные сети"]),
    claim(66, 19, (394, 395), "SPEAKER_02", "В цикле продажи и постпродажи узким местом названа неидеальная обратная связь.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["обратная связь", "цикл продажи", "постпродажа"]),
    claim(67, 19, (395, 405), "SPEAKER_01", "Модель Hydrawell отличается регулярным ТО, SMS-напоминаниями, агрессивной рекламой и сервисной выручкой, тогда как у Sveton системы продаются как не требующие регулярного ТО.", "strategy_claim", "service_model", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review", "price_or_guarantee_review"], terms=["Hydrawell", "ТО", "SMS", "сервисная выручка"]),
    claim(68, 19, (406, 410), "SPEAKER_01", "Sveton привлекает клиентов более спокойным подходом: обещанием забыть о головной боли на годы, но массовое ТО потребовало бы много машин и монтажников.", "strategy_claim", "strategy", ["business_kb", "sales_training", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review", "price_or_guarantee_review", "technical_confirmation_required"], terms=["без ТО", "головная боль", "монтажники", "сервис"]),

    # 0020-0024: technical/product/operations close
    claim(69, 20, (411, 413), "SPEAKER_01", "Компания не может точно сказать, что клиенту не нравится или что он хотел бы дополнительно, но знает проблему деградации свинцово-кислотных аккумуляторов.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["обратная связь", "свинцовые аккумуляторы", "деградация"]),
    claim(70, 20, (413, 413), "SPEAKER_01", "Свинцово-кислотные аккумуляторы описаны как работающие хорошо около двух лет, после чего деградация становится заметной; литий описан как существенно менее деградирующий.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["свинцово-кислотные аккумуляторы", "литий", "деградация"]),
    claim(71, 20, (419, 425), "SPEAKER_01", "В личном кейсе с малым UPS проблема после замены аккумулятора может быть связана не с новым аккумулятором, а с электроникой и недозарядом.", "technical_claim_needs_confirmation", "technical_context", ["review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["UPS", "аккумулятор", "электроника", "недозаряд"]),
    claim(72, 20, (432, 435), "SPEAKER_01", "Упомянут компактный инвертор со встроенными батареями на 1000 Вт⋅ч и возможностью подключения солнечной панели, с себестоимостью 16 тысяч.", "product_claim", "product", ["business_kb", "strategy", "review_only"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["1000 Вт⋅ч", "инвертор", "солнечная панель", "себестоимость"]),
    claim(73, 20, (436, 445), "SPEAKER_02", "Для малого сценария квартиры или села потребность формулируется как резерв 2-4 часа для сервера, роутера и интернета.", "sales_case", "sales_process", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "example_case", flags=["technical_confirmation_required", "price_or_guarantee_review"], sales_case={"customer_type": "малый личный/домашний IT-сценарий", "problem_situation": "Нужно обеспечить работу сервера, роутера и интернета при отключении электричества.", "diagnosis_path": "Уточнить мощность мини-ПК, роутера и ожидаемую длительность отключения.", "proposed_action": "Подобрать компактный UPS/инвертор на 2-4 часа резерва.", "risk_or_caveat": "Технические параметры требуют расчета."}, terms=["сервер", "роутер", "2-4 часа", "UPS"]),
    claim(74, 21, (446, 458), "SPEAKER_02", "Менеджерам нужен канонический абзац и отточенная pitch-презентация, потому что длинное объяснение перегружает клиента.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "sales_script", "presentation"], "not_relevant", "speaker_opinion", flags=["marketing_claim_review"], terms=["канонический абзац", "pitch", "менеджеры"]),
    claim(75, 21, (450, 456), "SPEAKER_02", "Качество позиционирования можно проверить экспериментом: спросить менеджеров, что компания продает и чем отличается.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "strategy"], "not_relevant", "speaker_opinion", flags=[], discovery_question={"question": "Что мы продаем и чем отличаемся?", "why_it_matters": "Ответ показывает единство и убедительность позиционирования.", "answer_changes": "Если ответы расходятся, нужен единый sales script."}, terms=["позиционирование", "менеджеры", "эксперимент"]),
    claim(76, 21, (465, 469), "SPEAKER_01", "Hydrawell-приложение не используется, потому что оно заточено на сервис; внедрение своего приложения ограничено старой 1С, стоимостью и сроком около года.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["Hydrawell", "мобильное приложение", "1С", "стоимость внедрения"]),
    claim(77, 21, (469, 470), "SPEAKER_01", "Для монтажников выбрано приложение Planada, которое планируется интегрировать быстрее, примерно за месяц.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["Planada", "монтажники", "интеграция"]),
    claim(78, 22, (471, 479), "SPEAKER_01", "Компании нужна функциональная карта и управленческий/бизнес/финансовый анализ, чтобы понимать, расширяет ли управленческий поворот возможности или сужает их.", "operational_claim", "operations", ["business_kb", "strategy", "manager_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["функциональная карта", "управленческий анализ", "финансовый анализ"]),
    claim(79, 22, (481, 487), "SPEAKER_01", "Типовая ERP/1С закрывает базовый функционал, но для аналитики и новых форм нужны доработки, за которые компания платит 50-200 тысяч рублей в месяц.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["ERP", "1С", "аналитика", "доработки"]),
    claim(80, 22, (487, 493), "SPEAKER_01", "Planada как стороннее мобильное приложение интегрируется с 1С/ERP через API или доработки.", "operational_claim", "operations", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["Planada", "1С", "API", "ERP"]),
    claim(81, 23, (494, 501), "SPEAKER_01", "Компания постоянно улучшает оборудование и внутренние документы на основе экспериментов, гарантийных и негарантийных выездов.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["улучшение", "гарантийные выезды", "внутренние документы"]),
    claim(82, 23, (494, 497), "SPEAKER_01", "Снижение себестоимости и коммерческое давление могут привести к ненадежной конфигурации, что затем дает проблемы и опыт для корректировки.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review", "strategy_claim_review"], terms=["себестоимость", "аккумуляторы", "надежность", "проблемы"]),
    claim(83, 23, (503, 507), "SPEAKER_01", "Системы стандартизированы на складские блоки, которые собираются заранее и уменьшают объем сборки на объекте.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["стандартизация", "блоки", "складская сборка", "монтаж"]),
    claim(84, 23, (506, 509), "SPEAKER_01", "Компактная стойка разработана из-за нехватки места у клиентов и отличается меньшим габаритом относительно оборудования.", "product_claim", "product", ["business_kb", "sales_training", "presentation"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "recognition_noise"], terms=["компактная стойка", "место у клиента", "шкаф"]),
    claim(85, 23, (512, 515), "SPEAKER_01", "Для свинцово-кислотных аккумуляторов был разработан собственный балансир/контроллер, который ставился в свинцовых системах с 2021 года.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "business_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "recognition_noise"], terms=["балансир", "свинцово-кислотные аккумуляторы", "контроллер", "2021"]),
    claim(86, 23, (516, 521), "SPEAKER_01", "Для литиевых аккумуляторов собственные доработки не делались, потому что они воспринимаются как закрытый готовый блок.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "business_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "recognition_noise"], terms=["литиевые аккумуляторы", "разработки", "готовый блок"]),
    claim(87, 23, (522, 526), "SPEAKER_01", "Текущий секретный соус компании описан скорее как подбор людей, знание правильного монтажа и технический контроль, чем как уникальное железо.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging", "presentation"], "context_only", "speaker_opinion", confidence="medium", flags=["recognition_noise", "marketing_claim_review", "public_use_review", "technical_confirmation_required"], terms=["секретный соус", "кадры", "монтаж", "технический контроль"]),
    claim(88, 24, (527, 532), "SPEAKER_02", "Перед разговорами с другими сотрудниками нужно сначала понять, что компания продает и как продает, используя картину генерального директора как исходную гипотезу.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["что продаем", "как продаем", "исходная гипотеза"]),
    claim(89, 24, (533, 534), "SPEAKER_01", "Ключевое позиционирование сформулировано как продажа спокойствия для среднеобеспеченного класса людей.", "positioning_claim", "positioning", ["business_kb", "sales_training", "website", "brochure", "presentation", "commercial_messaging", "content_bank"], "context_only", "speaker_opinion", flags=["marketing_claim_review", "public_use_review"], terms=["спокойствие", "среднеобеспеченный класс", "позиционирование"]),
    claim(90, 24, (535, 539), "SPEAKER_01", "В клиентском кейсе первоначальная идея меньшей системы была расширена до 18 кВт и 24 аккумуляторов после требования, чтобы работало все.", "sales_case", "sales_process", ["business_kb", "sales_training", "manager_training", "presentation"], "needs_confirmation", "example_case", confidence="medium", flags=["technical_confirmation_required", "price_or_guarantee_review", "marketing_claim_review"], sales_case={"customer_type": "состоятельный владелец дома", "problem_situation": "Семья хотела, чтобы при отключении работало не минимальное оборудование, а весь нужный контур.", "diagnosis_path": "В разговоре выяснилось, что малая мощность не соответствует реальному ожиданию.", "proposed_action": "Подобрать систему большей мощности; в кейсе упомянуты 18 кВт и 24 аккумулятора.", "risk_or_caveat": "Цифры и конфигурация требуют технической проверки."}, terms=["Апрелевка", "18 кВт", "24 аккумулятора", "клиентский кейс"]),
    claim(91, 24, (540, 547), "SPEAKER_01", "Для следующих интервью как источники картины предложены коммерческий директор и технический специалист, умеющий объяснять работу компании.", "operational_claim", "operations", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["коммерческий директор", "технический специалист", "следующие интервью"]),
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
        "interview_001_chunk_0008": [
            {
                "source_quote": chunk_by_id["interview_001_chunk_0008"]["text"],
                "reason": "not_business_relevant",
                "notes": "Off-topic food/coffee break; excluded from claim extraction.",
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
                    "open_questions_found": sum(1 for claim_item in claims if claim_item["claim_type"] == "open_question"),
                    "noise_or_transition_items": len(skipped_items) if chunk["chunk_status"] == "excluded" else 0,
                    "coverage_notes": (
                        "Excluded off-topic transition."
                        if chunk["chunk_status"] == "excluded"
                        else "Full interview_001 control extraction; meaningful business items extracted as source-backed claims."
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
