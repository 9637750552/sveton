---
# Sv-a3d
title: Design KB Postgres schema and migrations
status: todo
type: task
created_at: 2026-06-17T11:31:48Z
updated_at: 2026-06-17T11:31:48Z
parent: Sv-ldo
---

Design normalized Postgres schema for projects, corpora, sources, chunks, statements, clusters, images, review tasks, decisions, and audit log.

Checklist:
- [ ] Decide DB ownership and schema namespace.
- [ ] Define `kb_projects`, `kb_corpora`, and `kb_import_runs`.
- [ ] Define source/chunk tables.
- [ ] Define immutable statement tables.
- [ ] Define cluster, relation, and image-link tables.
- [ ] Define review task, decision, event, and proposed rewrite tables.
- [ ] Define indexes for queue filters and source traceability.
- [ ] Write SQL migration draft.
- [ ] Review immutability and audit-log constraints.
- [ ] Document rollback and re-import behavior.
