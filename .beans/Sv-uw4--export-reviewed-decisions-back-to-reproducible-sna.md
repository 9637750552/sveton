---
# Sv-uw4
title: Export reviewed decisions back to reproducible snapshots
status: todo
type: task
created_at: 2026-06-17T11:31:49Z
updated_at: 2026-06-17T11:31:49Z
parent: Sv-ldo
---

Define and implement export from Postgres review decisions back to file snapshots for repository traceability.

Checklist:
- [ ] Define export artifact names and target folder.
- [ ] Export review decisions JSONL.
- [ ] Export proposed rewrites JSONL.
- [ ] Export downstream status snapshot.
- [ ] Export blocked statements report.
- [ ] Include import run id, DB schema version, source git commit, and export timestamp.
- [ ] Make export deterministic for diff review.
- [ ] Validate export against current repository rules.
- [ ] Document when snapshots should be committed.
- [ ] Add smoke test for export round trip.
