---
# Sv-p41
title: Run business interviews pilot extraction batch
status: completed
type: task
priority: normal
created_at: 2026-07-02T10:57:48Z
updated_at: 2026-07-02T12:43:59Z
parent: Sv-3tw
---

Phase 5: select representative fragments, run pilot extraction, review quality, and revise schema/prompt.

Checklist:
- [x] Confirm inputs and acceptance criteria.
- [x] Produce the phase artifact(s).
- [x] Validate against BUSINESS_INTERVIEWS_PIPELINE.md.
- [x] Update parent epic checklist.

## Summary of Changes

Ran pilot extraction for 8 chunks from interview_001. Produced pilot_interview_claims.jsonl with 30 claims, pilot_extraction_results.jsonl with 8 per-chunk records, and pilot_extraction_review.md. Updated extraction prompt to support confirmed manual diarization overrides. Validation passed with 0 speaker_mapping_required flags and 0 needs_mapping identities.
