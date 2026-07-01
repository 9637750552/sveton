---
# Sv-073
title: Re-import 619 KB snapshot into Postgres
status: completed
type: task
priority: normal
created_at: 2026-07-01T20:34:00Z
updated_at: 2026-07-01T20:43:47Z
parent: Sv-ldo
---

Load the current 619-statement electricians KB snapshot with doc_017 review-gated statements and visual review candidates into sveton_kb_dev, migrate new images to OmniCRM/Nextcloud media layer, and re-seed review queues.

- [x] Run and verify importer dry-run
- [x] Apply snapshot import to Postgres
- [x] Re-seed review tasks and verify idempotency
- [x] Verify DB counts for 619 snapshot and doc_017 review gating
- [x] Migrate doc_017 images to Nextcloud media assets
- [x] Backfill managed statement media links
- [x] Create import report
- [x] Commit and push report

## Summary of Changes

Re-imported the current 619-statement electricians KB snapshot into `sveton_kb_dev.kb`.
Import run key: `electricians_knowledge_base_b36d6a5c25dd`.
Postgres now contains 619 statements, 158 chunks, 117 images, 150 statement relations, 236 statement-image links, and 1218 review tasks.
`doc_017` contributes 7 review-gated statements, 7 visual review candidate links, 7 managed media links, and 28 review tasks.
The `doc_017` schemes were migrated to OmniCRM/Nextcloud as `legacy_instruction_normalized`.
