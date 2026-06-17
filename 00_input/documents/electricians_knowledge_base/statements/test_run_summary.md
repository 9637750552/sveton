# Тестовый прогон извлечения атомарных утверждений

Дата: 2026-06-16

## Назначение

Этот файл фиксирует первый контрольный прогон извлечения атомарных утверждений на небольшой выборке чанков.

Это не полный `atomic_statements.jsonl`. Цель теста - проверить prompt, JSON-схему, валидатор, точность цитат и правила `related_image_ids`.

## Артефакты

- Prompt: `atomic_extraction_prompt.md`
- JSON Schema одного утверждения: `atomic_statement.schema.json`
- JSON Schema результата по чанку: `chunk_extraction_result.schema.json`
- Тестовый JSONL: `test_atomic_statements.jsonl`
- Валидатор: `06_scripts/validate_atomic_statements.py`
- Runner массового прогона: `mass_extraction_runner.md`

## Выборка чанков

| Chunk ID | Тема | Что проверяли |
|---|---|---|
| `doc_001_chunk_0001` | service_visit | сервисные действия, отчетность, safety-флаг |
| `doc_002_chunk_0001` | hiring_and_interview | найм, договорная модель сотрудничества |
| `doc_006_chunk_0010` | photo_report | фотоотчет и `related_image_ids` |
| `doc_011_chunk_0006` | basic_knowledge | определения и схема подключения АКБ |
| `doc_013_chunk_0004` | ups_components | определения по инвертору |
| `doc_015_chunk_0004` | installation_process | этап подготовки к монтажу |
| `doc_016_chunk_0003` | distribution_boards | заземление и safety-critical ревью |

## Результат

- Извлечено тестовых утверждений: `20`.
- Покрыто чанков: `7`.
- Утверждений с `related_image_ids`: `7`.
- Утверждений `review_required`: `3`.
- Валидатор: `VALID`.

Распределение по типам:

- `definition`: `8`;
- `requirement`: `4`;
- `checklist_item`: `3`;
- `process_step`: `2`;
- `instruction_step`: `1`;
- `interview_signal`: `1`;
- `reporting_requirement`: `1`.

Распределение по риску:

- `ordinary`: `2`;
- `important`: `15`;
- `safety_critical`: `3`.

## Что проверено

- Все `source_quote` являются точными подстроками соответствующего `text` чанка.
- Все `related_image_ids` существуют в соответствующем чанке.
- `excluded_image_ids` не используются в утверждениях.
- Safety-critical утверждения отправлены в `review_required`.
- Изображения используются только как визуальная опора к текстовым утверждениям.
- Утверждения из `previous_context` и `next_context` не извлекались.
- Runner `collect` проверен на smoke-run из 2 чанков: `7` валидных утверждений, `0` ошибок.

## Решения перед массовым прогоном

- Оставляем `source_quote` обязательным и точным.
- Оставляем safety-critical утверждения в `review_required` даже при высокой уверенности.
- Массовое извлечение можно запускать по одному чанку или небольшими батчами.
- Для PDF-чанков с `pdf_text_layout_review_required` массовое извлечение лучше не запускать до ручного решения по качеству текста.
- После массового прогона нужен отдельный validation gate: JSON validation, source quote validation, image id validation, review queue.

## Следующий шаг

Подготовить runner для массового извлечения атомарных утверждений по `source_chunks.jsonl`:

- формировать prompt input на один чанк;
- сохранять raw model output;
- парсить JSON;
- валидировать каждое утверждение;
- сохранять ошибки отдельно;
- не обрабатывать PDF/review chunks без явного разрешения.
