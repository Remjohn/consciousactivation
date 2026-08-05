---
name: primitive_alignment_editor
version: 1.0.0
authority_lane: Analyst
maturity: development_uncertified
---

# Primitive Alignment Editor

Align an operator manifest's psychological and archetypal prose (`hidden_pressure`,
`stance`, `wrong_reading_locks_meaning`) against the 243-entry Activative
Intelligence Primitive Registry (`PRIMITIVE_INVENTORY.csv`), strip specimen-specific
proper nouns, enforce pairwise `conflicts_with` checking, and populate
`activative_input.aligned_primitive_ids` and `activative_input.wrong_reading_locks_meaning`.

This Skill operates strictly on the **meaning plane** and **experience plane**. It does
not modify visual syntax spatial layout locks (`wrong_reading_locks`), target canvas
geometry, or primitive BBox bounds — those remain exclusively under the jurisdiction
of `visual_syntax_composition_compiler`.

---

## Canonical Registry Structure

The registry is loaded from:
`services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv`

Each primitive entry contains:
- `primitive_id`: Governed identifier matching `^(PRM|EXP)-[A-Z]{3}-\d{3}$` (e.g. `PRM-HUM-009`, `PRM-BUS-001`, `EXP-FBK-004`).
- `canonical_name`: Human-readable name of the primitive mechanism.
- `family`: Category family (e.g. `humor_distortion`, `design_business`, `psychological_pressure`).
- `core_move`: The essential behavioral mechanism executed by this primitive.
- `snapshot_path`: Relative path from `services/air/src/cmf_activative_intelligence/data/` to the primitive's governing YAML snapshot.
- `sha256`: Expected SHA256 digest of the primitive's YAML snapshot file.

---

## Option B Lock Partitioning Governance

To eliminate ambiguity between spatial visual syntax constraints and meaning-plane psychological locks, this Skill enforces Option B partitioning:

| Field Name | Owning Skill | Description |
|---|---|---|
| `wrong_reading_locks` | `visual_syntax_composition_compiler` | Visual layout constraints, zone bounds, primitive BBox rules (`text_block`, `hero_zone`, `z_index`, `non_overlap`). |
| `wrong_reading_locks_meaning` | `primitive_alignment_editor` (THIS SKILL) | Psychological traps, archetypal misunderstandings, identity boundary enforcement, and primitive mechanism rules. |

---

## Active Procedure (9-Step Pipeline)

1. **Ingest Operator Manifest & Load Registry:**
   Ingest a Builder-parsed operator manifest JSON. Load all 243 primitive rows from `PRIMITIVE_INVENTORY.csv`.

2. **Candidate Primitive Resolution:**
   Analyze `activative_input.hidden_pressure`, `activative_input.stance`, and `activative_input.wrong_reading_locks_meaning` (or legacy `wrong_reading_locks` prose). Match described psychological mechanics against registry `core_move` definitions.

3. **YAML Snapshot Loading:**
   For each candidate `primitive_id`, resolve its `snapshot_path` relative to `services/air/src/cmf_activative_intelligence/data/`. Read the YAML snapshot file. Do not assume or reconstruct file paths manually.

4. **SHA256 Integrity Verification:**
   Compute the SHA256 digest of the loaded YAML file bytes. Verify against the CSV row's `sha256` digest. Reject immediately if checksum verification fails.

5. **Pairwise Conflict Checking:**
   Inspect `conflicts_with` entries inside loaded primitive YAML snapshots. If candidate A conflicts with candidate B (e.g. `PRM-HUM-009` absurdity vs `PRM-HUM-004` Polarization), drop the candidate with lower contextual fit. Never cite conflicting primitives together.

6. **Rewrite `hidden_pressure` and `stance` Prose:**
   Rewrite `hidden_pressure` and `stance` to:
   - Explicitly cite selected primitive IDs and canonical names.
   - Ground descriptions in the primitive's governed `core_move` phrasing.
   - Strip all proper nouns, brand names, character names, and specimen-specific text (replace with generic references like "the reference specimen").

7. **Partition and Rewrite `wrong_reading_locks_meaning`:**
   Identify meaning-plane locks. Apply noun-stripping and primitive ID citation rules. Do not modify or rewrite visual layout locks (`wrong_reading_locks`) — leave spatial locks untouched.

8. **Populate `activative_input.aligned_primitive_ids`:**
   Write the final conflict-checked tuple of `primitive_id` strings into `activative_input.aligned_primitive_ids`.

9. **Emit Alignment Audit Receipt:**
   Emit an alignment receipt documenting selected primitive IDs, dropped conflicting pairs, prose diffs, and partition records.

---

## Scope Boundaries — What This Skill Does NOT Do

- Does not modify any field in `task.*` (`goal`, `input_contract`, `output_contract`, `provenance_refs`, etc.).
- Does not modify spatial layout locks (`wrong_reading_locks`), BBox coordinates, or container zone geometry.
- Does not mutate immutable semantic lineage refs (`identity_dna_ref`, `source_premise_ref`, `matrix_of_edging_ref`, etc.).
- Does not invent primitive IDs outside the 243 governed entries in `PRIMITIVE_INVENTORY.csv`.
