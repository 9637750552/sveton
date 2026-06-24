# Preflight semantic extraction: doc_012 technical cards

Date: 2026-06-23

Source:

- `doc_012`
- `ЭЛК_2_1 техн.карты изделий..docx`
- document type: technical cards
- source status in inventory: `raw, extracted, chunked`

Model recommendation:

- recommended model: `5.5`
- level: high
- reason: the source is table-heavy and visual-heavy; extraction must preserve table row structure, avoid creating facts from images alone, and mark electrical assembly content for expert review.

Scope guard:

- This is preflight only.
- No canonical KB artifacts were intentionally edited by this preflight.
- Do not write `atomic_statements.jsonl`, `statement_clusters.json`, `statement_relations.jsonl`, `statement_images.jsonl`, `source_coverage_report.*`, `coverage_warnings.jsonl`, or `extraction_errors.jsonl` until a separate extraction batch is approved.

## 1. Source And Extracted Text Quality

Extracted text path:

- `00_input/documents/electricians_knowledge_base/extracted/ЭЛК_2_1 техн.карты изделий..md`

Observed extracted text shape:

- `168` lines / about `10.5 KB`.
- The main table structure is preserved as HTML `<table>`.
- The extracted Markdown contains `3` tables, `16` table rows, and `30` image tags.
- Headings found:
  - `Изготовление кабеля «Инвертор-щит»`
  - `Изготовление перемычек для АКБ`
  - empty bold separator
  - `Назначение матриц пресс-клещей (CTF) из набора инструмента монтажника.`

Text quality:

- Good enough for table-aware extraction from text cells.
- Not good enough for blind full-document summary.
- The extracted text keeps row order, operation text, many dimensions, and tool names.
- Several image captions generated from nearby text are shifted or misleading. Examples:
  - `img_0018` is visually about correct crimping, but the inventory caption points to the next gofr tube operation.
  - `img_0019` is visually the gofr tube/cable, but caption points to the marking-label operation.
  - `img_0023` / `img_0024` captions are reversed around cutting/stripping jumper cable operations.
- Therefore `related_image_ids` are useful as candidates, not as approved visual evidence.

## 2. Table Extraction Quality

DOCX table parse confirms the source has three tables:

1. `Изготовление кабеля «Инвертор-щит»`
   - Header columns: `№П\П`, `Этапы обработки`, `Графическое изображение`, `Инструменты`.
   - Rows cover:
     - cut cable `5Х4`, length `2 м`;
     - strip cable ends: one side `100 мм`, other side `200 мм`;
     - cable sheath cutting method with cable stripping knife;
     - strip conductors;
     - put on and crimp `4 мм` ferrules on all stripped conductors at both cable ends;
     - correct ferrule crimping criteria;
     - cut gofr tube `ф25`, length `1.7 м`, and put it on the prepared cable;
     - apply cable marking label at the gofr tube edge where conductor length is `100 мм`.

2. `Виды используемых перемычек`
   - A one-cell table listing jumper types:
     - АКБ jumper `0.1 м`, `ф25`, black;
     - АКБ jumper `0.1 м`, `ф35`, red;
     - АКБ jumper `0.3 м`, `ф25`, black;
     - АКБ jumper `0.7 м`, `ф25`, black;
     - АКБ jumper `0.7 м`, `ф25`, red;
     - АКБ jumper `1.4 м`, `ф35`, red, `Н/Н`;
     - АКБ jumper `1.4 м`, `ф35`, black, `Н/Ш`;
     - `и другие`.

3. `Изготовление перемычек для АКБ`
   - Header columns: `№П\П`, `Этапы обработки`, `Графическое изображение`, `Инструменты`.
   - Rows cover:
     - cut cable pieces by required task length and quantity;
     - strip insulation to required length, not longer than the ferrule sleeve;
     - put ferrule on stripped conductors;
     - set crimp matrices by ferrule diameter: `ф25 -> 25/16`, `ф35 -> 35/25`;
     - crimp ferrule;
     - cut `60 мм` heat-shrink, put it on the crimped ferrule, heat evenly until it fully wraps the ferrule sleeve.

Table risks:

