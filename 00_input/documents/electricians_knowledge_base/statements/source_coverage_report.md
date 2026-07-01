# Source Coverage Report

## Summary

- Source files checked: `16`
- Chunks checked: `151`
- `covered`: `102`
- `ignored`: `45`
- `uncovered_content`: `4`

## By File

- `Действия на сервисном выезде.docx`: `covered`: `1`
- `Ищем_электриков_для_сотрудничества.docx`: `uncovered_content`: `4`
- `Обучение в офисе.docx`: `covered`: `1`
- `Обязанности монтажника.docx`: `covered`: `2`
- `Отчет по монтажу р1.docx`: `covered`: `15`, `ignored`: `22`
- `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx`: `covered`: `8`, `ignored`: `2`
- `Проверка_соответвие_описания_менеджера_правилам_заявки_на_монтаж.docx`: `covered`: `11`, `ignored`: `5`
- `Работа на объекте 2024 ред1_7.docx`: `covered`: `5`, `ignored`: `1`
- `Установка УЗО при монтаже.docx`: `covered`: `1`
- `Что_должен_знать_и_уметь_монтажник_каждой_ступени1_1.docx`: `covered`: `3`
- `ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1.docx`: `covered`: `4`, `ignored`: `2`
- `ЭЛК_2_1 техн.карты изделий..docx`: `covered`: `3`
- `ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5.docx`: `covered`: `19`, `ignored`: `5`
- `ЭЛК_3_1процесс монтажа.docx`: `covered`: `5`, `ignored`: `4`
- `ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx`: `covered`: `16`, `ignored`: `4`
- `ЭЛК_4_Базовые_знания_Элементы_распред_щитов_ред1.docx`: `covered`: `8`

## Uncovered Content Chunks

### `doc_002_chunk_0001`

- Source: `Ищем_электриков_для_сотрудничества.docx`
- Reason: `no_canonical_statement_for_content_chunk`
- Preview: Ищем электриков для сотрудничества Компания Ромашка приглашает электриков к сотрудничеству по монтажу систем бесперебойного питания ИБП в частных домах, коттеджах, офисах и на объе

### `doc_002_chunk_0002`

- Source: `Ищем_электриков_для_сотрудничества.docx`
- Reason: `no_canonical_statement_for_content_chunk`
- Preview: Что нужно делать: - монтаж и подключение резервных линий к ИБП; - аккуратная прокладка кабеля; - настройка системы после монтажа

### `doc_002_chunk_0003`

- Source: `Ищем_электриков_для_сотрудничества.docx`
- Reason: `no_canonical_statement_for_content_chunk`
- Preview: Требования: - статус самозанятого или ИП ; - опыт электромонтажных работ; - аккуратность и ответственность; - наличие электроинструмента и личного автомобиля

### `doc_002_chunk_0004`

- Source: `Ищем_электриков_для_сотрудничества.docx`
- Reason: `no_canonical_statement_for_content_chunk`
- Preview: Условия: - сотрудничество по договору; - свободный график; - заказы по мере поступления в вашем регионе; - понятные технические задания; - оплата за выполненные объекты; - возможно


## Coverage Overrides

### `doc_005_chunk_0004`

- Source: `Отчет по монтажу р1.docx`
- Reason: `split_example_continuation`
- Covered by: `doc_005_chunk_0027_stmt_002`, `doc_005_chunk_0027_stmt_003`
- Notes: Фрагмент продолжает пример из соседнего чанка: замер тока 15 А и максимальная нагрузка 5,2 кВт уже представлены в canonical через полный пример.

### `doc_005_chunk_0014`

- Source: `Отчет по монтажу р1.docx`
- Reason: `duplicate_example_and_heading`
- Covered by: `doc_005_chunk_0027_stmt_003`, `doc_005_chunk_0001_stmt_010`
- Notes: Чанк содержит повтор примера максимальной нагрузки и заголовок следующего пункта про ручной режим; оба знания уже представлены в canonical.

### `doc_005_chunk_0030`

- Source: `Отчет по монтажу р1.docx`
- Reason: `example_section_heading`
- Covered by: `doc_005_chunk_0001_stmt_006`, `doc_005_chunk_0006_stmt_002`
- Notes: Чанк является заголовком пункта полного примера: 'В группе резерва установлены автоматы'.

### `doc_005_chunk_0035`

- Source: `Отчет по монтажу р1.docx`
- Reason: `duplicate_example`
- Covered by: `doc_005_chunk_0011_stmt_001`
- Notes: Повтор примера обычной кабель-трассы в полном отчете; правило и пример уже представлены в canonical.

### `doc_006_chunk_0010`

- Source: `Правила_фотосъемки_монтажа_Чек_лист_ред1.docx`
- Reason: `duplicate_visual_rule`
- Covered by: `doc_006_chunk_0003_stmt_001`
- Notes: Визуальный блок повторяет правило о 4-6 качественных фото системы с запасом по сторонам; изображения связаны отдельно через statement_images.jsonl.

### `doc_013_chunk_0023`

- Source: `ЭЛК_2_Базовые_знания_Состав_ИБП_ред1_5.docx`
- Reason: `image_only_duplicate`
- Covered by: `doc_013_chunk_0010_stmt_001`, `doc_013_chunk_0010_stmt_002`
- Notes: Chunk contains only the heading 'Защитные панели' and image img_0044. Textual knowledge about protective panels is covered by doc_013_chunk_0010 statements; img_0044 is linked in the editorial visual layer.

### `doc_014_chunk_0002`

- Source: `ЭЛК_3_1процесс монтажа.docx`
- Reason: `duplicate_existing_canonical`
- Covered by: `doc_012_chunk_0002_stmt_020`, `doc_012_chunk_0002_stmt_021`, `doc_012_chunk_0002_stmt_022`, `doc_012_chunk_0002_stmt_029`, `doc_012_chunk_0002_stmt_030`
- Notes: Подготовка проводов балансира в doc_014 текстово дублирует уже продвинутые source-backed statements из doc_012 technical cards; новые canonical duplicates не создавались.

### `doc_014_chunk_0004`

- Source: `ЭЛК_3_1процесс монтажа.docx`
- Reason: `duplicate_and_ambiguous_visual_labels`
- Covered by: `doc_015_chunk_0014_stmt_007`, `doc_015_chunk_0014_stmt_010`, `doc_015_chunk_0014_stmt_008`
- Notes: Монтаж инвертора в doc_014 частично повторяет вентиляционные требования doc_015, но содержит неоднозначный extracted fragment "Не допустимо / 20 мм."; новые statements не создавались до manual visual review.

### `doc_014_chunk_0008`

- Source: `ЭЛК_3_1процесс монтажа.docx`
- Reason: `visual_scheme_labels_manual_review`
- Covered by: `doc_015_chunk_0016_stmt_003`, `doc_015_chunk_0016_stmt_004`, `doc_015_chunk_0016_stmt_005`
- Notes: Подключение проводов реверсивной линии в однофазном байпасном щите представлено главным образом схемой и короткими labels; image-only/diagram-only facts не продвигались в canonical.


## Machine Rows

See JSONL companion if generated by caller.
