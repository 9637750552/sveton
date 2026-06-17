# Epic: Postgres Knowledge Base Review Layer

Дата создания: 2026-06-17.

Beans epic: `Sv-ldo`.

## 1. Цель

Создать operational layer в Postgres для текущей и будущей базы знаний:

- импортировать существующие semantic extraction artifacts;
- дать инженерам и ревьюерам рабочую среду для просмотра и правок;
- сохранить исходный canonical слой как immutable source-backed snapshot;
- подключить будущую UI-смотрелку через read models / API;
- экспортировать решения ревью обратно в воспроизводимые snapshots.

Postgres не заменяет файлы сразу. На первом этапе файлы остаются source-of-truth, а Postgres становится рабочей базой для review workflow.

## 2. Scope

Входит:

- schema design;
- migrations;
- importer из текущих JSONL/CSV/JSON/MD artifacts;
- review queue;
- review decisions;
- audit log;
- read models для UI;
- export reviewed snapshots back to repository.

Не входит в первый этап:

- немедленный физический перенос `sveton-knowledge-base` в отдельный repo;
- массовое продолжение extraction по новым документам;
- production UI до проверки схемы на текущих 387 statements;
- перезапись canonical statements в Postgres без сохранения оригинала.

## 3. Current Input Snapshot

Текущий импортируемый корпус:

- `project_id`: `sveton`;
- `corpus_id`: `electricians_knowledge_base`;
- config: `semantic_project.yml`;
- chunks: `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`;
- statements: `00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl`;
- clusters: `statement_clusters.json`;
- relations: `statement_relations.jsonl`;
- image inventory: `images/inventory.csv`;
- statement-image links: `statement_images.jsonl`;
- review docs: `statements/review/`, safety review docs, coverage reports.

Known current scale:

- `387` atomic statements;
- `146` chunks;
- `17` source files;
- `204` safety-critical statements;
- `206` statements requiring review;
- `77` installation process safety-critical statements blocked for instruction.

## 4. Data Model Draft

Core tables:

- `kb_projects`;
- `kb_corpora`;
- `kb_import_runs`;
- `kb_sources`;
- `kb_chunks`;
- `kb_images`;
- `kb_statements`;
- `kb_clusters`;
- `kb_statement_clusters`;
- `kb_statement_relations`;
- `kb_statement_images`;
- `kb_review_tasks`;
- `kb_review_decisions`;
- `kb_review_events`;
- `kb_proposed_rewrites`.

Important rule:

`kb_statements.statement_text` imported from extraction is immutable. Human changes go to review decisions or proposed rewrites, not into the original statement row.

## 5. Review Status Model

Canonical extraction status:

- `extracted`;
- `review_required`;
- `rejected`.

Operational review task status:

- `todo`;
- `in_review`;
- `blocked`;
- `approved`;
- `needs_rewrite`;
- `requires_manufacturer_docs`;
- `done`.

Downstream status:

- `draft`;
- `approved_for_training`;
- `approved_for_checklist`;
- `approved_for_instruction`;
- `blocked_for_instruction`;

Review decision actions:

- `approve_for_training`;
- `approve_for_checklist`;
- `approve_for_instruction`;
- `block_for_instruction`;
- `needs_rewrite`;
- `requires_manufacturer_docs`;
- `ask_engineer`;
- `mark_duplicate`;
- `mark_conflict`;
- `reject`.

## 6. Import Pipeline

Importer steps:

1. Read `semantic_project.yml`.
2. Create or update `kb_projects` and `kb_corpora`.
3. Create `kb_import_runs` with source paths, schema version, engine version, git commit, and timestamp.
4. Import source inventory into `kb_sources`.
5. Import `source_chunks.jsonl` into `kb_chunks`.
6. Import image inventory into `kb_images`.
7. Import `atomic_statements.jsonl` into immutable `kb_statements`.
8. Import clusters and statement-cluster links.
9. Import statement relations.
10. Import statement-image links.
11. Seed review tasks from risk/review/downstream statuses.
12. Produce import summary and discrepancy report.

Importer must be idempotent by natural keys:

- `project_id`;
- `corpus_id`;
- `source_document_id`;
- `chunk_id`;
- `statement_id`;
- `image_id`;
- `cluster_id`;
- `import_run_id`.

## 7. Read Models / API Contract

Minimum UI views:

- statement review queue;
- statement detail;
- source chunk detail;
- source document detail;
- cluster detail;
- image detail;
- review history;
- review summary dashboard.

Minimum filters:

- project;
- corpus;
- topic;
- cluster;
- source file;
- risk level;
- review status;
- downstream status;
- has images;
- has conflict;
- safety-critical only;
- uncovered / coverage issue.

Statement detail must expose:

- statement id;
- extracted statement text;
- source quote;
- chunk context;
- source file;
- section path;
- risk level;
- topic;
- roles;
- cluster;
- related statements;
- linked images;
- current review task;
- decision history;
- proposed rewrite if any.

## 8. OmniCRM Viewer Integration

OmniCRM should not read repository files directly.

Target integration:

- OmniCRM adds a `База знаний` section;
- viewer consumes API/read models backed by Postgres;
- reviewer actions write review decisions/events;
- canonical extraction rows remain immutable;
- every decision is auditable.

First UI pilot:

- corpus: `electricians_knowledge_base`;
- topic: `installation_process`;
- risk: `safety_critical`;
- known block: 77 statements currently blocked for instruction.

## 9. Export Back To Snapshots

Postgres decisions must be exportable back to file artifacts:

- review decisions JSONL;
- reviewed statements snapshot;
- downstream approved snapshot;
- blocked statements report;
- proposed rewrites JSONL;
- audit summary.

Export snapshots must include:

- export timestamp;
- DB schema version;
- import run id;
- source git commit;
- reviewer decisions;
- changed statuses;
- unresolved items.

## 10. Beans Work Breakdown

Epic:

- `Sv-ldo`: Build Postgres knowledge base review layer.

Tasks:

- `Sv-a3d`: Design KB Postgres schema and migrations.
- `Sv-yzh`: Define extraction artifact import contract.
- `Sv-7sd`: Implement importer for current Sveton extraction snapshot.
- `Sv-dhj`: Seed review queues and status model.
- `Sv-c7a`: Create KB read models and API contract.
- `Sv-baj`: Plan OmniCRM Knowledge Base viewer integration.
- `Sv-uw4`: Export reviewed decisions back to reproducible snapshots.
- `Sv-mys`: Run pilot review on installation process statements.

## 11. Recommended Development Order

1. `Sv-a3d`: schema first.
2. `Sv-yzh`: exact artifact mapping.
3. `Sv-7sd`: importer and dry-run summary.
4. `Sv-dhj`: review queues.
5. `Sv-c7a`: read models/API.
6. `Sv-baj`: OmniCRM integration plan.
7. `Sv-uw4`: export snapshots.
8. `Sv-mys`: pilot review on installation process.

## 12. Definition Of Done

The epic is done when:

- current extraction snapshot is imported into Postgres;
- import is reproducible from repository files;
- original statements are immutable;
- reviewer decisions are append-only/auditable;
- UI/API can list and inspect review queue items;
- review decisions can be exported back to repository snapshots;
- installation process pilot has been reviewed through the new workflow.
