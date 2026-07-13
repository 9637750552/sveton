# Связки с базой знаний электриков v1

Дата: 2026-07-03

Статус: редакционная карта связей и ревью между claims из бизнес-интервью и базой знаний электриков.

Источник business layer:

```text
00_input/interviews/statements/interview_corpus_claims.jsonl
00_input/interviews/statements/statement_clusters.json
00_input/interviews/statements/statement_relations.jsonl
```

Источник electricians KB:

```text
01_docs/operations/electricians_knowledge_base/README.md
00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl
00_input/documents/electricians_knowledge_base/statements/statement_clusters.json
```

Назначение: зафиксировать, какие claims из бизнес-интервью можно использовать как контекст для базы электриков, какие можно связать с уже существующими техническими разделами, а какие нельзя переносить в монтажные инструкции без технического подтверждения.

## 1. Правило Границы

Интервью руководства и менеджеров не являются технической инструкцией. Они могут объяснять бизнес-логику, роль менеджера, ожидания клиента, процесс передачи заявки и риски коммуникации. Но технические правила монтажа, расчета, подключения, безопасности и гарантийных последствий должны опираться на техническую canonical базу электриков, а не на интервью.

Источник: `BIC004`, `BIC005`, `BIC006`, `BIC008`, `BIC010`, `BIC013`.

Практическое правило:

- `context_only` - можно использовать как операционный или sales-контекст.
- `needs_confirmation` - можно поставить в очередь ревью, но нельзя превращать в инструкцию.
- `technical_confirmation_required` - искать подтверждение в electricians KB или технических документах.
- `safety-review` - не использовать как правило до экспертное ревью.

## 2. Существующие разделы БЗ электриков для связки

| Electricians KB section | Назначение | Как связан с интервью |
| --- | --- | --- |
| `02_ups_components.md` | состав ИБП, инвертор, АКБ, байпас, балансир, DC-защита, GSM-розетка | проверять продуктовые и компонентные тезисы из `BIC004`, `BIC006` |
| `04_installation_process.md` | этапы монтажа, сборка ИБП, подключение к щиту, настройка, проверка | проверять claims про осмотр, монтаж, проверку и настройку |
| `07_photo_report.md` | фотофиксация до/после монтажа и состав фотоотчета | связать claims про фотографии на осмотре и перед монтажом |
| `08_installer_roles.md` | обязанности монтажника на выезде, прием задания, работа на объекте, отчет | связать claims про роль монтажника и эскалацию проблем |
| `09_installation_report.md` | структура отчета по монтажу | связать claims про карточку клиента, задание, фактическое состояние |
| `10_training_levels.md` | офисное обучение и проверка монтажника | связать claims про обучение, заменяемость и границу компетенций |
| `12_installation_request_check.md` | проверка заявки на монтаж, фото, ТЗ, 1С, резервная группа | связать claims про предварительную квалификацию, 1С и передачу задания |
| будущий `05_work_on_site.md` | работа на объекте | потенциальная связка с claims про поведение на осмотре/монтаже |
| будущий `06_service_visit.md` | сервисный выезд | потенциальная связка с service/quality claims |
| будущий `14_qualification_levels.md` | уровни квалификации монтажника | потенциальная связка с claims про обучение и заменяемость |
| будущий `15_uzo_installation.md` | УЗО, safety-critical | проверять claims про УЗО/заземление/зануление только через экспертное ревью |

Источник: electricians KB README; `BIC004`, `BIC005`, `BIC006`, `BIC010`, `BIC012`, `BIC013`.

## 3. Утверждения, которые можно использовать как операционный контекст

Эти claims не создают технических правил, но полезны для понимания ролей, процесса и ответственности.

| Claim интервью | Смысл | Связь с БЗ электриков | Решение |
| --- | --- | --- | --- |
| `interview_claim_007024` | отношения и история клиента должны принадлежать Светон и храниться в CRM | `08_installer_roles.md`, `12_installation_request_check.md` | context for role ownership |
| `interview_claim_007026` | человек Светон ведет разговор; электрик может участвовать, но сбор и документирование остаются у компании | `08_installer_roles.md`, `12_installation_request_check.md` | context for communication boundary |
| `interview_claim_007027` | без CRM возникает риск спорных обещаний и гарантийных конфликтов | `08_installer_roles.md`, `09_installation_report.md`, `12_installation_request_check.md` | context for documentation discipline |
| `interview_claim_006037` | монтажники едут с карточкой клиента и заданием, собранным менеджером | `08_installer_roles.md`, `12_installation_request_check.md` | context; align with existing task handoff |
| `interview_claim_006040` | из 1С можно сформировать карточку с адресом, описанием и списком работ | `12_installation_request_check.md`, `09_installation_report.md` | context; verify actual 1C fields |
| `interview_claim_006046` | монтажник не должен вести содержательный разговор с клиентом | `08_installer_roles.md` | кандидат в операционное правило коммуникации, не техническое правило |
| `interview_claim_007020` | типовой электрик не должен владеть сложной клиентской квалификацией | `10_training_levels.md`, `08_installer_roles.md` | training context |

