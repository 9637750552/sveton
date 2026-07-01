# Semantic analysis pipeline for technical documentation

Date: 2026-07-02

## Purpose

This document summarizes the actual process used to turn the Sveton electricians instruction corpus into a structured knowledge base. It covers both layers that mattered in practice:

- semantic extraction of source-backed atomic statements;
- visual layer extraction, image linking, Nextcloud migration, Postgres import, and review workflow.

The goal is to turn this experience into a repeatable product for other technical documents, not just preserve the history of one manual project.

## Source Material Studied

Primary Sveton artifacts:

- `00_input/documents/electricians_knowledge_base/inventory.md`
- `00_input/documents/electricians_knowledge_base/extracted/`
- `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`
- `00_input/documents/electricians_knowledge_base/chunks/summary.md`
- `00_input/documents/electricians_knowledge_base/images/inventory.csv`
- `00_input/documents/electricians_knowledge_base/images/inventory.md`
- `00_input/documents/electricians_knowledge_base/images/linking_plan.md`
- `00_input/documents/electricians_knowledge_base/statements/atomic_extraction_prompt.md`
- `00_input/documents/electricians_knowledge_base/statements/atomic_statement.schema.json`
- `00_input/documents/electricians_knowledge_base/statements/chunk_extraction_result.schema.json`
- `00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/statement_clusters.json`
- `00_input/documents/electricians_knowledge_base/statements/statement_relations.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/statement_images.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_report.md`
- `00_input/documents/electricians_knowledge_base/statements/coverage_warnings.jsonl`
- `01_docs/operations/electricians_knowledge_base/README.md`
- `01_docs/operations/electricians_knowledge_base/KB_CANONICAL_CREATION_COMPLETE.md`

Special-case extraction and visual artifacts:

- `01_docs/operations/electricians_knowledge_base/PREFLIGHT_DOC_012_TECHNICAL_CARDS.md`
- `00_input/documents/electricians_knowledge_base/statements/batch_011_doc012_technical_cards_summary.md`
- `00_input/documents/electricians_knowledge_base/statements/batch_012_doc012_visual_ocr_summary.md`
- `01_docs/operations/electricians_knowledge_base/PREFLIGHT_DOC_014_INSTALLATION_PROCESS.md`
- `01_docs/operations/electricians_knowledge_base/batch_014_doc014_installation_process_summary.md`
- `01_docs/operations/electricians_knowledge_base/batch_015_doc014_visual_links_summary.md`
- `01_docs/operations/electricians_knowledge_base/PREFLIGHT_DOC_017_DISTRIBUTION_BOARD_REWORK.md`
- `01_docs/operations/electricians_knowledge_base/batch_017_doc017_distribution_board_rework_summary.md`
- `00_input/documents/electricians_knowledge_base/statements/review/doc_017_visual_schemes_review.md`

Reusable engine artifacts:

- `/home/sergey/semantic-analysis-engine/README.md`
- `/home/sergey/semantic-analysis-engine/docs/PROJECT_CONTRACT.md`
- `/home/sergey/semantic-analysis-engine/prompts/atomic_extraction_prompt.md`
- `/home/sergey/semantic-analysis-engine/schemas/`
- `/home/sergey/semantic-analysis-engine/scripts/`
- `01_docs/operations/semantic_analysis_engine/EPIC_SEMANTIC_ANALYSIS_ENGINE.md`
- `01_docs/operations/semantic_analysis_engine/previous_project_review.md`

Postgres and OmniCRM runtime artifacts:

- `01_docs/operations/postgres_knowledge_base_review/IMPORT_CONTRACT.md`
- `01_docs/operations/postgres_knowledge_base_review/import_reports/2026-07-01_reimport_619_snapshot.md`
- `/home/sergey/omni-crm/docs/architecture/KNOWLEDGE_BASE_VIEWER_CONTRACT.md`
- `/home/sergey/omni-crm/docs/architecture/KNOWLEDGE_BASE_MEDIA_CONTRACT.md`
- `/home/sergey/omni-crm/docs/operations/KB_LEGACY_IMAGE_MIGRATION_DRY_RUN.md`
- `/home/sergey/omni-crm/scripts/knowledge-base/migrate-legacy-images-to-nextcloud.mjs`
- `/home/sergey/omni-crm/scripts/knowledge-base/backfill-legacy-statement-media-links.mjs`

