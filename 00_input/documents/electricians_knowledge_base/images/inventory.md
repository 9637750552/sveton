# Инвентаризация изображений базы знаний электриков

Дата создания: 2026-06-16

## Назначение

Этот файл фиксирует извлеченные изображения из исходных DOCX/PDF документов базы знаний.

На текущем этапе есть два уровня инвентаризации:

- source-level summary в этом файле;
- per-image таблица `inventory.csv`.

По каждому документу здесь зафиксировано:

- сколько визуальных артефактов извлечено;
- каким способом они получены;
- какой у них предварительный тип;
- какие требуют ручной проверки;
- что нужно сделать перед связыванием с чанками и атомарными утверждениями.

## Статусы

- `raw_extracted`: изображения извлечены в `images/raw/`;
- `needs_classification`: нужна ручная или полуавтоматическая классификация;
- `review_required`: изображения нельзя использовать без проверки;
- `ready_for_linking`: источник можно привязывать к чанкам и nearby text;
- `exclude_candidate`: вероятный мусор, декоративные элементы или дубли.

## Текущий итог

- Всего визуальных артефактов: `110`.
- Из DOCX извлечено встроенных изображений: `110`.
- Из PDF отрендерено страниц: `0`.
- Папка исходных изображений: `00_input/documents/electricians_knowledge_base/images/raw/`.
- Папка нормализованных изображений: `00_input/documents/electricians_knowledge_base/images/normalized/`.
- Для раздела `photo_report` созданы normalized-копии с короткими ASCII-именами: `photo_report_img_001.jpeg`, `photo_report_img_002.jpeg`.
- Детальная таблица по каждому изображению: `00_input/documents/electricians_knowledge_base/images/inventory.csv`.
- План привязки изображений к чанкам и утверждениям: `00_input/documents/electricians_knowledge_base/images/linking_plan.md`.

Распределение по предварительным типам:

- `diagram`: `94`;
- `photo_example`: `3`;
- `decorative_or_unclear`: `13`.

Распределение по статусам:

- `raw_extracted|needs_classification`: `84`;
- `raw_extracted|ready_for_linking`: `13`;
- `raw_extracted|exclude_candidate|needs_classification`: `13`.

Распределение по linking buckets:

- `ready_for_linking`: `13`;
- `candidate_for_linking`: `84`;
- `exclude_candidate`: `13`.

Контекст:

- `source_anchor` заполнен для `110` из `110` строк;
- `nearby_text` заполнен для `110` из `110` строк;
- DOCX-контекст привязан через исходные `media/imageN`;
- PDF-derived visual artifacts for `doc_014`/`doc_017` removed; current `doc_014` visual links use DOCX embedded media only.

## Метод извлечения

- `DOCX`: извлечение встроенных файлов из `word/media/`.
- `PDF`: рендер страниц в PNG через `ghostscript` only when explicitly approved for a source; obsolete `doc_014`/`doc_017` PDF renders are not part of the current corpus.

Важно:

- Для DOCX имя извлеченного файла сохраняет исходный номер `media/imageN`, чтобы можно было надежно связать картинку с markdown-текстом.
- PDF page renders are not used for current `doc_014` links.
- Картинка не должна порождать техническое правило без nearby text, подписи или ручной проверки.
- Мелкие иконки, пустые фрагменты и cropped-объекты помечаются `exclude_candidate`, пока не доказана их полезность.

## Источники

| Источник | Формат | Кол-во | Способ | Предварительный тип | Статус | Комментарий |
|---|---|---:|---|---|---|---|
| `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx` | DOCX | 2 | embedded media | `photo_example` | `raw_extracted, ready_for_linking` | Фото-примеры для правил съемки монтажа. Приоритетный источник для раздела `photo_report`. |
| `ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1.docx` | DOCX | 1 | embedded media | `diagram` | `raw_extracted, ready_for_linking` | Похоже на базовую схему/иллюстрацию по понятиям. |
| `ЭЛК_2_1 техн.карты изделий..docx` | DOCX | 27 | embedded media | `diagram` / `table_image` | `raw_extracted, needs_classification` | Крупный визуальный блок техкарт. Здесь вероятны схемы, карточки, таблицы и мелкие декоративные фрагменты. |
| `ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5.docx` | DOCX | 15 | embedded media | `diagram` | `raw_extracted, needs_classification` | Вероятные схемы и составные элементы ИБП. Высокая ценность для учебника. |
| `ЭЛК_3_1процесс монтажа.docx` | DOCX | 10 | selected embedded media | `diagram` / `photo_example` | `raw_extracted, ready_for_linking` | Отобранные вручную DOCX-картинки для accepted links к уже существующим `doc_014` text-backed statements; visual-only схемы не продвигались. |
| `ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx` | DOCX | 28 | embedded media | `diagram` / `photo_example` | `raw_extracted, needs_classification` | Крупный визуальный блок по этапам монтажа. Возможна смесь схем и фото. |
| `ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1.docx` | DOCX | 27 | embedded media | `diagram` | `raw_extracted, needs_classification` | Вероятные схемы и иллюстрации элементов щитов. |

## Что уже понятно по визуальному корпусу

- `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx` действительно содержит полезные фото-примеры монтажа.
- `ЭЛК_1_...Основные_понятия...` содержит читаемую схему соединения аккумуляторов.
- Техкарты, состав ИБП, этапы монтажа и элементы щитов в основном состоят из схем, карточек и технических иллюстраций.
- Внутри DOCX есть мелкие иконки, crop-фрагменты и пустые/почти пустые изображения; они автоматически помечены как `exclude_candidate`.
- Для `doc_014` добавлен отдельный manual visual-link pass: картинки иллюстрируют только уже извлеченные text-backed statements и не создают новые факты.

## Следующие действия

- [x] Извлечь изображения в `images/raw/`.
- [x] Просмотреть визуальные артефакты и отделить полезные изображения от декоративных/шумовых.
- [x] Заполнить первичную per-image классификацию для всех 118 артефактов в `inventory.csv`.
- [x] Добавить `image_id` для всех строк `inventory.csv`.
- [x] Подготовить `nearby_text`, `source_anchor` и первичные captions.
- [x] Выбрать изображения для разделов `photo_report`, `installation_process`, `ups_components`, `distribution_boards`.
- [x] Подготовить правила будущей привязки к чанкам и `related_image_ids`.
- [x] Привязать изображения `photo_report` к canonical-утверждениям: `img_0001`, `img_0002` -> `doc_006_chunk_0003_stmt_001`.
- [ ] Провести ручной отбор `candidate_for_linking` и `manual_pdf_review`.

## Риск

На текущем этапе инвентаризация не является окончательной классификацией. Она фиксирует корпус и точки внимания, но не заменяет ручной просмотр артефактов перед semantic extraction и учебной сборкой.
