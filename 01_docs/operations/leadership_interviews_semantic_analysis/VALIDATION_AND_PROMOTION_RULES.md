# Business interview validation and promotion rules

Дата: 2026-07-02

## Назначение

Этот документ фиксирует правила, по которым extracted interview claims
проверяются и только затем продвигаются в canonical слой Business / Sales /
Commercial KB.

Extraction output не является canonical по умолчанию.

## Входы

Минимальный набор входов для validation run:

- `transcript_chunks.jsonl` или pilot-файл chunks;
- `interview_claims.jsonl` или pilot-файл claims;
- `interview_chunk_extraction_results.jsonl`, если проверяется coverage;
- per-interview speaker mapping sidecar, если mapping не встроен в chunks;
- schemas из `00_input/interviews/statements/`.

## Validation Gates

### Gate 1. JSON and schema validity

Каждая запись claims должна:

- быть валидным JSON;
- иметь все обязательные поля из `interview_claim.schema.json`;
- не иметь неописанных полей;
- использовать только разрешенные значения `claim_type`, `business_area`,
  `target_outputs`, `evidence_status`, `confidence`, `review_status` и
  `review_flags`;
- иметь уникальный `claim_id`.

### Gate 2. Source traceability

Каждый claim должен иметь:

- `source_interview_id`;
- `source_file`;
- `source_chunk_id`;
- `speaker_label`;
- `speaker_identity`;
- `speaker_role`;
- `speaker_mapping_confidence`;
- `start_timestamp`;
- `end_timestamp`;
- `source_quote`.

`source_quote` должен быть дословным непрерывным фрагментом текста из
соответствующего chunk. Редакторские сокращения внутри `source_quote` запрещены.

### Gate 3. Speaker mapping

Если speaker mapping подтвержден пользователем или sidecar manual override
помечен как confirmed, claim может использовать реальное имя и роль.

Если speaker mapping не подтвержден:

- `speaker_identity = needs_mapping`;
- `speaker_role = needs_mapping`;
- claim получает `review_status = review_required`;
- claim получает `speaker_mapping_required`.

Manual override для повторяющейся ошибки диаризации не должен сам по себе
создавать review queue.

### Gate 4. Technical boundary

Interview claims не превращаются в технические инструкции.

Если claim звучит как техническое правило, техническое ограничение,
характеристика оборудования, надежность, срок службы, ресурс, монтажное
условие или конфигурация:

- использовать `claim_type = technical_claim_needs_confirmation` либо
  `applicability_to_electricians_kb = needs_confirmation`;
- добавить `technical_confirmation_required`;
- оставить `review_status = review_required`.

### Gate 5. Public and commercial boundary

Claims требуют review, если они влияют на:

- публичные обещания;
- сайт, брошюру, презентацию или коммерческое предложение;
- цены, гарантию, сроки, надежность, проценты, ресурс или экономику;
- стратегические решения;
- спорное позиционирование.

Такие claims должны иметь один или несколько флагов:

- `marketing_claim_review`;
- `public_use_review`;
- `price_or_guarantee_review`;
- `strategy_claim_review`.

### Gate 6. Specialized records

Если `claim_type = objection`, поле `objection` должно быть заполнено.

Если `claim_type = sales_case`, поле `sales_case` должно быть заполнено.

Если `claim_type = qualification_question`, поле `discovery_question` должно
быть заполнено.

Если `claim_type = open_question`, поле `open_question` должно быть заполнено,
а `evidence_status` должен быть `open_question`.

## Review Queue Rules

Review queue формируется автоматически из claims, где:

- `review_status = review_required`;
- есть любой review flag;
- `confidence = low`;
- `speaker_identity = needs_mapping`;
- `claim_type = technical_claim_needs_confirmation`;
- `applicability_to_electricians_kb = needs_confirmation`;
- `source_quote` не найден в chunk;
- claim влияет на public/commercial outputs.

Review queue не переписывает source claim. Reviewer decision должен быть
append-only.

## Promotion Rules

Claim может быть продвинут в canonical `interview_claims.jsonl`, если:

1. прошел все validation gates;
2. имеет дословный `source_quote`;
3. имеет подтвержденный speaker mapping или явно принятую manual override;
4. не имеет блокирующих validation errors;
5. review либо не требуется, либо завершен отдельным reviewer decision;
6. technical claims не используются как technical KB facts без внешнего
   подтверждения.

Canonical import сохраняет исходный `claim_id`. Новые ids при promotion не
генерируются.

## Coverage Report Format

Coverage report должен показывать:

- source files / interviews covered;
- chunks covered;
- claims count;
- claims by type;
- claims by business area;
- claims by review status;
- claims by review flag;
- claims requiring technical confirmation;
- claims relevant to electricians KB;
- source chunks with zero claims;
- skipped source items by reason;
- validation errors and warnings.

## Promotion Outputs

После validation/promotion ожидаемые файлы:

- `00_input/interviews/statements/interview_claims.jsonl`;
- `00_input/interviews/review/review_queue.md`;
- `00_input/interviews/review/coverage_report.md`;
- позже: `statement_relations.jsonl`, clusters и editorial outputs.

## Current pilot decision

Для `interview_001` ручные поправки диаризации приняты:

- `SPEAKER_00 = Дмитрий`;
- `SPEAKER_03 = Сергей`.

Эти labels не являются причиной speaker review. Review остается только по
содержательным причинам.
