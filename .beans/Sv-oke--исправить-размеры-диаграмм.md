---
# Sv-oke
title: Исправить размеры диаграмм при конвертации DOCX/PDF
status: completed
type: bug
priority: normal
created_at: 2026-06-25T16:44:54Z
updated_at: 2026-06-25T16:52:31Z
---

Большие Mermaid-диаграммы в Word/PDF выходят за нижнюю границу страницы.

- [x] Проверить текущие размеры диаграмм в DOCX/PDF
- [x] Исправить конвертер Markdown так, чтобы Mermaid-картинки вписывались в страницу
- [x] Пересобрать DOCX и PDF
- [x] Визуально проверить результат

## Summary of Changes

- Added automatic Mermaid PNG sizing for Markdown conversion so diagrams fit within page bounds.
- Embedded PDF resources into the generated HTML before browser printing, so Mermaid images survive PDF export.
- Regenerated and visually checked PDF pages; checked DOCX image sizes and Word-rendered pages from the corrected DOCX.
