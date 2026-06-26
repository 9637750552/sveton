---
# Sv-3uq
title: Добавить рендер Mermaid в convert_md
status: completed
type: task
priority: normal
created_at: 2026-06-25T16:27:54Z
updated_at: 2026-06-25T16:29:23Z
---

Нужно доработать 06_scripts/convert_md.sh, чтобы Mermaid-блоки перед конвертацией рендерились в изображения и попадали в DOCX/PDF как картинки.

- [x] Добавить препроцессинг Mermaid-блоков
- [x] Подключить mmdc и временные PNG
- [x] Проверить DOCX-конвертацию
- [x] Проверить PDF-конвертацию
- [x] Закрыть задачу

## Summary of Changes

06_scripts/convert_md.sh теперь перед запуском Pandoc находит fenced-блоки mermaid, рендерит их через mmdc в PNG во временную папку и подставляет изображения в временный Markdown. Проверена конвертация south_ups_sales_installation_process.md в DOCX и PDF: DOCX содержит 6 PNG-изображений, Mermaid-текст в DOCX/PDF не попадает.
