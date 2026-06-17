---
# Sv-baj
title: Plan OmniCRM Knowledge Base viewer integration
status: todo
type: task
created_at: 2026-06-17T11:31:49Z
updated_at: 2026-06-17T11:31:49Z
parent: Sv-ldo
---

Specify how OmniCRM universal viewer opens Knowledge Base queues and submits review decisions through API/Postgres.

Checklist:
- [ ] Inspect OmniCRM universal viewer contract.
- [ ] Decide whether OmniCRM reads Postgres directly or through API.
- [ ] Confirm OmniCRM owns only the reviewer UI, not canonical storage or extraction pipeline.
- [ ] Define `База знаний` navigation entry.
- [ ] Map KB queue columns to viewer list fields.
- [ ] Map statement detail to viewer detail panel.
- [ ] Define review actions and permissions.
- [ ] Define submit decision payload.
- [ ] Define error and conflict handling.
- [ ] Create OmniCRM-side Beans tasks after contract approval.
- [ ] Confirm pilot UI scope before implementation.
