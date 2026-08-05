# Mandate: New Skill — `primitive_alignment_editor`

## Problem statement

`activative_input.hidden_pressure`, `activative_input.stance`, and
`activative_input.wrong_reading_locks` are free-text prose fields. When
written by hand (or by an agent without this Skill), they tend to encode the
*specific reference specimen's* content — proper nouns, named individuals,
one-off phrasing — instead of the *generalizable mechanism* the format
actually runs on. This happened twice in this project already, across two
different harnesses, before it was caught by inspection rather than by any
enforced process. It should be enforced by a process.

Separately, `services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv`
(243 rows, `meaning_plane` + `experience_plane`) is never consulted anywhere
in `services/builder`. There is currently no step in the pipeline where a
harness's psychological/archetypal framing is checked against that registry
for (a) whether cited primitives actually exist, (b) whether cited primitives
conflict with each other per their own `conflicts_with` fields, or (c)
whether the prose genuinely reflects the primitive's `core_move`.

## Why this must NOT be added to `visual_syntax_composition_compiler`

Confirmed by re-reading
`services/builder/skill-packages/visual_syntax_composition_compiler/1.0.0/SKILL.md`
in full:

- Its own "What This Skill Does Not Do" section states explicitly: **"Does
  not modify wrong-reading locks — it only translates them into spatial
  constraints."** It is read-only with respect to `wrong_reading_locks` and
  never touches `hidden_pressure` or `stance` at all — neither field appears
  anywhere in `contracts/input.schema.json` or `contracts/output.schema.json`.
- Its Canonical Primitive Taxonomy (`text_block`, `image_region`,
  `grid_cluster`, `comparison_pair`, `badge`, `number_label`, `icon_row`,
  `caption_plate`, `callout_arrow`, `flow_diagram`) is a **layout/composition**
  registry — 10 entries, scoped to `carousels` and `supervisuals` only (step 1
  of its Active Procedure returns `NOT_APPLICABLE` for any other category).
  It has no relationship to the 243-entry meaning/experience-plane registry
  in `services/air` and imports nothing from that service.
- Folding primitive-registry alignment into this Skill means one compiler
  pass reasoning across two unrelated registries (10 layout primitives vs.
  243 meaning primitives) with two different failure modes and two different
  authoritative data sources. That's the "cognitive collision" risk — keep
  them as separate passes with separate scopes, matching the pattern already
  established by Builder ingest / Visual Syntax compilation / AIR's own
  Matrix-of-Edging being three already-separate stages.

## A concrete compatibility gap this Skill's ordering must account for

Re-reading `contracts/output.schema.json` for the Visual Syntax Compiler
turned up a real mismatch, not a hypothetical one: `wrong_reading_lock_constraints[]`
requires `spatial_constraints` with `minItems: 1` for **every** entry, and
`constraint_type` is a closed enum: `z_index_order, non_overlap, anchor_lock,
contrast_ratio, presence_required, absence_required, pairing_required,
content_separation`. Every one of those is a layout concept. A meaning-plane
lock — e.g. "do not assign a fixed pose to either slot in the comparison_pair,
because doing so would break PRM-HUM-009's recognition mechanic" — has no
honest mapping to any of these 8 constraint types. As written, the compiler's
own schema currently assumes every lock in `wrong_reading_locks` is spatially
translatable, which is no longer true once this Skill starts writing
meaning-plane locks into that same array.

**This mandate does not resolve that gap** — it's a `visual_syntax_composition_compiler`
schema question, not a `primitive_alignment_editor` one — but whoever
implements this Skill needs to hand it off explicitly rather than let it
surface as a silent validation failure later. Two options worth putting in
front of whoever owns that Skill next:
1. Loosen `output.schema.json` to allow `spatial_constraints: []` (or a
   `NOT_SPATIALLY_APPLICABLE` marker object) for locks the compiler
   recognizes as meaning-plane-only.
