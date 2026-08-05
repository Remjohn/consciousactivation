# Observability — Primitive Alignment Editor

## Alignment Audit Receipt Specification

Every alignment run produces a `PrimitiveAlignmentReceipt` that is a complete,
deterministic audit trail. A later reviewer should never be stuck re-deriving
"why does this manifest cite PRM-HUM-009" from scratch — the receipt answers
every question.

### Required Receipt Fields

| Field                         | Type              | Description                                                    |
|-------------------------------|-------------------|----------------------------------------------------------------|
| `receipt_id`                  | `string`          | Unique identifier for this alignment run.                      |
| `manifest_id`                 | `string`          | Input manifest identifier.                                     |
| `aligned_primitive_ids`       | `string[]`        | Final conflict-free tuple of `PRM-`/`EXP-` IDs.               |
| `candidate_selection_rationale` | `object[]`      | Why each primitive was selected, citing `core_move` match.     |
| `verified_yaml_checksums`     | `object[]`        | SHA256 verification audit for every loaded YAML snapshot.       |
| `dropped_conflict_pairs`      | `object[]`        | Candidates dropped via `conflicts_with` resolution.            |
| `prose_changes_applied`       | `object[]`        | Exact diff of `hidden_pressure`, `stance`, and `wrong_reading_locks_meaning` changes. |
| `structural_locks_preserved`  | `string[]`        | Spatial locks in `wrong_reading_locks` left untouched.         |
| `ambiguous_locks_flagged`     | `object[]`        | Locks flagged for human review instead of silently reclassified. |
| `outcome`                     | `enum`            | `PASS`, `FAIL`, or `PASS_WITH_REVIEW_REQUIRED`.                |

### Outcome Semantics

- **`PASS`** — All primitives verified, no conflicts, no ambiguous locks. Aligned manifest is ready for downstream use.
- **`PASS_WITH_REVIEW_REQUIRED`** — Alignment succeeded, but one or more locks were flagged as ambiguous between spatial and meaning-plane categories. A human reviewer must classify them before the manifest is considered fully aligned.
- **`FAIL`** — Checksum mismatch, unresolved conflict, unknown primitive ID, or out-of-scope mutation detected. No aligned manifest is produced.

### Checksum Verification Entry Schema

```json
{
  "primitive_id": "PRM-HUM-009",
  "snapshot_path": "sources/cmf_primitive_registry_snapshot/meaning_plane/_golden/PRM-HUM-009.yaml",
  "expected_sha256": "f4a5c42c74be88cd3c8d1dfaf4de1cf1a99829ce12dcfb2edfd848f7620cfd9a",
  "computed_sha256": "f4a5c42c74be88cd3c8d1dfaf4de1cf1a99829ce12dcfb2edfd848f7620cfd9a",
  "verified": true
}
```

### Prose Change Entry Schema

```json
{
  "field_name": "hidden_pressure",
  "original_prose": "The jealousy between Kinshasa and Lagos fashion creates...",
  "aligned_prose": "PRM-HUM-009 (Reference Funny Filter): The reference specimens deploy shared cultural references that make the audience recognize themselves, creating pressure through complicit recognition rather than explicit confrontation."
}
```
