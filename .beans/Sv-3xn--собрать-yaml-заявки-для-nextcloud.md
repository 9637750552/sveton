---
# Sv-3xn
title: Собрать YAML Заявки для Nextcloud Forms
status: completed
type: task
priority: normal
created_at: 2026-07-06T17:55:54Z
updated_at: 2026-07-06T17:59:04Z
---

Подготовить YAML-вопросник Заявки по шаблону существующей Nextcloud Forms анкеты.\n\n- [x] Проверить поддерживаемый формат YAML\n- [x] Составить вопросы Заявки по подготовленному Markdown\n- [x] Сохранить новый YAML в 07_forms/input\n- [x] Проверить YAML на валидность и полноту

## Summary of Changes

Создан YAML-вопросник Заявки для Nextcloud Forms: 53 вопроса, 16 секций, 34 обязательных вопроса, отдельное поле загрузки фото/видео/файлов. Файл прошел YAML-парсинг и dry-run 07_forms/create_nextcloud_form.py.
