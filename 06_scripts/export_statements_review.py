#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: export_statements_review.py <statements_jsonl> <review_md>", file=sys.stderr)
        return 1

    source_path = Path(argv[1]).resolve()
    output_path = Path(argv[2]).resolve()
    rows = [json.loads(line) for line in source_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    lines: list[str] = [
        "# Ревью утверждений batch 001",
        "",
        f"Источник: `{source_path}`",
        "",
        "## Как проводить ревью",
        "",
        "По каждому утверждению выбери одно решение:",
        "",
        "- [ ] OK - утверждение точное, атомарное, полезное.",
        "- [ ] Исправить - смысл верный, но нужна правка формулировки, типа, роли, темы, риска или цитаты.",
        "- [ ] Удалить - утверждение лишнее, слишком мелкое, фантазийное или не нужно в базе знаний.",
        "",
        "В поле `Комментарий ревью` можно написать, что именно исправить.",
        "",
        "## Список утверждений",
    ]

    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                "",
                f"### {index}. `{row['statement_id']}`",
                "",
                "- [ ] OK",
                "- [ ] Исправить",
                "- [ ] Удалить",
                "",
                f"**Утверждение:** {row['statement']}",
                "",
                f"**Цитата из источника:** {row['source_quote']}",
                "",
                f"**Источник:** `{row['source_file']}`",
                f"**Chunk:** `{row['source_chunk_id']}`",
                f"**Раздел:** {' > '.join(row['section_path'])}",
                "",
                f"**Тип:** `{row['statement_type']}`",
                f"**Тема:** `{row['topic']}`",
                f"**Роли:** `{', '.join(row['roles'])}`",
                f"**Риск:** `{row['risk_level']}`",
                f"**Статус:** `{row['review_status']}`",
                f"**Изображения:** `{', '.join(row['related_image_ids'])}`"
                if row.get("related_image_ids")
                else "**Изображения:** нет",
                "",
                "**Комментарий ревью:** ",
                "",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} statements to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
