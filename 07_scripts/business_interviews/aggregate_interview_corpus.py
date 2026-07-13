#!/usr/bin/env python3
"""Aggregate per-interview artifacts into corpus-level JSONL inputs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INTERVIEW_IDS = [f"interview_{index:03d}" for index in range(1, 8)]

INPUTS = {
    "chunks": (
        "00_input/interviews/chunks/{interview_id}_chunks.jsonl",
        "00_input/interviews/chunks/interview_corpus_chunks.jsonl",
    ),
    "claims": (
        "00_input/interviews/statements/{interview_id}_claims.jsonl",
        "00_input/interviews/statements/interview_corpus_claims.jsonl",
    ),
    "extraction_results": (
        "00_input/interviews/statements/{interview_id}_extraction_results.jsonl",
        "00_input/interviews/statements/interview_corpus_extraction_results.jsonl",
    ),
}


def aggregate(pattern: str, output: str) -> int:
    rows: list[str] = []
    for interview_id in INTERVIEW_IDS:
        path = ROOT / pattern.format(interview_id=interview_id)
        if not path.exists():
            raise FileNotFoundError(path)
        rows.extend(line for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

    output_path = ROOT / output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def main() -> int:
    for name, (pattern, output) in INPUTS.items():
        count = aggregate(pattern, output)
        print(f"{name}={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
