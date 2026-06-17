# Knowledge Base Review Workflow

Дата: 2026-06-18.

Beans task: `Sv-dhj`.

## 1. Purpose

This document defines how semantic statements become review tasks in Postgres.

The goal is to avoid manual file exchange with engineers. Reviewers should see a queue of concrete tasks in the future CRM viewer:

- what needs review;
- why it needs review;
- where it came from;
- what decision is expected.

## 2. Source Records

The review queue is seeded from immutable imported records:

- `kb.statements`;
- `kb.chunks`;
- imported statement metadata such as `risk_level`, `review_status`, `visual_review_required`, and `downstream_status`.

The seed step does not rewrite extracted statement text.

## 3. Task Types

Current seeded task types:

| Task type | Source condition | Meaning |
|---|---|---|
| `statement_review_required` | `kb.statements.review_status = 'review_required'` | The extraction is not approved as canonical business/technical knowledge until a reviewer checks it. |
| `technical_safety_review` | `kb.statements.risk_level = 'safety_critical'` | The statement contains safety-relevant technical content and needs expert validation. |
| `instruction_block_review` | `kb.statements.downstream_status = 'blocked_for_instruction'` | The statement must not be used in final instructions until expert review is complete. |
| `visual_evidence_review` | `kb.statements.visual_review_required = true` | Linked images/diagrams must be checked against the statement. |
| `source_chunk_review` | `kb.chunks.needs_review = true` | Source extraction quality or source document status needs manual review. |

Coverage/discrepancy review is handled by the same seeding layer when importer discrepancy rows or uncovered source chunks exist. The current imported snapshot has no hard importer discrepancies.

## 4. Downstream Status Rules

Current downstream statuses:

| Status | Meaning |
|---|---|
| `draft` | Imported statement is available as canonical draft knowledge but not approved for downstream use. |
| `blocked_for_instruction` | Statement is blocked from final instruction/checklist use until expert review. |
| `approved_for_training` | Reviewer approved the statement for training or explanation materials. |
| `approved_for_checklist` | Reviewer approved the statement for checklist use. |
| `approved_for_instruction` | Reviewer approved the statement for final operational instructions. |

Initial seed rule:

- all `safety_critical / review_required` statements are set to `blocked_for_instruction`;
- this includes the current `77` installation-process statements in `C009`.

## 5. Queue Priority Rules

Priority is assigned mechanically:

| Condition | Priority |
|---|---|
| safety-critical statement review | `critical` |
| blocked-for-instruction review | `critical` |
| visual review for safety-critical statement | `critical` |
| review-required important statement | `high` |
| source chunk review | `high` |
| visual review for non-safety statement | `high` |
| ordinary review-required statement | `normal` |

## 6. Review Task Statuses

Review task status is operational and separate from statement downstream status.

| Review task status | Meaning |
|---|---|
| `todo` | Task is waiting for reviewer action. |
| `in_review` | Reviewer has started the task. |
| `blocked` | Reviewer cannot decide because information is missing. |
| `approved` | Reviewer approved the item for the target use defined by the decision. |
| `needs_rewrite` | Statement meaning is useful, but wording must be rewritten. |
| `requires_manufacturer_docs` | Manufacturer/manual evidence is needed before approval. |
| `done` | Task is closed after a recorded decision. |

## 7. Reviewer Decisions

Reviewer decisions are append-only records in `kb.review_decisions`.

Allowed decision actions:

- `approve_for_training`;
- `approve_for_checklist`;
- `approve_for_instruction`;
- `block_for_instruction`;
- `needs_rewrite`;
- `requires_manufacturer_docs`;
- `ask_engineer`;
- `mark_duplicate`;
- `mark_conflict`;
- `reject`.

Decision rules:

- extracted statement text remains immutable;
- if wording must change, create a proposed rewrite instead of editing the original statement;
- every decision must preserve the source statement, source quote, chunk, and source file traceability;
- final instruction/checklist use requires explicit downstream approval.

## 8. Current Expected Queues

For the current imported snapshot:

- `206` statements require extraction review;
- `204` statements require technical safety review;
- `204` statements are blocked for instruction until expert review;
- `86` statements require visual evidence review;
- `5` source chunks require source-quality review;
- `77` `installation_process` safety-critical statements are included in the blocked-for-instruction queue.

The queue intentionally creates separate tasks for separate reasons. A safety-critical statement can appear in more than one queue because a reviewer may need to check extraction quality, technical safety, and visual evidence separately.
