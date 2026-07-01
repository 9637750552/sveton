---
# Sv-gha
title: Clean PDF artifacts for doc_014 and doc_017
status: completed
type: task
priority: normal
created_at: 2026-07-01T14:36:33Z
updated_at: 2026-07-01T14:38:34Z
---

Remove obsolete PDF-derived extraction artifacts for doc_014/doc_017 after DOCX sources were added.\n\n- [x] Update source inventory to DOCX-only working sources\n- [x] Remove PDF source chunks and chunk summary rows\n- [x] Remove PDF page image inventory rows and files\n- [x] Remove obsolete PDF raw/extracted files\n- [x] Verify no stale doc_014/doc_017 PDF references remain

## Summary of Changes\n\nRemoved obsolete PDF raw files, PDF text extraction files, PDF page-render images, and stale chunk/image inventory entries for doc_014/doc_017. Updated source inventory to treat the DOCX files as the only active working sources pending fresh extraction.
