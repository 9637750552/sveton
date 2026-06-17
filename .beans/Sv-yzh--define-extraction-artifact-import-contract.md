---
# Sv-yzh
title: Define extraction artifact import contract
status: todo
type: task
created_at: 2026-06-17T11:31:48Z
updated_at: 2026-06-17T11:31:48Z
parent: Sv-ldo
---

Define how current JSONL, CSV, JSON, and Markdown artifacts map into Postgres without losing source traceability.

Checklist:
- [ ] Inventory current artifacts from `semantic_project.yml`.
- [ ] Map `source_chunks.jsonl` fields to `kb_chunks`.
- [ ] Map `atomic_statements.jsonl` fields to `kb_statements`.
- [ ] Map image inventory CSV to `kb_images`.
- [ ] Map `statement_images.jsonl` to `kb_statement_images`.
- [ ] Map `statement_clusters.json` to cluster tables.
- [ ] Map `statement_relations.jsonl` to relation tables.
- [ ] Decide which Markdown review reports import as metadata and which stay file-only.
- [ ] Define required `import_run` metadata.
- [ ] Define discrepancy report format for missing or invalid links.
