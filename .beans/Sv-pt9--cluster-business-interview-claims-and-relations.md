---
# Sv-pt9
title: Cluster business interview claims and relations
status: completed
type: task
priority: normal
created_at: 2026-07-02T10:57:49Z
updated_at: 2026-07-02T21:53:32Z
parent: Sv-3tw
---

Phase 8: cluster claims and preserve duplicates, support, contradictions, examples, and open questions as relations.

Checklist:
- [x] Confirm inputs and acceptance criteria.
- [x] Produce the phase artifact(s).
- [x] Validate against BUSINESS_INTERVIEWS_PIPELINE.md.
- [x] Update parent epic checklist.

## Summary of Changes

Built Phase 8 clustering and relation artifacts for all 416 corpus claims:

- `00_input/interviews/statements/statement_clusters.json`
- `00_input/interviews/statements/statement_clusters.md`
- `00_input/interviews/statements/statement_relations.jsonl`
- `07_scripts/business_interviews/build_statement_clusters.py`

The clustering assigns every claim to exactly one primary cluster across 19 business-interview themes and creates 440 relations covering support/refinement, duplicate candidates, examples, technical-confirmation requirements, marketing-message derivations, open-question context, and curated contradiction/tension points. Validation checks report 416/416 assigned claims, 19 clusters, 440 valid relations, and 0 errors.
