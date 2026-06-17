# Review: doc_015 semantic extraction

Дата: 2026-06-17

Источник: `ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx`

Run-папки:

- `run_20260617_doc015_batch_a_v1`
- `run_20260617_doc015_batch_b_v1`
- `run_20260617_doc015_batch_c_v1`

## Итог

- Обработано содержательных чанков: `16`.
- Пропущены как заголовочные: `doc_015_chunk_0001`, `doc_015_chunk_0002`, `doc_015_chunk_0003`, `doc_015_chunk_0010`.
- Валидных утверждений: `101`.
- Errors: `0`.
- Coverage / quality warnings: `0`.
- Promotion в canonical: выполнен после review.

## Распределение

- Batch A: `19` утверждений.
- Batch B: `37` утверждений.
- Batch C: `45` утверждений.

По типам:

- `definition`: `24`
- `requirement`: `21`
- `instruction_step`: `18`
- `checklist_item`: `16`
- `process_step`: `13`
- `recommendation`: `6`
- `prohibition`: `3`

По риску:

- `safety_critical`: `77`
- `ordinary`: `24`

По review status:

- `review_required`: `77`
- `extracted`: `24`

## Проверки

- Все `safety_critical` утверждения имеют `review_status = review_required`.
- Нет `review_required` утверждений с не-safety risk.
- Нет длинных statement/source_quote, попадающих под quality warning.
- Нет нормализованных дублей внутри трех batch.
- Все `related_image_ids` входят в разрешенные `related_image_ids` соответствующего chunk.
- `excluded_image_ids` не использованы в утверждениях.
- Чистые image-маркеры не используются как самостоятельные `skipped_source_items`.

## Ручные правки после первого collect

- Batch B: убраны image-only записи из `skipped_source_items`, потому что валидатор запрещает чистые image markers как skipped source item.
- Batch C: заменены недопустимые `statement_type = example` на допустимые типы схемы.
- Review-pass добавил недостающие утверждения по:
  - удобству установки инвертора и расположению ЖК-дисплея;
  - причине требования по вентиляционным отверстиям и отступу 20 см;
  - пониманию принципа работы ИБП и байпаса перед схемой байпасного щита;
  - примерам расчета зарядного тока `20А` и `10А + 10А`;
  - включению автоматического двухполюсного выключателя в байпасном щите.

## Вывод

Extraction по `doc_015` продвинут в canonical.

Canonical после promotion:

- `387` валидных атомарных утверждений;
- `101` утверждение из `doc_015`;
- canonical validation: passed;
- source coverage по `doc_015`: `16` covered chunks, `4` ignored heading/context chunks, `0` uncovered.
- clustering: выполнен, добавлен `C009 / installation_process`;
- editorial layer: собран draft-раздел `04_installation_process.md`.

Ограничение: example-like утверждения сохранены как `definition` или `instruction_step`, потому что текущая схема не имеет отдельного `example` statement type.
