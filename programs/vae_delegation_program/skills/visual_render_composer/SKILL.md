---
name: "visual_render_composer"
version: "1.0.0"
description: "Guides ComfyUI workflow graph compilation, multi-stage layer materialization, segmentation mask generation, and alpha matte extraction."
lanes:
  - "COMPOSER"
---

# Visual Render Composer Skill

## Role & Purpose
Orchestrates multi-stage visual rendering across segmentation, matting, GNM geometry references, and ComfyUI workflow graph execution without mutating canonical CAE state.

## Execution Rules
1. **Multi-Stage Binding**: Bind discrete stages (`stage:segmentation`, `stage:matting`, `stage:geometry-reference`, `stage:composition`).
2. **Deterministic Artifact Placement**: Store all candidate visual artifacts, mask cutouts, and geometry metadata in Content-Addressed Storage.
3. **Lineage Preservation**: Link generated candidate artifacts to the upstream production plan hash and demand request ID.
4. **No Direct Consumption Assertion**: Emit execution artifacts as evaluation candidates only.
