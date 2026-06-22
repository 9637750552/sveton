# Batch 009 Review Notes: doc_009 UZO installation

Дата: 2026-06-23

## Review Result

Extraction accepted as source-backed canonical draft with mandatory safety review.

## Quality Notes

- The source is short and technically dense; all statements are safety-critical.
- The source has no images, diagrams, or media refs.
- Exact source quotes are preserved, including source typos where present.
- Statement `doc_009_chunk_0001_stmt_006` intentionally does not expand the phrase "в соответствии с п.1" into a free-form wiring scheme.
- Statement `doc_009_chunk_0001_stmt_010` normalizes the source typo `небходимо` in the statement while preserving the exact quote.
- Statement `doc_009_chunk_0001_stmt_012` normalizes the source typo `связаться в начальником` in the statement while preserving the exact quote.

## Potential Tension For Engineer Review

- `doc_009_chunk_0001_stmt_004` says reserve breakers can be distributed to one or several UZO.
- `doc_016_chunk_0006_stmt_004` says phases and neutrals of reserve consumers should be collected under one UZO during board rework.
- This is recorded as `cw_doc_009_002` and relation `rel_0067`; it should be resolved by expert review, not by rewriting either source-backed statement.

## Cluster And Relation Notes

New cluster `C012 / uzo_installation` is kept separate from `C008 / distribution_boards` and `C009 / installation_process` because `doc_009` is a focused safety-critical UZO installation method.

Main related clusters:

- `C008 / distribution_boards`
- `C009 / installation_process`
- `C010 / qualification_levels`
- `C002 / installer_roles`

## Visual Notes

No `statement_images.jsonl` rows were added. Existing images from other documents may be useful only in a separate documented visual-context pass; they are not evidence for new `doc_009` facts.
