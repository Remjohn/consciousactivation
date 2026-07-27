# Phase 07 Bundle Application Guide

Extract the bundle outside the Conscious Activations repository.

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

## Apply on a dedicated branch

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --create-branch implementation/phase-07-studio-supervision
```

## Apply, validate and commit locally

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --create-branch implementation/phase-07-studio-supervision `
  --commit
```

The script never pushes or merges.

## Rollback before committing

```powershell
python .\scripts\rollback_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

## Runtime requirements

- Python 3.12+ or separately validated compatible version
- Node.js and npm
- TypeScript compiler (`tsc`)
- FFmpeg and ffprobe, because the Phase 6 regression remains part of the apply validation
