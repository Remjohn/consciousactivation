---
name: derivative_composition_compiler
description: Compiles typed CompositionIR and triggers physical rendering passes for visual derivatives.
version: 1.0.0
lane: COMPOSER
---

# Derivative Composition Compiler Skill

## Role
Passive, flat skill executed within the `COMPOSER` authority lane.
Compiles `CompositionIR` data structures (pages, bounding boxes, negative spaces, pretext measurements) and executes real rendering engines (`CarouselService`, `SuperVisualService`, `AnimationSceneRealizer`).

## Invariants
- Enforces strict geometry non-overlap and text measurement fits.
- Encapsulates physical rendering execution without side effects outside designated directories.
- Zero sub-skill execution.
