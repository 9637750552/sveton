---
# Sv-ova
title: Обновить Windows env пароль для Nextcloud Forms
status: completed
type: task
priority: normal
created_at: 2026-07-06T18:09:24Z
updated_at: 2026-07-06T18:10:00Z
---

Обновить Windows user environment переменную NEXTCLOUD_APP_PASSWORD актуальным значением и подтвердить авторизацию.

- [ ] Обновить Windows env переменную NEXTCLOUD_APP_PASSWORD
- [ ] Проверить авторизацию Nextcloud с новым значением
- [x] Зафиксировать результат в bean

## Summary of Changes

- Обновил Windows user environment переменную NEXTCLOUD_APP_PASSWORD на актуальное рабочее значение.
- Проверил авторизацию на https://nc.domibp.ru/ocs/v2.php/cloud/user?format=json: сервер вернул 200 OK.
- Подтвердил, что проблема была в устаревшем значении переменной среды, а не в самом Nextcloud Forms.
