---
# Sv-kjv
title: Разрешить несколько файлов в поле фото работ NC Forms
status: completed
type: task
priority: normal
created_at: 2026-07-01T12:55:46Z
updated_at: 2026-07-01T13:00:05Z
---

Сделать поле загрузки фото работ в анкете электрика множественным, чтобы можно было приложить 3-5 файлов.

- [x] Найти настройку multiple files в Nextcloud Forms
- [x] Обновить YAML и/или скрипт синхронизации
- [x] Синхронизировать форму NC и проверить

## Summary of Changes

В YAML для q12_upload_photos добавлен лимит maxAllowedFilesCount 5. Живая Nextcloud Forms форма ID 1 обновлена: file-вопрос ID 13 теперь принимает до 5 файлов. Публичная форма проверена через decoded initial-state.
