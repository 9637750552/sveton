# Business interviews semantic analysis pipeline

Дата: 2026-07-02

## Назначение

Этот документ фиксирует рабочий pipeline для анализа интервью руководства,
стенограмм разборов продаж и разговоров менеджеров в проекте Sveton.

Цель pipeline - создать пополняемую Business / Sales / Commercial Knowledge
Base, которую можно использовать для:

- консультаций менеджеров;
- обучения продавцов и профильных специалистов;
- разбора типовых проблемных случаев;
- обработки возражений;
- подготовки сайта, буклетов, КП и презентаций;
- фиксации бизнес-модели, клиентских сегментов и коммерческой логики;
- вторичной связки с базой электриков без подмены технических источников.

Подход строится как отдельный профиль `business_interviews` поверх общего
semantic-analysis подхода. Мы переиспользуем каркас технического pipeline,
но меняем предметную модель, chunking, типы утверждений и review-гейты.

## Границы проекта

Sveton repository хранит:

- исходные интервью и стенограммы;
- инвентарь интервью;
- speaker mapping;
- transcript chunks;
- canonical interview claims;
- review artifacts;
- downstream business, sales and commercial knowledge-base outputs.

Semantic Analysis Engine должен в перспективе хранить переиспользуемые:

- схемы;
- prompts;
- chunking/extraction/validation scripts;
- runner;
- import/export adapters.

На текущем этапе reusable-части можно проектировать внутри Sveton, но нельзя
смешивать их с финальными бизнес-материалами. После pilot batch устойчивые
схемы и prompts можно переносить в reusable engine.

## Source of truth

Для этого направления первичны:

- `00_input/interviews/inventory.md`;
- `01_docs/operations/leadership_interviews_semantic_analysis/EPIC_LEADERSHIP_INTERVIEWS_SEMANTIC_ANALYSIS.md`;
- этот документ;
- будущие canonical artifacts в `00_input/interviews/statements/`.

Технический pipeline остается методологическим референсом:

- `01_docs/operations/semantic_analysis_engine/TECHNICAL_DOCUMENT_SEMANTIC_ANALYSIS_PIPELINE.md`.

## Главное отличие от технической документации

Техническая документация обычно содержит правила, инструкции, требования,
таблицы и визуальные примеры. Интервью содержат другой тип знания:

- управленческие тезисы;
- мнения и гипотезы;
- коммерческие аргументы;
- объяснения продукта;
- вопросы клиента;
- возражения;
- ответы менеджера;
- кейсы продаж;
- операционные ограничения;
- спорные места;
- формулировки, пригодные для маркетинга;
- открытые вопросы, которые требуют проверки.

Поэтому интервью нельзя обрабатывать как обычный документ с правилами.
Нужен профиль, который сохраняет разговорный контекст и отличает:

- факт;
- мнение руководителя;
- гипотезу;
- коммерческую формулировку;
- техническое утверждение, требующее подтверждения;
- вопрос без ответа;
- редакционную интерпретацию.

## Hard boundaries

1. Интервью не являются технической инструкцией.
2. Технические утверждения из интервью не попадают в Electricians / Installers
   KB как правила без подтверждения техническими документами.
3. Редакционные материалы не являются primary source.
4. Каждый canonical claim должен иметь source quote, speaker, timestamp и
   source chunk.
5. Спорные, низкоуверенные и стратегически рискованные утверждения идут в
   review queue.
6. Open questions не превращаются в утверждения.
7. Marketing-ready wording отделяется от source-backed claim.

## Целевая структура артефактов

```text
00_input/interviews/
  inventory.md
  review/
    speaker_mapping.md
    batch_reviews/
  chunks/
    transcript_chunks.jsonl
    pilot_chunks.jsonl
  runs/
    pilot_YYYYMMDD/
    full_YYYYMMDD/
  statements/
    interview_claims.jsonl
    objections.jsonl
    sales_cases.jsonl
    discovery_questions.jsonl
    open_questions.jsonl
    statement_relations.jsonl
    statement_clusters.json
    coverage_report.md
    coverage_warnings.jsonl
    review_queue.md
  exports/
    business_sales_commercial_kb.md
    business_model_map.md
    sales_playbook.md
    objection_handling.md
    manager_training_outline.md
    commercial_messaging.md
    website_content_bank.md
    presentation_outline.md
    links_to_electricians_kb.md
```

## Pipeline overview

```text
Interview inventory
  -> speaker mapping
  -> transcript normalization
  -> episode-based chunking
  -> pilot extraction
  -> schema/prompt review
  -> validation gates
  -> canonical promotion
  -> dedupe, relations and clusters
  -> human review
  -> editorial assembly
  -> periodic update cycle
```

