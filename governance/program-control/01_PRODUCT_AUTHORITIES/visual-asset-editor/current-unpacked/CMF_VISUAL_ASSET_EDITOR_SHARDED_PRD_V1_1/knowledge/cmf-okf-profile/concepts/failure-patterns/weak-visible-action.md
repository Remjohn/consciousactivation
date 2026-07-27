---
okf_version: "0.1"
cmf_profile: "cmf-okf-visual-memory-1.0"
type: Visual Failure Pattern
id: FAIL-WEAK-VISIBLE-ACTION
version: 1.0.0-example
lifecycle_status: experimental
authority_class: derived_observation
title: Weak visible action
description: The asset contains the intended subjects but their action or relationship is not immediately legible.
tags: [failure, composition, character, action]
asset_families: [human_character_assets]
failure_codes: [WEAK_VISIBLE_ACTION]
source_record_refs:
  - benchmark://VAE-R1-FORMAT02-BENCHMARK/B03
typed_edges:
  repaired_by:
    - ../steering-recipes/character-visible-action.md
  observed_in:
    - ../workflows/format02-character-scene.md
content_hash: EXAMPLE_HASH_PENDING_ARCHITECTURE
---

# Detection

The independent VLM can identify the intended entities but cannot state the action confidently from the asset or rendered composition.

# Common causes

- Pose control is too weak.
- The interaction object is too small or occluded.
- Hand geometry is ambiguous.
- The camera crop hides the causal relationship.
- The prompt names the action without exposing it visually.

# Repair ownership

The responsible layer is usually pose, regional conditioning, object visibility, or composition geometry—not semantic intent.
