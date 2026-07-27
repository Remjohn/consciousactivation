# Phase 6 Bundle Application Guide

## Prerequisites

- Phases 1–5 are applied.
- Python 3.12 or newer is available.
- `ffmpeg` and `ffprobe` are available on `PATH` for the actual media proof.
- The Git worktree is clean unless `--allow-dirty` is explicitly used.
- Extract this bundle outside the repository.

No font files are bundled. The validated reference rasterizer uses its embedded
minimal glyph program. A pinned production font and shaping adapter remain a
later gap.

## Verify

```powershell
python .\scripts\verify_bundle.py
```

## Dry run

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --dry-run
```

## Apply on a branch

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --create-branch implementation/phase-06-composition-media-runtimes
```

## Apply, validate, and commit locally

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --create-branch implementation/phase-06-composition-media-runtimes `
  --commit
```

The script never pushes or merges.

## Roll back before committing

```powershell
python .\scripts\rollback_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

## Claim boundary

`PHASE_06_COMPOSITION_MEDIA_RUNTIME_DEVELOPMENT_EVIDENCE`

No governing Spec is marked fully complete. Remotion/HyperFrames execution,
certified independent visual judgment, complete Skia-worker proof, VAE Stage 5,
Format 02, production readiness, and certification remain false.
