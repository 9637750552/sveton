CREATE SCHEMA IF NOT EXISTS kb;

CREATE TABLE IF NOT EXISTS kb.schema_migrations (
    version text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kb.projects (
    id bigserial PRIMARY KEY,
    project_key text NOT NULL UNIQUE,
    name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kb.corpora (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_key text NOT NULL,
    name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_key)
);

CREATE TABLE IF NOT EXISTS kb.import_runs (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    import_run_key text NOT NULL,
    source_git_commit text,
    engine_git_commit text,
    schema_version text NOT NULL,
    config_path text,
    source_summary jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_id, import_run_key)
);

CREATE TABLE IF NOT EXISTS kb.sources (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    source_document_id text NOT NULL,
    source_file text NOT NULL,
    source_format text,
    document_type text,
    topic text,
    roles text[] NOT NULL DEFAULT '{}'::text[],
    status text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_id, source_document_id),
    UNIQUE (project_id, corpus_id, source_file)
);

CREATE TABLE IF NOT EXISTS kb.chunks (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    source_id bigint REFERENCES kb.sources(id) ON DELETE SET NULL,
    chunk_id text NOT NULL,
    source_document_id text NOT NULL,
    source_file text NOT NULL,
    topic text,
    roles text[] NOT NULL DEFAULT '{}'::text[],
    section_path text[] NOT NULL DEFAULT '{}'::text[],
    chunk_text text NOT NULL,
    related_image_ids text[] NOT NULL DEFAULT '{}'::text[],
    excluded_image_ids text[] NOT NULL DEFAULT '{}'::text[],
    review_image_ids text[] NOT NULL DEFAULT '{}'::text[],
    previous_chunk_id text,
    next_chunk_id text,
    previous_context text,
    next_context text,
    needs_review boolean NOT NULL DEFAULT false,
    review_reasons text[] NOT NULL DEFAULT '{}'::text[],
    raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_id, chunk_id)
);

CREATE TABLE IF NOT EXISTS kb.images (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    image_id text NOT NULL,
    source_file text,
    file_name text,
    media_ref text,
    image_type text,
    topic text,
    roles text[] NOT NULL DEFAULT '{}'::text[],
    status text,
    width integer,
    height integer,
    caption text,
    source_anchor text,
    nearby_text text,
    linking_bucket text,
    raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_id, image_id)
);

CREATE TABLE IF NOT EXISTS kb.statements (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    source_id bigint REFERENCES kb.sources(id) ON DELETE SET NULL,
    chunk_db_id bigint REFERENCES kb.chunks(id) ON DELETE SET NULL,
    statement_id text NOT NULL,
    statement_text text NOT NULL,
    statement_type text NOT NULL,
    topic text,
    roles text[] NOT NULL DEFAULT '{}'::text[],
    source_document_id text NOT NULL,
    source_file text NOT NULL,
    source_chunk_id text NOT NULL,
    section_path text[] NOT NULL DEFAULT '{}'::text[],
    source_quote text NOT NULL,
    source_quote_is_exact boolean NOT NULL,
    related_image_ids text[] NOT NULL DEFAULT '{}'::text[],
    visual_review_required boolean NOT NULL DEFAULT false,
    risk_level text NOT NULL CHECK (risk_level IN ('ordinary', 'important', 'safety_critical')),
    confidence text NOT NULL CHECK (confidence IN ('high', 'medium', 'low')),
    review_status text NOT NULL CHECK (review_status IN ('extracted', 'review_required', 'rejected')),
    scope text,
    condition text,
    action text,
    object text,
    normalized_terms text[] NOT NULL DEFAULT '{}'::text[],
    extraction_notes text,
    downstream_status text NOT NULL DEFAULT 'draft',
    raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_id, statement_id)
);

CREATE TABLE IF NOT EXISTS kb.clusters (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    cluster_id text NOT NULL,
    title text,
    topic text,
    summary text,
    raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_id, cluster_id)
);

CREATE TABLE IF NOT EXISTS kb.statement_clusters (
    statement_id bigint NOT NULL REFERENCES kb.statements(id) ON DELETE CASCADE,
    cluster_id bigint NOT NULL REFERENCES kb.clusters(id) ON DELETE CASCADE,
    relation_type text NOT NULL DEFAULT 'member',
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (statement_id, cluster_id, relation_type)
);

CREATE TABLE IF NOT EXISTS kb.statement_relations (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    source_statement_id bigint NOT NULL REFERENCES kb.statements(id) ON DELETE CASCADE,
    target_statement_id bigint NOT NULL REFERENCES kb.statements(id) ON DELETE CASCADE,
    relation_type text NOT NULL,
    confidence text,
    notes text,
    raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_statement_id, target_statement_id, relation_type)
);

CREATE TABLE IF NOT EXISTS kb.statement_images (
    statement_id bigint NOT NULL REFERENCES kb.statements(id) ON DELETE CASCADE,
    image_id bigint NOT NULL REFERENCES kb.images(id) ON DELETE CASCADE,
    link_type text NOT NULL DEFAULT 'illustrates',
    review_status text,
    notes text,
    raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (statement_id, image_id, link_type)
);

