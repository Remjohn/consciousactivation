# Failure Taxonomy — Primitive Alignment Editor

## Error Codes

| Error Code                    | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `INVALID_MANIFEST_INPUT`      | Input JSON failed basic OperatorManifest schema parsing.                    |
| `REGISTRY_LOAD_FAILED`        | Could not open or read `PRIMITIVE_INVENTORY.csv`.                           |
| `UNKNOWN_PRIMITIVE_ID`        | Manifest cited a primitive ID not present in the 243-entry inventory.       |
| `SNAPSHOT_NOT_FOUND`          | Snapshot YAML file specified by CSV `snapshot_path` was missing.            |
| `SHA256_MISMATCH`             | Loaded YAML snapshot byte digest did not match CSV `sha256` column.         |
| `CONFLICTING_PRIMITIVE_PAIR`  | Selected primitive pair has unresolved `conflicts_with` declaration.        |
| `NOUN_LEAKAGE_DETECTED`       | Aligned prose still contains un-stripped specimen proper nouns.             |
| `OUT_OF_SCOPE_MUTATION`       | Skill attempted to mutate immutable `task.*` or spatial lock fields.        |
