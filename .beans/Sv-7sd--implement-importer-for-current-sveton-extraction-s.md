---
# Sv-7sd
title: Implement importer for current Sveton extraction snapshot
status: completed
type: task
priority: normal
created_at: 2026-06-17T11:31:48Z
updated_at: 2026-06-17T22:02:36Z
parent: Sv-ldo
---

Build importer that loads current Sveton electricians extraction artifacts into Postgres with import run metadata.

Checklist:
- [x] Choose implementation location: `semantic-analysis-engine` vs `Sveton` wrapper.
- [x] Add DB connection configuration without committing secrets.
- [x] Implement dry-run mode.
- [x] Implement idempotent upserts by project/corpus/source/chunk/statement ids.
- [x] Import sources and chunks.
- [x] Import statements.
- [x] Import clusters, relations, images, and statement-image links.
- [x] Write import summary.
- [x] Write discrepancy report.
- [x] Run importer against dev Postgres.
- [x] Verify row counts against current files.

## Summary of Changes

Added `07_scripts/import_kb_snapshot_to_postgres.py` as the project importer for the current Sveton electricians knowledge-base snapshot.

The importer validates source artifacts, writes dry-run summary/discrepancy/SQL outputs under `99_tmp/kb_import/`, and supports applying SQL through an external `psql` command without committed secrets.

Imported the current snapshot into `sveton_kb_dev.kb` with run key `electricians_knowledge_base_cbdb3712c7b5`: 17 sources, 146 chunks, 387 statements, 9 clusters, 387 statement-cluster links, 41 relations, 118 images, and 182 statement-image links.
