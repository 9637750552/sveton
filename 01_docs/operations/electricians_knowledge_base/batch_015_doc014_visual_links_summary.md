# Batch 015: doc_014 manual visual-link pass

Date: 2026-07-01

Source:

- `doc_014`
- `ЭЛК_3_1процесс монтажа.docx`
- source format: `DOCX`
- cluster: `C009 / installation_process`

## Result

- `doc_014` statements checked: `22`
- New atomic statements: `0`
- Existing atomic statements modified: `0`
- New `images/inventory.csv` rows: `10`
- New accepted `statement_images.jsonl` links: `16`
- `doc_014` statements with at least one accepted visual link: `15`
- `doc_014` statements left without visual link: `7`
- Meaningful image candidates reviewed: `24`
- Image candidates accepted: `10`
- Image candidates rejected/deferred: `14`
- Visual-only/manual-review zones retained: `3`
- Postgres import: not run

## Accepted Links

| statement_id | image_id | link_type | confidence | Why accepted |
|---|---|---|---|---|
| `doc_014_chunk_0001_stmt_001` | `img_0113` | `visual_context` | high | The image is adjacent to the source text for UPS placement and illustrates temperature-control context; the temperature range remains text-backed. |
| `doc_014_chunk_0001_stmt_002` | `img_0113` | `visual_context` | high | The image illustrates inverter/АКБ placement; the DC-wire length limit remains text-backed. |
| `doc_014_chunk_0001_stmt_003` | `img_0113` | `visual_context` | high | The image illustrates heating/radiator proximity context; the 1 m distance remains text-backed. |
| `doc_014_chunk_0001_stmt_004` | `img_0113` | `visual_context` | high | The image illustrates cabinet/air-circulation context; the prohibition remains text-backed. |
| `doc_014_chunk_0001_stmt_005` | `img_0113` | `visual_context` | high | The image illustrates the shared layout of rack, inverter, and shield; the placement requirement remains text-backed. |
| `doc_014_chunk_0001_stmt_006` | `img_0114` | `visual_example` | high | The image illustrates rack shelf variants next to the text-backed rack statement. |
| `doc_014_chunk_0001_stmt_007` | `img_0114` | `visual_example` | high | The image illustrates wide/narrow shelf variants; the distinction remains text-backed. |
| `doc_014_chunk_0001_stmt_008` | `img_0115` | `visual_example` | high | The image illustrates the protective panel referenced by the text-backed statement. |
| `doc_014_chunk_0001_stmt_008` | `img_0116` | `visual_example` | high | The image illustrates a self-tapping screw with press washer; it does not add a new fastening rule. |
| `doc_014_chunk_0001_stmt_010` | `img_0117` | `diagram` | high | The diagram illustrates fastening crossbars through lower holes, matching the nearby text-backed step. |
| `doc_014_chunk_0001_stmt_011` | `img_0118` | `diagram` | high | The diagram illustrates shelf placement, matching the nearby text-backed step. |
| `doc_014_chunk_0001_stmt_012` | `img_0118` | `diagram` | high | The diagram illustrates final fastening through upper holes, matching the nearby text-backed step. |
| `doc_014_chunk_0003_stmt_003` | `img_0119` | `diagram` | medium | The diagram gives balancer-wire visual context; wiring facts beyond the text-backed length-with-reserve statement were not promoted. |
| `doc_014_chunk_0005_stmt_001` | `img_0120` | `visual_example` | high | The image illustrates cable-channel entry into the bypass shield next to the text-backed drilling constraint. |
| `doc_014_chunk_0005_stmt_002` | `img_0121` | `visual_example` | high | The image illustrates factory hole markings next to the text-backed statement. |
| `doc_014_chunk_0006_stmt_001` | `img_0122` | `visual_context` | medium | The image illustrates the reverse-line route; terminal/wiring labels from the image were not promoted. |

## Statements Without Accepted Visual Link

- `doc_014_chunk_0001_stmt_009`: no sufficiently specific image was accepted for the abstract statement that rack assembly principle is universal.
- `doc_014_chunk_0001_stmt_013`: DC-protection/fuse images were not accepted for the fuse-window orientation statement without engineering visual review.
- `doc_014_chunk_0003_stmt_001`: balancer safe-place requirement has no direct non-ambiguous image.
- `doc_014_chunk_0003_stmt_002`: balancer visibility/reset-access requirement has no direct non-ambiguous image.
- `doc_014_chunk_0009_stmt_001`: priority-load selection is text-backed, but board diagrams contain visual-only labels and need manual engineering review.
- `doc_014_chunk_0009_stmt_002`: breaker identification is text-backed, but board diagrams contain visual-only labels and need manual engineering review.
- `doc_014_chunk_0009_stmt_003`: inverter nominal-power warning is text-backed, but no image directly illustrates the warning without adding new facts.

## Rejected Or Deferred Visual Candidates

Rejected/deferred meaningful candidates:

- `media/image24.png`: rack illustration was not specific enough for the universal assembly-principle statement.
- `media/image28.png`: DC-protection visual was not reliable enough for fuse-window orientation.
- `media/image69.jpeg`, `media/image70.jpeg`, `media/image71.jpeg`, `media/image72.png`, `media/image77.png`, `media/image78.jpeg`, `media/image79.jpeg`: balancer-wire preparation visuals mostly correspond to facts already covered by `doc_012` or would require image-only interpretation.
- `media/image81.png`, `media/image84.jpeg`: inverter clearance/installation visuals remain blocked by the ambiguous `Не допустимо / 20 мм` fragment.
- `media/image102.png`: one-phase bypass terminal scheme contains meaningful labels, but no new image-derived wiring facts were promoted.
- `media/image103.png`, `media/image104.png`: board-rework diagrams contain priority/non-priority and input/output labels that require manual engineering review.

Tiny 1-2 px images, arrows, layout fragments, and decorative crops were ignored and not added to `images/inventory.csv`.

## Why This Does Not Create New Facts

- Every accepted `statement_images.jsonl` row points to an existing `doc_014` statement from batch 014.
- Images were used only as `visual_example`, `diagram`, or `visual_context`.
- No statement text, source quote, risk level, or review status was changed.
- Visual-only labels from inverter clearance, bypass terminal wiring, and board-rework schemes remain manual-review material.

## Updated Artifacts

- `00_input/documents/electricians_knowledge_base/images/inventory.csv`
- `00_input/documents/electricians_knowledge_base/images/inventory.md`
- `00_input/documents/electricians_knowledge_base/images/raw/ЭЛК_3_1процесс_монтажа__img_*.png|jpeg`
- `00_input/documents/electricians_knowledge_base/images/normalized/elk3_1_installation_process_img_*.png|jpeg`
- `00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl`
- `00_input/documents/electricians_knowledge_base/chunks/summary.md`
- `00_input/documents/electricians_knowledge_base/statements/statement_images.jsonl`
- `00_input/documents/electricians_knowledge_base/statements/coverage_warnings.jsonl`

## Postgres Readiness

The snapshot is closer to Postgres import readiness: `doc_014` now has a limited accepted visual layer for reliable text-backed statements. Import should still preserve `review_status = review_required` for all `doc_014` statements and should not treat manual-review visual zones as canonical facts.
