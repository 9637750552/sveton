---
# Sv-7sd
title: Implement importer for current Sveton extraction snapshot
status: todo
type: task
created_at: 2026-06-17T11:31:48Z
updated_at: 2026-06-17T11:31:48Z
parent: Sv-ldo
---

Build importer that loads current Sveton electricians extraction artifacts into Postgres with import run metadata.

Checklist:
- [ ] Choose implementation location: `semantic-analysis-engine` vs `Sveton` wrapper.
- [ ] Add DB connection configuration without committing secrets.
- [ ] Implement dry-run mode.
- [ ] Implement idempotent upserts by project/corpus/source/chunk/statement ids.
- [ ] Import sources and chunks.
- [ ] Import statements.
- [ ] Import clusters, relations, images, and statement-image links.
- [ ] Write import summary.
- [ ] Write discrepancy report.
- [ ] Run importer against dev Postgres.
- [ ] Verify row counts against current files.
