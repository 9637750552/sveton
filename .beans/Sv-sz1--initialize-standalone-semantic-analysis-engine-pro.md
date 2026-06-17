---
# Sv-sz1
title: Initialize standalone semantic-analysis-engine project
status: completed
type: task
priority: normal
created_at: 2026-06-17T11:16:20Z
updated_at: 2026-06-17T11:18:28Z
parent: Sv-9to
---

Create a standalone semantic-analysis-engine project with reusable extraction scripts, schemas, prompts, docs, and smoke checks while keeping Sveton operational.

Checklist:
- [x] Create standalone project directory and git repository.
- [x] Copy reusable semantic scripts into the standalone project.
- [x] Copy schemas and prompt templates into project-owned folders.
- [x] Add README, AGENTS, example project config, and package metadata.
- [x] Run smoke checks against the Sveton corpus from the standalone project.
- [x] Link the standalone project from Sveton governance.
- [x] Update Beans with Phase 2 result.

## Summary of Changes

Created `/home/sergey/semantic-analysis-engine` as the initial standalone Semantic Analysis Engine project.

Copied reusable scripts, schemas, prompt template, and an example Sveton project config. Added standalone README, AGENTS, project contract docs, `.gitignore`, and `pyproject.toml`.

External smoke checks passed against `/home/sergey/Sveton`:

- Python scripts compile.
- `validate_atomic_statements.py`: 387 valid statements.
- `check_source_coverage.py`: reads external project config and writes smoke output to `99_tmp`.
- `run_atomic_extraction.py prepare`: prepares a 1-chunk temp run under `99_tmp`.
- `build_source_chunks.py`: writes 146 temp chunks for 17 documents under `99_tmp`.
