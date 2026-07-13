---
# Sv-3tw
title: Build Business / Sales / Commercial KB from interviews
status: completed
type: epic
priority: normal
created_at: 2026-07-02T10:55:44Z
updated_at: 2026-07-03T06:55:06Z
---

Build the Business / Sales / Commercial Knowledge Base from leadership and manager interview transcripts using a business_interviews profile on top of the existing semantic-analysis approach.

Scope boundaries:
- Source-backed canonical knowledge stays in Sveton under 00_input/interviews/.
- Domain methodology and operating docs stay under 01_docs/operations/leadership_interviews_semantic_analysis/.
- Reusable engine code/prompts/schemas can later move to semantic-analysis-engine after the pilot proves stable.
- Interview statements may support sales, marketing, strategy, and manager training outputs.
- Interview statements must not become technical installation instructions without confirmation from technical documents.

Phased plan:
- [x] Phase 1: Methodology and profile contract
  - [x] Create BUSINESS_INTERVIEWS_PIPELINE.md.
  - [x] Define source-backed vs editorial layers.
  - [x] Define artifact list, gates, and review rules.
- [x] Phase 2: Speaker and source preparation
  - [x] Create/update review/speaker_mapping.md.
  - [x] Confirm interview grouping, participants, roles, and diarization quality.
  - [x] Define source_interviews/interview inventory fields.
- [x] Phase 3: Interview chunking
  - [x] Define transcript chunk schema.
  - [x] Define episode-based chunking rules.
  - [x] Produce pilot transcript_chunks.jsonl for selected fragments.
- [x] Phase 4: Extraction contract
  - [x] Create interview_claim.schema.json.
  - [x] Create extraction prompt for business/sales/commercial claims.
  - [x] Define separate records for objections, sales cases, open questions, and discovery questions.
- [x] Phase 5: Pilot batch
  - [x] Select representative fragments across strategy, sales, objections, product explanation, partners, CRM/1C, and regional expansion.
  - [x] Run pilot extraction.
  - [x] Review quality and revise schema/prompt.
- [x] Phase 6: Validation and promotion
  - [x] Add validation rules for quote, timestamp, speaker, claim type, target output, confidence, and technical-confirmation boundaries.
  - [x] Define canonical promotion rules and coverage report format.
- [x] Phase 7: Full corpus extraction
  - [x] Chunk all seven transcripts.
  - [x] Extract canonical interview claims.
  - [x] Produce review_queue.md and coverage_report.md.
- [x] Phase 8: Clustering and relations
  - [x] Cluster by customer segment, pain, value proposition, objection, sales process, partner model, operations, strategy, and constraints.
  - [x] Preserve duplicates, related claims, contradictions, and open questions as relations.
- [x] Phase 9: Editorial outputs
  - [x] Assemble Business / Sales / Commercial KB.
  - [x] Assemble business model map, sales playbook, objection handling, manager training outline, messaging bank, website/content bank, presentation outline, and secondary links to electricians KB.

## Summary of Changes

Completed the Business / Sales / Commercial KB build from leadership and manager interviews. The workstream now has methodology, speaker/source preparation, chunking, extraction schema, pilot and full-corpus extraction, validation, canonical promotion, clustering/relations, review artifacts, and downstream editorial outputs for business, sales, training, messaging, website, presentation, and links to electricians KB.

Initial acceptance criteria:
- BUSINESS_INTERVIEWS_PIPELINE.md exists and states the reusable profile approach.
- First task is tracked as a child bean.
- No source-backed claim is promoted without source quote, speaker/timestamp, and review status.