## Corpus Shape

The working conversation often called the source set "20 instructions" because several files had earlier DOCX/PDF variants and intermediate PDF-derived artifacts. The normalized canonical/import corpus is smaller and more precise:

- `17` source documents in the knowledge-base import contract;
- `16` current raw DOCX files in `raw/`;
- `17` extracted Markdown files in `extracted/`;
- `158` source chunks;
- `619` atomic statements;
- `14` canonical clusters;
- `150` statement relations;
- `117` image inventory rows;
- `236` statement-image links;
- `0` extraction errors in the final snapshot;
- `25` coverage/review warnings, mostly deliberate review gates.

The difference between "files we handled" and "canonical source documents" matters. A product must treat source normalization as its own stage: duplicate formats, retired PDFs, replaced DOCX versions, and ignored files must be represented explicitly, not hidden inside extraction results.

## Factual Pipeline

### 1. Corpus Inventory

The process started with a stable source inventory. Each source received:

- `source_document_id`, for example `doc_014`;
- `source_file`;
- file format;
- document type;
- primary topic;
- target roles;
- processing status;
- comments about source quality or expected review.

This was not clerical work. The inventory became the root identity map for every later artifact: chunks, statements, images, clusters, coverage rows, Postgres sources, and OmniCRM viewer records.

Product requirement: no file should enter extraction without a source registry row and stable source identity.

### 2. Text Extraction

DOCX files were converted to Markdown-like text. The usable extraction preserved enough structure for semantic work:

- headings;
- paragraphs;
- lists;
- image references;
- some HTML tables.

PDF-derived artifacts were intentionally retired for `doc_014` and `doc_017` after quality checks showed that the DOCX versions were the safer working sources. This is important: the pipeline did not blindly accept every extracted text. It chose the working source per document.

Product requirement: extraction must produce both text and a source-quality assessment. The output is not "good" just because text exists.

### 3. Image Extraction And Inventory

Images were extracted separately from text. For DOCX, embedded media came from `word/media`. For visual-heavy documents, normalized page/scheme renders were created when raw embedded fragments were not meaningful by themselves.

The final visual inventory recorded:

- `image_id`;
- source file;
- raw or normalized file name;
- media reference;
- image type;
- topic and roles;
- width and height;
- caption;
- nearby text;
- source anchor;
- linking bucket;
- review status.

The image inventory separated several classes:

- useful photos;
- diagrams and schemes;
- technical-card row images;
- decorative or unclear fragments;
- full-page visual review renders.

The main rule was stable throughout the work: an image does not create a technical fact by itself. It can illustrate a text-backed statement, or it can become a manual review candidate if the fact lives only in the image.

Product requirement: visual artifacts need a first-class inventory and review status before they are linked to semantic statements.

### 4. Structure-Aware Chunking

The chunking step produced `source_chunks.jsonl`. Each chunk preserved:

- `chunk_id`;
- source identity;
- section path;
- chunk text;
- image markers;
- related, excluded, and review image ids;
- previous and next chunk ids;
- overlap context;
- review flags and review reasons.

The chunker used document structure first: headings, paragraph blocks, tables, image markers, and controlled overlap. This was a deliberate correction from the older interview project, where semantic boundary detection was LLM-assisted. For technical documents, source structure is more reliable than asking an LLM to decide where a section starts and ends.

Product requirement: chunking should be deterministic, reproducible, and source-structure aware. The model should not control chunk boundaries.

### 5. Preflight Before Extraction

For difficult documents, extraction did not start immediately. A preflight pass checked:

- whether extracted text was usable;
- whether tables were real semantic tables or layout tables;
- whether images were reliable evidence or only candidates;
- whether the source duplicated already extracted knowledge;
- whether the document needed table-aware, page-aware, or manual-review extraction;
- whether PDF artifacts should be ignored.

This was critical for `doc_012`, `doc_014`, and `doc_017`.

`doc_012` was table-heavy and visual-heavy, so it needed row-aware extraction plus a separate OCR/manual pass for image-only table facts.

