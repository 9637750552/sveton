# Runner массового извлечения атомарных утверждений

Дата: 2026-06-16

## Назначение

Runner готовит и собирает массовый прогон извлечения атомарных утверждений по `source_chunks.jsonl`.

Скрипт:

- формирует очередь чанков;
- создает prompt-пакеты для модели;
- исключает review/PDF чанки по умолчанию;
- принимает raw-ответы модели;
- парсит JSON;
- валидирует `coverage_summary` и `skipped_source_items` на уровне чанка;
- валидирует каждое утверждение;
- создает warnings по вероятно неполному покрытию bullet/checklist-пунктов;
- сохраняет валидные утверждения и ошибки отдельно.

Скрипт: `06_scripts/run_atomic_extraction.py`.

## Подготовленный run

Основной run:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_non_review_v1/
```

Параметры:

- чанков в очереди: `141`;
- review-чанки: исключены;
- чанки с изображениями: `29`;
- `suggested_topic`: заполнен для всех чанков;
- `suggested_roles`: заполнен для всех чанков;
- unknown topics: `0`.

## Структура run-папки

```text
run_.../
  manifest.json
  README.md
  atomic_extraction_prompt.md
  queue.jsonl
  inputs/
  prompts/
  raw/
  parsed/
```

Где:

- `inputs/<chunk_id>.json`: чистый JSON чанка для модели;
- `prompts/<chunk_id>.md`: prompt + input в одном файле;
- `raw/<chunk_id>.json`: сюда кладется сырой ответ модели;
- `parsed/atomic_statements.jsonl`: валидные утверждения после collect;
- `parsed/extraction_errors.jsonl`: ошибки парсинга и валидации.
- `parsed/coverage_warnings.jsonl`: предупреждения о вероятно неполном покрытии источника.

## Команды

Подготовить очередь без review-чанков:

```bash
python3 06_scripts/run_atomic_extraction.py prepare /home/sergey/Sveton --run-id run_20260616_non_review_v1
```

Собрать raw-ответы после модели:

```bash
python3 06_scripts/run_atomic_extraction.py collect /home/sergey/Sveton 00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_non_review_v1 --fail-on-errors --fail-on-warnings
```

Собрать и продвинуть результат в canonical files:

```bash
python3 06_scripts/run_atomic_extraction.py collect /home/sergey/Sveton 00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_non_review_v1 --promote --fail-on-errors --fail-on-warnings
```

## Smoke-test

Создан тестовый run:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_collect_smoke/
```

Результат:

- чанков: `2`;
- raw-ответов: `2`;
- валидных утверждений: `7`;
- ошибок: `0`.

## Batch 001

Первый малый реальный batch:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_batch_001/
```

Результат:

- чанков: `10`;
- raw-ответов: `10`;
- валидных утверждений: `33`;
- ошибок: `0`;
- promoted в общий `atomic_statements.jsonl`: нет.

Ревью:

- пользователь подтвердил валидность 33 утверждений;
- выборочный аудит полноты выявил пропуски в длинном чек-листе и справочном блоке АКБ;
- старый prompt нельзя масштабировать без контроля полноты.

Подробности: `batch_001_summary.md`, `review/batch_001_completeness_audit.md`.

## Batch 001 v2 без рекрутингового файла

Повторный batch после доработки контроля полноты:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_batch_001_v2_no_hiring/
```

Из выборки исключен `Ищем_электриков_для_сотрудничества.docx`, потому что это рекрутинговый текст, а не технический учебный/операционный материал.

Результат:

- чанков: `6`;
- валидных утверждений: `31`;
- ошибок: `0`;
- coverage warnings: `0`;
- promoted в общий `atomic_statements.jsonl`: нет.

Подробности: `batch_001_v2_no_hiring_summary.md`, `review/batch_001_v2_no_hiring_review.md`.

## Batch 002

