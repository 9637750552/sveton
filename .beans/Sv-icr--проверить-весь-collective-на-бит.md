---
# Sv-icr
title: Проверить весь collective на битый Text markup
status: completed
type: bug
priority: normal
created_at: 2026-06-29T20:03:52Z
updated_at: 2026-06-29T20:06:03Z
---

Проверить все страницы collective монтажников на остатки битого внутреннего Text/Collective markup и вычистить найденные случаи.

- [x] Проверить markdown-файлы collective на явный мусор.
- [x] Проверить внутренний Text-слой по страницам collective.
- [x] Исправить найденные поврежденные страницы.
- [x] Проверить итог в браузере и обновить индекс.

## Summary of Changes

Проверены все страницы collective монтажников в двух слоях: markdown-файлы и видимый Text/Collective-рендер через браузер. Явный мусор в markdown-файлах не найден. Внутренний сломанный Text-слой остался только у корневой страницы Readme (document_id=974). Для него очищены oc_text_documents, oc_text_steps и oc_text_sessions, затем выполнена переиндексация collective. После этого корневая страница рендерится чисто; страницы 00-17 по проверке браузером не содержат битого markup.
