---
# Sv-li1
title: Перенести анкету электрика в правильный Nextcloud Forms
status: completed
type: bug
priority: normal
created_at: 2026-06-28T20:17:52Z
updated_at: 2026-06-28T20:22:08Z
---

Исправить ошибку хоста: удалить форму электрика с nc2.c2030.ru и создать такую же форму на рабочем Nextcloud nc.domibp.ru.

- [x] Удалить ошибочную форму с nc2.c2030.ru
- [x] Найти корректные доступы к nc.domibp.ru
- [x] Создать форму на nc.domibp.ru
- [x] Проверить публичную ссылку и обновить YAML/README

## Summary of Changes

- Удалена ошибочно созданная форма электрика с неверного Nextcloud-хоста.
- Создана форма электрика на рабочем Nextcloud nc.domibp.ru, форма ID 1.
- Проверено через API и публичную ссылку: 24 вопроса, 22 обязательных, 1 public share, 9 maxSelections.
- YAML и README обновлены на правильный хост и ссылку.
- Скрипт create_nextcloud_form.py теперь берет nextcloudForms.baseUrl из YAML перед NEXTCLOUD_BASE_URL, чтобы не увести эту анкету на старый хост.
