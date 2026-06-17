from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path


PROJECT_KEY = "sveton"
CORPUS_KEY = "electricians_knowledge_base"


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def build_seed_sql(project_key: str, corpus_key: str) -> str:
    project = sql_literal(project_key)
    corpus = sql_literal(corpus_key)
    return f"""\\set ON_ERROR_STOP on
BEGIN;

WITH scope AS (
    SELECT p.id AS project_id, c.id AS corpus_id
    FROM kb.projects p
    JOIN kb.corpora c ON c.project_id = p.id
    WHERE p.project_key = {project}
      AND c.corpus_key = {corpus}
),
blocked AS (
    UPDATE kb.statements st
    SET downstream_status = 'blocked_for_instruction'
    FROM scope
    WHERE st.project_id = scope.project_id
      AND st.corpus_id = scope.corpus_id
      AND st.risk_level = 'safety_critical'
      AND st.review_status = 'review_required'
      AND st.downstream_status IS DISTINCT FROM 'blocked_for_instruction'
    RETURNING st.id
)
SELECT count(*) AS updated_blocked_for_instruction FROM blocked;

WITH scope AS (
    SELECT p.id AS project_id, c.id AS corpus_id
    FROM kb.projects p
    JOIN kb.corpora c ON c.project_id = p.id
    WHERE p.project_key = {project}
      AND c.corpus_key = {corpus}
),
candidate AS (
    SELECT
        st.project_id,
        st.corpus_id,
        st.id AS statement_id,
        st.chunk_db_id AS chunk_id,
        'statement_review_required'::text AS task_type,
        'todo'::text AS status,
        CASE
            WHEN st.risk_level = 'safety_critical' THEN 'critical'
            WHEN st.risk_level = 'important' THEN 'high'
            ELSE 'normal'
        END AS priority,
        'extraction_review_required'::text AS reason,
        jsonb_build_object(
            'seed_rule', 'review_status_review_required',
            'statement_id', st.statement_id,
            'risk_level', st.risk_level,
            'topic', st.topic,
            'source_file', st.source_file,
            'source_chunk_id', st.source_chunk_id
        ) AS metadata
    FROM kb.statements st
    JOIN scope ON scope.project_id = st.project_id AND scope.corpus_id = st.corpus_id
    WHERE st.review_status = 'review_required'
)
INSERT INTO kb.review_tasks(project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata)
SELECT project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata
FROM candidate c
WHERE NOT EXISTS (
    SELECT 1
    FROM kb.review_tasks rt
    WHERE rt.project_id = c.project_id
      AND rt.corpus_id = c.corpus_id
      AND rt.statement_id = c.statement_id
      AND rt.chunk_id = c.chunk_id
      AND rt.task_type = c.task_type
      AND rt.reason = c.reason
);

WITH scope AS (
    SELECT p.id AS project_id, c.id AS corpus_id
    FROM kb.projects p
    JOIN kb.corpora c ON c.project_id = p.id
    WHERE p.project_key = {project}
      AND c.corpus_key = {corpus}
),
candidate AS (
    SELECT
        st.project_id,
        st.corpus_id,
        st.id AS statement_id,
        st.chunk_db_id AS chunk_id,
        'technical_safety_review'::text AS task_type,
        'todo'::text AS status,
        'critical'::text AS priority,
        'safety_critical_statement'::text AS reason,
        jsonb_build_object(
            'seed_rule', 'risk_level_safety_critical',
            'statement_id', st.statement_id,
            'topic', st.topic,
            'source_file', st.source_file,
            'source_chunk_id', st.source_chunk_id
        ) AS metadata
    FROM kb.statements st
    JOIN scope ON scope.project_id = st.project_id AND scope.corpus_id = st.corpus_id
    WHERE st.risk_level = 'safety_critical'
)
INSERT INTO kb.review_tasks(project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata)
SELECT project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata
FROM candidate c
WHERE NOT EXISTS (
    SELECT 1
    FROM kb.review_tasks rt
    WHERE rt.project_id = c.project_id
      AND rt.corpus_id = c.corpus_id
      AND rt.statement_id = c.statement_id
      AND rt.chunk_id = c.chunk_id
      AND rt.task_type = c.task_type
      AND rt.reason = c.reason
);

WITH scope AS (
    SELECT p.id AS project_id, c.id AS corpus_id
    FROM kb.projects p
    JOIN kb.corpora c ON c.project_id = p.id
    WHERE p.project_key = {project}
      AND c.corpus_key = {corpus}
),
candidate AS (
    SELECT
        st.project_id,
        st.corpus_id,
        st.id AS statement_id,
        st.chunk_db_id AS chunk_id,
        'instruction_block_review'::text AS task_type,
        'todo'::text AS status,
        'critical'::text AS priority,
        'blocked_for_instruction_until_expert_review'::text AS reason,
        jsonb_build_object(
            'seed_rule', 'downstream_blocked_for_instruction',
            'statement_id', st.statement_id,
            'topic', st.topic,
            'source_file', st.source_file,
            'source_chunk_id', st.source_chunk_id
        ) AS metadata
    FROM kb.statements st
    JOIN scope ON scope.project_id = st.project_id AND scope.corpus_id = st.corpus_id
    WHERE st.downstream_status = 'blocked_for_instruction'
)
INSERT INTO kb.review_tasks(project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata)
SELECT project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata
FROM candidate c
WHERE NOT EXISTS (
    SELECT 1
    FROM kb.review_tasks rt
    WHERE rt.project_id = c.project_id
      AND rt.corpus_id = c.corpus_id
      AND rt.statement_id = c.statement_id
      AND rt.chunk_id = c.chunk_id
      AND rt.task_type = c.task_type
      AND rt.reason = c.reason
);

WITH scope AS (
    SELECT p.id AS project_id, c.id AS corpus_id
    FROM kb.projects p
    JOIN kb.corpora c ON c.project_id = p.id
    WHERE p.project_key = {project}
      AND c.corpus_key = {corpus}
),
candidate AS (
    SELECT
        st.project_id,
        st.corpus_id,
        st.id AS statement_id,
        st.chunk_db_id AS chunk_id,
        'visual_evidence_review'::text AS task_type,
        'todo'::text AS status,
        CASE WHEN st.risk_level = 'safety_critical' THEN 'critical' ELSE 'high' END AS priority,
        'visual_evidence_review_required'::text AS reason,
        jsonb_build_object(
            'seed_rule', 'visual_review_required',
            'statement_id', st.statement_id,
            'risk_level', st.risk_level,
            'topic', st.topic,
            'related_image_ids', st.related_image_ids,
            'source_file', st.source_file,
            'source_chunk_id', st.source_chunk_id
        ) AS metadata
    FROM kb.statements st
    JOIN scope ON scope.project_id = st.project_id AND scope.corpus_id = st.corpus_id
    WHERE st.visual_review_required
)
INSERT INTO kb.review_tasks(project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata)
SELECT project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata
FROM candidate c
WHERE NOT EXISTS (
    SELECT 1
    FROM kb.review_tasks rt
    WHERE rt.project_id = c.project_id
      AND rt.corpus_id = c.corpus_id
      AND rt.statement_id = c.statement_id
      AND rt.chunk_id = c.chunk_id
      AND rt.task_type = c.task_type
      AND rt.reason = c.reason
);

WITH scope AS (
    SELECT p.id AS project_id, c.id AS corpus_id
    FROM kb.projects p
    JOIN kb.corpora c ON c.project_id = p.id
    WHERE p.project_key = {project}
      AND c.corpus_key = {corpus}
),
candidate AS (
    SELECT
        ch.project_id,
        ch.corpus_id,
        NULL::bigint AS statement_id,
        ch.id AS chunk_id,
        'source_chunk_review'::text AS task_type,
        'todo'::text AS status,
        'high'::text AS priority,
        'source_chunk_needs_review'::text AS reason,
        jsonb_build_object(
            'seed_rule', 'chunk_needs_review',
            'chunk_id', ch.chunk_id,
            'source_file', ch.source_file,
            'review_reasons', ch.review_reasons
        ) AS metadata
    FROM kb.chunks ch
    JOIN scope ON scope.project_id = ch.project_id AND scope.corpus_id = ch.corpus_id
    WHERE ch.needs_review
)
INSERT INTO kb.review_tasks(project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata)
SELECT project_id, corpus_id, statement_id, chunk_id, task_type, status, priority, reason, metadata
FROM candidate c
WHERE NOT EXISTS (
    SELECT 1
    FROM kb.review_tasks rt
    WHERE rt.project_id = c.project_id
      AND rt.corpus_id = c.corpus_id
      AND rt.statement_id IS NULL
      AND rt.chunk_id = c.chunk_id
      AND rt.task_type = c.task_type
      AND rt.reason = c.reason
);

COMMIT;
"""


def apply_sql(sql_text: str, command: str) -> None:
    args = shlex.split(command)
    if not args:
        raise ValueError("empty apply command")
    result = subprocess.run(args, input=sql_text, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"apply command failed with exit code {result.returncode}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed Postgres review tasks for the Sveton KB review workflow.")
    parser.add_argument("--project-key", default=PROJECT_KEY)
    parser.add_argument("--corpus-key", default=CORPUS_KEY)
    parser.add_argument("--out", default="99_tmp/kb_review_tasks/seed_review_tasks.sql")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--apply-command", default=os.environ.get("SVETON_KB_PSQL_COMMAND"))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    sql_text = build_seed_sql(args.project_key, args.corpus_key)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(sql_text, encoding="utf-8")
    print(f"SQL: {out_path}")
    if args.apply:
        if not args.apply_command:
            print("--apply requires --apply-command or SVETON_KB_PSQL_COMMAND.", file=sys.stderr)
            return 2
        apply_sql(sql_text, args.apply_command)
        print("Seeded review tasks successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
