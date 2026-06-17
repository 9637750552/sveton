# Review Queue Seed Report

Дата: 2026-06-18.

Beans task: `Sv-dhj`.

## Target

- database: `sveton_kb_dev`;
- schema: `kb`;
- project: `sveton`;
- corpus: `electricians_knowledge_base`;
- seed script: `07_scripts/seed_kb_review_tasks.py`.

## Seeded Queues

| Task type | Reason | Rows |
|---|---|---:|
| `statement_review_required` | `extraction_review_required` | 206 |
| `technical_safety_review` | `safety_critical_statement` | 204 |
| `instruction_block_review` | `blocked_for_instruction_until_expert_review` | 204 |
| `visual_evidence_review` | `visual_evidence_review_required` | 86 |
| `source_chunk_review` | `source_chunk_needs_review` | 5 |
| **Total** |  | **705** |

## Downstream Status

The seed updated `204` safety-critical review-required statements to:

- `downstream_status = 'blocked_for_instruction'`.

Post-seed statement status counts:

| Downstream status | Rows |
|---|---:|
| `blocked_for_instruction` | 204 |
| `draft` | 183 |

## Installation Process Pilot Block

The expected `77` `installation_process` safety-critical review-required statements are included in the blocked-for-instruction queue.

Current queue counts for `installation_process`:

| Task type | Rows |
|---|---:|
| `statement_review_required` | 77 |
| `technical_safety_review` | 77 |
| `instruction_block_review` | 77 |

## Idempotency Check

The seed SQL was executed twice.

Second execution result:

- downstream status updates: `0`;
- inserted review tasks: `0`;
- duplicate review task groups: `0`.

## Notes

- No review decisions were created.
- No proposed rewrites were created.
- Review tasks are operational queue records only.
- Engineers still need to make explicit decisions before any safety-critical statement can be approved for checklist or instruction use.
