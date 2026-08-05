# Observability — Primitive Alignment Editor

## Telemetry & Alignment Receipts

Every alignment run produces a `PrimitiveAlignmentReceipt` containing:
- `receipt_id`: Unique identifier for this alignment run.
- `manifest_id`: Input manifest identifier.
- `aligned_primitive_ids`: Conflict-checked tuple of `PRM-`/`EXP-` IDs populated in `activative_input.aligned_primitive_ids`.
- `verified_yaml_checksums`: Audit list of loaded snapshot paths and verified SHA256 digests.
- `dropped_conflict_pairs`: List of candidate primitive pairs resolved via `conflicts_with` rules.
- `prose_changes_applied`: Exact diff of modified `hidden_pressure`, `stance`, and `wrong_reading_locks_meaning` fields.
- `outcome`: `PASS` or `FAIL`.
