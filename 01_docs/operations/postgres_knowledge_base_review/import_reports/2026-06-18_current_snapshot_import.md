# Current Snapshot Import Report

Дата: 2026-06-18.

Beans task: `Sv-7sd`.

## Target

- database: `sveton_kb_dev`;
- schema: `kb`;
- project: `sveton`;
- corpus: `electricians_knowledge_base`;
- importer: `07_scripts/import_kb_snapshot_to_postgres.py`;
- import run key: `electricians_knowledge_base_cbdb3712c7b5`;
- schema version: `001_create_kb_review_schema`.

## Dry Run Result

The importer validated the current extraction snapshot before applying SQL.

Dry-run outputs were generated under `99_tmp/kb_import/`:

- `import_summary.json`;
- `discrepancies.jsonl`;
- `import.sql`.

Validation result:

- hard errors: `0`;
- warnings: `0`.

## Imported Row Counts

| Table | Rows |
|---|---:|
| `kb.projects` | 1 |
| `kb.corpora` | 1 |
| `kb.import_runs` | 1 |
| `kb.sources` | 17 |
| `kb.chunks` | 146 |
| `kb.images` | 118 |
| `kb.statements` | 387 |
| `kb.clusters` | 9 |
| `kb.statement_clusters` | 387 |
| `kb.statement_relations` | 41 |
| `kb.statement_images` | 182 |

## Notes

- Markdown review files were not parsed as structured review decisions.
- `kb.review_tasks`, `kb.review_decisions`, `kb.review_events`, and `kb.proposed_rewrites` were not populated in this import.
- Review queue seeding remains the next task: `Sv-dhj`.
