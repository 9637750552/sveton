# ТЗ: раздел "База знаний" в OmniCRM

Дата: 2026-06-18.

Связанный Beans task в Sveton: `Sv-baj`.

## 1. Назначение

Нужно добавить в `OmniCRM` новый раздел `База знаний`, чтобы инженеры и ответственные сотрудники могли ревьюить семантические утверждения из базы знаний Светон через существующий UI Kit / универсальную смотрелку.

Сейчас база знаний уже подготовлена на стороне проекта `Sveton`:

- исходные документы разобраны на chunks;
- из chunks извлечены atomic semantic statements;
- statements, chunks, sources, clusters, images и связи загружены в Postgres;
- созданы очереди review tasks;
- safety-critical утверждения заблокированы для использования в инструкциях до экспертного ревью.

Задача `OmniCRM` - сделать рабочий интерфейс поверх этих данных.

## 2. Бизнес-сценарий

Инженер или ответственный ревьюер открывает в CRM раздел `База знаний`.

Он видит не Word-документы и не JSON-файлы, а рабочую очередь конкретных утверждений:

- какое утверждение нужно проверить;
- почему оно попало на проверку;
- из какого документа и фрагмента текста оно взято;
- есть ли связанные схемы или изображения;
- можно ли это утверждение использовать в обучении, чек-листе или инструкции;
- что именно решил ревьюер.

Цель MVP - не строить финального smart-assistant. Цель MVP - дать людям нормальный интерфейс для проверки базы утверждений, чтобы дальше эту базу можно было безопасно использовать в обучении, поиске, помощнике и инструкциях.

## 3. Граница ответственности

### Sveton отвечает за

- исходные документы;
- extraction pipeline;
- canonical statements;
- source traceability;
- Postgres schema для KB review layer;
- импорт snapshot-а в Postgres;
- seed review queues;
- export reviewed decisions back to reproducible snapshots.

### OmniCRM отвечает за

- раздел `База знаний` в CRM;
- UI списка задач ревью;
- UI карточки утверждения;
- фильтры, поиск, сортировки;
- действия ревьюера;
- отправку решений в backend;
- права доступа к разделу;
- удобство работы инженеров.

### OmniCRM не отвечает за

- запуск semantic extraction;
- редактирование исходных Word/PDF документов;
- изменение immutable extracted statement text;
- хранение canonical snapshot в файлах;
- самостоятельную перезапись canonical knowledge без export-back процесса.

## 4. Текущий источник данных

Dev Postgres:

- host: `192.168.1.32`;
- database: `sveton_kb_dev`;
- schema: `kb`;
- project: `sveton`;
- corpus: `electricians_knowledge_base`.

Секреты и DSN не хранить в репозитории `Sveton` или `OmniCRM`.

OmniCRM должен получать доступ к данным через свой backend/API. Frontend не должен подключаться к Postgres напрямую.

## 5. Обновление базы новыми утверждениями

`OmniCRM` не импортирует canonical artifacts из репозитория `Sveton`.

Порядок обновления базы знаний такой:

1. В проекте `Sveton` выполняется semantic extraction очередного документа.
2. В `Sveton` обновляются и коммитятся canonical artifacts:
   - `atomic_statements.jsonl`;
   - `statement_clusters.json`;
   - `statement_relations.jsonl`;
   - `statement_images.jsonl`, если есть подтвержденные связи;
   - coverage reports;
   - warnings/errors;
   - batch summary/review notes.
3. В `Sveton` запускается Postgres importer `07_scripts/import_kb_snapshot_to_postgres.py`.
4. В `Sveton` запускается seed review queues `07_scripts/seed_kb_review_tasks.py`.
5. `OmniCRM` через свой backend/API читает уже обновленную Postgres KB и автоматически показывает новые statements/review tasks в разделе `База знаний`.

Граница ответственности:

- `Sveton` добавляет новые canonical statements в Postgres;
- `Sveton` создает/обновляет review tasks;
- `OmniCRM` не читает JSONL/JSON/MD-файлы напрямую;
- `OmniCRM` не создает statement ids и не меняет immutable extracted evidence;
- `OmniCRM` показывает актуальное состояние Postgres и пишет только review decisions/events/proposed rewrites через разрешенный backend workflow.

Для `OmniCRM` это означает: раздел `База знаний` должен быть рассчитан не на один фиксированный snapshot, а на регулярное появление новых statements и review tasks после каждого re-import/re-seed со стороны `Sveton`.

