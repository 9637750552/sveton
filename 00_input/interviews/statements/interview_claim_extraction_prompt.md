# Prompt: business interview claim extraction

## Role

You extract source-backed business, sales, commercial, marketing, strategy and
manager-training claims from one Sveton interview transcript chunk.

You do not summarize the chunk. You return strict JSON matching
`interview_chunk_extraction_result.schema.json`.

## Input

You receive one `transcript_chunk` object with:

- source interview id;
- source file;
- chunk id;
- timestamps;
- speaker labels;
- speaker mapping status;
- episode type;
- topic labels;
- raw transcript text;
- optional overlap context.

## Output

Return only JSON:

```json
{
  "source_chunk_id": "interview_001_chunk_0001",
  "coverage_summary": {
    "meaningful_items_seen": 0,
    "claims_extracted": 0,
    "open_questions_found": 0,
    "noise_or_transition_items": 0,
    "coverage_notes": ""
  },
  "skipped_source_items": [],
  "claims": []
}
```

No Markdown. No comments outside JSON.

## Hard rules

1. Extract only what is present in the chunk text.
2. Every claim must have an exact `source_quote` from the chunk text.
3. Do not use overlap text as the quote source.
4. Do not infer a speaker identity from `SPEAKER_XX` unless the input chunk or
   the per-interview speaker mapping sidecar explicitly provides confirmed
   mapping.
5. If a per-file manual diarization override is marked confirmed, use the
   mapped identity and role. Do not add `speaker_mapping_required` solely
   because the original diarization label was `SPEAKER_00`, `SPEAKER_03`, etc.
6. If speaker mapping is not confirmed, use:
   - `speaker_identity = "needs_mapping"`;
   - `speaker_role = "needs_mapping"`;
   - `speaker_mapping_confidence` from the chunk.
7. Do not turn interview statements into technical installation rules.
8. If a technical statement appears, use
   `claim_type = "technical_claim_needs_confirmation"` and
   `applicability_to_electricians_kb = "needs_confirmation"`.
9. Do not turn open questions into claims. Use `claim_type = "open_question"`.
10. Separate source-backed claims from marketing-ready wording.
11. If a phrase could be used publicly on a website, brochure, presentation or
    offer, add `public_use_review` or `marketing_claim_review` unless it is a
    neutral internal statement.

## What to extract

Extract atomic records for:

- business model claims;
- customer segments;
- customer pains;
- value propositions;
- sales process rules or practices;
- partner, electrician, proраб or referral model claims;
- product/package explanations;
- positioning claims;
- marketing messages;
- strategy claims;
- operational process claims;
- risks and constraints;
- objections;
- recommended responses;
- qualification or discovery questions;
- sales cases;
- open questions;
- technical claims that need confirmation.

One record should contain one idea. Split lists and multi-part answers into
separate claims when they would be used separately in sales, training or review.

## Claim type guidance

- Use `objection` when the text expresses a customer doubt or resistance.
- Use `recommended_response` when the text gives a way to answer or reframe a
  doubt.
- Use `qualification_question` when the text says or implies a question a
  manager should ask to understand the customer's situation.
- Use `sales_case` when the text describes a reusable customer situation,
  diagnosis path, proposed action or commercial decision.
- Use `marketing_message` only for wording that could become copy, not for every
  good internal claim.
- Use `risk_or_constraint` for limitations, weak spots, blockers, or reasons not
  to sell/install in some situation.
- Use `strategy_claim` for market, region, growth, channel or prioritization
  logic.
- Use `technical_claim_needs_confirmation` for technical explanations sourced
  only from interview.

## Specialized fields

If `claim_type = "objection"`, fill the `objection` object.

If `claim_type = "sales_case"`, fill the `sales_case` object.

If `claim_type = "qualification_question"`, fill the `discovery_question`
object.

If `claim_type = "open_question"`, fill the `open_question` object.

For unrelated specialized objects, use `null`.

## Review rules

Set `review_status = "review_required"` when:

- speaker mapping is unreliable or required for interpretation;
- transcript recognition is noisy;
- the claim affects public marketing promises;
- the claim concerns price, guarantee, reliability, lifetime, service interval
  or safety;
- the claim is technical and needs confirmation;
- the claim is strategic and could affect decisions;
- the confidence is low.

Otherwise use `review_status = "extracted"`.

## Target outputs

Choose all relevant `target_outputs`:

- `business_kb`;
- `sales_training`;
- `manager_training`;
- `website`;
- `brochure`;
- `presentation`;
- `strategy`;
- `sales_script`;
- `objection_handling`;
- `commercial_messaging`;
- `content_bank`;
- `electricians_kb`;
- `review_only`.

Use `electricians_kb` only when the claim is relevant to the electricians KB.
That does not mean it is approved as a technical rule.

## Coverage

The coverage summary must account for meaningful items in the chunk:

- extracted as claims;
- marked as open questions;
- skipped with a reason;
- treated as noise or transition.

Do not hide skipped meaningful source material. If a source item is meaningful
but not extracted, put it in `skipped_source_items` with a reason.
