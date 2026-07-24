# Phase 8 Bundle Application Guide

## Prerequisites

The repository must already contain Phases 1–7 and match the exact governing Spec and RC4 hashes in `BASELINE_LOCK.json`.

Required local tools:

- Python 3.12 or later;
- Git for branch/commit options;
- Node.js, npm and TypeScript compiler;
- FFmpeg and ffprobe.

## Verify the bundle

```powershell
python .\scripts\verify_bundle.py
```

Expected:

```text
result: PASS
operation_count: 117
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
  --create-branch implementation/phase-08-delegation-vae
```

## Apply, validate and create a local commit

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --create-branch implementation/phase-08-delegation-vae `
  --commit
```

The script never pushes or merges.

## Rollback before committing

```powershell
python .\scripts\rollback_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

## Validation performed after application

- complete Phase 1–8 regression;
- exact RC4 release and two-copy identity checks;
- Delegation validator and protocol suites;
- VAE schema export and package-data sync;
- clean isolated installation of seven Python packages;
- actual local reference PNG, Asset Result, acknowledgement, Control Tower and OKF projection;
- Phase 8 traceability checks.
