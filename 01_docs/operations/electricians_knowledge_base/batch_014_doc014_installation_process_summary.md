# Batch 014: doc_014 controlled installation-process extraction

Date: 2026-07-01

Source:

- `doc_014`
- `ЭЛК_3_1процесс монтажа.docx`
- source format: `DOCX`
- topic: `installation_process`
- roles: `installer`, `electrician`

Preflight:

- `01_docs/operations/electricians_knowledge_base/PREFLIGHT_DOC_014_INSTALLATION_PROCESS.md`

## Result

- New canonical statements added: `22`
- New cluster created: no
- Cluster used: `C009 / installation_process`
- New `statement_images.jsonl` links: `0`
- New relations added: `19`
- New coverage warnings added: `4`
- Extraction errors added: `0`
- Postgres import: not run

## Dedupe Gate

Potential duplicate statements not promoted against `doc_015 / C009`: `9`.

Skipped duplicate/C009-covered areas:

- bypass shield must be near the inverter;
- DC protection mounting to the plus АКБ terminal and inverter plus cable details;
- inverter free-air / ventilation / clearance context;
- one-phase bypass terminal labels for L/N input-output routing.

Additional duplicate coverage outside `doc_015 / C009`:

- `5` balancer-wire preparation facts in `doc_014_chunk_0002` matched existing `doc_012` canonical statements and were covered through `source_coverage_overrides.jsonl`.

## Manual Visual Review

Manual visual review zones: `3`.

- `doc_014_chunk_0004`: inverter placement / clearance labels, including ambiguous `Не допустимо / 20 мм`.
- `doc_014_chunk_0008`: one-phase bypass terminal wiring scheme labels.
- `doc_014_chunk_0009`: priority vs non-priority visual labels and board-rework scheme labels.

No image-only canonical statements were created. Embedded images and схемы remain manual-review candidates.

## Safety Review

All `22` new statements have `review_status = review_required`.

`14` new statements have `risk_level = safety_critical`:

- `doc_014_chunk_0001_stmt_002`
- `doc_014_chunk_0001_stmt_003`
- `doc_014_chunk_0001_stmt_004`
- `doc_014_chunk_0001_stmt_005`
- `doc_014_chunk_0001_stmt_013`
- `doc_014_chunk_0003_stmt_001`
- `doc_014_chunk_0003_stmt_002`
- `doc_014_chunk_0003_stmt_003`
- `doc_014_chunk_0005_stmt_001`
- `doc_014_chunk_0005_stmt_002`
- `doc_014_chunk_0006_stmt_001`
- `doc_014_chunk_0009_stmt_001`
- `doc_014_chunk_0009_stmt_002`
- `doc_014_chunk_0009_stmt_003`

## Covered Source Zones

Covered with new statements:

- location constraints for UPS installation;
- rack selection and rack assembly sequence;
- protective-panel attachment detail;
- DC-protection fuse insert orientation;
- balancer placement and wire-length reserve;
- bypass shield cable-entry preparation;
- reverse cable route from the main home power board;
- priority-load selection and inverter nominal-power warning.

Covered by duplicate/override rather than new statements:

- balancer-wire preparation already covered by `doc_012`;
- inverter free-air / clearance context already partly covered by `doc_015` but requires manual visual review for the `20 мм` fragment;
- one-phase bypass wiring labels already partly covered by `doc_015` and require manual visual review before any additional facts.

## Files Updated

- `00_input/documents/electricians_knowledge_base/extracted/ЭЛК_3_1процесс монтажа.md`
- `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`
- `00_input/documents/electricians_knowledge_base/chunks/summary.md`
- `00_input/documents/electricians_knowledge_base/inventory.md`
- `00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/statement_clusters.json`
- `00_input/documents/electricians_knowledge_base/statements/statement_clusters.md`
- `00_input/documents/electricians_knowledge_base/statements/statement_relations.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_overrides.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_report.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_report.md`
- `00_input/documents/electricians_knowledge_base/statements/coverage_warnings.jsonl`
- `01_docs/operations/electricians_knowledge_base/README.md`

## Constraints Confirmed

- Source chunks are DOCX-based.
- No `doc_014` `.pdf` source_file was added.
- `doc_017` was not extracted or chunked.
- `statement_images.jsonl` was not changed for `doc_014`.
- No commit or push was made.
