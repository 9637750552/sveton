---
# Sv-1l4
title: Починить отображение вариантов ответов в Nextcloud Forms
status: completed
type: bug
priority: normal
created_at: 2026-06-28T20:24:01Z
updated_at: 2026-06-28T20:28:15Z
---

В форме на nc.domibp.ru созданы заголовки вопросов, но варианты ответов не отображаются в UI. Нужно исправить формат options через API и обновить форму.

- [x] Проверить структуру questions/options в API
- [x] Найти корректный формат optionType для Nextcloud Forms
- [x] Исправить скрипт и форму
- [x] Проверить публичную форму в браузере/API

## Summary of Changes

- Причина: варианты ответов были созданы с optionType = null, из-за чего Nextcloud Forms не отображал radio/checkbox в публичной форме.
- Скрипт 07_forms/create_nextcloud_form.py обновлен: новые варианты создаются с optionType = choice, существующие варианты при синхронизации допатчиваются до choice.
- Форма ID 1 на nc.domibp.ru пересинхронизирована.
- Проверено через API: 118 вариантов, 0 null optionType, 118 choice.
- Проверено в браузере: вопрос города показывает radio-варианты Краснодар, Горячий Ключ, Анапа и остальные.
