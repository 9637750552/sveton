---
# Sv-le5
title: Создать Nextcloud Forms версию анкеты электрика
status: completed
type: task
priority: normal
created_at: 2026-06-28T20:08:35Z
updated_at: 2026-06-28T20:16:32Z
---

Сделать аналог актуальной анкеты электрика в Nextcloud Forms на базе текущего YAML и адаптированного скрипта из C:\Projects\your_camping_managementorms.

- [x] Изучить внешний скрипт Nextcloud Forms и требования API
- [x] Адаптировать скрипт под проект Светон и текущий YAML
- [x] Создать/обновить форму в нашем Nextcloud Forms
- [x] Проверить результат и описать ограничения

## Summary of Changes

- Адаптирован скрипт create_nextcloud_form.py из C:\Projects\your_camping_managementorms под проект Светон.
- Создана и синхронизирована Nextcloud Forms форма ID 14 по 07_forms/input/electrician_screening_form.yaml.
- Проверено через API: 24 вопроса, 22 обязательных, 1 публичная ссылка, 9 ограничений maxSelections.
- Публичная ссылка для кандидатов: https://nc2.c2030.ru/apps/forms/s/75AdRnf9QA6DrrkrWqqaR6Mk
- В YAML и README добавлены сведения о Nextcloud Forms и ручных проверках.
