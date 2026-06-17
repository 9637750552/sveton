# Инвентаризация интервью с руководством

Дата создания: 2026-06-16

## Назначение

Этот файл фиксирует корпус интервью с руководителями компании и связанными участниками.

Главная цель будущего анализа интервью - создать отдельную Business / Sales / Commercial Knowledge Base.

Эта база знаний должна:

- описать бизнес-модель компании;
- собрать доказательную базу для продаж, коммерции и маркетинговых материалов;
- подготовить тезисы для сайта, буклетов, презентаций, КП и стратегии;
- подготовить материалы для обучения продавцов;
- подготовить материалы для обучения менеджеров и профильных специалистов;
- подготовить sales playbook, скрипты продаж и обработку возражений;
- выделить управленческие утверждения, риски, ограничения, сегменты, ценность продукта и каналы продаж.

В проекте фиксируются две разные базы знаний:

1. Business / Sales / Commercial KB - основной результат анализа интервью.
2. Electricians / Installers KB - отдельная база по электрикам, монтажникам, качеству монтажа и техническим инструкциям.

Связь интервью с базой знаний электриков вторична. Из интервью можно брать контекст про качество, ожидания к электрикам, партнерскую модель и сервис, но нельзя превращать интервью в техническую инструкцию без подтверждения документами.

## Порядок работ

1. Сейчас: инвентаризация интервью и план эпика.
2. Сначала завершаем первый слой semantic extraction по документации электриков.
3. Затем запускаем semantic extraction интервью отдельным пайплайном.
4. Сначала формируем Business / Sales / Commercial KB.
5. Затем связываем часть утверждений с базой электриков через отдельный вторичный слой relevance mapping.

## Статусы

- `raw_transcript`: исходная diarized TXT-стенограмма найдена;
- `inventory_pending`: нужно уточнить участников, тему и качество;
- `speaker_mapping_pending`: нужно сопоставить `SPEAKER_XX` с людьми/ролями;
- `chunking_pending`: интервью еще не разбито на чанки;
- `statements_pending`: утверждения еще не извлечены;
- `review_required`: требуется ручная проверка;
- `approved`: утверждения/выводы подтверждены.

## Документы

| № | Файл | Предполагаемая дата | Формат | Размер, символы | Непустых строк | Статус | Комментарий |
|---:|---|---|---|---:|---:|---|---|
| 1 | `260405_sveton_2_converted_t_large-v3_diar.txt` | 2026-04-05 | txt transcript / diarized | 87131 | 562 | raw_transcript, inventory_pending, speaker_mapping_pending | Нужно подтвердить участников, тему интервью и качество диаризации. |
| 2 | `260405_sveton_converted_t_large-v3_diar.txt` | 2026-04-05 | txt transcript / diarized | 79868 | 547 | raw_transcript, inventory_pending, speaker_mapping_pending | Нужно подтвердить участников, тему интервью и качество диаризации. |
| 3 | `260408_sveton3_converted_t_large-v3_diar.txt` | 2026-04-08 | txt transcript / diarized | 52474 | 448 | raw_transcript, inventory_pending, speaker_mapping_pending | Нужно подтвердить участников, тему интервью и качество диаризации. |
| 4 | `260408_sveton4_converted_t_large-v3_diar.txt` | 2026-04-08 | txt transcript / diarized | 74925 | 496 | raw_transcript, inventory_pending, speaker_mapping_pending | Нужно подтвердить участников, тему интервью и качество диаризации. |
| 5 | `260609_sveton_2_converted_t_large-v3_diar.txt` | 2026-06-09 | txt transcript / diarized | 57633 | 538 | raw_transcript, inventory_pending, speaker_mapping_pending | Нужно подтвердить участников, тему интервью и качество диаризации. |
| 6 | `260609_sveton_converted_t_large-v3_diar.txt` | 2026-06-09 | txt transcript / diarized | 21255 | 92 | raw_transcript, inventory_pending, speaker_mapping_pending | Нужно подтвердить участников, тему интервью и качество диаризации. |
| 7 | `260610_sveton_converted_t_large-v3_diar.txt` | 2026-06-10 | txt transcript / diarized | 60925 | 436 | raw_transcript, inventory_pending, speaker_mapping_pending | Нужно подтвердить участников, тему интервью и качество диаризации. |

## Что нужно уточнить перед анализом

- Кто именно говорит в каждом файле: генеральный директор, коммерческий директор, интервьюер, другие участники.
- Какие интервью являются частями одного разговора.
- Какие темы обсуждались в каждом интервью.
- Есть ли исходные аудио/видео, если потребуется проверить спорные фрагменты.
- Насколько корректна автоматическая диаризация.

## Целевые выходы будущего анализа

- `business_model_claims.jsonl`
- `business_sales_commercial_kb.md`
- `marketing_claims.jsonl`
- `strategy_claims.jsonl`
- `business_model_map.md`
- `sales_training_knowledge_base.md`
- `sales_playbook.md`
- `objection_handling.md`
- `manager_training_outline.md`
- `commercial_messaging.md`
- `marketing_content_bank.md`
- `website_content_bank.md`
- `presentation_outline.md`
- `links_to_electricians_kb.md`

## Следующие действия

- [x] Найти 7 стенограмм интервью.
- [x] Создать инвентаризацию.
- [ ] Создать `review/speaker_mapping.md`.
- [ ] Подтвердить участников и роли.
- [ ] После завершения первого слоя анализа документов электриков запустить chunking интервью.
