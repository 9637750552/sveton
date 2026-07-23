---
# Sv-5kw
title: Fix Contract_revier appendix signatures and checklist numbering
status: completed
type: bug
priority: normal
created_at: 2026-07-22T10:03:57Z
updated_at: 2026-07-22T12:02:05Z
---

Fix duplicate signatures in Appendix 1 and correct Appendix 4 checklist title/section order in the generated Contract_revier PDF.

- [x] Remove duplicate Appendix 1 signature block from PDF build
- [x] Add Appendix N 4 marker to checklist heading
- [x] Move checklist section 4 into numeric order
- [x] Rebuild and visually verify PDF

## Summary of Changes

Rebuilt 01_docs/operations/contracts/Contract_revier.pdf. Removed the extra generated Appendix 1 signature block, added the Appendix N 4 marker to the checklist page, and sorted the checklist sections so section 4 appears before sections 5-8. Rendered and visually checked the affected Appendix 1 and Appendix 4 pages.
