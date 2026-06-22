# Batch 007: doc_010 qualification levels

Дата: 2026-06-22

Источник:

```text
Что_должен_знать_и_уметь_монтажник_каждой_ступени1_1.docx
```

Run:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260622_doc010_qualification_levels_v1
```

## Scope

Цель extraction: qualification levels, уровни самостоятельности, критерии допуска, что монтажник должен знать и уметь на каждом уровне.

Покрытые chunks:

- `doc_010_chunk_0001`: стажер и критерии перехода в монтажник-электрик;
- `doc_010_chunk_0002`: критерии перехода из монтажника-электрика в 1-й разряд;
- `doc_010_chunk_0003`: самостоятельность 1-го разряда и критерии перехода во 2-й разряд.

Источник не содержит отдельного полного раздела по 2-му разряду; в canonical перенесены только критерии перехода из 1-го разряда во 2-й разряд.

## Result

- Valid statements: `60`
- Extraction errors: `0`
- Coverage / quality warnings: `0`
- Promoted to canonical: `yes`
- Canonical before promotion: `387`
- Canonical after promotion: `447`
- Cluster: `C010 / qualification_levels`
- Statement copy: `batch_007_doc010_qualification_levels_statements.jsonl`

## Review Profile

- `35` statements: `important / extracted`
- `25` statements: `safety_critical / review_required`

Safety-critical statements are about independent монтаж, АКБ, инверторы, байпасные щиты, УЗО, резервные группы, стабилизаторы, автономные системы and admission to independent work. They are added to `safety_review_queue.md` as `SR017`.

## Importer Compatibility

Updated artifacts:

- `atomic_statements.jsonl`
- `statement_clusters.json`
- `statement_clusters.md`
- `source_coverage_report.md`
- `source_coverage_report.jsonl`
- `safety_review_queue.md`

No new `statement_relations.jsonl` rows were added in this pass: the overlaps with existing clusters are thematic, not exact duplicate/example relations.

No image links were added: `doc_010` promotion is text-only.