- Row cells contain both process actions and parameters. One table row is not always one atomic statement.
- Several rows contain multiple atomic facts and must be split.
- Some facts are references to a job/task (`по заданию`) rather than fixed source parameters; those should preserve condition/scope instead of inventing a number.
- The chunker did not mark table chunks as `needs_review`, but they should be treated as `review_required` for extraction because of table + visual dependency.

## 3. Chunks

`doc_012` currently has `3` chunks:

| Chunk | Section path | Text chars | Images | Preflight status |
|---|---:|---:|---:|---|
| `doc_012_chunk_0001` | `Изготовление кабеля «Инвертор-щит»` | `2818` | `17 related`, `1 excluded` | extractable table text; safety/review required |
| `doc_012_chunk_0002` | `Изготовление кабеля «Инвертор-щит» > Изготовление перемычек для АКБ` | `1817` | `10 related` | extractable table text plus visual-only scheme candidate |
| `doc_012_chunk_0003` | `... > Назначение матриц пресс-клещей (CTF) ...` | `202` | `1 related` | visual-only matrix table; OCR/manual review required before facts |

Chunk preflight decision:

- Mark all three chunks as table-aware extraction scope.
- Treat all three as source-review candidates even though `needs_review=false` in current chunk metadata.
- `doc_012_chunk_0003` should not produce canonical facts from the image alone unless an OCR/manual source pass is explicitly approved.

## 4. Image Inventory And Visual Candidates

Image inventory:

- `27` image rows for `doc_012`.
- `img_0004` is already `exclude_candidate`.
- `img_0005` through `img_0030` are `candidate_for_linking` and `needs_classification`.
- Raw images exist under `00_input/documents/electricians_knowledge_base/images/raw/ЭЛК_2_1_техн.карты_изделий.__img_*`.
- No dedicated committed normalized/contact-sheet artifact for `doc_012` was found. Existing `elk2_contact_sheet.jpg` belongs to the earlier base UPS components source, not this technical-card source.

Visual candidate groups:

| Images | Meaning | Preflight decision |
|---|---|---|
| `img_0004` | small `2 м` cable fragment | keep excluded unless needed only as row illustration |
| `img_0005` | side cutters tool | candidate only for tool illustration |
| `img_0006`-`img_0010` | cable stripping lengths and cable knife use | candidate visual evidence, but link only after row-level statement exists |
| `img_0011`-`img_0013` | conductor stripping / stripper | candidate visual evidence |
| `img_0014`-`img_0018` | ferrules, crimping, correct crimp example | candidate visual evidence; captions require manual verification |
| `img_0019`-`img_0021` | gofr tube / marking / cable conductor colors | candidate visual evidence; `img_0021` may be label/color marking, not standalone fact unless text-backed |
| `img_0022` | АКБ jumper examples | candidate visual evidence for listed jumper types |
| `img_0023`-`img_0028` | jumper making operations and tools | candidate visual evidence; captions around cutting/stripping/matrix rows need manual verification |
| `img_0029` | "Подготовка проводов балансира" scheme | contains important visual text not extracted as text; OCR/manual pass required |
| `img_0030` | CTF press-matrix assignment table | contains table facts as image only; OCR/manual pass required |

Visual-link rule for this batch:

- Images do not create facts.
- For `statement_images.jsonl`, only link images where the extracted text already supports the statement and the image clearly illustrates the same row/operation.
- If a statement relies on text visible only inside `img_0029` or `img_0030`, do not create it in the normal semantic batch. Put it into an OCR/manual review candidate list first.

## 5. Expected Statement Groups

Recommended new/updated cluster:

- New cluster candidate: `technical_cards`.
- Purpose: concrete product technical-card operations, dimensions, tooling, and assembly parameters.
- Expected relation targets:
  - `C007 / ups_components`
  - `C008 / distribution_boards`
  - `C009 / installation_process`
  - `C010 / qualification_levels`
  - `C012 / uzo_installation` only if the extracted row explicitly involves UZO/reserve group; currently doc_012 itself does not provide UZO installation text.

Safe text-backed groups from `doc_012_chunk_0001`:

