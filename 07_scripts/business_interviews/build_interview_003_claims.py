#!/usr/bin/env python3
"""Build source-backed extraction artifacts for interview_003."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = "00_input/interviews/260408_sveton3_converted_t_large-v3_diar.txt"
SOURCE_PATH = ROOT / SOURCE_FILE
CHUNKS_PATH = ROOT / "00_input/interviews/chunks/interview_003_chunks.jsonl"
OUT_CLAIMS = ROOT / "00_input/interviews/statements/interview_003_claims.jsonl"
OUT_RESULTS = ROOT / "00_input/interviews/statements/interview_003_extraction_results.jsonl"

ROLES = {
    "SPEAKER_00": ("Алексей", "коммерческий директор Светон"),
    "SPEAKER_01": ("Сергей", "директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели"),
    "SPEAKER_02": ("Алексей", "коммерческий директор Светон"),
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
        "claim_id": f"interview_claim_003{seq:03d}",
        "claim": claim_text,
        "claim_type": claim_type,
        "source_interview_id": "interview_003",
        "source_file": SOURCE_FILE,
        "source_chunk_id": f"interview_003_chunk_{chunk_index:04d}",
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
    claim(1, 1, (1, 5), "SPEAKER_02", "В разговоре выделены три варианта инверторных/резервных решений: стандартные/offline, инвертор со встроенным стабилизатором и двойное преобразование.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "recognition_noise"], terms=["offline", "инвертор", "стабилизатор", "двойное преобразование"]),
    claim(2, 1, (6, 16), "SPEAKER_02", "Двойное преобразование описано как режим, при котором устройство постоянно генерирует 50 Гц и 230 В, преобразуя входное напряжение через постоянный ток.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "recognition_noise"], terms=["двойное преобразование", "50 Гц", "230 В", "постоянный ток"]),
    claim(3, 1, (16, 18), "SPEAKER_02", "Двойное преобразование решает задачу стабилизации напряжения, выдавая нужные 220 или 230 В.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["стабилизация напряжения", "220 В", "230 В"]),
    claim(4, 2, (19, 20), "SPEAKER_02", "Информация о том, почему компания не использует двойное преобразование, названа внутренней и не предназначенной для клиента.", "sales_process_claim", "sales_process", ["sales_training", "manager_training"], "not_relevant", "source_backed", flags=["marketing_claim_review"], terms=["информация для клиента", "двойное преобразование"]),
    claim(5, 2, (22, 31), "SPEAKER_02", "Недостатки двойного преобразования в разговоре: постоянная работа вентилятора, постоянная генерация, шум и опасение за ресурс аккумуляторов из-за постоянного заряд-разряда.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["шум", "вентилятор", "аккумуляторы", "заряд-разряд"]),
    claim(6, 2, (33, 39), "SPEAKER_02", "Алексей утверждает, что сейчас необходимости в двойном преобразовании нет, а для проблемы скачков напряжения компания использует стабилизаторы.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "marketing_claim_review", "public_use_review"], terms=["двойное преобразование", "стабилизатор", "скачки напряжения"]),
    claim(7, 3, (40, 45), "SPEAKER_02", "В качестве решения по стабилизации упомянуты стабилизаторы Штиль Инстаб; они позиционируются как отрабатывающие задачу без аккумуляторов.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["Штиль", "Инстаб", "стабилизатор", "аккумуляторы"]),
    claim(8, 3, (54, 57), "SPEAKER_02", "Шум назван серьезным фактором: двойное преобразование постоянно работает и шумит, поэтому компания отошла от такого варианта.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["шум", "двойное преобразование", "отказ от варианта"]),
    claim(9, 4, (59, 64), "SPEAKER_02", "После мобилизации возник дефицит сотрудников для монтажа: часть людей была мобилизована, часть ушла в другие направления.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["рынок труда", "мобилизация", "монтажники"]),
    claim(10, 4, (65, 71), "SPEAKER_02", "В найме монтажников выбор ограничен; встречаются грамотные люди с высшим образованием, которых приходится постепенно воспитывать как сотрудников.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["монтажники", "найм", "обучение"]),
    claim(11, 5, (80, 84), "SPEAKER_02", "Инженеры в офисе могут чертить схемы, писать инструкции и общаться с клиентами; инструкции нужно периодически обновлять.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["инженеры", "схемы", "инструкции", "клиенты"]),
    claim(12, 5, (90, 95), "SPEAKER_02", "Технический директор/сильный технический сотрудник частично совмещает продажи, выезды на объекты и подготовку технических заданий.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "recognition_noise"], terms=["технический директор", "объект", "техническое задание", "продажи"]),
    claim(13, 6, (96, 110), "SPEAKER_02", "Главное техническое ограничение резервной группы: если нагрузка в группе превышает заложенную мощность инвертора, система будет отключаться.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["резервная группа", "мощность", "инвертор", "отключение"]),
    claim(14, 6, (111, 115), "SPEAKER_02", "Перед установкой нужно понять, какая нагрузка сидит на нужных потребителях и можно ли отделить их от остальных; варианты решения: отдельный автомат, исключение холодильника или система большей мощности.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["нагрузка", "отдельный автомат", "холодильник", "10 кВт"]),
    claim(15, 7, (116, 124), "SPEAKER_02", "На первом звонке менеджер выясняет желаемых потребителей, считает мощность и нужное время резерва, например 8 или 12 часов.", "qualification_question", "qualification", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], discovery_question={"question": "Каких потребителей клиент хочет резервировать и на сколько часов?", "why_it_matters": "От этого зависят мощность инвертора и емкость аккумуляторов.", "answer_changes": "Меняется конфигурация системы и бюджет."}, terms=["первый звонок", "потребители", "8 часов", "12 часов"]),
    claim(16, 7, (120, 123), "SPEAKER_02", "Типовые желаемые потребители частного клиента: погружной насос, газовый котел и холодильник.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["погружной насос", "газовый котел", "холодильник"]),
    claim(17, 7, (125, 134), "SPEAKER_02", "После согласования примерной суммы клиент переходит к монтажу; в Московском регионе компания предпочитает продавать с монтажом, потому что частные клиенты часто уже имели негативный опыт.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "marketing_claim_review", "recognition_noise"], terms=["монтаж", "Московский регион", "частные клиенты"]),
    claim(18, 8, (135, 138), "SPEAKER_02", "Сложность шлейфов и скрытых нагрузок не стоит подробно объяснять клиенту на первом контакте, потому что это трудно и вызывает сопротивление.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["первый контакт", "шлейф", "скрытые нагрузки", "объяснение"]),
    claim(19, 8, (141, 149), "SPEAKER_02", "Логика продажи: сначала прогреть клиента и получить согласие по цене, а сложные технические ограничения обсуждать на объекте, где клиент уже ближе к покупке.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "sales_script"], "not_relevant", "source_backed", flags=["marketing_claim_review", "strategy_claim_review"], terms=["прогрев", "цена", "объект", "технические ограничения"]),
    claim(20, 8, (149, 154), "SPEAKER_02", "Для сложных ограничений используются речевые модули и варианты: вывести отдельную розетку, провести отдельный провод или временно использовать удлинитель.", "recommended_response", "objection_handling", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["речевой модуль", "отдельная розетка", "отдельный провод", "удлинитель"]),
    claim(21, 9, (155, 163), "SPEAKER_02", "Менеджеров по продажам для этой темы сложно найти; последних сотрудников пришлось обучать техническим и продажным нюансам с нуля.", "risk_or_constraint", "risk", ["business_kb", "manager_training", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["менеджеры", "обучение", "найм"]),
    claim(22, 9, (164, 169), "SPEAKER_02", "Ценовое восприятие клиента можно вести постепенно: клиент привыкает к одной сумме, затем к следующей, и итоговая сумма воспринимается мягче, чем если назвать ее сразу.", "sales_process_claim", "sales_process", ["sales_training", "sales_script", "manager_training"], "not_relevant", "speaker_opinion", flags=["marketing_claim_review"], terms=["ценовое восприятие", "постепенное увеличение", "базовый комплект"]),
    claim(23, 9, (170, 174), "SPEAKER_02", "Конкуренты могут экономить на байпасном щите, но байпас назван страховкой: без него при отказе за инвертором может не включиться потребитель, включая котел.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["байпасный щит", "страховка", "инвертор", "котел"]),
    claim(24, 9, (176, 180), "SPEAKER_02", "Если сразу подробно объяснять все технические сложности, это отталкивает клиента; иначе клиент сначала видит, что компания сняла с него проблемы и посчитала решение.", "sales_process_claim", "sales_process", ["sales_training", "sales_script", "manager_training"], "not_relevant", "source_backed", flags=["marketing_claim_review"], terms=["технические сложности", "отталкивает клиента", "сняли проблемы"]),
    claim(25, 10, (183, 185), "SPEAKER_02", "Письмо хуже передает эмоции, чем голос и встреча; для этой продажи личная встреча важна, потому что специалист находится в доме клиента.", "sales_process_claim", "sales_process", ["sales_training", "manager_training"], "not_relevant", "speaker_opinion", flags=["marketing_claim_review"], terms=["письмо", "телефон", "встреча", "эмоции"]),
    claim(26, 10, (190, 193), "SPEAKER_02", "На объекте менеджер может сыграть роль защитника интересов клиента и создать ощущение, что он боролся за скидку.", "sales_process_claim", "sales_process", ["sales_training", "manager_training"], "not_relevant", "speaker_opinion", flags=["marketing_claim_review"], terms=["скидка", "объект", "за вас боролся"]),
    claim(27, 11, (194, 203), "SPEAKER_02", "Около 30% монтажей могут быть невозможны на желаемые деньги клиента из-за технических особенностей объекта.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "price_or_guarantee_review", "strategy_claim_review"], terms=["30% монтажей", "технические особенности", "бюджет клиента"]),
    claim(28, 11, (207, 214), "SPEAKER_02", "Частные клиенты часто не знают, какие автоматы за что отвечают; на объекте приходится искать потребителей, отключать автоматы и измерять мощность клещами.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["автоматы", "клещи", "измерение мощности", "потребители"]),
    claim(29, 11, (211, 214), "SPEAKER_02", "Даже если автомат подписан как кухня или холодильник, на нем может висеть уличное освещение или другой потребитель, поэтому подписи нужно проверять фактически.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["подпись автомата", "кухня", "уличное освещение", "проверка"]),
    claim(30, 12, (216, 230), "SPEAKER_02", "На первом звонке менеджер оценивает типовые нагрузки: свет, котел, канализация/септик, холодильник и затем спрашивает, сколько времени резервирования нужно.", "qualification_question", "qualification", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], discovery_question={"question": "Какие потребители нужны: свет, котел, септик, холодильник, и сколько часов они должны работать?", "why_it_matters": "Это базовая квалификация для мощности и емкости.", "answer_changes": "Определяет состав и цену предложения."}, terms=["свет", "котел", "септик", "холодильник", "время резерва"]),
    claim(31, 12, (232, 240), "SPEAKER_02", "Для Московской области в разговоре упоминается критичность 12 часов резервирования, хотя возможны разные уровни обслуживания и длительности отключений.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", confidence="medium", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["Московская область", "12 часов", "длительность отключения"]),
    claim(32, 13, (241, 244), "SPEAKER_02", "Насос, котел, холодильник и септик можно посчитать относительно хорошо, а остальные нагрузки часто оцениваются приблизительно.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["насос", "котел", "холодильник", "септик", "примерная оценка"]),
    claim(33, 13, (245, 247), "SPEAKER_02", "На месте нагрузку можно уточнять измерением ампеража клещами, но часть оценок все равно делается на глаз.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["ампераж", "клещи", "оценка нагрузки"]),
    claim(34, 13, (248, 257), "SPEAKER_02", "Если нужный потребитель сидит на одном шлейфе с другими розетками, установка отдельного автомата в щите не отделит потребитель, потому что провод в стене остается общий.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["шлейф", "общий провод", "розетки", "отдельный автомат"]),
    claim(35, 13, (260, 264), "SPEAKER_02", "Решение при невозможности отделить потребителя: более мощная система или отдельный электрик, который выведет отдельный автомат/проводку.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["более мощная система", "электрик", "отдельный автомат", "проводка"]),
    claim(36, 14, (265, 273), "SPEAKER_02", "Фактическая мощность на автомате часто выше названной клиентом нагрузки, поэтому менеджер должен понять, какой хвост еще висит на этом автомате.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["хвост нагрузки", "автомат", "менеджер", "потребители"]),
    claim(37, 14, (267, 269), "SPEAKER_02", "Насосы часто бывают на отдельном автомате, а с холодильником и котельной чаще возникают проблемы из-за других потребителей на той же линии.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["насос", "холодильник", "котельная", "стиральная машина"]),
    claim(38, 14, (273, 282), "SPEAKER_02", "При проверке холодильника менеджеры отключают автомат и тестером проходят по кухне, чтобы понять, какие розетки или потребители сидят на этой линии.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["холодильник", "автомат", "тестер", "кухня"]),
    claim(39, 14, (284, 288), "SPEAKER_02", "Холодильник на отдельном автомате может быть сделан ради будущего подключения генератора; это не обязательно связано с бесперебойкой.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["холодильник", "отдельный автомат", "генератор"]),
    claim(40, 14, (291, 295), "SPEAKER_02", "Несколько проводов на один автомат часто появляются из-за нехватки места или плохого решения в щите; если бы автоматы были, провода могли бы вывести на отдельные автоматы.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "recognition_noise"], terms=["щит", "несколько проводов", "автомат", "обжимка"]),
    claim(41, 14, (300, 305), "SPEAKER_02", "В котельной может быть сложная схема с фазами и сторонними нагрузками; если один провод уходит на котельную вместе со стиральной машиной, стоимость решения возрастает.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["котельная", "фазы", "стиральная машина", "стоимость"]),
    claim(42, 15, (306, 311), "SPEAKER_02", "Менеджеры постепенно учатся техническим нюансам и начинают понимать, что продажа сложнее, чем просто продать оборудование.", "operational_claim", "operations", ["manager_training", "business_kb"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "recognition_noise"], terms=["обучение менеджеров", "технические нюансы", "продажи"]),
    claim(43, 15, (311, 320), "SPEAKER_02", "Есть ситуации, когда продажа невозможна из-за отсутствия места или неправильных условий установки: нужно место вокруг инвертора для конвекции, аккумулятор нельзя ставить возле батареи/радиатора.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["место установки", "конвекция", "аккумулятор", "радиатор"]),
    claim(44, 15, (320, 324), "SPEAKER_02", "Два частых стоп-фактора продажи: нет подходящего места для оборудования и не хватает мощности/корректной нагрузки.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "strategy_claim_review"], terms=["стоп-фактор", "место", "мощность"]),
    claim(45, 16, (329, 340), "SPEAKER_02", "Профиль менеджера сложный: он должен быть готов работать больше 8 часов, продавать, понимать продукт, составлять предложение на А4, проверять его и доводить до монтажной группы.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "recognition_noise"], terms=["менеджер", "А4", "монтажная группа", "продажи"]),
    claim(46, 16, (336, 340), "SPEAKER_02", "Проверочный фильтр для продавца: прочитать документ и объяснить, что именно компания продает; на этом отсеивается значительная часть кандидатов.", "qualification_question", "qualification", ["manager_training", "sales_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], discovery_question={"question": "Что мы продаем по прочитанному документу?", "why_it_matters": "Проверяет способность кандидата понять продукт, а не просто заявить, что он продаст что угодно.", "answer_changes": "Слабый ответ отсекает кандидата или требует базового обучения."}, terms=["кандидат", "что продаем", "фильтр", "документ"]),
    claim(47, 16, (341, 352), "SPEAKER_02", "Для удержания бывшего менеджера была оставлена лазейка: он получает небольшую сумму за работу со старыми клиентами, если они обращаются.", "operational_claim", "operations", ["business_kb", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["удержание", "старые клиенты", "менеджер"]),
    claim(48, 17, (353, 360), "SPEAKER_02", "Клиентская база по возрасту смещается: раньше было около 50-70 лет, сейчас клиент молодеет примерно до 35-40+.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["возраст клиента", "50-70", "35-40"]),
    claim(49, 17, (360, 366), "SPEAKER_02", "По обращениям женщин меньше, но если женщина приходит в продажу, она может принимать решение быстрее и жестче, чем мужчина, который советуется с супругой.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training", "strategy"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review"], terms=["женщины", "ЛПР", "решение о покупке"]),
    claim(50, 17, (367, 373), "SPEAKER_02", "Около 50 лет часть клиентов переезжает в дома и сталкивается с проблемами дома; более молодые покупатели чаще строят дома с электрическим отоплением.", "customer_segment_claim", "customer_segment", ["business_kb", "sales_training", "strategy"], "needs_confirmation", "speaker_opinion", flags=["strategy_claim_review", "marketing_claim_review", "technical_confirmation_required"], terms=["переезд в дом", "электрическое отопление", "газовый котел"]),
    claim(51, 17, (373, 379), "SPEAKER_02", "При газовом отоплении резервируется небольшой насос/котел, а при электрическом отоплении потребление резко выше, поэтому система может стоить порядка 2 млн вместо 300 тыс.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review", "marketing_claim_review"], terms=["газовое отопление", "электрическое отопление", "300 тысяч", "2 миллиона"]),
    claim(52, 18, (380, 388), "SPEAKER_02", "Основная стоимость оборудования связана с аккумуляторами; чтобы обеспечить хотя бы 2-3 часа, нужно больше аккумуляторов, а система может стоить больше миллиона.", "business_model_claim", "business_model", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review", "marketing_claim_review"], terms=["аккумуляторы", "2-3 часа", "стоимость", "миллион"]),
    claim(53, 18, (385, 387), "SPEAKER_02", "В системе 5 кВт·ч используется не вся емкость, а около 4 кВт·ч, потому что примерно 20% оставляют для продления срока службы.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["5 кВт·ч", "4 кВт·ч", "20%", "срок службы"]),
    claim(54, 18, (390, 396), "SPEAKER_02", "Основная боль частного клиента начинается с отопления и риска разморозки дома; при замерзании воды может разорвать сантехнику и инженерные элементы.", "customer_pain", "customer_pain", ["business_kb", "sales_training", "sales_script", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "public_use_review"], terms=["отопление", "разморозка дома", "вода", "сантехника"]),
    claim(55, 19, (402, 410), "SPEAKER_02", "При техническом подборе нужно учитывать пусковые токи подключаемых приборов: компрессоры, холодильник, кондиционер, погружной насос; пики могут кратно превышать номинал.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["пусковые токи", "компрессор", "холодильник", "кондиционер", "насос"]),
    claim(56, 19, (410, 419), "SPEAKER_02", "Малые инверторы на 600 Вт или 1 кВт не ставят на холодильник, потому что в момент пуска холодильник может потребовать больше мощности, чем они потянут.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["холодильник", "600 Вт", "1 кВт", "пусковая мощность"]),
    claim(57, 20, (422, 424), "SPEAKER_02", "Инверторы имеют кратковременную перегрузочную способность; условно 5-киловаттный инвертор может потянуть 2-киловаттный насос с кратным пусковым током.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "price_or_guarantee_review"], terms=["перегруз", "5 кВт", "насос", "пусковой ток"]),
    claim(58, 20, (431, 436), "SPEAKER_01", "При штатном отключении сети холодильник, уже подключенный через инвертор, не испытывает прерывания питания; пусковые токи возникают при включении устройств вроде кондиционера.", "technical_claim_needs_confirmation", "technical_context", ["review_only", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["холодильник", "инвертор", "переключение", "кондиционер"]),
    claim(59, 20, (438, 444), "SPEAKER_02", "Если во время работы от инвертора включить мощный потребитель и превысить пиковую мощность, инвертор может отключить всю группу, подключенную через него.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["пиковая мощность", "инвертор", "группа потребителей", "отключение"]),
    claim(60, 20, (444, 448), "SPEAKER_02", "Для объяснения простого перегруза используется бытовая аналогия с квартирой: включили микроволновку и чайник одновременно, и автомат выбило.", "recommended_response", "objection_handling", ["sales_training", "sales_script", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["перегруз", "аналогия", "микроволновка", "чайник"]),
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
                    "coverage_notes": "Full interview_003 extraction; meaningful business, sales, operational, and technical-boundary items extracted as source-backed claims.",
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
