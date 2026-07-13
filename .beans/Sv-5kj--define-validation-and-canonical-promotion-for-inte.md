---
# Sv-5kj
title: Define validation and canonical promotion for interview claims
status: completed
type: task
priority: normal
created_at: 2026-07-02T10:57:49Z
updated_at: 2026-07-02T12:53:35Z
parent: Sv-3tw
---

Phase 6: add validation rules, promotion gates, coverage report format, and review queue rules.

Checklist:
- [x] Confirm inputs and acceptance criteria.
- [x] Produce the phase artifact(s).
- [x] Validate against BUSINESS_INTERVIEWS_PIPELINE.md.
- [x] Update parent epic checklist.

## Summary of Changes

Defined validation and canonical promotion rules for business interview claims. Added coverage_report and review_queue item schemas, implemented 07_scripts/business_interviews/validate_claims.py, regenerated review_queue and coverage_report for the pilot, and fixed pilot source_quote fields so all quotes are exact contiguous fragments from source chunks. Pilot validation now reports 30 claims, 8 chunks, 0 errors, and 0 warnings.
