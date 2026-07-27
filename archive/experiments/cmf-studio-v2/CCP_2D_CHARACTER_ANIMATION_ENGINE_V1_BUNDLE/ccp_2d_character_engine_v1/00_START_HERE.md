# CCP 2D Character Animation Engine — Agent Start Here

## Purpose

This bundle is the canonical implementation context for a production-grade, JSON-driven 2D character animation engine inside CCP Studio / Conscious Media Factory.

The engine does **not** accept loose prompts as its primary input. It compiles a deterministic performance program from pinned, structured context:

- Brand Context Version;
- Interview Brief;
- Interview Asset Contract;
- Transcript Beat Map;
- Expression Moments;
- Voice DNA and Visual DNA;
- Primitive evaluations;
- Doctrines and Negative Space;
- Asset Package Specification;
- approved Character Identity Pack;
- approved 64-state Acting Library;
- approved Character Rig Version;
- scene template;
- format target.

The canonical runtime artifact is `TwoDCharacterProgram`. All renderers consume it. No provider is allowed to invent production behavior during final rendering.

## Binding architecture decisions

1. **Python is the semantic runtime.** Pydantic contracts, DSPy programs, Pi orchestration, evaluation, state machines, provider adapters, and receipts live in Python.
2. **TypeScript is a rendering consumer.** Motion Canvas, Remotion, and browser previews consume generated TypeScript types derived from Pydantic schemas.
3. **Character creation and performance compilation are separate lifecycles.** Character Genesis is occasional and approval-heavy; performance compilation happens per asset.
4. **Generative output must be promoted into an approved version before production.** No image model, decomposition model, or LLM runs inside the final deterministic render.
5. **Time is represented as integer ticks.** Floating-point seconds are never the source of truth.
6. **The operator is the final approval authority.** Automatic repair may propose or generate candidates, but publication requires an approved receipt.
7. **The character remains brand-owned and versioned.** Every output pins identity, art, layered asset, rig, performance library, materials, costume, props, and Micro-Semiotic Anchors.

## Recommended reading order

1. `01_MASTER_SPEC.md`
2. `02_PIPELINE_AND_PROVIDER_ROLES.md`
3. `03_RIGGING_AND_ASSET_CONTRACTS.md`
4. `04_PERFORMANCE_COMPILER.md`
5. `05_RENDERING_AND_REPRODUCIBILITY.md`
6. `06_EVALS_APPROVAL_AND_REPAIR.md`
7. `models/two_d_character_models.py`
8. `examples/example_two_d_character_program.json`

## Definition of done

The engine is production-ready only when it can:

- ingest an approved layered character package;
- compile a full `TwoDCharacterProgram` from structured interview context;
- render the same approved program reproducibly;
- preserve identity and materiality across scenes;
- synchronize mouth, gesture, gaze, props, subtitles, and audio to the canonical timebase;
- produce rig, blocking, and final previews;
- run automatic evaluations;
- accept typed operator repair commands;
- create an immutable final render receipt.
