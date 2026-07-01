---
# Sv-npp
title: Add doc_017 review visual layer links
status: completed
type: task
priority: normal
created_at: 2026-07-01T20:17:41Z
updated_at: 2026-07-01T20:19:19Z
---

## Checklist

- [x] Inspect statement_images schema
- [x] Add 7 doc_017 review-required visual links
- [x] Update summaries and batch report
- [x] Validate statement-image integrity and no accepted misuse

## Summary of Changes

- Added 7 doc_017 statement_images links with link_type=visual_review_candidate and status=review_required.
- Kept them out of accepted visual evidence; all links are low-confidence review artifacts.
- Updated batch summary, review markdown, and coverage README wording.
- Validated every link points to an existing statement and PNG.
