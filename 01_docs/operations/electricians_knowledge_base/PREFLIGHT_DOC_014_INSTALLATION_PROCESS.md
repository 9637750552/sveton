# Preflight semantic extraction: doc_014 installation process

Date: 2026-07-01

Source:

- `doc_014`
- `ЭЛК_3_1процесс монтажа.docx`
- source path: `00_input/documents/electricians_knowledge_base/raw/ЭЛК_3_1процесс монтажа.docx`
- source format: `DOCX`
- topic: `Процесс монтажа`
- target roles: `монтажник`, `электрик`
- source status in inventory: `raw, pending_extraction`

Why DOCX and not PDF:

- The current working source for `doc_014` is the DOCX file.
- Earlier PDF-derived artifacts for `doc_014` were intentionally removed.
- This preflight does not restore PDF extraction, PDF chunks, or PDF page-render images.
- The temporary checks below are based on the DOCX package and a temporary DOCX-to-Markdown conversion only.

Model recommendation:

- recommended model for this preflight: `5.5`
- level: `high`
- reason: the task requires DOCX structure review, duplicate analysis against `doc_015`, visual-layer triage, and extraction strategy without modifying canonical artifacts.

- recommended model for a future extraction pass: `5.5`
- level: `highest`
- reason: future extraction will touch safety-critical electrical installation instructions, diagram-heavy evidence, and dedupe decisions against the existing `C009 / installation_process` cluster.

Scope guard:

- This is preflight only.
- Semantic extraction was not run.
- Canonical KB artifacts were not intentionally edited by this preflight.
- Do not write to `atomic_statements.jsonl`, `statement_clusters.json`, `statement_images.jsonl`, coverage reports, or review queues until a separate extraction batch is approved.
- Do not mix `doc_014` with `doc_017` in one extraction pass.

## 1. DOCX Source Check

The DOCX source exists:

```text
00_input/documents/electricians_knowledge_base/raw/ЭЛК_3_1процесс монтажа.docx
```

Observed file size: about `4.97 MB`.

Inventory row:

```text
doc_014 | ЭЛК_3_1процесс монтажа.docx | DOCX | обучение / инструкция | Процесс монтажа | монтажник, электрик | raw, pending_extraction
```

## 2. DOCX Extraction Snapshot

Temporary DOCX preflight extraction found:

- `100` top-level OOXML content blocks
- `99` paragraph blocks
- `94` non-empty text paragraphs
- `5` image-only paragraphs
- `1` Word table
- `6` rows in that Word table
- `106` embedded media files in `word/media/`
- `106` unique media hashes
- temporary Pandoc Markdown: `225` lines, `186` non-empty lines, about `10.5 KB`
- `56` image references in the temporary Markdown
- `45` unique image files referenced in the temporary Markdown

Observed extracted heading structure:

- `Выбор места установки ИБП`
- `Сборка стелажа`
- numbered rack assembly steps `1`, `2`, `3`
- `Сборка и подключение «защиты по постоянному току»`
- `Установка АКБ, подключение, и установка балансира`
- `Монтаж инвертора`
- `Подготовка байпасного щита`
- `Прокладка кабеля реверсивной линии`
- `Подключение проводов реверсивной линии в однофазном байпасном щите`
- `Переборка щита`

Text quality:

- DOCX text extraction is usable: there are normal text blocks, section headings, warnings, procedural steps, and short captions.
- The source is not clean prose. Many paragraphs are visual-layout fragments around images, arrows, and callouts.
- Several captions are preserved as text, but their attachment to the right image/diagram is not always structurally reliable.
- Some visual labels are mixed into heading lines, for example an image tag is merged into the DC-protection heading.
- The final board-rework section has meaningful text and diagram labels interleaved: `ВВОД`, `N`, `L`, `вход на инвертор`, `выход от инвертора`, priority/non-priority load labels.

Manual-check text risks:

- Do not treat every short extracted line as a standalone fact; many are diagram labels.
- The inverter-installation area contains a potentially confusing extracted fragment: `Не допустимо 20 мм.` Existing `doc_015` states a minimum inverter clearance of `20 см`. This must be manually checked against the visual source before any statement is created.
- Spelling noise is present (`стелаж`, `длинну`, `Запрещатется`, `опрессовать/опресовать` variants). Normalize only in statement text, not in source quotes.
- Captions and images should be reviewed together before image links are promoted.

## 3. Table Extraction Quality

Formal DOCX tables:

- `1`

The table is not a semantic data table. It is a layout table around small images and the short marker `5Х`.

Preflight decision:

- Do not run table-aware semantic extraction on this table as if it were row/column domain data.
- Treat it as visual/layout context for the rack assembly section.
- If the future extractor sees a table here, it should mark it `manual_review` and avoid creating row-level facts from empty cells or image-only cells.

## 4. Expected DOCX-Based Chunks

All future chunks should carry:

```text
source_document_id = doc_014
source_file = ЭЛК_3_1процесс монтажа.docx
source_format = DOCX
topic = Процесс монтажа
roles = монтажник, электрик
suggested_topic = installation_process
suggested_roles = electrician, installer
```

Recommended chunk plan:

| Chunk | Section | Expected extraction posture | Duplicate risk |
|---|---|---|---|
| `doc_014_chunk_0001` | `Выбор места установки ИБП` | text-backed extraction with visual/manual review | overlaps `doc_015` inverter/bypass placement, but has unique constraints: temperature `+5..28`, distance from heaters/pipes/radiators at least `1 м`, no unventilated cabinets |
| `doc_014_chunk_0002` | `Стеллажи, типы полок, защитные панели` | extract only clear text-backed facts; images illustrate rack variants | mostly unique detail under existing `C009` assembly scope |
| `doc_014_chunk_0003` | `Сборка стеллажа`, steps `1-3` | extract procedural facts only where text supports the step; keep images as candidates | mostly unique; should relate to `doc_015_chunk_0005_stmt_001` and `doc_015_chunk_0014_stmt_001` rather than duplicate them |
| `doc_014_chunk_0004` | `Сборка и подключение защиты по постоянному току` + balancer-wire preparation | split into two subscopes if needed; mark safety-critical | overlaps `doc_015_chunk_0013`; has unique details such as fuse insert orientation and balancer-wire preparation |
| `doc_014_chunk_0005` | `Установка АКБ, подключение, установка балансира` | text-backed extraction with safety review | overlaps `doc_015_chunk_0014`; unique details about balancer placement, visibility, reset access, and wire-length reserve |
| `doc_014_chunk_0006` | `Монтаж инвертора` | extract cautiously; manual check required for clearance labels | overlaps `doc_015_chunk_0014`; potential conflict/ambiguity around `20 мм` vs existing `20 см` |
| `doc_014_chunk_0007` | `Подготовка байпасного щита` | text-backed extraction; visual manual review for drill-entry examples | partly unique; relates to `doc_015_chunk_0015` |
| `doc_014_chunk_0008` | `Прокладка кабеля реверсивной линии` and one-phase bypass terminal connection | extract terminal/wiring facts only when text and diagram labels agree | overlaps `doc_015_chunk_0016`; visual labels likely need manual review |
| `doc_014_chunk_0009` | `Переборка щита` / priority load | text-backed extraction for load-selection warning; diagram facts manual review | overlaps `doc_015_chunk_0018`; unique warning that total priority load must not exceed inverter nominal power |

Chunking note:

- `doc_014_chunk_0004` may be split into `DC protection` and `balancer wire preparation` if the extractor needs smaller safety-review units.
- Image-only fragments and tiny decorative images should not become standalone chunks.

## 5. Visual Layer Assessment

Embedded media count:

- `106` embedded media files in the DOCX package.

Media shape:

- `45` unique files are referenced by the temporary Markdown.
- Many media files are tiny fragments: 1-2 px images, arrows, curves, shadows, and Word-composition pieces.
- Exact hash comparison against committed `doc_015` raw images found `0` exact matches. This does not prove semantic uniqueness; the same diagram can be re-exported or recomposed differently.

