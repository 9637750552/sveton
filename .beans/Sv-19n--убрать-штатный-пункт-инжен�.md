---
# Sv-19n
title: Убрать штатный пункт инженерной консультации из v3
status: completed
type: task
priority: normal
created_at: 2026-07-03T12:36:21Z
updated_at: 2026-07-03T12:39:43Z
---

Коллега отклонил инженерную консультацию как штатный этап. Нужно убрать пункт 21 и перестроить этап 6 так, чтобы контроль инженера был только исключением для первых монтажей/нестандартных вопросов по оборудованию ИБП, а не обязательной частью процесса.

- [x] Проверить текущий этап 6 и связанные диаграммы
- [x] Убрать штатный пункт 21
- [x] Обновить диаграммы и короткую схему
- [x] Проверить отсутствие штатной инженерной консультации

## Summary of Changes

- Removed the штатный engineering consultation/control stage from the normal process.
- Kept engineer involvement only as a non-numbered exception note for first training installs or nonstandard UPS/equipment situations.
- Renumbered subsequent stages and steps.
- Removed engineer-control branch from the second-visit diagram and synchronized embedded Mermaid blocks with external .mmd files.
- Rendered all six Mermaid diagrams successfully and verified no штатная engineering consultation remains.