CREATE TABLE IF NOT EXISTS kb.review_tasks (
    id bigserial PRIMARY KEY,
    project_id bigint NOT NULL REFERENCES kb.projects(id) ON DELETE RESTRICT,
    corpus_id bigint NOT NULL REFERENCES kb.corpora(id) ON DELETE RESTRICT,
    statement_id bigint REFERENCES kb.statements(id) ON DELETE CASCADE,
    chunk_id bigint REFERENCES kb.chunks(id) ON DELETE CASCADE,
    task_type text NOT NULL,
    status text NOT NULL CHECK (status IN ('todo', 'in_review', 'blocked', 'approved', 'needs_rewrite', 'requires_manufacturer_docs', 'done')),
    priority text NOT NULL DEFAULT 'normal' CHECK (priority IN ('critical', 'high', 'normal', 'low', 'deferred')),
    reason text NOT NULL,
    assigned_to text,
    due_at timestamptz,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, corpus_id, statement_id, chunk_id, task_type, reason)
);

CREATE TABLE IF NOT EXISTS kb.review_decisions (
    id bigserial PRIMARY KEY,
    review_task_id bigint REFERENCES kb.review_tasks(id) ON DELETE SET NULL,
    statement_id bigint REFERENCES kb.statements(id) ON DELETE CASCADE,
    decision_action text NOT NULL,
    downstream_status text,
    reviewer text NOT NULL,
    review_comment text,
    proposed_statement_text text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kb.review_events (
    id bigserial PRIMARY KEY,
    review_task_id bigint REFERENCES kb.review_tasks(id) ON DELETE SET NULL,
    statement_id bigint REFERENCES kb.statements(id) ON DELETE SET NULL,
    event_type text NOT NULL,
    actor text,
    event_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kb.proposed_rewrites (
    id bigserial PRIMARY KEY,
    statement_id bigint NOT NULL REFERENCES kb.statements(id) ON DELETE CASCADE,
    proposed_statement_text text NOT NULL,
    proposer text NOT NULL,
    reason text,
    status text NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed', 'accepted', 'rejected', 'superseded')),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION kb.prevent_statement_immutable_update()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.statement_text IS DISTINCT FROM NEW.statement_text
        OR OLD.source_quote IS DISTINCT FROM NEW.source_quote
        OR OLD.source_chunk_id IS DISTINCT FROM NEW.source_chunk_id
        OR OLD.source_document_id IS DISTINCT FROM NEW.source_document_id
        OR OLD.source_file IS DISTINCT FROM NEW.source_file
    THEN
        RAISE EXCEPTION 'immutable extracted statement fields cannot be updated';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_prevent_statement_immutable_update ON kb.statements;
CREATE TRIGGER trg_prevent_statement_immutable_update
BEFORE UPDATE ON kb.statements
FOR EACH ROW
EXECUTE FUNCTION kb.prevent_statement_immutable_update();

CREATE OR REPLACE FUNCTION kb.prevent_update_delete()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'append-only table cannot be updated or deleted';
END;
$$;

DROP TRIGGER IF EXISTS trg_review_decisions_append_only_update ON kb.review_decisions;
DROP TRIGGER IF EXISTS trg_review_decisions_append_only_delete ON kb.review_decisions;
CREATE TRIGGER trg_review_decisions_append_only_update
BEFORE UPDATE ON kb.review_decisions
FOR EACH ROW
EXECUTE FUNCTION kb.prevent_update_delete();
CREATE TRIGGER trg_review_decisions_append_only_delete
BEFORE DELETE ON kb.review_decisions
FOR EACH ROW
EXECUTE FUNCTION kb.prevent_update_delete();

DROP TRIGGER IF EXISTS trg_review_events_append_only_update ON kb.review_events;
DROP TRIGGER IF EXISTS trg_review_events_append_only_delete ON kb.review_events;
CREATE TRIGGER trg_review_events_append_only_update
BEFORE UPDATE ON kb.review_events
FOR EACH ROW
EXECUTE FUNCTION kb.prevent_update_delete();
CREATE TRIGGER trg_review_events_append_only_delete
BEFORE DELETE ON kb.review_events
FOR EACH ROW
EXECUTE FUNCTION kb.prevent_update_delete();

CREATE INDEX IF NOT EXISTS idx_kb_chunks_project_corpus_source ON kb.chunks(project_id, corpus_id, source_document_id);
CREATE INDEX IF NOT EXISTS idx_kb_chunks_topic ON kb.chunks(project_id, corpus_id, topic);
CREATE INDEX IF NOT EXISTS idx_kb_statements_chunk ON kb.statements(project_id, corpus_id, source_chunk_id);
CREATE INDEX IF NOT EXISTS idx_kb_statements_topic ON kb.statements(project_id, corpus_id, topic);
CREATE INDEX IF NOT EXISTS idx_kb_statements_risk ON kb.statements(project_id, corpus_id, risk_level);
CREATE INDEX IF NOT EXISTS idx_kb_statements_review_status ON kb.statements(project_id, corpus_id, review_status);
CREATE INDEX IF NOT EXISTS idx_kb_statements_downstream_status ON kb.statements(project_id, corpus_id, downstream_status);
CREATE INDEX IF NOT EXISTS idx_kb_review_tasks_queue ON kb.review_tasks(project_id, corpus_id, status, priority, task_type);
CREATE INDEX IF NOT EXISTS idx_kb_review_tasks_statement ON kb.review_tasks(statement_id);
CREATE INDEX IF NOT EXISTS idx_kb_review_decisions_statement ON kb.review_decisions(statement_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_kb_review_events_statement ON kb.review_events(statement_id, created_at DESC);

INSERT INTO kb.schema_migrations(version)
VALUES ('001_create_kb_review_schema')
ON CONFLICT (version) DO NOTHING;
