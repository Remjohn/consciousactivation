PRAGMA foreign_keys = ON;

-- Phase 5 adds semantic object types to the existing immutable air_objects and
-- air_object_edges stores. The schema remains intentionally generic, while these
-- indexes support the new production-compiler query paths.
CREATE INDEX IF NOT EXISTS idx_air_objects_type_current_revision
ON air_objects(object_type, is_current, revision);

CREATE INDEX IF NOT EXISTS idx_air_edges_target_relation
ON air_object_edges(target_object_id, relation_type);
