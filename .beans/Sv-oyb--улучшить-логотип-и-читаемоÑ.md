---
# Sv-oyb
title: Улучшить логотип и читаемость header Nextcloud Forms
status: completed
type: task
priority: normal
created_at: 2026-06-29T12:36:08Z
updated_at: 2026-06-29T12:39:21Z
---

Увеличить логотип в публичном header Nextcloud Forms, добавить белую подложку и зафиксировать белый цвет текста на синем фоне.

- [x] Найти текущее место правки header
- [x] Добавить стили для публичного header
- [x] Проверить публичные формы

## Summary of Changes

В публичный шаблон Nextcloud Forms добавлен inline CSS sveton-public-header-style: логотип увеличен до 96px, добавлена белая подложка, фильтр инверсии отключен, текст header закреплен белым цветом. Apache перезапущен, обе публичные формы проверены: CSS-блок отдается в HTML. Резервная копия: /var/www/nextcloud/core/templates/layout.public.php.bak-sveton-20260629-logo-header.
