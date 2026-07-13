---
# Sv-ipl
title: Убрать accept из YAML анкеты партнера
status: completed
type: bug
created_at: 2026-07-07T18:22:12Z
updated_at: 2026-07-07T18:22:12Z
---

Nextcloud Forms API возвращал 500 при патче первого file-вопроса анкеты партнера.\n\n- [x] Убрать поле accept из partner_onboarding_form.yaml\n- [x] Проверить Nextcloud dry-run\n- [x] Проверить Yandex dry-run\n\n## Summary of Changes\n\nИз YAML удалено поле accept у q01_requisites_file. Ограничение Word/PDF оставлено в тексте описания и manualSettings, потому что текущий Nextcloud API на этом поле может падать 500.