`doc_014` was DOCX-based installation-process material with many images and overlap against `doc_015`; it needed dedupe gating and a later manual visual-link pass.

`doc_017` was not a normal text source at all. It was a visual schematic source where meaning lived in composed page-level diagrams, so it was processed as review-gated visual material rather than normal text-first extraction.

Product requirement: the pipeline needs a preflight classifier that recommends an extraction mode per source.

### 6. Atomic Statement Extraction

The core extraction unit was one source chunk. The model received one chunk and returned strict JSON:

- `coverage_summary`;
- `skipped_source_items`;
- `statements`.

Each statement had:

- stable `statement_id`;
- normalized statement text;
- statement type;
- roles;
- topic;
- source document and source chunk ids;
- section path;
- exact source quote;
- related image ids;
- visual review flag;
- risk level;
- confidence;
- review status;
- optional scope, condition, action, object, normalized terms, notes.

The extraction prompt enforced several hard rules:

- only extract what is explicitly written in the chunk;
- use previous/next context only for understanding, not as quote source;
- split lists into separate atomic statements;
- do not turn headings into statements;
- do not use generic filler phrasing;
- handle tables by row meaning, not isolated cells;
- do not create statements from images alone;
- mark safety-critical content as `safety_critical` and `review_required`;
- every source item must be extracted or explicitly skipped.

This was the main shift from summarization to semantic extraction. The output was not a summary, not a rewritten instruction, and not a questionnaire. It was a source-backed record set.

Product requirement: extraction must be schema-bound, quote-bound, and coverage-bound.

### 7. Runner, Validation, And Coverage Gates

The runner automated part of the extraction workflow:

- prepared run folders;
- selected chunks;
- generated prompts and JSON inputs;
- accepted raw model outputs;
- parsed JSON;
- validated schema;
- validated each statement;
- produced extraction errors;
- produced coverage warnings;
- promoted valid outputs into canonical artifacts only when gates passed.

The runner evolved during the project. The first batch looked valid, but audit found missing source items. Later versions added:

- `coverage_summary`;
- `skipped_source_items`;
- warnings for uncovered bullets/checklist items;
- warnings for headings extracted as facts;
- warnings for generic statements;
- warnings for table fragments without context;
- paragraph coverage detection, because interview-like sources may have few bullets and many meaningful prose sentences.

This was one of the most important engineering lessons. Counting statements is not enough. The pipeline must check whether source units were covered.

Product requirement: every extraction run must have a machine validation gate and a source coverage gate before canonical promotion.

### 8. Canonical Promotion

Statements were not automatically merged into the canonical file just because a model returned JSON. Promotion happened only after:

- parsing succeeded;
- schema validation passed;
- coverage warnings were resolved or intentionally accepted;
- manual review or audit accepted the batch;
- duplicates and overlaps were checked.

Canonical artifacts included:

- `atomic_statements.jsonl`;
- `statement_clusters.json`;
- `statement_relations.jsonl`;
- `statement_images.jsonl`;
- `source_coverage_report.jsonl`;
- `source_coverage_report.md`;
- `coverage_warnings.jsonl`;
- `extraction_errors.jsonl`.

Product requirement: "run extraction" and "promote to canonical" must be separate commands and separate states.

### 9. Deduplication, Relations, And Clustering

The pipeline did not simply delete duplicates. It preserved the fact that multiple sources can support the same or related knowledge.

The resulting canonical layer used:

- clusters for topic grouping;
- relations such as duplicate, related, example, and contextual links;
- source coverage overrides where a chunk was covered by existing statements instead of new ones.

This mattered especially for `doc_014`, which overlapped with `doc_015` and `doc_012`. The process added only genuinely useful new statements and marked duplicate-covered zones through coverage overrides.

Product requirement: dedupe should produce relations and coverage decisions, not just remove rows.

### 10. Visual Layer

The visual layer had three separate meanings, and the project only worked because they were kept separate.

First, image candidates at source/chunk level:

- extracted or rendered visual artifacts;
- linked to source document and nearby text;
- classified as ready, candidate, excluded, or manual review.

Second, accepted statement-image links:

