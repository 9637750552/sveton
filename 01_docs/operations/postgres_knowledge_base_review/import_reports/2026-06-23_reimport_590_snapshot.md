# Re-import Report: 590-Statement Snapshot

Дата: 2026-06-23.

Beans task: `Sv-z02`.

## Target

- database: `sveton_kb_dev`;
- schema: `kb`;
- project: `sveton`;
- corpus: `electricians_knowledge_base`;
- import run key: `electricians_knowledge_base_c8fa722c1599`;
- importer: `07_scripts/import_kb_snapshot_to_postgres.py`;
- review queue seed: `07_scripts/seed_kb_review_tasks.py`.

## Dry Run Result

Importer dry-run completed before applying SQL.

Input row counts:

| Artifact | Rows |
|---|---:|
| sources | 17 |
| chunks | 146 |
| statements | 590 |
| clusters | 14 |
| relations | 124 |
| images | 118 |
| statement-image links | 213 |

Validation result:

- hard errors: `0`;
- warnings: `0`.

## Postgres Counts After Re-import

| Table | Rows |
|---|---:|
| `kb.sources` | 17 |
| `kb.chunks` | 146 |
| `kb.images` | 118 |
| `kb.statements` | 590 |
| `kb.clusters` | 14 |
| `kb.statement_clusters` | 590 |
| `kb.statement_relations` | 124 |
| `kb.statement_images` | 213 |
| `kb.review_tasks` | 1128 |

## Review Queue Re-seed

The review queue seed added tasks for the new canonical statements and preserved existing task statuses.

Seed insert/update result:

| Operation | Rows |
|---|---:|
| new `blocked_for_instruction` statement updates | 135 |
| new `statement_review_required` tasks | 141 |
| new `technical_safety_review` tasks | 135 |
| new `instruction_block_review` tasks | 135 |
| new `visual_evidence_review` tasks | 10 |
| new `source_chunk_review` tasks | 2 |

Final review task counts:

| Task type / status / priority | Rows |
|---|---:|
| `instruction_block_review / approved / critical` | 1 |
| `instruction_block_review / todo / critical` | 338 |
| `source_chunk_review / todo / high` | 7 |
| `statement_review_required / approved / critical` | 1 |
| `statement_review_required / todo / critical` | 338 |
| `statement_review_required / todo / high` | 7 |
| `statement_review_required / todo / normal` | 1 |
| `technical_safety_review / approved / critical` | 1 |
| `technical_safety_review / todo / critical` | 338 |
| `visual_evidence_review / todo / critical` | 63 |
| `visual_evidence_review / todo / high` | 33 |

## Idempotency Check

The review queue seed was executed a second time after the update.

Second execution result:

- downstream status updates: `0`;
- inserted review tasks: `0`;
- duplicate review task groups: `0`.

## Notes For OmniCRM

The OmniCRM Knowledge Base UI should now read the updated Postgres KB and show the expanded `590`-statement snapshot after pressing `Обновить список` or reloading the queue.

OmniCRM did not import repository files directly; the update was applied by the Sveton importer and review queue seed.
