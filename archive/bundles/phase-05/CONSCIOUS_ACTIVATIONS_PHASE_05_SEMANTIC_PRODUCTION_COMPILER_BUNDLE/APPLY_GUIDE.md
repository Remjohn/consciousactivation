# Phase 5 Semantic Production Compiler Bundle — Apply Guide

Bundle ID: `CA-PHASE05-SEMANTIC-PRODUCTION-COMPILER-2026-07-24`

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
  --create-branch implementation/phase-05-semantic-production-compiler
```

## Apply, validate, and commit locally

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --create-branch implementation/phase-05-semantic-production-compiler `
  --commit
```

The script never pushes or merges.

## Roll back before committing

```powershell
python .\scripts\rollback_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

The bundle requires the exact Phase 4 baseline hashes recorded in `BASELINE_LOCK.json`.
Its maximum claim is `PHASE_05_SEMANTIC_PRODUCTION_COMPILER_DEVELOPMENT_EVIDENCE`.
