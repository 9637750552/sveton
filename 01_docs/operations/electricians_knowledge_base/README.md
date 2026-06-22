# База знаний электриков: карта покрытия

Дата обновления: 2026-06-23

## Текущее состояние

Редакционная база знаний сейчас опирается на canonical statements после batch 011 по `doc_012`:

- `574` валидных атомарных утверждения;
- `14` канонических кластеров покрывают все `574` утверждения;
- `101` утверждение по `doc_015 / installation_process` сгруппировано в `C009`;
- `60` утверждений по `doc_010 / qualification_levels` сгруппировано в `C010`;
- `66` утверждений по `doc_008 / work_on_site` сгруппировано в `C011`;
- `12` утверждений по `doc_009 / uzo_installation` сгруппировано в `C012`;
- `12` утверждений по `doc_001 / service_visit` сгруппировано в `C013`;
- `37` утверждений по `doc_012 / technical_cards` сгруппировано в `C014`;
- `9` собранных markdown-разделов;
- `0` extraction errors;
- `14` coverage / review warnings после batch 011: `3` по `doc_009`, `6` по `doc_001`, `5` по `doc_012`.

Источники состояния:

- `00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/statement_clusters.json`
- `00_input/documents/electricians_knowledge_base/statements/statement_images.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_report.md`

## Карта покрытия

| Раздел | Статус | Каноническая база | Утверждения | Изображения | Основной источник | Комментарий |
|:---|:---|:---|---:|---:|:---|:---|
| `01_basic_knowledge.md` | собран | `C006 / basic_knowledge` | 14 | 1 | `ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1.docx` | Есть source-quality issue по строке про `DC`; раздел годится как учебный слой, не как финальная инструкция без review. |
| `02_ups_components.md` | собран | `C007 / ups_components` | 59 | 14 | `ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5.docx` | Много `safety_critical` знаний: байпас, балансиры, перемычки, DC-защита, GSM-розетка. |
| `03_distribution_boards.md` | собран | `C008 / distribution_boards` | 62 | 17 | `ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1.docx` | Почти весь раздел требует технического review перед использованием как монтажной инструкции. |
| `04_installation_process.md` | собран | `C009 / installation_process` | 101 | 26 | `ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx` | Раздел собран как черновик; `77` пунктов разнесены в safety-review пакет `SR011-SR016`, pre-expert audit выполнен, все safety-critical пункты остаются `blocked_for_instruction` до expert review. |
| будущий `06_service_visit.md` | canonical готов, editorial не собран | `C013 / service_visit` | 12 | 15 context links | `Действия на сервисном выезде.docx` | Кластер покрывает сервисный выезд по выравниванию АКБ: проверки инвертора, АКБ, балансира, затяжки соединений и фото/видео фиксацию. Визуальный слой добавлен как cross-source context из уже accepted image links; прямых изображений в источнике нет. |
| будущий `16_technical_cards.md` | canonical text-backed готов, OCR/manual pending | `C014 / technical_cards` | 37 | 0 | `ЭЛК_2_1 техн.карты изделий..docx` | Кластер покрывает table-aware text-backed технические карты изготовления кабеля «Инвертор-щит» и перемычек АКБ. Факты из `img_0029` и `img_0030` не извлекались; они требуют отдельного OCR/manual review pass. |
| `07_photo_report.md` | собран | `C004 / photo_report` | 30 | 2 | `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx` | Раздел собран как чек-лист фотофиксации и контроль состава фотоотчета. |
| `08_installer_roles.md` | собран | `C002 / installer_roles` | 31 | 0 | `Обязанности монтажника.docx` | Организационный регламент выезда, закрытия работ и передачи результата. |
| `09_installation_report.md` | собран | `C003 / reporting` | 51 | 0 | `Отчет по монтажу р1.docx` | Есть rule/example связи; они сохранены, а не схлопнуты. |
| `10_training_levels.md` | собран | `C001 / training_levels` | 19 | 0 | `Обучение в офисе.docx` | HTML-таблица контрольного листа еще не разобрана table-aware способом. |
| `12_installation_request_check.md` | собран | `C005 / installation_request_check` | 20 | 0 | `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx` | Раздел доведен completion-pass'ом и теперь покрывает исходник по canonical-слою. |
| будущий `14_qualification_levels.md` | canonical готов, editorial не собран | `C010 / qualification_levels` | 60 | 0 | `Что_должен_знать_и_уметь_монтажник_каждой_ступени1_1.docx` | Кластер покрывает стажера, монтажника-электрика, 1-й разряд и критерии перехода во 2-й разряд; `25` утверждений требуют safety-review перед допусковым регламентом. |
| будущий `05_work_on_site.md` | canonical готов, editorial не собран | `C011 / work_on_site` | 66 | 0 | `Работа на объекте 2024 ред1_7.docx` | Кластер покрывает распределение действий первого номера, второго номера и стажера на объекте; `39` утверждений требуют safety-review перед использованием как регламента. |
| будущий `15_uzo_installation.md` | canonical готов, editorial не собран | `C012 / uzo_installation` | 12 | 0 | `Установка УЗО при монтаже.docx` | Кластер покрывает safety-critical методику установки УЗО при монтаже: риск схемы с ИБП между УЗО и автоматами резервной группы, дополнительное УЗО, размещение УЗО и обязательное согласование. Все `12` утверждений требуют expert review перед использованием как инструкции. |

