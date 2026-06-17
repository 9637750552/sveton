# Atomic Extraction Run: run_20260616_batch_002

## Назначение

Эта папка содержит очередь чанков для массового извлечения атомарных утверждений.

## Как использовать

1. Для каждого файла `prompts/<chunk_id>.md` получить ответ модели.
2. Сохранить ответ в `raw/<chunk_id>.json`.
3. Запустить collect mode runner-а.

## Важно

- Review/PDF чанки исключены, если run создан без `--include-review`.
- Ответ модели должен быть чистым JSON либо JSON внутри markdown code fence.
- Ответ модели должен содержать `coverage_summary` и `skipped_source_items`.
- Валидатор проверит точные цитаты, image ids, safety flags и связь с чанком.
- Runner создаст `parsed/coverage_warnings.jsonl`, если покрытие чек-листа выглядит неполным.

Всего чанков в очереди: `30`.
