# Preflight doc_001: service_visit semantic extraction

Дата: 2026-06-22

Источник: `doc_001 / Действия на сервисном выезде.docx`

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

По текущей карте покрытия `06_service_visit.md` нельзя объявлять source-backed разделом: в canonical слое нет самостоятельного сервисного корпуса. `doc_001` является прямым кандидатом на новый `service_visit` cluster, но его нельзя записывать в общий canonical слой до завершения параллельных extraction/preflight runs и синхронизации общего слоя.

Postgres import contract требует сохранять `source_document_id`, `source_file`, `source_chunk_id`, source quotes, review flags, risk fields и валидные связи с clusters/statements. Поэтому этот preflight фиксирует только будущие candidates и relation notes.

## 2. Extracted Text Quality

Extracted text найден:

- `00_input/documents/electricians_knowledge_base/extracted/Действия на сервисном выезде.md`
- формат: короткий markdown checklist
- raw docx и extracted markdown совпадают по смысловому содержанию
- изображений и media refs нет

Качество пригодно для semantic extraction:

- структура сохранена как заголовок и 12 checklist bullets;
- таблиц, OCR-шума и потерянных ролей нет;
- HTML-комментарии `<!-- -->` в markdown не несут смысла и не должны превращаться в statements;
- chunk metadata сейчас имеет `needs_review=false`, но будущий extraction должен пометить технические statements как `review_required`.

Source-quality ограничения:

- документ не задает норм напряжения АКБ, моментов затяжки, типа смазки, списка режимов инвертора или методику выравнивания АКБ;
- условие `при выключенном инверторе` явно относится к продувке инвертора, но не должно автоматически переноситься на снятие крышки и повторную продувку без отдельного review;
- пункт `во всех режимах` требует экспертного уточнения перед использованием в инструкции;
- пункт `Выравнивание АКБ` является действием без описанной процедуры, поэтому не годится для пошаговой инструкции без expert review.

## 3. Chunks doc_001

Все chunks лежат в:

- `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`

| chunk_id | section_path | chars | needs_review | содержание |
|:---|:---|---:|:---:|:---|
| `doc_001_chunk_0001` | `Методика проведения сервисного выезда по выравниванию АКБ.` | 595 | no | Один checklist сервисного выезда: затяжка проводов, продувка инвертора, настройки инвертора, напряжение и болты АКБ, режимы инвертора, балансир, выравнивание АКБ, фото/видео фиксация. |

Рекомендация для будущего run: оставить один source chunk, но внутри prompt явно разделить технические проверки и отчетную фиксацию.

## 4. Потенциальные Statement Groups

Ниже не финальные canonical statements, а source-backed candidates для будущего extraction. Все candidates должны использовать:

- `source_document_id`: `doc_001`
- `source_file`: `Действия на сервисном выезде.docx`
- `source_chunk_id`: `doc_001_chunk_0001`

