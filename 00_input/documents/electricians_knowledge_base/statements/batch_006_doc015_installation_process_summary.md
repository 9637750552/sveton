# Batch 006: doc_015 installation process

Дата: 2026-06-17

Источник:

- `ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx`

Run-папки:

- `runs/run_20260617_doc015_batch_a_v1`
- `runs/run_20260617_doc015_batch_b_v1`
- `runs/run_20260617_doc015_batch_c_v1`

## Результат extraction

- Обработано содержательных чанков: `16`.
- Заголовочные/context chunks пропущены: `4`.
- Валидных утверждений: `101`.
- Errors: `0`.
- Coverage / quality warnings: `0`.
- Promotion в canonical: да.

## Canonical после promotion

- Было: `286` утверждений.
- Добавлено: `101` утверждение.
- Стало: `387` утверждений.
- Валидация `atomic_statements.jsonl`: passed.

## Source coverage

Отдельный отчет:

- `source_coverage_doc015.md`
- `source_coverage_doc015.jsonl`

Результат по `doc_015`:

- `covered`: `16`
- `ignored`: `4`
- `uncovered_content`: `0`

Общий source coverage report пересобран по `9` закрытым источникам:

- `source_coverage_report.md`
- `source_coverage_report.jsonl`

Итог общего отчета:

- chunks checked: `124`
- `covered`: `84`
- `ignored`: `40`
- `uncovered_content`: `0`

## Методологическое изменение

Перед promotion добавлен paragraph coverage gate в `06_scripts/run_atomic_extraction.py`.

Причина: документ `doc_015` показал, что содержательные утверждения в обычных абзацах могут не ловиться старым bullet/checklist gate. Новый gate проверяет покрытие конкретных candidate source items через `source_quote` или `skipped_source_items`.

Это изменение нужно также для будущего эпика semantic extraction по интервью с руководством, где основная структура источников будет абзацной.

## Ограничения

- Кластеризация обновлена: `101` утверждение batch 006 сгруппировано в `C009 / installation_process`.
- Раздел `04_installation_process.md` собран как source-backed draft editorial layer.
- `safety_review_queue.md` обновлен под batch 006; детальный пакет создан в `safety_review_c009_installation_process.md`.
- `statement_images.jsonl`, `statement_relations.jsonl` и `duplicates.md` еще не пересобраны под batch 006.
- Перед финальным использованием раздела нужен экспертный technical safety-review по `SR011-SR016` и отдельный image-link pass по `doc_015`.
