---
# Sv-nyl
title: Добавить сценарий некачественной самостоятельной подготовки клиента
status: completed
type: task
priority: normal
created_at: 2026-07-03T13:27:39Z
updated_at: 2026-07-03T13:29:14Z
---

В v3 нужно учесть, что если клиент делает подготовку сам/сторонним электриком, а электрик-партнер Светон на монтажном выезде обнаруживает некачественную подготовку, клиент либо оплачивает исправление партнеру, либо устраняет недочеты своим электриком и оплачивает холостой выезд. Стоимость исправления/холостого выезда согласуется напрямую между клиентом и электриком-партнером.

- [x] Найти места для предупреждения и проверки подготовки
- [x] Добавить коммерческую развилку при некачественной подготовке
- [x] Обновить диаграмму монтажа
- [x] Проверить рендер Mermaid

## Summary of Changes

- Added upfront warning when the client chooses self/third-party preparation but Sveton partner will do монтаж/настройка.
- Added second-visit readiness check by the Sveton partner electrician.
- Added branch for bad preparation: client either pays the partner to fix defects or fixes with their own executor and pays the partner for a wasted visit.
- Updated the монтаж diagram and rendered all Mermaid diagrams successfully.
