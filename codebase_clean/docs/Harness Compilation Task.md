# Harness Compilation Task

You are compiling the harness `CAR-LST-Olympics-4-5-10` into a production-valid `manifest.json` for the `cmf_builder` pipeline.

## Input Material
- **Harness reference material:** `atomic_harnesses_visual_syntax/carousels/CAR-LST-Olympics-4-5-10/` — raw image specimens, plus process docs `ONE_HARNESS_BUILD_PROMPT.md`, `DRILL_ME_FORMAT.md`, `DRILL_ME_BBOX_WHY.md`, `HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md`.
- **Compiled evidence (load this first):** `stage1_output/CAR-LST-Olympics-4-5-10_STAGE1_REPORT.json` and `stage1_output/specs/CAR-LST-Olympics-4-5-10_STAGE2_SPEC.json`.

## ⚠️ MANDATORY: Specimen Inspection Rule (Non-Negotiable)
Load the two files above first. Treat them as the verified, canonical evidence base for visual syntax and `wrong_reading_locks`. Only fall back to raw-image inspection if those reports are thin or missing.

## ⚠️ Critical Validator Rules (Must Follow)
1. `category_id`: `carousels`
2. `capability_requirements`: MUST be `[]` (empty) — non-empty breaks campaign-creation today (Blocker 2).
3. `input_contract.properties`: `identity_dna` is FORBIDDEN — belongs only in `activative_input.identity_dna_ref`.
4. `wrong_reading_locks`: non-empty, ≥3 format-specific locks, grounded in the actual Stage 1/2 observations for this harness — not generic.
5. `provenance_refs`: include `visual_syntax_composition_compiler@1.0.0`.
6. Slugs: `manifest_id: "operator-manifest-car-lst-olympics-4-5-10"`, `task_id: "car_lst_olympics_4_5_10_v1"`.

## Instructions
1. Execute the 5-step procedure from `ONE_HARNESS_BUILD_PROMPT.md`.
2. Stop after step 5 and report back — category, what's real vs. asked-about, and your `wrong_reading_locks` reasoning in one line. Wait for go-ahead before touching the CLI.