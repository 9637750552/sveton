# Preflight semantic extraction: doc_017 distribution board rework

Date: 2026-07-01

Source:

- `doc_017`
- `ЭЛК_5 - Переборка щитов_1.0.docx`
- source path: `00_input/documents/electricians_knowledge_base/raw/ЭЛК_5 - Переборка щитов_1.0.docx`
- source format: `DOCX`
- topic: `Переборка щитов`
- target roles: `монтажник`, `электрик`, `инженер ГО`
- source status in inventory: `raw, pending_extraction`

Why DOCX and not PDF:

- The DOCX file is now the only working source for `doc_017`.
- Earlier PDF-derived artifacts for `doc_017` were intentionally removed.
- Preflight must not restore old PDF extraction, chunks, or page-render image artifacts.
- This report is based only on the current Word source and temporary preflight QA outputs.

Model recommendation:

- for this preflight task: `5.4`
- level: `high`
- reason: enough for DOCX inventory, render QA, extraction-risk analysis, and chunk planning without running semantic extraction

- recommended model for a future extraction pass: `5.5`
- level: `highest`
- reason: the document is almost entirely diagram-driven, carries electrical wiring facts, and needs page-aware visual review instead of blind text-first extraction

Scope guard:

- This is preflight only.
- Semantic extraction was not run.
- Canonical KB artifacts must remain unchanged.
- Do not restore or recreate any deleted PDF-derived artifacts for `doc_017`.
- Do not mix `doc_017` with `doc_014` in the same extraction pass.

## 1. DOCX Extraction Snapshot

Temporary DOCX preflight extraction found:

- `270` OOXML paragraph blocks
- only `45` non-empty text blocks
- `0` Word tables
- `117` embedded media files
- `91` unique media hashes and `26` repeated/reused image fragments
- `6` rendered pages from the DOCX via Word PDF export for visual QA

Observed text shape:

- There are no normal prose sections and no stable instructional paragraphs.
- Extracted text is mostly short labels attached to diagrams:
  - `Ввод`
  - `N`
  - `Фаза на инвертор "in"`
  - `Фаза от инвертора "OUT"`
  - `A1`, `A2`
  - `PE`, `L`, `N`, `вход input`, `выход output`
  - terminal numbers `1..6`
- Some labels merge when two similar schemes sit on one page, for example `Ввод    Ввод` and `N    N`.

Preflight conclusion on plain/structured text:

- DOCX text extraction technically works.
- DOCX text extraction does not produce a normal text body suitable for standard text-first semantic extraction.
- The meaningful content lives in page-level composed wiring diagrams, not in standalone paragraphs.

## 2. Table Extraction Quality

Formal DOCX tables:

- `0`

What looks tabular but is not a DOCX table:

- terminal number groups `1..6`
- input/output legends `PE / L / N`
- repeated left/right scheme variants

Conclusion:

- There are no table objects to parse table-aware.
- Diagram labels should not be misclassified as tables.
- Any future extractor must treat these as visual schematic regions, not as table rows.

## 3. Visual Layer Assessment

Embedded image count:

- `117` embedded media files in `word/media/`

Visual structure:

- Most embedded images are small reusable component fragments, not complete standalone схемы.
- The largest media objects are breaker/contact module fragments, terminal blocks, and a wall-switch icon.
- The actual meaning appears only after Word composes many fragments plus short text labels on the page.

What contains semantic facts:

- Page-level schemes on pages `2-6` contain wiring relationships, output numbering, and input/output labeling.
- Raw embedded media files by themselves usually do not contain the full fact.
- Page `1` is mostly a component lineup and gives only weak visual context without a complete instruction.

Visual candidates for future statement linking:

- page `2`: two side-by-side shield rewiring schemes with `Ввод`, `N`, inverter input/output phase labels, and contactor coil labels `A1/A2`
- page `3`: single assembled rewiring scheme with the same key labels and branch layout
- page `4`: numbered outputs `1..6`, PE/N/input/output legend, and simplified lower scheme
- page `5`: alternate scheme variant with split numbered outputs and lower legend/module composition
- page `6`: alternate routing variant with repeated legend and direct conductor paths

Manual review requirement:

- Mark all page-level visual facts as `manual_review`.
- Do not create source-backed statements from raw component fragments alone.
- Do not create source-backed statements from a page image unless the fact is also tied to page-local text labels and manually checked.

Practical visual conclusion:

- The useful visual unit is the rendered page, not the raw embedded image file.
- Future `statement_id -> image_id` linking should be delayed until a page-zone or manual visual pass exists.

## 4. Text Quality And Extraction Risks

Normal text blocks:

- Not present in a meaningful instructional form.

Captions and labels:

- The main callout labels are preserved in extracted text.
- Labels are incomplete without the surrounding diagram geometry.
- Duplicate labels from parallel diagrams can merge into one extracted block.

Scheme/table mixing:

- No DOCX tables were mixed into prose.
- The real risk is different: visual schemes are decomposed into many media fragments and sparse labels.

Parts that require manual checking:

- every page-level wiring relation
- every mapping between numbered outputs and conductors
- every interpretation of `PE`, `L`, `N`, `input`, `output`
- every statement about inverter input/output phase routing
- every statement involving contactor coil terminals `A1/A2`
- any future interpretation of branch numbering or bus assignment

