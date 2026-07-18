---
# Sv-zj3
title: Учесть подготовку объекта силами клиента или стороннего электрика
status: completed
type: task
priority: normal
created_at: 2026-07-03T12:28:10Z
updated_at: 2026-07-03T12:32:49Z
---

В v3 нужно учесть, что после первого выезда клиент может подготовить объект своими силами или через другого монтажника по ТЗ. При этом первый выезд остается только осмотром, а подготовка нашим электриком делается только во второй выезд вместе с монтажом.

- [x] Проверить текущие шаги 18-20 и диаграммы
- [x] Добавить выбор способа подготовки после первого выезда
- [x] Развести второй выезд для готового и неподготовленного объекта без возврата монтажа на первый выезд
- [x] Обновить Mermaid-диаграммы и проверить рендер

## Summary of Changes

- Added explicit choice of object preparation method after the first visit: client, client-side electrician/installer, or Sveton partner electrician on the second visit.
- Updated second-visit logic: if the object is prepared by the client or third party, Sveton partner electrician performs mounting/configuration only; if not, he performs preparation plus mounting on the second visit.
- Updated embedded Mermaid blocks and external .mmd files, then rendered all six diagrams successfully.
- Verified there are no remaining references to preparation work during the first visit.
