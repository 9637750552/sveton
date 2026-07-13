# Speaker mapping for leadership and manager interviews

Дата создания: 2026-07-02

## Назначение

Этот файл фиксирует правила и рабочие карточки сопоставления speaker labels
из diarized TXT-стенограмм с реальными участниками интервью.

Сырые стенограммы не редактируются. Все уточнения по участникам, ролям,
качеству диаризации и надежности speaker labels фиксируются только здесь.

## Основное правило

Перед разбором каждой конкретной стенограммы:

1. Codex показывает карточку файла: имя, предполагаемую дату, первые фрагменты,
   список найденных `SPEAKER_XX`.
2. Пользователь по памяти сообщает:
   - кто участвовал в разговоре;
   - кто, вероятно, соответствует каким `SPEAKER_XX`;
   - где есть уверенность;
   - где диаризация плавает или ненадежна.
3. Codex фиксирует решение в этом файле.
4. Исходный TXT-файл не изменяется.

Если сопоставление ненадежно, extraction сохраняет только локальную speaker
метку (`SPEAKER_01`, `SPEAKER_02` и т.д.) и статус `needs_mapping`.

Если пользователь явно принимает повторяющуюся ошибку диаризации как рабочую
поправку для конкретного файла, такая speaker label используется как
`confirmed` для extraction. Это не означает проверку по аудио; это означает,
что данная label не должна сама по себе создавать review queue. Review должен
создаваться по содержательным причинам: технические утверждения, цены,
надежность, маркетинговые обещания, стратегические гипотезы или явный шум
распознавания.

## Уровни надежности

- `confirmed`: пользователь уверенно подтвердил соответствие speaker label
  конкретному человеку или роли для данного файла; также используется для
  явной ручной поправки повторяющейся ошибки диаризации, если пользователь
  сказал считать эту label конкретным участником.
- `likely`: сопоставление вероятно, но основано на памяти и содержании, без
  прямой проверки по аудио.
- `low_confidence`: есть рабочая гипотеза, но speaker label может прыгать.
- `unreliable`: диаризация явно ненадежна; speaker label нельзя использовать
  как личность.
- `needs_mapping`: участник или speaker label пока не сопоставлен.

## Правила использования в extraction

В future claims обязательно сохранять:

- `source_file`;
- `source_interview_id`;
- `speaker_label`;
- `speaker_identity`, если подтверждено;
- `speaker_role`, если подтверждено;
- `speaker_mapping_confidence`;
- `mapping_source`, например `user_confirmed_in_chat`;
- `source_quote`;
- `start_timestamp`;
- `end_timestamp`.

Если speaker mapping не подтвержден и нет ручной поправки для данного файла,
использовать:

```json
{
  "speaker_identity": "needs_mapping",
  "speaker_role": "needs_mapping",
  "speaker_mapping_confidence": "unreliable"
}
```

## Corpus-level warning

Текущие стенограммы имеют автоматическую диаризацию. По замечанию пользователя,
разделение на `SPEAKER_01`, `SPEAKER_02` и другие labels может быть некорректным.
Одинаковая speaker label не должна автоматически считаться одним человеком на
протяжении всего файла или между разными файлами.

Для Business / Sales / Commercial KB важнее:

- точная цитата;
- timestamp;
- тема разговора;
- список участников файла;
- надежность утверждения;
- review status.

Точная личность каждой реплики используется только там, где она подтверждена.

## Interview cards

### interview_001

- Source file: `260405_sveton_converted_t_large-v3_diar.txt`
- Assumed date: 2026-04-05
- Topic: first business-model discussion for southern branch preparation, including филиалы, прорабы, SMB, monitoring, pitch, product/service value, and internal developments.
- Participants confirmed by user: Дмитрий, генеральный директор Светон; Сергей, директор южного филиала / новый сотрудник, разбирающий бизнес-модель и материалы для запуска южного филиала.
- Diarization status: manual_override_accepted_for_extraction; `SPEAKER_03` and `SPEAKER_00` are treated as recurring diarization artifacts with accepted manual mapping.
- Mapping source: user_confirmed_in_chat, 2026-07-02