- Cable `Инвертор-щит` preparation:
  - cut `5Х4` cable to `2 м`;
  - strip cable ends to `100 мм` on one side and `200 мм` on the other side;
  - use cable stripping knife to cut external insulation according to the measurement from the previous step;
  - pull the knife toward the cable edge to cut insulation lengthwise;
  - before stripping, adjust blade extension to avoid damaging conductor insulation;
  - strip conductor ends;
  - put on and crimp `4 мм` ferrules on all stripped conductor ends at both cable ends;
  - correct crimping criteria: no bare conductor protrudes from under the ferrule skirt; stripped conductor length matches ferrule sleeve length;
  - cut `ф25` gofr tube to `1.7 м` and put it on prepared cable;
  - apply marking label at the gofr tube edge where conductor length is `100 мм`.

Safe text-backed groups from `doc_012_chunk_0002`:

- АКБ jumper nomenclature:
  - jumper variants listed above, preserving `и другие` as an open-ended note, not as a closed exhaustive list.
- АКБ jumper preparation:
  - cut cable pieces by task length and quantity;
  - strip cable insulation to required length, not longer than ferrule sleeve length;
  - put ferrule on stripped conductors;
  - set crimp matrices by ferrule diameter: `ф25 -> 25/16`, `ф35 -> 35/25`;
  - crimp ferrule;
  - cut heat-shrink to `60 мм`, place on crimped ferrule, heat evenly until full wrap of ferrule sleeve.

Visual-only / blocked groups:

- `img_0029`: preparation of balancer wires, including approximate `70 см`, stripping `20 мм` / `10 мм`, terminal block extraction, and color-order connection. These are safety-relevant and not adequately present in extracted text.
- `img_0030`: CTF matrix assignment table with section ranges and crimp profiles. These are table facts visible in image only.

## 6. Potential Duplicates And Relations

No exact duplicates found for doc_012-specific parameters:

- no existing canonical exact hit for `5Х4`;
- no exact hit for `гофротруба`;
- no exact hit for `ф25` / `ф35`;
- no exact hit for `термоусадка`;
- no exact hit for matrix mapping `25/16`, `35/25`.

Likely relations, not duplicates:

- `doc_015_chunk_0011_stmt_005`: existing simple 24 V system uses 5-core `4 мм2` `Инвертор-щит` cable. Relate to doc_012 statement about preparing/cutting `5Х4` cable.
- `doc_015_chunk_0011_stmt_006`: existing system includes АКБ jumpers. Relate to doc_012 АКБ jumper nomenclature and making operations.
- `doc_015_chunk_0013_stmt_001`: DC protection is mounted to positive АКБ terminal using `0.1 м`, `35 мм2` jumper. Relate to doc_012 listed jumper variants, especially `0.1 м ф35 красная`.
- `doc_015_chunk_0013_stmt_002`: positive inverter terminal is connected to DC protection with red `35 мм2`, `1.4-1.8 м` cable. Relate to doc_012 jumper/cable preparation if a matching statement is extracted.
- `doc_015_chunk_0014_stmt_003`: АКБ groups use комплектные jumpers by parallel/serial схемы. Relate to doc_012 АКБ jumper list and preparation steps.
- `doc_013_chunk_0018_stmt_001`-`003`: equalizing jumpers purpose and use with balancer. Relate to doc_012 jumper nomenclature; do not duplicate purpose if doc_012 only gives fabrication steps.
- `doc_013_chunk_0020_stmt_002`: jumper connection errors can lead to insulation fire. Relate as safety context for doc_012 jumper preparation and balancer-wire visual review.
- `doc_010_chunk_0001_stmt_006`: installer must know how to crimp terminals of different sections and their purpose. Relate to doc_012 crimping, matrix, ferrule steps.
- `doc_010_chunk_0001_stmt_007`: installer must mount cable route in cable channel or gofr. Relate to `ф25` gofr tube step.
- `doc_010_chunk_0001_stmt_010` and `doc_010_chunk_0002_stmt_004`: installer competence around АКБ groups, balancers, and equalizing jumpers. Relate to doc_012 jumper/balancer technical cards.

Possible `uzo_installation` relations:

- No direct UZO statement should be extracted from doc_012 based on current text.
- If a future visual/OCR pass confirms that `img_0021` or another visual fragment encodes reserve-line color/labeling for input/output conductors, relate to `C009 / installation_process` and maybe `C008 / distribution_boards`, but do not force a `C012 / uzo_installation` relation unless UZO-specific text appears.

## 7. Review Required And Safety Critical Zones

