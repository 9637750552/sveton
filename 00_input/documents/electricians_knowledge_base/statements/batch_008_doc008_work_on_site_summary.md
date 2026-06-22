# Batch 008: doc_008 work_on_site

Дата: 2026-06-22

Источник:

```text
Работа на объекте 2024 ред1_7.docx
```

Run:

```text
00_input/documents/electricians_knowledge_base/statements/runs/run_20260622_doc008_work_on_site_v1
```

## Scope

Цель extraction: работа на объекте, распределение действий между первым номером, вторым номером и стажером, правила контроля, самостоятельности, коммуникации с клиентом и сдачи оборудования.

Покрытые chunks:

- `doc_008_chunk_0002`: стандартный монтаж, первый номер + стажер;
- `doc_008_chunk_0003`: изменение порядка действий на усмотрение первого номера;
- `doc_008_chunk_0004`: первый номер 1-го разряда + второй номер;
- `doc_008_chunk_0005`: ответственность сотрудника 2-го разряда на выезде;
- `doc_008_chunk_0006`: пара 2-го и 1-го разрядов, самораспределение работ.

`doc_008_chunk_0001` не продвигался, потому что содержит только заголовок.

## Result

- Valid statements: `66`
- Extraction errors: `0`
- Coverage / quality warnings: `0`
- Promoted to canonical: `yes`
- Canonical before promotion: `447`
- Canonical after promotion: `513`
- Cluster: `C011 / work_on_site`
- Statement copy: `batch_008_doc008_work_on_site_statements.jsonl`
- New relations: `20`

## Review Profile

- `39` statements: `safety_critical / review_required`
- `25` statements: `important / extracted`
- `2` statements: `ordinary / extracted`

Safety-critical statements are about DC work boundaries, АКБ, балансир, инвертор, байпасный щит, щит клиента, резервная группа, имитация отключения and role permissions for trainee / second number work. They are added to `safety_review_queue.md` as `SR018`.

## Importer Compatibility

Updated artifacts:

- `atomic_statements.jsonl`
- `statement_clusters.json`
- `statement_clusters.md`
- `statement_relations.jsonl`
- `source_coverage_report.md`
- `source_coverage_report.jsonl`
- `safety_review_queue.md`

No image links were added: `doc_008` has no related approved images.