- stored in `statement_images.jsonl`;
- linked a specific existing statement to a specific image;
- used link types like `visual_example`, `visual_context`, `diagram`, or `manual_ocr_source`;
- did not modify statement text or create new facts.

Third, review-gated visual candidates:

- used when a diagram itself was valuable but not safe to turn into a wiring instruction;
- `doc_017` created `7` `visual_review_candidate` statements;
- each candidate had a linked scheme image and `review_required`;
- these were imported for engineer review, not treated as approved evidence.

The `doc_012` OCR/manual pass shows another important pattern. Facts visible only in images were not extracted in the normal text batch. They were promoted only after a manual OCR transcript was explicitly added to the source/chunk layer, and then linked with `manual_ocr_source`.

Product requirement: visual processing must support at least four modes: illustration, evidence, OCR source, and review candidate.

### 11. Editorial Assembly

Some Markdown knowledge-base sections were assembled from canonical clusters. The rule was strict:

- facts come from atomic statements and clusters;
- images come from accepted `statement_images.jsonl` links;
- images illustrate facts and do not create them;
- editorial sections are not primary sources.

This rule was added because mixing images, statements, and editorial writing by hand quickly creates inconsistent sections.

Product requirement: generated or edited instructions must be downstream artifacts, never the primary canonical layer.

### 12. Postgres Import

The file-based canonical layer was imported into Postgres after the snapshot stabilized.

The importer loaded, in order:

- projects;
- corpora;
- import runs;
- sources;
- chunks;
- images;
- statements;
- clusters;
- statement-cluster links;
- statement relations;
- statement-image links;
- coverage/discrepancy metadata.

The final import snapshot had:

- `17` sources;
- `158` chunks;
- `117` images;
- `619` statements;
- `14` clusters;
- `619` statement-cluster links;
- `150` relations;
- `236` statement-image links;
- `1218` review tasks.

Natural keys made the importer idempotent. It did not invent new ids. It preserved `source_document_id`, `chunk_id`, `statement_id`, `cluster_id`, and `image_id`.

Product requirement: DB import must be deterministic, idempotent, and tied to a source artifact hash / git commit.

### 13. Review Queue Seeding

Review tasks were seeded from structured flags:

- `review_status = review_required`;
- `risk_level = safety_critical`;
- `visual_review_required = true`;
- downstream blocked status.

For safety-critical statements, downstream status was set to `blocked_for_instruction` until expert review.

This is the correct boundary: extraction can prepare knowledge, but it cannot approve safety-critical technical instructions.

Product requirement: the pipeline must automatically create review queues from risk and evidence flags.

### 14. Nextcloud Media Migration

The local image bank was migrated to managed media in OmniCRM:

- legacy extracted instruction images were uploaded to Nextcloud;
- media metadata was inserted into `kb.media_assets`;
- existing `kb.statement_images` links were backfilled into `kb.statement_media_links`;
- runtime serving became Nextcloud-first;
- disk paths remained only as fallback.

For `doc_017`, the script had to be extended because its images existed only as normalized page/scheme renders, not raw extracted files.

Product requirement: media must not remain as loose local files. The product needs managed storage, metadata, checksum validation, and statement-level links.

### 15. OmniCRM Review UI

OmniCRM became the human review surface:

- review queue;
- all statements;
- filters;
- statement detail;
- source context;
- images;
- status and review decisions.

The viewer contract intentionally keeps immutable evidence fields read-only:

- statement text;
- source quote;
- source chunk;
- source document;
- source file.

If a reviewer wants a better formulation, the system records a proposed rewrite, not a mutation of the original extracted evidence.

Product requirement: reviewers must work through decisions and rewrites, not direct edits to source evidence.

## What Was Manual

The work was only partially automated. Manual or semi-manual parts included:

- deciding which source version to trust;
- reading preflight results and choosing extraction strategy;
- excluding hiring/non-technical material from technical canonical extraction;
- running separate focused batches;
- reviewing model quality;
- changing prompts after failures;
- manually handling table-heavy and visual-heavy sources;
- selecting image links for `doc_014`;
- creating manual OCR transcripts for `doc_012`;
- creating page-aware visual review units for `doc_017`;
- deciding dedupe/coverage overrides;
- committing and importing snapshots;
- manually migrating and verifying some media states.