| Speaker label | Identity | Role | Confidence | Notes |
|---|---|---|---|---|
| SPEAKER_01 | Дмитрий | генеральный директор Светон | confirmed | Пользователь подтвердил: `01` это Дмитрий. |
| SPEAKER_02 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | Пользователь подтвердил, что это он; задает вопросы и формирует материалы для южного филиала. |
| SPEAKER_03 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | Ручная поправка диаризации: пользователь сказал считать `03` Сергеем, чтобы не отправлять такие реплики на review только из-за speaker label. |
| SPEAKER_00 | Дмитрий | генеральный директор Светон | confirmed | Ручная поправка диаризации: пользователь сказал считать `00` Дмитрием, чтобы не отправлять такие реплики на review только из-за speaker label. |

### interview_002

- Source file: `260405_sveton_2_converted_t_large-v3_diar.txt`
- Assumed date: 2026-04-05
- Topic: second business-model and sales-process discussion for southern branch preparation, including customer profile, SMB segments, regional model, sales funnel, commercial process, competitors, growth constraints, finances, staffing, and development priorities.
- Participants confirmed by user: Дмитрий, генеральный директор Светон; Сергей, директор южного филиала / новый сотрудник, разбирающий бизнес-модель и материалы для запуска южного филиала.
- Diarization status: manual_override_accepted_for_extraction; `SPEAKER_00` is treated as Дмитрий.
- Mapping source: user_confirmed_in_chat, 2026-07-02

| Speaker label | Identity | Role | Confidence | Notes |
|---|---|---|---|---|
| SPEAKER_00 | Дмитрий | генеральный директор Светон | confirmed | Пользователь подтвердил: `SPEAKER_00 = Дмитрий`. |
| SPEAKER_01 | Дмитрий | генеральный директор Светон | confirmed | По содержанию и продолжению первого интервью это основная label Дмитрия; пользователь подтвердил `SPEAKER_00`, не возражал против карточки `SPEAKER_01 = Дмитрий`. |
| SPEAKER_02 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | По содержанию это Сергей: задает вопросы, ведет интервью и формирует материалы для южного филиала. |

### interview_003

- Source file: `260408_sveton3_converted_t_large-v3_diar.txt`
- Assumed date: 2026-04-08
- Topic: technical-commercial discussion with the commercial director, including inverter types, double conversion, stabilizers, installer/engineer roles, manager discovery, load calculation, bypass cabinet, technical constraints on installation, sales explanation strategy, customer age/gender patterns, and private-home backup sizing.
- Participants confirmed by user: Алексей, коммерческий директор; Сергей, директор южного филиала / новый сотрудник, разбирающий бизнес-модель и материалы для запуска южного филиала.
- Diarization status: manual_override_accepted_for_extraction; `SPEAKER_00` is treated as Алексей.
- Mapping source: user_confirmed_in_chat, 2026-07-02

| Speaker label | Identity | Role | Confidence | Notes |
|---|---|---|---|---|
| SPEAKER_00 | Алексей | коммерческий директор Светон | confirmed | Пользователь подтвердил: `00` это Алексей. |
| SPEAKER_01 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | Пользователь подтвердил: `01` это Сергей. |
| SPEAKER_02 | Алексей | коммерческий директор Светон | confirmed | Пользователь подтвердил: `02` это Алексей. |

### interview_004

- Source file: `260408_sveton4_converted_t_large-v3_diar.txt`
- Assumed date: 2026-04-08
- Topic: continuation of technical-commercial and regional model discussion with the commercial director, including southern region market testing, partner/agent model, SMB segments, installation constraints, regional electricians/installers, training materials, logistics, and later an off-topic camping business discussion.
- Participants confirmed by user: Алексей, коммерческий директор; Сергей, директор южного филиала / новый сотрудник, разбирающий бизнес-модель и материалы для запуска южного филиала.
- Diarization status: manual_override_accepted_for_extraction; `SPEAKER_00` and `SPEAKER_03` are treated as Алексей.
- Mapping source: user_confirmed_in_chat, 2026-07-02

| Speaker label | Identity | Role | Confidence | Notes |
|---|---|---|---|---|
| SPEAKER_00 | Алексей | коммерческий директор Светон | confirmed | Пользователь подтвердил: `00` это Алексей. |
| SPEAKER_01 | Алексей | коммерческий директор Светон | confirmed | По карточке файла это основная label Алексея; пользователь подтвердил дополнительные labels `00` и `03` как Алексея. |
| SPEAKER_02 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | По содержанию это Сергей: обсуждает региональную гипотезу, тестирование рынка и кемпинг. |
| SPEAKER_03 | Алексей | коммерческий директор Светон | confirmed | Пользователь подтвердил: `03` это Алексей. |

