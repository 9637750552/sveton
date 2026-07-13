#!/usr/bin/env python3
"""Build source-backed extraction artifacts for interview_007."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = "00_input/interviews/260610_sveton_converted_t_large-v3_diar.txt"
SOURCE_PATH = ROOT / SOURCE_FILE
CHUNKS_PATH = ROOT / "00_input/interviews/chunks/interview_007_chunks.jsonl"
OUT_CLAIMS = ROOT / "00_input/interviews/statements/interview_007_claims.jsonl"
OUT_RESULTS = ROOT / "00_input/interviews/statements/interview_007_extraction_results.jsonl"

ROLES = {
    "SPEAKER_00": ("Дмитрий", "генеральный директор Светон"),
    "SPEAKER_01": ("Сергей", "директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели"),
    "SPEAKER_02": ("Дмитрий", "генеральный директор Светон"),
    "SPEAKER_03": ("Вадик", "участник обсуждения региональной модели; потенциальный специалист/партнер южного направления"),
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
        "claim_id": f"interview_claim_007{seq:03d}",
        "claim": claim_text,
        "claim_type": claim_type,
        "source_interview_id": "interview_007",
        "source_file": SOURCE_FILE,
        "source_chunk_id": f"interview_007_chunk_{chunk_index:04d}",
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
    claim(1, 1, (4, 13), "SPEAKER_02", "При превышении нагрузки по выходу инвертор уходит в защиту по перегрузке; это аварийная, а не штатная ситуация.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["инвертор", "перегрузка", "защита"]),
    claim(2, 1, (13, 15), "SPEAKER_02", "Повторяющиеся аварийные перегрузки могут сокращать ресурс силовых ключей инвертора.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["силовые ключи", "ресурс", "аварийная ситуация"]),
    claim(3, 1, (28, 30), "SPEAKER_02", "Задача системы формулируется как бесшовное аварийное электроснабжение; если при пропадании электричества инвертор выключился, он не выполнил свою роль.", "product_claim", "product", ["business_kb", "sales_training", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["бесшовное электроснабжение", "инвертор", "роль системы"]),
    claim(4, 2, (37, 44), "SPEAKER_02", "Байпас вручную исключает инвертор из цепи, но Дмитрий считает такие схемы нежелательными и говорит, что лучше ставить более мощный инвертор, чем городить обходные сценарии.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["байпас", "инвертор", "мощность"]),
    claim(5, 2, (40, 40), "SPEAKER_02", "Если система смонтирована с превышением нагрузки, клиент может быть уведомлен в акте приемки, что поломка инвертора в таком режиме не является гарантийным случаем.", "risk_or_constraint", "risk", ["business_kb", "manager_training", "review_only"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["акт приемки", "гарантия", "превышение нагрузки"]),
    claim(6, 2, (45, 52), "SPEAKER_02", "За мощность системы отвечает инвертор, но батареи должны быть согласованы с инвертором по допустимому току разряда и BMS.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["инвертор", "батарея", "BMS", "ток разряда"]),
    claim(7, 2, (56, 57), "SPEAKER_02", "Аккумуляторы подбираются прежде всего по требуемому времени резерва: при 8 часах нужно примерно вдвое больше аккумуляторов, чем при 4 часах.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["аккумуляторы", "время резерва", "емкость"]),
    claim(8, 2, (63, 64), "SPEAKER_02", "Дмитрий утверждает, что высоковольтные системы нельзя ставить в жилых домах без специализированных помещений и обслуживания; выше примерно 60 В уже опасно.", "technical_claim_needs_confirmation", "technical_context", ["review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["высоковольтные системы", "жилой дом", "48 В", "безопасность"]),
    claim(9, 3, (72, 80), "SPEAKER_02", "Для больших мощностей компания масштабирует систему количеством инверторов и шин, а не мыслит ее как одну общую шину.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["мощность", "инверторы", "шины", "масштабирование"]),
    claim(10, 3, (85, 86), "SPEAKER_02", "Дмитрий повторяет правило: у 5-киловаттной системы желательно держать нагрузку не выше 70% номинала, чтобы компоненты работали в долговременном режиме.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["70%", "номинал", "долговременный режим"]),
    claim(11, 4, (88, 95), "SPEAKER_03", "Вадик выдвигает гипотезу, что клиентам не стоит подробно объяснять мощность инвертора, а лучше фокусироваться на времени работы системы.", "marketing_message", "marketing", ["business_kb", "sales_training", "commercial_messaging"], "context_only", "hypothesis", flags=["marketing_claim_review", "strategy_claim_review"], terms=["клиентский язык", "мощность", "время работы"]),
    claim(12, 4, (96, 96), "SPEAKER_02", "Дмитрий формулирует позиционирование: Светон продает не инверторы и аккумуляторы, а систему бесперебойного электроснабжения с гарантийным обслуживанием.", "positioning_claim", "positioning", ["business_kb", "website", "brochure", "presentation", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["позиционирование", "система", "услуга", "гарантийное обслуживание"]),
    claim(13, 4, (99, 104), "SPEAKER_01", "Сергей считает допустимым объяснять клиенту запас по мощности через пиковые токи при запуске, потому что часть клиентов это понимает, а остальные принимают утверждение специалиста.", "marketing_message", "positioning", ["sales_training", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["пиковые токи", "объяснение клиенту", "запас мощности"]),
    claim(14, 4, (109, 113), "SPEAKER_02", "Для обычного клиента компания упрощает объяснение до подбора системы под запрос; если клиент не знает мощность, специалист выясняет параметры по косвенным признакам.", "sales_process_claim", "qualification", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], discovery_question={"question": "Какая котельная, насосы и площадь дома у клиента, если он не знает мощность оборудования?", "why_it_matters": "Косвенные признаки позволяют сделать предварительную оценку без точных шильдиков.", "answer_changes": "Меняется предварительный подбор системы и необходимость выезда."}, terms=["косвенные признаки", "котельная", "мощность", "квалификация"]),
    claim(15, 5, (118, 121), "SPEAKER_02", "Клиенты обычно не могут назвать мощность насоса или оборудования; для скважины они чаще знают глубину, а не электрические характеристики.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["клиент не знает мощность", "насос", "скважина", "глубина"]),
    claim(16, 5, (121, 126), "SPEAKER_02", "Перед выездом нужно дать клиенту ценовые ориентиры, потому что выезд к клиенту, который рассчитывал на 100 тысяч, а получил расчет на 300 тысяч, будет пустым.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "context_only", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["ценовой ориентир", "выезд", "предварительная оценка"]),
    claim(17, 5, (123, 127), "SPEAKER_01", "Сергей формулирует процесс: специалист должен удаленно оценить стоимость по разговору и косвенным признакам, а выезд должен подтверждать оценку, а не полностью переделывать ее.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["удаленная оценка", "выезд", "косвенные признаки"]),
    claim(18, 5, (127, 127), "SPEAKER_01", "Сергей считает, что электрик не способен оценивать стоимость системы; эту роль должен выполнять специалист, которым должен стать Вадик.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["электрик", "оценка стоимости", "Вадик", "специалист"]),
    claim(19, 5, (145, 145), "SPEAKER_02", "Детальная первичная квалификация нужна, чтобы понять реальные нагрузки, режимы работы и бюджет клиента до выезда.", "qualification_question", "qualification", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review"], discovery_question={"question": "Какие приборы, мощности, режимы работы и ограничения по бюджету есть у клиента?", "why_it_matters": "Без этого можно предложить слишком дорогую или технически неподходящую систему.", "answer_changes": "Определяет конфигурацию, необходимость исключить нагрузки и решение о выезде."}, terms=["квалификация", "нагрузки", "бюджет", "выезд"]),
    claim(20, 6, (146, 152), "SPEAKER_01", "Сергей утверждает, что типовой электрик не умеет вести сложный разговор с клиентом, задавать вопросы и вежливо выслушивать для экспертной оценки.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["электрик", "разговор с клиентом", "экспертная оценка"]),
    claim(21, 6, (153, 162), "SPEAKER_03", "Вадик возражает, что электрики бывают разными: некоторые способны вести объект полностью и имеют заказы на годы вперед.", "partner_model_claim", "partner_model", ["business_kb", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["электрики", "звезды", "объект под ключ"]),
    claim(22, 6, (163, 163), "SPEAKER_02", "Дмитрий формулирует принцип: бизнес не может держаться на звездах, он должен держаться на конвейере и взаимозаменяемых людях.", "business_model_claim", "business_model", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["конвейер", "звезды", "взаимозаменяемость"]),
    claim(23, 6, (165, 168), "SPEAKER_02", "Дмитрий считает невозможным просто скопировать московскую модель в Краснодар без клонирования ключевых людей компании.", "strategy_claim", "strategy", ["business_kb", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["Краснодар", "московская модель", "ключевые люди"]),
    claim(24, 6, (177, 188), "SPEAKER_01", "Сергей настаивает, что в сервисной модели отношения с клиентом должны принадлежать Светону: клиент должен звонить компании, а история коммуникаций должна храниться в CRM.", "business_model_claim", "business_model", ["business_kb", "strategy", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["сервисная модель", "отношения с клиентом", "CRM", "клиентская база"]),
    claim(25, 6, (187, 188), "SPEAKER_01", "Сергей считает клиентскую базу стратегическим активом, через который в будущем можно продавать новые сервисы вроде мобильного приложения или видеонаблюдения.", "strategy_claim", "strategy", ["business_kb", "strategy", "commercial_messaging"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["клиентская база", "допродажи", "мобильное приложение", "видеонаблюдение"]),
    claim(26, 7, (192, 198), "SPEAKER_01", "Сергей предлагает, чтобы разговор с клиентом вел человек Светона, а электрик мог участвовать, но сбор информации, документирование и учет деталей оставались у компании.", "sales_process_claim", "sales_process", ["business_kb", "strategy", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["разговор с клиентом", "электрик", "документирование", "CRM"]),
    claim(27, 7, (198, 204), "SPEAKER_01", "Если информацию передавать через электрика без CRM и записи разговоров, возникает риск испорченного телефона, спорных обещаний и гарантийных конфликтов.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["CRM", "запись разговоров", "испорченный телефон", "гарантийный случай"]),
    claim(28, 7, (204, 206), "SPEAKER_01", "При объеме 10-20 монтажей в месяц работать без CRM, по мнению Сергея, невозможно из-за претензий и несоответствия ожиданий клиента.", "operational_claim", "operations", ["business_kb", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["10-20 монтажей", "CRM", "претензии", "масштаб"]),
    claim(29, 7, (207, 207), "SPEAKER_02", "Дмитрий формулирует бизнес как стандартизацию информации и решение клиентских вопросов; без стандарта жить нельзя.", "business_model_claim", "business_model", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["стандартизация", "клиентские вопросы", "бизнес"]),
    claim(30, 7, (208, 216), "SPEAKER_01", "Если электрик обещает клиенту неподходящую систему, а клиент потом сталкивается с аварийным отключением, ответственность и негативные отзывы ударят по Светону.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required", "marketing_claim_review"], terms=["электрик", "обещания", "негативный отзыв", "ответственность"]),
    claim(31, 7, (217, 219), "SPEAKER_02", "Дмитрий приводит пример бывших менеджеров, которые ушли в собственную компанию и получили плохие отзывы, как аргумент в пользу жесткого контроля качества и продажи услуги, а не оборудования.", "sales_case", "service_model", ["business_kb", "sales_training", "manager_training"], "context_only", "example_case", flags=["strategy_claim_review", "marketing_claim_review"], sales_case={"customer_type": "внутренний пример конкурентного сервиса", "problem_situation": "бывшие менеджеры начали самостоятельно продавать и монтировать оборудование", "diagnosis_path": "без жесткого контроля качества сервис деградировал и появились плохие отзывы", "proposed_action": "продавать контролируемую услугу, а не просто оборудование", "risk_or_caveat": "пример требует проверки деталей перед публичным использованием"}, terms=["контроль качества", "услуга", "оборудование", "отзывы"]),
    claim(32, 7, (220, 229), "SPEAKER_02", "Прорабская схема может работать, но, по словам Дмитрия, дает слишком мало продаж: 10-15 активных прорабов приносят нерегулярные заказы, а две продажи в месяц не решают задачу масштаба.", "partner_model_claim", "partner_model", ["business_kb", "strategy"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["прорабы", "масштаб", "две продажи", "партнерский канал"]),
    claim(33, 8, (231, 242), "SPEAKER_02", "Дмитрий считает, что строительные компании обычно не заинтересованы продавать резервное электроснабжение: им важнее продажа и стройка дома, а потребность у клиента часто возникает через полгода-год жизни в доме.", "customer_segment_claim", "customer_segment", ["business_kb", "strategy", "sales_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["строительные компании", "новый дом", "потребность", "полгода-год"]),
    claim(34, 8, (250, 256), "SPEAKER_02", "Дмитрий считает, что системы часто ставятся в уже обжитые дома, где электрика может быть нестандартной и непредсказуемой.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["обжитые дома", "электрика", "нестандартность"]),
    claim(35, 8, (258, 263), "SPEAKER_01", "Сергей формулирует стратегию: прорабы и строительные компании могут быть дополнительным каналом, но core-модель должна масштабироваться через аутсорсинговых электриков для аудита, монтажа и сервиса.", "strategy_claim", "strategy", ["business_kb", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["аутсорсинговые электрики", "аудит", "монтаж", "сервис", "core model"]),
    claim(36, 9, (265, 267), "SPEAKER_02", "Дмитрий описывает идеальную модель как аналог уберизации: пул заказов, пул свободных электриков и менеджер, который передает заказы конкретным исполнителям.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "context_only", "hypothesis", flags=["strategy_claim_review"], terms=["уберизация", "пул электриков", "пул заказов", "менеджер"]),
    claim(37, 9, (270, 271), "SPEAKER_01", "Сергей говорит, что отказался от собственных монтажников и машин, потому что держать их на зарплате круглый год невозможно; базовая ставка делается на аутсорс.", "business_model_claim", "business_model", ["business_kb", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["аутсорс", "свои монтажники", "машины", "зарплата"]),
    claim(38, 9, (273, 273), "SPEAKER_02", "Московская модель Светона рассматривается как полигон: нужно понять, что из нее можно перенести в Краснодар и на юг.", "strategy_claim", "strategy", ["business_kb", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["Москва", "Краснодар", "юг", "перенос модели"]),
    claim(39, 10, (276, 284), "SPEAKER_02", "Дмитрий утверждает, что задержка переключения 5-10 мс обычно не влияет на работу котла, потому что электроника имеет сглаживающие элементы.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["5-10 мс", "котел", "переключение", "электроника"]),
    claim(40, 10, (289, 294), "SPEAKER_02", "Некоторые котлы могут быть чувствительны к форме сигнала, генератору, нулю, заземлению и занулению, поэтому такие случаи требуют технической проверки на объекте.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["котел", "форма сигнала", "ноль", "заземление"]),
    claim(41, 10, (297, 302), "SPEAKER_02", "Проблемы заземления и зануления при монтаже должен понимать монтажник; в каждом конкретном случае возможны разные схемы решения.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["заземление", "зануление", "монтажник", "схемы"]),
    claim(42, 11, (303, 313), "SPEAKER_02", "Дмитрий уточняет ценность продукта: сейчас клиенты чаще покупают не только защиту от разморозки, а комфорт жизни при отключении электричества.", "value_proposition_claim", "value_proposition", ["business_kb", "website", "brochure", "presentation", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["комфорт", "отключение электричества", "ценность продукта"]),
    claim(43, 11, (323, 327), "SPEAKER_02", "Резервное электроснабжение сравнивается с КАСКО: клиент покупает уверенность, что система продержит дом какое-то время и даст сигнал о проблеме.", "marketing_message", "marketing", ["sales_training", "commercial_messaging", "content_bank"], "context_only", "source_backed", flags=["marketing_claim_review", "public_use_review"], terms=["КАСКО", "уверенность", "SMS", "безопасность"]),
    claim(44, 11, (331, 337), "SPEAKER_03", "Вадик подтверждает личную релевантность продукта: у него часто отключают электричество, поэтому он точно будет ставить такую систему.", "sales_case", "customer_pain", ["business_kb", "sales_training", "content_bank"], "context_only", "example_case", flags=["marketing_claim_review"], sales_case={"customer_type": "частный дом", "problem_situation": "частые отключения электричества", "diagnosis_path": "владелец хочет видеть состояние дома и снизить риск дискомфорта", "proposed_action": "рассмотреть установку системы резервного электроснабжения", "risk_or_caveat": "личный пример, не использовать публично без согласования"}, terms=["частые отключения", "личный пример", "Вадик"]),
    claim(45, 12, (343, 344), "SPEAKER_02", "Дмитрий готов прислать Вадику инструкции и технические материалы по инвертору.", "operational_claim", "operations", ["business_kb", "manager_training"], "context_only", "source_backed", flags=["technical_confirmation_required"], terms=["инструкции", "инвертор", "материалы"]),
    claim(46, 12, (351, 361), "SPEAKER_02", "Светон не собирает инверторы локально; технические специалисты нужны для сложных нестандартных ситуаций, а не для массовой сборки оборудования.", "operational_claim", "operations", ["business_kb", "manager_training"], "context_only", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["инверторы", "технический директор", "инженеры", "нестандартные случаи"]),
    claim(47, 13, (367, 373), "SPEAKER_02", "По словам Дмитрия, к прошлому году было около 1300 монтажей, а до 2020 года компания делала примерно 400-500 монтажей в год после первых малых лет.", "business_model_claim", "business_model", ["business_kb", "presentation", "review_only"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "public_use_review"], terms=["1300 монтажей", "400-500 в год", "история компании"]),
    claim(48, 13, (376, 389), "SPEAKER_02", "Компания отказалась от старых презентаций и финмоделей для клиентов; менеджеры используют простой аргумент про стоимость генератора, который реально проработает 5 лет.", "marketing_message", "marketing", ["sales_training", "commercial_messaging", "content_bank"], "context_only", "source_backed", flags=["marketing_claim_review", "price_or_guarantee_review"], terms=["генератор", "финмодель", "презентация", "аргумент продаж"]),
    claim(49, 14, (390, 396), "SPEAKER_02", "Для работы со строительными компаниями материалы придется делать заново, потому что старые экономические модели и слайды не используются и, по словам Дмитрия, ничего не дали.", "strategy_claim", "strategy", ["business_kb", "strategy", "presentation"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["строительные компании", "слайды", "финмодель", "B2B"]),
    claim(50, 14, (396, 412), "SPEAKER_02", "Компания сместила усилия с презентаций на продуктовую документацию: с системой выдается пакет из 5-6 листов, включая схемы, листы настройки, рекомендации по работе и аварийным ситуациям.", "product_claim", "product", ["business_kb", "manager_training", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["документация", "схемы", "листы настройки", "авария"]),
    claim(51, 15, (423, 426), "SPEAKER_01", "Сергей просит складывать материалы и вопросы в Telegram-группу, чтобы не дублировать коммуникации, и просит выложить доступные калькуляторы или финмодели.", "operational_claim", "operations", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["Telegram", "материалы", "калькуляторы", "финмодель"]),
    claim(52, 15, (429, 432), "SPEAKER_01", "Сергей сообщает о первом потенциальном региональном клиенте: модератор выставочной сессии, связанная со строительными компаниями, заканчивает дом и может получить подарок от Светона.", "sales_case", "sales_process", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review", "price_or_guarantee_review"], sales_case={"customer_type": "региональный контакт со строительными связями", "problem_situation": "заканчивает дом и может быть первым демонстрационным клиентом", "diagnosis_path": "контакт может открыть доступ к строительным компаниям и ассоциациям", "proposed_action": "подумать о формате подарка или пилотного предложения", "risk_or_caveat": "нужна отдельная коммерческая проработка"}, terms=["первый клиент", "регион", "строительные компании", "подарок"]),
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
                    "coverage_notes": "Full interview_007 extraction; three-person strategy, CRM, service-model, partner-channel, technical-boundary, and marketing claims extracted.",
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