## Stage 1. Interview inventory

Each transcript must have stable source metadata:

- `source_interview_id`, for example `interview_001`;
- `source_file`;
- date or assumed date;
- participants;
- known roles;
- transcript type;
- diarization quality;
- topic summary;
- processing status;
- notes about source quality.

No transcript should enter extraction without a stable interview id.

## Stage 2. Speaker mapping

Before meaningful extraction, create:

```text
00_input/interviews/review/speaker_mapping.md
```

For each transcript, map:

- `SPEAKER_00`, `SPEAKER_01`, etc.;
- person name, if known;
- role, if known;
- confidence;
- evidence or notes;
- unresolved mapping issues.

If identity is not confirmed, use `needs_mapping`. The extraction may still run,
but the claim must carry `speaker_role = needs_mapping` and require review for
role-sensitive outputs.

## Stage 3. Transcript normalization

The raw diarized text is kept unchanged. A normalized working representation may
be created for processing, but it must preserve:

- timestamps;
- speaker labels;
- utterance order;
- source line numbers where possible;
- raw quote text.

Normalization may fix whitespace and line wrapping. It must not silently rewrite
meaning, repair recognition errors, or merge speakers in a way that hides the
original transcript.

## Stage 4. Episode-based chunking

Technical documents are chunked by source structure. Interviews are chunked by
conversation episodes.

A transcript chunk should usually represent one of these units:

- question and answer;
- objection and response;
- product explanation;
- customer problem case;
- sales process fragment;
- partner/electrician workflow fragment;
- operational or CRM/1C process explanation;
- strategy or market hypothesis;
- disagreement or clarification;
- summary decision.

Chunk boundaries should prefer semantic turns over fixed token limits. However,
the chunker should still enforce practical size limits and overlap.

Recommended chunk fields:

```json
{
  "chunk_id": "interview_001_chunk_0001",
  "source_interview_id": "interview_001",
  "source_file": "260405_sveton_converted_t_large-v3_diar.txt",
  "start_timestamp": "00:00:00",
  "end_timestamp": "00:03:30",
  "speakers": ["SPEAKER_01", "SPEAKER_02"],
  "speaker_roles": ["needs_mapping"],
  "episode_type": "question_answer",
  "topic": "generator_objection",
  "text": "raw transcript excerpt",
  "previous_chunk_id": null,
  "next_chunk_id": "interview_001_chunk_0002",
  "review_flags": []
}
```

## Stage 5. Extraction model

Extraction must return structured records, not summaries.

Core claim types:

- `business_model_claim`;
- `customer_segment_claim`;
- `customer_pain`;
- `value_proposition_claim`;
- `sales_process_claim`;
- `partner_model_claim`;
- `product_claim`;
- `positioning_claim`;
- `marketing_message`;
- `strategy_claim`;
- `operational_claim`;
- `risk_or_constraint`;
- `objection`;
- `recommended_response`;
- `qualification_question`;
- `sales_case`;
- `open_question`;
- `technical_claim_needs_confirmation`.

Recommended claim fields:

```json
{
  "claim_id": "interview_claim_000001",
  "claim": "Компания продает не оборудование, а услугу бесперебойного электроснабжения.",
  "claim_type": "positioning_claim",
  "source_interview_id": "interview_001",
  "source_file": "260405_sveton_converted_t_large-v3_diar.txt",
  "source_chunk_id": "interview_001_chunk_0001",
  "speaker": "SPEAKER_01",
  "speaker_role": "needs_mapping",
  "start_timestamp": "00:29:47",
  "end_timestamp": "00:29:58",
  "source_quote": "Решение, услугу. То есть мы говорим, что мы продаем не оборудование, а мы продаем услугу бесперебойного электроснабжения.",
  "business_area": "positioning",
  "target_outputs": ["business_kb", "sales_training", "website", "presentation"],
  "applicability_to_electricians_kb": "context_only",
  "confidence": "high",
  "review_status": "extracted",
  "notes": ""
}
```

## Stage 6. Specialized record layers

Some extracted records should also be available in specialized files for direct
sales usage.

### Objections

`objections.jsonl` should capture:

- objection text;
- objection category;
- customer assumption;
- recommended response;
- supporting claims;
- source quote;
- review status.

### Sales cases

`sales_cases.jsonl` should capture:

- problem situation;
- customer type;
- context;
- diagnosis path;
- proposed action;
- risk or caveat;
- source-backed evidence;
- whether it is ready for manager training.

### Discovery questions

`discovery_questions.jsonl` should capture:

- question managers should ask;
- why the question matters;
- what answer changes;
- linked sales process or product claims.