Источник: `BIC010`, `BIC012`, `BIC013`.

## 4. Утверждения, которые можно связать с проверкой заявки и осмотром

Эти claims полезны для будущего workflow между менеджером, специалистом и монтажником. Но часть из них содержит технические элементы и требует подтверждения через electricians KB.

| Claim интервью | Смысл | Связь с БЗ электриков | Решение |
| --- | --- | --- | --- |
| `interview_claim_005008` | первый шаг аудита - выяснить, какие электроприборы клиент хочет зарезервировать | `12_installation_request_check.md` | кандидат в менеджерский чек-лист; техническая форма требует подтверждения |
| `interview_claim_005015` | спросить критичные нагрузки, названия, номинальную и пиковую мощность | `12_installation_request_check.md`, `09_installation_report.md` | technical confirmation required |
| `interview_claim_006004` | уточнить одновременный пуск котла, насоса и холодильника | `02_ups_components.md`, `12_installation_request_check.md` | требуется техническое подтверждение; не превращать в правило расчета |
| `interview_claim_006023` | менеджер заполняет нагрузки со слов клиента, затем данные проверяются на выезде | `12_installation_request_check.md`, `09_installation_report.md` | strong bridge; exact fields need ревью процесса |
| `interview_claim_007014` | если клиент не знает мощность, специалист выясняет параметры по косвенным признакам | `12_installation_request_check.md`, future CRM form | требуется техническое и процессное подтверждение |
| `interview_claim_007015` | клиенты часто не знают мощность насосов и оборудования | `12_installation_request_check.md` | context for discovery form |
| `interview_claim_007019` | первичная квалификация нужна до выезда: нагрузки, режимы, бюджет | `12_installation_request_check.md` | менеджерское правило процесса; технические поля требуют ревью |

Источник: `BIC008`, `BIC013`.

## 5. Утверждения, которые пересекаются с фотофиксацией и выездом

| Claim интервью | Смысл | Связь с БЗ электриков | Решение |
| --- | --- | --- | --- |
| `interview_claim_006033` | на осмотре электрик фотографирует место установки и проверяет габариты рулеткой | `07_photo_report.md`, `12_installation_request_check.md` | сверить с действующими правилами фотофиксации/чек-листов; точный объем требует ревью |
| `interview_claim_006045` | перед монтажом монтажник фотографирует фактическое состояние, сверяется с заданием и эскалирует проблемы | `07_photo_report.md`, `08_installer_roles.md`, `04_installation_process.md` | strong bridge; use electricians KB as source of actual rules |
| `interview_claim_006037` | монтажник едет с карточкой клиента и заданием | `08_installer_roles.md`, `12_installation_request_check.md` | context for handoff |
| `interview_claim_006040` | карточка содержит адрес, описание и список работ | `12_installation_request_check.md`, `09_installation_report.md` | verify against actual 1C/process |

Источник: `BIC010`, `BIC013`.

## 6. Утверждения, которые нельзя переносить как технические правила

Эти claims могут быть полезны как очередь ревью, но не должны попадать в electricians KB как инструкции без подтверждения техническими документами и экспертное ревью.

