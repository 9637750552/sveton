---
# Sv-6vc
title: Extract doc_010 qualification levels statements
status: completed
type: task
priority: normal
created_at: 2026-06-22T19:19:14Z
updated_at: 2026-06-22T19:29:08Z
---

## Goal

Выполнить semantic extraction для doc_010 по стратегии qualification levels, собрать валидные atomic statements и подготовить artifacts, совместимые с текущим Postgres importer.

## Checklist

- [x] Подготовить отдельный run только для doc_010 chunks
- [x] Сгенерировать raw JSON ответы по всем chunks
- [x] Собрать parsed artifacts через collect и проверить warnings/errors
- [x] Подготовить summary и точки для следующего canonical promotion pass

## Summary of Changes

Создан отдельный extraction run un_20260622_doc010_qualification_levels_v1 только для doc_010_chunk_0001..0003.
Записаны raw JSON ответы с level-scoped qualification statements и выполнен штатный collect-проход.
Результат: 60 валидных atomic statements, 0 extraction errors, 0 coverage warnings, promotion в canonical не выполнялся.
Следующий шаг для canonical слоя: review выборки, затем при подтверждении пользователя promotion и обновление statement_clusters.json / statement_relations.jsonl / coverage artifacts под новый source.
