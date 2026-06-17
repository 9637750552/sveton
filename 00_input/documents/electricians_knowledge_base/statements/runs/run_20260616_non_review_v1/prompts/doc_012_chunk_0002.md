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
  "chunk_id": "doc_012_chunk_0002",
  "source_document_id": "doc_012",
  "source_file": "ЭЛК_2_1 техн.карты изделий..docx",
  "topic": "Технические карты изделий",
  "roles": [
    "монтажник",
    "электрик",
    "инженер ГО"
  ],
  "section_path": [
    "Изготовление кабеля «Инвертор-щит»",
    "Изготовление перемычек для АКБ"
  ],
  "text": "**Изготовление перемычек для АКБ**\n\nВиды используемых перемычек:\n\n<table>\n<colgroup>\n<col style=\"width: 100%\" />\n</colgroup>\n<thead>\n<tr>\n<th><p>- перемычка АКБ 0,1 м. ф25 черная.</p>\n<p>- перемычка АКБ 0,1 м ф35 красная.</p>\n<p>- перемычка АКБ 0,3 м. ф25 черная.</p>\n<p>- перемычка АКБ 0,7 м. ф25 черная.</p>\n<p>- перемычка АКБ 0,7 м. ф25 красная.</p>\n<p>- перемычка АКБ 1,4 м. ф35 красная Н/Н.</p>\n<p>- перемычка АКБ 1,4 м. ф35 черная Н/Ш.</p>\n<p><em>и другие</em>…</p>\n<p>[IMAGE:img_0022|media/image19.png|candidate_for_linking|перемычка АКБ 1,4 м. ф35 красная Н/Н.]</p></th>\n</tr>\n</thead>\n<tbody>\n</tbody>\n</table>\n\n<table style=\"width:100%;\">\n<colgroup>\n<col style=\"width: 5%\" />\n<col style=\"width: 21%\" />\n<col style=\"width: 48%\" />\n<col style=\"width: 25%\" />\n</colgroup>\n<thead>\n<tr>\n<th style=\"text-align: center;\">№П\\П</th>\n<th style=\"text-align: center;\"><blockquote>\n<p>Этапы обработки</p>\n</blockquote></th>\n<th style=\"text-align: center;\">Графическое изображение</th>\n<th style=\"text-align: center;\">Инструменты</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td style=\"text-align: center;\">1.</td>\n<td style=\"text-align: center;\">-Нарезать куски кабеля, необходимого по заданию длинны и количества:</td>\n<td style=\"text-align: center;\">[IMAGE:img_0023|media/image20.png|candidate_for_linking|Зачистить концы кабеля от изоляции необходимой длинны, не больше длинны втулки наконечника]</td>\n<td style=\"text-align: center;\">[IMAGE:img_0005|media/image2.jpeg|candidate_for_linking|Бокорез]</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">2.</td>\n<td style=\"text-align: center;\">-Зачистить концы кабеля от изоляции необходимой длинны, не больше длинны втулки наконечника</td>\n<td style=\"text-align: center;\">[IMAGE:img_0024|media/image21.png|candidate_for_linking|Нарезать куски кабеля, необходимого по заданию длинны и количества:]</td>\n<td style=\"text-align: center;\">[IMAGE:img_0008|media/image5.png|candidate_for_linking|Нож для разделки кабеля]</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\"></td>\n<td style=\"text-align: center;\"></td>\n<td style=\"text-align: center;\"></td>\n<td style=\"text-align: center;\"></td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">3.</td>\n<td style=\"text-align: center;\"><p>-Надеть наконечник на зачищенные жилы.</p>\n<p>-Установить матрицы согласно диаметру втулки наконечника:</p>\n<p>ф25-&gt; 25/16</p>\n<p>ф35-&gt;35/25</p>\n<p>-Опресовать наконечник.</p></td>\n<td style=\"text-align: center;\">[IMAGE:img_0025|media/image22.png|candidate_for_linking|ф25- 25/16]</td>\n<td style=\"text-align: center;\">[IMAGE:img_0026|media/image23.png|candidate_for_linking|ф25- 25/16]</td>\n</tr>\n<tr>\n<td style=\"text-align: center;\">4.</td>\n<td style=\"text-align: center;\">-Отрезать ножницами кусок термоусадки длинной 60мм, надеть на опресованный наконечник и строительным феном равномерно прогреть отрезок термоусадки до полного обволакивания втулки наконечника</td>\n<td style=\"text-align: center;\">[IMAGE:img_0027|media/image24.png|candidate_for_linking|ф35-35/25]</td>\n<td style=\"text-align: center;\">[IMAGE:img_0028|media/image25.png|candidate_for_linking|ф35-35/25]</td>\n</tr>\n</tbody>\n</table>\n\n**  **\n\n[IMAGE:img_0029|media/image26.png|candidate_for_linking|Назначение матриц пресс-клещей (CTF) из набора инструмента монтажника.]",
  "related_image_ids": [
    "img_0022",
    "img_0023",
    "img_0005",
    "img_0024",
    "img_0008",
    "img_0025",
    "img_0026",
    "img_0027",
    "img_0028",
    "img_0029"
  ],
  "excluded_image_ids": [],
  "previous_context": " кабеля.] [IMAGE:img_0020|media/image17.jpeg|candidate_for_linking|Наклеить на край гофротрубы (там, где длина жил кабеля 100 мм .) наклейку с маркировкой кабеля.] 6. Наклеить на край гофротрубы (там, где длина жил кабеля 100 мм .) наклейку с маркировкой кабеля. [IMAGE:img_0021|media/image18.png|candidate_for_linking|Изготовление перемычек для АКБ]",
  "next_context": "**Назначение матриц пресс-клещей (CTF) из набора инструмента монтажника.** [IMAGE:img_0030|media/image27.png|candidate_for_linking|Назначение матриц пресс-клещей (CTF) из набора инструмента монтажника.]",
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
