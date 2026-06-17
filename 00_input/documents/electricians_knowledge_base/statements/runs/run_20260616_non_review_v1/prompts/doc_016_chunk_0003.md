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
6. Если точную цитату подобрать нельзя, не извлекай утверждение.
7. Не исправляй смысл источника. Можно нормализовать формулировку `statement`, но нельзя менять условие, объект или обязательность.
8. Не создавай утверждение только по изображению. Изображение можно указать в `related_image_ids` только если текст чанка сам подтверждает утверждение.
9. Используй только `image_id` из входного поля `related_image_ids`. Никогда не используй `excluded_image_ids`.
10. Если утверждение связано с электробезопасностью, риском повреждения оборудования, пожаром, УЗО, DC/AC подключениями, фазой/нулем, входом/выходом инвертора или отключением питания, выставь `risk_level = "safety_critical"` и `review_status = "review_required"`.
11. Если входной чанк имеет `needs_review = true`, все извлеченные из него утверждения должны иметь `review_status = "review_required"`.
12. Если полезных атомарных утверждений нет, верни пустой список `statements`.

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


## Source Chunk Input

```json

{
  "chunk_id": "doc_016_chunk_0003",
  "source_document_id": "doc_016",
  "source_file": "ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1.docx",
  "topic": "Элементы распределительных щитов",
  "roles": [
    "монтажник",
    "электрик"
  ],
  "section_path": [
    "Электрический щит клиента и его компоненты",
    "Необходимо разобраться в схеме электрощита и понять его схему следующим образом:",
    "Подключение заземляющих проводников."
  ],
  "text": "**Подключение заземляющих проводников.**\n\nЗаземляющий проводник (PE) от заземляющего контура дома идет к шине заземления в щитке. Далее провод присоединяется к шине заземления в щитке. От нее отходят PE-кабели к розеткам, в которых они подключаются к своим клеммам. Таким образом обеспечивается возможность заземления электроприборов.",
  "related_image_ids": [],
  "excluded_image_ids": [],
  "previous_context": " к общей шине заземления, которая соединена с контуром заземления дома. При необходимости на первых самостоятельных монтажах, пока проходит обучение, лучше схему зарисовать на бумаге в любом удобном виде. Проще всего в однолинейной схеме если щит 3х фазный. [IMAGE:img_0087|media/image2.png|candidate_for_linking|Подключение заземляющих проводников.]",
  "next_context": "**Нейтральные и заземляющие шины.** [IMAGE:img_0088|media/image3.jpeg|candidate_for_linking|Подключение заземляющих проводников.] [IMAGE:img_0089|media/image4.png|exclude_candidate|Small icon or fragment] [IMAGE:img_0090|media/image5.png|exclude_candidate|Small icon or fragment] К нейтральным (N) и заземляющим (PE) шинам (цвет проводов и шин заземл",
  "needs_review": false,
  "review_reasons": [],
  "suggested_topic": "distribution_boards",
  "suggested_roles": [
    "electrician",
    "installer"
  ]
}

```