| group | source quote | будущая атомаризация |
|:---|:---|:---|
| `service_visit.wire_tightening` | `Проверка затяжки проводов в клеммных терминалах инвертора, щитах.` | Отдельный checklist item про проверку затяжки проводов в клеммных терминалах инвертора и щитах. |
| `service_visit.inverter_cleaning` | `Продувка инвертора(при выключенном инверторе).` | Отдельный statement: продувка инвертора проводится при выключенном инверторе. |
| `service_visit.inverter_cleaning` | `Снятие крышки инвертора и повторная продувка(при необходимости).` | Отдельный conditional statement: при необходимости снимается крышка инвертора и выполняется повторная продувка. |
| `service_visit.inverter_settings` | `Проверка настроек инвертора.` | Отдельный checklist item про проверку настроек инвертора без добавления конкретных параметров. |
| `service_visit.battery_measurement` | `Замер напряжения на АКБ.` | Отдельный checklist item про замер напряжения на АКБ. |
| `service_visit.battery_bolts` | `Проверка болтов на АКБ(затяжка, состояние).` | Отдельный checklist item про проверку затяжки и состояния болтов АКБ. |
| `service_visit.battery_bolts` | `Смазка болтов АКБ(при необходимости).` | Отдельный conditional statement про смазку болтов АКБ при необходимости. |
| `service_visit.inverter_modes` | `Проверка работы инвертора во всех режимах.` | Отдельный checklist item; не раскрывать режимы, если они не названы в источнике. |
| `service_visit.balancer` | `Проверка работы балансира.` | Отдельный checklist item про проверку работы балансира. |
| `service_visit.battery_equalization` | `Выравнивание АКБ.` | Отдельный checklist item; не превращать в процедуру выравнивания. |
| `service_visit.battery_measurement` | `Проверка напряжения на АКБ.` | Потенциальный дубль/усиление к `Замер напряжения на АКБ`; лучше связать как duplicate/related внутри doc_001, если оба сохраняются. |
| `service_visit.reporting_media` | `Фотографии и видеозаписи настроек оборудования, измерений, выполненной работы.` | Отдельное reporting requirement: фото/видео фиксация настроек, измерений и выполненной работы. |

Предварительный объем: 10-12 атомарных statements. Если объединять `Замер напряжения на АКБ` и `Проверка напряжения на АКБ`, ожидаемый объем ближе к 10-11.

## 5. Safety / Review Flags

Рекомендуемые флаги для будущих statements:

| theme | recommended flags | причина |
|:---|:---|:---|
| Затяжка проводов в инверторе и щитах | `risk_level=safety_critical`, `review_status=review_required` | Электрические соединения и щиты. |
| Продувка инвертора при выключенном инверторе | `risk_level=safety_critical`, `review_status=review_required` | Действие с инвертором и явно заданное условие выключения. |
| Снятие крышки инвертора и повторная продувка | `risk_level=safety_critical`, `review_status=review_required` | Открытие оборудования и обслуживание инвертора. |
| Проверка настроек инвертора | `risk_level=safety_critical`, `review_status=review_required` | Настройки инвертора влияют на режимы и АКБ; параметры не перечислены. |
| Замер/проверка напряжения АКБ | `risk_level=safety_critical`, `review_status=review_required` | Измерения на АКБ без указанных норм и процедуры. |
| Проверка затяжки и состояния болтов АКБ | `risk_level=safety_critical`, `review_status=review_required` | АКБ и болтовые соединения. |
| Смазка болтов АКБ | `risk_level=safety_critical`, `review_status=review_required` | Действие с АКБ; источник не задает материал и условия применения. |
| Проверка инвертора во всех режимах | `risk_level=safety_critical`, `review_status=review_required` | Режимы работы не определены источником. |
| Проверка балансира | `risk_level=safety_critical`, `review_status=review_required` | Балансир связан с АКБ и выравниванием напряжения. |
| Выравнивание АКБ | `risk_level=safety_critical`, `review_status=review_required`, `downstream_status=blocked_for_instruction` | Процедура не раскрыта, но действие технически критичное. |
| Фото/видео фиксация настроек, измерений и работы | `risk_level=important`, `review_status=review_required`, `visual_review_required=true` | Это отчетное требование, но оно фиксирует safety-relevant настройки и измерения. |

Для всех safety-critical statements будущий downstream status должен оставаться `blocked_for_instruction` до expert review.

## 6. Потенциальные Дубли И Пересечения

В текущем canonical слое нет statements, coverage rows, relations или image links с `doc_001`. Поэтому `doc_001` не является canonical duplicate как документ. Пересечения ниже являются relation candidates для будущего dedup/relation pass.