## 6. Текущее состояние данных

Первичный snapshot, уже загруженный в Postgres:

| Entity | Count |
|---|---:|
| `kb.sources` | 17 |
| `kb.chunks` | 146 |
| `kb.statements` | 387 |
| `kb.clusters` | 9 |
| `kb.statement_clusters` | 387 |
| `kb.statement_relations` | 41 |
| `kb.images` | 118 |
| `kb.statement_images` | 182 |
| `kb.review_tasks` | 705 |

Текущий canonical snapshot в репозитории после последующих extraction-батчей содержит около `590` statements. После очередного запуска importer/re-seed в `Sveton` Postgres KB должна получить эти новые statements и новые review tasks. `OmniCRM` должен показывать результат из Postgres после обновления, а не пытаться импортировать файлы самостоятельно.

Очереди ревью:

| Task type | Count |
|---|---:|
| `statement_review_required` | 206 |
| `technical_safety_review` | 204 |
| `instruction_block_review` | 204 |
| `visual_evidence_review` | 86 |
| `source_chunk_review` | 5 |

Критичный пилотный блок:

- `installation_process`;
- cluster: `C009 / Этапы монтажа ИБП`;
- `77` safety-critical statements;
- все `77` должны быть видны в очереди `instruction_block_review`.

## 7. MVP Scope

В первый релиз входит:

- пункт навигации `База знаний`;
- список review tasks;
- фильтры по ключевым полям;
- карточка review task / statement;
- просмотр source quote и chunk context;
- просмотр связанных images;
- просмотр cluster/topic/source;
- отправка review decision;
- создание proposed rewrite, если формулировку надо переписать;
- история решений по statement.

В первый релиз не входит:

- генерация финальных инструкций;
- smart assistant / chatbot;
- полнотекстовый RAG-поиск по всей базе;
- массовое редактирование statements;
- экспорт решений обратно в файлы;
- запуск новых extraction runs.

## 8. Навигация

Добавить раздел:

- label: `База знаний`;
- рекомендуемая позиция: рядом с рабочими операционными разделами, не в настройках;
- первый экран: `Очередь ревью`;
- будущие вкладки: `Утверждения`, `Кластеры`, `Источники`, `Отчеты`.

Для MVP достаточно одной страницы с вкладками:

- `Очередь`;
- `Утверждение`;
- `Источник`;
- `История`.

Если текущая универсальная смотрелка уже работает как list/detail layout, использовать ее.

## 9. Основной экран: очередь ревью

Список должен показывать review tasks из `kb.review_tasks`.

Минимальные колонки:

| UI field | Source |
|---|---|
| Priority | `review_tasks.priority` |
| Task type | `review_tasks.task_type` |
| Status | `review_tasks.status` |
| Reason | `review_tasks.reason` |
| Topic | `statements.topic` or `chunks.topic` |
| Risk | `statements.risk_level` |
| Review status | `statements.review_status` |
| Downstream status | `statements.downstream_status` |
| Statement preview | `statements.statement_text` |
| Source file | `statements.source_file` or `chunks.source_file` |
| Chunk id | `statements.source_chunk_id` or `chunks.chunk_id` |
| Has images | derived from `statement_images` / `statements.related_image_ids` |

Сортировка по умолчанию:

1. `priority`: `critical`, `high`, `normal`, `low`, `deferred`;
2. `task_type`: `instruction_block_review`, `technical_safety_review`, `statement_review_required`, `visual_evidence_review`, `source_chunk_review`;
3. newest task first or stable by `review_tasks.id`.

## 10. Фильтры очереди

Обязательные фильтры:

- project;
- corpus;
- task type;
- task status;
- priority;
- topic;
- cluster;
- source file;
- risk level;
- review status;
- downstream status;
- has images;
- safety-critical only;
- blocked-for-instruction only.

Быстрые preset-фильтры:

- `Все задачи`;
- `Критичные`;
- `Заблокировано для инструкций`;
- `Этапы монтажа: 77`;
- `Требует visual review`;
- `Проблемы источника`.

## 11. Карточка утверждения

При открытии задачи пользователь должен видеть одну рабочую карточку.

Блок `Задача`:

- task id;
- task type;
- priority;
- status;
- reason;
- created_at;
- metadata.

Блок `Утверждение`:

- statement id;
- statement text;
- statement type;
- topic;
- roles;
- risk level;
- review status;
- downstream status;
- visual review required;
- confidence.

Блок `Источник`:

