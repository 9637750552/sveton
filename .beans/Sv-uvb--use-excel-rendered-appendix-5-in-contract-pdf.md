---
# Sv-uvb
title: Use Excel-rendered Appendix 5 in contract PDF
status: completed
type: task
priority: normal
created_at: 2026-07-22T02:03:19Z
updated_at: 2026-07-22T02:08:59Z
---

Update Contract_revier.pdf so Appendix 3 has spacing before signatures and Appendix 5 is inserted from the Excel sheet as an exact visual copy.\n\n- [x] Export Appendix 5 sheet from Excel\n- [x] Update PDF builder to use the Excel-rendered Appendix 5\n- [x] Add spacing before Appendix 3 signatures\n- [x] Rebuild and visually verify the PDF

## Summary of Changes\n\n- Rebuilt Contract_revier.pdf.\n- Added spacing before the Appendix 3 signature row.\n- Replaced the generated Appendix 5 page with the Excel-rendered sheet from appendix_2_object_inspection_request.xlsx.\n- Verified the resulting PDF opens through pypdf and renders pages 8-10 through Poppler.
