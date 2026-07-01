# Re-import Report: 619-Statement Snapshot

Дата: 2026-07-01.

Beans task: `Sv-073`.

## Target

- database: `sveton_kb_dev`;
- schema: `kb`;
- project: `sveton`;
- corpus: `electricians_knowledge_base`;
- import run key: `electricians_knowledge_base_b36d6a5c25dd`;
- source Sveton commit: `c2eb96f0ada0c88c1abba45a3ebfa84978f54b96`;
- importer: `06_scripts/import_kb_snapshot_to_postgres.py`;
- review queue seed: `06_scripts/seed_kb_review_tasks.py`;
- OmniCRM media migration: `scripts/knowledge-base/migrate-legacy-images-to-nextcloud.mjs`.

## Dry Run Result

Importer dry-run completed before applying SQL.

Input row counts:

| Artifact | Rows |
|---|---:|
| sources | 17 |
| chunks | 158 |
| statements | 619 |
| clusters | 14 |
| relations | 150 |
| images | 117 |
| statement-image links | 236 |
| coverage report rows | 158 |
| coverage overrides | 10 |
| coverage warnings | 25 |
| extraction errors | 0 |

Validation result:

- hard errors: `0`;
- warnings: `7`;
- all warnings are expected `source_quote_is_exact = false` warnings for the seven `doc_017` review-gated visual statements.

## Apply Notes

The import SQL was applied through the home Postgres LXC. A CSV quoting issue in `images/inventory.csv` for `img_0124` and `img_0128` was fixed before the final import metadata refresh, because those rows contained comma-bearing fields that needed CSV quoting.

The import was applied twice:

1. initial apply after the CSV fix was made in the working tree;
2. final metadata refresh after commit `c2eb96f`, so `kb.import_runs.source_git_commit` points to the committed source artifact state.

## Postgres Counts After Re-import

| Table | Rows |
|---|---:|
| `kb.sources` | 17 |
| `kb.chunks` | 158 |
| `kb.images` | 117 |
| `kb.statements` | 619 |
| `kb.clusters` | 14 |
| `kb.statement_clusters` | 619 |
| `kb.statement_relations` | 150 |
| `kb.statement_images` | 236 |
| `kb.review_tasks` | 1218 |

## doc_017 Checks

| Check | Rows |
|---|---:|
| `doc_017` chunks | 7 |
| `doc_017` statements | 7 |
| `doc_017` review_required statements | 7 |
| `doc_017` safety_critical statements | 7 |
| `doc_017` visual_review_required statements | 7 |
| `doc_017` downstream blocked statements | 7 |
| `doc_017` statement-image links | 7 |
| `doc_017` managed media links | 7 |
| `doc_017` review tasks | 28 |

`doc_017` image links remain review-gated:

| Field | Value |
|---|---|
| `link_type` | `visual_review_candidate` |
| `review_status` | `review_required` |
| source `status` | `review_required` |
| source `confidence` | `low` |

No `accepted` image links were created for `doc_017`.

## Review Queue Re-seed

The review queue seed was run after import.

Seed insert/update result:

| Operation | Rows |
|---|---:|
| new `blocked_for_instruction` statement updates | 7 |
| new `statement_review_required` tasks | 7 |
| new `technical_safety_review` tasks | 7 |
| new `instruction_block_review` tasks | 7 |
| new `visual_evidence_review` tasks | 7 |
| new `source_chunk_review` tasks | 7 |

The review queue seed was executed again after the final import metadata refresh.

Second execution result:

- downstream status updates: `0`;
- inserted review tasks: `0`.

Final `doc_017` review task distribution:

| Task type | Status | Priority | Rows |
|---|---|---|---:|
| `instruction_block_review` | `todo` | `critical` | 7 |
| `statement_review_required` | `todo` | `critical` | 7 |
| `technical_safety_review` | `todo` | `critical` | 7 |
| `visual_evidence_review` | `todo` | `critical` | 7 |

## OmniCRM / Nextcloud Media Layer

`doc_017` schemes are DOCX-derived normalized page renders. They have no local `raw` files, so OmniCRM's legacy image migration was extended to use `images/normalized` as a fallback when `images/raw` does not contain the image file.

Media migration result:

| Check | Rows |
|---|---:|
| `img_0123`-`img_0129` media assets | 7 |
| source kind | `legacy_instruction_normalized` |
| active managed links for `doc_017` | 7 |
| total active managed links | 236 |
| active duplicate managed link pairs | 0 |

Nextcloud checksum verification for `img_0123`-`img_0129` passed.

## Notes

- `doc_017` is imported as review-gated knowledge, not as accepted wiring instruction.
- All seven `doc_017` statements remain `review_required`, `safety_critical`, `visual_review_required`, and `blocked_for_instruction`.
- The seven linked schemes are review material for engineers, not accepted visual evidence.
- No PDF artifacts were restored or imported.
