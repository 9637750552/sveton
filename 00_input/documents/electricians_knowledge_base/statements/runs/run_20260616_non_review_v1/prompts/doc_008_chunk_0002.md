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
  "chunk_id": "doc_008_chunk_0002",
  "source_document_id": "doc_008",
  "source_file": "Работа на объекте 2024 ред1_7.docx",
  "topic": "Работа на объекте",
  "roles": [
    "монтажник",
    "электрик"
  ],
  "section_path": [
    "Работа на объекте в паре",
    "Стандартный монтаж:"
  ],
  "text": "**Стандартный монтаж:**\n\n<table>\n<colgroup>\n<col style=\"width: 50%\" />\n<col style=\"width: 49%\" />\n</colgroup>\n<thead>\n<tr>\n<th style=\"text-align: center;\"><p><strong>Монтажник электрик 1й-2й разряд</strong></p>\n<p><strong>«Первый номер»</strong></p></th>\n<th style=\"text-align: center;\"><p><strong>Стажёр</strong></p>\n<p><strong>(первые несколько выездов)</strong></p></th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td colspan=\"2\" style=\"text-align: center;\">Разгрузка оборудования и инструмента</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\"><p>Получение доплаты за оборудование.</p>\n<p>Осмотр места монтажа.</p>\n<p>Внесение изменений ( по необходимости), согласование с клиентом.</p></td>\n<td style=\"text-align: center;\">Наблюдает за работой первого номера.</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">Вешает инвертор и байпасный щит.</td>\n<td style=\"text-align: center;\">Собирает стеллаж.</td>\n</tr>\n<tr>\n<td colspan=\"2\" style=\"text-align: center;\"><p>Устанавливают АКБ на стеллаж (150 и200 АЧ всегда вместе)</p>\n<p>100АЧ в первый раз далее по ситуации.</p></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\"><p>Проводит трассу инвертор-щит, но это может сделать стажёр (решается на месте).</p>\n<p>-Выводит начало трассы к основному щиту заказчика.</p>\n<p>- делает проход в щит клиента.</p></td>\n<td style=\"text-align: center;\"><p>Самостоятельно собирает группу АКБ</p>\n<p>Подготавливает провода, а именно:</p>\n<p>- изготавливает провода балансира</p>\n<p>- собирает защиту по постоянному току</p>\n<p>- прокладывает трассу к щиту клиента (при наличии)</p></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\"><p>Изучает щит заказчика для итоговой переборки.</p>\n<p>Предварительно проверяет резервную группу с клиентом.</p>\n<p>По необходимости осуществляется помощь стажеру.</p></td>\n<td style=\"text-align: center;\"><p>!! При этом концы, которые подключаются к инвертору должны быть заизолированы.</p>\n<p>!!\n\nСтажёр ни при каких условиях не подключает основные провода по постоянному току.</p></td>\n</tr>\n<tr>\n<td colspan=\"2\" style=\"text-align: center;\"><p>Вместе со стажёром <strong>первый номер</strong>:</p>\n<p>- Первые несколько раз подключает провода балансира.</p>\n<p>- Проверяет верно ли собрана группа АКБ.</p>\n<p>- Учит самостоятельно проверять верно ли собрана группа АКБ и подключены провода балансира.</p>\n<p>- В дальнейшем только контроль работы стажёра на этом этапе.</p></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">. Подключает группу АКБ к инвертору</td>\n<td style=\"text-align: center;\">Наблюдает за работой первого номера</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">Подключает балансир</td>\n<td style=\"text-align: center;\">Наблюдает за работой первого номера.</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">По необходимости осуществляется помощь второму номеру.</td>\n<td style=\"text-align: center;\">Проводит кабель-трассу</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">Перебирает щит.</td>\n<td style=\"text-align: center;\">наблюдает за работой первого номера.</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\"><p>Настройка инвертора</p>\n<p>Настройка инвертора ,фотографирование результатов и видео запись для отчета.</p></td>\n<td style=\"text-align: center;\">Наблюдает за работой первого номера.</td>\n</tr>\n<tr>\n<td colspan=\"2\" style=\"text-align: center;\"><p>Сдача оборудования клиенту:</p>\n<p>- Имитация отключения электричества.</p>\n<p>- Проверка с клиентом, что всё заявленное им электрооборудование находится в резервной группе.</p>\n<p>- Консультация, как работать с байпасным щитом.</p>\n<p>-Уборка помещения, сбор инструмента и т.д.</p>\n<p>-Приём оплаты и подпись документов.</p>\n<p>-Написание отчета.</p></td>\n</tr>\n</tbody>\n</table>",
  "related_image_ids": [],
  "excluded_image_ids": [],
  "previous_context": "**Работа на объекте в паре**",
  "next_context": "**Если не позволяет место на объекте, то порядок действий может быть изменён на усмотрение первого номера.** ** **",
  "needs_review": false,
  "review_reasons": [],
  "suggested_topic": "work_on_site",
  "suggested_roles": [
    "electrician",
    "installer"
  ]
}

```
