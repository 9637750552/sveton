# Prompt: извлечение атомарных утверждений из одного чанка

## Назначение

Промпт используется для извлечения атомарных утверждений из одного `source_chunk` базы знаний электриков.

Модель не управляет пайплайном. Она получает один JSON-объект чанка и возвращает JSON-объект результата. Все границы источника, идентификаторы, изображения и review-флаги задаются кодом.

## System / Developer Instruction

Ты извлекаешь атомарные утверждения из одного фрагмента исходного документа.

Критические правила:

1. Извлекай только то, что явно написано в поле `text`.
2. `previous_context` и `next_context` можно использовать только для понимания локального контекста, но `source_quote` должен быть точной цитатой из `text`, а не из соседнего контекста.
3. Не добавляй технические выводы, которых нет в тексте.
4. Не объединяй несколько разных требований в одно утверждение.
5. Если мысль состоит из списка действий, каждое самостоятельное действие извлекай отдельным утверждением.
6. В списках, чек-листах и этапах не выбирай только "самые важные" пункты: каждый самостоятельный bullet/пункт должен быть либо извлечен отдельным утверждением, либо явно указан в `skipped_source_items` с причиной пропуска.
7. Справочные параметры оборудования, числовые значения, номиналы и диапазоны извлекай как отдельные утверждения, если они явно полезны для базы знаний.
8. Если точную цитату подобрать нельзя, не извлекай утверждение.
9. Не исправляй смысл источника. Можно нормализовать формулировку `statement`, но нельзя менять условие, объект или обязательность.
10. Не создавай утверждение только по изображению. Изображение можно указать в `related_image_ids` только если текст чанка сам подтверждает утверждение.
11. Используй только `image_id` из входного поля `related_image_ids`. Никогда не используй `excluded_image_ids`.
12. Если утверждение связано с электробезопасностью, риском повреждения оборудования, пожаром, УЗО, DC/AC подключениями, фазой/нулем, входом/выходом инвертора или отключением питания, выставь `risk_level = "safety_critical"` и `review_status = "review_required"`.
13. Если входной чанк имеет `needs_review = true`, все извлеченные из него утверждения должны иметь `review_status = "review_required"`.
14. Если полезных атомарных утверждений нет, верни пустой список `statements`, но все равно заполни `coverage_summary` и `skipped_source_items`.

## Input

На вход приходит один JSON-объект `source_chunk` со следующими важными полями:

- `chunk_id`
- `source_document_id`
- `source_file`
- `topic`
- `roles`
- `section_path`
- `text`
- `related_image_ids`
- `excluded_image_ids`
- `previous_context`
- `next_context`
- `needs_review`
- `review_reasons`
- `suggested_topic`
- `suggested_roles`

Поля `topic` и `roles` могут быть исходными русскоязычными метаданными документа. Для вывода используй нормализованные поля `suggested_topic` и `suggested_roles`, если они заданы.

## Output

Верни только валидный JSON без Markdown:

```json
{
  "source_chunk_id": "doc_000_chunk_0000",
  "coverage_summary": {
    "source_items_detected": 1,
    "source_items_extracted": 1,
    "source_items_skipped": 0,
    "coverage_notes": "Все явные самостоятельные пункты чанка извлечены."
  },
  "skipped_source_items": [],
  "statements": [
    {
      "statement_id": "doc_000_chunk_0000_stmt_001",
      "statement": "Короткая нормализованная формулировка одного утверждения.",
      "statement_type": "requirement",
      "roles": ["installer"],
      "topic": "photo_report",
      "source_document_id": "doc_000",
      "source_file": "example.docx",
      "source_chunk_id": "doc_000_chunk_0000",
      "section_path": ["Раздел"],
      "source_quote": "Точная цитата из поля text.",
      "source_quote_is_exact": true,
      "related_image_ids": [],
      "visual_review_required": false,
      "risk_level": "ordinary",
      "confidence": "high",
      "review_status": "extracted",
      "scope": "",
      "condition": "",
      "action": "",
      "object": "",
      "normalized_terms": [],
      "extraction_notes": ""
    }
  ]
}
```

## Coverage Rules

`coverage_summary` и `skipped_source_items` обязательны для каждого чанка.

Правила покрытия:

- `source_items_detected`: сколько явных самостоятельных смысловых единиц ты увидел в `text`. Считай самостоятельными единицами отдельные bullet-пункты, этапы, требования, определения, запреты, предупреждения, параметры оборудования и числовые справочные значения.
- `source_items_extracted`: сколько самостоятельных единиц превращено в утверждения. Обычно это равно количеству объектов в `statements`.
- `source_items_skipped`: сколько самостоятельных единиц не извлечено и перечислено в `skipped_source_items`.
- `coverage_notes`: коротко объясни покрытие, особенно если что-то пропущено.

Каждый элемент `skipped_source_items` должен иметь вид:

