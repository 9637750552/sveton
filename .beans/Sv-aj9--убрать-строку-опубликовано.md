---
# Sv-aj9
title: Убрать строку опубликовано пользователем из header Nextcloud Forms
status: completed
type: task
priority: normal
created_at: 2026-06-29T12:29:38Z
updated_at: 2026-06-29T12:33:31Z
---

Скрыть публичную строку Опубликовано пользователем Sergey Elyutin в header Nextcloud Forms, оставив логотип и название формы.

- [x] Найти источник строки header
- [x] Применить минимальное изменение
- [x] Проверить публичные формы

## Summary of Changes

Из публичного шаблона Nextcloud core/templates/layout.public.php удален вывод span.header-shared-by. Заголовок формы и логотип сохранены. Резервная копия на сервере: /var/www/nextcloud/core/templates/layout.public.php.bak-sveton-20260629-hide-shared-by. Обе публичные формы проверены: header-shared-by / Shared by / Опубликовано в HTML отсутствуют.
