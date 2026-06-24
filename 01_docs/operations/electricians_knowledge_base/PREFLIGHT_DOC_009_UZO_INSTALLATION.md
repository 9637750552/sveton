# Preflight doc_009: UZO installation semantic extraction

Дата: 2026-06-22

Источник: `doc_009 / Установка УЗО при монтаже.docx`

Статус: preflight only. Canonical artifacts не изменялись.

Запрещенные для этого preflight файлы не записывались:

- `atomic_statements.jsonl`
- `statement_clusters.json`
- `statement_relations.jsonl`
- `statement_images.jsonl`
- `source_coverage_report.jsonl`
- `source_coverage_report.md`
- `coverage_warnings.jsonl`
- `extraction_errors.jsonl`

## 1. Контекст правил

Документ `doc_009` в inventory помечен как `raw, extracted, chunked, review_required` и как safety-related материал, который нужно отправить на ручное ревью до semantic extraction.

По текущей методологии:

- будущие facts должны извлекаться только как source-backed atomic statements;
- технические требования по УЗО, щиту, резервной группе, подключению и размещению должны получать `risk_level=safety_critical` и `review_status=review_required`;
- такие statements должны быть `blocked_for_instruction` в downstream layer до экспертного технического review;
- existing canonical слой нельзя переписывать во время параллельных doc_010/doc_008 работ.

## 2. Extracted Text Quality

Extracted text найден:

- `00_input/documents/electricians_knowledge_base/extracted/Установка УЗО при монтаже.md`
- raw source: `00_input/documents/electricians_knowledge_base/raw/Установка УЗО при монтаже.docx`
- chunk: `doc_009_chunk_0001`
- embedded media: none
- related image ids: none

Проверка raw DOCX показала 11 текстовых абзацев; extracted markdown и chunk сохраняют весь текст. Потерь контента не обнаружено.

Ограничения качества:

- документ короткий и технически плотный, поэтому почти каждое утверждение требует expert review;
- нет схемы, фото или visual evidence;
- есть опечатки источника: `небходимо`, `связаться в начальником`;
- формулировка "выполнить его коммутацию в соответствии с п.1" требует осторожного extraction: нельзя расширять ее в самостоятельную схему подключения;
- документ описывает обязательный порядок действий, но не задает полный electrical design context, номиналы, типы УЗО, допустимые схемы и нормативные условия.

## 3. Chunks doc_009

Все chunks лежат в:

- `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`

| chunk_id | section_path | chars | needs_review | содержание |
|:---|:---|---:|:---:|:---|
| `doc_009_chunk_0001` | `Методика установки УЗО на монтажах и сервисах.` | 1136 | yes | Методика установки УЗО при монтажах/сервисах: риск схемы с ИБП между УЗО и автоматами резервной группы; действия при наличии УЗО в щите; варианты размещения дополнительного УЗО; обязательное обращение к начальнику монтажно-сервисной службы. |

## 4. Потенциальные Statement Groups

Рекомендуемые смысловые группы для будущего extraction:

1. `uzo_installation.problem_scenario`
   - При монтаже ИБП возможна схема, где ИБП устанавливается между УЗО и автоматами резервной группы потребителей.
   - В такой схеме при токе утечки на резервной линии УЗО отработает.
   - В такой схеме после срабатывания УЗО подача напряжения на резервную линию продолжится от ИБП.

2. `uzo_installation.existing_uzo_rewire`
   - Если в щите заказчика есть несколько УЗО, резервные автоматы нужно распределить на одно или несколько УЗО.
   - УЗО, к которым отнесены резервные автоматы, нужно подключить после ИБП.
   - При необходимости устанавливается УЗО из набора ЗИП с коммутацией по правилу п.1.

3. `uzo_installation.trip_current_match`
   - Устанавливаемое УЗО должно соответствовать по току срабатывания УЗО, от которого ранее были подключены автоматы группы резерва.

