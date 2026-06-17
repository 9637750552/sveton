#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import validate_atomic_statements as statement_validator


DEFAULT_STATEMENTS_DIR = Path("00_input/documents/electricians_knowledge_base/statements")
DEFAULT_CHUNKS_PATH = Path("00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl")
PROMPT_PATH = DEFAULT_STATEMENTS_DIR / "atomic_extraction_prompt.md"
ATOMIC_STATEMENTS_PATH = DEFAULT_STATEMENTS_DIR / "atomic_statements.jsonl"
EXTRACTION_ERRORS_PATH = DEFAULT_STATEMENTS_DIR / "extraction_errors.jsonl"
COVERAGE_WARNINGS_PATH = DEFAULT_STATEMENTS_DIR / "coverage_warnings.jsonl"

SOURCE_ITEM_RE = re.compile(r"^\s*(?:[-*•]\s+|\\-\s+|\d+[.)]\s+|[A-Za-zА-Яа-я]\)\s+)")
SOURCE_FIELD_RE = re.compile(r"^[A-Za-zА-Яа-яЁё0-9№][^<>\n]{2,100}\s[-–—:]$")
HTML_TAG_RE = re.compile(r"<[^>]+>")
IMAGE_MARKER_RE = re.compile(r"\[IMAGE:[^\]]+\]")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZА-ЯЁ0-9])")
NUMERIC_VALUE_RE = re.compile(r"\b\d+(?:[,.]\d+)?\s*(?:В|А|Ач|мм|см|метр|метра|м|%|кВт|Вт)\b", re.IGNORECASE)
TECHNICAL_MARKERS = (
    "акб",
    "инвертор",
    "ибп",
    "узо",
    "байпас",
    "щит",
    "автомат",
    "выключатель",
    "контактор",
    "фаза",
    "ноль",
    "нейтрал",
    "заземл",
    "dc",
    "ac",
    "вход",
    "выход",
    "ток",
    "напряж",
    "заряд",
    "кабель",
    "провод",
    "перемыч",
    "клемм",
    "нагруз",
    "резерв",
    "сеть",
    "генератор",
)
MODAL_ACTION_MARKERS = (
    "долж",
    "необходимо",
    "нужно",
    "нельзя",
    "запрещ",
    "важно",
    "следует",
    "треб",
    "провер",
    "контрол",
    "подключ",
    "установ",
    "переключ",
    "включ",
    "отключ",
    "соблюд",
    "выбира",
    "производ",
    "осуществ",
    "использ",
    "располаг",
    "монтир",
    "собир",
)
CONDITION_MARKERS = (
    "если",
    "при ",
    "перед ",
    "после ",
    "в случае",
    "когда",
    "например",
    "предположим",
)

HEADING_LABELS = {
    "краткое интервью",
    "комментарий",
    "настройки",
    "особенности",
    "фото элементов системы",
    "задание для переборки щита",
    "кабель-трасса",
}
TABLE_CONTEXTLESS_VALUES = {
    "удовлетворительные",
    "неудовлетворительные",
}
GENERIC_TEMPLATE_MARKERS = (
    "нужно указать или учитывать",
    "нужно отработать или оценить",
    "нужно выполнить требование",
)
HTML_TABLE_MARKERS = (
    "<table",
    "</table",
    "<tr",
    "</tr",
    "<td",
    "</td",
    "<th",
    "</th",
)

ROLE_MAP = {
    "монтажник": "installer",
    "электрик": "electrician",
    "менеджер": "manager",
    "инженер ГО": "hq_engineer",
    "руководитель": "leader",
    "клиент": "customer",
}

