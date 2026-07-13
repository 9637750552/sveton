#!/usr/bin/env python3
"""Build source-backed extraction artifacts for interview_006."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = "00_input/interviews/260609_sveton_2_converted_t_large-v3_diar.txt"
SOURCE_PATH = ROOT / SOURCE_FILE
CHUNKS_PATH = ROOT / "00_input/interviews/chunks/interview_006_chunks.jsonl"
OUT_CLAIMS = ROOT / "00_input/interviews/statements/interview_006_claims.jsonl"
OUT_RESULTS = ROOT / "00_input/interviews/statements/interview_006_extraction_results.jsonl"

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
        "claim_id": f"interview_claim_006{seq:03d}",
        "claim": claim_text,
        "claim_type": claim_type,
        "source_interview_id": "interview_006",
        "source_file": SOURCE_FILE,
        "source_chunk_id": f"interview_006_chunk_{chunk_index:04d}",
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
    claim(1, 1, (1, 5), "SPEAKER_01", "В коммерческом разговоре компания может переводить клиента с системы 3-4 на 5-4, объясняя, что более мощный инвертор работает с меньшей нагрузкой и стоит ненамного дороже.", "marketing_message", "positioning", ["sales_training", "commercial_messaging", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "price_or_guarantee_review"], terms=["3-4", "5-4", "инвертор", "апсейл"]),
    claim(2, 2, (6, 14), "SPEAKER_01", "Для разных холодильников пиковая мощность при старте может сильно отличаться: в разговоре названы примеры от 1:2 для инверторного холодильника до 1:15 для простого холодильника.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["холодильник", "пиковая мощность", "компрессор", "инверторный холодильник"]),
    claim(3, 2, (19, 21), "SPEAKER_01", "Дмитрий формулирует рабочее правило: не рассчитывать постоянную нагрузку больше чем на 70% от номинала инвертора.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["70%", "номинал инвертора", "постоянная нагрузка"]),
    claim(4, 2, (22, 24), "SPEAKER_02", "Сергей фиксирует ключевой вопрос расчета: нужно ли закладываться на одновременный пуск котла, насоса и холодильника, потому что иначе подбор инвертора может резко подорожать.", "qualification_question", "qualification", ["sales_training", "manager_training", "sales_script"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "price_or_guarantee_review"], discovery_question={"question": "Какие резервируемые приборы могут стартовать одновременно?", "why_it_matters": "Одновременный пуск влияет на требуемую пиковую мощность инвертора.", "answer_changes": "Может измениться модель системы и стоимость предложения."}, terms=["одновременный пуск", "котел", "насос", "холодильник"]),
    claim(5, 3, (31, 34), "SPEAKER_01", "В обсуждаемой системе используется оффлайновый ИБП с реле и временем переключения около 10 миллисекунд; по словам Дмитрия, компьютеры при этом не сбрасываются.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["оффлайновый ИБП", "реле", "10 миллисекунд", "переключение"]),
    claim(6, 4, (36, 42), "SPEAKER_01", "Дмитрий считает онлайн-ИБП менее подходящим для типового сценария резервирования из-за меньшего КПД, большего собственного потребления, шума и возможного влияния на ресурс старых аккумуляторов.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "commercial_messaging", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review", "price_or_guarantee_review"], terms=["онлайн-ИБП", "КПД", "собственное потребление", "шум"]),
    claim(7, 4, (42, 43), "SPEAKER_01", "Онлайн-ИБП, по объяснению Дмитрия, нужен там, где требуется точное напряжение 220-230 В на выходе.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["онлайн-ИБП", "220-230 В", "качество напряжения"]),
    claim(8, 5, (48, 55), "SPEAKER_01", "Дмитрий утверждает, что одновременный старт нагрузок является стандартной расчетной ситуацией, например после выключения и включения автомата, и ее нельзя игнорировать.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["одновременный старт", "автомат", "пиковая нагрузка"]),
    claim(9, 5, (57, 59), "SPEAKER_01", "Если инвертор не выдерживает пиковый запуск, возможен цикл старт-перегрузка-выключение, который снижает ресурс ИБП.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["перегрузка", "холодный старт", "ресурс ИБП"]),
    claim(10, 5, (61, 66), "SPEAKER_01", "Постоянная мощность подключенных нагрузок не должна превышать номинал инвертора и желательно должна оставаться в пределах 70%; пиковая мощность берется из характеристик инвертора.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["постоянная мощность", "номинал", "пиковая мощность", "характеристики инвертора"]),
    claim(11, 5, (72, 81), "SPEAKER_01", "Дмитрий приводит пример расчета пика: холодильник 150 Вт с десятикратным пуском дает 1,5 кВт, насос 800 Вт с пятикратным пуском дает 4 кВт, вместе около 5,5 кВт.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["пример расчета", "холодильник", "насос", "пиковая мощность"]),
    claim(12, 6, (82, 84), "SPEAKER_01", "В анкете 1С есть вкладка нагрузок, куда менеджер вносит потребители; система автоматически считает номинальную мощность, емкость аккумулятора, пиковую мощность и подходящую систему.", "operational_claim", "operations", ["business_kb", "manager_training", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["1С", "анкета", "нагрузки", "автоматический расчет"]),
    claim(13, 6, (85, 99), "SPEAKER_02", "Сергей предлагает использовать исторические анкеты 1С как источник для справочной базы типовых приборов, их названий и мощностей.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "context_only", "hypothesis", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["1С", "справочная база", "типовые приборы", "мощность"]),
    claim(14, 6, (100, 105), "SPEAKER_01", "Дмитрий допускает техническую возможность выгрузить или просмотреть данные 1С, но предупреждает, что результат может быть нерепрезентативным без проверки фактического качества анкет.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["1С", "качество данных", "анкеты", "репрезентативность"]),
    claim(15, 7, (135, 142), "SPEAKER_01", "Вкладка нагрузок в анкете содержит мощность и среднее время работы в сутки; по кнопке печати нагрузки может формироваться Word-файл с таблицей.", "operational_claim", "operations", ["manager_training", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["вкладка нагрузки", "СВР", "печать нагрузки", "Word"]),
    claim(16, 7, (157, 160), "SPEAKER_01", "Дмитрий предупреждает, что многие анкеты в 1С часто не заполнены, поэтому для демонстрации нужно брать конкретную заполненную анкету.", "risk_or_constraint", "risk", ["business_kb", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["1С", "анкеты", "качество заполнения"]),
    claim(17, 8, (161, 199), "SPEAKER_01", "Для поиска старой анкеты Дмитрий ведет Сергея через фильтры 1С, включая снятие отбора по дате и ответственному, что показывает сложность интерфейса для нового пользователя.", "operational_claim", "operations", ["manager_training", "review_only"], "not_relevant", "source_backed", confidence="medium", flags=["recognition_noise"], terms=["1С", "фильтры", "анкеты клиентов", "интерфейс"]),
    claim(18, 9, (200, 215), "SPEAKER_01", "На примере анкеты видно, что менеджеры могут заносить нагрузки неполно или неясно: отдельная нагрузка на 1300 Вт не названа, а поля включают время работы, количество, коэффициент пика и коэффициент коррекции.", "operational_claim", "operations", ["business_kb", "manager_training", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["нагрузки", "коэффициент пика", "коэффициент коррекции", "качество заполнения"]),
    claim(19, 9, (216, 228), "SPEAKER_01", "1С автоматически рассчитывает параметры системы из вручную заполненных нагрузок, но если менеджер ввел неверные данные, расчет тоже будет ошибочным.", "risk_or_constraint", "risk", ["business_kb", "manager_training", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["1С", "автоматический расчет", "ошибка ввода", "качество данных"]),
    claim(20, 9, (220, 222), "SPEAKER_02", "Сергей формулирует риск процесса: если менеджер заполнит нагрузки неправильно, рассчитанные параметры системы будут недостоверными.", "risk_or_constraint", "risk", ["manager_training", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["менеджер", "расчет", "ошибка", "нагрузки"]),
    claim(21, 9, (223, 229), "SPEAKER_01", "В рассчитанных параметрах анкеты отображаются время работы на максимальной и средней нагрузке, минимальная емкость аккумулятора и другие технические показатели.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["время работы", "емкость аккумулятора", "расчетные параметры"]),
    claim(22, 10, (239, 241), "SPEAKER_01", "В анкете обычно указываются generic-названия потребителей вроде освещения, холодильников и телевизоров, а не точные модели приборов; сложные приборы выносятся на консультацию с техническим отделом.", "operational_claim", "operations", ["business_kb", "manager_training", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["потребители", "модели приборов", "технический отдел"]),
    claim(23, 10, (250, 255), "SPEAKER_01", "Менеджер предварительно заполняет таблицу нагрузок со слов клиента, а затем данные должны проверяться и корректироваться при выезде, включая фактическую мощность приборов.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["предварительное заполнение", "выезд", "аудит", "мощность приборов"]),
    claim(24, 10, (257, 261), "SPEAKER_01", "В 1С нет отдельной версии нагрузок со слов клиента и отдельной версии после аудита; данные по ходу корректируются в той же анкете.", "operational_claim", "operations", ["business_kb", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["1С", "версии данных", "аудит", "корректировка"]),
    claim(25, 11, (270, 279), "SPEAKER_01", "В коммерческом предложении может быть несколько вариантов, один из которых выделяется как утвержденный; варианты могут отличаться суммами и скидками.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "context_only", "source_backed", flags=["price_or_guarantee_review"], terms=["коммерческое предложение", "варианты", "скидка", "утвержденный вариант"]),
    claim(26, 11, (281, 296), "SPEAKER_01", "Название варианта коммерческого предложения можно использовать для понятного описания конфигурации, например '5 киловатт 1600' или 'вариант с гелевыми аккумуляторами', но менеджеры часто это не делают.", "marketing_message", "marketing", ["sales_training", "manager_training", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["название варианта", "КП", "конфигурация", "гелевые аккумуляторы"]),
    claim(27, 11, (305, 320), "SPEAKER_01", "После заполнения нагрузок менеджер создает коммерческое предложение из анкеты через кнопку 'Создать КП' или связанную команду в 1С.", "operational_claim", "operations", ["manager_training", "sales_training"], "context_only", "source_backed", flags=[], terms=["1С", "Создать КП", "анкета", "коммерческое предложение"]),
    claim(28, 12, (323, 343), "SPEAKER_01", "Коммерческое предложение формируется в Word и требует ручного редактирования под конкретного клиента, чтобы текст выглядел аккуратно и релевантно.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review"], terms=["Word", "КП", "редактирование", "клиент"]),
    claim(29, 12, (343, 347), "SPEAKER_01", "Клиенту следует отправлять коммерческое предложение в PDF, а не в Word.", "operational_claim", "operations", ["sales_training", "manager_training"], "not_relevant", "source_backed", flags=["marketing_claim_review"], terms=["PDF", "Word", "отправка клиенту"]),
    claim(30, 12, (348, 358), "SPEAKER_01", "До выезда на аудит клиенту можно дать предварительное коммерческое предложение или озвучить порядок цен, чтобы он был подготовлен и понимал примерный бюджет.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training", "sales_script"], "context_only", "source_backed", flags=["price_or_guarantee_review", "marketing_claim_review"], terms=["предварительное КП", "аудит", "порядок цен", "подготовка клиента"]),
    claim(31, 12, (359, 359), "SPEAKER_02", "Сергей делает вывод, что обычных электриков невозможно быстро обучить работе с 1С и подбору системы, потому что для этого нужен менеджер-специалист.", "risk_or_constraint", "risk", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["электрик", "1С", "подбор системы", "менеджер"]),
    claim(32, 13, (364, 367), "SPEAKER_01", "После выезда электрик должен подтвердить возможность решения: например, можно ли выделить линию, перебрать щиток или зарезервировать одну фазу.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["выезд", "щиток", "фаза", "резервирование"]),
    claim(33, 13, (364, 386), "SPEAKER_01", "На осмотре электрик должен фотографировать место установки, а также проверить габариты рулеткой, чтобы понять, влезет ли система.", "operational_claim", "operations", ["manager_training", "electricians_kb", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["осмотр", "фото", "место установки", "рулетка"]),
    claim(34, 13, (376, 386), "SPEAKER_01", "Хороший осмотр обычно включает много фотографий, а слабый исполнитель фотографирует только минимально нужное и может пропустить важные детали.", "risk_or_constraint", "risk", ["manager_training", "electricians_kb", "business_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["фотофиксация", "осмотр", "качество исполнителя"]),
    claim(35, 13, (392, 395), "SPEAKER_01", "Сложные монтажи в региональной модели предполагается делать иначе, а не передавать на стандартный сценарий местного монтажника.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["сложный монтаж", "региональная модель", "местный монтажник"]),
    claim(36, 14, (398, 405), "SPEAKER_01", "После осмотра и проверки реальных данных формируется окончательное коммерческое предложение, затем заказ покупателя, договор и документы на монтаж.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training"], "context_only", "source_backed", flags=["price_or_guarantee_review"], terms=["осмотр", "окончательное КП", "заказ покупателя", "договор"]),
    claim(37, 14, (405, 411), "SPEAKER_01", "Монтажники выезжают на монтаж с карточкой клиента и заданием, которое менеджер собирает по шаблону вручную; планируется автоматизировать этот процесс кнопками.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["карточка клиента", "задание монтажнику", "шаблон", "автоматизация"]),
    claim(38, 14, (406, 409), "SPEAKER_01", "Задание для монтажников готовит менеджер, а при технических вопросах его корректируют технические специалисты.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "context_only", "source_backed", flags=["technical_confirmation_required"], terms=["менеджер", "технический специалист", "задание монтажнику"]),
    claim(39, 14, (418, 424), "SPEAKER_01", "Детализированное задание для монтажников необходимо и включает описание работ, комплектацию и особенности монтажа.", "operational_claim", "operations", ["manager_training", "electricians_kb", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["задание", "комплектация", "особенности монтажа"]),
    claim(40, 15, (443, 448), "SPEAKER_01", "Из 1С можно сформировать карточку, которую распечатывают для выезда; в ней есть адрес, описание и список работ, написанный менеджером.", "operational_claim", "operations", ["manager_training", "electricians_kb"], "context_only", "source_backed", flags=["technical_confirmation_required"], terms=["карточка", "1С", "список работ", "выезд"]),
    claim(41, 15, (449, 453), "SPEAKER_01", "Обычный электрик без подготовки не сможет сформировать список работ, но предварительно обученный постоянный электрик может выполнять монтаж по готовому списку.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "electricians_kb", "manager_training"], "needs_confirmation", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["электрик", "обучение", "список работ", "постоянный партнер"]),
    claim(42, 15, (455, 459), "SPEAKER_01", "Опытный специалист может составить список работ по фотографиям и описанию, которые электрик соберет на аудите.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["фотографии", "описание", "список работ", "удаленный специалист"]),
    claim(43, 15, (460, 467), "SPEAKER_01", "Нового монтажника желательно сопровождать: сначала тренировка в офисе, затем несколько монтажей вторым номером и контроль опытным специалистом.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "electricians_kb", "manager_training"], "needs_confirmation", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["обучение монтажника", "стажер", "второй номер", "контроль"]),
    claim(44, 15, (471, 475), "SPEAKER_01", "Монтажники обычно не должны определять, что надо делать на объекте; предполагаемые и фактически выполненные работы нужно записывать в систему.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["монтажник", "система", "работы", "фиксация"]),
    claim(45, 15, (475, 482), "SPEAKER_01", "Перед началом монтажа монтажник фотографирует фактическое состояние объекта, сверяется с заданием и при проблемах звонит менеджеру или техническому специалисту.", "operational_claim", "operations", ["manager_training", "electricians_kb", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required"], terms=["монтаж", "фотографии до", "сверка задания", "эскалация"]),
    claim(46, 15, (483, 486), "SPEAKER_01", "Монтажнику запрещено содержательно разговаривать с клиентом: он может отвечать коротко, но не должен рассуждать, потому что не умеет правильно говорить с клиентом.", "operational_claim", "operations", ["business_kb", "manager_training", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["монтажник", "клиент", "коммуникация", "правило"]),
    claim(47, 16, (492, 504), "SPEAKER_01", "При работе в живой базе 1С Дмитрий рекомендует не записывать изменения: закрывать документы через 'Закрыть', а не через 'ОК', потому что 'ОК' записывает изменения без вопроса.", "operational_claim", "operations", ["manager_training", "review_only"], "not_relevant", "source_backed", flags=[], terms=["1С", "живая база", "ОК", "Закрыть"]),
    claim(48, 16, (506, 506), "SPEAKER_02", "Сергей фиксирует, что перед звонками электрикам нужно описать алгоритм взаимодействия: что им говорить, что просить и какие действия они должны делать.", "strategy_claim", "strategy", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["алгоритм взаимодействия", "электрики", "холодные звонки", "MVP"]),
    claim(49, 17, (510, 516), "SPEAKER_01", "Дмитрий предлагает Сергею или Вадику выехать хотя бы на первый час реального монтажа с действующей бригадой, чтобы увидеть процесс на практике.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["выезд на монтаж", "Вадик", "обучение", "практика"]),
    claim(50, 17, (516, 518), "SPEAKER_02", "Сергей рассматривает вариант, при котором Вадик станет региональным специалистом и сможет удаленно готовить карточку клиента и список работ по фотографиям монтажника.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "context_only", "hypothesis", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["Вадик", "региональный специалист", "удаленная работа", "фотографии"]),
    claim(51, 17, (518, 524), "SPEAKER_01", "Дмитрий формулирует принцип кадровой модели: компания старается выращивать не суперлюдей, а заменяемых менеджеров и монтажников, которых можно обучить за недели или месяцы.", "business_model_claim", "business_model", ["business_kb", "strategy", "manager_training"], "context_only", "speaker_opinion", flags=["strategy_claim_review"], terms=["кадровая модель", "заменяемость", "обучение", "менеджеры"]),
    claim(52, 17, (523, 524), "SPEAKER_01", "Подбор менеджеров и монтажников стал сложнее: менеджера в прошлом году искали 9 месяцев, а монтажника отбирают примерно одного из 5-6 кандидатов.", "risk_or_constraint", "risk", ["business_kb", "strategy", "review_only"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["подбор персонала", "менеджер", "монтажник", "отбор"]),
    claim(53, 17, (525, 530), "SPEAKER_02", "Для Горячего Ключа Сергей предлагает региональную цепочку: электрики из объявлений делают выезд и аудит, бэк-офис по фотографиям заполняет карточку клиента и список работ, а главным узким местом остается обучение электрика монтажу.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "context_only", "hypothesis", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["Горячий Ключ", "электрики", "бэк-офис", "узкое место"]),
    claim(54, 17, (531, 535), "SPEAKER_01", "Дмитрий считает, что без практики в 1С, общения с клиентами и электромонтажниками трудно понять правильный путь региональной модели; после поездки в Китай у него появились мысли о другом подходе.", "open_question", "open_question", ["business_kb", "strategy", "review_only"], "context_only", "open_question", flags=["strategy_claim_review", "open_question"], open_question={"question": "Какой альтернативный путь региональной модели Дмитрий имеет в виду после поездки в Китай?", "why_it_matters": "Это может изменить схему запуска южного филиала и работу с местными электриками.", "needed_validation": "Нужно отдельное интервью или уточнение после практического просмотра 1С, клиентов и монтажников.", "possible_owner": "Дмитрий"}, terms=["региональная модель", "Китай", "альтернативный подход"]),
    claim(55, 17, (536, 538), "SPEAKER_02", "Следующий практический шаг, предложенный Сергеем: описать крупными мазками порядок взаимодействия с электромонтажниками для первых холодных звонков.", "strategy_claim", "strategy", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review"], terms=["следующий шаг", "электромонтажники", "холодные звонки", "крупные мазки"]),
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
        skipped = []
        if not claims:
            skipped.append(
                {
                    "source_reference": f"{chunk['source_file']}:{chunk['start_line']}-{chunk['end_line']}",
                    "reason": "navigation_or_low_information",
                    "notes": "Mostly 1C navigation, repeated confirmations, or diarization noise without durable business claim.",
                }
            )
        results.append(
            {
                "source_chunk_id": chunk_id,
                "coverage_summary": {
                    "meaningful_items_seen": len(claims),
                    "claims_extracted": len(claims),
                    "open_questions_found": sum(1 for item in claims if item["claim_type"] == "open_question"),
                    "noise_or_transition_items": len(skipped),
                    "coverage_notes": "Full interview_006 extraction; sales-process, 1C workflow, load-calculation, inspection, installer-training, and regional-model claims extracted.",
                },
                "skipped_source_items": skipped,
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
