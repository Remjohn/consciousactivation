# Harness Authoring Master Prompts & Execution Guide

**Version:** 1.1.0  
**Status:** RATIFIED_AUTHORING_GUIDE  
**Target Repository:** `consciousactivation`  
**Location of Raw Harness Bundles:** `atomic_harnesses_visual_syntax/`  
**Location of Output Library:** `storage/harness-library/`  
**Governing Visual Syntax Skill:** `services/builder/skill-packages/visual_syntax_composition_compiler/1.0.0/`

---

## 1. Overview

This document provides the master prompt template and execution instructions for compiling raw visual harness bundles into production-ready `operator_manifest.json` definitions.

All raw harness bundles reside directly inside the repository at `atomic_harnesses_visual_syntax/`. The compiled manifests reference the canonical `visual_syntax_composition_compiler` skill to bind visual grammar primitives without duplicating syntax logic.

---

## 2. Format Category Mapping

Every harness must bind to **exactly one** of the 5 canonical UI categories:

| Format Directory in `atomic_harnesses_visual_syntax/` | Canonical `category_id` | UI Display Name (`category_name`) |
|---|---|---|
| `supervisuals/` | `supervisuals` | SuperVisuals |
| `carousels/` | `carousels` | Carousels & Slide Documentaries |
| `format01_story_video/` | `short_form_edited_video` | Short-Form Edited Video |
| `format02_minimal_coach_theatre/` | `2d_character_animation` | 2D Character Animation |
| `format03_living_commentary/` | `short_form_edited_video` | Short-Form Edited Video |
| `format04_conscious_reaction/` | `short_form_edited_video` | Short-Form Edited Video |
| `format05_silent_dialogue_theatre/` | `2d_character_animation` | 2D Character Animation |
| `format06_bar_chart_race/` | `supervisuals` | SuperVisuals |
| `format07_coaching/` | `conversational_activation_expression` | Conversational Activation |
| `format08_poetic_quote_theatre/` | `2d_character_animation` | 2D Character Animation |

---

## 3. Master Prompt Snippet (For Claude Chat Sessions)

Copy and paste the snippet below when starting a Claude chat session to author or validate a harness:

```markdown
# Harness Compilation Task — Direct Zip Upload

You are compiling the attached raw visual harness zip file into a production-valid `manifest.json` for the `cmf_builder` pipeline.

## Input Material
- **Uploaded Zip:** Contains `ONE_HARNESS_BUILD_PROMPT.md`, `DRILL_ME_FORMAT.md`, `DRILL_ME_BBOX_WHY.md`, `HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md`, and visual image specimens (`.png`/`.jpg`).

## ⚠️ Critical Validator Rules (Must Follow)
1. `category_id`: MUST be set to exactly one of the 5 canonical categories:
   - `supervisuals` (SuperVisuals — single-frame portrait/quote graphics)
   - `carousels` (Carousels & Slide Documentaries — multi-slide editorial)
   - `short_form_edited_video` (Short-Form Edited Video — Reels/TikToks)
   - `2d_character_animation` (2D Character Animation — animated theatre)
   - `conversational_activation_expression` (Conversational Activation — dynamic chat)
2. `capability_requirements`: MUST be a non-empty list — use `["activative_contract_validation"]`.
3. `input_contract.properties`: `identity_dna` is FORBIDDEN here. It belongs exclusively in `activative_input.identity_dna_ref`. Use `source_expression_moment` and `voice_context` for runtime input properties.
4. `wrong_reading_locks`: MUST be a non-empty list of at least 3 format-specific negative constraints derived from the visual specimens and DRILL_ME files.
5. `provenance_refs`: Include reference to `visual_syntax_composition_compiler@1.0.0` in addition to prompt/specimen source refs.
6. **Primitive Taxonomy Mapping (Visual Syntax):** Classify slide visual elements into the canonical primitive taxonomy:
   - `text_block`, `image_region`, `grid_cluster`, `comparison_pair`, `badge`, `number_label`, `icon_row`, `caption_plate`, `callout_arrow`, `flow_diagram`
   - Map elements into container zones (`header_zone`, `hero_zone`, `footer_zone`, `overlay_zone`, `full_bleed`).
   - Do NOT invent new primitive names or hardcode content strings as types.
7. Slugs & IDs: Set `manifest_id` to `"operator-manifest-<slug>"` and `task_id` to `"<slug>_v1"` using a clean slug (e.g. `twq_img_portrait_v1`).

## Instructions
1. Inspect all files and image specimens inside the uploaded zip.
2. Execute the 5-step classification & synthesis procedure from `ONE_HARNESS_BUILD_PROMPT.md`.
3. Output the complete, valid, un-truncated `manifest.json` ready for `cmf-builder ingest`.
```

---

## 4. CLI Execution & Pipeline Build Commands

Once a `manifest.json` is written for a harness, run the 4-step build sequence in your terminal to ingest, build, inspect, and export the built harness definition:

```bash
# Step 1: Ingest manifest (validates schema & governance gates)
cd services/builder
python -m cmf_builder.cli ingest "path/to/manifest.json"

# Step 2: Build harness definition
python -m cmf_builder.cli build --artifact-id <operator-manifest-id>

# Step 3: Inspect definition (sanity check)
python -m cmf_builder.cli inspect --artifact-id <definition-artifact-id>

# Step 4: Export zip package to Harness Library (ALWAYS specify explicit --output path)
python -m cmf_builder.cli export --artifact-id <definition-artifact-id> --output "../../storage/harness-library/<HARNESS_NAME>.zip"
```

---

## 5. Strict Naming Conventions & Export Rules

When exporting compiled harness packages to `storage/harness-library/`, enforce the 3-tier naming convention:

| Identity Layer | Format / Example | Purpose |
|---|---|---|
| **Cryptographic ID (`definition_id`)** | `atomic-harness-definition_7f0e70c1...` | Auto-generated by Builder (sha256 digest) to guarantee no collisions in database. |
| **Manifest Slug (`task_id`)** | `TWQ-STD-Standard` or `twq_std_standard_v1` | Human-readable slug in `manifest.json`. |
| **Library Package File (`package_file`)** | `TWQ-STD-Standard.zip` | Explicit `--output` filename saved to `storage/harness-library/`. |
