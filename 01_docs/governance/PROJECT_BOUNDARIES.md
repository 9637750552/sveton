# Границы проектов: Sveton, Semantic Analysis Engine, Knowledge Base

Дата решения: 2026-06-17.

## 1. Решение

Текущий репозиторий фактически содержит три разных проекта:

1. `Sveton` - бизнес-проект и доменный workspace.
2. `Semantic Analysis Engine` - переиспользуемый продукт для извлечения и проверки смысловых утверждений.
3. `Sveton Knowledge Base` - продуктовая база знаний, собранная из источников Sveton через semantic analysis pipeline.

Дальше эти направления должны развиваться как отдельные project boundaries. Физическое разделение по репозиториям выполняется поэтапно, после фиксации контрактов и без потери traceability.

## 2. Sveton

Назначение: хранить бизнес-контекст и исходные материалы проекта.

Остается в `Sveton`:

- стратегия, roadmap, governance, юридические и операционные документы;
- входящие документы, интервью, аудио, исходные PDF/DOCX/MD;
- инвентаризация источников;
- project-specific конфигурация для запуска внешнего semantic engine;
- ссылки на результаты базы знаний и состояние работ.

Не должно разрастаться в `Sveton`:

- универсальные runner-ы semantic extraction;
- универсальные валидаторы atomic statements;
- общий Postgres review workflow;
- reusable UI/API для review;
- продуктовая логика, не завязанная на домен Sveton.

## 3. Semantic Analysis Engine

Назначение: отдельный reusable-продукт для semantic extraction и review workflow.

Вынести в отдельный проект:

- извлечение текста из источников;
- structure-aware chunking;
- atomic statement extraction runner;
- JSON-схемы и validators;
- coverage и quality gates;
- deduplication и clustering;
- review queue / export tooling;
- Postgres import/export contracts;
- универсальные prompt templates;
- конфигурационный слой для разных доменных проектов.

Engine не должен знать бизнес-логику Sveton. Он получает project config и источники, а возвращает machine-readable артефакты.

## 4. Sveton Knowledge Base

Назначение: продуктовая база знаний Sveton, пригодная для ревью, обучения, чек-листов, инструкций и UI.

Содержит:

- canonical atomic statements;
- clusters, relations, source links;
- image links;
- review statuses и safety review;
- editorial sections;
- checklists и training materials;
- экспортные snapshots для Postgres / CRM UI.

База знаний зависит от:

- `Sveton` как источника документов и бизнес-контекста;
- `Semantic Analysis Engine` как инструмента обработки.

База знаний не должна становиться местом разработки engine-кода.

## 5. Контракт между проектами

Минимальный контракт должен быть файловым и машинно-читаемым:

- `project_id`;
- source inventory;
- source document ids;
- extracted text paths;
- chunk ids;
- statement ids;
- image ids;
- cluster ids;
- review statuses;
- downstream statuses;
- source quotes / source spans;
- run manifest;
- tool version / prompt version / schema version.

Рекомендуемый формат для project-specific конфига:

```yaml
project_id: sveton
corpus_id: electricians_knowledge_base
source_inventory: 00_input/documents/electricians_knowledge_base/inventory.md
raw_sources: 00_input/documents/electricians_knowledge_base/raw
extracted_texts: 00_input/documents/electricians_knowledge_base/extracted
chunks: 00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl
statements: 00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl
images: 00_input/documents/electricians_knowledge_base/images/inventory.csv
```

## 6. Миграция

### Phase 0: зафиксировать границы

- Зафиксировать это решение в governance.
- Создать Beans-эпик на разделение.
- Не переносить файлы физически до описания контракта.

### Phase 1: отделить engine от hardcoded путей

- Убрать жесткие пути `00_input/documents/electricians_knowledge_base` из runner-ов.
- Ввести project config.
- Сохранить обратную совместимость для текущего корпуса электриков.
- Проверить, что текущий extraction/review workflow воспроизводится.

### Phase 2: создать отдельный проект `semantic-analysis-engine`

- Перенести generic scripts, schemas, prompt templates и tests.
- Оставить в `Sveton` только project config и данные.
- Зафиксировать версию engine, которой создан текущий canonical слой.

### Phase 3: отделить `sveton-knowledge-base`

- Перенести canonical knowledge, clusters, image links, safety review и editorial sections.
- Оставить в `Sveton` ссылки на published KB и source provenance.
- Настроить export/import в Postgres и CRM UI.

### Phase 4: подключить новые домены

- Прогнать leadership interviews через тот же engine.
- Не смешивать interview corpus с electricians corpus без явного project/corpus id.
- Проверить, что review workflow работает на абзацах и интервью, а не только на bullet-point документах.

## 7. Текущее правило

До физического разделения:

- `Sveton` остается source-of-truth для текущих исходников и текущей базы знаний.
- Новую универсальную логику semantic analysis нужно проектировать так, как будто она будет вынесена.
- Новые scripts не должны добавлять новые hardcoded пути к корпусу электриков без необходимости.
- Любые новые outputs должны сохранять `project_id`, `corpus_id`, `source_document_id`, `chunk_id` и `statement_id`.
