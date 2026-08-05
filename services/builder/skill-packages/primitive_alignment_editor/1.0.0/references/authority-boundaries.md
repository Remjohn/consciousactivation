# Authority Boundaries — Primitive Alignment Editor

## Lane Authority

This Skill operates strictly within the **Analyst** authority lane.

### Permitted Actions
- Read and verify the 243-entry Activative Intelligence Primitive Registry (`PRIMITIVE_INVENTORY.csv`) and YAML snapshots.
- Match manifest prose against governed `core_move` definitions.
- Strip specimen-specific proper nouns, character names, brand names, and episode titles from prose.
- Rewrite `hidden_pressure` and `stance` to cite primitive IDs and canonical names.
- Re-author meaning-plane locks in `wrong_reading_locks_meaning`.
- Populate `activative_input.aligned_primitive_ids`.
- Emit alignment audit receipts.

### Prohibited Actions
- Cannot mutate any `task.*` field (`goal`, `input_contract`, `output_contract`, `provenance_refs`, etc.).
- Cannot mutate spatial layout locks (`wrong_reading_locks`), container zones, or primitive BBox bounds.
- Cannot mutate the 7 immutable semantic lineage refs (`identity_dna_ref`, `source_premise_ref`, etc.).
- Cannot invent primitive IDs outside the 243 governed entries in `PRIMITIVE_INVENTORY.csv`.
- Cannot authorize production readiness or certify manifests — that power belongs exclusively to the Commander lane.
