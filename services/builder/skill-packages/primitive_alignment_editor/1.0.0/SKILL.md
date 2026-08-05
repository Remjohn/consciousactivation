---
name: primitive_alignment_editor
version: 1.0.0
authority_lane: Analyst
maturity: development_uncertified
---

# Primitive Alignment Editor

Align an operator manifest's psychological and archetypal prose fields
(`hidden_pressure`, `stance`, `wrong_reading_locks_meaning`) against the
243-entry Activative Intelligence Primitive Registry, strip specimen-specific
proper nouns, enforce pairwise `conflicts_with` checking, and populate
`activative_input.aligned_primitive_ids`. The output is an aligned manifest
where every psychological mechanism claim is grounded in a verified, conflict-
free primitive from the governed registry — this Skill does not render content,
select specimens, or produce campaign artifacts.

## Primitive Registry Structure

The authoritative registry lives at:
`services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv`

All snapshot paths are relative to:
`services/air/src/cmf_activative_intelligence/data/`

### CSV Columns (Confirmed by Direct Read)

| Column              | Description                                                                  |
|---------------------|------------------------------------------------------------------------------|
| `plane`             | `meaning_plane` (192 entries) or `experience_plane` (51 entries)             |
| `primitive_id`      | Governed ID matching `^(PRM\|EXP)-[A-Z]{3}-\d{3}$`                           |
| `canonical_name`    | Human-readable name (e.g. "Reference Funny Filter")                          |
| `family`            | Category family (e.g. `humor_distortion`, `persuasion`, `psychological_diagnostics`) |
| `core_move`         | The essential behavioral mechanism — match on this, not on `canonical_name`  |
| `snapshot_path`     | Relative path to the primitive's governing YAML snapshot                      |
| `sha256`            | Expected SHA256 digest of the YAML snapshot file bytes                        |
| `active_feature_ids`| Pipe-delimited feature flags (e.g. `F04\|F20`), may be empty                 |

### Families (20 Families Across 2 Planes)

| Family                        | Count | Plane             |
|-------------------------------|-------|--------------------|
| `humor_distortion`            | 40    | meaning_plane      |
| `persuasion`                  | 35    | meaning_plane      |
| `visual_sonic_guidance`       | 33    | meaning_plane      |
| `psychological_diagnostics`   | 27    | meaning_plane      |
| `design_business`             | 14    | meaning_plane      |
| `voice_audio_intimacy`        | 12    | meaning_plane      |
| `narrative_structure`         | 11    | meaning_plane      |
| `trigger_timing`              | 10    | meaning_plane      |
| `performance_delivery`        | 10    | meaning_plane      |
| `referral_trust_transfer`     | 9     | meaning_plane      |
| `progression_replay`          | 7     | meaning_plane      |
| `friction_ability`            | 6     | meaning_plane      |
| `personalization_identity`    | 6     | meaning_plane      |
| `safe_failure_recovery`       | 6     | meaning_plane      |
| `trust_branding`              | 5     | meaning_plane      |
| `social_referral`             | 5     | meaning_plane      |
| `feedback_scoring`            | 6     | experience_plane   |
| `story_discovery`             | 1     | meaning_plane      |
| *(+ experience families)*     | 51    | experience_plane   |

### Snapshot YAML Structure (Confirmed by Direct Read)

Meaning-plane primitives (`PRM-*`) carry these top-level keys:
`primitive_id`, `canonical_name`, `aliases`, `family`, `implementation_role`,
`source_audits`, `book_reference`, `summary`, `core_move`, `why_it_works`,
`examples`, `anti_examples`, `phase_fit`, `surface_fit`, `goal_bias`,
`ccp_workflow_fit`, `trigger_conditions`, `suppression_conditions`,
`misuse_modes`, `synergizes_with`, `conflicts_with`, `crosswalk_id`,
`crosswalk_note`, `notes`

Experience-plane primitives (`EXP-*`) carry a different schema:
`experience_primitive_id`, `canonical_name`, `aliases`, `experience_family`,
`mechanic_role`, `moment_role`, `implementation_role`, `source_audits`,
`book_reference`, `summary`, `core_move`, `why_it_works`, `examples`,
`anti_examples`, `experience_stage_fit`, `surface_fit`, `user_state_effects`,
`ccp_workflow_fit`, `activation_conditions`, `suppression_conditions`,
`misuse_modes`, `synergizes_with`, `conflicts_with`, `implementation_targets`,
`experience_metrics`, `crosswalk_id`, `crosswalk_note`

