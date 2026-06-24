---
# Sv-yzh
title: Define extraction artifact import contract
status: completed
type: task
priority: normal
created_at: 2026-06-17T11:31:48Z
updated_at: 2026-06-17T21:54:44Z
parent: Sv-ldo
---

Define how current JSONL, CSV, JSON, and Markdown artifacts map into Postgres without losing source traceability.

Checklist:
- [x] Inventory current artifacts from `semantic_project.yml`.
- [x] Map `source_chunks.jsonl` fields to `kb.chunks`.
- [x] Map `atomic_statements.jsonl` fields to `kb.statements`.
- [x] Map image inventory CSV to `kb.images`.
- [x] Map `statement_images.jsonl` to `kb.statement_images`.
- [x] Map `statement_clusters.json` to cluster tables.
- [x] Map `statement_relations.jsonl` to relation tables.
- [x] Decide which Markdown review reports import as metadata and which stay file-only.
- [x] Define required `import_run` metadata.
- [x] Define discrepancy report format for missing or invalid links.

## Summary of Changes

Created `01_docs/operations/postgres_knowledge_base_review/IMPORT_CONTRACT.md` with the artifact-to-Postgres mapping for the current electricians knowledge-base snapshot.

The contract defines import scope, file sources of truth, import order, natural keys, table mappings, validation rules, import run metadata, and discrepancy report format for `Sv-7sd`.
