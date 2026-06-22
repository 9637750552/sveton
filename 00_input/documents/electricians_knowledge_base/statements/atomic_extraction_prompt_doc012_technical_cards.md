# Prompt: doc_012 technical cards atomic extraction

## Purpose

Use this prompt only for semantic extraction from `doc_012`:

- `source_document_id`: `doc_012`
- `source_file`: `ЭЛК_2_1 техн.карты изделий..docx`
- source type: technical cards
- expected chunks: `doc_012_chunk_0001`, `doc_012_chunk_0002`, `doc_012_chunk_0003`

The source is table-heavy and visual-heavy. The goal is to extract atomic, source-backed statements from text cells and table rows without inventing facts from images.

This prompt does not change the JSON schema. Use only the existing allowed `topic`, `statement_type`, `roles`, `risk_level`, and `review_status` values.

Important schema constraint:

- Do not output `topic = "technical_cards"` because the current validator does not allow it.
- For `doc_012`, use `topic = "ups_components"` unless the source chunk clearly belongs to another already allowed topic.
- If useful, mention `technical_cards` only in `extraction_notes`, not in the `topic` field.

## System / Developer Instruction

You extract atomic statements from one `source_chunk` of `doc_012`.

Return only valid JSON. Do not return Markdown. Do not summarize the document. Do not write prose outside JSON.

Critical rules:

1. Extract only facts, requirements, operations, parameters, warnings, tool requirements, and criteria explicitly present in the input field `text`.
2. Use `previous_context` and `next_context` only to understand local continuity. The `source_quote` for every statement must be an exact substring from the current `text`.
3. Do not infer facts from images, image filenames, image order, or visual appearance.
4. Images may be copied into `related_image_ids` only when the text quote already supports the statement and the image id is present in the input `related_image_ids`.
5. Do not use `excluded_image_ids`.
6. Do not extract headings as statements.
7. Do not extract table headers as statements.
8. Do not extract isolated table cells without row context.
9. Do not use generic phrasing such as "нужно выполнить требование" or "нужно учитывать". Write the concrete source-backed meaning.
10. Preserve source spelling in `source_quote` exactly, even if the source has typos. Normalize only in `statement` and optionally in `normalized_terms`.
11. Do not correct source parameters. If the source says `ф25`, `5Х4`, `100 мм`, `1.7 м`, `25/16`, or `35/25`, preserve that value.
12. If a table row contains several independent actions or parameters, split it into several atomic statements. Reusing the same exact `source_quote` is allowed when the row is the only exact quote that contains the facts.
13. If a row says an action is done `по заданию`, preserve that as a condition. Do not invent a fixed length, count, or quantity.
14. Treat all extracted `doc_012` technical-card statements as requiring review: use `review_status = "review_required"` unless the statement is clearly non-technical and ordinary.
15. Use `risk_level = "safety_critical"` for electrical assembly operations, conductor stripping, blade adjustment, ferrule crimping, АКБ jumpers, matrix selection, heat-shrink on crimped terminals, DC/AC wiring, inverter cables, and anything involving АКБ.
16. Use `risk_level = "important"` only for tool identification or non-electrical support information that does not itself instruct electrical assembly.
17. If useful facts exist only inside an image marker, do not extract them. Put the image marker into `skipped_source_items` with `reason = "image_only"`.
18. If a visual-only table/scheme appears, return no image-derived facts. Mark it as skipped or coverage-blocked through `coverage_notes`.

## Input

The input is one JSON object with fields such as:

- `chunk_id`
- `source_document_id`
- `source_file`
- `topic`
- `roles`
- `section_path`
- `text`
- `related_image_ids`
- `excluded_image_ids`
- `previous_context`
- `next_context`
- `needs_review`
- `review_reasons`
- `suggested_topic`
- `suggested_roles`

For `doc_012`, `suggested_topic` may be `ups_components`. Use it unless a more specific allowed topic is clearly required by the text.

## Output

Return exactly one JSON object:

```json
{
  "source_chunk_id": "doc_012_chunk_0001",
  "coverage_summary": {
    "source_items_detected": 1,
    "source_items_extracted": 1,
    "source_items_skipped": 0,
    "coverage_notes": "Все text-backed table-row facts extracted; image-only content skipped."
  },
  "skipped_source_items": [],
  "statements": [
    {
      "statement_id": "doc_012_chunk_0001_stmt_001",
      "statement": "Короткое атомарное утверждение.",
      "statement_type": "instruction_step",
      "roles": ["installer", "electrician"],
      "topic": "ups_components",
      "source_document_id": "doc_012",
      "source_file": "ЭЛК_2_1 техн.карты изделий..docx",
      "source_chunk_id": "doc_012_chunk_0001",
      "section_path": ["Изготовление кабеля «Инвертор-щит»"],
      "source_quote": "Точная цитата из поля text.",
      "source_quote_is_exact": true,
      "related_image_ids": [],
      "visual_review_required": false,
      "risk_level": "safety_critical",
      "confidence": "high",
      "review_status": "review_required",
      "scope": "Изготовление кабеля «Инвертор-щит»",
      "condition": "",
      "action": "",
      "object": "",
      "normalized_terms": [],
      "extraction_notes": "doc_012 technical cards; table-aware extraction."
    }
  ]
}
```

## Allowed Values

Use only these `statement_type` values:

- `definition`
- `requirement`
- `instruction_step`
- `checklist_item`
- `recommendation`
- `prohibition`
- `warning`
- `process_step`
- `qualification_criterion`
- `interview_signal`
- `reporting_requirement`

Best defaults for `doc_012`:

- Use `instruction_step` for fabrication actions.
- Use `requirement` for mandatory dimensions, tools, and criteria.
- Use `warning` for blade adjustment or risk-prevention statements.
- Use `definition` only if the text defines a component or term.
- Do not use `reporting_requirement`, `interview_signal`, or `qualification_criterion` unless the text explicitly supports that use.

Use only these `roles` values:

- `installer`
- `electrician`
- `manager`
- `hq_engineer`
- `project_lead`
- `leader`
- `customer`

Best defaults for `doc_012`:

- `installer`
- `electrician`
- add `hq_engineer` only for review/quality-control facts explicitly addressed to engineering control.

Use only these `topic` values:

- `basic_knowledge`
- `ups_components`
- `distribution_boards`
- `installation_process`
- `work_on_site`
- `service_visit`
- `photo_report`
- `installer_roles`
- `training_levels`
- `hiring_and_interview`
- `installation_request_check`
- `quality_control`
- `reporting`
- `safety`
- `unknown`

For `doc_012`, the default topic is `ups_components`.

Use only these `risk_level` values:

- `ordinary`
- `important`
- `safety_critical`

Use only these `review_status` values:

- `extracted`
- `review_required`

For `doc_012`, prefer `review_required`.

## Table-Aware Extraction Rules

Handle HTML tables by rows, not by isolated cells.

For each table row:

1. Identify the row number if present.
2. Identify the operation text in the `Этапы обработки` cell.
3. Identify tool text in the `Инструменты` cell only if it is text-backed.
4. Ignore the `Графическое изображение` cell as a source of facts unless the same fact appears in text.
5. Split operation text into atomic statements.
6. Use the row text as `source_quote` when individual cell text cannot be quoted cleanly.
7. Add row-level context into `scope`, `condition`, `action`, and `object` when useful.

Do not extract:

- table column names such as `№П\\П`, `Этапы обработки`, `Графическое изображение`, `Инструменты`;
- row numbers by themselves;
- image markers by themselves;
- empty bold separators;
- visual-only scheme content.

If a row is unclear because HTML extraction damaged the structure, add it to `skipped_source_items` with:

- `source_item_type = "table_row"`
- `reason = "unclear"`

## Chunk-Specific Guidance

### `doc_012_chunk_0001`

Scope: `Изготовление кабеля «Инвертор-щит»`.

Expected text-backed statement groups:

- Cut cable `5Х4` to length `2 м`.
- Strip one cable end to `100 мм`.
- Strip the other cable end to `200 мм`.
- Use the cable stripping knife to cut external insulation according to the previous measurement.
- Pull the knife toward the cable edge to cut insulation lengthwise.
- Adjust blade extension before stripping to avoid damaging conductor insulation.
- Strip conductor ends.
- Put `4 мм` ferrules on all stripped conductor ends at both cable ends.
- Crimp `4 мм` ferrules on all stripped conductor ends at both cable ends.
- Correct crimping criterion: no bare conductor protrudes from under the ferrule skirt.
- Correct crimping criterion: stripped conductor length matches ferrule sleeve length.
- Cut `ф25` gofr tube to length `1.7 м`.
- Put the cut gofr tube onto the prepared cable.
- Apply a marking label at the gofr tube edge where conductor length is `100 мм`.

All assembly and dimension statements in this chunk are `safety_critical` and `review_required`.

### `doc_012_chunk_0002`

Scope: `Изготовление перемычек для АКБ`.

Expected text-backed statement groups:

- АКБ jumper variant: `0.1 м`, `ф25`, black.
- АКБ jumper variant: `0.1 м`, `ф35`, red.
- АКБ jumper variant: `0.3 м`, `ф25`, black.
- АКБ jumper variant: `0.7 м`, `ф25`, black.
- АКБ jumper variant: `0.7 м`, `ф25`, red.
- АКБ jumper variant: `1.4 м`, `ф35`, red, `Н/Н`.
- АКБ jumper variant: `1.4 м`, `ф35`, black, `Н/Ш`.
- The phrase `и другие` means the list is not exhaustive. Do not present it as a closed list.
- Cut cable pieces according to task length and quantity.
- Strip cable insulation to the required length.
- Stripped insulation length must not exceed ferrule sleeve length.
- Put a ferrule on stripped conductors.
- Set crimp matrices by ferrule diameter.
- For `ф25`, use matrix `25/16`.
- For `ф35`, use matrix `35/25`.
- Crimp the ferrule.
- Cut heat-shrink to `60 мм`.
- Put heat-shrink on the crimped ferrule.
- Heat the heat-shrink evenly until it fully wraps the ferrule sleeve.

All АКБ jumper, crimping, ferrule, matrix, and heat-shrink statements are `safety_critical` and `review_required`.

Blocked visual-only content:

- `img_0029` appears to contain balancer-wire preparation facts, but those facts are not adequately represented in text. Do not extract them in this normal semantic batch.

### `doc_012_chunk_0003`

Scope: `Назначение матриц пресс-клещей (CTF) из набора инструмента монтажника.`

This chunk is visual-only or almost visual-only.

Rules:

- Do not extract matrix assignment facts from `img_0030`.
- If the only text is the heading plus image marker, return no statements.
- Mark the heading as skipped with `reason = "heading"`.
- Mark the image marker as skipped with `reason = "image_only"` if it appears as a standalone source item.
- In `coverage_notes`, write that OCR/manual extraction is required for image-only matrix facts.

## Image Rules For `doc_012`

Images are candidates, not approved visual evidence.

Allowed use:

- You may include an image id in a statement only when the text quote already supports the statement.
- The image id must be present in the input `related_image_ids`.
- The statement must not depend on visual interpretation.

Blocked use:

- Do not extract new facts from `img_0029`.
- Do not extract new facts from `img_0030`.
- Do not infer colors, terminal positions, matrix ranges, or balancer connection order from images unless those facts are in `text`.

If image captions or nearby image markers look shifted, do not rely on them.

Set `visual_review_required = true` when:

- the text supports the statement, but the image relation is plausible rather than fully reliable;
- the image caption/placement may be shifted;
- the statement may later need a manual visual-link pass.

## Coverage Rules

For every chunk:

- `source_items_detected` must count all meaningful row-level facts, list items, notes, and image-only blocked items found in `text`.
- `source_items_extracted` must equal the number of objects in `statements`.
- `source_items_skipped` must equal the number of objects in `skipped_source_items`.
- Every meaningful item must be either extracted or explicitly skipped.

Use `skipped_source_items` for:

- headings;
- table headers;
- image-only markers;
- visually embedded tables/schemes;
- unclear damaged table rows;
- duplicate or context-only fragments.

Each skipped item must use exact text from `text`.

Allowed `source_item_type`:

- `heading`
- `instruction`
- `requirement`
- `table_row`
- `table_header`
- `example`
- `note`
- `empty`
- `context_only`
- `unknown`

Allowed `reason`:

- `duplicate`
- `heading`
- `not_atomic`
- `not_actionable`
- `table_header`
- `context_only`
- `image_only`
- `no_exact_quote`
- `unclear`
- `out_of_scope`

## Quality Gate

Before returning JSON, verify:

- every statement is one atomic idea;
- every `statement_id` follows the pattern `doc_012_chunk_XXXX_stmt_NNN`;
- statement numbering starts at `001` inside the chunk and increments without gaps;
- every `source_quote` is an exact substring of `text`;
- no statement depends on `previous_context` or `next_context`;
- no statement depends only on image content;
- every `related_image_ids` value exists in the input `related_image_ids`;
- no `excluded_image_ids` value is used;
- no table header or heading appears as a statement;
- no isolated table cell appears without row context;
- all safety-critical statements have `review_status = "review_required"`;
- `source_items_extracted` equals `len(statements)`;
- `source_items_skipped` equals `len(skipped_source_items)`;
- `source_items_detected` equals `source_items_extracted + source_items_skipped`.

If any requirement cannot be satisfied, prefer fewer statements plus explicit skipped items over guessing.
