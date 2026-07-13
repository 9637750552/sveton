#!/usr/bin/env python3
"""Build source-backed extraction artifacts for interview_004."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = "00_input/interviews/260408_sveton4_converted_t_large-v3_diar.txt"
SOURCE_PATH = ROOT / SOURCE_FILE
CHUNKS_PATH = ROOT / "00_input/interviews/chunks/interview_004_chunks.jsonl"
OUT_CLAIMS = ROOT / "00_input/interviews/statements/interview_004_claims.jsonl"
OUT_RESULTS = ROOT / "00_input/interviews/statements/interview_004_extraction_results.jsonl"

ROLES = {
    "SPEAKER_00": ("Алексей", "коммерческий директор Светон"),
    "SPEAKER_01": ("Алексей", "коммерческий директор Светон"),
    "SPEAKER_02": ("Сергей", "директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели"),
    "SPEAKER_03": ("Алексей", "коммерческий директор Светон"),
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
        "claim_id": f"interview_claim_004{seq:03d}",
        "claim": claim_text,
        "claim_type": claim_type,
        "source_interview_id": "interview_004",
        "source_file": SOURCE_FILE,
        "source_chunk_id": f"interview_004_chunk_{chunk_index:04d}",
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
    claim(1, 2, (11, 14), "SPEAKER_02", "Для южного региона сначала нужно подтвердить гипотезу о емкости рынка; Сергей готов временно работать как региональный менеджер и ездить на объекты, если это поможет проверить рынок.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["южный регион", "емкость рынка", "региональный менеджер", "выезд"]),
    claim(2, 2, (15, 24), "SPEAKER_01", "На первом этапе региональной работы задача не в сложном расчете системы, а в том, чтобы объяснить существование решения, собрать потребителей и понять, есть ли у человека боль.", "sales_process_claim", "sales_process", ["business_kb", "sales_training", "manager_training", "sales_script"], "context_only", "source_backed", flags=["marketing_claim_review", "technical_confirmation_required"], terms=["регион", "первый контакт", "боль клиента", "потребители"]),
    claim(3, 2, (16, 21), "SPEAKER_01", "Для первых региональных сделок расчет можно делать совместно с Сергеем Донасовым или Алексеем, а не требовать от нового регионального человека самостоятельного расчета с первого дня.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["регион", "расчет", "Сергей Донасов", "обучение"]),
    claim(4, 2, (22, 24), "SPEAKER_01", "Возможные SMB-направления для проверки включают магазины, склады, курятники, IT-специалистов и другие небольшие бизнесы с потребностью в резервном питании.", "customer_segment_claim", "customer_segment", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["SMB", "магазины", "склады", "курятники", "IT"]),
    claim(5, 2, (24, 30), "SPEAKER_01", "На начальном этапе региональная задача может быть простой: объяснить продукт, выявить потребность, передать данные на расчет, а позже перейти к самостоятельному расчету.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "sales_script"], "context_only", "source_backed", flags=["marketing_claim_review", "strategy_claim_review"], terms=["объяснить продукт", "выявить потребность", "передать на расчет"]),
    claim(6, 3, (31, 36), "SPEAKER_01", "Компании нужно диверсифицировать получение лидов и заявок из разных источников; один из фокусов - посредники.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["диверсификация лидов", "источники заявок", "посредники"]),
    claim(7, 3, (40, 49), "SPEAKER_01", "Для региональной модели самая большая проблема - локальный штат установщиков; частные клиенты для первого захода являются точечной историей и не основным фокусом.", "risk_or_constraint", "risk", ["business_kb", "strategy"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["регион", "установщики", "частные клиенты", "штат"]),
    claim(8, 4, (50, 53), "SPEAKER_02", "Даже если масштаб SMB больше, на частных клиентах можно потренироваться как на малых кейсах до выхода на промышленные или более сложные объекты.", "strategy_claim", "strategy", ["business_kb", "strategy", "manager_training"], "not_relevant", "speaker_opinion", flags=["strategy_claim_review"], terms=["SMB", "частные клиенты", "тестирование"]),
    claim(9, 4, (53, 59), "SPEAKER_01", "SMB разбивается на подсегменты: магазины, стоматологии, франшизные стоматологии, медицинские сценарии и системные администраторы с небольшими системами.", "customer_segment_claim", "customer_segment", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["SMB", "магазин", "стоматология", "франшиза", "сисадмин"]),
    claim(10, 4, (60, 64), "SPEAKER_02", "Кейс упаковки чая показывает SMB-боль: при отключении линия встает, большой заказ может сорваться, и бизнес теряет заказы.", "sales_case", "sales_process", ["business_kb", "sales_training", "content_bank"], "context_only", "example_case", flags=["marketing_claim_review", "public_use_review"], sales_case={"customer_type": "небольшое производство / упаковка чая", "problem_situation": "Отключение электричества останавливает линию и ставит под риск большой заказ.", "diagnosis_path": "Проверить мощность линии, длительность критичного простоя и экономику потерь.", "proposed_action": "Использовать как SMB-кейс для проверки спроса на резервное питание.", "risk_or_caveat": "Кейс требует фактического технического расчета."}, terms=["упаковка чая", "линия", "потеря заказов", "SMB"]),
    claim(11, 4, (71, 80), "SPEAKER_01", "На примере пеллетного котла показано, что внешне похожие системы могут иметь сильно разную мощность из-за шнеков, горелки и масштаба подачи топлива.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["пеллетный котел", "шнек", "мощность", "горелка"]),
    claim(12, 5, (81, 85), "SPEAKER_01", "Для пеллетных и дровяных котлов критична работа насоса при отключении электричества; малые котельные решения для компании являются побочной и неинтересной рыбой.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "sales_training", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "marketing_claim_review"], terms=["пеллетный котел", "дровяной котел", "насос", "малые системы"]),
    claim(13, 5, (87, 96), "SPEAKER_01", "Компания постепенно уходит от киловаттных решений к 3-5 кВт, потому что в малых системах возникают ограничения по пусковым токам, стандартной мощности и BMS аккумуляторов.", "product_claim", "product", ["business_kb", "strategy", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review", "marketing_claim_review"], terms=["1 кВт", "3 кВт", "5 кВт", "BMS", "пусковые токи"]),
    claim(14, 5, (101, 107), "SPEAKER_01", "Для больших систем сложные технические нюансы можно использовать как плюс: показать клиенту, что компания учитывает вентиляцию, аккумуляторы и надежность, в отличие от конкурентов.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "marketing_claim_review", "public_use_review"], terms=["большая система", "вентиляция", "репутация", "конкуренты"]),
    claim(15, 5, (103, 105), "SPEAKER_01", "Алексей утверждает, что компания первой системно вышла на рынок частных бесперебойников и развила рынок, после чего начали присоединяться конкуренты.", "positioning_claim", "positioning", ["business_kb", "commercial_messaging", "presentation"], "not_relevant", "speaker_opinion", flags=["marketing_claim_review", "public_use_review", "strategy_claim_review"], terms=["рынок частников", "бесперебойники", "конкуренты"]),
    claim(16, 5, (110, 112), "SPEAKER_01", "Отсутствие вентиляции грозит выходом электроники из строя, а размещение аккумуляторов возле нагревателя - быстрым выходом аккумуляторов из строя.", "technical_claim_needs_confirmation", "technical_context", ["sales_training", "manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["вентиляция", "электроника", "аккумулятор", "нагреватель"]),
    claim(17, 6, (113, 118), "SPEAKER_01", "Приоритеты региональной работы: частники внизу, SMB на втором месте как экспериментальное развитие, основной приоритет - посредники.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["частники", "SMB", "посредники", "приоритет"]),
    claim(18, 6, (118, 127), "SPEAKER_01", "Идеальный посредник в региональной модели сам рекламирует, сам устанавливает и связан со строительством или электрикой.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["посредник", "строительство", "электрика", "установка"]),
    claim(19, 6, (128, 132), "SPEAKER_01", "По бизнес-клиентам пока много неизвестных; частники и посредники более отработаны, а бизнес идет вторым приоритетом.", "open_question", "open_question", ["business_kb", "strategy", "review_only"], "not_relevant", "open_question", flags=["open_question", "strategy_claim_review"], open_question={"question": "Какая модель продаж и монтажа лучше работает для бизнес-клиентов в регионе?", "why_open": "Алексей прямо говорит, что по бизнесу много неизвестных.", "needed_evidence": "Нужны пилотные региональные SMB-кейсы и обратная связь от менеджеров."}, terms=["бизнес-клиенты", "частники", "посредники"]),
    claim(20, 8, (140, 151), "SPEAKER_01", "Компания не продает решения для критически важного медицинского оборудования и жизнедеятельности, включая кислородные концентраторы и ветеринарные/медицинские сценарии, где отказ может повлиять на жизнь.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "manager_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["критическая инфраструктура", "медицина", "кислородный концентратор", "жизнедеятельность"]),
    claim(21, 8, (148, 154), "SPEAKER_01", "Для критически важного оборудования требуется другая архитектура с двойной защитой; промышленные мощности вроде 60 кВт компания пока не пробовала и не конкурирует с промышленными игроками.", "technical_claim_needs_confirmation", "technical_context", ["business_kb", "strategy", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["двойная защита", "60 кВт", "промышленные решения"]),
    claim(22, 9, (156, 162), "SPEAKER_01", "Серверы названы перспективной темой, но клиенты серверных систем исторически привыкли к двойному преобразованию; проблему стабилизации можно решать стабилизатором.", "strategy_claim", "strategy", ["business_kb", "strategy", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review", "marketing_claim_review"], terms=["серверы", "двойное преобразование", "стабилизатор"]),
    claim(23, 9, (164, 178), "SPEAKER_01", "Стандартные серверные ИБП двойного преобразования часто рассчитаны на 10-15 минут, а Sveton может предлагать альтернативу с более длительной работой, например 8 часов, но без двойного преобразования и при необходимости со стабилизатором.", "value_proposition_claim", "value_proposition", ["business_kb", "sales_training", "commercial_messaging"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "price_or_guarantee_review", "public_use_review"], terms=["сервер", "10-15 минут", "8 часов", "стабилизатор"]),
    claim(24, 9, (180, 193), "SPEAKER_01", "Ограничение серверного сегмента: у типовых серверных ИБП есть протокол корректного отключения сервера при пропадании питания, а у текущего решения Sveton такого протокола нет.", "risk_or_constraint", "risk", ["business_kb", "sales_training", "strategy"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["сервер", "протокол отключения", "ИБП", "ограничение"]),
    claim(25, 9, (190, 199), "SPEAKER_01", "Если протокол отключения серверу не важен, часть клиентов может согласиться на более длительное резервирование; тема становится актуальнее, потому что компании переносят серверы из облака обратно в офис.", "strategy_claim", "strategy", ["business_kb", "strategy", "sales_training"], "needs_confirmation", "speaker_opinion", flags=["technical_confirmation_required", "strategy_claim_review", "marketing_claim_review"], terms=["серверы", "облако", "офис", "резервирование"]),
    claim(26, 10, (203, 210), "SPEAKER_02", "Для Сергея на этапе тестирования важнее понять потенциал рынка и направление поиска, чем сразу определить точные коммерческие отношения.", "strategy_claim", "strategy", ["business_kb", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review"], terms=["тестирование рынка", "потенциал", "коммерческие отношения"]),
    claim(27, 11, (211, 215), "SPEAKER_01", "В Краснодарском крае основной региональный запрос связан с тем, чтобы кто-то смонтировал; прорабы и посредники имеют гораздо большую силу воздействия на заказчика, чем удаленная компания из интернета.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "sales_training"], "context_only", "source_backed", flags=["strategy_claim_review", "marketing_claim_review"], terms=["Краснодарский край", "прораб", "посредник", "монтаж"]),
    claim(28, 11, (218, 224), "SPEAKER_01", "Компания может официально работать с посредником через агентский договор и платить за проведенную работу; у Сергея есть ИП для расчетов.", "business_model_claim", "business_model", ["business_kb", "strategy", "manager_training"], "not_relevant", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["агентский договор", "ИП", "посредник"]),
    claim(29, 12, (225, 235), "SPEAKER_01", "В агентской и региональной модели важно понимать скидки и маржу: у менеджеров есть скидки, действует специальная скидка на литий, а цена компании выше рынка.", "business_model_claim", "business_model", ["business_kb", "strategy", "review_only"], "not_relevant", "source_backed", flags=["price_or_guarantee_review", "strategy_claim_review"], terms=["скидка", "маржа", "литий", "цена выше рынка"]),
    claim(30, 13, (237, 243), "SPEAKER_01", "Региональных электриков не нужно заново учить переменному току и переборке щитов; задача компании - снять страх перед бесперебойкой за счет документации и инструкции.", "partner_model_claim", "partner_model", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["региональный электрик", "переменный ток", "переборка щита", "инструкция"]),
    claim(31, 13, (243, 249), "SPEAKER_01", "Лист настройки снижает риск ошибки при настройке инвертора и тока зарядки; вместо 30-страничной книги нужен короткий документ настройки.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["лист настройки", "инвертор", "ток зарядки", "AGM"]),
    claim(32, 13, (250, 253), "SPEAKER_01", "Для монтажа систем нужна визуализированная инструкция по переменному току, перемычкам, сборке и переборке щита.", "technical_claim_needs_confirmation", "technical_context", ["manager_training", "electricians_kb", "review_only"], "needs_confirmation", "needs_external_confirmation", flags=["technical_confirmation_required"], terms=["визуальная инструкция", "переменный ток", "перемычки", "переборка щита"]),
    claim(33, 13, (254, 258), "SPEAKER_01", "Для регионального монтажа достаточно связки монтажник плюс монтажник; оборудование можно отправлять транспортной компанией со склада без локального склада.", "operational_claim", "operations", ["business_kb", "strategy", "manager_training"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["монтажники", "регион", "транспортная компания", "склад"]),
    claim(34, 13, (258, 260), "SPEAKER_01", "Если заявка получена до трех часов, оборудование можно отгрузить транспортной компанией на следующий день; если позже - через рабочий день.", "operational_claim", "operations", ["business_kb", "manager_training", "strategy"], "not_relevant", "source_backed", flags=["strategy_claim_review", "price_or_guarantee_review"], terms=["отгрузка", "транспортная компания", "следующий день"]),
    claim(35, 13, (262, 268), "SPEAKER_01", "Монтажников сейчас готовят через приезд в компанию, объяснение руководителем монтажной группы, обучающий стенд и работу с первым номером.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "context_only", "source_backed", flags=["strategy_claim_review", "technical_confirmation_required"], terms=["обучение монтажников", "обучающий стенд", "руководитель монтажной группы"]),
    claim(36, 14, (271, 275), "SPEAKER_01", "В региональной модели можно искать электриков, которые уже разбираются в электрике, снять у них страх перед бесперебойкой документами, а затем использовать лучших как подрядчиков или кандидатов в штат.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["региональный электрик", "подрядчик", "штат", "документы"]),
    claim(37, 14, (277, 286), "SPEAKER_01", "Собственный штат монтажников является важным критерием доверия для частных клиентов, потому что они опасаются субподрядчиков и хотят, чтобы компания отвечала за монтаж.", "positioning_claim", "positioning", ["business_kb", "sales_training", "commercial_messaging"], "context_only", "source_backed", flags=["marketing_claim_review", "strategy_claim_review"], terms=["штат монтажников", "доверие", "субподрядчики", "ответственность за монтаж"]),
    claim(38, 14, (290, 294), "SPEAKER_01", "Малый частный и малый-средний бизнес не обязательно откладывать без собственного регионального штата: можно убеждать, что электрик, разбирающийся в схемах, сможет поставить систему по листу настройки и схемам.", "sales_process_claim", "sales_process", ["sales_training", "manager_training", "strategy"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "marketing_claim_review", "strategy_claim_review"], terms=["электрик", "схема подключения", "лист настройки", "регион"]),
    claim(39, 14, (294, 303), "SPEAKER_02", "Региональная работа с прорабами может дать список электриков, которых можно проверить на нескольких инсталляциях и затем использовать как референс для монтажа.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["прораб", "электрик", "референс", "инсталляции"]),
    claim(40, 15, (309, 319), "SPEAKER_01", "В идеале региональный прораб сам является электриком и сам монтирует; если прораб не монтирует, он должен приводить проверенных электриков, иначе для компании это проблема качества.", "partner_model_claim", "partner_model", ["business_kb", "strategy", "sales_training"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["прораб", "электрик", "качество", "монтаж"]),
    claim(41, 15, (321, 331), "SPEAKER_02", "Практический порядок поиска: сначала искать электриков, готовых пробовать новое направление; если они есть, затем активнее работать с прорабами, у которых есть способные электрики.", "strategy_claim", "strategy", ["business_kb", "strategy"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["поиск электриков", "прорабы", "новое направление"]),
    claim(42, 15, (332, 338), "SPEAKER_01", "Качество нескольких разных региональных электриков трудно обеспечить; даже штатного электрика нужно контролировать фотографиями и проверками.", "risk_or_constraint", "risk", ["business_kb", "strategy", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["контроль качества", "фотографии", "штатный электрик", "регион"]),
    claim(43, 15, (338, 345), "SPEAKER_01", "Обучение может быть реализовано в виде визуализированной инструкции и коротких видеофрагментов, которые проще обновлять при изменении джамперов или поставок.", "operational_claim", "operations", ["business_kb", "manager_training", "electricians_kb"], "needs_confirmation", "source_backed", flags=["technical_confirmation_required", "strategy_claim_review"], terms=["видео", "визуализированная инструкция", "джамперы", "обучение"]),
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
        "interview_004_chunk_0001": [
            {"source_quote": chunk_by_id["interview_004_chunk_0001"]["text"], "reason": "noise", "notes": "Session scheduling and setup."}
        ],
        "interview_004_chunk_0007": [
            {"source_quote": chunk_by_id["interview_004_chunk_0007"]["text"], "reason": "noise", "notes": "Short time-management transition."}
        ],
        "interview_004_chunk_0016": [
            {"source_quote": chunk_by_id["interview_004_chunk_0016"]["text"], "reason": "not_business_relevant", "notes": "Camping business discussion; not promoted into Sveton Business KB in this pass."}
        ],
        "interview_004_chunk_0017": [
            {"source_quote": chunk_by_id["interview_004_chunk_0017"]["text"], "reason": "not_business_relevant", "notes": "Camping market/rules discussion; not promoted into Sveton Business KB in this pass."}
        ],
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
                        "Excluded or skipped as setup/off-topic."
                        if skipped_items and not claims
                        else "Full interview_004 extraction for Sveton-relevant business, sales, operations, partner, and technical-boundary items."
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
