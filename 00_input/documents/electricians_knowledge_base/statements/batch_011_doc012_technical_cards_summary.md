# Batch 011: doc_012 technical cards semantic extraction

Дата: 2026-06-23

Источник: `doc_012 / ЭЛК_2_1 техн.карты изделий..docx`

## Scope

- chunks:
  - `doc_012_chunk_0001`
  - `doc_012_chunk_0002`
  - `doc_012_chunk_0003`
- extracted text: `00_input/documents/electricians_knowledge_base/extracted/ЭЛК_2_1 техн.карты изделий..md`
- preflight: `01_docs/operations/electricians_knowledge_base/PREFLIGHT_DOC_012_TECHNICAL_CARDS.md`
- dedicated prompt: `00_input/documents/electricians_knowledge_base/statements/atomic_extraction_prompt_doc012_technical_cards.md`

## Output

- Added `37` atomic statements:
  - `doc_012_chunk_0001_stmt_001` through `doc_012_chunk_0001_stmt_018`
  - `doc_012_chunk_0002_stmt_001` through `doc_012_chunk_0002_stmt_019`
- Added canonical cluster `C014 / technical_cards`.
- Added `15` statement relations: `rel_0098` through `rel_0112`.
- Added `3` source coverage rows for `doc_012`.
- Added `5` coverage/review warnings:
  - table-structure review for `doc_012_chunk_0001`;
  - table-structure review for `doc_012_chunk_0002`;
  - image-only text not extracted for `img_0029`;
  - image-only text not extracted for `img_0030`;
  - no accepted statement-image links for doc_012 in this pass.
- Added no `statement_images.jsonl` rows.
- Added no extraction errors.

## Statement Groups

1. `doc_012_chunk_0001`: fabrication of cable `Инвертор-щит`
   - cut `5Х4` cable to `2 м`;
   - strip cable ends to `100 мм` and `200 мм`;
   - use cable stripping knife and adjust blade extension;
   - strip conductor ends;
   - apply and crimp `4 мм` ferrules;
   - check correct crimping criteria;
   - cut and apply gofr tube `ф25`, `1,7 м`;
   - apply cable marking label;
   - preserve text-backed tool references: бокорез, нож для разделки кабеля, стрипер, пресс-клещи.

2. `doc_012_chunk_0002`: АКБ jumper variants and fabrication
   - listed АКБ jumper variants by length, diameter, color, and terminal type;
   - open-ended `и другие` list marker;
   - cut cable pieces by task length and quantity;
   - strip insulation to required length, not beyond ferrule sleeve length;
   - install ferrule and crimp matrix;
   - preserve matrix mappings `ф25 -> 25/16` and `ф35 -> 35/25`;
   - crimp ferrule;
   - cut and heat-shrink `60 мм` sleeve over crimped ferrule.

3. `doc_012_chunk_0003`: no statements
   - chunk contains only heading text and `img_0030`;
   - matrix assignment facts are image-only and require OCR/manual review.

## Topic And Cluster Note

Atomic statements use `topic = "ups_components"` because the current `atomic_statement` validator does not allow `technical_cards` as a statement topic.

The semantic cluster is still `C014 / technical_cards`, which preserves the intended knowledge-base grouping.

## Review Flags

- All assembly, cable, conductor, ferrule, АКБ jumper, matrix, crimping, and heat-shrink statements are `risk_level=safety_critical` and `review_status=review_required`.
- Tool-only references are `risk_level=important` and `review_status=review_required`.
- No statements were extracted from image-only content.

## Coverage

- `doc_012_chunk_0001`: `covered`, `18` statements.
- `doc_012_chunk_0002`: `covered`, `19` statements.
- `doc_012_chunk_0003`: `needs_review`, `0` statements, OCR/manual review required.

## Visual/OCR Boundary

Images are not treated as source facts in this batch.

Blocked for separate pass:

- `img_0029`: visual scheme/text for balancer-wire preparation.
- `img_0030`: visual table for CTF press-matrix assignment.

No accepted `statement_images.jsonl` links were added because image captions and nearby text are not reliable enough for automatic linking.
