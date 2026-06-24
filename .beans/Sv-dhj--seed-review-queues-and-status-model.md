---
# Sv-dhj
title: Seed review queues and status model
status: completed
type: task
priority: normal
created_at: 2026-06-17T11:31:49Z
updated_at: 2026-06-17T22:13:51Z
parent: Sv-ldo
---

Create review tasks for safety critical, review required, blocked, uncovered, and disputed semantic statements.

Checklist:
- [x] Define review task types.
- [x] Define review statuses and transitions.
- [x] Seed tasks for `review_required`.
- [x] Seed tasks for `safety_critical`.
- [x] Seed tasks for `blocked_for_instruction`.
- [x] Seed tasks for coverage/discrepancy issues.
- [x] Prevent duplicate open review tasks for the same statement and reason.
- [x] Add queue priority rules.
- [x] Validate current expected queues, including 77 installation process statements.
- [x] Document reviewer workflow rules.

## Summary of Changes

Added `07_scripts/seed_kb_review_tasks.py` to seed operational review queues in Postgres without committing secrets.

Documented the review workflow in `01_docs/operations/postgres_knowledge_base_review/REVIEW_WORKFLOW.md`.

Seeded `705` review tasks in `sveton_kb_dev.kb`: `206` extraction review tasks, `204` safety review tasks, `204` instruction-block tasks, `86` visual review tasks, and `5` source chunk review tasks.

Set `204` safety-critical review-required statements to `downstream_status = blocked_for_instruction`, including the expected `77` `installation_process` statements.