4. `uzo_installation.placement_options`
   - Дополнительное УЗО может размещаться в щите заказчика.
   - Дополнительное УЗО может размещаться в байпасном щите Светон.
   - Для установки УЗО в байпасном щите источник требует извлечь клеммы `"выход фаза"` и `"выход ноль"`, раздвинуть остальные клеммы и установить УЗО.
   - Дополнительное УЗО может размещаться в двухмодульном щите из набора ЗИП рядом со щитом заказчика.

5. `uzo_installation.approval_boundary`
   - При необходимости установки дополнительного УЗО нужно связаться с начальником монтажно-сервисной службы или замещающим его сотрудником.

## 5. Потенциальные Safety-Critical Statements

Ниже не финальные JSONL records, а preflight-кандидаты для будущего extraction. Все используют:

- `source_document_id`: `doc_009`
- `source_file`: `Установка УЗО при монтаже.docx`
- `source_chunk_id`: `doc_009_chunk_0001`

| future candidate | statement draft | source quote | flags |
|:---|:---|:---|:---|
| `doc_009_chunk_0001_stmt_001` | При монтаже ИБП возможна схема, где ИБП устанавливается между УЗО и автоматами резервной группы потребителей. | `ИБП устанавливается между УЗО и автоматами резервной группы потребителей` | `safety_critical`, `review_required` |
| `doc_009_chunk_0001_stmt_002` | Если в такой схеме возникает ток утечки на резервной линии, УЗО отработает. | `в случае образования тока утечки на резервной линии УЗО отработает` | `safety_critical`, `review_required` |
| `doc_009_chunk_0001_stmt_003` | В такой схеме после срабатывания УЗО подача напряжения на резервную линию продолжится от ИБП. | `подача напряжения на резервную линию продолжится уже от ИБП` | `safety_critical`, `review_required`, `blocked_for_instruction` |
| `doc_009_chunk_0001_stmt_004` | Если в щите заказчика несколько УЗО, резервные автоматы нужно распределить на одно или несколько УЗО. | `Если имеется несколько УЗО, то распределить все резервные автоматы на одно, или несколько УЗО` | `safety_critical`, `review_required` |
| `doc_009_chunk_0001_stmt_005` | УЗО, к которым распределены резервные автоматы, нужно подключить после ИБП. | `подключить данные УЗО после ИБП` | `safety_critical`, `review_required`, `blocked_for_instruction` |
| `doc_009_chunk_0001_stmt_006` | УЗО из набора ЗИП устанавливается и коммутируется по правилу распределения резервных автоматов на УЗО после ИБП. | `Установить из набора ЗИП УЗО и выполнить его коммутацию в соответствии с п.1.` | `safety_critical`, `review_required`; wording needs review |
| `doc_009_chunk_0001_stmt_007` | Устанавливаемое УЗО должно соответствовать по току срабатывания УЗО, от которого ранее были подключены автоматы группы резерва. | `Устанавливаемое УЗО должно соответствовать по току срабатывания УЗО, от которого ранее были подключены автоматы группы резерва.` | `safety_critical`, `review_required`, `requires_engineer_review` |
| `doc_009_chunk_0001_stmt_008` | Дополнительное УЗО может быть размещено в щите заказчика. | `В щите заказчика.` | `safety_critical`, `review_required` |
| `doc_009_chunk_0001_stmt_009` | Дополнительное УЗО может быть размещено в байпасном щите Светон. | `В нашем байпасном щите.` | `safety_critical`, `review_required` |
| `doc_009_chunk_0001_stmt_010` | Для установки УЗО в байпасном щите источник требует извлечь клеммы `"выход фаза"` и `"выход ноль"`, раздвинуть остальные клеммы и установить УЗО. | `извлечь клеммы "выход фаза" и "выход ноль", раздвинуть остальные клеммы и установить УЗО` | `safety_critical`, `review_required`, `blocked_for_instruction` |
| `doc_009_chunk_0001_stmt_011` | Дополнительное УЗО может быть размещено рядом со щитом заказчика в двухмодульном щите из набора ЗИП. | `Рядом с щитом заказчика установить двухмодульный щит из набора ЗИП с УЗО.` | `safety_critical`, `review_required` |
| `doc_009_chunk_0001_stmt_012` | При необходимости установки дополнительного УЗО монтажник должен связаться с начальником монтажно-сервисной службы или замещающим его сотрудником. | `необходимо связаться в начальником монтажно-сервисной службы, или замещающим его сотрудником` | `important`, `review_required`; relation to safety-critical approval boundary |