2. Split `wrong_reading_locks` into two fields at the `activative_input`
   schema level (e.g. add `wrong_reading_locks_spatial` alongside the
   existing field). This is architecturally cleaner but is a real, required-field
   migration this time — `wrong_reading_locks` is already in
   `ACTIVATIVE_REQUIRED_FIELDS` in `manifest_parser.py`, unlike the optional
   field added in `MANDATE_01`.

## Ordering requirement

This Skill must run **before** `visual_syntax_composition_compiler` in any
pipeline that runs both, because the compiler only reads `wrong_reading_locks`
— it doesn't rewrite them, and its input schema requires them non-empty at
call time (`contracts/input.schema.json`, `required: [..., "wrong_reading_locks", ...]`).
If this Skill runs second, the compiler will have already translated the
noun-leaked, un-aligned version into a spec, and that spec would need to be
regenerated. Run primitive alignment first, structural compilation second.

## What this Skill does

**Input:** a Builder-valid operator manifest JSON (the same shape ingested by
`services/builder/src/cmf_builder/application/manifest_parser.py` —
i.e. it should already pass `OperatorManifestParser.parse()` before this
Skill runs; this Skill is a post-ingest editor, not a replacement for
ingest validation).

**Output:** the same manifest, with only these `activative_input` fields
changed: `hidden_pressure`, `stance`, `wrong_reading_locks` (meaning-plane
entries only — see "Scope boundary" below), and the new
`activative_input.aligned_primitive_ids` field once `MANDATE_01` ships. Every
other field, including all of `task.*` and the manifest's `manifest_id` /
`task_id`, is passed through byte-identical.

**Procedure (mirroring the Active Procedure structure the compiler already
uses, so both Skills read the same way):**

1. **Load the registry.** Read
   `services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv`.
   Columns, confirmed by direct read: `plane, primitive_id, canonical_name,
   family, core_move, snapshot_path, sha256, active_feature_ids`.
2. **Resolve candidate primitives.** From the manifest's current
   `hidden_pressure`/`stance`/`wrong_reading_locks` prose (or from an
   already-selected `aligned_primitive_ids` list if one exists), identify
   which registry rows actually match the mechanism at work — same method
   used by hand this session: match on `core_move` text, not on
   `canonical_name` alone.
3. **Load each candidate's full YAML via the CSV's `snapshot_path` column —
   do not reconstruct the path.** Confirmed directly: the path is *not*
   uniform. `PRM-HUM-009`'s snapshot lives at
   `sources/cmf_primitive_registry_snapshot/meaning_plane/_golden/PRM-HUM-009.yaml`
   (the `_golden` subfolder) while `PRM-HUM-023`'s lives at
   `sources/cmf_primitive_registry_snapshot/meaning_plane/humor_distortion/PRM-HUM-023.yaml`
   (its family subfolder, no `_golden`). Always take the path from the CSV
   row for that specific `primitive_id`; never assume `<plane>/<family>/<id>.yaml`
   or `<plane>/_golden/<id>.yaml` as a fixed pattern.
4. **Verify integrity.** Hash the loaded YAML and compare to the CSV row's
   `sha256` column. Reject on mismatch rather than silently proceeding —
   this mirrors how `services/builder` already treats every other reference
   in this codebase (`IMMUTABLE_REF_PATTERN` requires a `#sha256:` suffix on
   every ref in a manifest; this Skill should hold its own registry reads to
   the same standard even though the manifest schema itself doesn't yet
   require it for this field).
5. **Check `conflicts_with` pairwise across every candidate being cited
   together.** Confirmed present in the YAML schema: `PRM-HUM-009`'s own
   snapshot lists `PRM-HUM-004` (Contrastive Extreme Polarization) under
   `conflicts_with`, with the stated reason "absurdity conflicts with
   recognition realism." If two candidates conflict, drop the lower-fit one
   rather than citing both — do not let the prose-rewrite step launder a
   conflict into agreeable-sounding text.