## Что покрыто полностью

Сейчас в рабочем контуре закрыты тринадцать исходных документов полностью и один источник закрыт по text-backed extraction с OCR/manual остатком:

- `Действия на сервисном выезде.docx`
- `Обучение в офисе.docx`
- `Обязанности монтажника.docx`
- `Отчет по монтажу р1.docx`
- `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx`
- `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx`
- `Работа на объекте 2024 ред1_7.docx`
- `Установка УЗО при монтаже.docx`
- `Что_должен_знать_и_уметь_монтажник_каждой_ступени1_1.docx`
- `ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1.docx`
- `ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5.docx`
- `ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx`
- `ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1.docx`

По `source_coverage_report.md` эти документы закрыты прямыми canonical-утверждениями или явными coverage overrides для split/duplicate-фрагментов.

`ЭЛК_2_1 техн.карты изделий..docx` закрыт по текстовым HTML-таблицам chunks `doc_012_chunk_0001` и `doc_012_chunk_0002`; chunk `doc_012_chunk_0003` оставлен `needs_review`, потому что содержит image-only таблицу назначения матриц пресс-клещей и требует OCR/manual extraction.

## Что пока не собрано как самостоятельные разделы

В целевой структуре эпика есть разделы:

- `05_work_on_site.md`
- `06_service_visit.md`
- `11_hiring_and_interview.md`
- `13_quality_control.md`
- будущий раздел по квалификационным уровням и допускам монтажника.

Для `04_installation_process.md` canonical extraction, кластер, editorial layer, image-link pass и pre-expert safety audit уже собраны; остался экспертный technical safety-review.

Для квалификационных уровней canonical extraction и кластер `C010 / qualification_levels` уже собраны; editorial layer еще не собран, а `25` safety-critical утверждений вынесены в `SR017`.

Для `05_work_on_site.md` canonical extraction и кластер `C011 / work_on_site` уже собраны; editorial layer еще не собран, а `39` safety-critical утверждений вынесены в `SR018`.

Для будущего раздела по установке УЗО canonical extraction и кластер `C012 / uzo_installation` уже собраны; editorial layer еще не собран, все `12` утверждений остаются `safety_critical/review_required`, а warning по возможному напряжению с `doc_016_chunk_0006_stmt_004` требует expert review.

Для `06_service_visit.md` canonical extraction и кластер `C013 / service_visit` уже собраны; editorial layer еще не собран, все технические statements остаются `safety_critical/review_required`, а warnings по напряжению АКБ, режимам инвертора, процедуре выравнивания и отсутствию прямого visual evidence из самого `doc_001` требуют review. Визуальный слой есть как `visual_context` links к уже accepted изображениям из других источников.

Для будущего раздела технических карт изделий canonical text-backed extraction и кластер `C014 / technical_cards` уже собраны; editorial layer еще не собран, все операции изготовления кабеля, перемычек АКБ, опрессовки, матриц и термоусадки остаются `review_required`, а `img_0029` и `img_0030` заблокированы до отдельного OCR/manual review pass.

Для `11/13` сейчас нет отдельного канонического кластера. Это означает следующее:

- их нельзя честно объявлять самостоятельными source-backed разделами;
- их можно потом собирать только как редакционные композитные документы поверх уже готовых кластеров;
- если нужен новый самостоятельный источник истины для этих тем, понадобится новый extraction по дополнительным документам.

## Рекомендуемая привязка будущих разделов

| Будущий раздел | Как собирать | Основание |
|:---|:---|:---|
| `04_installation_process.md` | source-backed draft собран | `C009 / installation_process` |
| `05_work_on_site.md` | source-backed editorial layer после review-структурирования | `C011 / work_on_site` + связи с `C002`, `C004`, `C003`, `C009`, `C010` |
| `06_service_visit.md` | source-backed editorial layer после expert review | `C013 / service_visit` + связи с `C002`, `C003`, `C004`, `C007`, `C009`, `C010`, `C011` |
| `16_technical_cards.md` | source-backed editorial layer после technical/OCR review | `C014 / technical_cards` + связи с `C007`, `C009`, `C010` |
| `11_hiring_and_interview.md` | не собирать до нового extraction | рекрутинговый файл исключен из benchmark и не лежит в canonical как технический источник |
| `13_quality_control.md` | композитный editorial layer | `C004` + `C005` + `C003` + future safety-review |
| `14_qualification_levels.md` | source-backed editorial layer после review-структурирования | `C010 / qualification_levels` |
| `15_uzo_installation.md` | source-backed editorial layer после expert review | `C012 / uzo_installation` + связи с `C008`, `C009`, `C010`, `C002` |

## Практический вывод

Сейчас база знаний находится в хорошем состоянии для двух типов работы:

1. Дальше собирать source-backed разделы только там, где уже есть отдельный canonical-кластер.
2. Начинать собирать композитные прикладные документы поверх готовых кластеров, явно помечая их как editorial composition, а не как новый первичный источник.

Граница между этими двумя типами документов теперь должна оставаться жесткой.
