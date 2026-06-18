---
# Sv-baj
title: Plan OmniCRM Knowledge Base viewer integration
status: in-progress
type: task
priority: normal
created_at: 2026-06-17T11:31:49Z
updated_at: 2026-06-18T20:55:15Z
parent: Sv-ldo
---

Specify how OmniCRM universal viewer opens Knowledge Base queues and submits review decisions through API/Postgres.

Checklist:
- [ ] Inspect OmniCRM universal viewer contract.
- [x] Decide whether OmniCRM reads Postgres directly or through API.
- [x] Confirm OmniCRM owns only the reviewer UI, not canonical storage or extraction pipeline.
- [x] Define `База знаний` navigation entry.
- [x] Map KB queue columns to viewer list fields.
- [x] Map statement detail to viewer detail panel.
- [x] Define review actions and permissions.
- [x] Define submit decision payload.
- [x] Define error and conflict handling.
- [ ] Create OmniCRM-side Beans tasks after contract approval.
- [ ] Confirm pilot UI scope before implementation.

## Handoff Draft

Created 01_docs/operations/postgres_knowledge_base_review/OMNICRM_HANDOFF_TZ.md as the transfer specification for the OmniCRM Knowledge Base viewer. Remaining open items require work inside the OmniCRM repository: inspect the actual universal viewer contract, create OmniCRM-side Beans tasks, and confirm the pilot UI scope before implementation.
