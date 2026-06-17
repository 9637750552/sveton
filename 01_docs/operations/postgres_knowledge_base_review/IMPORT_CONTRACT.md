# KB Postgres Import Contract

Дата: 2026-06-18.

Beans task: `Sv-yzh`.

## 1. Purpose

This document defines how the current Sveton semantic extraction artifacts are imported into the Postgres KB review layer.

The goal is to make importer task `Sv-7sd` mechanical: no field mapping should be guessed during implementation.

## 2. Import Scope

Current import target:

- database: `sveton_kb_dev`;
- schema: `kb`;
- project: `sveton`;
- corpus: `electricians_knowledge_base`;
- config: `semantic_project.yml`.

Current input scale:

- `17` source documents;
- `146` chunks;
- `387` atomic statements;
- `9` clusters;
- `41` statement relations;
- `118` image inventory rows;
- `182` accepted or candidate statement-image links;
- `6` coverage overrides;
- `124` coverage report rows.

## 3. Source Of Truth Files

Machine-imported files:

- `semantic_project.yml`;
- `00_input/documents/electricians_knowledge_base/inventory.md`;
- `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`;
- `00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl`;
- `00_input/documents/electricians_knowledge_base/statements/statement_clusters.json`;
- `00_input/documents/electricians_knowledge_base/statements/statement_relations.jsonl`;
- `00_input/documents/electricians_knowledge_base/images/inventory.csv`;
- `00_input/documents/electricians_knowledge_base/statements/statement_images.jsonl`;
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_report.jsonl`;
- `00_input/documents/electricians_knowledge_base/statements/source_coverage_overrides.jsonl`.

File-only evidence for the first importer version:

- Markdown batch summaries;
- Markdown review notes;
- `safety_review_queue.md`;
- `safety_review_c009_installation_process.md`;
- `source_quality_issues.md`;
- editorial section markdown files.

These Markdown files should be referenced in importer summary/discrepancy output, but not parsed into structured review tables in the first importer version.

## 4. Import Order

Importer must load data in this order:

1. `kb.projects`.
2. `kb.corpora`.
3. `kb.import_runs`.
4. `kb.sources`.
5. `kb.chunks`.
6. `kb.images`.
7. `kb.statements`.
8. `kb.clusters`.
9. `kb.statement_clusters`.
10. `kb.statement_relations`.
11. `kb.statement_images`.
12. Coverage/discrepancy metadata for later review queue seeding.

`kb.review_tasks`, `kb.review_decisions`, `kb.review_events`, and `kb.proposed_rewrites` are not populated by this contract except where explicitly stated by the later review queue task `Sv-dhj`.

## 5. Identity And Natural Keys

Importer must be idempotent. Natural keys:

- project: `project_key`;
- corpus: `(project_id, corpus_key)`;
- source: `(project_id, corpus_id, source_document_id)`;
- chunk: `(project_id, corpus_id, chunk_id)`;
- image: `(project_id, corpus_id, image_id)`;
- statement: `(project_id, corpus_id, statement_id)`;
- cluster: `(project_id, corpus_id, cluster_id)`;
- statement relation: `(source_statement_id, target_statement_id, relation_type)`;
- statement image link: `(statement_id, image_id, link_type)`;
- import run: `(project_id, corpus_id, import_run_key)`.

Importer must not create new statement ids, chunk ids, image ids, or cluster ids.

## 6. `semantic_project.yml` Mapping

Import use:

- `project_id` -> `kb.projects.project_key`;
- `corpus_id` -> `kb.corpora.corpus_key`;
- all paths -> `kb.import_runs.source_summary`;
- config path -> `kb.import_runs.config_path`.

Recommended display names:

- `kb.projects.name`: `Sveton`;
- `kb.corpora.name`: `Electricians Knowledge Base`.

## 7. `inventory.md` -> `kb.sources`

The inventory table contains source document metadata.

Mapping:

- document number -> `source_document_id` as `doc_001`, `doc_002`, etc.;
- `Файл` -> `source_file`;
- `Формат` -> `source_format`;
- `Тип` -> `document_type`;
- `Основная тема` -> `topic`;
- `Роли` -> `roles`;
- `Статус` -> `status`;
- `Комментарий` and raw inventory row -> `metadata`.

Validation:

- every `source_document_id` referenced by chunks/statements must exist in `kb.sources`;
- every `source_file` referenced by chunks/statements must exist in `kb.sources`;
- duplicate source files are import errors.

## 8. `source_chunks.jsonl` -> `kb.chunks`

Mapping:

- `chunk_id` -> `chunk_id`;
- `source_document_id` -> `source_document_id`;
- `source_file` -> `source_file`;
- source lookup by `(project_id, corpus_id, source_document_id)` -> `source_id`;
- `topic` -> `topic`;
- `roles` -> `roles`;
- `section_path` -> `section_path`;
- `text` -> `chunk_text`;
- `related_image_ids` -> `related_image_ids`;
- `excluded_image_ids` -> `excluded_image_ids`;
- `review_image_ids` -> `review_image_ids`;
- `previous_chunk_id` -> `previous_chunk_id`;
- `next_chunk_id` -> `next_chunk_id`;
- `previous_context` -> `previous_context`;
- `next_context` -> `next_context`;
- `needs_review` -> `needs_review`;
- `review_reasons` -> `review_reasons`;
- full source row -> `raw_payload`.

Fields kept only in `raw_payload` in migration `001`:

- `source_format`;
- `source_type`;
- `source_status`;
- `extracted_path`;
- `page_start`;
- `page_end`;
- `char_start_approx`;
- `char_end_approx`;
- `text_char_count`;
- `media_refs`;
- `overlap_group_id`.

Validation:

- `chunk_id` must be unique in corpus;
- `source_document_id` must resolve to `kb.sources`;
- previous/next chunk ids, when present, must resolve inside the same corpus;
- image ids in `related_image_ids`, `excluded_image_ids`, `review_image_ids` should resolve after `kb.images` import; unresolved ids become discrepancy rows, not hard failure.

## 9. `images/inventory.csv` -> `kb.images`

Mapping:

- `image_id` -> `image_id`;
- `source_file` -> `source_file`;
- `file_name` -> `file_name`;
- `media_ref` -> `media_ref`;
- `image_type` -> `image_type`;
- `topic` -> `topic`;
- `roles` split by `|` -> `roles`;
- `status` -> `status`;
- `width` -> `width`;
- `height` -> `height`;
- `caption` -> `caption`;
- `source_anchor` -> `source_anchor`;
- `nearby_text` -> `nearby_text`;
- `linking_bucket` -> `linking_bucket`;
- full CSV row -> `raw_payload`.

Fields kept only in `raw_payload` in migration `001`:

- `source_key`;
- `related_section`;
- `notes`.

Validation:

- `image_id` must be unique in corpus;
- `width` and `height` must be integers or null;
- `source_file`, when present, should resolve to `kb.sources`; unresolved files become discrepancy rows.

## 10. `atomic_statements.jsonl` -> `kb.statements`

Mapping:

- `statement_id` -> `statement_id`;
- `statement` -> `statement_text`;
- `statement_type` -> `statement_type`;
- `topic` -> `topic`;
- `roles` -> `roles`;
- `source_document_id` -> `source_document_id`;
- `source_file` -> `source_file`;
- `source_chunk_id` -> `source_chunk_id`;
- source lookup -> `source_id`;
- chunk lookup -> `chunk_db_id`;
- `section_path` -> `section_path`;
- `source_quote` -> `source_quote`;
- `source_quote_is_exact` -> `source_quote_is_exact`;
- `related_image_ids` -> `related_image_ids`;
- `visual_review_required` -> `visual_review_required`;
- `risk_level` -> `risk_level`;
- `confidence` -> `confidence`;
- `review_status` -> `review_status`;
- `scope` -> `scope`;
- `condition` -> `condition`;
- `action` -> `action`;
- `object` -> `object`;
- `normalized_terms` -> `normalized_terms`;
- `extraction_notes` -> `extraction_notes`;
- full source row -> `raw_payload`.

`downstream_status`:

- default to `draft` during first import;
- do not infer final instructional approval from editorial markdown;
- later review/export tasks may update downstream status through review decisions, not by changing immutable statement text.

Validation:

- `statement_id` must be unique in corpus;
- `source_chunk_id` must resolve to `kb.chunks`;
- `source_document_id` and `source_file` must match the referenced chunk;
- `source_quote_is_exact` should be true for accepted current canonical statements;
- `risk_level`, `confidence`, and `review_status` must satisfy DB check constraints;
- image ids in `related_image_ids` should resolve to `kb.images`; unresolved ids become discrepancy rows.

## 11. `statement_clusters.json` -> `kb.clusters` and `kb.statement_clusters`

Cluster mapping:

- `cluster_id` -> `kb.clusters.cluster_id`;
- `title` -> `title`;
- `topic` -> `topic`;
- `notes` -> `summary`;
- full cluster object -> `raw_payload`.

Fields kept only in `raw_payload` in migration `001`:

- `source_files`;
- `primary_outputs`;
- `statement_count`;
- `statement_ids`.

Membership mapping:

- each `statement_ids[]` entry resolves to `kb.statements.id`;
- cluster resolves to `kb.clusters.id`;
- insert into `kb.statement_clusters` with `relation_type = 'member'`.

Important:

- top-level `statement_clusters.json.relations` is a path string to `statement_relations.jsonl`, not relation data;
- importer must load relation data from `statement_relations.jsonl`.

Validation:

- every cluster `statement_count` must equal actual `statement_ids` count;
- total assigned statement ids should equal canonical statement count;
- no statement id should be assigned to multiple clusters unless this is explicitly allowed later;
- missing statements are hard import errors.

## 12. `statement_relations.jsonl` -> `kb.statement_relations`

Mapping:

- `source_statement_id` -> lookup `kb.statements.id` -> `source_statement_id`;
- `target_statement_id` -> lookup `kb.statements.id` -> `target_statement_id`;
- `relation_type` -> `relation_type`;
- `notes` -> `notes`;
- full relation row -> `raw_payload`.

Fields kept only in `raw_payload` in migration `001`:

- `relation_id`;
- `group_id`.

`confidence`:

- import as null in migration `001`, unless future relation files add confidence.

Validation:

- source and target statements must exist;
- source and target must not be the same statement;
- duplicate `(source_statement_id, target_statement_id, relation_type)` is an idempotent no-op if payload is identical;
- payload mismatch for an existing relation is a discrepancy.

## 13. `statement_images.jsonl` -> `kb.statement_images`

Mapping:

- `statement_id` -> lookup `kb.statements.id`;
- `image_id` -> lookup `kb.images.id`;
- `link_type` -> `link_type`;
- `status` -> `review_status`;
- `rationale` -> `notes`;
- full source row -> `raw_payload`.

Fields kept only in `raw_payload` in migration `001`:

- `source_file`;
- `statement_source_chunk_id`;
- `image_source_chunk_id`;
- `confidence`;
- `raw_path`;
- `normalized_path`;
- `created_at`.

Validation:

- statement must exist;
- image must exist;
- source file should match statement/image provenance when available;
- duplicate `(statement_id, image_id, link_type)` is an idempotent no-op if payload is identical.

## 14. Coverage Files

`source_coverage_report.jsonl` and `source_coverage_overrides.jsonl` are imported as importer metadata/discrepancy inputs in `Sv-7sd`, not as first-class relational tables in migration `001`.

Use them to generate:

- import summary counts;
- uncovered chunk discrepancy rows;
- ignored/override notes;
- later review task seeds in `Sv-dhj`.

Mapping target for first importer:

- `kb.import_runs.source_summary.coverage_report`;
- `kb.import_runs.source_summary.coverage_overrides`;
- external discrepancy JSONL report generated by importer.

## 15. Markdown Review Files

Markdown review files stay file-only in the first importer version.

Reason:

- they are human-readable audit evidence;
- their structure is not stable enough for reliable parsing;
- importing them as structured decisions would risk creating fake review decisions.

Importer must reference their paths in import summary:

- `statements/review/*.md`;
- `safety_review_queue.md`;
- `safety_review_c009_installation_process.md`;
- `source_quality_issues.md`;
- batch summary markdown files.

Structured review tasks are seeded later from statement fields and coverage/discrepancy rules, not by parsing free-form Markdown review text.

## 16. Import Run Metadata

Each import run must record:

- `import_run_key`;
- `project_id`;
- `corpus_id`;
- source repository git commit;
- semantic engine git commit when available;
- DB schema version;
- config path;
- input file paths;
- input file hashes where practical;
- row counts for all imported artifacts;
- discrepancy counts;
- started/finished timestamps in generated summary.

DB table:

- `kb.import_runs.source_summary` stores machine-readable metadata.

Generated file:

- importer writes a deterministic import summary markdown or JSON under `99_tmp` during dry run;
- committed import reports should be placed under `01_docs/operations/postgres_knowledge_base_review/import_reports/` only after the import workflow is approved.

## 17. Discrepancy Report Contract

Importer must produce discrepancy rows with this shape:

```json
{
  "severity": "error|warning|info",
  "artifact": "atomic_statements.jsonl",
  "row_id": "doc_003_chunk_0001_stmt_001",
  "check": "missing_chunk",
  "message": "source_chunk_id does not resolve to kb.chunks",
  "related_ids": ["doc_003_chunk_0001"]
}
```

Hard errors block import:

- duplicate ids inside the same corpus;
- missing source for chunk/statement;
- missing chunk for statement;
- missing statement for cluster membership;
- invalid enum values rejected by DB constraints.

Warnings do not block import:

- image id referenced before accepted image-link pass;
- markdown review file not parsed;
- coverage row points to ignored/split/duplicate content;
- source file path exists in historical metadata but not in current import set.

## 18. Source-Of-Truth Rules

For initial import:

- canonical statements come from `atomic_statements.jsonl`;
- chunk context comes from `source_chunks.jsonl`;
- clusters come from `statement_clusters.json`;
- relation rows come from `statement_relations.jsonl`;
- images come from `images/inventory.csv`;
- statement-image links come from `statement_images.jsonl`;
- coverage status comes from coverage JSONL files;
- Markdown review files are evidence, not structured decisions.

Postgres is the operational review layer.

Repository files remain the reproducible canonical snapshot until export-back workflow is implemented and accepted.
