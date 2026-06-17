# AGENTS.md

## Project Scope

This repository contains the operating materials, research artifacts, and knowledge-base build workflow for the Sveton project.

Primary active workstreams:

- electricians knowledge base;
- semantic extraction engine for atomic statements;
- future business / sales / commercial knowledge base from leadership interviews.

## Source Of Truth

For project rules and process details, use these files first:

- `01_docs/governance/GUIDE.md`
- `01_docs/operations/electricians_knowledge_base/EPIC_ELECTRICIANS_KNOWLEDGE_BASE.md`
- `01_docs/operations/electricians_knowledge_base/README.md`
- `01_docs/operations/semantic_analysis_engine/EPIC_SEMANTIC_ANALYSIS_ENGINE.md`

If these files disagree with older notes, follow the newer governance and epic documents.

## Mandatory Model-Selection Rule

Before every new task, next step, epic, or major decision:

1. Explicitly state the recommended model family and level.
2. Briefly explain why that level is appropriate.
3. Wait for explicit user confirmation.
4. Only then start execution.

Required format:

```text
Рекомендуемая модель: 5.4 / 5.5 / другая.
Уровень: средний / высокий / самый высокий.
Почему: краткое обоснование.
```

Exception:

- If the user explicitly asks to update this rule itself, the rule text may be edited immediately.

## Knowledge-Base Build Rules

Do not present a derived editorial document as if it were a primary source.

Keep a hard distinction between:

- `source-backed canonical knowledge`: atomic statements, clusters, source links, image links, coverage reports;
- `editorial composition`: assembled instructions, check-lists, training materials, and composite operational documents built on top of canonical knowledge.

When building or editing knowledge-base sections:

- preserve source traceability through `statement_id`;
- preserve image traceability through `image_id` where visual evidence exists;
- do not hide source-quality issues or contradictions;
- mark safety-critical technical content for review when needed.

### Editorial Section Assembly Methodology

All source-backed knowledge-base sections must be assembled with the same methodology as the existing sections.

Mandatory rules:

- Facts in editorial sections must come from `atomic_statements.jsonl` and the relevant canonical cluster, not from images or free-form interpretation.
- Approved images must come from `statement_images.jsonl`; raw extraction `related_image_ids` are not enough by themselves to create an editorial visual layer.
- Images never create new facts. They only illustrate already extracted canonical statements.
- Visual examples must be placed inline next to the relevant semantic subsection and linked statements, using the established pattern: image, `image_id`, and `statement_id -> image_id` links.
- Do not add a standalone top-level "visual layer" or image catalog to a section when the rest of the knowledge base uses inline visual examples.
- Manual image links are allowed only as a separate documented pass. Do not silently mix manual visual links into extraction-backed editorial sections.
- If a section needs a different visual presentation, update the methodology explicitly first; do not introduce a one-off format inside a single section.

## Semantic Extraction Rules

Do not run naive full-document summarization as a substitute for semantic extraction.

Preferred pipeline:

1. extract text;
2. chunk with structure awareness and overlap where needed;
3. extract atomic statements with source references;
4. validate structure and completeness;
5. deduplicate and cluster;
6. only then assemble editorial materials.

For new extractions:

- prefer separate focused chats for separate extraction runs;
- keep extraction work separate from editorial rewriting;
- treat noisy PDF extraction as review-required before promoting results into canonical knowledge.

## Current Editorial Coverage Rule

As of the current project state, the honest source-backed sections are tracked in:

- `01_docs/operations/electricians_knowledge_base/README.md`

If a target section has no dedicated canonical cluster yet, it must be labeled and treated as:

- editorial composition from existing clusters; or
- blocked pending new extraction from additional raw sources.

Do not imply stronger source coverage than actually exists.

## File And Workspace Notes

Key directories:

- `00_input/`: raw and extracted inputs;
- `01_docs/`: governed project documents and editorial knowledge-base outputs;
- `07_scripts/`: extraction and validation scripts.

Do not overwrite or delete user-authored materials unless explicitly asked.
Prefer additive updates with clear traceability.
