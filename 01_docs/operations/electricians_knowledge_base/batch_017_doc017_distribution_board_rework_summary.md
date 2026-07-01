# Batch 017: doc_017 controlled distribution-board rework extraction

Date: 2026-07-01

Source:

- `doc_017`
- `ЭЛК_5 - Переборка щитов_1.0.docx`
- source format: `DOCX`
- topic: `Переборка щитов`
- roles: `монтажник`, `электрик`, `инженер ГО`

Preflight:

- `01_docs/operations/electricians_knowledge_base/PREFLIGHT_DOC_017_DISTRIBUTION_BOARD_REWORK.md`

## Result

- Page-aware chunks processed: `7`
- Visual scheme artifacts extracted for manual review: `7`
- New canonical review-candidate statements added: `7`
- New cluster created: no
- Cluster used: `C008 / distribution_boards`
- New `statement_images.jsonl` links: `7` review-required links
- New relations added: `7`
- New coverage warnings added: `7`
- Extraction errors added: `0`
- Postgres import: not run

## Decision

Controlled extraction stopped before final instructional statement promotion, but the valuable schemes were preserved as separate reviewable visual units and entered the review pipeline through `visual_review_candidate` atomic statements.

The DOCX source is usable and valuable as a visual source artifact, but not as a text-first extraction source. The meaningful content is carried by full-page wiring schemes, conductor routes, terminal labels, numbered outputs, and PE/L/N legends. These visual facts are safety-critical; the batch adds review candidates that describe what each scheme shows, but does not promote specific wiring instructions before expert visual review.

## Manual Visual Review

Manual visual review zones: `7`.

- `doc_017_chunk_0001` / `img_0123` / `doc_017_scheme_001`: page 1 component lineup and A1/A2 labels.
- `doc_017_chunk_0002` / `img_0124` / `doc_017_scheme_002`: page 2 left scheme with Ввод, N, A1/A2 labels.
- `doc_017_chunk_0003` / `img_0125` / `doc_017_scheme_003`: page 2 right scheme with inverter `in` / `OUT` phase labels.
- `doc_017_chunk_0004` / `img_0126` / `doc_017_scheme_004`: page 3 assembled scheme with inverter input/output labels.
- `doc_017_chunk_0005` / `img_0127` / `doc_017_scheme_005`: page 4 numbered outputs `1-6` and PE/L/N input-output legend.
- `doc_017_chunk_0006` / `img_0128` / `doc_017_scheme_006`: page 5 alternate split-output/routing scheme.
- `doc_017_chunk_0007` / `img_0129` / `doc_017_scheme_007`: page 6 alternate routing scheme.

No final image-only or diagram-only wiring instructions were created. The rendered schemes are linked through `statement_images.jsonl` with `link_type = visual_review_candidate` and `status = review_required`, not as accepted visual evidence.

Review-candidate statements:

- `doc_017_chunk_0001_stmt_001`
- `doc_017_chunk_0002_stmt_001`
- `doc_017_chunk_0003_stmt_001`
- `doc_017_chunk_0004_stmt_001`
- `doc_017_chunk_0005_stmt_001`
- `doc_017_chunk_0006_stmt_001`
- `doc_017_chunk_0007_stmt_001`

Primary descriptions and review questions:

- `00_input/documents/electricians_knowledge_base/statements/review/doc_017_visual_schemes_review.md`
- `00_input/documents/electricians_knowledge_base/statements/review/doc_017_visual_schemes.jsonl`

## Dedupe Gate

No new final wiring instructions were introduced. The `7` new statements are low-confidence `visual_review_candidate` records connected to existing context through `related_to` relations.

Relevant existing canonical coverage for future review includes:

- `doc_015_chunk_0012_stmt_003`: control input/output context.
- `doc_015_chunk_0016_stmt_004`: inverter input L/N feed.
- `doc_015_chunk_0016_stmt_005`: inverter output L/N return to reserve consumers.
- `doc_016_chunk_0006_stmt_003`: reserve-group phase/null handling.
- `doc_016_chunk_0006_stmt_004`: reserve consumers under one UZO.
- `doc_016_chunk_0006_stmt_007`: master-switch coil A1/A2 context.
- `doc_016_chunk_0006_stmt_012`: contactor operation.
- `doc_016_chunk_0008_stmt_001`: master-switch breaker powered from reserve line.

## Safety Review

New `safety_critical` statements: `7`.

All `7` new statements have:

- `risk_level = safety_critical`
- `review_status = review_required`
- `statement_type = visual_review_candidate`
- `confidence = low`

All potential wiring, shield-rework, DC/AC routing, reserve-group, terminal, output-numbering, and inverter input/output facts remain blocked until expert review turns candidates into precise instructions.

## Files Updated

- `00_input/documents/electricians_knowledge_base/extracted/ЭЛК_5 - Переборка щитов_1.0.md`
- `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`
- `00_input/documents/electricians_knowledge_base/chunks/summary.md`
- `00_input/documents/electricians_knowledge_base/inventory.md`
- `00_input/documents/electricians_knowledge_base/images/inventory.csv`
- `00_input/documents/electricians_knowledge_base/images/inventory.md`
- `00_input/documents/electricians_knowledge_base/images/normalized/doc017_scheme_001_page_1_component_lineup.png`
- `00_input/documents/electricians_knowledge_base/images/normalized/doc017_scheme_002_page_2_left.png`
- `00_input/documents/electricians_knowledge_base/images/normalized/doc017_scheme_003_page_2_right.png`
- `00_input/documents/electricians_knowledge_base/images/normalized/doc017_scheme_004_page_3_assembled.png`
- `00_input/documents/electricians_knowledge_base/images/normalized/doc017_scheme_005_page_4_outputs_1_6.png`
- `00_input/documents/electricians_knowledge_base/images/normalized/doc017_scheme_006_page_5_split_outputs.png`
- `00_input/documents/electricians_knowledge_base/images/normalized/doc017_scheme_007_page_6_alternate_routing.png`
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_report.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_report.md`
- `00_input/documents/electricians_knowledge_base/statements/coverage_warnings.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/statement_clusters.json`
- `00_input/documents/electricians_knowledge_base/statements/statement_clusters.md`
- `00_input/documents/electricians_knowledge_base/statements/statement_relations.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/statement_images.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/review/doc_017_visual_schemes_review.md`
- `00_input/documents/electricians_knowledge_base/statements/review/doc_017_visual_schemes.jsonl`
- `01_docs/operations/electricians_knowledge_base/README.md`

## Canonical Artifacts Not Changed

No canonical artifact was left unchanged in the visual layer for `doc_017`: `statement_images.jsonl` now has review-required links, not accepted links.

## Constraints Confirmed

- Only the DOCX source was used.
- PDF-derived artifacts were not restored or used.
- `doc_017` was not mixed with `doc_014`.
- No semantic extraction runner was launched blindly.
- No editorial section was created.
- Postgres import was not run.
- OmniCRM import was not run.
