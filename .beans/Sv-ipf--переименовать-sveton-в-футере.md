---
# Sv-ipf
title: Переименовать Sveton в футере форм в СВЕТ ON
status: completed
type: task
priority: normal
created_at: 2026-06-29T12:48:31Z
updated_at: 2026-06-29T12:51:56Z
---

Точечно заменить текст бренда в публичном футере Nextcloud Forms: Sveton -> СВЕТ ON, не меняя глобальное имя темы.

- [x] Добавить точечную замену в шаблон
- [x] Проверить публичные формы

## Summary of Changes

В apps/theming/lib/ThemingDefaults.php добавлена отдельная переменная footerEntity: если глобальное имя темы Sveton, в коротком публичном футере выводится СВЕТ ON. Ссылка на https://sveton-ibp.ru и слоган сохранены. Apache перезапущен, обе публичные формы проверены.
