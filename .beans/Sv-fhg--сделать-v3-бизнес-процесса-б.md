---
# Sv-fhg
title: Сделать v3 бизнес-процесса без монтажа на первом выезде
status: completed
type: task
priority: normal
created_at: 2026-07-03T11:20:43Z
updated_at: 2026-07-03T11:26:53Z
---

Актуальный бизнес-процесс находится в Nextcloud. Нужно сохранить v2 и создать v3 рядом, убрав двойственные сценарии: первый выезд только осмотр, второй выезд включает подготовку, щит, трассы/каблирование, монтаж и настройку ИБП.

- [x] Создать копию v3 рядом с v2
- [x] Убрать подготовку/монтаж с первого выезда
- [x] Обновить этап второго выезда и диаграммы
- [x] Проверить, что в v3 не осталось противоречий по первому выезду

## Summary of Changes

- Created south_ups_sales_installation_process_v3.md next to v2.
- Removed the scenario where preparation or монтажные работы happen during the first visit.
- Removed second-visit branching between ready/not-ready object; second visit now includes preparation and монтаж.
- Updated Mermaid files in the same folder and rendered all diagrams successfully with mmdc.
