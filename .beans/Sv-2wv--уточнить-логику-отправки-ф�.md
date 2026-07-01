---
# Sv-2wv
title: Уточнить логику отправки фото в анкете и Yandex форме
status: completed
type: task
priority: normal
created_at: 2026-06-28T20:02:18Z
updated_at: 2026-06-28T20:04:06Z
---

Нужно заменить вариант ответа про отправку фото после анкеты на понятный вариант: кандидат готов отправить фото в ответ на наш запрос. Убрать лишнее условное поле q12_photo_messenger из Markdown, YAML и Yandex Forms draft. Проверить YAML и обновить существующий черновик формы.

## Checklist

- [x] Rewrite photo answer in Markdown
- [x] Rewrite photo answer in YAML
- [x] Remove extra q12_photo_messenger field from YAML
- [x] Validate YAML with dry-run
- [x] Update existing Yandex Forms draft
- [x] Verify Yandex draft through API

## Summary of Changes

Updated the photo workflow wording: candidates can either upload photos immediately or agree to send them after our request. Removed the extra q12_photo_messenger field from Markdown/YAML and deleted it from the existing Yandex Forms draft. The Yandex draft now keeps only q12_work_photos and q12_upload_photos for the photo flow.
