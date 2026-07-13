---
# Sv-qro
title: Проверить подключение к Postgres базе знаний монтажников
status: completed
type: task
priority: normal
created_at: 2026-07-06T17:02:58Z
updated_at: 2026-07-06T17:06:07Z
---

Проверить доступ к базе sveton_kb_dev через SVETON_KB_DATABASE_URL и схему kb.

- [x] Проверить наличие переменной подключения
- [x] Проверить подключение к базе
- [x] Проверить доступ к corpus electricians_knowledge_base

## Summary of Changes

Подтверждено подключение к sveton_kb_dev через SVETON_KB_DATABASE_URL после удаления параметра schema и замены MagicDNS host на Tailscale IP 100.102.208.14. Проверены схема kb, таблицы и корпус electricians_knowledge_base.
