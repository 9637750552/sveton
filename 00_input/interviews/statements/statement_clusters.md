# Business interview statement clusters v1

Дата: 2026-07-03

Источник:

```text
00_input/interviews/statements/interview_corpus_claims.jsonl
```

## Статус

Это первичная кластеризация v1 по всем семи интервью. Она не меняет extracted claims, а группирует их для review, дедупликации, relation mapping и последующей сборки Business / Sales / Commercial KB.

- Claims total: `416`
- Clusters total: `19`
- Relations total: `440`
- Technical confirmation required: `218`

## Важные ограничения

- Технические claims из интервью остаются review-required и не являются техническими правилами.
- Marketing/public claims требуют отдельного review перед сайтом, КП, буклетом или презентацией.
- Дубликаты не удаляются: связи фиксируются в `statement_relations.jsonl`.

## BIC001. Бизнес-модель и сервисное позиционирование

Тема: `business_model_service_positioning`

Количество claims: `16`

Охват: Что продает Светон: услуга, сервисная модель, клиентские отношения, гарантийное обслуживание, отличие от продажи железа.

Основные выходы:

- `business_kb`
- `business_model_map`
- `presentation`

Источники:

- `interview_001`: 1
- `interview_002`: 8
- `interview_003`: 1
- `interview_004`: 1
- `interview_005`: 1
- `interview_006`: 1
- `interview_007`: 3

Типы claims:

- `business_model_claim`: 15
- `strategy_claim`: 1

Review flags:

- `marketing_claim_review`: 2
- `price_or_guarantee_review`: 10
- `public_use_review`: 1
- `strategy_claim_review`: 15
- `technical_confirmation_required`: 2

Примеры claim_id:

- `interview_claim_001067`
- `interview_claim_002033`
- `interview_claim_002036`
- `interview_claim_002037`
- `interview_claim_002041`
- `interview_claim_002042`
- `interview_claim_002054`
- `interview_claim_002056`

## BIC002. Клиентские сегменты и ситуации покупки

Тема: `customer_segments`

Количество claims: `12`

Охват: Частные дома, SMB, строительные компании, прорабы, ЛПР и разные моменты возникновения потребности.

Основные выходы:

- `business_kb`
- `sales_playbook`
- `website_content_bank`

Источники:

- `interview_001`: 1
- `interview_002`: 4
- `interview_003`: 3
- `interview_004`: 2
- `interview_007`: 2

Типы claims:

- `customer_segment_claim`: 12

Review flags:

- `marketing_claim_review`: 12
- `strategy_claim_review`: 8
- `technical_confirmation_required`: 2

Примеры claim_id:

- `interview_claim_001036`
- `interview_claim_002001`
- `interview_claim_002006`
- `interview_claim_002016`
- `interview_claim_002020`
- `interview_claim_003048`
- `interview_claim_003049`
- `interview_claim_003050`

## BIC003. Боли клиента и ценность продукта

Тема: `customer_pains_value_proposition`

Количество claims: `17`

Охват: Комфорт, безопасность, разморозка, вода, интернет, спокойствие клиента и ценностные формулировки.

Основные выходы:

- `sales_playbook`
- `commercial_messaging`
- `website_content_bank`

Источники:

- `interview_001`: 8
- `interview_002`: 5
- `interview_003`: 2
- `interview_007`: 2

Типы claims:

- `customer_pain`: 10
- `value_proposition_claim`: 7

Review flags:

- `marketing_claim_review`: 16
- `price_or_guarantee_review`: 2
- `public_use_review`: 7
- `strategy_claim_review`: 2
- `technical_confirmation_required`: 7

Примеры claim_id:

- `interview_claim_001009`
- `interview_claim_001010`
- `interview_claim_001011`
- `interview_claim_001037`
- `interview_claim_001038`
- `interview_claim_001039`
- `interview_claim_001049`
- `interview_claim_001063`

## BIC004. Продуктовая логика, мощность и резерв

Тема: `product_package_sizing`

Количество claims: `48`

Охват: Инвертор, аккумуляторы, мощность, пиковые нагрузки, время резерва, типовые потребители и подбор конфигурации.

