# Batch 010 Review Notes: doc_001 service visit

Дата: 2026-06-23

## Review Result

Extraction accepted as source-backed canonical draft with mandatory technical safety review.

## Quality Notes

- The source is short and checklist-like; each bullet was preserved as an atomic statement.
- The two source bullets about АКБ voltage were preserved separately for traceability and linked with `duplicate_of`.
- The extraction does not add voltage thresholds, bolt torque values, lubricant type, inverter mode lists, shutdown/startup sequence, or АКБ equalization procedure.
- The source has no images, diagrams, media refs, or related image ids.
- Exact source quotes are preserved with source punctuation and spacing.

## Coverage Warnings

- `cw_doc_001_001`: missing voltage thresholds for АКБ measurement/checking.
- `cw_doc_001_002`: missing АКБ equalization procedure.
- `cw_doc_001_003`: undefined scope of "all inverter modes".
- `cw_doc_001_004`: ambiguous scope of the condition "при выключенном инверторе".
- `cw_doc_001_005`: no direct visual evidence in `doc_001`; cross-source visual context was added after extraction.
- `cw_doc_001_006`: internal duplicate/near-duplicate between АКБ voltage measurement and voltage checking.

## Cluster And Relation Notes

New cluster `C013 / service_visit` is kept separate from `C009 / installation_process` and `C011 / work_on_site` because `doc_001` is a focused service checklist, not a монтаж sequence or role-distribution matrix.

Main related clusters:

- `C002 / installer_roles`
- `C003 / reporting`
- `C004 / photo_report`
- `C007 / ups_components`
- `C009 / installation_process`
- `C010 / qualification_levels`
- `C011 / work_on_site`

## Visual Notes

An explicit visual-context pass was added after extraction.

Added `15` `statement_images.jsonl` rows with `link_type=visual_context`:

- `doc_001_chunk_0001_stmt_001`: `img_0078`, `img_0061`
- `doc_001_chunk_0001_stmt_004`: `img_0082`
- `doc_001_chunk_0001_stmt_005`: `img_0061`
- `doc_001_chunk_0001_stmt_006`: `img_0061`
- `doc_001_chunk_0001_stmt_007`: `img_0061`
- `doc_001_chunk_0001_stmt_008`: `img_0084`, `img_0085`
- `doc_001_chunk_0001_stmt_009`: `img_0037`, `img_0038`
- `doc_001_chunk_0001_stmt_010`: `img_0039`, `img_0040`
- `doc_001_chunk_0001_stmt_011`: `img_0061`
- `doc_001_chunk_0001_stmt_012`: `img_0001`, `img_0002`

These images are cross-source contextual illustrations from already accepted visual links. They are not direct evidence from `doc_001`, do not create new facts, and do not resolve the technical review warnings by themselves.