Do not promote any of these statements into final instruction/checklist text before expert review.

## 6. Потенциальные Дубли И Пересечения

Ниже не финальные relations, а preflight-кандидаты для будущего duplicate/related pass.

| doc_009 theme | likely canonical overlap | тип |
|:---|:---|:---|
| Использование/установка УЗО на резервную группу | `doc_003_chunk_0001_stmt_005`, `doc_003_chunk_0001_stmt_006` | `related_to`; training-level overlap, not duplicate |
| Общая логика УЗО и срабатывание при разнице токов | `doc_016_chunk_0005_stmt_005`, `doc_016_chunk_0005_stmt_006` | `related_to`; doc_009 adds UPS-specific failure mode |
| Учет подключения до/после УЗО и нейтрали | `doc_016_chunk_0005_stmt_009`, `doc_016_chunk_0005_stmt_010`, `doc_016_chunk_0006_stmt_001` | `related_to`; safety context |
| Несколько УЗО в щите и отдельные цепи | `doc_016_chunk_0005_stmt_011` | possible partial duplicate/`related_to`; doc_009 adds reserve automats after UPS |
| Определение, к каким УЗО были подключены потребители резерва | `doc_016_chunk_0006_stmt_003` | strong `related_to`; not duplicate because doc_009 prescribes post-UPS connection |
| Сбор фаз и нулей потребителей резерва под одним УЗО | `doc_016_chunk_0006_stmt_004` | potential conflict/needs engineer review: doc_009 allows one or several UZO |
| Выделение резервной группы через изменение схемы в щите | `doc_015_chunk_0018_stmt_002`, `doc_015_chunk_0018_stmt_005` | `related_to` |
| Сохранение безопасности потребителей после УЗО | `doc_015_chunk_0018_stmt_008` | strong `related_to`; doc_009 explains a concrete risk scenario |
| Вариант установки отдельного УЗО на резервную группу | `doc_015_chunk_0018_stmt_009` | possible partial duplicate/`related_to`; doc_009 adds placement and trip-current rule |
| Использование существующего УЗО | `doc_015_chunk_0018_stmt_010`, `doc_015_chunk_0018_stmt_011`, `doc_015_chunk_0018_stmt_017` | `related_to`; possible scenario-specific tension with doc_009 |
| Байпасный щит и реверсивные трассы | `doc_015_chunk_0019_stmt_003`, `doc_015_chunk_0020_stmt_003`, `doc_015_chunk_0020_stmt_004` | `related_to` |
| Обязательное обращение к руководителю при необходимости дополнительного УЗО | `doc_004_chunk_0001_stmt_009`, `doc_004_chunk_0001_stmt_012`, `doc_004_chunk_0001_stmt_016` | `related_to`; doc_009 narrows approval trigger |

Главная новая ценность `doc_009`: конкретный safety risk и правила установки/размещения дополнительного УЗО при резервной группе. Это не нужно схлопывать в существующие общие statements про УЗО или выделение резервной группы.

## 7. Потенциальные Кластеры И Relations

Рекомендуемый основной вариант:

- Новый cluster: `uzo_installation`
- proposed title: `Установка УЗО при монтаже ИБП`
- topic: `uzo_installation`
- source_file: `Установка УЗО при монтаже.docx`
- source_document_id: `doc_009`

Почему лучше отдельный кластер, а не только расширение `C008` или `C009`:

- `C008 / distribution_boards` описывает УЗО, шины, фазы/нули и работу в щите клиента.
- `C009 / installation_process` описывает этапы монтажа, выделение резервной группы, байпас и пусконаладку.
- `doc_009` содержит узкий safety-critical регламент по УЗО при конкретном сценарии подключения ИБП и резервной линии.