| doc_001 theme | likely canonical overlap | тип |
|:---|:---|:---|
| Сервисный выезд как выполнение задания | `doc_004_chunk_0001_stmt_001`, `doc_004_chunk_0001_stmt_012`, `doc_004_chunk_0002_stmt_012`, `doc_004_chunk_0002_stmt_013` | `related_to`: `doc_004` задает обязанности на выезде, `doc_001` задает сервисные действия. |
| Проверка затяжки проводов в инверторе и щитах | `doc_015_chunk_0019_stmt_007`, `doc_015_chunk_0012_stmt_004` | `related_to`, не duplicate: installation pre-start/assembly control vs service visit check. |
| Продувка инвертора и снятие крышки | прямого duplicate не найдено | Новый service_visit content; связать с `C007 / ups_components` и `C009 / installation_process` только на уровне component/process context. |
| Проверка настроек инвертора | `doc_015_chunk_0019_stmt_011`-`doc_015_chunk_0019_stmt_015`, `doc_015_chunk_0019_stmt_017`-`doc_015_chunk_0019_stmt_020`, `doc_005_chunk_0002_stmt_004`, `doc_005_chunk_0027_stmt_001` | `related_to`: `doc_001` требует проверку, canonical уже содержит конкретные installation/reporting settings. |
| Замер/проверка напряжения АКБ | `doc_011_chunk_0006_stmt_003`-`doc_011_chunk_0006_stmt_005`, `doc_013_chunk_0014_stmt_003`, `doc_013_chunk_0015_stmt_001`, `doc_013_chunk_0015_stmt_002` | `related_to`; не duplicate, потому что existing statements описывают свойства/сборку АКБ, а не сервисный замер. |
| Проверка и смазка болтов АКБ | `doc_015_chunk_0012_stmt_004` | Частичный `related_to`; смазка болтов АКБ прямого canonical overlap не имеет. |
| Проверка работы инвертора во всех режимах | `doc_015_chunk_0019_stmt_009`, `doc_015_chunk_0019_stmt_015`, `doc_015_chunk_0020_stmt_001`, `doc_015_chunk_0020_stmt_005`, `doc_015_chunk_0020_stmt_006`, `doc_005_chunk_0001_stmt_010` | `related_to`; не раскрывать список режимов на основе этих связей. |
| Проверка работы балансира | `doc_013_chunk_0007_stmt_001`, `doc_013_chunk_0017_stmt_001`-`doc_013_chunk_0017_stmt_003`, `doc_005_chunk_0001_stmt_014`, `doc_005_chunk_0025_stmt_001` | `related_to`: component knowledge/reporting issue vs service check. |
| Выравнивание АКБ | `doc_013_chunk_0017_stmt_001`, `doc_013_chunk_0018_stmt_002`, `doc_013_chunk_0020_stmt_002` | `related_to`, safety-critical. Не превращать в duplicate, потому что `doc_001` задает действие сервисного выезда. |
| Фото/видео фиксация настроек, измерений и работы | `doc_006_chunk_0006_stmt_001`-`doc_006_chunk_0006_stmt_005`, `doc_006_chunk_0004_stmt_001`, `doc_006_chunk_0004_stmt_002`, `doc_004_chunk_0002_stmt_004` | Сильное пересечение с `photo_report`; future relation может быть `related_to` или частичный duplicate для фиксации настроек инвертора. |
| Два пункта про напряжение АКБ внутри `doc_001` | future `doc_001` candidates на `Замер напряжения` и `Проверка напряжения` | Внутренний `duplicate_of` или `related_to`; решение принять на extraction/review pass. |

## 7. Потенциальные Кластеры И Relations

Рекомендуемый основной вариант:

- Новый cluster topic: `service_visit`
- Title: `Сервисный выезд по выравниванию АКБ`
- Source file: `Действия на сервисном выезде.docx`
- Primary future output: `06_service_visit.md`

Не фиксировать `cluster_id` в preflight. Сейчас canonical содержит `C001`-`C009`, а параллельно уже готовятся `doc_008`, `doc_009` и `doc_010`; номер нового кластера нужно назначать только после общей синхронизации.

Рекомендуемые межкластерные связи:

- `service_visit -> C002 installer_roles`: сервисный выезд, выполнение задания, закрытие результата.
- `service_visit -> C003 reporting`: фиксация измерений, настроек, неисправностей и выполненной работы.
- `service_visit -> C004 photo_report`: фото/видео настроек инвертора, показаний, АКБ и результата.
- `service_visit -> C007 ups_components`: АКБ, инвертор, балансир, выравнивающая перемычка.
- `service_visit -> C009 installation_process`: настройки инвертора, проверка режимов, затяжка соединений, АКБ.

Связь с `installation_process` должна оставаться relation/context. Не нужно переносить service actions в `C009`, если statement добавляет именно сервисный контекст.

## 8. Coverage / Review Пометки

Для будущего coverage pass:

- `doc_001_chunk_0001` сейчас отсутствует в `source_coverage_report.jsonl`;
- после extraction он должен стать `covered` только если все технические bullets получили statements или documented duplicate/override;
- если два пункта про напряжение АКБ объединяются, coverage должен явно указать duplicate/merge rationale;
- reporting bullet про фото/видео не должен покрывать технические проверки и наоборот.

Рекомендуемые warnings/review notes, но не для записи сейчас:

| artifact | future check | note |
|:---|:---|:---|
| `coverage_warnings.jsonl` | `undefined_modes` | Источник требует проверку инвертора во всех режимах, но режимы не перечислены. |
| `coverage_warnings.jsonl` | `missing_thresholds` | Источник требует замер/проверку напряжения АКБ без норм и допустимых диапазонов. |
| `coverage_warnings.jsonl` | `missing_procedure` | Источник требует выравнивание АКБ без процедуры. |
| `coverage_warnings.jsonl` | `ambiguous_condition_scope` | Условие выключенного инвертора явно указано для продувки, но не для снятия крышки/повторной продувки. |
| `coverage_warnings.jsonl` | `potential_internal_duplicate` | `Замер напряжения на АКБ` и `Проверка напряжения на АКБ` могут быть duplicate/near-duplicate. |
| review queue | `technical_safety_review` | Большинство technical candidates должны быть blocked for instruction до expert review. |
| review queue | `visual_evidence_review` | Фото/видео settings/measurements/work should seed visual evidence review после появления approved image/video evidence workflow. |

## 9. Рекомендуемая Batch-Стратегия

Не запускать extraction и не писать canonical artifacts, пока не завершены и не синхронизированы параллельные runs.

После синхронизации:

1. Создать отдельный run directory, например:
   - `run_YYYYMMDD_doc001_service_visit_v1`
2. Обрабатывать только `doc_001_chunk_0001`.
3. В prompt явно запретить:
   - добавлять нормы напряжения, моменты затяжки, тип смазки, порядок отключения/включения;
   - раскрывать список режимов инвертора, если источник их не называет;
   - превращать `Выравнивание АКБ` в процедуру.
4. Внутри одного batch разделить candidates на две группы:
   - technical service checks: провода, инвертор, АКБ, болты, режимы, балансир, выравнивание;
   - reporting/media: фото и видео настроек, измерений, выполненной работы.
5. После extraction выполнить manual dedup/relation pass против `C002`, `C003`, `C004`, `C007`, `C009`.
6. Для safety-critical candidates сразу ставить `review_status=review_required`; для downstream use ставить `blocked_for_instruction` до expert review.
7. Назначить cluster id только после общей синхронизации с `doc_008`, `doc_009`, `doc_010`.

## 10. Preflight Conclusion

`doc_001` готов к отдельному semantic extraction pass как источник нового `service_visit` cluster. Документ короткий и extraction-friendly, но технически рискованный: почти все действия связаны с инвертором, АКБ, балансиром, электрическими соединениями или режимами работы.

Главная новая ценность `doc_001`: не общие знания об ИБП и не монтажный процесс, а сервисный checklist по выравниванию АКБ с отдельной отчетной фиксацией настроек, измерений и выполненной работы.