6. **Rewrite `hidden_pressure` and `stance`.** Prose must (a) name the
   selected primitive(s) by ID and `canonical_name`, (b) describe the
   mechanism using the primitive's own `core_move` language, (c) contain zero
   proper nouns, named individuals, brand names, or content specific to any
   one reference specimen — refer to specimens only as "the reference
   specimen(s)," generically, exactly as this session's rewrite did for both
   the Jealousy and Anthem harnesses.
7. **Partition `wrong_reading_locks`.** Leave locks written in visual-syntax
   vocabulary (`comparison_pair`, `text_block`, `header_zone`, etc.) untouched
   — those belong to `visual_syntax_composition_compiler`'s scope, not this
   Skill's. Rewrite only the locks that are actually meaning-plane claims,
   applying the same noun-stripping and primitive-ID-citation rule as step 6.
   If a lock is ambiguous between the two categories, flag it for human
   review rather than guessing — do not silently reclassify it.
8. **Populate `activative_input.aligned_primitive_ids`** with the final,
   conflict-checked ID list (requires `MANDATE_01` to have shipped first;
   until then, this step's output can't be written back into the manifest
   without failing ingest, since the field doesn't exist yet — hold it in the
   Skill's own receipt/output instead).
9. **Emit a receipt**, matching the project's existing convention
   (`services/builder/skill-packages/visual_syntax_composition_compiler/1.0.0/PACKAGE_RECEIPT.json`
   is the pattern to follow) recording: which primitive IDs were selected and
   why, which candidates were rejected for conflicting, which locks were
   left untouched as structural, and a diff of exactly what prose changed.
   This is for auditability — so a later reviewer isn't stuck re-deriving
   "why does this manifest cite PRM-HUM-009" from scratch the way this
   session had to re-derive the wrong_reading_locks sampling error by hand.

## Scope boundary — what this Skill must NOT touch

- Any `task.*` field (`goal`, `success_condition`, `atomic_boundary`,
  `input_contract`, `output_contract`, `required_context`,
  `capability_requirements`, `acceptance_tests`, `authority_ref`,
  `provenance_refs`) — structural/visual-syntax territory, not this Skill's.
- The 7 semantic ref fields validated by `_SEMANTIC_REF_FIELDS` in
  `services/builder/src/cmf_builder/domain/category_binding.py`
  (`source_premise_ref`, `identity_dna_ref`, `context_premise_ref`,
  `resonance_map_ref`, `matrix_of_edging_ref`,
  `activative_intelligence_pack_ref`, `evaluation_contract_ref`) — these are
  immutable pointers, never prose to rewrite.
- `evidence_provenance_refs`, `roles`, `activation_directions`, `stakes`,
  `identity_urges`, `participation_design`, `intended_reaction`,
  `smallest_useful_commitment` — leave these as authored unless a future
  version of this mandate explicitly extends scope to them. Today's mandate
  is `hidden_pressure` + `stance` + the meaning-plane subset of
  `wrong_reading_locks` + the new `aligned_primitive_ids` field, nothing wider.

## Suggested package layout

Mirroring `services/builder/skill-packages/visual_syntax_composition_compiler/1.0.0/`
file-for-file, at
`services/builder/skill-packages/primitive_alignment_editor/1.0.0/`:
`SKILL.md`, `PACKAGE_RECEIPT.json`, `compatibility.json`, `manifest.json`,
`contracts/input.schema.json`, `contracts/output.schema.json`,
`execution/execution-instructions.md`, `execution/system-instructions.md`,
`references/authority-boundaries.md`, `references/behavioral-anchors.md`,
`references/context-requirements.md`, `references/failure-taxonomy.md`,
`references/observability.md`, `references/wrong-reading-locks.md` (this last
one specifically should document the "leave structural locks alone, rewrite
only meaning-plane locks" partition rule from step 7 above, since it's the
single easiest step for an implementing agent to get wrong).

Note this package's own `PACKAGE_RECEIPT.json` should almost certainly start
with `"certified": false, "maturity": "development_uncertified",
"production_eligible": false` — matching the Visual Syntax Compiler's own
current receipt values exactly, since this is a newer, less-proven skill.
