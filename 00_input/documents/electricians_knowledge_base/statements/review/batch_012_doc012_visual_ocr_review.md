# Batch 012 Review Notes: doc_012 visual/OCR manual pass

Дата: 2026-06-23

## Review Result

Visual/OCR pass accepted as canonical draft for two previously blocked images:

- `img_0029`: preparation of balancer wires;
- `img_0030`: CTF press-matrix assignment table.

The pass remains technical-review gated. None of the new statements should be used as final installation or fabrication instruction before expert review.

## Method

- The visible image text was manually transcribed into the source/chunk layer.
- Atomic statements were extracted only from that manual OCR transcript.
- `source_quote` values are exact substrings of the updated chunk text.
- `statement_images.jsonl` links use `link_type=manual_ocr_source`.
- No additional facts were inferred from tools, product photos, row position, or visual interpretation beyond the transcribed text.

## Chunk Decisions

| Chunk | Decision | Notes |
|---|---|---|
| `doc_012_chunk_0002` | covered | Existing table statements plus `11` manual OCR statements from `img_0029`. |
| `doc_012_chunk_0003` | covered | `5` manual OCR statements from `img_0030`; previous `needs_review` coverage gap is closed. |

## Safety Review

Safety-critical areas:

- preparing and crimping balancer wires;
- color-order connection to the balancer terminal block;
- removing the balancer terminal block before connection;
- selecting press matrices by terminal type, section range, and crimp profile.

All new statements are `safety_critical/review_required`.

## Visual Links

Added `16` accepted image links:

- `11` links from `doc_012_chunk_0002_stmt_020`-`030` to `img_0029`;
- `5` links from `doc_012_chunk_0003_stmt_001`-`005` to `img_0030`.

These links are accepted only as OCR-source links for their own statements. They do not approve the rest of doc_012 images as editorial row illustrations.

## Residual Risk

- OCR text was readable, but the source is still image-derived; expert review is required.
- The approximate `~70см` value is retained as approximate and should not be treated as a fixed universal length without technical confirmation.
- The rest of the row-level technical-card images remain unapproved candidates because extracted captions are shifted.