Первый широкий технический batch после проверки batch 001 v2:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_batch_002/
```

Из batch исключен `Ищем_электриков_для_сотрудничества.docx`.

Результат:

- чанков: `30`;
- валидных утверждений: `129`;
- ошибок: `0`;
- coverage warnings: `0`;
- promoted в общий `atomic_statements.jsonl`: нет.

Смысловой аудит batch 002 провален: заголовки превращены в утверждения, есть шаблонные формулировки, длинные пункты не всегда атомарны, HTML-таблицы обработаны шумно. Batch 002 считается диагностическим и не должен продвигаться в canonical.

Подробности: `batch_002_summary.md`, `review/batch_002_review.md`, `review/batch_002_quality_audit.md`.

## Extraction pipeline v3

После ручного просмотра batch 002 добавлена версия v3.

Что изменено:

- prompt запрещает извлекать заголовки, подписи разделов и служебные метки как утверждения;
- `skipped_source_items` теперь требует `source_item_type`, чтобы отличать заголовок, строку таблицы, требование, инструкцию, примечание и контекстный элемент;
- добавлены причины пропуска `heading`, `table_header`, `context_only`;
- prompt требует table-aware extraction: таблицы обрабатываются по строкам и смысловым связям, а не по отдельным ячейкам;
- runner создает quality warnings для заголовков, шаблонных формулировок, HTML/table fragments, табличных значений без контекста, явных дублей и слишком длинных неатомарных утверждений;
- detector source items дополнительно учитывает короткие строки-поля, например `Напряжение внешней сети -`.

При `--fail-on-warnings` эти quality warnings блокируют collect так же, как coverage warnings.

## Paragraph coverage gate

После extraction по `ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx` добавлен более строгий coverage gate для обычных абзацев.

Причина:

- старый gate хорошо ловил неполное покрытие bullet/checklist-пунктов;
- но содержательные предложения в обычных абзацах могли не попасть в extraction, если модель формально указала достаточный `source_items_detected`;
- это критично для будущего эпика по интервью с руководством, где основная структура источника будет состоять из абзацев, а не bullets.

Что изменено в `06_scripts/run_atomic_extraction.py`:

- runner теперь строит candidate source items не только из bullets, но и из содержательных предложений обычного текста;
- candidate-предложения выбираются кодом по признакам: технические термины, действия, условия, числовые значения, параметры, примеры;
- collect проверяет не только количество покрытых source items, но и покрытие конкретных candidate source items через `source_quote` или `skipped_source_items`;
- если candidate item не покрыт, создается warning `candidate_source_items_uncovered`;
- контекстные, переходные и вводные предложения теперь должны быть явно объяснены в `skipped_source_items`, если они похожи на source item, но не должны становиться утверждением.

Регрессионная проверка:

- `run_20260617_doc015_batch_a_v1`: `19` statements, `0` errors, `0` warnings;
- `run_20260617_doc015_batch_b_v1`: `37` statements, `0` errors, `0` warnings;
- `run_20260617_doc015_batch_c_v1`: `45` statements, `0` errors, `0` warnings.

Важно:

- старые run-папки с raw-ответами, созданными до paragraph gate, могут давать новые coverage warnings при повторном collect;
- для новых extraction-run нужно пересоздавать prompt-пакеты через `prepare`, чтобы в них попала обновленная инструкция про обычные абзацы;
- для интервью потребуется отдельный профиль эвристик, потому что business/source claims отличаются от технических source items.

## Batch 002 v3

Повторный широкий batch после внедрения v3:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260616_batch_002_v3/
```

Состав чанков идентичен diagnostic batch 002, рекрутинговый файл исключен.

Результат:

- чанков: `30`;
- валидных утверждений: `132`;
- ошибок: `0`;
- coverage / quality warnings: `0`;
- promoted в общий `atomic_statements.jsonl`: да, после пользовательского подтверждения.

Batch 002 v3 прошел Codex-ревью и был продвинут в canonical после пользовательского подтверждения.

Подробности: `batch_002_v3_summary.md`, `review/batch_002_v3_review.md`, `review/batch_002_v3_codex_audit.md`.

## Контроль полноты

После аудита batch 001 runner и prompt переведены на расширенный формат raw-ответа:

- `coverage_summary`: сколько самостоятельных source items модель нашла, извлекла и пропустила;
- `skipped_source_items`: точные цитаты пропущенных source items и причины пропуска;
- `coverage_warnings.jsonl`: автоматические предупреждения, если явных bullet/checklist-пунктов больше, чем извлеченных или объясненно пропущенных source items, а также quality warnings v3.

Если включен `--fail-on-warnings`, collect завершается с ошибкой при обнаружении coverage warnings.

## Source coverage gate

После выявленного недопокрытия документа проверки заявки добавлен отдельный gate прямого покрытия исходника:

```bash
python3 06_scripts/check_source_coverage.py /home/sergey/Sveton \
  --source-file 'Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx' \
  --fail-on-uncovered
```

Что проверяет gate:

- берет `source_chunks.jsonl`;
- берет canonical `atomic_statements.jsonl`;
- для каждого чанка выбранного документа проверяет, есть ли canonical-утверждения;
- заголовочные и контекстные чанки помечает как `ignored`;
- содержательные чанки без утверждений помечает как `uncovered_content`;
- при `--fail-on-uncovered` завершает проверку с ошибкой, если есть содержательные непокрытые чанки.

Текущие отчеты:

- общий отчет по пяти редакционным источникам: `source_coverage_report.md`;
- машинный JSONL общего отчета: `source_coverage_report.jsonl`;
- отдельный отчет по документу проверки заявки: `source_coverage_doc007.md`.
- объясненные исключения split/duplicate-фрагментов: `source_coverage_overrides.jsonl`.

Текущий результат:

- документ проверки заявки после completion-pass проходит gate без `uncovered_content`;
- общий gate по пяти редакционным источникам проходит после добавления `1` недостающего утверждения и `5` coverage overrides для split/duplicate-фрагментов.

Важно: уже подготовленные run-папки содержат копию prompt-а на момент создания run. После изменения prompt/schema старые prompt-пакеты нельзя использовать для нового извлечения. Для повторного batch 001 и следующих batch нужно создать новые run-папки командой `prepare`.

## Ограничения

- Runner не вызывает API сам. Он готовит задания и собирает ответы.
- Старые raw-ответы без `coverage_summary` и `skipped_source_items` не соответствуют новой схеме.
- Raw-ответы старых run без `source_item_type` в `skipped_source_items` не соответствуют схеме v3.
- Старые prompt-пакеты из уже созданных run-папок соответствуют прежней схеме и должны быть пересозданы.
- PDF/review чанки не входят в основной run.
- Для review-чанков нужен отдельный run с явным `--include-review` после решения по качеству PDF и safety review.
- Следующий шаг: выбрать следующий batch документов для extraction v3 или перейти к дедупликации canonical-утверждений.
