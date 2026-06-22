# Batch 012: doc_012 visual/OCR manual pass

Дата: 2026-06-23

Источник: `doc_012 / ЭЛК_2_1 техн.карты изделий..docx`

## Scope

- `doc_012_chunk_0002`
- `doc_012_chunk_0003`
- `img_0029 / media/image26.png`
- `img_0030 / media/image27.png`

This batch promotes only visible text from the two previously blocked images after a manual OCR transcript was added to the source/chunk layer.

## Output

- Added `16` atomic statements:
  - `doc_012_chunk_0002_stmt_020` through `doc_012_chunk_0002_stmt_030`;
  - `doc_012_chunk_0003_stmt_001` through `doc_012_chunk_0003_stmt_005`.
- Updated `C014 / technical_cards` from `37` to `53` statements.
- Added `12` statement relations: `rel_0113` through `rel_0124`.
- Added `16` accepted `statement_images.jsonl` rows with `link_type=manual_ocr_source`.
- Added normalized image copies:
  - `images/normalized/elk2_1_technical_cards_img_026.png`;
  - `images/normalized/elk2_1_technical_cards_img_027.png`.
- Updated source coverage so all `3` doc_012 chunks are `covered`.
- Added no extraction errors.

## Statement Groups

1. `img_0029`: preparation of balancer wires
   - use wires from the balancer connection kit;
   - determine balancer installation location and cut wire length;
   - strip and crimp according to instruction;
   - strip one end to `20 мм`, bend or make a loop, insert into a terminal, and crimp;
   - record approximate wire length `~70см`;
   - strip the other end to `10 мм` and put on a terminal;
   - connect prepared wires to the balancer terminal block by color order;
   - remove the terminal block from the balancer before connection.

2. `img_0030`: CTF press-matrix assignment table
   - isolated terminals/connectors: `0.5-6.0 мм²`, oval two-contour profile;
   - ferrules `НШВИ`, `НШВ`: `0.25-6.0 мм²`, trapezoidal profile;
   - ferrules `НШВИ`, `НШВ`: `6-16 мм²`, trapezoidal profile;
   - double-crimp auto terminals: `0.5-6.0 мм²`, petal two-contour profile;
   - copper terminals and sleeves: `0.5-10 мм²`, wedge profile.

## Review Flags

- All new statements are `risk_level=safety_critical`.
- All new statements are `review_status=review_required`.
- OCR statements are source-backed through explicit manual OCR transcript in the chunk text.
- The images are linked only to statements derived from their own OCR transcript.

## Boundary

This batch does not approve the rest of doc_012 row-level images as editorial visual examples. Those images remain candidate/review because nearby captions are shifted in the extracted DOCX text.