This does not mean the approach is weak. It means the real workflow is known now and can be turned into product stages.

## Product Proposal

The product should not start as "AI reads documents and makes a KB." That framing is too vague and unsafe for technical documentation.

The product should be:

```text
Source-backed semantic analysis system for technical documentation
```

It takes a corpus of DOCX/PDF/visual technical documents and produces a reviewable knowledge base:

- source registry;
- extracted text;
- visual inventory;
- source chunks;
- atomic statements;
- statement clusters;
- statement relations;
- image links;
- coverage report;
- review queues;
- importable DB snapshot;
- optional downstream instruction drafts.

## Product Architecture

Recommended components:

1. Project workspace manager

Creates and validates a project structure:

```text
raw/
extracted/
images/raw/
images/normalized/
chunks/
statements/
review/
exports/
```

It owns `project.yml` and stable ids.

2. Source ingest service

Registers files, detects duplicates and versions, assigns `source_document_id`, and records source status.

3. Text extractor

Converts DOCX/PDF into structured Markdown plus extraction quality metrics. It should classify extraction quality as `usable_text`, `table_heavy`, `visual_heavy`, `ocr_required`, or `blocked`.

4. Visual extractor

Extracts embedded images and page renders, computes dimensions/checksums, creates inventory rows, and classifies obvious decorative fragments.

5. Preflight classifier

Decides extraction mode per document:

- normal text-first;
- table-aware;
- paragraph-heavy;
- visual/manual;
- OCR/manual;
- duplicate/reference-only;
- blocked.

6. Chunk builder

Builds deterministic chunks with source ids, section paths, related image candidates, overlap context, and review flags.

7. Extraction orchestrator

Prepares model batches, sends requests through an API, stores raw model responses, collects results, and never promotes directly to canonical without validation.

8. Validation and coverage engine

Validates schema, exact quotes, ids, image refs, risk flags, coverage summaries, skipped items, duplicate source items, headings-as-facts, table noise, and uncovered paragraph candidates.

9. Canonical builder

Promotes accepted statements, keeps immutable statement ids, deduplicates, creates relations, clusters, coverage overrides, warnings, and source coverage reports.

10. Visual linker

Links images to existing statements as evidence, illustration, OCR source, or visual review candidate. It must never create text facts from images silently.

11. Review backend

Imports canonical artifacts into Postgres, seeds review queues, and exposes stable APIs for human review.

12. Review UI

Lets engineers review statements, source context, images, visual candidates, risk flags, duplicates, and proposed rewrites.

13. Exporter

Exports reviewed statements back to file snapshots, downstream instructions, search indexes, RAG corpora, and API-ready read models.

## Automation Roadmap

### Stage 1. Make current scripts into one CLI

Current state: many useful scripts exist, but orchestration is manual.

Target command shape:

```bash
semantic-kb init --project sveton --corpus electricians_knowledge_base
semantic-kb ingest
semantic-kb extract-text
semantic-kb extract-images
semantic-kb preflight
semantic-kb chunk
semantic-kb prepare-runs
semantic-kb collect-runs
semantic-kb validate
semantic-kb promote
semantic-kb import-postgres
semantic-kb seed-review
```

The product should support dry-run by default and explicit `--apply` for destructive or canonical-changing stages.

### Stage 2. Add document strategy detection

Preflight should become a structured JSON artifact, not only Markdown.

Example:

```json
{
  "source_document_id": "doc_017",
  "recommended_mode": "visual_review_candidate",
  "text_quality": "poor",
  "visual_quality": "page_level_required",
  "table_quality": "none",
  "duplicate_risk": "medium",
  "requires_human_gate": true
}
```

This lets the orchestrator refuse unsafe normal extraction for sources like `doc_017`.

### Stage 3. Automate model calls and run management

The current runner can prepare and collect, but the raw model-answer step was still largely manual.

The product needs:

- API-backed model runner;
- retry;
- rate limits;
- cost log;
- per-batch manifest;
- raw input/output archive;
- model/version metadata;
- reproducible run ids;
- partial rerun by failed chunk.