Set `risk_level = safety_critical` and `review_status = review_required` for statements involving:

- cable preparation for `Инвертор-щит`;
- conductor stripping dimensions;
- blade adjustment to avoid damaging conductor insulation;
- ferrule crimping criteria;
- АКБ jumper dimensions, colors, terminal types, and fabrication;
- matrix selection for ferrules;
- heat-shrink application on crimped terminals;
- balancer wire preparation and connection order;
- any statement that can affect DC/AC wiring, АКБ, inverter, bypass, reserve group, UZO, or electrical safety.

Potentially `important` rather than `safety_critical`:

- tool identification only, when not framed as a safety instruction;
- statement that a table contains examples of jumper types, if not used instructionally.

Extraction-review warnings to prepare if batch proceeds:

- `table_structure_review_required`: doc_012 facts are table-row dependent.
- `visual_caption_shift`: image captions/nearby text are not reliable enough for automatic approved links.
- `visual_text_not_extracted`: `img_0029` and `img_0030` contain factual tables/schemes not represented as source text.
- `source_quality_spelling`: source contains spelling issues such as `опресовать`, `длинной`; preserve source quote exactly but normalize terms in `normalized_terms`.

## 8. Coverage Rules For Table And Visual Chunks

Coverage should be row-aware, not chunk-summary-based.

Recommended coverage statuses:

- `covered_by_statements`: a text cell or row-level fact is represented by one or more source-backed statements.
- `covered_as_duplicate_or_relation`: row repeats an already covered component-purpose statement and should be related rather than duplicated.
- `visual_candidate_only`: image illustrates a text-backed row but is not approved as a fact source.
- `blocked_visual_text`: factual content exists only inside image and requires OCR/manual extraction before canonical import.
- `review_required_table_structure`: table row/cell structure is ambiguous or image captions are misaligned.
- `ignored_decorative`: decorative/small image fragment such as `img_0004`.

Coverage warnings likely needed:

- `doc_012_chunk_0001`: table structure and shifted captions; manual visual-link review required.
- `doc_012_chunk_0002`: table structure, shifted captions, and visual-only `img_0029` balancer scheme.
- `doc_012_chunk_0003`: visual-only matrix assignment table; no text-backed facts beyond title.

## 9. Recommended Table-Aware Batch Strategy

Batch A: text-backed table statements for cable `Инвертор-щит`

- Scope: `doc_012_chunk_0001`.
- Extract row-by-row.
- Split rows with multiple operations into separate atomic statements.
- Do not create image links yet except maybe low-risk candidate notes in `related_image_ids`.
- Expected output: technical-card statements under `technical_cards`, with relations to `installation_process` and `qualification_levels`.

Batch B: text-backed table statements for АКБ jumpers

- Scope: text-backed parts of `doc_012_chunk_0002`.
- Separate nomenclature statements from fabrication-operation statements.
- Preserve open-ended list wording: `и другие` means the list is not exhaustive.
- Expected output: `technical_cards` statements, related to `ups_components`, `installation_process`, and `qualification_levels`.

Batch C: visual review / OCR candidate pass

- Scope: `img_0029` and `img_0030` only.
- Do not merge into canonical extraction until explicitly approved.
- If approved, create separate source-reviewed statements with `visual_review_required=true`, `risk_level=safety_critical`, `review_status=review_required`.
- If not approved, record coverage warning `blocked_visual_text` and keep images as candidates only.

Batch D: relation and image-link pass

- After statements are accepted, add relations to C007/C008/C009/C010/C012 where warranted.
- Add `statement_images.jsonl` rows only for clear row-to-image matches.
- Keep unclear links as review candidates, not accepted links.

Batch E: coverage pass

- Add coverage rows only after statements and relation decisions are stable.
- Coverage must state whether each table row was covered by text statements, blocked for visual-only review, or ignored as decorative.

## 10. Preflight Decision

Proceed with extraction only after explicit approval.

Recommended first approved extraction scope:

- `doc_012_chunk_0001`
- `doc_012_chunk_0002` text-backed rows

Do not include in first semantic extraction batch:

- visual-only facts from `img_0029`;
- visual-only facts from `img_0030`;
- accepted `statement_images.jsonl` rows without a separate visual-link review pass.
