---
# Sv-qad
title: Подтянуть Windows env в WSL для Yandex Forms
status: completed
type: bug
priority: normal
created_at: 2026-06-25T17:38:05Z
updated_at: 2026-06-25T17:38:40Z
---

Добавить чтение YANDEX_FORMS_TOKEN и YANDEX_FORMS_ORG_ID из пользовательских переменных Windows при запуске create_yandex_form.py из WSL.

- [x] Проверить текущую логику чтения env
- [x] Добавить fallback на Windows env из WSL
- [x] Проверить запуск

## Summary of Changes

- Добавлен fallback на пользовательские переменные Windows через powershell.exe при запуске из WSL.
- get_env теперь подхватывает YANDEX_FORMS_TOKEN и YANDEX_FORMS_ORG_ID без ручного export в Linux-сессии.
- Чтение токена и org id подтверждено в текущем окружении.