**Critical:** `conflicts_with` is a `list[str]` of primitive IDs that this
primitive must not be co-cited with (e.g. `PRM-HUM-009.conflicts_with` =
`["PRM-HUM-024", "PRM-HUM-004"]`).

### Snapshot Path Warning — Do Not Reconstruct Paths

Snapshot paths are **not uniform**. Confirmed directly:
- `PRM-HUM-009` lives at `sources/cmf_primitive_registry_snapshot/meaning_plane/_golden/PRM-HUM-009.yaml` (the `_golden` subfolder)
- `PRM-HUM-023` lives at `sources/cmf_primitive_registry_snapshot/meaning_plane/humor_distortion/PRM-HUM-023.yaml` (its family subfolder, no `_golden`)

Always take the path from the CSV row's `snapshot_path` column for that
specific `primitive_id`. Never assume `<plane>/<family>/<id>.yaml` or
`<plane>/_golden/<id>.yaml` as a fixed pattern.

## Option B Lock Partitioning Governance

To eliminate ambiguity between spatial visual-syntax constraints and meaning-
plane psychological locks, this system enforces Option B partitioning:

| Field Name                    | Owning Skill                         | Contains                                      |
|-------------------------------|--------------------------------------|-----------------------------------------------|
| `wrong_reading_locks`         | `visual_syntax_composition_compiler` | Layout constraints, zone bounds, BBox rules, primitive spatial vocabulary (`text_block`, `hero_zone`, `z_index`, `non_overlap`, `anchor_lock`) |
| `wrong_reading_locks_meaning` | `primitive_alignment_editor` (THIS)  | Psychological traps, archetypal misreadings, identity boundary enforcement, primitive mechanism rules citing `PRM-`/`EXP-` IDs |

**Ambiguity Rule:** If a lock is ambiguous between spatial and meaning-plane
categories, flag it for human review rather than guessing — do not silently
reclassify it. Emit the ambiguous lock in the alignment receipt under a
dedicated `ambiguous_locks_flagged` field.

## Ordering Requirement

This Skill must run **before** `visual_syntax_composition_compiler` in any
pipeline that runs both.

Rationale: The compiler only reads `wrong_reading_locks` — it does not rewrite
them. Its `input.schema.json` requires them non-empty at call time. If this
Skill runs second, the compiler will have already translated the noun-leaked,
un-aligned version into a spec, and that spec would need to be regenerated.
Run primitive alignment first, structural compilation second.

## Active Procedure

1. **Load the Registry.** Read `PRIMITIVE_INVENTORY.csv`. Parse all 243 rows
   into an in-memory map indexed by `primitive_id`. Columns: `plane`,
   `primitive_id`, `canonical_name`, `family`, `core_move`, `snapshot_path`,
   `sha256`, `active_feature_ids`.

2. **Resolve Candidate Primitives.** From the manifest's current
   `hidden_pressure` / `stance` / `wrong_reading_locks` / `wrong_reading_locks_meaning`
   prose (or from an already-provided `aligned_primitive_ids` list if one
   exists), identify which registry rows actually match the mechanism at work.
   Match on `core_move` text, not on `canonical_name` alone. Read the
   primitive's `summary` and `why_it_works` for deeper matching when
   `core_move` alone is insufficient.

3. **Load Each Candidate's Full YAML via the CSV's `snapshot_path` Column.**
   For each candidate `primitive_id`, resolve `snapshot_path` relative to
   `services/air/src/cmf_activative_intelligence/data/`. Read the YAML
   snapshot file bytes. Do not reconstruct or assume the path — always read
   it from the CSV row.

4. **Verify Integrity.** Compute `sha256 = hashlib.sha256(file_bytes).hexdigest()`.
   Compare against the CSV row's `sha256` column. Reject on mismatch and emit
   error code `SHA256_MISMATCH` rather than silently proceeding — this mirrors
   how `services/builder` already treats every other reference in this codebase
   via `IMMUTABLE_REF_PATTERN`.

