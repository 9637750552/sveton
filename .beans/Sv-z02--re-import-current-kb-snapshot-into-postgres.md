---
# Sv-z02
title: Re-import current KB snapshot into Postgres
status: completed
type: task
priority: normal
created_at: 2026-06-23T04:53:31Z
updated_at: 2026-06-23T04:54:45Z
parent: Sv-ldo
---

Load the current 590-statement canonical electricians KB snapshot into sveton_kb_dev and re-seed review queues for OmniCRM.

## Summary of Changes

Re-imported the current 590-statement electricians KB canonical snapshot into sveton_kb_dev.kb. Import run key: electricians_knowledge_base_c8fa722c1599.

Postgres now contains 590 statements, 14 clusters, 124 statement relations, 213 statement-image links, and 1128 review tasks. Re-seed idempotency was verified: second seed inserted 0 tasks and duplicate review task groups = 0.

Created import report: 01_docs/operations/postgres_knowledge_base_review/import_reports/2026-06-23_reimport_590_snapshot.md
