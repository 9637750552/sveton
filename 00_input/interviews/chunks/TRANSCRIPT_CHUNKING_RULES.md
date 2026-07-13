# Transcript chunking rules for business interviews

Дата создания: 2026-07-02

## Назначение

Этот документ фиксирует практические правила разбиения leadership / manager
interview transcripts на `transcript_chunks.jsonl`.

Правила являются конкретизацией профиля `business_interviews` из:

- `01_docs/operations/leadership_interviews_semantic_analysis/BUSINESS_INTERVIEWS_PIPELINE.md`;
- `00_input/interviews/chunks/transcript_chunk.schema.json`.

## Общий принцип

Интервью режутся не по фиксированному размеру и не по speaker labels, а по
смысловым эпизодам разговора.

Один chunk должен быть достаточно полным, чтобы модель могла извлечь
source-backed claims без догадок, но достаточно малым, чтобы не смешивать
несколько разных коммерческих или стратегических тем.

## Speaker mapping boundary

Speaker mapping выполняется перед разбором конкретного файла, но chunking не
должен зависеть от точной личности speaker label.

Если speaker mapping не подтвержден:

- `speaker_mapping_status = "needs_mapping"` или `"unreliable"`;
- добавить `review_flags: ["speaker_mapping_required"]`;
- сохранить исходные `SPEAKER_XX` в поле `speakers`;
- не пытаться переименовывать speaker labels внутри текста.

## Chunk identity

Идентификатор chunk:

```text
interview_001_chunk_0001
```

Где:

- `interview_001` соответствует карточке в `inventory.md` и `speaker_mapping.md`;
- `chunk_0001` является порядковым номером внутри стенограммы.

## Recommended episode types

Использовать `episode_type` из схемы:

- `question_answer`: обычный вопрос и ответ.
- `objection_response`: возражение, сомнение или спор и ответ на него.
- `product_explanation`: объяснение продукта, системы, комплекта или принципа.
- `customer_case`: конкретный клиентский или рыночный случай.
- `sales_process`: процесс продажи, КП, выезда, follow-up, квалификации сделки.
- `qualification_discovery`: вопросы, которые помогают понять запрос клиента.
- `partner_workflow`: партнеры, электрики, прорабы, агенты влияния.
- `operations_process`: CRM, 1C, документы, монтажные задания, внутренняя работа.
- `strategy_hypothesis`: гипотеза рынка, региона, сегмента, роста.
- `market_context`: описание рынка, конкурентов, альтернатив.
- `disagreement_clarification`: спор, уточнение, исправление понимания.
- `decision_summary`: итоговое решение или договоренность.
- `technical_explanation_needs_confirmation`: техническое объяснение из интервью,
  которое нельзя превращать в техническое правило без подтверждения документами.
- `noise_or_transition`: шум, переход, служебная фраза.
- `mixed`: временно, если chunk еще требует ручного split.

## Boundary rules

Создавать новый chunk, когда:

- меняется тема разговора;
- вопрос переходит к новой области: продажи, продукт, рынок, CRM, партнеры;
- начинается новый клиентский кейс;
- начинается отдельное возражение или спор;
- техническое объяснение сменяется коммерческим выводом;
- speaker явно подводит итог и разговор идет дальше;
- фрагмент становится слишком длинным.

Не разрывать chunk, если:

- короткий вопрос нужен для понимания длинного ответа;
- несколько реплик уточняют одно возражение;
- speaker labels прыгают, но смысловой эпизод один;
- в середине ответа есть перебивки без новой темы.

## Size guidance

Целевой размер:

- обычный chunk: 1-4 минуты разговора;
- сложный спор или техническое объяснение: до 6 минут, если тема единая;
- короткий sales-case: может быть меньше 1 минуты, если он самодостаточен.

Если chunk длиннее 6 минут, проверить, нельзя ли разделить его по:

- вопросам;
- клиентским ситуациям;
- аргументам;
- шагам процесса;
- смене вывода.

Если chunk короче 30 секунд, проверить, не является ли он:

- частью соседнего вопроса/ответа;
- шумом;
- переходом.

## Overlap

Для каждого chunk сохранять:

- `overlap_previous`: короткий контекст из предыдущего chunk, если нужен;
- `overlap_next`: короткий контекст в следующий chunk, если переход резкий.

Overlap используется только для понимания. Claims должны опираться на цитату
из основного `text` chunk, а не на overlap.

## Topic labels

`primary_topic` должен быть коротким machine-readable label:

```text
generator_objection
service_not_equipment
peak_load_explanation
manager_discovery_questions
partner_electrician_model
crm_1c_offer_workflow
southern_market_expansion
post_sale_feedback
```

`secondary_topics` использовать только если они реально помогут later clustering.

## Review flags

Ставить `review_flags`, если:

- speaker mapping не подтвержден;
- диаризация явно путает людей;
- распознавание текста шумное;
- фрагмент содержит техническое утверждение;
- формулировка потенциально пойдет в публичный маркетинг;
- фрагмент содержит стратегическое обещание или риск;
- есть открытый вопрос без ответа;
- chunk получился слишком длинным или смешанным.

## Exclusion

Фрагмент можно исключить из extraction только явно:

```json
{
  "chunk_status": "excluded",
  "episode_type": "noise_or_transition",
  "exclude_reason": "служебный переход без смыслового содержания"
}
```

Исключение не должно скрывать возможные бизнес-тезисы.

## Pilot chunking rule

Pilot chunks создаются только после выбора первой стенограммы и пофайлового
speaker mapping в чате.

Для pilot выбрать 6-10 фрагментов разных типов:

- возражение про генератор;
- тезис "продаем услугу, не оборудование";
- расчет мощности / резерва / пиковых нагрузок;
- квалификация клиента менеджером;
- партнеры, электрики или прорабы;
- CRM / 1C / КП;
- региональная стратегия;
- постпродажная обратная связь.

## Validation before extraction

Перед extraction каждый chunk должен пройти проверки:

- `chunk_id` уникален;
- `source_interview_id` есть в inventory;
- `source_file` существует;
- timestamps заполнены;
- line range заполнен;
- speaker labels найдены в тексте;
- speaker mapping status заполнен;
- episode type допустим;
- text не пустой;
- previous/next chunk ids согласованы;
- review flags соответствуют known risks.
