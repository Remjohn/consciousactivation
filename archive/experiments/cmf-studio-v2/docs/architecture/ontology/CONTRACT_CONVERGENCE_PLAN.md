# Contract Convergence Plan V1

## Goal

Converge the existing codebase, prior bundles, visual/motion skills, and methodology docs into a single canonical contract system.

## Strategy

Use a strangler-refactor approach:

```text
Keep existing working harness.
Create canonical V2 ontology/contracts.
Wrap old V1 contracts with adapters.
Move components one by one to V2.
Deprecate old duplicate objects after tests pass.
```

## Wave 1 — Ontology kernel

Create or formalize:

```text
contracts/ontology.py
contracts/primitive_coalition.py
contracts/source_reference.py
contracts/frame_profiles.py
contracts/style_routes.py
```

## Wave 2 — Research and ingredient contracts

Create or formalize:

```text
contracts/visual_schema.py
contracts/visual_ingredient.py
contracts/creative_ingredient.py
contracts/asset_intelligence.py
contracts/paper_cut_artifact.py
```

## Wave 3 — Component contracts

Split or enrich:

```text
contracts/supervisual.py
contracts/carousel.py
contracts/video_editing.py
contracts/two_d_character.py
contracts/sequence.py
```

## Wave 4 — Receipt contracts

Unify:

```text
contracts/evaluation_receipts.py
contracts/composition_decision.py
contracts/provider_jobs.py
contracts/render_receipts.py
contracts/usage_receipts.py
```

## Wave 5 — Compatibility adapters

For every old contract:

```text
V1 → V2 converter
V2 → existing service projection
deprecation notice
test coverage
```

## Immediate high-risk convergence areas

1. `PrimitiveTriadContract` → `PrimitiveCoalitionContract`.
2. `asset_program_compilers.py` → split domain modules.
3. `StillVisualCompositionProgram` → lower-level runtime under SuperVisual/SingleImage.
4. `VisualResearchQuery` → search primitive under Visual Schema pipeline.
5. `VideoEditProgram` → enrich into VideoEditingProgram V2.
6. `16:9` output assumptions → source-only for short-form delivery.
