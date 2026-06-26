---
# Sv-4yp
title: Установить Mermaid CLI для рендера диаграмм
status: completed
type: task
priority: normal
created_at: 2026-06-25T16:19:59Z
updated_at: 2026-06-25T16:21:11Z
---

Нужно установить mmdc (@mermaid-js/mermaid-cli) в WSL и проверить доступность команды для дальнейшей доработки конвертации Markdown.

- [x] Установить @mermaid-js/mermaid-cli
- [x] Проверить mmdc --version
- [x] Проверить рендер тестовой диаграммы
- [x] Закрыть задачу

## Summary of Changes

Установлен @mermaid-js/mermaid-cli в пользовательский npm prefix. Команда mmdc доступна как /home/sergey/.npm-global/bin/mmdc, версия 11.15.0. Проверен рендер тестовой Mermaid-диаграммы в PNG.
