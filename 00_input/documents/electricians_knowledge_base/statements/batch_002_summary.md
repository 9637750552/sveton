# Batch 002: первый широкий технический batch

Дата: 2026-06-16

Run:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_batch_002/
```

## Назначение

Проверить новую схему extraction на более широком наборе технических и операционных чанков после доработки контроля полноты.

Используется новая схема:

- `coverage_summary`;
- `skipped_source_items`;
- `coverage_warnings.jsonl`;
- collect с `--fail-on-errors --fail-on-warnings`.

## Исключения

Файл `Ищем_электриков_для_сотрудничества.docx` не включался в batch 002.

Причина: это рекрутинговый текст для объявления/вакансии, а не технический учебный или операционный материал.

## Состав batch

В batch вошло `30` чанков:

- `Обучение в офисе.docx`: `1` чанк;
- `Обязанности монтажника.docx`: `2` чанка;
- `Отчет по монтажу р1.docx`: `14` чанков;
- `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx`: `8` чанков;
- `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx`: `5` чанков.

## Результат collect

- Queue chunks: `30`;
- Parsed chunk results: `30`;
- Валидных утверждений: `129`;
- Ошибок: `0`;
- Coverage warnings: `0`;
- Promoted в общий `atomic_statements.jsonl`: нет.

Проверка:

```text
VALID: 129 statements
```

## Распределение по документам

- `Обучение в офисе.docx`: `33`;
- `Обязанности монтажника.docx`: `16`;
- `Отчет по монтажу р1.docx`: `47`;
- `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx`: `31`;
- `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx`: `2`.

## Распределение по типам

- `reporting_requirement`: `87`;
- `checklist_item`: `28`;
- `requirement`: `9`;
- `interview_signal`: `3`;
- `prohibition`: `2`.

## Распределение по темам

- `reporting`: `47`;
- `training_levels`: `33`;
- `photo_report`: `31`;
- `installer_roles`: `16`;
- `installation_request_check`: `2`.

## Риски и review

- `important`: `115`;
- `safety_critical`: `14`;
- `extracted`: `115`;
- `review_required`: `14`.

## Coverage

Все 30 чанков прошли coverage gate:

- `coverage_warnings.jsonl`: `0` строк;
- `extraction_errors.jsonl`: `0` строк.

Три заголовочных чанка из документа проверки заявки менеджера (`doc_007_chunk_0001`, `doc_007_chunk_0002`, `doc_007_chunk_0003`) обработаны как чанки без самостоятельных утверждений.

## Quality audit

Выборочный смысловой аудит: [review/batch_002_quality_audit.md](review/batch_002_quality_audit.md).

Итог: **quality gate failed**.

Причины:

- заголовки превращены в утверждения;
- есть шаблонные слабые формулировки;
- длинные пункты обязанностей монтажника не разбиты на атомарные действия;
- coverage gate не поймал пропуск пункта `Напряжение внешней сети -`;
- HTML-таблица контрольного листа обработана шумно.

Пользователь подтвердил часть проблем на ручном просмотре: пункты `1` и `13` являются заголовками, `19/22/23` выглядят как дубли, `30/31` непонятны без табличного контекста.

Решение: batch 002 не продвигать в canonical. Считать диагностическим прогоном.

## Артефакты

- Machine output: `runs/run_20260616_batch_002/parsed/atomic_statements.jsonl`
- Chunk results: `runs/run_20260616_batch_002/parsed/chunk_results.jsonl`
- Review file: `review/batch_002_review.md`

## Следующее решение

Перед следующим batch нужно доработать extraction pipeline v3:

- запретить утверждения из одних заголовков;
- добавить явную типизацию source items;
- расширить skipped reasons для `heading`, `table_header`, `context_only`;
- усилить атомарность длинных пунктов;
- добавить table-aware extraction;
- добавить quality warnings по HTML/table fragments, табличным значениям без контекста, дублям, длинным неатомарным пунктам и шаблонным формулировкам;
- повторить batch 002 после доработки.

Статус v3: доработка внесена в prompt/schema/runner. Диагностический batch 002 остается непродвинутым; для повторной проверки нужно создать новый run по v3.

Повторная проверка выполнена как batch 002 v3: [batch_002_v3_summary.md](batch_002_v3_summary.md).

Результат v3 после Codex-ревью и пользовательского подтверждения: `132` валидных утверждения, `0` ошибок, `0` coverage / quality warnings. V3-результат продвинут в canonical `atomic_statements.jsonl`.
