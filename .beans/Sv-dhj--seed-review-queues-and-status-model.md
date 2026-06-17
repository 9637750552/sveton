---
# Sv-dhj
title: Seed review queues and status model
status: todo
type: task
created_at: 2026-06-17T11:31:49Z
updated_at: 2026-06-17T11:31:49Z
parent: Sv-ldo
---

Create review tasks for safety critical, review required, blocked, uncovered, and disputed semantic statements.

Checklist:
- [ ] Define review task types.
- [ ] Define review statuses and transitions.
- [ ] Seed tasks for `review_required`.
- [ ] Seed tasks for `safety_critical`.
- [ ] Seed tasks for `blocked_for_instruction`.
- [ ] Seed tasks for coverage/discrepancy issues.
- [ ] Prevent duplicate open review tasks for the same statement and reason.
- [ ] Add queue priority rules.
- [ ] Validate current expected queues, including 77 installation process statements.
- [ ] Document reviewer workflow rules.
