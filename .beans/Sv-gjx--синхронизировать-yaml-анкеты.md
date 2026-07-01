---
# Sv-gjx
title: Синхронизировать YAML анкеты с ручными правками NC Forms
status: completed
type: task
priority: normal
created_at: 2026-06-29T10:02:57Z
updated_at: 2026-06-29T10:07:29Z
---

Забрать текущую форму электрика из Nextcloud Forms и обновить локальный YAML, сохранив служебные scoring/stopFactors.

- [x] Забрать текущую форму из Nextcloud Forms
- [x] Сравнить NC форму с локальным YAML
- [x] Обновить YAML без потери служебных блоков
- [x] Проверить YAML и diff

## Summary of Changes

- Считана текущая форма Nextcloud Forms ID 1 с nc.domibp.ru.
- Локальный YAML 07_forms/input/electrician_screening_form.yaml обновлен по живой NC форме: заголовок, вводная часть, 25 вопросов, типы, обязательность и варианты.
- Добавлен новый вопрос q03_city_other для населенного пункта, которого нет в списке.
- Сохранены служебные блоки stopFactors, scoring, visibleIf и maxSelections.
- Проверено: локальный YAML совпадает с NC по вопросам, create_nextcloud_form.py и create_yandex_form.py проходят dry-run на 25 вопросов.