Основные выходы:

- `manager_training`
- `sales_training`
- `commercial_messaging`

Источники:

- `interview_001`: 7
- `interview_002`: 2
- `interview_003`: 12
- `interview_004`: 4
- `interview_005`: 10
- `interview_006`: 6
- `interview_007`: 7

Типы claims:

- `technical_claim_needs_confirmation`: 48

Review flags:

- `marketing_claim_review`: 11
- `price_or_guarantee_review`: 9
- `recognition_noise`: 3
- `technical_confirmation_required`: 48

Примеры claim_id:

- `interview_claim_001040`
- `interview_claim_001045`
- `interview_claim_001048`
- `interview_claim_001070`
- `interview_claim_001071`
- `interview_claim_001085`
- `interview_claim_001086`
- `interview_claim_002004`

## BIC005. Технические edge cases и границы подтверждения

Тема: `technical_edge_cases_review`

Количество claims: `25`

Охват: Монтажные и электрические нюансы из интервью: щиты, фазы, байпас, заземление, зануление, место установки, превышение нагрузки.

Основные выходы:

- `review_only`
- `links_to_electricians_kb`

Источники:

- `interview_001`: 3
- `interview_002`: 2
- `interview_003`: 12
- `interview_004`: 2
- `interview_005`: 1
- `interview_006`: 2
- `interview_007`: 3

Типы claims:

- `technical_claim_needs_confirmation`: 25

Review flags:

- `marketing_claim_review`: 4
- `price_or_guarantee_review`: 2
- `recognition_noise`: 2
- `strategy_claim_review`: 1
- `technical_confirmation_required`: 25

Примеры claim_id:

- `interview_claim_001024`
- `interview_claim_001025`
- `interview_claim_001026`
- `interview_claim_002030`
- `interview_claim_002048`
- `interview_claim_003014`
- `interview_claim_003023`
- `interview_claim_003028`

## BIC006. Генератор, стабилизатор и типы ИБП

Тема: `generator_stabilizer_ups_comparisons`

Количество claims: `20`

Охват: Сравнения с генераторами, стабилизаторами, online/offline/line-interactive ИБП и двойным преобразованием.

Основные выходы:

- `objection_handling`
- `sales_training`
- `commercial_messaging`

Источники:

- `interview_001`: 3
- `interview_002`: 2
- `interview_003`: 8
- `interview_004`: 2
- `interview_006`: 3
- `interview_007`: 2

Типы claims:

- `marketing_message`: 1
- `positioning_claim`: 1
- `risk_or_constraint`: 1
- `sales_process_claim`: 1
- `strategy_claim`: 4
- `technical_claim_needs_confirmation`: 11
- `value_proposition_claim`: 1

Review flags:

- `marketing_claim_review`: 11
- `price_or_guarantee_review`: 6
- `public_use_review`: 2
- `recognition_noise`: 2
- `strategy_claim_review`: 4
- `technical_confirmation_required`: 17

Примеры claim_id:

- `interview_claim_001030`
- `interview_claim_001031`
- `interview_claim_001033`
- `interview_claim_002065`
- `interview_claim_002076`
- `interview_claim_003001`
- `interview_claim_003002`
- `interview_claim_003003`

## BIC007. Продажный процесс, КП и сделка

Тема: `sales_process`

Количество claims: `33`

Охват: Воронка, предварительное и финальное КП, цены, скидки, договор, заказ покупателя, отправка клиенту.

Основные выходы:

- `sales_playbook`
- `manager_training`
- `commercial_messaging`

Источники:

- `interview_001`: 6
- `interview_002`: 9
- `interview_003`: 7
- `interview_004`: 3
- `interview_005`: 3
- `interview_006`: 3
- `interview_007`: 2

Типы claims:

- `sales_process_claim`: 33

Review flags:

- `marketing_claim_review`: 18
- `price_or_guarantee_review`: 7
- `recognition_noise`: 3
- `strategy_claim_review`: 17
- `technical_confirmation_required`: 6

Примеры claim_id:

- `interview_claim_001014`
- `interview_claim_001028`
- `interview_claim_001034`
- `interview_claim_001043`
- `interview_claim_001074`
- `interview_claim_001075`
- `interview_claim_002007`
- `interview_claim_002009`

## BIC008. Квалификация и discovery-вопросы

Тема: `qualification_discovery`

Количество claims: `10`

Охват: Вопросы к клиенту, косвенные признаки, сбор нагрузок, режимы работы, бюджет, решение о выезде.

Основные выходы:

- `sales_script`
- `manager_training`
- `sales_playbook`

Источники:

- `interview_001`: 2
- `interview_003`: 3
- `interview_005`: 2
- `interview_006`: 1
- `interview_007`: 2

Типы claims:

- `qualification_question`: 9
- `sales_process_claim`: 1

Review flags:

- `marketing_claim_review`: 1
- `price_or_guarantee_review`: 2
- `strategy_claim_review`: 2
- `technical_confirmation_required`: 7

Примеры claim_id:

- `interview_claim_001021`
- `interview_claim_001060`
- `interview_claim_003015`
- `interview_claim_003030`
- `interview_claim_003046`
- `interview_claim_005008`
- `interview_claim_005015`
- `interview_claim_006004`

## BIC009. Возражения и рекомендуемые ответы

Тема: `objection_handling`

Количество claims: `8`

Охват: Возражения клиентов, ответы, спорные коммерческие тезисы и аргументация менеджера.

Основные выходы:

- `objection_handling`
- `sales_training`
- `sales_script`

Источники:

- `interview_001`: 2
- `interview_002`: 4
- `interview_003`: 2

Типы claims:

- `customer_pain`: 1
- `objection`: 2
- `recommended_response`: 5

Review flags:

- `marketing_claim_review`: 8
- `price_or_guarantee_review`: 3
- `public_use_review`: 2
- `technical_confirmation_required`: 5

Примеры claim_id:

- `interview_claim_001029`
- `interview_claim_001032`
- `interview_claim_002011`
- `interview_claim_002012`
- `interview_claim_002028`
- `interview_claim_002029`
- `interview_claim_003020`
- `interview_claim_003060`

## BIC010. Электрики, монтажники и партнерская модель

Тема: `electrician_installer_partner_model`

Количество claims: `62`

Охват: Роли электриков и монтажников, аудит, выезд, обучение, аутсорс, контроль, ограничения передачи клиентского разговора.

Основные выходы:

- `business_kb`
- `manager_training`
- `strategy`

Источники:

- `interview_001`: 8
- `interview_002`: 16
- `interview_003`: 5
- `interview_004`: 5
- `interview_005`: 6
- `interview_006`: 17
- `interview_007`: 5

Типы claims:

- `marketing_message`: 1
- `operational_claim`: 25
- `partner_model_claim`: 5
- `positioning_claim`: 3
- `risk_or_constraint`: 15
- `strategy_claim`: 13

Review flags:

- `marketing_claim_review`: 8
- `price_or_guarantee_review`: 8
- `public_use_review`: 2
- `recognition_noise`: 5
- `strategy_claim_review`: 51
- `technical_confirmation_required`: 33

Примеры claim_id:

- `interview_claim_001004`
- `interview_claim_001023`
- `interview_claim_001027`
- `interview_claim_001058`
- `interview_claim_001068`
- `interview_claim_001077`
- `interview_claim_001083`
- `interview_claim_001087`

## BIC011. Прорабы, строители и партнерские каналы

Тема: `foremen_builders_channels`

Количество claims: `19`

Охват: Прорабы, строительные компании, девелоперы, модульные дома и ограниченность каналов через стройку.

Основные выходы:

- `strategy`
- `business_kb`
- `sales_playbook`

Источники:

- `interview_001`: 8
- `interview_002`: 1
- `interview_004`: 5
- `interview_005`: 2
- `interview_007`: 3

Типы claims:

- `operational_claim`: 1
- `partner_model_claim`: 13
- `risk_or_constraint`: 1
- `strategy_claim`: 4

Review flags:

- `marketing_claim_review`: 2
- `recognition_noise`: 1
- `strategy_claim_review`: 17
- `technical_confirmation_required`: 6

Примеры claim_id:

- `interview_claim_001005`
- `interview_claim_001006`
- `interview_claim_001007`
- `interview_claim_001008`
- `interview_claim_001012`
- `interview_claim_001013`
- `interview_claim_001018`
- `interview_claim_001022`

## BIC012. Роли менеджера, специалиста и обучение

Тема: `manager_training_roles`

Количество claims: `17`

Охват: Что должен делать менеджер/специалист, где нужен технический специалист, как обучать и заменять людей.

Основные выходы:

- `manager_training`
- `sales_training`

Источники:

- `interview_001`: 4
- `interview_002`: 2
- `interview_003`: 4
- `interview_004`: 1
- `interview_006`: 3
- `interview_007`: 3

Типы claims:

- `marketing_message`: 2
- `operational_claim`: 8
- `positioning_claim`: 1
- `product_claim`: 1
- `risk_or_constraint`: 4
- `strategy_claim`: 1

Review flags:

- `marketing_claim_review`: 6
- `price_or_guarantee_review`: 1
- `public_use_review`: 1
- `recognition_noise`: 3
- `strategy_claim_review`: 10
- `technical_confirmation_required`: 10

Примеры claim_id:

- `interview_claim_001019`
- `interview_claim_001057`
- `interview_claim_001061`
- `interview_claim_001091`
- `interview_claim_002063`
- `interview_claim_002081`
- `interview_claim_003011`
- `interview_claim_003021`

## BIC013. CRM, 1C, документация и операционный учет

Тема: `crm_one_c_operations`

Количество claims: `33`

Охват: 1C, CRM, анкеты, нагрузки, карточки, задания, записи разговоров, документация, отчеты и материалы.

Основные выходы:

- `manager_training`
- `business_kb`
- `operations`

Источники:

- `interview_001`: 5
- `interview_002`: 2
- `interview_004`: 3
- `interview_005`: 1
- `interview_006`: 16
- `interview_007`: 6

Типы claims:

- `business_model_claim`: 1
- `operational_claim`: 18
- `partner_model_claim`: 2
- `product_claim`: 1
- `risk_or_constraint`: 7
- `sales_process_claim`: 3
- `strategy_claim`: 1

Review flags:

- `marketing_claim_review`: 5
- `price_or_guarantee_review`: 5
- `recognition_noise`: 1
- `strategy_claim_review`: 21
- `technical_confirmation_required`: 16

Примеры claim_id:

- `interview_claim_001059`
- `interview_claim_001076`
- `interview_claim_001079`
- `interview_claim_001080`
- `interview_claim_001081`
- `interview_claim_002008`
- `interview_claim_002047`
- `interview_claim_004030`

## BIC014. Сервис, качество, мониторинг и обратная связь

Тема: `service_quality_monitoring`

Количество claims: `50`

Охват: Качество сервиса, гарантийные случаи, мониторинг, SMS, постпродажа, отзывы, репутация.

Основные выходы:

- `business_kb`
- `manager_training`
- `commercial_messaging`

Источники:

- `interview_001`: 20
- `interview_002`: 13
- `interview_003`: 1
- `interview_004`: 8
- `interview_006`: 2
- `interview_007`: 6

Типы claims:

- `marketing_message`: 3
- `operational_claim`: 4
- `positioning_claim`: 9
- `product_claim`: 10
- `risk_or_constraint`: 8
- `strategy_claim`: 16

Review flags:

- `marketing_claim_review`: 28
- `price_or_guarantee_review`: 8
- `public_use_review`: 8
- `recognition_noise`: 6
- `strategy_claim_review`: 32
- `technical_confirmation_required`: 24

Примеры claim_id:

- `interview_claim_001016`
- `interview_claim_001035`
- `interview_claim_001041`
- `interview_claim_001042`
- `interview_claim_001044`
- `interview_claim_001046`
- `interview_claim_001047`
- `interview_claim_001050`

## BIC015. Региональная экспансия и южный филиал

Тема: `regional_expansion`

Количество claims: `22`

Охват: Южный филиал, Краснодар, Горячий Ключ, региональный MVP, Вадик, локальные электрики, первые контакты.

Основные выходы:

- `strategy`
- `business_model_map`
- `manager_training`

Источники:

- `interview_001`: 9
- `interview_002`: 6
- `interview_004`: 4
- `interview_005`: 1
- `interview_007`: 2

Типы claims:

- `business_model_claim`: 3
- `operational_claim`: 3
- `risk_or_constraint`: 1
- `strategy_claim`: 15

Review flags:

- `marketing_claim_review`: 5
- `price_or_guarantee_review`: 2
- `recognition_noise`: 2
- `strategy_claim_review`: 22
- `technical_confirmation_required`: 3

Примеры claim_id:

- `interview_claim_001001`
- `interview_claim_001002`
- `interview_claim_001003`
- `interview_claim_001015`
- `interview_claim_001017`
- `interview_claim_001020`
- `interview_claim_001051`
- `interview_claim_001055`

## BIC016. Ограничения роста, экономика и найм

Тема: `growth_constraints_finance_staffing`

Количество claims: `10`

Охват: Финансовые ограничения, маржа, склад, штат, подбор менеджеров/монтажников, масштабирование и операционные пределы.

Основные выходы:

- `strategy`
- `business_model_map`

Источники:

- `interview_001`: 1
- `interview_002`: 7
- `interview_004`: 1
- `interview_007`: 1

Типы claims:

- `business_model_claim`: 6
- `risk_or_constraint`: 3
- `strategy_claim`: 1

Review flags:

- `marketing_claim_review`: 2
- `price_or_guarantee_review`: 6
- `strategy_claim_review`: 7
- `technical_confirmation_required`: 3

Примеры claim_id:

- `interview_claim_001064`
- `interview_claim_002002`
- `interview_claim_002005`
- `interview_claim_002019`
- `interview_claim_002027`
- `interview_claim_002055`
- `interview_claim_002069`
- `interview_claim_002073`

## BIC017. Маркетинговые формулировки и публичный контент

Тема: `marketing_public_content`

Количество claims: `2`

Охват: Формулировки для сайта, буклетов, презентаций, публичные утверждения и материалы, требующие review.

Основные выходы:

- `commercial_messaging`
- `website_content_bank`
- `presentation`

Источники:

- `interview_001`: 1
- `interview_005`: 1

Типы claims:

- `positioning_claim`: 1
- `risk_or_constraint`: 1

Review flags:

- `marketing_claim_review`: 2
- `public_use_review`: 2
- `technical_confirmation_required`: 1

Примеры claim_id:

- `interview_claim_001089`
- `interview_claim_005025`

## BIC018. Кейсы, примеры и пилотные возможности

Тема: `sales_cases_examples`

Количество claims: `8`

Охват: Конкретные клиентские, партнерские и внутренние кейсы, примеры продаж и пилотные региональные возможности.

Основные выходы:

- `sales_training`
- `content_bank`
- `business_kb`

Источники:

- `interview_001`: 2
- `interview_002`: 2
- `interview_004`: 1
- `interview_007`: 3

Типы claims:

- `sales_case`: 8

Review flags:

- `marketing_claim_review`: 7
- `price_or_guarantee_review`: 3
- `public_use_review`: 1
- `strategy_claim_review`: 2
- `technical_confirmation_required`: 3

Примеры claim_id:

- `interview_claim_001073`
- `interview_claim_001090`
- `interview_claim_002013`
- `interview_claim_002015`
- `interview_claim_004010`
- `interview_claim_007031`
- `interview_claim_007044`
- `interview_claim_007052`

## BIC019. Открытые вопросы и блокеры

Тема: `open_questions_blockers`

Количество claims: `4`

Охват: Вопросы, которые нельзя превращать в факты без дополнительного интервью, документов или проверки.

Основные выходы:

- `review_only`
- `strategy`

Источники:

- `interview_002`: 2
- `interview_004`: 1
- `interview_006`: 1

Типы claims:

- `open_question`: 4

Review flags:

- `open_question`: 4
- `strategy_claim_review`: 4

Примеры claim_id:

- `interview_claim_002021`
- `interview_claim_002068`
- `interview_claim_004019`
- `interview_claim_006054`

