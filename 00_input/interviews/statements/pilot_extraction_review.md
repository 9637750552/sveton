# Pilot extraction review: interview_001

Date: 2026-07-02

## Inputs

- Source chunks: `00_input/interviews/chunks/pilot_chunks.jsonl`
- Speaker mapping: `00_input/interviews/review/interview_001_speaker_mapping.json`
- Extraction prompt: `00_input/interviews/statements/interview_claim_extraction_prompt.md`

## Outputs

- `pilot_interview_claims.jsonl`: 30 extracted claims
- `pilot_extraction_results.jsonl`: 8 per-chunk extraction result records

## Validation summary

- JSONL parse: passed
- Required claim fields: passed
- Allowed claim types: passed
- Allowed review flags: passed
- Exact `source_quote` containment in source chunks: passed
- Result records: 8
- Claims: 30
- Claims with `speaker_mapping_required`: 0
- Claims with `speaker_identity = needs_mapping`: 0
- Validation errors after Phase 6 validator: 0
- Validation warnings after Phase 6 validator: 0

## Review profile

The pilot intentionally keeps review on content-sensitive claims:

- marketing or public wording;
- technical claims sourced only from interview;
- price, reliability, metric, cost or timeline claims;
- strategic claims that affect business decisions;
- noisy recognition fragments.

Speaker labels `SPEAKER_00` and `SPEAKER_03` are not treated as review reasons
for `interview_001` because the user accepted manual diarization overrides.

## Quality notes

- The extraction separates source-backed business claims from future editorial
  copy.
- Technical content is not promoted into electricians KB; it is marked as
  `technical_claim_needs_confirmation` or `applicability_to_electricians_kb =
  needs_confirmation`.
- Some claims retain `recognition_noise` because the source transcript is noisy,
  but the extracted business meaning is still usable for pilot review.
- The extraction prompt was updated so confirmed per-file manual diarization
  overrides can be used as speaker identity sources.
