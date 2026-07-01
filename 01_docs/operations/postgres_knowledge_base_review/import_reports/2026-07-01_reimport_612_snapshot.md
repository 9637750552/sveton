# Re-import Report: 612-Statement Snapshot

Дата: 2026-07-01.

Beans task: `Sv-6xc`.

## Target

- database: `sveton_kb_dev`;
- schema: `kb`;
- project: `sveton`;
- corpus: `electricians_knowledge_base`;
- import run key: `electricians_knowledge_base_d2f3bbbca546`;
- source Sveton commit: `a22f1a4`;
- importer: `06_scripts/import_kb_snapshot_to_postgres.py`;
- review queue seed: `06_scripts/seed_kb_review_tasks.py`.

## Dry Run Result

Importer dry-run completed before applying SQL.

Input row counts:

| Artifact | Rows |
|---|---:|
| sources | 17 |
| chunks | 151 |
| statements | 612 |
| clusters | 14 |
| relations | 143 |
| images | 110 |
| statement-image links | 229 |
| coverage report rows | 151 |
| coverage overrides | 10 |
| coverage warnings | 18 |
| extraction errors | 0 |

Validation result:

- hard errors: `0`;
- warnings: `0`.

## Apply Notes

The import SQL was applied through the home Postgres LXC because the local `POSTGRES_DSN` environment variable points to a different public Postgres endpoint that does not contain `sveton_kb_dev`.

The importer is upsert-based and does not delete removed source artifacts. After applying the import, a targeted cleanup removed stale PDF-derived records left from the old `doc_014` / `doc_017` PDF pass:

| Cleanup item | Rows |
|---|---:|
| stale review tasks for removed chunks | 1 |
| stale chunks | 1 |
| stale statement-image links | 0 |
| stale PDF page-render images | 12 |

After cleanup, no `doc_017` chunks/statements remained and no PDF source/image rows remained for `doc_014` / `doc_017`.

## Postgres Counts After Re-import

| Table | Rows |
|---|---:|
| `kb.sources` | 17 |
| `kb.chunks` | 151 |
| `kb.images` | 110 |
| `kb.statements` | 612 |
| `kb.clusters` | 14 |
| `kb.statement_clusters` | 612 |
| `kb.statement_relations` | 143 |
| `kb.statement_images` | 229 |
| `kb.review_tasks` | 1183 |

## doc_014 Checks

| Check | Rows |
|---|---:|
| `doc_014` statements | 22 |
| `doc_014` review_required statements | 22 |
| `doc_014` safety_critical statements | 14 |
| `doc_014` statement-image links | 16 |

`doc_014` source file in Postgres is `ЭЛК_3_1процесс монтажа.docx`; no `.pdf` source file remains for its imported statements or chunks.

## doc_017 Checks

| Check | Rows |
|---|---:|
| `doc_017` statements | 0 |
| `doc_017` chunks | 0 |

`doc_017` remains excluded from canonical import and pending a separate visual/page-aware extraction workflow.

## Review Queue Re-seed

The review queue seed was run after import.

Seed insert/update result:

| Operation | Rows |
|---|---:|
| new `blocked_for_instruction` statement updates | 14 |
| new `statement_review_required` tasks | 22 |
| new `technical_safety_review` tasks | 14 |
| new `instruction_block_review` tasks | 14 |
| new `visual_evidence_review` tasks | 0 |
| new `source_chunk_review` tasks | 6 |

The review queue seed was executed a second time after the update.

Second execution result:

- downstream status updates: `0`;
- inserted review tasks: `0`;
- duplicate review task groups: `0`.

Final review task counts:

| Task type / status / priority | Rows |
|---|---:|
| `instruction_block_review / approved / critical` | 52 |
| `instruction_block_review / done / critical` | 6 |
| `instruction_block_review / needs_rewrite / critical` | 1 |
| `instruction_block_review / todo / critical` | 294 |
| `source_chunk_review / todo / high` | 12 |
| `statement_review_required / approved / critical` | 52 |
| `statement_review_required / approved / normal` | 1 |
| `statement_review_required / done / critical` | 6 |
| `statement_review_required / needs_rewrite / critical` | 1 |
| `statement_review_required / todo / critical` | 294 |
| `statement_review_required / todo / high` | 12 |
| `statement_review_required / todo / normal` | 3 |
| `technical_safety_review / approved / critical` | 52 |
| `technical_safety_review / done / critical` | 6 |
| `technical_safety_review / needs_rewrite / critical` | 1 |
| `technical_safety_review / todo / critical` | 294 |
| `visual_evidence_review / approved / critical` | 11 |
| `visual_evidence_review / approved / high` | 3 |
| `visual_evidence_review / done / critical` | 2 |
| `visual_evidence_review / needs_rewrite / high` | 1 |
| `visual_evidence_review / todo / critical` | 50 |
| `visual_evidence_review / todo / high` | 29 |

## OmniCRM Verification

The OmniCRM backend is reachable on the home network. The KB routes are protected by application authorization:

- `GET /knowledge-base/health` returned `Unauthorized`;
- `/api/knowledge-base/...` is not the backend prefix for these routes.

Therefore the database-backed import was verified directly in Postgres. The OmniCRM Knowledge Base UI should show the updated `612`-statement snapshot after a normal authenticated reload / `Обновить список`.

## Notes

- `doc_014` is available in the review queue with `review_required` preserved.
- `doc_014` has accepted statement-image links where the visual pass found stable links.
- `doc_017` is intentionally not imported as canonical knowledge.
- No semantic extraction was run during this import.
