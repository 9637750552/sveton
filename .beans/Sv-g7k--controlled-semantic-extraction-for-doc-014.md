---
# Sv-g7k
title: Controlled semantic extraction for doc_014
status: completed
type: task
priority: normal
created_at: 2026-07-01T16:58:33Z
updated_at: 2026-07-01T17:12:19Z
---

Controlled DOCX-based extraction for doc_014 with dedupe against doc_015/C009.

- [x] Read preflight and canonical context
- [x] Build DOCX-based extracted text/chunks for doc_014 only
- [x] Add unique source-backed doc_014 statements with dedupe controls
- [x] Update coverage, warnings/errors, and summary artifacts
- [x] Validate JSON/JSONL and safety/source constraints

## Summary of Changes

- Added 22 DOCX-backed canonical statements for doc_014 in C009.
- Marked all 22 doc_014 statements review_required; 14 are safety_critical.
- Added dedupe/manual-review coverage overrides and warnings instead of promoting duplicate or image-only facts.
- Left statement_images and extraction_errors unchanged for doc_014.
