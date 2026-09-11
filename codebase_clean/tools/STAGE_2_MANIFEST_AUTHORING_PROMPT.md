# Stage 2: Harness Manifest Authoring Prompt (Non-Vision Model)
# ---------------------------------------------------------------
# WHAT YOU RECEIVE:
#   - VISUAL_SYNTAX_ANALYSIS.json  (output of harness_vision_analyst.py — Stage 1)
#   - ONE_HARNESS_BUILD_PROMPT.md  (extracted from the original harness zip)
#   - HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md  (extracted from the original harness zip)
#   - DRILL_ME_FORMAT.md  (extracted from the original harness zip)
#
# DO NOT request or use images. Visual syntax analysis is already done. Use ONLY
# the `deduplication_summary.unique_slide_roles` from VISUAL_SYNTAX_ANALYSIS.json
# as the visual layout source.
# ---------------------------------------------------------------

You are an expert manifest compiler for the Conscious Activations Builder system (`cmf_builder`).
You have received a pre-completed Visual Syntax Analysis (VISUAL_SYNTAX_ANALYSIS.json) produced
by a vision model in Stage 1. Your job is Stage 2: authoring the production-valid `manifest.json`.

---

## YOUR INPUTS

1. **VISUAL_SYNTAX_ANALYSIS.json** — Read `deduplication_summary` carefully:
   - `unique_slide_roles` = the canonical layout patterns (duplicates already collapsed).
   - Each entry has `slide_role`, `container_zones`, `primitives`, `reading_order`, `anchor_elements`.
   - Use these as the authoritative source for `wrong_reading_locks` spatial constraints.
   - DO NOT invent additional layout observations not present in this file.

2. **ONE_HARNESS_BUILD_PROMPT.md** — Follow the manifest template and field rules exactly.

3. **DRILL_ME_FORMAT.md** — Use for understanding the format's activative purpose, stakes, and identity urges.

4. **HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md** — Reference for schema rules and category registry.

---

## STRICT SCHEMA RULES (Builder Validation Will Reject Any Deviation)

1. **`category_id`:** Must be exactly ONE of:
   `supervisuals` | `carousels` | `short_form_edited_video` | `2d_character_animation` | `conversational_activation_expression`

2. **`task.capability_requirements`:** MUST be `[]` (empty array). Do NOT put anything here.

3. **`task.provenance_refs`:** MUST include:
   `"visual_syntax_composition_compiler@1.0.0#sha256:788d157313e2aed64b259b22bdbd51c0763c06953faa92a81cdf795cd604e724"`

4. **Option B Lock Partitioning:**

   `activative_input.wrong_reading_locks` — SPATIAL LOCKS ONLY:
   - Derived directly from `unique_slide_roles[].primitives` and `unique_slide_roles[].container_zones` in VISUAL_SYNTAX_ANALYSIS.json.
   - Must reference canonical primitive types (`text_block`, `image_region`, `comparison_pair`, `badge`, `number_label`, `icon_row`, `caption_plate`, `callout_arrow`, `flow_diagram`) and zones (`header_zone`, `hero_zone`, `footer_zone`, `overlay_zone`, `full_bleed`).
   - Minimum 3 locks. Each must be a specific, non-generic constraint derived from the actual visual syntax.

   `activative_input.wrong_reading_locks_meaning` — PSYCHOLOGICAL LOCKS ONLY:
   - Each lock must cite at least one AIR primitive ID (format `PRM-XXX-000` or `EXP-XXX-000`).
   - Must contain ZERO specimen-specific proper nouns, character names, or brand names.
   - Valid primitive IDs include: `PRM-HUM-009`, `PRM-BUS-001`, `PRM-PSY-018`, `EXP-FBK-004` and any others from the registry.
   - Minimum 2 locks.

5. **`activative_input.aligned_primitive_ids`:** List 2–4 AIR Primitive IDs matching the harness's core psychological mechanics. Must match regex `^(PRM|EXP)-[A-Z]{3}-\d{3}$`.

6. **Noun-Stripping Discipline:**
   - `hidden_pressure` and `stance` must contain ZERO proper nouns, character names, brand names, or specimen-specific references.
   - Refer to subjects generically: "the reference specimen", "the speaker", "the participant", "the audience".

7. **Identifiers:**
   - `manifest_id`: `"operator-manifest-<slug>"` (kebab-case slug)
   - `task_id`: `"<slug>_v1"` (snake_case slug + `_v1`)

8. **Visual Syntax Deduplication (already done for you):**
   - The `unique_slide_roles` array already has duplicates collapsed. Do not re-invent or expand it.
   - Your spatial locks should reflect the UNIQUE layout patterns only, not every individual slide.

---

## OUTPUT REQUIREMENT

Output ONLY the complete, valid, un-truncated `manifest.json` as a JSON code block.
No preamble, no explanation, no markdown outside the JSON block.
Ready for `cmf-builder ingest` without modification.