Primary extraction risks:

- `visual_only_structure`: most facts are carried by layout, arrows, and line routing
- `fragmented_media`: raw `word/media/*` objects do not equal usable semantic images
- `label_merge`: repeated labels on the same page merge in plain text extraction
- `no_table_objects`: numbered scheme elements may be mistaken for tables
- `safety_critical_wiring`: wrong interpretation would create unsafe electrical statements

## 5. Recommended DOCX-Based Chunking

Recommended chunk basis:

- chunk by rendered page and scheme variant, not by plain extracted text blocks

Suggested chunks:

| Chunk | Scope | Preflight status | Notes |
|---|---|---|---|
| `doc_017_chunk_0001` | Page 1 component lineup / visual context | `manual_review_only` | component inventory only; weak source for statements |
| `doc_017_chunk_0002` | Page 2 left scheme | `review_required` | input, neutral, inverter input/output phase, contactor coil labels |
| `doc_017_chunk_0003` | Page 2 right scheme | `review_required` | similar topology with variant routing; keep separate to avoid label merge |
| `doc_017_chunk_0004` | Page 3 single assembled scheme | `review_required` | cleaner single-view topology than page 2 |
| `doc_017_chunk_0005` | Page 4 numbered outputs + lower legend scheme | `review_required` | output numbering `1..6`, PE/L/N legend, lower module context |
| `doc_017_chunk_0006` | Page 5 alternate split-output scheme | `review_required` | different output grouping and lower composed module |
| `doc_017_chunk_0007` | Page 6 alternate routing scheme | `review_required` | conductor-routing variant with repeated legend |

Chunk metadata guidance:

- `source_document_id = doc_017`
- `source_file = ЭЛК_5 - Переборка щитов_1.0.docx`
- `source_format = DOCX`
- `topic = Переборка щитов`
- `roles = монтажник, электрик, инженер ГО`

Cluster guidance:

- Do not create a new cluster by default.
- Future statements should land primarily in `distribution_boards`.
- Add relations to nearby clusters only when the extracted fact clearly touches them:
  - `installation_process`
  - `uzo_installation`
  - possibly component-level board context already covered by existing board-related clusters

## 6. Can Semantic Extraction Proceed?

Decision:

- `Not ready for normal text-first semantic extraction.`
- `Conditionally ready for a constrained page-aware visual extraction pass.`

Allowed only under these conditions:

- use DOCX as the only source
- chunk by rendered page/scheme, not by paragraph stream
- attach page render context to each chunk
- treat all resulting technical statements as review candidates
- do not infer facts from raw component fragments
- do not infer facts from line color alone without page-local labels and manual confirmation

If those conditions are not available:

- keep `doc_017` blocked for extraction

## 7. Runner / Extractor Restrictions

Required restrictions:

- `DOCX-only`: ignore all deleted PDF-derived material
- `page-aware`: use rendered page images as the primary semantic unit
- `no raw-media fact extraction`: `word/media/*` files are context fragments, not direct fact sources
- `manual_review`: all extracted statements from this document start as `review_required`
- `safety flag`: all wiring, conductor routing, terminal assignment, inverter input/output, bus, contactor, PE/L/N statements start with `risk_level = safety_critical`
- `no auto-cluster creation`: default to existing `distribution_boards` cluster family
- `no doc_014 mixing`: do not merge evidence from `doc_014` into `doc_017` statements during the first pass
- `no image-only claims`: if a fact exists only through geometry or a visual route without explicit text support, keep it as visual/manual review candidate

Recommended extractor behavior:

- one page or one scheme variant per prompt
- include a compact extracted-label list with the page render
- store warnings when left/right labels duplicate or merge
- preserve uncertainty instead of normalizing ambiguous conductor routes

## 8. Recommended Batch Strategy

Recommended batch shape:

1. Single-document batch only for `doc_017`.
2. Build page-based chunks from the DOCX render, not from old PDF chunks.
3. Use a visual/manual extraction prompt, not a prose summarization prompt.
4. Keep page `1` as visual context unless a human reviewer confirms it supports component-identification statements.
5. Extract pages `2-6` separately with explicit uncertainty capture.
6. Run a manual review pass before any canonical promotion or image linking.

Recommended review focus:

- conductor source and destination
- branch numbering `1..6`
- PE/L/N input/output assignment
- inverter `input` vs `output` phase routing
- contactor and coil terminal interpretation

## 9. Final Preflight Conclusion

`doc_017` is found and usable as a DOCX source, and the old PDF path should stay retired.

The document is not a normal textual instruction. It is a visual schematic source assembled from many embedded image fragments plus short labels. Plain extraction is too weak for safe semantic import, formal tables are absent, and most meaningful facts require page-level visual interpretation.

Final readiness decision:

- `not ready` for standard semantic extraction
- `ready with conditions` for a DOCX-based, page-aware, manual-review-heavy extraction pass

Those conditions are strict:

- DOCX only
- page-level chunking
- no PDF artifact restoration
- no raw-image-only statements
- `review_required` plus `risk_level = safety_critical` for wiring-related statements