### interview_005

- Source file: `260609_sveton_converted_t_large-v3_diar.txt`
- Assumed date: 2026-06-09
- Topic: focused discussion on MVP testing of regional electrician outreach, electrician vs foreman role, object audit checklist, cold market testing, inspection compensation, and initial system sizing logic.
- Participants confirmed by user: Дмитрий, генеральный директор Светон; Сергей, директор южного филиала / новый сотрудник, тестирующий региональную модель.
- Diarization status: confirmed_for_extraction.
- Mapping source: user_confirmed_in_chat, 2026-07-03

| Speaker label | Identity | Role | Confidence | Notes |
|---|---|---|---|---|
| SPEAKER_00 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | Пользователь подтвердил mapping для файла. |
| SPEAKER_01 | Дмитрий | генеральный директор Светон | confirmed | Пользователь подтвердил mapping для файла. |

### interview_006

- Source file: `260609_sveton_2_converted_t_large-v3_diar.txt`
- Assumed date: 2026-06-09
- Topic: continuation of June 9 discussion with Дмитрий, including marketing upsell logic, peak/nominal load calculation, 1C questionnaire workflow, commercial offer preparation, electrician inspection, photo evidence, installer task cards, regional specialist model, and next steps for cold outreach to electricians.
- Participants confirmed by user: Дмитрий, генеральный директор Светон; Сергей, директор южного филиала / новый сотрудник, тестирующий региональную модель.
- Diarization status: manual_override_accepted_for_extraction; `SPEAKER_00` is treated as Дмитрий and `SPEAKER_03` is treated as Сергей.
- Mapping source: user_confirmed_in_chat, 2026-07-03

| Speaker label | Identity | Role | Confidence | Notes |
|---|---|---|---|---|
| SPEAKER_00 | Дмитрий | генеральный директор Светон | confirmed | Пользователь подтвердил mapping для файла; редкая label/ошибка диаризации. |
| SPEAKER_01 | Дмитрий | генеральный директор Светон | confirmed | Пользователь подтвердил mapping для файла; основная label Дмитрия. |
| SPEAKER_02 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | Пользователь подтвердил mapping для файла; основная label Сергея. |
| SPEAKER_03 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | Пользователь подтвердил mapping для файла; редкая label/ошибка диаризации. |

### interview_007

- Source file: `260610_sveton_converted_t_large-v3_diar.txt`
- Assumed date: 2026-06-10
- Topic: three-person discussion with Дмитрий, Сергей, and Вадик about inverter overload behavior, bypass, power/battery sizing, customer-facing explanations, remote qualification before site visit, CRM ownership, service model, electricians/foremen as channels, scalable outsourced electrician model, technical edge cases with boilers/grounding, customer motivation, documentation, and first regional next steps.
- Participants confirmed by user: Дмитрий, генеральный директор Светон; Сергей, директор южного филиала / новый сотрудник; Вадик, участник обсуждения региональной модели / потенциальный специалист южного направления.
- Diarization status: manual_override_accepted_for_extraction; `SPEAKER_00` is treated as Дмитрий.
- Mapping source: user_confirmed_in_chat, 2026-07-03

| Speaker label | Identity | Role | Confidence | Notes |
|---|---|---|---|---|
| SPEAKER_00 | Дмитрий | генеральный директор Светон | confirmed | Пользователь подтвердил mapping для файла; редкая label/ошибка диаризации. |
| SPEAKER_01 | Сергей | директор южного филиала; новый сотрудник; интервьюер/аналитик бизнес-модели | confirmed | Пользователь подтвердил mapping для файла. |
| SPEAKER_02 | Дмитрий | генеральный директор Светон | confirmed | Пользователь подтвердил mapping для файла; основная label Дмитрия. |
| SPEAKER_03 | Вадик | участник обсуждения региональной модели; потенциальный специалист/партнер южного направления | confirmed | Пользователь подтвердил mapping для файла. |

## Update protocol

Когда пользователь подтверждает участников для конкретного файла, обновить
только карточку этого файла:

- заполнить `Topic`;
- заполнить `Participants confirmed by user`;
- указать `Diarization status`;
- заменить `needs_scan` строками по фактически найденным speaker labels;
- указать `Mapping source: user_confirmed_in_chat`;
- добавить дату обновления и краткие notes.

Если позже выясняется, что mapping был ошибочным, не переписывать историю
молча. Добавить notes с датой уточнения и новым статусом надежности.
