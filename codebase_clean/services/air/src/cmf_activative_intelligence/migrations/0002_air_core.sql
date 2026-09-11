PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS air_product_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    applied_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS air_objects (
    object_id TEXT NOT NULL,
    revision INTEGER NOT NULL CHECK (revision >= 1),
    object_type TEXT NOT NULL,
    semantic_version TEXT NOT NULL,
    canonical_sha256 TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    epistemic_state TEXT,
    lifecycle_state TEXT,
    authority_state TEXT NOT NULL,
    is_current INTEGER NOT NULL CHECK (is_current IN (0, 1)),
    created_at_utc TEXT NOT NULL,
    command_id TEXT NOT NULL,
    supersedes_object_id TEXT,
    supersedes_revision INTEGER,
    PRIMARY KEY (object_id, revision),
    UNIQUE (object_id, canonical_sha256),
    FOREIGN KEY (command_id) REFERENCES commands(command_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_air_one_current_object
ON air_objects(object_id)
WHERE is_current = 1;

CREATE INDEX IF NOT EXISTS idx_air_object_type_current
ON air_objects(object_type, is_current);

CREATE TABLE IF NOT EXISTS air_object_edges (
    source_object_id TEXT NOT NULL,
    source_revision INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    target_object_id TEXT NOT NULL,
    target_revision INTEGER,
    evidence_json TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    PRIMARY KEY (
        source_object_id,
        source_revision,
        relation_type,
        target_object_id,
        target_revision
    ),
    FOREIGN KEY (source_object_id, source_revision)
        REFERENCES air_objects(object_id, revision)
);

CREATE TABLE IF NOT EXISTS air_registry_snapshots (
    registry_id TEXT NOT NULL,
    registry_version TEXT NOT NULL,
    registry_kind TEXT NOT NULL,
    source_manifest_sha256 TEXT NOT NULL,
    item_count INTEGER NOT NULL CHECK (item_count >= 0),
    imported_at_utc TEXT NOT NULL,
    PRIMARY KEY (registry_id, registry_version)
);

CREATE TABLE IF NOT EXISTS air_primitives (
    primitive_id TEXT NOT NULL,
    canonical_name TEXT NOT NULL,
    plane TEXT NOT NULL,
    family TEXT NOT NULL,
    core_move TEXT NOT NULL,
    source_relative_path TEXT NOT NULL,
    source_sha256 TEXT NOT NULL,
    active_feature_ids_json TEXT NOT NULL,
    synergizes_with_json TEXT NOT NULL,
    conflicts_with_json TEXT NOT NULL,
    suppression_conditions_json TEXT NOT NULL,
    misuse_modes_json TEXT NOT NULL,
    source_text TEXT NOT NULL,
    registry_version TEXT NOT NULL,
    PRIMARY KEY (primitive_id, source_sha256)
);

CREATE INDEX IF NOT EXISTS idx_air_primitive_family
ON air_primitives(family, plane);

CREATE INDEX IF NOT EXISTS idx_air_primitive_id
ON air_primitives(primitive_id);

CREATE TABLE IF NOT EXISTS air_archetypes (
    archetype_prompt_id TEXT PRIMARY KEY,
    family TEXT NOT NULL,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    source_relative_path TEXT NOT NULL,
    source_sha256 TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    source_text TEXT NOT NULL,
    registry_version TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_air_archetype_family
ON air_archetypes(family, evidence_status);

CREATE TABLE IF NOT EXISTS air_failure_layers (
    layer_id TEXT PRIMARY KEY,
    owner_product TEXT NOT NULL,
    local_repair_authorized INTEGER NOT NULL
        CHECK (local_repair_authorized IN (0, 1))
);
