# Batch 011 Review Notes: doc_012 technical cards

Дата: 2026-06-23

## Review Result

Extraction accepted as source-backed canonical draft for text-backed table content only.

All technical statements require expert review before use as installation, fabrication, or training instructions.

## Quality Notes

- Extraction was table-aware and row-aware.
- Facts were extracted only from text cells and preserved HTML table text.
- No facts were extracted from images, filenames, image captions, image order, or visual interpretation.
- Source spelling and source units were preserved in exact quotes, including forms such as `длинной`, `опресовать`, `5Х4`, `ф25`, `ф35`, `25/16`, and `35/25`.
- Atomic statement `topic` is `ups_components` for schema compatibility; semantic cluster `C014` carries the intended `technical_cards` grouping.
- `statement_images.jsonl` was not changed because this batch did not include a manual visual-link review.

## Chunk Decisions

| Chunk | Decision | Notes |
|---|---|---|
| `doc_012_chunk_0001` | covered | `18` statements extracted from the cable `Инвертор-щит` table. |
| `doc_012_chunk_0002` | covered | `19` statements extracted from АКБ jumper list and fabrication table. |
| `doc_012_chunk_0003` | needs review | No statements extracted; `img_0030` is image-only matrix assignment material. |

## Safety Review

Safety-critical areas:

- cable `Инвертор-щит` fabrication;
- stripping dimensions `100 мм` and `200 мм`;
- blade adjustment before cable stripping;
- ferrule placement and crimping;
- correct crimping criteria;
- gofr tube `ф25`, `1,7 м`;
- АКБ jumper variants and fabrication;
- matrix selection `ф25 -> 25/16`, `ф35 -> 35/25`;
- heat-shrink application over crimped ferrules.

These statements should remain blocked from final instructional use until expert technical review.

## Relation Notes

Added relations connect `C014 / technical_cards` to:

- `C007 / ups_components`: АКБ jumpers, balancers, and related component context;
- `C009 / installation_process`: cable and jumper use during installation;
- `C010 / qualification_levels`: crimping, gofr work, АКБ/balancer competencies.

No direct `C012 / uzo_installation` relation was added because `doc_012` text does not contain UZO-specific facts.

## Visual/OCR Review Needed

The following image-only items were intentionally blocked:

- `img_0029`: appears to contain balancer-wire preparation text/scheme.
- `img_0030`: contains a CTF matrix assignment table.

These should be handled in a separate OCR/manual review pass. If promoted later, their statements must preserve `source_document_id=doc_012`, use explicit OCR/manual provenance notes, and remain `safety_critical/review_required` where technical.

## Statement Images

No accepted statement-image links were added.

Reason:

- image captions around doc_012 are shifted in several places;
- images can illustrate only already extracted text-backed facts;
- automatic linking would risk treating visual noise as source evidence.