Images likely containing semantic facts or useful visual evidence:

| Media candidates | Meaning | Preflight decision |
|---|---|---|
| `image1.png` | installation place constraints: temperature, distance to АКБ, heater/radiator distance, bypass shield near inverter, no unventilated cabinet | candidate for future statement links after text-backed extraction |
| `image9.png`, `image24.png`, `image25.jpeg`, `image26.png`, `image27.png` | rack shelf variants, protective panels, and rack assembly steps | candidate for rack assembly statements; manual review for image/text alignment |
| `image28.png`, `image69.jpeg`, `image70.jpeg` | DC protection/fuse block context | safety-critical visual candidates; do not create facts from image alone |
| `image71.jpeg`, `image72.png`, `image77.png`, `image78.jpeg` | balancer wire preparation, crimping, ferrules, terminal block | candidate visual context; overlaps technical-card practices and requires manual review |
| `image79.jpeg`, `image80.png` | balancer placement and connection scheme | visual/manual review candidate |
| `image81.png`, `image84.jpeg` | inverter placement/clearance and allowed/disallowed variants | visual/manual review required because extracted text may mix labels |
| `image94.jpeg`, `image98.jpeg` | bypass shield cable-entry/drilling examples | candidate visual evidence for shield preparation, manual review required |
| `image101.png`, `image102.png` | reverse cable route and one-phase bypass terminal wiring | safety-critical visual candidates |
| `image103.png`, `image104.png`, `image105.png`, `image106.png` | board rework, input/output labels, priority vs non-priority loads | safety-critical visual candidates; future statements must be text-backed and reviewed |

Images to keep out of source-backed facts:

- tiny 1-2 px images
- arrows, curves, shadows, decorative rectangles
- repeated drawing fragments
- empty/near-empty layout placeholders

Visual-link rule:

- Images never create facts.
- If a fact exists only on a scheme/image, classify it as `visual/manual review candidate`, not as a normal text-backed statement.
- Future `statement_images.jsonl` links should be added only after a statement is supported by extracted text or manually reviewed visual OCR/source evidence.

## 6. Comparison With doc_015

Existing canonical state:

- `doc_015 / ЭЛК_3_Базовые_знания_Описание_этапов_монтажа_ред1_9.docx` is already extracted and chunked.
- It contributes `101` statements to `C009 / installation_process`.
- The editorial section `04_installation_process.md` is already assembled from `C009`.
- `77` `doc_015` installation-process statements are `safety_critical` and `review_required`.

Overlapping themes:

- general installation process and preparation
- UPS assembly
- rack / АКБ / inverter / bypass shield placement
- DC-protection connection
- balancer connection
- reverse cable line
- one-phase bypass shield wiring
- distribution-board rework and reserve group selection
- priority load / inverter input-output concepts

Potential duplicate zones:

- DC protection connected to АКБ and inverter plus cable cross-section/distance: overlaps `doc_015_chunk_0013`.
- АКБ installation on rack and relation to inverter: overlaps `doc_015_chunk_0014`.
- inverter placement, ventilation, and bypass shield proximity: overlaps `doc_015_chunk_0014` and `doc_015_chunk_0015`.
- reverse cable line / five-wire cable / input-output separation: overlaps `doc_015_chunk_0016`.
- reserve group and board rework: overlaps `doc_015_chunk_0018`.

Likely unique zones in `doc_014`:

- practical location-selection constraints:
  - room temperature `+5..28`
  - at least `1 м` from heating devices, pipes, collectors, and radiators
  - no unventilated cabinet installation
- rack-specific assembly details:
  - shelf type variants
  - protective panels
  - lower and upper fastening sequence
  - not tightening bolts before shelf placement
- DC-protection detail:
  - fuse insert should be installed with inspection window upward
- balancer-wire preparation:
  - use wires from the balancer connection kit
  - cut by actual balancer placement
  - strip and crimp according to instruction
  - connect wires to balancer terminal block by color order
  - remove terminal block from balancer before connecting