```json
{
  "source_item_quote": "Точная цитата пропущенного пункта из поля text.",
  "reason": "duplicate",
  "notes": "Почему пункт не был превращен в отдельное утверждение."
}
```

Допустимые `reason`:

- `duplicate`: пункт полностью дублирует уже извлеченное утверждение;
- `not_atomic`: пункт нельзя корректно сделать атомарным без соседнего контекста;
- `not_actionable`: пункт не несет полезного знания для базы;
- `image_only`: пункт является только маркером изображения без текстовой опоры;
- `no_exact_quote`: невозможно дать точную цитату из `text`;
- `unclear`: смысл пункта неясен и требует ручной проверки;
- `out_of_scope`: пункт явно не относится к базе знаний электриков.

Не используй `skipped_source_items`, чтобы скрывать полезные пункты. Если пункт можно извлечь с точной цитатой, извлекай его.

## Statement Types

Используй только эти значения:

- `definition`: определение термина или объекта.
- `requirement`: обязательное требование без пошаговости.
- `instruction_step`: конкретное действие в процессе.
- `checklist_item`: пункт проверки или чек-листа.
- `recommendation`: рекомендация или желательное действие.
- `prohibition`: запрет.
- `warning`: предупреждение о риске.
- `process_step`: этап процесса.
- `qualification_criterion`: требование к квалификации.
- `interview_signal`: признак для отбора или интервью.
- `reporting_requirement`: требование к отчетности.

## Roles

В поле `roles` используй только эти значения:

- `installer`
- `electrician`
- `manager`
- `hq_engineer`
- `project_lead`
- `leader`
- `customer`

Если во входе есть `suggested_roles`, используй их как основную подсказку.

## Topics

В поле `topic` используй только эти значения:

- `basic_knowledge`
- `ups_components`
- `distribution_boards`
- `installation_process`
- `work_on_site`
- `service_visit`
- `photo_report`
- `installer_roles`
- `training_levels`
- `hiring_and_interview`
- `installation_request_check`
- `quality_control`
- `reporting`
- `safety`
- `unknown`

Если во входе есть `suggested_topic`, используй его как основную подсказку.

## Risk Levels

- `ordinary`: обычное организационное или справочное знание.
- `important`: важно для качества работы, но не является прямым safety-critical риском.
- `safety_critical`: электробезопасность, риск повреждения оборудования, риск пожара, неправильное подключение, УЗО, фаза/ноль, DC/AC, вход/выход инвертора, отключение питания.

## Image Rules

Если в `text` есть маркер `[IMAGE:img_XXXX|...]`, это не источник нового утверждения.

Можно добавить `img_XXXX` в `related_image_ids`, только если:

- `img_XXXX` есть во входном поле `related_image_ids`;
- утверждение подтверждается текстовой цитатой из `text`;
- картинка находится в том же смысловом блоке или прямо иллюстрирует цитируемый текст.

Если утверждение нельзя подтвердить без визуального анализа картинки, не извлекай его либо выставь `visual_review_required = true` и `review_status = "review_required"` только при наличии текстовой опоры.

## Quality Gate

Перед ответом проверь:

- каждое `statement` содержит только одну мысль;
- каждое `source_quote` является точной подстрокой `text`;
- все `related_image_ids` существуют во входном `related_image_ids`;
- нет утверждений из `previous_context` или `next_context`;
- нет утверждений, основанных только на изображении;
- safety-related утверждения отправлены на ревью.
- каждый самостоятельный bullet/checklist-пункт либо извлечен, либо указан в `skipped_source_items`;
- `source_items_extracted` равно количеству объектов в `statements`;
- `source_items_skipped` равно количеству объектов в `skipped_source_items`.


## Source Chunk Input

```json

{
  "chunk_id": "doc_013_chunk_0004",
  "source_document_id": "doc_013",
  "source_file": "ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5.docx",
  "topic": "Состав ИБП",
  "roles": [
    "монтажник",
    "электрик"
  ],
  "section_path": [
    "ЭЛК-Базовые знания",
    "Состав ИБП:",
    "- Инвертор"
  ],
  "text": "**- Инвертор**\n\nЭто преобразователь.\n\nПреобразует постоянный ток (DC) аккумуляторов в переменный (AC) для питания стандартных электропотребителей.\n\nВсе инверторы, используемые в наших системах, имеют зарядные устройства, то есть при необходимости подзаряжают аккумуляторы.",
  "related_image_ids": [],
  "excluded_image_ids": [],
  "previous_context": "**Основные элементы, входящие в состав источника бесперебойного питания (ИБП)**",
  "next_context": "**- Аккумуляторы (АКБ)** Обеспечивают запас энергии. Более подробное описание АКБ будет далее.",
  "needs_review": false,
  "review_reasons": [],
  "suggested_topic": "ups_components",
  "suggested_roles": [
    "electrician",
    "installer"
  ]
}

```
