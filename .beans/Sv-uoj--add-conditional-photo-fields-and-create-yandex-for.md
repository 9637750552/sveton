---
# Sv-uoj
title: Add conditional photo fields and create Yandex form
status: completed
type: task
priority: normal
created_at: 2026-06-28T19:47:25Z
updated_at: 2026-06-28T19:49:38Z
---

Update 07_forms/input/electrician_screening_form.yaml with conditional photo-related fields, validate it, and create a Yandex Forms draft from the existing script. Note that current script stores visibleIf in source but does not apply display conditions through the API.

## Checklist

- [x] Add conditional photo upload field to YAML
- [x] Add conditional messenger follow-up field to YAML
- [x] Mirror conditional fields in the markdown questionnaire
- [x] Validate YAML with dry-run
- [x] Create Yandex Forms draft

## Summary of Changes

Added two photo-related conditional fields to 07_forms/input/electrician_screening_form.yaml and mirrored them in 01_docs/operations/ELECTRICIAN_SCREENING_FORM_260628.md. Created a Yandex Forms draft from the YAML: https://forms.yandex.ru/cloud/admin/6a417a91bf4fde41dca771d1/edit. The draft is not published. Yandex Forms manual setup remains required for logo, colors, required flags, maxSelections, and the two visibility rules.
