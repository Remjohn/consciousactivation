# Lane D — Visual Asset Editor Stage 5 Core and Visual Providers

## Exclusive target paths

Lane D owns VAE Stage 5 core except the GNM paths reserved for Lane F.

```text
02_VISUAL_ASSET_EDITOR/src/cmf_vae/**
02_VISUAL_ASSET_EDITOR/tests/stage5/**
02_VISUAL_ASSET_EDITOR/docs/implementation/stage5/**
```

Exclusions:

```text
02_VISUAL_ASSET_EDITOR/src/cmf_vae/domain/avatar/**
02_VISUAL_ASSET_EDITOR/src/cmf_vae/application/avatar_expression/**
02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/gnm/**
02_VISUAL_ASSET_EDITOR/src/cmf_vae/adapters/comfyui/gnm/**
02_VISUAL_ASSET_EDITOR/comfyui/workflows/gnm_*
02_VISUAL_ASSET_EDITOR/tests/stage5/gnm/**
```

Shared contracts, package exports, dependency files, source registries, and status
surfaces require integrator requests.

## Deliver

- Implement all dependency-ready existing VAE Stories under the live local story plan.
- Visual Asset Demand intake.
- Visual Production Plan IR.
- Durable asset, version, and lineage state.
- Local worker and fake-provider boundary.
- Real SAM3 adapter for semantic segmentation or tracking when runtime permits.
- Real Lucida adapter for alpha matting and background removal.
- Capability-specific provider routing and benchmark fixtures.
- Pipeline-compatible Asset Result.
- Real artifact hashes; fake outputs remain development-only and cannot pass release.
- Stable VAE ports that Lane F can use for GNM request, result, storage, and evaluation.

## Lane F integration boundary

Lane F owns the GNM and GNM-specific ComfyUI implementation.

Lane D supplies only the stable VAE interfaces needed by that implementation:

```text
Visual Production Plan
Asset Store
Worker Runtime
Evaluation Port
Asset Result
Execution Receipt
```

Lane D must not duplicate GNM code.
