# Postgres KB Review DB Decision

Дата: 2026-06-17.

Beans task: `Sv-a3d`.

## Decision

Use the existing home Postgres instance, but keep the knowledge-base review layer isolated from OmniCRM data.

Development database:

- database: `sveton_kb_dev`;
- schema: `kb`;
- migration table: `kb.schema_migrations`;
- migration location: `01_docs/operations/postgres_knowledge_base_review/migrations/`;
- initial migration: `001_create_kb_review_schema.sql`.

## Ownership

For the initial development migration, database ownership stays with the Postgres admin role used through the server access procedure.

Application/reviewer roles and credentials are not created in this task. They must be added later when the API/UI integration path is approved, using environment variables or server-side secret storage only.

## Boundary

OmniCRM will use this DB/schema through API/read models for the `База знаний` reviewer UI.

OmniCRM does not own:

- raw source documents;
- extraction runner;
- canonical file snapshots;
- immutable extracted statement rows;
- export-back workflow.

## Rollback / Re-Import

Importer tasks must be idempotent by natural keys:

- `project_id`;
- `corpus_id`;
- `source_document_id`;
- `chunk_id`;
- `statement_id`;
- `image_id`;
- `cluster_id`;
- `import_run_id`.

The first migration creates empty structure only. It does not import extraction data.

## Applied Status

Status on 2026-06-17:

- database `sveton_kb_dev` created;
- schema `kb` created;
- migration `001_create_kb_review_schema` applied;
- `16` tables visible in schema `kb`;
- migration marker written to `kb.schema_migrations`;
- extraction data not imported yet.
