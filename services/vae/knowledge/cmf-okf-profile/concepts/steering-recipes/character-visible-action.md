---
okf_version: "0.1"
cmf_profile: "cmf-okf-visual-memory-1.0"
type: Visual Steering Recipe
id: STEER-CHAR-ACTION-007
version: 1.0.0-example
lifecycle_status: experimental
authority_class: derived_validated_knowledge
title: Strengthening visible comparative character actions
description: Steering intervention for character scenes where an intended hand or object interaction is visually ambiguous.
tags: [format02, character, pose, visible-action, repair]
asset_families: [human_character_assets]
failure_codes: [WEAK_VISIBLE_ACTION]
syntax_roles: [active_demonstration, comparative_selection]
workflow_profiles: [comfy-format02-character-prod]
source_record_refs:
  - visual-memory://production-runs/RUN-EXAMPLE-0182
typed_edges:
  derived_from:
    - ../failure-patterns/weak-visible-action.md
  compatible_with:
    - ../workflows/format02-character-scene.md
content_hash: EXAMPLE_HASH_PENDING_ARCHITECTURE
---

# Intervention

Increase pose-control strength inside the validated envelope and apply regional conditioning to the hands and interaction object.

# Preserve

- Character identity
- Authorized expression
- Camera direction
- Composition role
- Sequence palette

# Do not apply when

- The syntax role is passive reaction.
- Hands are intentionally hidden.
- Gaze rather than gesture carries the interaction.

# Evidence status

This is a PRD-level example. It is not production knowledge until controlled comparisons, benchmark evidence, shadow routing, and promotion have occurred.
