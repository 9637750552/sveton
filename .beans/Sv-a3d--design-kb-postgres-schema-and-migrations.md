---
# Sv-a3d
title: Design KB Postgres schema and migrations
status: completed
type: task
priority: normal
created_at: 2026-06-17T11:31:48Z
updated_at: 2026-06-17T20:53:30Z
parent: Sv-ldo
---

Design normalized Postgres schema for projects, corpora, sources, chunks, statements, clusters, images, review tasks, decisions, and audit log.

Checklist:
- [x] Decide DB ownership and schema namespace.
- [x] Decide whether KB uses a separate database or a separate schema in an existing Postgres instance.
- [x] Decide DB/schema/user names without committing secrets.
- [x] Define `kb_projects`, `kb_corpora`, and `kb_import_runs`.
- [x] Define source/chunk tables.
- [x] Define immutable statement tables.
- [x] Define cluster, relation, and image-link tables.
- [x] Define review task, decision, event, and proposed rewrite tables.
- [x] Define indexes for queue filters and source traceability.
- [x] Write SQL migration draft.
- [x] Create dev Postgres DB/schema.
- [x] Apply migration `001` to the dev DB/schema.
- [x] Verify DB connectivity and table visibility.
- [x] Review immutability and audit-log constraints.
- [x] Document rollback and re-import behavior.

## Summary of Changes

Created migration `001_create_kb_review_schema.sql` and applied it to dev database `sveton_kb_dev`, schema `kb`.

The first migration creates projects, corpora, import runs, sources, chunks, images, immutable statements, clusters, relations, statement-image links, review tasks, review decisions, review events, proposed rewrites, indexes, migration marker table, and immutability/audit triggers.

Verification:

- `16` tables visible in schema `kb`.
- `kb.schema_migrations` contains `001_create_kb_review_schema`.
- No extraction data imported yet.
