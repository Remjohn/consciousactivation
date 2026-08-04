# Harness Authoring Master Prompts & Execution Guide

**Version:** 1.0.0  
**Status:** RATIFIED_AUTHORING_GUIDE  
**Target Repository:** `consciousactivation`  
**Location of Raw Harness Bundles:** `atomic_harnesses_visual_syntax/`  
**Location of Output Library:** `storage/harness-library/`  

---

## 1. Overview

This document provides the master prompt template and execution instructions for compiling raw visual harness bundles into production-ready `operator_manifest.json` definitions.

Because all 72+ raw harness bundles and their spec files reside directly inside the repository at `atomic_harnesses_visual_syntax/`, you do **not** need to upload individual zip files. Simply reference the repository path in your Claude chat sessions.

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
# Harness Compilation Task — Repo-Grounded Execution

You are compiling a raw visual harness bundle into a production-valid `operator_manifest.json` for the `cmf_builder` pipeline inside the `consciousactivation` repository.

## Target Harness
- Target directory in repo: `atomic_harnesses_visual_syntax/<category>/<HARNESS_NAME>/`

## Source Files inside the Target Directory
1. `ONE_HARNESS_BUILD_PROMPT.md` — Procedure & task guidelines.
2. `HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md` — Gap analysis & compilation skill.
3. `DRILL_ME_FORMAT.md` — Format purpose, boundaries, and native primitives.
4. `DRILL_ME_BBOX_WHY.md` — Component geometry & attention path rules.
5. Visual Specimen (`.png` if present) — Visual layout reference.

## Governance & Reference Files in Codebase
- Governance Constitution: `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`
- Reference Working Manifest: `services/builder/tests/fixtures/productization/manifests/activative_expression.json`
- Schema Definition: `services/builder/src/cmf_builder/domain/operator_manifest.py`

## ⚠️ Critical Validator Gotchas (Must Follow)
1. `capability_requirements` MUST be a non-empty list — use `["activative_contract_validation"]`. Setting `[]` will fail ingest.
2. `identity_dna` is FORBIDDEN in `input_contract.properties` — it belongs exclusively in `activative_input.identity_dna_ref`. Use `voice_context` or `source_expression_moment` for runtime input properties.
3. `wrong_reading_locks` MUST be a non-empty list — provide at least 3 format-specific negative constraints derived from the visual specimen and DRILL_ME files.
4. No licensing or rights bots — do not invent rights analysis layers.
5. `category_id` MUST be exactly one of: `supervisuals`, `carousels`, `short_form_edited_video`, `2d_character_animation`, or `conversational_activation_expression`.

## Instructions
Please analyze the target harness directory, execute the 5-step classification & synthesis procedure from `ONE_HARNESS_BUILD_PROMPT.md`, and produce the complete, un-truncated `manifest.json`.
```

---

## 4. CLI Execution & Pipeline Build Commands

Once a `manifest.json` is written for a harness, run the 4-step build sequence in your terminal to ingest, build, inspect, and export the built harness definition:

```bash
# Step 1: Ingest manifest (validates schema & governance gates)
cd services/builder
python -m cmf_builder.cli ingest "path/to/manifest.json"
# → Output returns: artifact_id (e.g., operator-manifest-twq-std-standard)

# Step 2: Build harness definition
python -m cmf_builder.cli build --artifact-id <operator-manifest-id>
# → Output returns: artifact_id (e.g., atomic-harness-definition_7f0e70c1...)

# Step 3: Inspect definition (sanity check)
python -m cmf_builder.cli inspect --artifact-id <definition-artifact-id>

# Step 4: Export zip package to Harness Library (ALWAYS specify explicit --output path)
python -m cmf_builder.cli export --artifact-id <definition-artifact-id> --output "../../storage/harness-library/<HARNESS_NAME>.zip"
```

## 4.1 Strict Naming Conventions & Export Rules

When exporting compiled harness packages to `storage/harness-library/`, you must enforce the 3-tier naming convention:

| Identity Layer | Format / Example | Purpose |
|---|---|---|
| **Cryptographic ID (`definition_id`)** | `atomic-harness-definition_7f0e70c1...` | Auto-generated by Builder (sha256 digest) to guarantee no collisions in database. |
| **Manifest Slug (`task_id`)** | `TWQ-STD-Standard` or `twq_std_standard_v1` | Human-readable slug in `manifest.json`. |
| **Library Package File (`package_file`)** | `TWQ-STD-Standard.zip` | Explicit `--output` filename saved to `storage/harness-library/`. |

### 🚨 Critical Export Rule
- **NEVER** export packages using default sha256 names like `atomic-harness-definition_<hash>.zip`.
- **ALWAYS** pass `--output "../../storage/harness-library/<HARNESS_NAME>.zip"` during step 4 export.
- **NEVER** leave leftover build zips inside `atomic_harnesses_visual_syntax/` source folders. The source directory contains only raw input specs and media specimens.

---

## 5. Verification Gate

Verify that the newly built harness is visible in the Harness Library API:

```bash
python -c "import zipfile, json; z = zipfile.ZipFile('storage/harness-library/<HARNESS_NAME>.zip'); print(json.dumps(json.loads(z.read('atomic_harness_definition.json')), indent=2))"
```

A valid build will show `category_binding.category_id`, `wrong_reading_locks`, and non-empty `semantic_lineage_refs`.
