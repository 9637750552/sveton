---
# Sv-6y0
title: Normalize business interview export language
status: completed
type: task
priority: normal
created_at: 2026-07-03T16:17:07Z
updated_at: 2026-07-03T16:23:39Z
parent: Sv-3tw
---

Cleanup pass for Phase 9 business-interview exports: translate visible English headings, service labels, and review notes to Russian while preserving claim IDs, cluster IDs, review semantics, and source traceability.

Checklist:
- [x] Normalize headings and labels in export markdown files.
- [x] Translate visible review/status notes where they were reader-facing prose.
- [x] Validate claim and cluster references after edits.
- [x] Run beans check.
- [x] Record summary.

Summary:
- Updated all 9 files in 00_input/interviews/exports/.
- Kept machine identifiers and stable abbreviations such as BIC, CRM, MVP, SMB, claim_id, and file paths where appropriate.
- Validation result: missing claim refs = 0; missing cluster refs = 0.
