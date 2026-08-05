# Execution Instructions — Primitive Alignment Editor

## Execution Algorithm

### Step 1: Ingest Operator Manifest & Validate Pre-Conditions
1. Read the input operator manifest JSON.
2. Verify `mode` is `"activative"` and `activative_input` is present.
3. Verify that the manifest has already passed `OperatorManifestParser.parse()` — this Skill is a post-ingest editor, not a replacement for ingest validation.
4. If parsing fails, emit error code `INVALID_MANIFEST_INPUT` and halt.

### Step 2: Load the Registry
1. Read `services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv`.
2. Parse all 243 rows into an in-memory map indexed by `primitive_id`.
3. Columns: `plane`, `primitive_id`, `canonical_name`, `family`, `core_move`, `snapshot_path`, `sha256`, `active_feature_ids`.
4. If the CSV cannot be opened or parsed, emit error code `REGISTRY_LOAD_FAILED` and halt.

### Step 3: Resolve Candidate Primitives
1. Extract existing `hidden_pressure`, `stance`, and `wrong_reading_locks` / `wrong_reading_locks_meaning` prose from the manifest.
2. If `aligned_primitive_ids` is already provided and non-empty, treat those as the initial candidate set.
3. Otherwise, search candidate primitive rows by comparing prose semantics against registry `core_move` descriptions. Match on `core_move` text, not on `canonical_name` alone. Read `summary` and `why_it_works` for deeper matching when `core_move` alone is insufficient.
4. If a cited primitive ID is not present in the 243-entry inventory, emit error code `UNKNOWN_PRIMITIVE_ID` and halt.

### Step 4: Load YAML Snapshots & Verify Checksums
1. For each candidate primitive, resolve `snapshot_path` relative to `services/air/src/cmf_activative_intelligence/data/`.
2. **Critical: Do not reconstruct paths.** Snapshot paths are non-uniform — always read the path from the CSV row. `PRM-HUM-009` lives under `_golden/` while `PRM-HUM-023` lives under its family subfolder. Never assume a fixed path pattern.
3. Read the YAML snapshot file bytes.
4. Compute `sha256 = hashlib.sha256(file_bytes).hexdigest()`.
5. Compare against the CSV row's `sha256` column.
6. If checksum mismatches, emit error code `SHA256_MISMATCH` and halt. Do not proceed silently.
7. Record each verification in the receipt's `verified_yaml_checksums` array with `expected_sha256`, `computed_sha256`, and `verified: true/false`.

### Step 5: Pairwise Conflict Resolution
1. Parse `conflicts_with` entries from all loaded primitive YAML snapshots. `conflicts_with` is a `list[str]` of primitive IDs (e.g. `PRM-HUM-009.conflicts_with = ["PRM-HUM-024", "PRM-HUM-004"]`).
2. Check every pair `(A, B)` in the candidate set.
3. If primitive A lists primitive B under `conflicts_with`, retain the higher-fit primitive and drop the lower-fit one.
4. Do not let the prose-rewrite step launder a conflict into agreeable-sounding text — if they conflict, one must be dropped.
5. Record every dropped pair in the receipt's `dropped_conflict_pairs` array with `kept_primitive_id`, `dropped_primitive_id`, and `conflict_reason`.

### Step 6: Rewrite `hidden_pressure` and `stance`
1. Re-author `hidden_pressure` to ground the psychological tension in the retained primitive's `core_move` language, explicitly citing `primitive_id` and `canonical_name`.
2. Re-author `stance` to ground the participant orientation in the retained primitive's `core_move`.
3. Strip all specimen-specific proper nouns, named individuals, brand names, episode titles, or character names. Replace with generic terms ("the reference specimen," "the subject," "the audience").
4. Record original and aligned prose in the receipt's `prose_changes_applied` array.

### Step 7: Partition and Rewrite Locks (Option B)
1. Review every entry in `wrong_reading_locks`.
2. **Spatial locks** — locks containing visual-syntax vocabulary (`comparison_pair`, `text_block`, `header_zone`, `hero_zone`, `footer_zone`, `overlay_zone`, `full_bleed`, `z_index`, `non_overlap`, `anchor_lock`, `contrast_ratio`, `presence_required`, `absence_required`, `pairing_required`, `content_separation`, or BBox coordinates) — leave completely untouched in `wrong_reading_locks`. Record them in the receipt's `structural_locks_preserved` array.
3. **Meaning-plane locks** — locks describing psychological traps, archetypal misreadings, or identity boundary violations — rewrite into `wrong_reading_locks_meaning`. Apply noun-stripping and primitive-ID-citation rules from Step 6.
4. **Ambiguous locks** — if a lock could reasonably belong to either category, do NOT silently reclassify it. Flag it for human review in the receipt's `ambiguous_locks_flagged` array with the lock text and reason for ambiguity. Set the receipt outcome to `PASS_WITH_REVIEW_REQUIRED`.

### Step 8: Populate `activative_input.aligned_primitive_ids`
1. Store the final conflict-checked list of `primitive_id` strings.
2. Ensure no duplicates exist (duplicates are rejected by Builder ingest validation).
3. All IDs must match `^(PRM|EXP)-[A-Z]{3}-\d{3}$`.

### Step 9: Assemble Output & Emit Receipt
1. Assemble the updated manifest object.
2. **Immutability verification:** Confirm that `task.*` fields, all 7 semantic lineage refs, `wrong_reading_locks` (spatial), `evidence_provenance_refs`, `roles`, `activation_directions`, `stakes`, `identity_urges`, `participation_design`, `intended_reaction`, and `smallest_useful_commitment` are byte-identical to input.
3. Generate the `alignment_receipt` with all required fields per `contracts/output.schema.json`.
4. Set outcome:
   - `PASS` — all primitives verified, no conflicts, no ambiguous locks.
   - `PASS_WITH_REVIEW_REQUIRED` — alignment succeeded but ambiguous locks were flagged for human review.
   - `FAIL` — checksum mismatch, unresolved conflict, or out-of-scope mutation detected.
5. Output the result matching `contracts/output.schema.json`.
