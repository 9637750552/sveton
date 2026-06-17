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
  "chunk_id": "doc_012_chunk_0001",
  "source_document_id": "doc_012",
  "source_file": "ЭЛК_2_1 техн.карты изделий..docx",
  "topic": "Технические карты изделий",
  "roles": [
    "монтажник",
    "электрик",
    "инженер ГО"
  ],
  "section_path": [
    "Изготовление кабеля «Инвертор-щит»"
  ],
  "text": "**Изготовление кабеля «Инвертор-щит»**\n\n<table>\n<colgroup>\n<col style=\"width: 5%\" />\n<col style=\"width: 23%\" />\n<col style=\"width: 44%\" />\n<col style=\"width: 26%\" />\n</colgroup>\n<thead>\n<tr>\n<th style=\"text-align: center;\">№П\\П</th>\n<th style=\"text-align: center;\"><blockquote>\n<p>Этапы обработки</p>\n</blockquote></th>\n<th style=\"text-align: center;\">Графическое изображение</th>\n<th style=\"text-align: center;\">Инструменты</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td style=\"text-align: center;\">1.</td>\n<td>Отрезать кусок кабеля 5Х4, длинной 2 метра:</td>\n<td style=\"text-align: center;\">[IMAGE:img_0004|media/image1.png|exclude_candidate|Small icon or fragment]</td>\n<td style=\"text-align: center;\"><p>[IMAGE:img_0005|media/image2.jpeg|candidate_for_linking|Бокорез]</p>\n<p>Бокорез</p></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">2.</td>\n<td><p>Зачистить концы кабеля:</p>\n<blockquote>\n<p>-с одной стороны 100мм.</p>\n<p>-с другой стороны 200мм.</p>\n</blockquote></td>\n<td style=\"text-align: center;\">[IMAGE:img_0006|media/image3.png|candidate_for_linking|Нож для разделки кабеля][IMAGE:img_0007|media/image4.png|candidate_for_linking|Нож для разделки кабеля]</td>\n<td style=\"text-align: center;\"><p>[IMAGE:img_0008|media/image5.png|candidate_for_linking|Нож для разделки кабеля]</p>\n<p>Нож для разделки кабеля</p></td>\n</tr>\n<tr>\n<td colspan=\"4\" style=\"text-align: center;\"><p>2.1.Чтобы разделать конец кабеля:</p>\n<blockquote>\n<p>1)Нужно надеть нож на кабель согласно размеру отреза указанному в п.2., провернуть несколько оборотов вокруг кабеля, чтобы прорезать внешнюю изоляцию.</p>\n</blockquote>\n<p>2)Затем, не снимая нож с кабеля, потянуть его в сторону края кабеля, прорезая тем самым изоляцию вдоль кабеля.(Важно!\n\nПеред разделкой необходимо отрегулировать вылет лезвия, чтобы не повредить изоляцию жил.)</p>\n<p>1)[IMAGE:img_0009|media/image6.png|candidate_for_linking|Зачистить концы жил:] 2) [IMAGE:img_0010|media/image7.png|candidate_for_linking|Зачистить концы жил:]</p></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">3.</td>\n<td style=\"text-align: left;\"><blockquote>\n<p>Зачистить концы жил:</p>\n</blockquote></td>\n<td style=\"text-align: center;\">[IMAGE:img_0011|media/image8.png|candidate_for_linking|Стрипер][IMAGE:img_0012|media/image9.png|candidate_for_linking|Стрипер]</td>\n<td style=\"text-align: center;\"><p>[IMAGE:img_0013|media/image10.png|candidate_for_linking|Стрипер]</p>\n<p>Стрипер</p></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">4.</td>\n<td>Надеть и <strong>опресовать</strong> наконечники сечением <strong>4мм</strong> на все зачищенные концы жил кабеля с обоих концов:.</td>\n<td style=\"text-align: center;\">[IMAGE:img_0014|media/image11.jpeg|candidate_for_linking|Пресс-клещи][IMAGE:img_0015|media/image12.png|candidate_for_linking|Пресс-клещи][IMAGE:img_0016|media/image13.png|candidate_for_linking|Пресс-клещи]</td>\n<td style=\"text-align: center;\"><p>[IMAGE:img_0017|media/image14.jpeg|candidate_for_linking|Пресс-клещи]</p>\n<p>Пресс-клещи</p></td>\n</tr>\n<tr>\n<td colspan=\"4\" style=\"text-align: center;\"><p>4.1.\n\nПравильная опресовка наконечника: 1- из под «юбки» наконечника не торчит оголенная жила или её часть; 2- длинна зачищенного участка жилы соответствует длине втулки наконечника.</p>\n<p>[IMAGE:img_0018|media/image15.jpeg|candidate_for_linking|Отрезать кусок гофротрубы ф25 длинной 1,7 м .надеть на подготовленный кабель][IMAGE:img_0018|media/image15.jpeg|candidate_for_linking|Отрезать кусок гофротрубы ф25 длинной 1,7 м .надеть на подготовленный кабель]</p></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">5.</td>\n<td>Отрезать кусок гофротрубы ф25 длинной <strong>1,7 м</strong>.надеть на подготовленный кабель</td>\n<td style=\"text-align: center;\">[IMAGE:img_0019|media/image16.png|candidate_for_linking|Наклеить на край гофротрубы (там, где длина жил кабеля 100 мм .) наклейку с маркировкой кабеля.]</td>\n<td style=\"text-align: center;\">[IMAGE:img_0020|media/image17.jpeg|candidate_for_linking|Наклеить на край гофротрубы (там, где длина жил кабеля 100 мм .) наклейку с маркировкой кабеля.]</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">6.</td>\n<td>Наклеить на край гофротрубы (там, где длина жил кабеля <strong>100 мм</strong>.) наклейку с маркировкой кабеля.</td>\n<td style=\"text-align: center;\">[IMAGE:img_0021|media/image18.png|candidate_for_linking|Изготовление перемычек для АКБ]</td>\n<td style=\"text-align: center;\"></td>\n</tr>\n</tbody>\n</table>",
  "related_image_ids": [
    "img_0005",
    "img_0006",
    "img_0007",
    "img_0008",
    "img_0009",
    "img_0010",
    "img_0011",
    "img_0012",
    "img_0013",
    "img_0014",
    "img_0015",
    "img_0016",
    "img_0017",
    "img_0018",
    "img_0019",
    "img_0020",
    "img_0021"
  ],
  "excluded_image_ids": [
    "img_0004"
  ],
  "previous_context": "",
  "next_context": "**Изготовление перемычек для АКБ** Виды используемых перемычек: - перемычка АКБ 0,1 м. ф25 черная. - перемычка АКБ 0,1 м ф35 красная. - перемычка АКБ 0,3 м. ф25 черная. - перемычка АКБ 0,7 м. ф25 черная. - перемычка АКБ 0,7 м. ф25 красная. - перемычка АКБ 1,4 м. ф35 красная Н/Н. - перемычка АКБ 1,4 м. ф35 черная Н/Ш. и другие … [IMAGE:img_0022|medi",
  "needs_review": false,
  "review_reasons": [],
  "suggested_topic": "ups_components",
  "suggested_roles": [
    "electrician",
    "hq_engineer",
    "installer"
  ]
}

```
