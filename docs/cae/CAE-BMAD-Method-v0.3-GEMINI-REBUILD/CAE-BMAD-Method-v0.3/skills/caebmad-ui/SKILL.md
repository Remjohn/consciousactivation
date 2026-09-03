---
name: caebmad-ui
description: Designs operator interfaces, visual telemetry monitors, interaction flows, and Atomic Harness design token mappings.
version: 0.3.0-rebuild
agent: cae-ux-agent
---

# Skill: caebmad-ui

## 1. Purpose & Invocation
The `caebmad-ui` skill enables the `cae-ux-agent` to author, validate, and maintain operator studio UI/UX specifications at `Level 01: PRODUCT / INTENT` and `Level 07: APPLICATION`.

## 2. Invocation Preconditions
1. Product Brief and Architecture specifications available.
2. Atomic Harness design token references accessible.
3. Schema `schemas/ui_ux_spec.schema.json` loaded.

## 3. Execution Logic
1. **Operator View Design:** Detail studio workspace layouts (Interview Telemetry, Signal Provenance, Storyboard Assembly).
2. **Atomic Harness Token Binding:** Bind color palettes, typography, and telemetry badges to formal design tokens.
3. **Interaction Flow Mapping:** Detail keyboard navigation, error modals, and step transitions.
4. **Deliverable Emission:** Assemble `docs/cae-bmad/06_ui_ux/UI_UX_SPECIFICATION.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/06_ui_ux/UI_UX_SPECIFICATION.json`
- `docs/cae-bmad/06_ui_ux/UI_UX_SPECIFICATION.md`
