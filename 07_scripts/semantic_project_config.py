from __future__ import annotations

from pathlib import Path


DEFAULT_CONFIG_PATH = Path("semantic_project.yml")

DEFAULT_CONFIG = {
    "project_id": "sveton",
    "corpus_id": "electricians_knowledge_base",
    "source_inventory": "00_input/documents/electricians_knowledge_base/inventory.md",
    "raw_sources": "00_input/documents/electricians_knowledge_base/raw",
    "extracted_texts": "00_input/documents/electricians_knowledge_base/extracted",
    "chunks": "00_input/documents/electricians_knowledge_base/chunks/source_chunks.jsonl",
    "chunks_summary": "00_input/documents/electricians_knowledge_base/chunks/summary.md",
    "statements_dir": "00_input/documents/electricians_knowledge_base/statements",
    "statements": "00_input/documents/electricians_knowledge_base/statements/atomic_statements.jsonl",
    "prompt": "00_input/documents/electricians_knowledge_base/statements/atomic_extraction_prompt.md",
    "extraction_errors": "00_input/documents/electricians_knowledge_base/statements/extraction_errors.jsonl",
    "coverage_warnings": "00_input/documents/electricians_knowledge_base/statements/coverage_warnings.jsonl",
    "coverage_report": "00_input/documents/electricians_knowledge_base/statements/source_coverage_report.md",
    "coverage_overrides": "00_input/documents/electricians_knowledge_base/statements/source_coverage_overrides.jsonl",
    "images_raw": "00_input/documents/electricians_knowledge_base/images/raw",
    "images_normalized": "00_input/documents/electricians_knowledge_base/images/normalized",
    "images_inventory": "00_input/documents/electricians_knowledge_base/images/inventory.csv",
}


def parse_flat_yaml(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise ValueError(f"Invalid config line {line_no}: {line}")
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if not key:
            raise ValueError(f"Invalid empty config key on line {line_no}")
        values[key] = value
    return values


def load_project_config(project_root: Path, config_path: str | Path | None = None) -> dict[str, str]:
    config = dict(DEFAULT_CONFIG)
    path = project_root / (Path(config_path) if config_path else DEFAULT_CONFIG_PATH)
    if path.exists():
        config.update(parse_flat_yaml(path.read_text(encoding="utf-8")))
    return config


def config_path(project_root: Path, config: dict[str, str], key: str) -> Path:
    value = config[key]
    path = Path(value)
    if path.is_absolute():
        return path
    return project_root / path