Рекомендуемые cluster links:

- `uzo_installation -> C008 distribution_boards`: устройство и логика УЗО, подключение до/после УЗО, фаза/ноль, несколько УЗО в щите.
- `uzo_installation -> C009 installation_process`: выделение резервной группы, ИБП, байпасный щит, пусконаладка.
- `uzo_installation -> C002 installer_roles`: границы ответственности и обязательное обращение к руководителю.
- optional `uzo_installation -> C001 training_levels`: training overlap по вводному УЗО и установке УЗО в щит байпаса.

Не рекомендуется:

- смешивать `doc_009` с editorial section без canonical extraction;
- привязывать к `statement_images.jsonl` без отдельного visual pass, потому что у `doc_009` нет собственных изображений;
- использовать existing images `img_0076`, `img_0077`, `img_0078` как evidence для новых facts. Они могут быть visual context only после отдельного documented manual image-link pass.

## 8. Что Должно Попасть В Coverage Warnings

При будущем extraction ожидаемые warnings/review notes:

- `source_document_review_required`: документ уже помечен в inventory как safety-related review-required.
- `safety_critical_requires_expert_review`: все technical connection/placement/UZO/reserve-group statements должны быть blocked for instruction.
- `short_source_high_density`: короткий документ содержит много технических требований, поэтому нельзя выпускать как инструкцию без expert review.
- `ambiguous_instruction_reference`: формулировка `выполнить его коммутацию в соответствии с п.1` не раскрывает полную схему коммутации.
- `possible_tension_with_existing_statement`: `doc_016_chunk_0006_stmt_004` говорит собирать фазы и нули потребителей резерва под одним УЗО, а `doc_009` допускает распределение резервных автоматов на одно или несколько УЗО; это нужно проверить инженером.
- `source_typo`: `небходимо`, `связаться в начальником`.
- `no_visual_evidence`: в `doc_009` нет схем/изображений, а технические действия с байпасным щитом и клеммами требуют проверки по инженерной документации.

## 9. Рекомендуемая Batch-Стратегия

Не запускать extraction и не писать canonical artifacts, пока не завершен и не синхронизирован текущий `doc_010` run.

После завершения `doc_010`:

1. Создать отдельный run directory, например:
   - `run_YYYYMMDD_doc009_uzo_installation_v1`
2. Обрабатывать только `doc_009_chunk_0001`; документ слишком короткий для разделения на несколько batch chunks.
3. В prompt явно указать:
   - не расширять source text в полную инструкцию;
   - source quotes должны быть exact;
   - все technical statements по УЗО/резервной группе/щиту/байпасу помечать `safety_critical` + `review_required`;
   - approval/boundary statement о начальнике монтажно-сервисной службы помечать как `important` + `review_required`;
   - downstream для technical statements должен быть `blocked_for_instruction`.
4. Ожидаемый объем: 10-12 atomic statements.
5. После extraction выполнить manual dedup/relation pass против:
   - `C008 / distribution_boards`
   - `C009 / installation_process`
   - `C002 / installer_roles`
   - точечно `C001 / training_levels`
6. Сначала создать новый кластер `uzo_installation` или staged cluster candidate, затем связать его с existing clusters.
7. Не добавлять image links в первый extraction pass. Если нужны визуальные подсказки, сделать отдельный documented visual/context pass без утверждения новых facts из изображений.
8. До expert review не использовать результат как монтажную инструкцию, чек-лист подключения или CRM-подсказку для самостоятельного выполнения работ.

## 10. Preflight Conclusion

`doc_009` готов к будущему isolated semantic extraction pass после завершения параллельного `doc_010` процесса. Extracted text и chunk пригодны, но документ safety-critical и должен оставаться blocked for instruction до инженерного review.

Целевой результат будущего pass: новый или staged canonical cluster `uzo_installation`, который уточняет существующие знания `C008/C009` и фиксирует обязательную boundary rule: при необходимости дополнительного УЗО монтажник связывается с начальником монтажно-сервисной службы или замещающим сотрудником.
