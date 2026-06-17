---
# Sv-yvi
title: Parameterize semantic scripts with project config
status: completed
type: task
priority: normal
created_at: 2026-06-17T10:59:39Z
updated_at: 2026-06-17T11:05:10Z
parent: Sv-9to
---

Introduce a project config for the current Sveton electricians corpus and remove hardcoded corpus paths from reusable semantic scripts.

Checklist:
- [x] Add project config for the electricians knowledge-base corpus.
- [x] Update chunk/source scripts to read configured paths.
- [x] Update validation/coverage/extraction scripts to read configured paths.
- [x] Run smoke checks without changing canonical data.
- [x] Update Beans with Phase 1 result.

## Summary of Changes

Added `semantic_project.yml` and a shared config loader for semantic scripts.

Updated chunking, validation, coverage, extraction runner, image inventory, image enrichment, image extraction, and text extraction helpers to read configured corpus paths while keeping existing defaults.

Smoke checks passed without changing canonical data:

- `validate_atomic_statements.py`: 387 valid statements.
- `check_source_coverage.py`: read config and wrote reports to `99_tmp`.
- `run_atomic_extraction.py prepare`: prepared 1 temp chunk under `99_tmp`.
- `build_source_chunks.py`: wrote 146 temp chunks for 17 documents under `99_tmp`.