| Interview claim | Тема | Почему нельзя переносить напрямую | Где проверять |
| --- | --- | --- | --- |
| `interview_claim_006010` | 70% от номинала инвертора | техническое правило расчета нагрузки | `02_ups_components.md`, `04_installation_process.md`, технический эксперт |
| `interview_claim_007010` | повтор правила 70% | техническое правило долговременной нагрузки | `02_ups_components.md`, технический эксперт |
| `interview_claim_006002` | пиковая мощность холодильников | технические коэффициенты зависят от оборудования | `02_ups_components.md`, product docs |
| `interview_claim_006011` | пример пикового расчета холодильника и насоса | пример расчета нельзя превращать в норму | `02_ups_components.md`, calculator/technical docs |
| `interview_claim_007004` | ручной байпас нежелателен, лучше мощнее инвертор | затрагивает схемы, стоимость и техническое проектирование | `02_ups_components.md`, `04_installation_process.md`, экспертное ревью |
| `interview_claim_007005` | гарантийные последствия превышения нагрузки | юридико-гарантийный и технический вопрос | ревью политики + технический эксперт |
| `interview_claim_007040` | чувствительность котлов к форме сигнала, генератору, нулю, заземлению | safety-critical и зависит от объекта | future `15_uzo_installation.md`, экспертное ревью |
| `interview_claim_007041` | заземление и зануление при монтаже | safety-critical | future `15_uzo_installation.md`, экспертное ревью |
| `interview_claim_006005` | offline UPS, реле, 10 мс, компьютеры не сбрасываются | техническое утверждение по типу ИБП | `02_ups_components.md`, product docs |
| `interview_claim_006006` | online UPS менее подходит из-за КПД, шума, ресурса АКБ | сравнительное техническое/маркетинговое утверждение | product docs + маркетинговое ревью |

Источник: `BIC004`, `BIC005`, `BIC006`.

## 7. Рекомендуемые задачи перекрестного ревью

### Задача A. Связка между менеджерской заявкой и монтажом

Цель: связать sales discovery с `12_installation_request_check.md`.

Claims из интервью:

- `interview_claim_005008`
- `interview_claim_006023`
- `interview_claim_007014`
- `interview_claim_007019`

Основание в базе электриков:

- `12_installation_request_check.md`
- `09_installation_report.md`

Ожидаемый результат: отдельный manager-side checklist "что должно быть собрано до передачи заявки на монтаж", не монтажная инструкция.

### Задача B. Связка фотофиксации и состояния объекта

Цель: связать осмотр, фотофиксацию и проверку фактического состояния объекта.

Claims из интервью:

- `interview_claim_006033`
- `interview_claim_006045`

Основание в базе электриков:

- `07_photo_report.md`
- `08_installer_roles.md`
- `04_installation_process.md`

Ожидаемый результат: уточнить, какие фото нужны на этапе первичного осмотра, а какие уже в фотоотчете монтажа.

### Задача C. Граница ролей

Цель: согласовать, что говорит менеджер, что может говорить электрик, и когда нужен технический специалист.

Claims из интервью:

- `interview_claim_006046`
- `interview_claim_007020`
- `interview_claim_007024`
- `interview_claim_007026`
- `interview_claim_007027`
- `interview_claim_007030`

Основание в базе электриков:

- `08_installer_roles.md`
- `10_training_levels.md`
- future `14_qualification_levels.md`

Ожидаемый результат: communication policy для выезда и чеклист эскалации.

### Задача D. Очередь ревью технических утверждений

Цель: проверить interview-based технические claims против technical KB и product documentation.

Claims из интервью:

- `interview_claim_006010`
- `interview_claim_007010`
- `interview_claim_006002`
- `interview_claim_006011`
- `interview_claim_007004`
- `interview_claim_007005`
- `interview_claim_007040`
- `interview_claim_007041`
- `interview_claim_006005`
- `interview_claim_006006`

Основание в базе электриков:

- `02_ups_components.md`
- `04_installation_process.md`
- future `15_uzo_installation.md`
- source product documentation

Ожидаемый результат: either confirm with `statement_id`, reject, or keep as sales-context-only.

## 8. Предлагаемые статусы для будущего импорта

Если эту карту потом переносить в Postgres/слой ревью, использовать такие статусы:

- `context_only`: business/process context, not instruction.
- `candidate_operational_rule`: может стать правилом процесса после ревью владельца.
- `technical_confirmation_required`: нужен технический источник перед использованием.
- `safety_review_required`: safety-critical; blocked for instruction.
- `confirmed_by_electricians_kb`: matched to canonical electricians statement.
- `rejected_for_electricians_kb`: should not enter electricians KB.

## 9. Практический вывод

Главный результат связки: business interviews хорошо объясняют, почему менеджер должен собирать данные до выезда, почему клиентская история должна оставаться в CRM, почему электрик не должен владеть обещаниями клиенту, и какие вопросы нужно передавать на техническую проверку.

Но claims из интервью не должны усиливать техническую базу сами по себе. Для electricians KB они являются:

- контекстом процесса;
- источником вопросов для ревью;
- картой разрывов между sales discovery и монтажной заявкой;
- но не primary source для монтажных правил.