### Stage 4. Turn visual layer into a first-class workflow

Visual handling should have its own pipeline:

```text
extract images
  -> classify image
  -> connect to chunks
  -> detect decorative fragments
  -> OCR candidate images
  -> create visual review units
  -> link accepted visuals to statements
  -> migrate media
```

This should support:

- embedded DOCX image extraction;
- PDF/page render extraction;
- page-aware visual units;
- image OCR transcript attachment;
- statement-image link review;
- Nextcloud/media migration;
- checksum verification.

### Stage 5. Automate dedupe and clustering assistance

The product should not auto-delete duplicates. It should propose:

- exact duplicates;
- semantic near-duplicates;
- related statements;
- conflicting statements;
- cluster candidates;
- source coverage overrides.

Human or configured policy decides promotion for safety-critical technical content.

### Stage 6. Make Postgres import and review export standard

The Postgres layer should be a standard product target:

- idempotent import;
- schema migrations;
- import run metadata;
- review task seeding;
- review decision export;
- reviewed snapshot export back to files.

The current Sveton importer is a strong prototype, but it should move into the reusable engine or a dedicated review backend package.

### Stage 7. Add project templates

The product should ship templates for common corpora:

- technical instruction corpus;
- visual schematic corpus;
- table-heavy technical cards;
- interview transcript corpus;
- policy/regulation corpus.

Each template defines:

- statement types;
- roles;
- topics;
- risk rules;
- review rules;
- extraction prompt profile;
- visual rules;
- coverage heuristics.

## Minimal Viable Product

The smallest useful product is not a chatbot. It is a pipeline and review system.

MVP scope:

- project config;
- source inventory;
- DOCX text extraction;
- DOCX image extraction;
- deterministic chunking;
- strict atomic extraction with API calls;
- validation and coverage gates;
- canonical JSONL artifacts;
- basic image inventory;
- accepted/manual image links;
- Postgres import;
- review queue;
- read-only review UI integration.

Out of MVP:

- automatic final instruction writing;
- automatic safety approval;
- full visual reasoning over wiring diagrams;
- autonomous contradiction resolution;
- direct mutation of canonical statements by reviewers.

## Key Design Rules

1. Code owns the pipeline. The model only performs bounded tasks.
2. Every statement must be traceable to source document, chunk, and quote.
3. Visual facts must be separated from text-backed facts.
4. Safety-critical technical statements are blocked until expert review.
5. Canonical promotion is a gate, not a side effect of extraction.
6. Duplicate handling must preserve source support and relations.
7. Review decisions are append-only; extracted evidence remains immutable.
8. Postgres is a runtime/review layer, not the only source of truth.
9. Editorial instructions are downstream artifacts, not primary evidence.
10. The product should prefer explicit warnings over silent "best effort".

## Practical Next Steps

1. Update `/home/sergey/semantic-analysis-engine` from toolkit to CLI product skeleton.
2. Move or wrap Sveton-specific scripts behind config-driven commands.
3. Define `preflight_report.schema.json`.
4. Define `visual_asset.schema.json` and `statement_image_link.schema.json`.
5. Add API-backed extraction execution to replace manual raw-response placement.
6. Add test fixtures from `doc_012`, `doc_014`, and `doc_017` because they cover the hardest cases: tables, mixed DOCX text/images, and page-level visual schemes.
7. Move Postgres importer contract into reusable docs and keep Sveton mappings as one concrete project config.
8. Add reviewed snapshot export so OmniCRM review decisions can return to canonical artifacts.

## Product Boundary

The reusable product should live outside the Sveton domain repository.

Sveton should keep:

- source documents;
- domain configs;
- canonical artifacts;
- review decisions;
- editorial knowledge-base sections;
- business/project governance.

Semantic Analysis Engine should own:

- extraction/chunking/validation scripts;
- schemas;
- prompts;
- CLI orchestration;
- preflight and visual workflows;
- import/export adapters;
- test fixtures.

OmniCRM should own:

- review UI;
- media management UI;
- business-facing reviewer workflows;
- backend adapter to the KB Postgres schema.

This boundary keeps the engine reusable while preserving source traceability and business ownership in the domain project.
