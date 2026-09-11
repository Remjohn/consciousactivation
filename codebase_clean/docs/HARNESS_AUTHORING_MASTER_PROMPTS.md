# Harness Authoring Master Prompts & Execution Guide

**Version:** 1.3.0  
**Status:** RATIFIED_AUTHORING_GUIDE  
**Target Repository:** `consciousactivation`  
**Location of Raw Harness Bundles:** `atomic_harnesses_visual_syntax/`  
**Location of Compiled Evidence:** `stage1_output/` (Stage 1 reports) and `stage1_output/specs/` (Stage 2 specs)  
**Location of Output Library:** `${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library}` — resolved at runtime by `api/routers/harnesses.py::get_harness_library_root()`; never a fixed repo path.  
**Governing Visual Syntax Skill:** `services/builder/skill-packages/visual_syntax_composition_compiler/1.0.0/`

> **2026-08-14 correction (v1.3.0):** fixed three defects found in audit — (1) `storage/harness-library/` was never a real path, it doesn't exist and nothing reads it; the real library root is env-resolved, see above; (2) `capability_requirements` guidance below previously said "non-empty," which directly contradicted `ONE_HARNESS_BUILD_PROMPT.md` and would break every harness at campaign-creation time (known Blocker 2, see `docs/PRD/CURRENT.md` §1.10#1) — corrected to `[]`; (3) Stage 1 report path corrected — Stage 1 reports live directly in `stage1_output/`, not `stage1_output/reports/` (that subfolder holds Stage 2 reports instead).

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

## 2.1 Mandatory Specimen Inspection Enforcement

**THIS IS A NON-NEGOTIABLE EXECUTION RULE. VIOLATION IS A CONSTITUTIONAL BREACH.**

Laziness, superficial skimming, or assuming "the rest look the same" when analyzing visual specimens is **strictly prohibited**. Every harness's visual syntax, wrong-reading locks, and primitive taxonomy mapping MUST be derived from thorough individual inspection of the actual specimen images — not from guessing, summarizing titles, or extrapolating from one or two examples.

### Inspection Minimums

| Content Type | Minimum Inspection Requirement |
|---|---|
| **Carousels** | Inspect **every individual slide image** in the harness folder. Each slide may have a different zone layout, different primitive composition, and different wrong-reading risk. Treating slide 1 as representative of slides 2–10 is a failure. |
| **SuperVisuals** | Inspect **every specimen image** in the harness folder. Each specimen variant (quote card, stat card, meme template, comparison split) may use different primitives and zones. |
| **Video formats** | Inspect a **minimum of 20 screenshots/frames** from the reference material. If fewer than 20 exist, inspect all of them. |

### What "Inspect" Means

For each image/slide/frame, the agent MUST:
1. **Open and view the actual image** — not just read filenames or metadata.
2. **Identify every visual element** present in that specific image.
3. **Map each element** to a canonical primitive type (`text_block`, `image_region`, `badge`, etc.).
4. **Note the container zone** each element occupies (`header_zone`, `hero_zone`, etc.).
5. **Record differences** between this slide and previous slides — layout changes, missing elements, new elements, different z-ordering, changed font weights.

### What Counts as a Violation

- Viewing only 2–3 slides of a 10-slide carousel and writing locks based on those alone.
- Describing visual syntax without having opened the actual images.
- Writing generic wrong-reading locks that could apply to any format rather than locks grounded in specific observed specimen details.
- Assuming all slides in a carousel share identical layout without verifying each one.

---

## 3. Master Prompt Snippet (For Claude Chat Sessions)

Copy and paste the snippet below when starting a Claude chat session to author or validate a harness:

