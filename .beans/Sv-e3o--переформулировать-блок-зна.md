---
# Sv-e3o
title: Переформулировать блок знаний и обновить Yandex форму
status: completed
type: task
priority: normal
created_at: 2026-06-28T19:55:33Z
updated_at: 2026-06-28T19:58:36Z
---

Переформулировать вопросы блока знаний в анкете электриков так, чтобы они проверяли понимание задачи, а не личный опыт работы с ИБП. Обновить Markdown, YAML, проверить dry-run и обновить форму в Yandex Forms.

## Checklist

- [x] Rewrite knowledge-block wording in Markdown
- [x] Rewrite matching questions and options in YAML
- [x] Validate YAML with dry-run
- [x] Update existing Yandex Forms draft through API
- [x] Verify updated Yandex questions remain multiple-choice

## Summary of Changes

Reworded the knowledge block so questions test understanding of reserve-power logic rather than asking what the candidate personally usually does. Updated 01_docs/operations/ELECTRICIAN_SCREENING_FORM_260628.md and 07_forms/input/electrician_screening_form.yaml. Dry-run validation passes with 25 questions. Existing Yandex Forms draft 6a417a91bf4fde41dca771d1 was updated through the API for questions q13-q21; q13, q15, and q21 were verified afterward as enum checkbox questions with the expected labels and options.