TOPIC_MAP = {
    "Сервисный выезд": "service_visit",
    "Поиск электриков для сотрудничества": "hiring_and_interview",
    "Офисное обучение монтажников": "training_levels",
    "Обязанности монтажника": "installer_roles",
    "Отчетность по монтажу": "reporting",
    "Фотофиксация монтажа": "photo_report",
    "Проверка заявки на монтаж": "installation_request_check",
    "Работа на объекте": "work_on_site",
    "Установка УЗО": "safety",
    "Уровни монтажника": "training_levels",
    "Базовые понятия": "basic_knowledge",
    "Технические карты изделий": "ups_components",
    "Состав ИБП": "ups_components",
    "Процесс монтажа": "installation_process",
    "Этапы монтажа": "installation_process",
    "Элементы распределительных щитов": "distribution_boards",
    "Переборка щитов": "distribution_boards",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def select_chunks(
    chunks: list[dict[str, Any]],
    include_review: bool,
    limit: int | None,
    chunk_ids: set[str],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for chunk in chunks:
        if chunk_ids and chunk["chunk_id"] not in chunk_ids:
            continue
        if chunk.get("needs_review") and not include_review:
            continue
        selected.append(chunk)
        if limit is not None and len(selected) >= limit:
            break
    return selected


def prompt_input_for_chunk(chunk: dict[str, Any]) -> dict[str, Any]:
    fields = [
        "chunk_id",
        "source_document_id",
        "source_file",
        "topic",
        "roles",
        "section_path",
        "text",
        "related_image_ids",
        "excluded_image_ids",
        "previous_context",
        "next_context",
        "needs_review",
        "review_reasons",
    ]
    payload = {field: chunk.get(field) for field in fields}
    payload["suggested_topic"] = TOPIC_MAP.get(str(chunk.get("topic", "")), "unknown")
    payload["suggested_roles"] = [
        ROLE_MAP.get(str(role).strip(), "installer")
        for role in chunk.get("roles", [])
        if str(role).strip()
    ]
    payload["suggested_roles"] = sorted(set(payload["suggested_roles"]))
    return payload


def prepare_run(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    chunks = load_jsonl(project_root / DEFAULT_CHUNKS_PATH)
    prompt_path = project_root / PROMPT_PATH
    if not prompt_path.exists():
        print(f"Prompt not found: {prompt_path}", file=sys.stderr)
        return 1

    selected = select_chunks(chunks, args.include_review, args.limit, set(args.chunk_id or []))
    run_id = args.run_id or datetime.now().strftime("run_%Y%m%d_%H%M%S")
    run_dir = project_root / DEFAULT_STATEMENTS_DIR / "runs" / run_id
    inputs_dir = run_dir / "inputs"
    raw_dir = run_dir / "raw"
    parsed_dir = run_dir / "parsed"
    prompts_dir = run_dir / "prompts"

    for directory in (inputs_dir, raw_dir, parsed_dir, prompts_dir):
        directory.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(prompt_path, run_dir / "atomic_extraction_prompt.md")

    queue_rows: list[dict[str, Any]] = []
    prompt_text = prompt_path.read_text(encoding="utf-8")
    for chunk in selected:
        chunk_id = chunk["chunk_id"]
        input_payload = prompt_input_for_chunk(chunk)
        input_path = inputs_dir / f"{chunk_id}.json"
        prompt_packet_path = prompts_dir / f"{chunk_id}.md"
        input_path.write_text(json.dumps(input_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        prompt_packet_path.write_text(
            "\n\n".join(
                [
                    prompt_text,
                    "## Source Chunk Input",
                    "```json",
                    json.dumps(input_payload, ensure_ascii=False, indent=2),
                    "```",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        queue_rows.append(
            {
                "chunk_id": chunk_id,
                "source_file": chunk["source_file"],
                "needs_review": chunk.get("needs_review", False),
                "related_image_ids": chunk.get("related_image_ids", []),
                "input_path": str(input_path.relative_to(run_dir)),
                "prompt_packet_path": str(prompt_packet_path.relative_to(run_dir)),
                "raw_output_path": str((raw_dir / f"{chunk_id}.json").relative_to(run_dir)),
            }
        )

    write_jsonl(run_dir / "queue.jsonl", queue_rows)
    manifest = {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "prepare",
        "chunk_count": len(selected),
        "include_review": args.include_review,
        "prompt": str((run_dir / "atomic_extraction_prompt.md").relative_to(project_root)),
        "queue": str((run_dir / "queue.jsonl").relative_to(project_root)),
        "inputs_dir": str(inputs_dir.relative_to(project_root)),
        "raw_dir": str(raw_dir.relative_to(project_root)),
        "parsed_dir": str(parsed_dir.relative_to(project_root)),
        "notes": [
            "Put one model response per chunk into raw/<chunk_id>.json.",
            "Each raw response must be a JSON object with source_chunk_id, coverage_summary, skipped_source_items, and statements.",
            "Run collect mode after raw outputs are present.",
        ],
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "README.md").write_text(render_run_readme(manifest), encoding="utf-8")

    print(f"Prepared {len(selected)} chunks in {run_dir}")
    return 0


def render_run_readme(manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Atomic Extraction Run: {manifest['run_id']}",
            "",
            "## Назначение",
            "",
            "Эта папка содержит очередь чанков для массового извлечения атомарных утверждений.",
            "",
            "## Как использовать",
            "",
            "1. Для каждого файла `prompts/<chunk_id>.md` получить ответ модели.",
            "2. Сохранить ответ в `raw/<chunk_id>.json`.",
            "3. Запустить collect mode runner-а.",
            "",
            "## Важно",
            "",
            "- Review/PDF чанки исключены, если run создан без `--include-review`.",
            "- Ответ модели должен быть чистым JSON либо JSON внутри markdown code fence.",
            "- Ответ модели должен содержать `coverage_summary` и `skipped_source_items`.",
            "- Валидатор проверит точные цитаты, image ids, safety flags и связь с чанком.",
            "- Runner создаст `parsed/coverage_warnings.jsonl`, если покрытие чек-листа выглядит неполным.",
            "",
            f"Всего чанков в очереди: `{manifest['chunk_count']}`.",
            "",
        ]
    )


def extract_json_object(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    if not text:
        raise ValueError("empty raw output")
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
        raise ValueError("raw JSON is not an object")
    except json.JSONDecodeError:
        pass

    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.IGNORECASE | re.DOTALL)
    if fence:
        parsed = json.loads(fence.group(1))
        if isinstance(parsed, dict):
            return parsed
        raise ValueError("fenced JSON is not an object")

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON object found")
    parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("extracted JSON is not an object")
    return parsed


def source_item_candidates(text: str) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    seen: set[str] = set()

    def add_candidate(quote: str, source_item_type: str) -> None:
        clean = strip_markup(IMAGE_MARKER_RE.sub(" ", quote))
        if not clean or len(clean) < 12:
            return
        if looks_like_heading_label(quote):
            return
        normalized = normalize_for_duplicate(clean)
        if not normalized or normalized in seen:
            return
        seen.add(normalized)
        candidates.append({"quote": quote.strip(), "source_item_type": source_item_type})

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("[IMAGE:") or TABLE_SEPARATOR_RE.match(stripped):
            continue
        clean_line = strip_markup(stripped)
        if SOURCE_ITEM_RE.match(stripped):
            add_candidate(stripped, "list_item")
            continue
        if SOURCE_FIELD_RE.match(clean_line):
            add_candidate(stripped, "field")
            continue
        if stripped.startswith("|"):
            without_images = IMAGE_MARKER_RE.sub(" ", stripped)
            for cell in without_images.strip("|").split("|"):
                add_candidate(cell, "table_cell")
            continue
        for sentence in SENTENCE_SPLIT_RE.split(stripped):
            sentence = sentence.strip()
            if is_meaningful_paragraph_source_item(sentence):
                add_candidate(sentence, "paragraph_sentence")
    return candidates


def count_explicit_source_items(text: str) -> int:
    return len(source_item_candidates(text))


def strip_markup(value: str) -> str:
    unescaped = html.unescape(value)
    without_tags = HTML_TAG_RE.sub(" ", unescaped)
    without_markdown = re.sub(r"[*_`#>]+", " ", without_tags)
    without_markdown = re.sub(r"\[[ xX]\]", " ", without_markdown)
    return re.sub(r"\s+", " ", without_markdown).strip(" -–—|:;")


def normalize_for_duplicate(value: str) -> str:
    clean = strip_markup(value).lower()
    clean = re.sub(r"[^\wа-яё]+", " ", clean, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", clean).strip()


def is_meaningful_paragraph_source_item(value: str) -> bool:
    clean = strip_markup(IMAGE_MARKER_RE.sub(" ", value))
    if len(clean) < 45:
        return False
    if looks_like_heading_label(value):
        return False
    lower = clean.lower()
    has_technical_marker = any(marker in lower for marker in TECHNICAL_MARKERS)
    if not has_technical_marker:
        return False
    has_action_or_condition = any(marker in lower for marker in MODAL_ACTION_MARKERS) or any(
        marker in lower for marker in CONDITION_MARKERS
    )
    has_numeric_value = bool(NUMERIC_VALUE_RE.search(clean))
    return has_action_or_condition or has_numeric_value


def looks_like_heading_label(value: str) -> bool:
    clean = strip_markup(value)
    if not clean:
        return False
    normalized = clean.lower().strip(" .:")
    if normalized in HEADING_LABELS:
        return True
    if value.strip().endswith(":") and len(clean.split()) <= 8:
        return True
    return False


def build_quality_warnings(chunk: dict[str, Any], statements: list[Any]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    seen_normalized: dict[str, str] = {}

    for statement in statements:
        if not isinstance(statement, dict):
            continue
        statement_id = str(statement.get("statement_id", ""))
        statement_text = str(statement.get("statement", ""))
        source_quote = str(statement.get("source_quote", ""))
        statement_lower = statement_text.lower()
        source_quote_lower = source_quote.lower()
        clean_statement = strip_markup(statement_text).lower()

        warning_base = {
            "chunk_id": chunk["chunk_id"],
            "stage": "quality",
            "statement_id": statement_id,
            "source_file": chunk.get("source_file"),
        }

        if looks_like_heading_label(statement_text) or looks_like_heading_label(source_quote):
            warnings.append(
                {
                    **warning_base,
                    "warning": "statement_looks_like_heading_label",
                    "statement": statement_text,
                    "source_quote": source_quote,
                }
            )

        if any(marker in statement_lower for marker in GENERIC_TEMPLATE_MARKERS):
            warnings.append(
                {
                    **warning_base,
                    "warning": "generic_template_statement",
                    "statement": statement_text,
                }
            )

        if any(marker in source_quote_lower for marker in HTML_TABLE_MARKERS):
            warnings.append(
                {
                    **warning_base,
                    "warning": "html_table_fragment_statement",
                    "source_quote": source_quote[:240],
                }
            )

        if clean_statement in TABLE_CONTEXTLESS_VALUES:
            warnings.append(
                {
                    **warning_base,
                    "warning": "contextless_table_value_statement",
                    "statement": statement_text,
                }
            )

        normalized = normalize_for_duplicate(statement_text)
        if len(normalized) >= 24:
            previous_statement_id = seen_normalized.get(normalized)
            if previous_statement_id:
                warnings.append(
                    {
                        **warning_base,
                        "warning": "duplicate_normalized_statement",
                        "duplicate_of_statement_id": previous_statement_id,
                        "statement": statement_text,
                    }
                )
            else:
                seen_normalized[normalized] = statement_id

        separator_count = sum(source_quote.count(separator) for separator in (";", "\n", ". ", ".\n"))
        if len(statement_text) > 260 or (len(source_quote) > 320 and separator_count >= 2):
            warnings.append(
                {
                    **warning_base,
                    "warning": "possibly_non_atomic_long_statement",
                    "statement_length": len(statement_text),
                    "source_quote_length": len(source_quote),
                    "source_quote": source_quote[:240],
                }
            )

    return warnings


def build_coverage_warnings(chunk: dict[str, Any], result: dict[str, Any], statements: list[Any]) -> list[dict[str, Any]]:
    warnings = build_quality_warnings(chunk, statements)
    chunk_id = chunk["chunk_id"]
    source_items = source_item_candidates(str(chunk.get("text", "")))
    explicit_source_items = len(source_items)
    coverage_summary = result.get("coverage_summary")
    skipped_source_items = result.get("skipped_source_items")
    skipped_count = len(skipped_source_items) if isinstance(skipped_source_items, list) else 0
    covered_count = len(statements) + skipped_count

    if explicit_source_items == 0:
        return warnings

    detected = None
    if isinstance(coverage_summary, dict):
        detected_value = coverage_summary.get("source_items_detected")
        if isinstance(detected_value, int):
            detected = detected_value

    if detected is not None and detected < explicit_source_items:
        warnings.append(
            {
                "chunk_id": chunk_id,
                "stage": "coverage",
                "warning": "detected_source_items_below_candidate_count",
                "explicit_source_items": explicit_source_items,
                "source_items_detected": detected,
                "source_file": chunk.get("source_file"),
                "candidate_source_items": [item["quote"][:180] for item in source_items[:8]],
            }
        )

    if covered_count < explicit_source_items:
        warnings.append(
            {
                "chunk_id": chunk_id,
                "stage": "coverage",
                "warning": "covered_source_items_below_candidate_count",
                "explicit_source_items": explicit_source_items,
                "statements": len(statements),
                "skipped_source_items": skipped_count,
                "covered_source_items": covered_count,
                "source_file": chunk.get("source_file"),
                "candidate_source_items": [item["quote"][:180] for item in source_items[:8]],
            }
        )

    covered_quotes = []
    for statement in statements:
        if isinstance(statement, dict):
            covered_quotes.append(str(statement.get("source_quote", "")))
    if isinstance(skipped_source_items, list):
        for item in skipped_source_items:
            if isinstance(item, dict):
                covered_quotes.append(str(item.get("source_item_quote", "")))

    uncovered = []
    for item in source_items:
        if not source_item_is_covered(item["quote"], covered_quotes):
            uncovered.append(item)

    if uncovered:
        warnings.append(
            {
                "chunk_id": chunk_id,
                "stage": "coverage",
                "warning": "candidate_source_items_uncovered",
                "uncovered_count": len(uncovered),
                "uncovered_source_items": [
                    {"quote": item["quote"][:240], "source_item_type": item["source_item_type"]}
                    for item in uncovered[:12]
                ],
                "source_file": chunk.get("source_file"),
            }
        )

    return warnings


def source_item_is_covered(candidate_quote: str, covered_quotes: list[str]) -> bool:
    candidate_norm = normalize_for_duplicate(IMAGE_MARKER_RE.sub(" ", candidate_quote))
    if not candidate_norm:
        return True
    candidate_tokens = set(candidate_norm.split())
    for covered_quote in covered_quotes:
        covered_norm = normalize_for_duplicate(IMAGE_MARKER_RE.sub(" ", covered_quote))
        if not covered_norm:
            continue
        if candidate_norm in covered_norm or covered_norm in candidate_norm:
            return True
        covered_tokens = set(covered_norm.split())
        if candidate_tokens:
            overlap = len(candidate_tokens & covered_tokens) / len(candidate_tokens)
            if overlap >= 0.82:
                return True
    return False


def collect_run(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    run_dir = (project_root / args.run_dir).resolve()
    raw_dir = run_dir / "raw"
    parsed_dir = run_dir / "parsed"
    queue_path = run_dir / "queue.jsonl"

    if not queue_path.exists():
        print(f"Queue not found: {queue_path}", file=sys.stderr)
        return 1
    if not raw_dir.exists():
        print(f"Raw output directory not found: {raw_dir}", file=sys.stderr)
        return 1
    parsed_dir.mkdir(parents=True, exist_ok=True)

    chunks = statement_validator.load_chunks(project_root)
    queue_rows = load_jsonl(queue_path)
    all_statements: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    coverage_warnings: list[dict[str, Any]] = []
    parsed_results: list[dict[str, Any]] = []
    seen_statement_ids: set[str] = set()

    for queue_row in queue_rows:
        chunk_id = queue_row["chunk_id"]
        raw_path = raw_dir / f"{chunk_id}.json"
        if not raw_path.exists():
            errors.append({"chunk_id": chunk_id, "stage": "missing_raw", "error": f"missing {raw_path.name}"})
            continue
        try:
            result = extract_json_object(raw_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append({"chunk_id": chunk_id, "stage": "parse_raw", "error": str(exc)})
            continue

        if result.get("source_chunk_id") != chunk_id:
            errors.append(
                {
                    "chunk_id": chunk_id,
                    "stage": "chunk_id_mismatch",
                    "error": f"raw source_chunk_id={result.get('source_chunk_id')!r}",
                }
            )
            continue
        result_validation_errors = statement_validator.validate_chunk_result(result, chunks)
        if result_validation_errors:
            errors.append(
                {
                    "chunk_id": chunk_id,
                    "stage": "result_validation",
                    "error": result_validation_errors,
                }
            )
        statements = result.get("statements")
        if not isinstance(statements, list):
            errors.append({"chunk_id": chunk_id, "stage": "shape", "error": "statements must be an array"})
            continue

        for idx, statement in enumerate(statements, start=1):
            if not isinstance(statement, dict):
                errors.append({"chunk_id": chunk_id, "stage": "shape", "error": f"statement {idx} is not an object"})
                continue
            validation_errors = statement_validator.validate_statement(statement, chunks, idx)
            statement_id = statement.get("statement_id")
            if statement_id in seen_statement_ids:
                validation_errors.append(f"duplicate statement_id {statement_id}")
            seen_statement_ids.add(statement_id)
            if validation_errors:
                errors.append(
                    {
                        "chunk_id": chunk_id,
                        "statement_id": statement.get("statement_id"),
                        "stage": "validation",
                        "error": validation_errors,
                    }
                )
                continue
            all_statements.append(statement)
        chunk = chunks.get(chunk_id)
        if chunk:
            coverage_warnings.extend(build_coverage_warnings(chunk, result, statements))
        parsed_results.append(result)

    write_jsonl(parsed_dir / "chunk_results.jsonl", parsed_results)
    write_jsonl(parsed_dir / "atomic_statements.jsonl", all_statements)
    write_jsonl(parsed_dir / "extraction_errors.jsonl", errors)
    write_jsonl(parsed_dir / "coverage_warnings.jsonl", coverage_warnings)

    if args.promote:
        write_jsonl(project_root / ATOMIC_STATEMENTS_PATH, all_statements)
        write_jsonl(project_root / EXTRACTION_ERRORS_PATH, errors)
        write_jsonl(project_root / COVERAGE_WARNINGS_PATH, coverage_warnings)

    summary = {
        "run_dir": str(run_dir),
        "queue_chunks": len(queue_rows),
        "parsed_chunk_results": len(parsed_results),
        "valid_statements": len(all_statements),
        "errors": len(errors),
        "coverage_warnings": len(coverage_warnings),
        "promoted": args.promote,
    }
    (parsed_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors and args.fail_on_errors:
        return 1
    if coverage_warnings and args.fail_on_warnings:
        return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Prepare and collect atomic statement extraction runs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Prepare prompt packets for selected chunks.")
    prepare.add_argument("project_root")
    prepare.add_argument("--run-id")
    prepare.add_argument("--include-review", action="store_true")
    prepare.add_argument("--limit", type=int)
    prepare.add_argument("--chunk-id", action="append")
    prepare.set_defaults(func=prepare_run)

    collect = subparsers.add_parser("collect", help="Parse and validate raw model outputs for a run.")
    collect.add_argument("project_root")
    collect.add_argument("run_dir")
    collect.add_argument("--promote", action="store_true", help="Write parsed outputs to canonical statements files.")
    collect.add_argument("--fail-on-errors", action="store_true")
    collect.add_argument("--fail-on-warnings", action="store_true")
    collect.set_defaults(func=collect_run)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
