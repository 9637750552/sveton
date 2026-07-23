---
# Sv-wcz
title: Lock one-page print settings for contract workbook
status: completed
type: task
priority: normal
created_at: 2026-07-20T15:26:33Z
updated_at: 2026-07-20T15:30:20Z
---

Ensure all contract workbook sheets except the portrait checklist keep one-page print settings after future rebuilds.

- [x] Inspect current workbook print settings
- [x] Patch workbook builders to restore print settings after export
- [x] Apply print settings to current workbook
- [x] Verify non-portrait sheets fit one page

## Summary of Changes

Added one-page print settings for request, report, checklist, and equipment selection sheets; kept the portrait checklist as its separate portrait layout; wired the print-settings fixer into the active workbook builders; verified print areas and rendered previews.