- source file;
- source document id;
- source chunk id;
- section path;
- source quote;
- full chunk text;
- previous context;
- next context.

Блок `Кластер`:

- cluster id;
- cluster title;
- cluster topic;
- other statements in cluster, at least ids and short previews.

Блок `Изображения`:

- image id;
- thumbnail or link;
- link type;
- review status;
- notes/rationale;
- source file;
- caption;
- nearby text.

Блок `История`:

- existing review decisions;
- proposed rewrites;
- review events.

## 12. Reviewer Actions

В карточке должны быть действия:

| Action | Meaning |
|---|---|
| `approve_for_training` | Можно использовать в обучающих материалах. |
| `approve_for_checklist` | Можно использовать в чек-листах. |
| `approve_for_instruction` | Можно использовать в финальной инструкции. |
| `block_for_instruction` | Нельзя использовать в инструкции. |
| `needs_rewrite` | Смысл полезен, но формулировку надо переписать. |
| `requires_manufacturer_docs` | Нужна сверка с документацией производителя. |
| `ask_engineer` | Нужен вопрос инженеру/эксперту. |
| `mark_duplicate` | Дублирует другое утверждение. |
| `mark_conflict` | Конфликтует с другим утверждением или источником. |
| `reject` | Не использовать как знание. |

Для всех действий обязателен комментарий ревьюера, кроме простого `approve_for_training`, где комментарий можно сделать optional.

Для `needs_rewrite` нужно поле `proposed_statement_text`.

Для `mark_duplicate` и `mark_conflict` желательно поле `related_statement_id`.

## 13. Decision Payload

Рекомендуемый payload от frontend к backend:

```json
{
  "reviewTaskId": 123,
  "statementId": 456,
  "decisionAction": "approve_for_instruction",
  "downstreamStatus": "approved_for_instruction",
  "reviewer": "user-id-or-email",
  "reviewComment": "Проверено инженером. Формулировка применима для инструкции.",
  "proposedStatementText": null,
  "metadata": {
    "relatedStatementId": null,
    "uiSource": "omnicrm_knowledge_base",
    "clientVersion": "mvp"
  }
}
```

Backend должен:

- записать строку в `kb.review_decisions`;
- записать событие в `kb.review_events`;
- обновить `kb.review_tasks.status`;
- при необходимости обновить `kb.statements.downstream_status`;
- при `needs_rewrite` создать запись в `kb.proposed_rewrites`.

Нельзя обновлять:

- `kb.statements.statement_text`;
- `kb.statements.source_quote`;
- `kb.statements.source_chunk_id`;
- `kb.statements.source_document_id`;
- `kb.statements.source_file`.

Эти поля защищены как immutable extracted evidence.

## 14. Recommended API Endpoints

Финальный стиль endpoint-ов должен соответствовать паттернам `OmniCRM`.

