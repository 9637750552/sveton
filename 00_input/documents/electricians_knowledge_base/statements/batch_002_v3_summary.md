# Batch 002 v3: повторный широкий batch после quality gate

Дата: 2026-06-16

Модель шага: `5.5`, уровень: `самый высокий`.

Run:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_batch_002_v3/
```

## Назначение

Повторить diagnostic batch 002 на том же составе `30` чанков, но уже по extraction pipeline v3.

В v3 проверялись проблемы, найденные в предыдущем batch:

- заголовки и служебные метки не должны попадать в утверждения;
- HTML-таблицы не должны давать отдельные утверждения по ячейкам;
- длинные пункты обязанностей нужно атомизировать;
- шаблонные формулировки не должны проходить quality gate;
- короткие строки-поля отчета должны учитываться coverage detector-ом.

## Исключения

Файл `Ищем_электриков_для_сотрудничества.docx` не включался, как и в diagnostic batch 002.

Причина: это рекрутинговый текст для объявления/вакансии, а не технический учебный или операционный материал.

## Состав batch

Состав идентичен diagnostic batch 002:

- `Обучение в офисе.docx`: `1` чанк;
- `Обязанности монтажника.docx`: `2` чанка;
- `Отчет по монтажу р1.docx`: `14` чанков;
- `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx`: `8` чанков;
- `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx`: `5` чанков.

## Результат collect

- Queue chunks: `30`;
- Parsed chunk results: `30`;
- Валидных утверждений: `132`;
- Ошибок: `0`;
- Coverage / quality warnings: `0`;
- Promoted в общий `atomic_statements.jsonl`: да, после пользовательского подтверждения.

Проверка:

```text
VALID: 132 statements
```

## Распределение по документам

- `Отчет по монтажу р1.docx`: `50`;
- `Обязанности монтажника.docx`: `31`;
- `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx`: `30`;
- `Обучение в офисе.docx`: `19`;
- `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx`: `2`.

## Распределение по типам

- `reporting_requirement`: `87`;
- `requirement`: `25`;
- `checklist_item`: `13`;
- `recommendation`: `4`;
- `interview_signal`: `3`.

## Распределение по темам

- `reporting`: `50`;
- `installer_roles`: `31`;
- `photo_report`: `30`;
- `training_levels`: `19`;
- `installation_request_check`: `2`.

## Риски и review

- `important`: `80`;
- `safety_critical`: `52`;
- `extracted`: `80`;
- `review_required`: `52`.

## Отличия от diagnostic batch 002

Diagnostic batch 002 дал `129` валидных JSON-утверждений, но провалил смысловой quality gate.

Batch 002 v3 после Codex-ревью дал `132` утверждения и прошел machine gate без warnings.

Ключевые изменения:

- `Краткое интервью:`, `Комментарий:` и похожие заголовки больше не извлекаются как утверждения;
- табличные ячейки `Удовлетворительные` / `Неудовлетворительные` не попали в утверждения;
- HTML-таблица контрольного листа в `doc_003_chunk_0001` вынесена в `skipped_source_items` как табличный блок для отдельного структурного разбора;
- обязанности монтажника в `doc_004` атомизированы подробнее, поэтому по этому документу стало больше утверждений;
- поля отчета вроде `Напряжение внешней сети -` учтены и не пропущены coverage gate.
- фото-чеклист нормализован без чекбокс-маркеров, а составные пункты про АТОМ, настройки инвертора и дополнительные фото разделены на атомарные утверждения.

## Артефакты

- Machine output: `runs/run_20260616_batch_002_v3/parsed/atomic_statements.jsonl`
- Chunk results: `runs/run_20260616_batch_002_v3/parsed/chunk_results.jsonl`
- Review file: `review/batch_002_v3_review.md`
- Codex audit: `review/batch_002_v3_codex_audit.md`
- Errors: `runs/run_20260616_batch_002_v3/parsed/extraction_errors.jsonl`
- Warnings: `runs/run_20260616_batch_002_v3/parsed/coverage_warnings.jsonl`
- Clusters v1: `statement_clusters.md`, `statement_clusters.json`
- Duplicate candidates v1: `duplicates.md`
- Statement relations v1: `statement_relations.jsonl`
- Safety-review queue v1: `safety_review_queue.md`

## Решение

Пользователь бегло просмотрел первые `50` утверждений и подтвердил, что они выглядят корректно.

Batch 002 v3 продвинут в canonical:

```text
00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl
```

Canonical-проверка на момент promotion batch 002 v3: `132` валидных утверждения, `0` errors, `0` warnings.

## Addendum: completion-pass по документу проверки заявки

После сборки редакционного раздела `12_installation_request_check.md` обнаружено, что документ `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx` был покрыт неполно: batch 002 v3 включал только первые `5` чанков этого документа, а содержательные чанки `doc_007_chunk_0006` - `doc_007_chunk_0016` не попали в canonical.

Выполнен completion-pass:

- источник новых утверждений: `doc_007_completion_statements.jsonl`;
- добавлено `18` валидных atomic statements;
- canonical расширен с `132` до `150` утверждений;
- кластер `C005 / installation_request_check` расширен с `2` до `20` утверждений;
- `12_installation_request_check.md` пересобран по полному coverage этого источника.

Проверка после completion-pass:

```text
VALID: 150 statements
```

После запуска source coverage gate по пяти текущим редакционным источникам найдено `6` content chunks без прямого покрытия. Разбор показал:

- `1` чанк содержал реальный пропуск по примеру отчета монтажа; добавлено утверждение `doc_005_chunk_0010_stmt_001`;
- `5` чанков являются split/duplicate-фрагментами и оформлены в `source_coverage_overrides.jsonl`;
- canonical расширен до `151` валидного утверждения.

Проверка после закрытия source coverage:

```text
VALID: 151 statements
```

## Следующий слой после canonical

Созданы первичные артефакты группировки:

- `statement_clusters.md`: пять смысловых кластеров;
- `statement_clusters.json`: machine-readable описание кластеров с точными `statement_ids` для всех `151` canonical-утверждения;
- `duplicates.md`: кандидаты на дедупликацию и связи rule/example/related;
- `statement_relations.jsonl`: `41` связь между утверждениями;
- `safety_review_queue.md`: очередь проверки safety-critical тем;
- `statement_images.jsonl`: связи утверждений с визуальными примерами.

Создан первый редакционный раздел базы знаний:

- `01_docs/operations/electricians_knowledge_base/07_photo_report.md`: раздел фотоотчета и фотофиксации монтажа, собран из кластера `C004 / photo_report`, содержит `30` ссылок на canonical `statement_id`, `2` визуальных примера и пометки `safety-review`.
- `01_docs/operations/electricians_knowledge_base/08_installer_roles.md`: раздел обязанностей монтажника на выезде, собран из кластера `C002 / installer_roles`, содержит `31` ссылку на canonical `statement_id` и контрольный чек-лист выезда.
- `01_docs/operations/electricians_knowledge_base/09_installation_report.md`: раздел отчета по монтажу, собран из кластера `C003 / reporting`, содержит `51` ссылку на canonical `statement_id`, копируемый шаблон отчета и пример заполнения.
- `01_docs/operations/electricians_knowledge_base/10_training_levels.md`: раздел офисного обучения и проверки монтажника, собран из кластера `C001 / training_levels`, содержит `19` ссылок на canonical `statement_id`; HTML-таблица контрольного листа оставлена для отдельного table-aware разбора.
- `01_docs/operations/electricians_knowledge_base/12_installation_request_check.md`: раздел проверки заявки на монтаж, собран из кластера `C005 / installation_request_check`, содержит `20` ссылок на canonical `statement_id` после completion-pass по исходнику.
