# doc_008 work_on_site extraction review

Дата: 2026-06-22

Статус: draft extraction run. Canonical promotion не выполнялся.

Run:

- `run_20260622_doc008_work_on_site_v1`
- source: `doc_008 / Работа на объекте 2024 ред1_7.docx`
- included chunks: `doc_008_chunk_0002` - `doc_008_chunk_0006`
- excluded chunk: `doc_008_chunk_0001`, because it is only the document title

## Validation

Collect result:

- queue chunks: 5
- parsed chunk results: 5
- valid statements: 66
- extraction errors: 0
- coverage warnings: 0
- promoted: false

Statement distribution:

| Dimension | Counts |
|:---|:---|
| by chunk | `0002`: 33, `0003`: 1, `0004`: 16, `0005`: 1, `0006`: 15 |
| by risk | `safety_critical`: 39, `important`: 25, `ordinary`: 2 |
| by review status | `review_required`: 39, `extracted`: 27 |
| by type | `instruction_step`: 28, `requirement`: 16, `process_step`: 11, `checklist_item`: 6, `reporting_requirement`: 4, `prohibition`: 1 |

## Cluster Recommendation

`C010` is already occupied by `qualification_levels` after `doc_010`.

Recommended future canonical cluster:

- `C011 / work_on_site`
- title: `Работа на объекте и распределение ролей в паре`
- source file: `Работа на объекте 2024 ред1_7.docx`
- primary future editorial output: `05_work_on_site.md`

## Main Value Of doc_008

The new value is role/action distribution on site:

- first number vs trainee;
- first number vs second number;
- 1st rank and 2nd rank pair behavior;
- trainee restrictions;
- supervision and control rules;
- self-distribution of work by agreement;
- client handover steps as part of work-on-site flow.

The draft intentionally keeps role-specific statements even when the underlying technical action overlaps with `C009 / installation_process` or `C010 / qualification_levels`.

## Updated Overlap After doc_010

### Strong `related_to` candidates

| doc_008 draft area | canonical target | rationale |
|:---|:---|:---|
| trainee works only by observing / under first-number control | `doc_010_chunk_0001_stmt_001`, `doc_010_chunk_0001_stmt_023` | `doc_010` defines qualification/duty boundary; `doc_008` defines on-site behavior. |
| first number role in pair | `doc_010_chunk_0003_stmt_001`, `doc_010_chunk_0003_stmt_002` | `doc_010` says 1st rank is first number and responsible; `doc_008` gives action matrix. |
| first number teaches trainee | `doc_010_chunk_0003_stmt_004` | `doc_010` states ability to teach; `doc_008` shows teaching AKB/balancer checks on site. |
| trainee assembles AKB / balancer-related work | `doc_010_chunk_0001_stmt_010` | `doc_010` is qualification criterion; `doc_008` is supervised work allocation. |
| first/second number report and photo/video handling | `doc_010_chunk_0002_stmt_019`, `doc_006_chunk_0006_stmt_001`, `doc_006_chunk_0006_stmt_002` | reporting/photo layer overlaps, but role assignment is new. |
| payment on site | `doc_010_chunk_0002_stmt_020`, `doc_004_chunk_0002_stmt_007` | payment ability/process overlaps; `doc_008` lists it in closeout. |

### Existing non-doc_010 overlaps

| doc_008 draft area | canonical target | relation |
|:---|:---|:---|
| inspecting installation site | `doc_004_chunk_0001_stmt_008` | `related_to` |
| agreeing changes with customer | `doc_015_chunk_0004_stmt_002` | `related_to` |
| installing inverter and bypass board | `doc_015_chunk_0005_stmt_002` | `related_to` |
| cable route to customer board | `doc_015_chunk_0005_stmt_003`, `doc_015_chunk_0016_stmt_003` | `related_to` |
| AKB on rack | `doc_015_chunk_0014_stmt_001`, `doc_013_chunk_0022_stmt_001` | `related_to` |
| checking AKB group correctness | `doc_015_chunk_0019_stmt_001` | `related_to` |
| inverter settings photo/video | `doc_006_chunk_0006_stmt_001`, `doc_006_chunk_0006_stmt_002` | likely `related_to`; duplicate only if role context is removed |
| outage simulation and reserve group check | `doc_015_chunk_0007_stmt_003`, `doc_015_chunk_0007_stmt_004`, `doc_015_chunk_0008_stmt_002` | `related_to` |
| cleanup, documents, payment, written report | `doc_004_chunk_0002_stmt_003`, `doc_004_chunk_0002_stmt_005`, `doc_004_chunk_0002_stmt_007`, `doc_004_chunk_0002_stmt_012`, `doc_004_chunk_0002_stmt_013` | `related_to` / possible duplicate for generic closeout steps |

## Promotion Guidance

Before canonical promotion:

1. Keep `doc_008` in a new `C011 / work_on_site` cluster.
2. Do not merge it into `C010`; `C010` is qualification criteria, while `C011` is on-site work distribution.
3. Consider trimming exact repeated closeout statements if canonical layer should avoid repeated generic process steps.
4. Keep role-bearing duplicates if they add who performs or supervises the action.
5. Create relation rows for the overlaps above, especially with `C010`, `C009`, `C004`, and `C002`.
6. Keep all `safety_critical` rows as `review_required`.
7. Do not create image links; `doc_008` has no approved related images.

## Review Risks

- The source inventory says the 2024 version requires актуальность review.
- Several statements define permission boundaries for trainee/second number work. These should be reviewed before becoming instructional material.
- The table extraction preserves role context through `scope` and statement wording, but source quotes are often cell-level snippets; reviewer should check role context against the original table before promotion.
