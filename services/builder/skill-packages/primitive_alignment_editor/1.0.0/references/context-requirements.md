# Context Requirements — Primitive Alignment Editor

## Context Classification Matrix

| Context Element               | Requirement Status    | Description                                            |
|-------------------------------|-----------------------|--------------------------------------------------------|
| `operator_manifest`           | REQUIRED              | Builder-parsed operator manifest JSON                  |
| `PRIMITIVE_INVENTORY.csv`     | REQUIRED              | 243-row registry CSV from `services/air`               |
| `snapshot_yaml_files`         | REQUIRED              | YAML snapshot files loaded per primitive               |
| `wrong_reading_locks`         | READ_ONLY             | Spatial locks (never mutated by this skill)            |
| `task.*` fields               | FORBIDDEN_MUTATION    | Task goals, contracts, and refs (must not be mutated)  |
| `semantic_lineage_refs`       | FORBIDDEN_MUTATION    | Immutable lineage pointers (must not be mutated)       |
| `raw_image_bytes`             | FORBIDDEN             | Skill handles psychological prose, not image assets    |
| `provider_credentials`        | FORBIDDEN             | Skill is provider-neutral                              |
