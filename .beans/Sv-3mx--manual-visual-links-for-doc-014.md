---
# Sv-3mx
title: Manual visual links for doc_014
status: completed
type: task
created_at: 2026-07-01T18:03:45Z
updated_at: 2026-07-01T18:11:23Z
---

Manual visual-link pass for doc_014 DOCX before Postgres import.

- [x] Verify clean baseline and canonical counts
- [x] Read preflight, extraction summary, and visual methodology
- [x] Prepare DOCX visual candidates without restoring PDF artifacts
- [x] Add only accepted visual links and review notes
- [x] Validate JSONL/source constraints and summarize status

## Summary of Changes

- Added 10 selected DOCX embedded images for `doc_014` to image inventory and raw/normalized image folders.
- Added 16 accepted `statement_images.jsonl` links for existing text-backed `doc_014` statements.
- Left image-only facts and ambiguous schemes in manual review notes.
- Confirmed canonical statement count remains 612 and `doc_017` was not touched.