```markdown
# Harness Compilation Task

You are compiling a raw visual harness bundle into a production-valid `manifest.json` for the `cmf_builder` pipeline.

## Input Material
- **Harness reference material:** `atomic_harnesses_visual_syntax/<category>/<harness_id>/` — raw image specimens (`.png`/`.jpg`), plus process docs `ONE_HARNESS_BUILD_PROMPT.md`, `DRILL_ME_FORMAT.md`, `DRILL_ME_BBOX_WHY.md`, `HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md`.
- **Compiled evidence (load this first):** `stage1_output/{harness_id}_STAGE1_REPORT.json` and `stage1_output/specs/{harness_id}_STAGE2_SPEC.json`.

## ⚠️ MANDATORY: Specimen Inspection Rule (Non-Negotiable)
Before writing ANY manifest fields, you MUST first load `stage1_output/{harness_id}_STAGE1_REPORT.json` and `stage1_output/specs/{harness_id}_STAGE2_SPEC.json`. Treat these as the verified, canonical evidence base for visual syntax and `wrong_reading_locks`.

ONLY if those reports are thin or missing should you fall back to raw-image inspection. If you must fall back, individually open and inspect:
- **Carousels:** EVERY slide image in the harness folder. Do not skip any.
- **SuperVisuals:** EVERY specimen image in the harness folder. Do not skip any.
- **Video formats:** At least 20 frames/screenshots. If fewer than 20 exist, inspect ALL.

For each image you MUST: identify every visual element, map it to a canonical primitive (`text_block`, `image_region`, `grid_cluster`, `comparison_pair`, `badge`, `number_label`, `icon_row`, `caption_plate`, `callout_arrow`, `flow_diagram`), note its container zone (`header_zone`, `hero_zone`, `footer_zone`, `overlay_zone`, `full_bleed`), and record per-slide layout differences.

Skimming, assuming, or extrapolating from a subset is a constitutional violation.

## ⚠️ Critical Validator Rules (Must Follow)
1. `category_id`: MUST be set to exactly one of the 5 canonical categories:
   - `supervisuals` (SuperVisuals — single-frame portrait/quote graphics)
   - `carousels` (Carousels & Slide Documentaries — multi-slide editorial)
   - `short_form_edited_video` (Short-Form Edited Video — Reels/TikToks)
   - `2d_character_animation` (2D Character Animation — animated theatre)
   - `conversational_activation_expression` (Conversational Activation — dynamic chat)
2. `capability_requirements`: MUST be `[]` (empty). Non-empty values fail at campaign-creation time today — `capability_metadata` is hardcoded to `{}` at that call site, so it can never satisfy a non-empty requirements list (known gate, tracked in `docs/PRD/CURRENT.md` §1.10#1). Not this harness's problem to solve.
3. `input_contract.properties`: `identity_dna` is FORBIDDEN here. It belongs exclusively in `activative_input.identity_dna_ref`. Use `source_expression_moment` and `voice_context` for runtime input properties.
4. `wrong_reading_locks`: MUST be a non-empty list of at least 3 format-specific negative constraints derived from the visual specimens and DRILL_ME files. Each lock MUST reference specific primitive types and spatial constraints observed in the inspected specimens.
5. `provenance_refs`: Include reference to `visual_syntax_composition_compiler@1.0.0` in addition to prompt/specimen source refs.
6. **Primitive Taxonomy Mapping (Visual Syntax):** Classify slide visual elements into the canonical primitive taxonomy:
   - `text_block`, `image_region`, `grid_cluster`, `comparison_pair`, `badge`, `number_label`, `icon_row`, `caption_plate`, `callout_arrow`, `flow_diagram`
   - Map elements into container zones (`header_zone`, `hero_zone`, `footer_zone`, `overlay_zone`, `full_bleed`).
   - Do NOT invent new primitive names or hardcode content strings as types.
7. Slugs & IDs: Set `manifest_id` to `"operator-manifest-<slug>"` and `task_id` to `"<slug>_v1"` using a clean slug (e.g. `twq_img_portrait_v1`).

## Instructions
1. Load the Stage 1/Stage 2 outputs for this harness, and only fall back to inspecting the raw image specimens per the Mandatory Specimen Inspection Rule above if those outputs are thin or missing.
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
# Library root resolves to ${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library} — confirm the
# actual value in your environment before exporting; do not hardcode a repo-relative path.
python -m cmf_builder.cli export --artifact-id <definition-artifact-id> --output "${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library}/<HARNESS_NAME>.zip"
```

---

## 5. Strict Naming Conventions & Export Rules

When exporting compiled harness packages to `${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library}`, enforce the 3-tier naming convention:

| Identity Layer | Format / Example | Purpose |
|---|---|---|
| **Cryptographic ID (`definition_id`)** | `atomic-harness-definition_7f0e70c1...` | Auto-generated by Builder (sha256 digest) to guarantee no collisions in database. |
| **Manifest Slug (`task_id`)** | `TWQ-STD-Standard` or `twq_std_standard_v1` | Human-readable slug in `manifest.json`. |
| **Library Package File (`package_file`)** | `TWQ-STD-Standard.zip` | Explicit `--output` filename saved to `${CA_HARNESS_LIBRARY_ROOT:-$CA_DATA_ROOT/harness-library}`. |
