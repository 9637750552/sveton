---
# Sv-n6x
title: Run full interview corpus extraction
status: completed
type: task
priority: normal
created_at: 2026-07-02T10:57:49Z
updated_at: 2026-07-02T21:40:33Z
parent: Sv-3tw
---

Phase 7: chunk all seven transcripts, extract canonical claims, and produce review and coverage artifacts.

Checklist:
- [x] Confirm inputs and acceptance criteria.
- [x] Produce the phase artifact(s).
- [x] Validate against BUSINESS_INTERVIEWS_PIPELINE.md.
- [x] Update parent epic checklist.

## Progress Note: interview_001 full-control run

Completed full chunking and extraction for interview_001 only. Produced interview_001_chunks.jsonl with 24 chunks, interview_001_claims.jsonl with 91 claims, interview_001_extraction_results.jsonl with 24 result records, and interview_001_review_queue / interview_001_coverage_report artifacts. Validation reports 0 errors and 0 warnings. Phase 7 remains in progress because interviews 002-007 are not yet processed.

## Progress Note: interview_002 speaker mapping and chunking\n\nConfirmed speaker mapping for interview_002: SPEAKER_00 and SPEAKER_01 are Дмитрий; SPEAKER_02 is Сергей. Produced interview_002_chunks.jsonl with 32 sequential chunks covering source lines 1-562; 31 chunks are ready_for_extraction and 1 opening setup chunk is excluded. Claims extraction for interview_002 remains pending.

## Progress Note: interview_002 full extraction\n\nCompleted full extraction for interview_002. Produced interview_002_claims.jsonl with 87 claims, interview_002_extraction_results.jsonl with 32 result records, interview_002_review_queue artifacts, interview_002_coverage_report artifacts, and interview_002_claims_review.md. Validation reports 0 errors and 0 warnings. Phase 7 remains in progress because interviews 003-007 are not yet processed.

## Progress Note: interview_003 speaker mapping and chunking\n\nConfirmed speaker mapping for interview_003: SPEAKER_01 is Сергей; SPEAKER_00 and SPEAKER_02 are Алексей, commercial director. Produced interview_003_chunks.jsonl with 20 sequential chunks covering source lines 1-448; all chunks are ready_for_extraction. Claims extraction for interview_003 remains pending.

## Progress Note: interview_003 full extraction\n\nCompleted full extraction for interview_003. Produced interview_003_chunks.jsonl with 20 chunks, interview_003_claims.jsonl with 60 claims, interview_003_extraction_results.jsonl with 20 result records, interview_003_review_queue artifacts, interview_003_coverage_report artifacts, and interview_003_claims_review.md. Validation reports 0 errors and 0 warnings. This file is technical-heavy: 43 claims require technical confirmation. Phase 7 remains in progress because interviews 004-007 are not yet processed.

## Progress Note: interview_004 speaker mapping and chunking\n\nConfirmed speaker mapping for interview_004: SPEAKER_00, SPEAKER_01, and SPEAKER_03 are Алексей, commercial director; SPEAKER_02 is Сергей. Produced interview_004_chunks.jsonl with 17 sequential chunks covering source lines 1-496; 13 chunks are ready_for_extraction, 1 mixed/off-topic chunk needs review, and 3 chunks are excluded as setup/off-topic. Claims extraction for interview_004 remains pending.

## Progress Note: interview_004 full extraction\n\nCompleted full extraction for interview_004. Produced interview_004_chunks.jsonl with 17 chunks, interview_004_claims.jsonl with 43 claims, interview_004_extraction_results.jsonl with 17 result records, interview_004_review_queue artifacts, interview_004_coverage_report artifacts, and interview_004_claims_review.md. Validation reports 0 errors and 0 warnings. Off-topic camping blocks were skipped from Sveton Business KB claims. Phase 7 remains in progress because interviews 005-007 are not yet processed.

## Progress Note: interview_005 speaker mapping and chunking\n\nConfirmed speaker mapping for interview_005: SPEAKER_00 is Сергей; SPEAKER_01 is Дмитрий. Produced interview_005_chunks.jsonl with 7 sequential chunks covering source lines 1-92; all chunks are ready_for_extraction. Claims extraction for interview_005 remains pending.

## Progress Note: interview_005 full extraction\n\nCompleted full extraction for interview_005. Produced interview_005_chunks.jsonl with 7 chunks, interview_005_claims.jsonl with 28 claims, interview_005_extraction_results.jsonl with 7 result records, interview_005_review_queue artifacts, interview_005_coverage_report artifacts, and interview_005_claims_review.md. Validation reports 0 errors and 0 warnings. Phase 7 remains in progress because interviews 006-007 are not yet processed.

## Progress Note: interview_006 full extraction

Confirmed speaker mapping for interview_006: SPEAKER_00 and SPEAKER_01 are Дмитрий; SPEAKER_02 and SPEAKER_03 are Сергей. Completed full chunking and extraction for interview_006. Produced interview_006_chunks.jsonl with 17 chunks, interview_006_claims.jsonl with 55 claims, interview_006_extraction_results.jsonl with 17 result records, interview_006_review_queue artifacts, interview_006_coverage_report artifacts, and interview_006_claims_review.md. Validation reports 0 errors and 0 warnings. This file is technical/operations-heavy: 39 claims require technical confirmation. Phase 7 remains in progress because interview_007 is not yet processed.

## Progress Note: interview_007 full extraction

Confirmed speaker mapping for interview_007: SPEAKER_00 and SPEAKER_02 are Дмитрий; SPEAKER_01 is Сергей; SPEAKER_03 is Вадик. Completed full chunking and extraction for interview_007. Produced interview_007_chunks.jsonl with 15 chunks, interview_007_claims.jsonl with 52 claims, interview_007_extraction_results.jsonl with 15 result records, interview_007_review_queue artifacts, interview_007_coverage_report artifacts, and interview_007_claims_review.md. Validation reports 0 errors and 0 warnings. This file covers CRM ownership, service model, electricians/foremen channels, scalable outsourced electrician model, product value, technical edge cases, and regional next steps. Phase 7 is complete for all seven transcripts.

## Progress Note: corpus aggregate

Created corpus-level aggregate artifacts for downstream clustering: interview_corpus_chunks.jsonl with 132 chunks, interview_corpus_claims.jsonl with 416 claims, and interview_corpus_extraction_results.jsonl with 132 result records. Regenerated corpus-level review_queue and coverage_report for all seven interviews. Corpus validation reports 0 errors and 0 warnings.
