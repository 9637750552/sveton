---
# Sv-ldo
title: Build Postgres knowledge base review layer
status: in-progress
type: epic
created_at: 2026-06-17T11:31:33Z
updated_at: 2026-06-17T11:31:33Z
---

Plan and implement a Postgres-backed operational layer for importing existing semantic extraction artifacts, reviewing statements, and serving the future Knowledge Base UI.

Planning document:

- `01_docs/operations/postgres_knowledge_base_review/EPIC_POSTGRES_KB_REVIEW_LAYER.md`

Child tasks:

- `Sv-a3d`: Design KB Postgres schema and migrations.
- `Sv-yzh`: Define extraction artifact import contract.
- `Sv-7sd`: Implement importer for current Sveton extraction snapshot.
- `Sv-dhj`: Seed review queues and status model.
- `Sv-c7a`: Create KB read models and API contract.
- `Sv-baj`: Plan OmniCRM Knowledge Base viewer integration.
- `Sv-uw4`: Export reviewed decisions back to reproducible snapshots.
- `Sv-mys`: Run pilot review on installation process statements.

Epic checklist:

- [x] Create detailed implementation plan.
- [x] Create child Beans tasks.
- [ ] Approve schema and migration approach.
- [ ] Create dev Postgres DB/schema in `Sv-a3d`.
- [ ] Import current extraction snapshot into Postgres.
- [ ] Enable reviewer queue workflow.
- [ ] Validate pilot review on installation process statements.
- [ ] Export reviewed decisions back to repository snapshots.
