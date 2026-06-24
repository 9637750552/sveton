# Batch 009: doc_009 UZO installation semantic extraction

Дата: 2026-06-23

Источник: `doc_009 / Установка УЗО при монтаже.docx`

## Scope

- chunk: `doc_009_chunk_0001`
- extracted text: `00_input/documents/electricians_knowledge_base/extracted/Установка УЗО при монтаже.md`
- images: none

## Output

- Added `12` atomic statements: `doc_009_chunk_0001_stmt_001` through `doc_009_chunk_0001_stmt_012`.
- Added canonical cluster `C012 / uzo_installation`.
- Added `14` statement relations: `rel_0062` through `rel_0075`.
- Added `1` source coverage row for `doc_009_chunk_0001`.
- Added `3` coverage/review warnings for ambiguous source reference, possible tension with existing UZO statement, and missing visual evidence.
- Added no `statement_images.jsonl` rows because `doc_009` contains no images or media refs.
- Added no extraction errors.

## Statement Groups

1. Safety scenario: ИБП between UZO and reserve-group breakers, UZO trips on leakage, reserve line remains powered from UPS.
2. Existing UZO handling: reserve breakers are distributed to one or several UZO and those UZO are connected after UPS.
3. Additional UZO: UZO from ZIP is installed and commutated by reference to point 1.
4. Trip-current requirement: installed UZO must match the trip current of the previous UZO for the reserve-group breakers.
5. Placement options: customer board, Sveton bypass board, or a two-module ZIP board near the customer board.
6. Approval boundary: additional UZO installation requires contacting the head of installation-service or substitute.

## Review Flags

All `doc_009` statements are `risk_level=safety_critical` and `review_status=review_required`.

Do not use the extracted statements as final wiring instructions until expert technical review is complete.
