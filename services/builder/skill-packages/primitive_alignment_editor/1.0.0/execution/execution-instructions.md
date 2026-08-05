# Execution Instructions — Primitive Alignment Editor

## Execution Algorithm

### Step 1: Ingest Operator Manifest
1. Read the input operator manifest JSON.
2. Verify that `manifest_id`, `task_id`, `mode`, and `activative_input` pass basic schema validation.
3. If parsing fails, return failure code `INVALID_MANIFEST_INPUT`.

### Step 2: Load Registry & CSV Checksums
1. Open `services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv`.
2. Parse all 243 rows into an in-memory primitive map indexed by `primitive_id`.

### Step 3: Match Candidate Primitives
1. Extract existing `hidden_pressure`, `stance`, `wrong_reading_locks`, and `wrong_reading_locks_meaning` prose.
2. If `aligned_primitive_ids` is already provided, load those candidate IDs.
3. Otherwise, search candidate primitive rows by comparing prose semantics against registry `core_move` descriptions.

### Step 4: Resolve Snapshot Paths & Verify Checksums
1. For each candidate primitive, resolve `snapshot_path` relative to `services/air/src/cmf_activative_intelligence/data/`.
2. Read the YAML snapshot file bytes.
3. Compute `sha256 = hashlib.sha256(data).hexdigest()`.
4. Compare against the CSV row's `sha256` digest.
5. If checksum mismatches, halt execution and emit error code `SHA256_MISMATCH`.

### Step 5: Perform Pairwise Conflict Resolution
1. Parse `conflicts_with` entries from all loaded primitive YAML snapshots.
2. Check every pair `(A, B)` in the candidate primitive list.
3. If primitive A lists primitive B under `conflicts_with`, retain the higher-fit primitive and drop the lower-fit primitive.
4. Record dropped conflict pairs in the alignment receipt (`dropped_conflict_pairs`).

### Step 6: Rewrite `hidden_pressure` and `stance`
1. Re-author `hidden_pressure` to ground the psychological tension in the retained primitive `core_move` language, explicitly citing `primitive_id` and `canonical_name`.
2. Re-author `stance` to ground the participant orientation in the retained primitive `core_move`.
3. Strip all specimen-specific proper nouns, named individuals, brand names, or episode titles (replace with generic terms like "the reference specimen").

### Step 7: Partition & Rewrite `wrong_reading_locks_meaning` (Option B)
1. Separate meaning-plane locks from visual-syntax spatial locks.
2. Leave spatial layout locks in `wrong_reading_locks` completely untouched.
3. Re-author meaning-plane locks in `wrong_reading_locks_meaning` to cite primitive IDs and enforce archetypal boundary rules without proper nouns.

### Step 8: Populate `activative_input.aligned_primitive_ids`
1. Store the final conflict-checked list of `primitive_id` strings into `activative_input.aligned_primitive_ids`.
2. Ensure no duplicates exist in the list.

### Step 9: Assemble Output Manifest & Emit Receipt
1. Assemble the updated manifest object. Verify that `task.*` fields and all 7 semantic lineage refs remain byte-identical.
2. Generate `alignment_receipt` with `receipt_id`, checksum audit trail, prose diffs, and outcome `PASS`.
3. Output the result matching `contracts/output.schema.json`.
