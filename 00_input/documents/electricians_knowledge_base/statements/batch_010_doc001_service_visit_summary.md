# Batch 010: doc_001 service visit semantic extraction

Дата: 2026-06-23

Источник: `doc_001 / Действия на сервисном выезде.docx`

## Scope

- chunk: `doc_001_chunk_0001`
- extracted text: `00_input/documents/electricians_knowledge_base/extracted/Действия на сервисном выезде.md`
- direct images: none
- visual context: added from already accepted cross-source image links

## Output

- Added `12` atomic statements: `doc_001_chunk_0001_stmt_001` through `doc_001_chunk_0001_stmt_012`.
- Added canonical cluster `C013 / service_visit`.
- Added `22` statement relations: `rel_0076` through `rel_0097`.
- Added `1` source coverage row for `doc_001_chunk_0001`.
- Added `6` coverage/review warnings for missing voltage thresholds, missing АКБ equalization procedure, undefined inverter modes, ambiguous condition scope, missing direct visual evidence, and internal duplicate voltage wording.
- Added `15` `statement_images.jsonl` visual-context rows using `11` already accepted cross-source images.
- Direct `doc_001` images still do not exist: the added visual layer is contextual and does not create new facts for `doc_001`.
- Added no extraction errors.

## Statement Groups

1. Service visit electrical checks: wire tightening in inverter terminals and boards.
2. Inverter cleaning: blowing out the inverter, and removing the inverter cover with repeat blowing when needed.
3. Inverter diagnostics: checking inverter settings and operation in all modes.
4. Battery checks: measuring/checking АКБ voltage, checking АКБ bolt tightness and condition, lubricating АКБ bolts when needed.
5. Balancer and equalization: checking balancer operation and performing АКБ equalization.
6. Reporting/media: photos and videos of equipment settings, measurements, and completed work.

## Review Flags

All technical `doc_001` statements are `risk_level=safety_critical` and `review_status=review_required`.

The reporting/media statement is `risk_level=important`, `review_status=review_required`, and `visual_review_required=true`.

Do not use these statements as final service instructions until expert technical review resolves the warnings.

## Visual Layer

The visual layer uses `link_type=visual_context` to distinguish cross-source illustrations from direct `doc_001` evidence.

Visual-context groups:

- АКБ / inverter connection context: `img_0061`
- inverter settings / commissioning context: `img_0082`
- inverter mode / final-test context: `img_0084`, `img_0085`
- balancer context: `img_0037`, `img_0038`
- АКБ equalization / jumper context: `img_0039`, `img_0040`
- photo-report examples: `img_0001`, `img_0002`
- board/pre-start context: `img_0078`
