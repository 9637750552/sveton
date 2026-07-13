---
# Sv-2up
title: Create sales Collective and publish first page
status: completed
type: task
priority: high
created_at: 2026-07-04T14:08:55Z
updated_at: 2026-07-04T14:19:17Z
---

Создать новый Nextcloud Collective Продажи и добавить первый раздел 01 из подготовленного Markdown серверным способом, без использования старой sales wiki-папки.

- [x] Проверить текущие Collectives на сервере
- [x] Создать Collective Продажи, если его еще нет
- [x] Добавить первый раздел из 01_model_yug_responsibility.md
- [x] Переиндексировать/проверить Collective
- [x] Вернуть ссылку или точное место просмотра

## Summary of Changes

Создан Nextcloud Collective Продажи штатной командой occ collectives:create --owner=sergey. В коллектив импортирован первый раздел 01 - Модель продажи на Юге и границы ответственности.md через occ collectives:import:markdown. Выполнены generate-slugs и index. Проверено: collective ID 3, slug Prodazi, page DB id 33, file_id 2637.