5. **Check `conflicts_with` Pairwise Across Every Candidate Being Cited
   Together.** `conflicts_with` is a `list[str]` of primitive IDs. If
   candidate A lists candidate B under `conflicts_with`, drop the lower-fit
   candidate rather than citing both. Do not let the prose-rewrite step
   launder a conflict into agreeable-sounding text. Record every dropped
   conflict pair in the alignment receipt with:
   - `kept_primitive_id`
   - `dropped_primitive_id`
   - `conflict_reason` (from the YAML's `conflicts_with` context)

6. **Rewrite `hidden_pressure` and `stance`.** The rewritten prose must:
   - (a) Name the selected primitive(s) by `primitive_id` and `canonical_name`.
   - (b) Describe the mechanism using the primitive's own `core_move` language.
   - (c) Contain zero proper nouns, named individuals, brand names, or content
     specific to any one reference specimen — refer to specimens only as "the
     reference specimen(s)," generically.

7. **Partition `wrong_reading_locks`.** Leave locks written in visual-syntax
   vocabulary (`comparison_pair`, `text_block`, `header_zone`, `z_index`,
   `non_overlap`, `anchor_lock`, BBox coordinates, etc.) completely untouched
   — those belong to `visual_syntax_composition_compiler`'s scope, not this
   Skill's. Rewrite only the locks that are actually meaning-plane claims into
   `wrong_reading_locks_meaning`, applying the same noun-stripping and
   primitive-ID-citation rules as step 6.

   **If a lock is ambiguous between the two categories, flag it for human
   review rather than guessing — do not silently reclassify it.**

8. **Populate `activative_input.aligned_primitive_ids`** with the final,
   conflict-checked ID tuple. Ensure no duplicates. These IDs must all pass
   `PRIMITIVE_ID_PATTERN` validation (`^(PRM|EXP)-[A-Z]{3}-\d{3}$`).

9. **Emit an Alignment Audit Receipt** recording:
   - Which primitive IDs were selected and why (citing `core_move` match rationale)
   - Which candidates were rejected for conflicting (with `conflicts_with` reason)
   - Which locks were left untouched as structural (spatial vocabulary)
   - Which locks were flagged as ambiguous for human review
   - A diff of exactly what prose changed in `hidden_pressure`, `stance`, and
     `wrong_reading_locks_meaning`
   - SHA256 verification audit trail for every loaded YAML snapshot

## Completion Criteria

- Every `aligned_primitive_ids` entry exists in `PRIMITIVE_INVENTORY.csv` (243 rows).
- Every loaded YAML snapshot passes SHA256 digest verification.
- No pairwise `conflicts_with` violation exists in the final primitive set.
- `hidden_pressure` and `stance` prose cite selected primitive IDs and `core_move` language.
- Zero proper nouns, named individuals, brand names, or specimen-specific content remain in aligned prose.
- `wrong_reading_locks` (spatial) is byte-identical to input — completely untouched.
- All `task.*` fields are byte-identical to input — completely untouched.
- All 7 semantic lineage refs are byte-identical to input — completely untouched.
- Ambiguous locks are flagged rather than silently reclassified.
- Alignment audit receipt is emitted with complete diff trail.

## Scope Boundary — What This Skill Must NOT Touch

- Any `task.*` field (`goal`, `success_condition`, `atomic_boundary`,
  `input_contract`, `output_contract`, `required_context`,
  `capability_requirements`, `acceptance_tests`, `authority_ref`,
  `provenance_refs`) — structural/visual-syntax territory.
- The 7 semantic ref fields: `source_premise_ref`, `identity_dna_ref`,
  `context_premise_ref`, `resonance_map_ref`, `matrix_of_edging_ref`,
  `activative_intelligence_pack_ref`, `evaluation_contract_ref` — immutable
  lineage pointers, never prose to rewrite.
- `evidence_provenance_refs`, `roles`, `activation_directions`, `stakes`,
  `identity_urges`, `participation_design`, `intended_reaction`,
  `smallest_useful_commitment` — leave these as authored unless a future
  version of this mandate explicitly extends scope.
- `wrong_reading_locks` (spatial layout locks) — owned by
  `visual_syntax_composition_compiler`, not this Skill.

Today's scope is exactly: `hidden_pressure` + `stance` + `wrong_reading_locks_meaning`
+ `aligned_primitive_ids`, nothing wider.

## What This Skill Does Not Do

- Does not render pixels, produce final media, or generate campaign content.
- Does not select photographs, illustrations, or UGC images.
- Does not generate copy, headlines, or caption text.
- Does not modify visual syntax spatial layout locks (`wrong_reading_locks`)
  — it only rewrites meaning-plane locks into `wrong_reading_locks_meaning`.
- Does not modify `task.*` fields, semantic lineage refs, or structural
  provenance.
- Does not invent primitive IDs outside the 243 governed entries in
  `PRIMITIVE_INVENTORY.csv`.
- Does not resolve `conflicts_with` by laundering both primitives into
  agreeable-sounding prose — it drops the lower-fit candidate.
- Does not silently reclassify ambiguous locks — it flags them for human review.

Load branch-specific detail only from the package references named by the
immutable manifest.
