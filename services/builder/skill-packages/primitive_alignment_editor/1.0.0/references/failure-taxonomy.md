# Failure Taxonomy — Primitive Alignment Editor

## Error Codes

| Error Code                    | Severity | Description                                                                 | Recovery                                      |
|-------------------------------|----------|-----------------------------------------------------------------------------|-----------------------------------------------|
| `INVALID_MANIFEST_INPUT`      | FATAL    | Input JSON failed basic schema parsing or `mode` is not `activative`.       | Fix manifest and re-submit.                   |
| `REGISTRY_LOAD_FAILED`        | FATAL    | Could not open or read `PRIMITIVE_INVENTORY.csv`.                           | Verify file exists at governed path.           |
| `UNKNOWN_PRIMITIVE_ID`        | FATAL    | Manifest cited a primitive ID not present in the 243-entry inventory.       | Remove unknown ID or add it to the registry.   |
| `SNAPSHOT_NOT_FOUND`          | FATAL    | Snapshot YAML at CSV `snapshot_path` was missing from disk.                 | Verify snapshot exists at the CSV path.        |
| `SHA256_MISMATCH`             | FATAL    | Loaded YAML byte digest did not match CSV `sha256` column.                 | Regenerate registry or restore YAML snapshot.  |
| `CONFLICTING_PRIMITIVE_PAIR`  | WARN     | Selected candidate pair has unresolved `conflicts_with` declaration.        | Auto-resolved by dropping lower-fit candidate. |
| `NOUN_LEAKAGE_DETECTED`       | WARN     | Aligned prose still contains un-stripped specimen proper nouns.             | Re-run noun-stripping pass.                   |
| `OUT_OF_SCOPE_MUTATION`       | FATAL    | Skill attempted to mutate immutable `task.*`, spatial locks, or lineage refs. | Roll back mutation and re-run.               |
| `AMBIGUOUS_LOCK_FLAGGED`      | INFO     | Lock could not be classified as spatial or meaning-plane.                   | Flagged for human review. Outcome set to `PASS_WITH_REVIEW_REQUIRED`. |

## Severity Levels

- **FATAL:** Halt execution immediately. Do not produce an aligned manifest. Emit receipt with `outcome: FAIL`.
- **WARN:** Log the issue and auto-resolve where possible. Continue execution. Emit receipt with details.
- **INFO:** Log for auditability. Does not affect execution flow. May upgrade receipt outcome to `PASS_WITH_REVIEW_REQUIRED`.