### Open questions

`open_questions.jsonl` should capture:

- question;
- why it matters;
- possible owner;
- needed source or validation;
- blocked downstream outputs.

## Stage 7. Validation gates

Before promotion to canonical artifacts, validate:

- JSON schema validity;
- unique ids;
- valid source interview id;
- valid source chunk id;
- source quote is present;
- speaker is present;
- timestamp is present;
- claim type is in allowed vocabulary;
- target outputs are in allowed vocabulary;
- confidence is in allowed vocabulary;
- technical claims are marked `technical_claim_needs_confirmation` or
  `applicability_to_electricians_kb = needs_confirmation`;
- open questions are not treated as facts;
- marketing messages are linked to source-backed claims;
- low-confidence or role-unknown claims go to review.

Coverage should check whether the chunk's meaningful source items were either:

- extracted;
- intentionally skipped with reason;
- marked as noise;
- marked as unresolved/open question.

## Stage 8. Canonical promotion

Extraction run output is not canonical by default.

Promotion requires:

- successful parsing;
- schema validation;
- quote/timestamp/speaker validation;
- coverage warnings reviewed or accepted;
- duplicates checked;
- review flags assigned.

Canonical artifacts should be appendable and reproducible. They should preserve
source ids rather than generating new identities during import.

## Stage 9. Relations and clusters

Do not delete duplicates silently. Use relations:

- `duplicate_of`;
- `supports`;
- `refines`;
- `contradicts`;
- `example_of`;
- `context_for`;
- `requires_technical_confirmation`;
- `derived_marketing_message_for`.

Recommended cluster themes:

- customer segments;
- customer pains;
- value propositions;
- product and package logic;
- generator objections;
- stabilizer / online UPS comparisons;
- sales process;
- qualification and discovery;
- partner and electrician model;
- manager training;
- service model;
- CRM/1C and operations;
- regional expansion;
- growth constraints;
- marketing messages.

## Stage 10. Human review

Review is required for:

- unknown or uncertain speaker role;
- low-confidence claims;
- claims with recognition noise;
- claims that affect public marketing promises;
- claims about prices, guarantees, service periods, or reliability;
- claims that sound technical but are sourced only from interview;
- contradictions between speakers or interviews;
- open questions that block downstream materials.

Reviewer decisions should be append-only. The source quote and extracted claim
remain immutable; approved rewrites are stored separately.

## Stage 11. Editorial assembly

Editorial outputs are downstream artifacts. They must cite canonical claim ids
or cluster ids internally during assembly.

Editorial outputs include:

- `business_sales_commercial_kb.md`;
- `business_model_map.md`;
- `sales_playbook.md`;
- `objection_handling.md`;
- `manager_training_outline.md`;
- `commercial_messaging.md`;
- `website_content_bank.md`;
- `presentation_outline.md`;
- `links_to_electricians_kb.md`.

Editorial text may simplify, group and explain claims, but it must not invent
new facts. If a needed fact is absent, the output should mark it as blocked or
as an open question.

## Stage 12. Periodic update cycle

This KB should be designed for periodic replenishment.

Recommended cycle:

1. Add new transcript to inventory.
2. Confirm speaker mapping.
3. Run chunking.
4. Run extraction.
5. Validate and review.
6. Promote accepted claims.
7. Update clusters and relations.
8. Regenerate affected editorial outputs.
9. Record coverage and unresolved questions.

## Pilot scope

The first pilot should use fragments from different conversation types:

- generator as customer objection;
- "we sell service, not equipment";
- power, reserve time, peak load and manager explanation;
- client qualification and discovery questions;
- partner/electrician model;
- CRM/1C and commercial proposal workflow;
- southern regional expansion;
- service model and post-sale feedback.

The pilot goal is not volume. The goal is to test whether schema and prompt
correctly separate facts, opinions, objections, answers, cases and open
questions.

## Model recommendation

For profile design, schema, prompt and pilot review:

```text
Рекомендуемая модель: 5.5.
Уровень: самый высокий.
Почему: эти шаги задают контракт данных и правила извлечения; ошибки приведут к слабой canonical базе.
```

For later mass extraction after successful pilot:

```text
Рекомендуемая модель: 5.5.
Уровень: высокий.
Почему: массовый прогон должен следовать уже проверенной схеме, но интервью остаются неоднородными и требуют аккуратной типизации.
```

## Next steps

1. Create or update `00_input/interviews/review/speaker_mapping.md`.
2. Define `transcript_chunk.schema.json`.
3. Define `interview_claim.schema.json`.
4. Create pilot extraction prompt.
5. Select pilot fragments.
