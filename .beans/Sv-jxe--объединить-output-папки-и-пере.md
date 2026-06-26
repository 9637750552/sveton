---
# Sv-jxe
title: Объединить output-папки и перенумеровать верхние каталоги
status: completed
type: task
priority: normal
created_at: 2026-06-25T16:01:27Z
updated_at: 2026-06-25T16:04:52Z
---

Нужно объединить 04_output в 02_output, перенумеровать последующие верхние каталоги и обновить ссылки в документах/настройках.

- [x] Проверить содержимое и конфликты 02_output/04_output
- [x] Перенести 04_output в 02_output
- [x] Переименовать 05_research/06_website/07_scripts
- [x] Обновить ссылки в документах и настройках
- [x] Проверить итоговую структуру и экспортный скрипт
- [x] Закрыть задачу

## Summary of Changes

Объединены 02_output и 04_output: материалы из 04_output перенесены в 02_output без конфликтов. Верхние каталоги перенумерованы: 05_research -> 04_research, 06_website -> 05_website, 07_scripts -> 06_scripts. В convert_md.sh обновлен внутренний путь к export_html_to_pdf.ps1. Проверены старые ссылки на 04_output/05_research/06_website/07_scripts; экспорт Markdown в DOCX и PDF через 06_scripts/convert_md.sh успешно выполнен.
