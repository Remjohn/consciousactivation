# Authority Boundaries — Primitive Alignment Editor

## Lane Authority

This Skill operates strictly within the **Analyst** authority lane.

### Permitted Actions (Exhaustive List)
- Read and verify the 243-entry Activative Intelligence Primitive Registry (`PRIMITIVE_INVENTORY.csv`) and YAML snapshots.
- Match manifest prose against governed `core_move` definitions.
- Strip specimen-specific proper nouns, character names, brand names, and episode titles from prose.
- Rewrite `hidden_pressure` and `stance` to cite primitive IDs and canonical names.
- Re-author meaning-plane locks into `wrong_reading_locks_meaning`.
- Populate `activative_input.aligned_primitive_ids`.
- Flag ambiguous locks for human review.
- Emit alignment audit receipts.

### Prohibited Actions (Exhaustive List)
- **Cannot mutate any `task.*` field:** `goal`, `success_condition`, `atomic_boundary`, `input_contract`, `output_contract`, `required_context`, `capability_requirements`, `acceptance_tests`, `authority_ref`, `provenance_refs`.
- **Cannot mutate spatial layout locks (`wrong_reading_locks`):** container zones, BBox bounds, z-index constraints, anchor lock declarations — all owned by `visual_syntax_composition_compiler`.
- **Cannot mutate the 7 immutable semantic lineage refs:** `source_premise_ref`, `identity_dna_ref`, `context_premise_ref`, `resonance_map_ref`, `matrix_of_edging_ref`, `activative_intelligence_pack_ref`, `evaluation_contract_ref`.
- **Cannot mutate non-extended prose fields:** `evidence_provenance_refs`, `roles`, `activation_directions`, `stakes`, `identity_urges`, `participation_design`, `intended_reaction`, `smallest_useful_commitment` — leave as authored unless a future mandate version explicitly extends scope.
- **Cannot invent primitive IDs** outside the 243 governed entries in `PRIMITIVE_INVENTORY.csv`.
- **Cannot authorize production readiness or certify manifests** — that power belongs exclusively to the Commander lane.
- **Cannot silently reclassify ambiguous locks** — must flag for human review.
