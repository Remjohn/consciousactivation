---
okf_version: "0.1"
cmf_profile: "cmf-okf-visual-memory-1.0"
type: Workflow Capability Profile
id: WORKFLOW-F02-CHAR-SCENE
version: 0.1.0-example
lifecycle_status: represented
authority_class: registry_projection
title: Format 02 character scene workflow
description: Planned ComfyUI capability profile for identity-, pose-, expression-, and composition-controlled Minimal Coach Theatre assets.
tags: [format02, comfyui, character, identity, pose]
asset_families: [human_character_assets]
syntax_roles: [guide_character, listener_reaction, active_demonstration]
source_record_refs:
  - registry://visual-capabilities/comfy-format02-character-prod
typed_edges:
  known_failure:
    - ../failure-patterns/weak-visible-action.md
  compatible_with:
    - ../steering-recipes/character-visible-action.md
content_hash: EXAMPLE_HASH_PENDING_ARCHITECTURE
---

# Required capabilities

- Character identity conditioning
- Pose and expression control
- Regional conditioning
- Transparent subject extraction
- Composition simulation
- Independent VLM evaluation

# Release status

This concept is structurally represented in the PRD. Architecture and benchmark evidence are required before a production workflow profile exists.
