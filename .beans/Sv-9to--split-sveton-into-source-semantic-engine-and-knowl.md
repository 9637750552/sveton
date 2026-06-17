---
# Sv-9to
title: Split Sveton into source, semantic engine, and knowledge base projects
status: in-progress
type: epic
created_at: 2026-06-17T10:35:42Z
updated_at: 2026-06-17T10:35:42Z
---

Goal: define and execute the separation of the current repository into three logical projects: Sveton source/business workspace, reusable semantic analysis engine, and Sveton knowledge base product.

Checklist:
- [x] Document target project boundaries.
- [x] Define migration phases.
- [x] Define contracts between projects.
- [x] Link the decision from project governance.

## Phase 0 Result

Project boundaries are documented in `01_docs/governance/PROJECT_BOUNDARIES.md` and linked from governance rules.

## Next Checklist

- [ ] Extract hardcoded corpus paths from semantic scripts into project config.
- [ ] Create or initialize the separate `semantic-analysis-engine` project.
- [ ] Define the `sveton-knowledge-base` repository/package layout.
- [ ] Plan the first migration commit set without breaking current canonical data.