- balancer placement criteria:
  - safe place
  - visible indication
  - convenient reset access
  - wire length with small reserve
- bypass shield preparation:
  - cable-channel drilling not above the cable channel
  - for corrugated route, factory hole markings can be used
- board rework / load selection:
  - total priority load must not exceed inverter nominal power
  - priority vs non-priority load visual labeling

Preflight conclusion on duplicates:

- `doc_014` is not a clean replacement for `doc_015`.
- It is an overlapping, more practical/visual installation-process source.
- Future extraction should reuse `C009 / installation_process` and create new statements only for genuinely additional details, constraints, warnings, or clarified procedural steps.
- Duplicates should become relations or source support for existing clusters/statements, not parallel conflicting facts.

## 7. Extraction Risks

Major risks:

- diagram labels may be mistaken for standalone instructions;
- visual-only facts may be promoted without source-backed text;
- small decorative media may pollute image inventory and statement links;
- `doc_014` may duplicate already extracted `doc_015` facts;
- mixed text/image layout can attach a caption to the wrong image;
- safety-critical electrical facts require expert review before instructional use;
- the `20 мм` inverter-clearance fragment may conflict with existing `20 см` knowledge and must not be extracted without manual visual check.

Required future statement metadata:

- `source_document_id`: `doc_014`
- `source_file`: `ЭЛК_3_1процесс монтажа.docx`
- `source_format`: `DOCX`
- `topic`: `installation_process`
- `roles`: include `electrician`, `installer`
- safety-critical technical instructions: `risk_level = safety_critical`
- safety-critical technical instructions: `review_status = review_required`
- image-dependent facts: `visual_review_required = true`
- duplicates/supporting facts: link to existing `C009` coverage instead of creating competing statements

## 8. Recommended Batch Strategy

Recommended approach:

1. Build DOCX-based chunks for `doc_014` from the extracted DOCX text, not from any PDF artifact.
2. Run a text-first extraction only on the planned chunks, with `doc_015`/`C009` dedupe context in the prompt.
3. Start with the likely unique chunks:
   - location-selection constraints;
   - rack assembly;
   - balancer preparation/placement;
   - bypass shield preparation;
   - priority-load warning.
4. Process high-overlap chunks only if the runner can explicitly classify output as:
   - duplicate/support for existing `C009` statements;
   - unique detail under `C009`;
   - visual/manual review candidate.
5. Do a separate manual visual/OCR pass only for scheme-only facts after text-backed extraction is reviewed.

Do not run a blind full-document extraction that treats every extracted line and every image as fact-bearing.

## 9. Runner / Extractor Restrictions

Use these restrictions for the future extraction runner:

- input source must be the DOCX-derived text/chunks only;
- do not read or recreate deleted PDF-derived text, chunks, or page-render images;
- write outputs into an isolated run directory first, not directly into canonical artifacts;
- include `doc_015` canonical statements or cluster summary as dedupe context;
- require exact `source_quote` for every text-backed statement;
- reject statements whose only support is an embedded image unless they are explicitly routed to manual visual review;
- ignore tiny/decorative media and image fragments;
- mark all wiring, АКБ, DC, inverter, bypass, reserve-group, and distribution-board statements as `safety_critical` and `review_required`;
- preserve possible contradictions as warnings rather than resolving them silently;
- do not merge this batch with `doc_017`;
- do not update editorial sections until canonical statements, dedupe, and image links have passed review.

## 10. Can Semantic Extraction Start?

Yes, but only conditionally.

`doc_014` is ready for a controlled DOCX-based extraction pass if:

- chunks are generated from DOCX text with the metadata above;
- the runner has a dedupe gate against `doc_015` / `C009`;
- visual-only facts are routed to `manual_review`;
- safety-critical facts are marked `review_required`;
- outputs are staged in a new run directory before any canonical merge.

Recommended first extraction scope:

- extract unique text-backed operational details first;
- defer visual-only схемы and ambiguous clearance labels to a separate manual visual/OCR pass.

Not recommended:

- full blind semantic extraction over the whole DOCX without dedupe and visual-review controls.