Минимальный API contract:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/knowledge-base/review-tasks` | List review queue with filters. |
| `GET` | `/api/knowledge-base/review-tasks/:id` | Full task detail. |
| `GET` | `/api/knowledge-base/statements/:id` | Statement detail without task context. |
| `GET` | `/api/knowledge-base/clusters/:id` | Cluster detail. |
| `GET` | `/api/knowledge-base/sources/:id` | Source/chunk context. |
| `POST` | `/api/knowledge-base/review-decisions` | Submit reviewer decision. |
| `POST` | `/api/knowledge-base/review-tasks/:id/status` | Move task to `in_review`, `blocked`, or similar operational status. |

For MVP можно сделать только:

- list review tasks;
- get review task detail;
- submit review decision.

## 15. Recommended Read Model Shape

Queue item DTO:

```json
{
  "taskId": 1,
  "taskType": "instruction_block_review",
  "status": "todo",
  "priority": "critical",
  "reason": "blocked_for_instruction_until_expert_review",
  "statement": {
    "id": 10,
    "statementId": "doc_015_chunk_0016_stmt_002",
    "text": "Ни при каких обстоятельствах нельзя допускать соединения или замыкания входа и выхода.",
    "topic": "installation_process",
    "riskLevel": "safety_critical",
    "reviewStatus": "review_required",
    "downstreamStatus": "blocked_for_instruction"
  },
  "source": {
    "sourceFile": "ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx",
    "chunkId": "doc_015_chunk_0016"
  },
  "cluster": {
    "clusterId": "C009",
    "title": "Этапы монтажа ИБП"
  },
  "hasImages": false,
  "createdAt": "2026-06-18T00:00:00Z"
}
```

Task detail DTO:

```json
{
  "task": {},
  "statement": {},
  "source": {
    "quote": "",
    "chunkText": "",
    "previousContext": "",
    "nextContext": ""
  },
  "cluster": {},
  "images": [],
  "relations": [],
  "reviewHistory": [],
  "proposedRewrites": []
}
```

## 16. Permissions

Минимальные роли:

| Role | Access |
|---|---|
| `kb.viewer` | Can read queue and statement details. |
| `kb.reviewer` | Can take tasks and submit decisions. |
| `kb.engineer_reviewer` | Can approve safety-critical technical statements. |
| `kb.admin` | Can see all tasks and manage statuses. |

Для MVP можно начать с одной роли `kb.reviewer`, если в `OmniCRM` пока нет granular permissions.

Safety-critical approval rule:

- `approve_for_instruction` for `safety_critical` statements should be allowed only to `kb.engineer_reviewer` or `kb.admin`.

## 17. UI Kit Expectations

Использовать существующие паттерны `OmniCRM`:

- list/detail layout;
- table/list with filters;
- right-side or full-page detail panel;
- status badges;
- priority badges;
- action buttons;
- tabs inside detail panel;
- modal for decision submission;
- image preview component if already exists.

Не делать отдельный визуальный стиль. Раздел должен выглядеть как рабочий CRM-инструмент, а не как лендинг или справочник.

## 18. Error And Conflict Handling

Frontend должен показывать понятные ошибки:

- task already closed;
- statement immutable field cannot be changed;
- reviewer has no permission for selected action;
- proposed rewrite required but missing;
- related statement id not found;
- database/API unavailable.

Backend должен защищать от двойной отправки:

- review decision может быть append-only;
- task status должен обновляться предсказуемо;
- повторная отправка той же формы не должна создавать конфликтные статусы.

## 19. MVP Acceptance Criteria

MVP считается готовым, если:

- в `OmniCRM` есть раздел `База знаний`;
- пользователь видит актуальный список review tasks из dev DB;
- после re-import/re-seed в `Sveton` новые statements и review tasks появляются в `OmniCRM` без чтения файлов репозитория;
- preset `Этапы монтажа: 77` показывает ровно 77 blocked installation-process statements;
- карточка statement показывает statement text, source quote, chunk context, source file и cluster;
- visual review tasks показывают связанные images;
- reviewer может отправить хотя бы решения `approve_for_training`, `block_for_instruction`, `needs_rewrite`, `requires_manufacturer_docs`;
- решение записывается в `kb.review_decisions`;
- событие записывается в `kb.review_events`;
- task status меняется после решения;
- immutable extracted fields не меняются;
- UI не требует открытия файлов из репозитория `Sveton`.

## 20. Suggested OmniCRM Tasks

После утверждения этого ТЗ в проекте `OmniCRM` нужно создать отдельные задачи:

1. Add `База знаний` navigation entry.
2. Add backend connection/config for `sveton_kb_dev` without committed secrets.
3. Implement review task list endpoint.
4. Implement review task detail endpoint.
5. Implement review decision submit endpoint.
6. Build review queue UI using existing universal viewer / UI Kit.
7. Build statement detail panel.
8. Build decision modal and validation.
9. Add permissions for KB reviewer roles.
10. Run pilot on `installation_process` 77-statement block.
11. Verify that newly imported Sveton statements appear in the KB UI after re-import/re-seed without OmniCRM-side file import.

## 21. Open Questions For OmniCRM Project

Before implementation, confirm:

- exact name and location of the existing universal viewer component;
- current OmniCRM permission model;
- whether OmniCRM backend can connect to `sveton_kb_dev` directly or needs a separate API boundary;
- how users/reviewers are identified in review decisions;
- whether images should be served from file paths, static storage, or a backend file endpoint;
- whether the MVP should write directly into `kb.review_decisions` or through an internal service layer.

## 22. References

- [EPIC_POSTGRES_KB_REVIEW_LAYER.md](EPIC_POSTGRES_KB_REVIEW_LAYER.md)
- [IMPORT_CONTRACT.md](IMPORT_CONTRACT.md)
- [REVIEW_WORKFLOW.md](REVIEW_WORKFLOW.md)
- [2026-06-18_current_snapshot_import.md](import_reports/2026-06-18_current_snapshot_import.md)
- [2026-06-18_review_queue_seed.md](import_reports/2026-06-18_review_queue_seed.md)
