# Lane F — VAE GNM Main-Avatar Expression Reference Tool

## Product owner

```yaml
product_owner: Visual Asset Editor
pipeline_core_owner: false
interview_expression_owner: false
```

## Exclusive target paths

```text
02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/avatar/**
02_VISUAL_ASSET_EDITOR/src/cmf_vae/application/avatar_expression/**
02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/gnm/**
02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/comfyui/gnm/**
02_VISUAL_ASSET_EDITOR/comfyui/workflows/gnm_avatar_expression_reference_v1.json
02_VISUAL_ASSET_EDITOR/comfyui/workflows/gnm_avatar_expression_edit_v1.json
02_VISUAL_ASSET_EDITOR/tests/stage5/gnm/**
```

Package exports, shared VAE contracts, dependency files, and status surfaces require
integrator requests.

## Upstream repository

```text
Remjohn/GNM/
  gnm/shape/gnm_numpy.py
  gnm/shape/gnm_pytorch.py
  gnm/shape/semantic_sampler.py
  gnm/shape/gnm_data_schema.py
  gnm/shape/visualization/**
  gnm/shape/fitting_utils/**
```

## Deliver

- Pinned GNM source, model-data, and license identities.
- Isolated GNM worker using one approved backend.
- Main-avatar identity geometry profile from approved references or an explicitly
  approved temporary development profile.
- Typed avatar expression reference request and result.
- Deterministic semantic-expression blend, pose, gaze, camera, and seed handling.
- GNM mesh generation and OBJ or GLB export.
- Front, three-quarter, and profile reference renders.
- Depth, normal, silhouette, landmark, and semantic-mask outputs where supported.
- `gnm_avatar_expression_reference_v1` ComfyUI workflow.
- `gnm_avatar_expression_edit_v1` ComfyUI workflow.
- VAE Asset Result and execution receipt mapping.
- At least five controlled expression examples for the main avatar.

## Do not do

- Do not import GNM into Interview Expression.
- Do not place GNM under Pipeline core.
- Do not use demographic semantic identity sampling as the main-avatar identity.
- Do not treat GNM geometry as identity meaning or emotional truth.
- Do not train a model before the deterministic baseline is measured.
- Do not emit an unconstrained full expression vector from language.

## Future Programmed Model experiment

Prepare an experiment package, but do not make it launch-critical:

```text
desired avatar expression
→ named GNM controls and bounded residual
→ deterministic GNM compiler
→ multiview reference pack
→ ComfyUI realization
→ independent evaluation
```
