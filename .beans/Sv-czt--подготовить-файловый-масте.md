---
# Sv-czt
title: Подготовить файловый мастер-слой База знаний/Электрики и База знаний/Продажи
status: completed
type: task
priority: normal
created_at: 2026-07-03T16:40:22Z
updated_at: 2026-07-03T16:43:41Z
---

Подготовить в Nextcloud файловый мастер-слой для базы знаний: создать папки База знаний/Электрики и База знаний/Продажи, выгрузить текущие страницы Collective электриков в обычные файлы и подготовить папку Продажи для текущих экспортов.

- [x] Найти фактический способ доступа к рабочему Nextcloud-хранилищу.
- [x] Создать папки База знаний/Электрики и База знаний/Продажи.
- [x] Выгрузить текущие страницы collective электриков в файловую папку Электрики.
- [x] Подготовить папку Продажи и положить туда текущие sales-материалы.
- [x] Проверить итоговую структуру и зафиксировать результат.

## Summary of Changes

Рабочий Nextcloud sync-корень подтвержден как `C:\Users\serge\Nextcloud2\Компания\База знаний`. Внутри него созданы папки `Электрики` и `Продажи`.

В `Электрики` выгружены текущие страницы collective `Инструкции монтажников DOMIBP` напрямую из внутреннего storage Nextcloud: `/var/www/nextcloud-data/appdata_oca57jrez2dd/collectives/2`. Получен файловый мастер-слой из 19 элементов: root `Readme.md`, страницы `00-16`, подпапка страницы `02 - Как устроен процесс по объекту`, и `.templates`.

В `Продажи` скопированы 9 актуальных markdown-экспортов из `00_input/interviews/exports`:
- business_sales_commercial_kb.md
- business_model_map.md
- sales_playbook.md
- objection_handling.md
- manager_training_outline.md
- commercial_messaging.md
- links_to_electricians_kb.md
- website_content_bank.md
- presentation_outline.md
