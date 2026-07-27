# Phase 9 Final Bundle Application Guide

## Prerequisites

The repository must already contain Phases 1–8 and match `BASELINE_LOCK.json`.

Required local tools:

- Python 3.12 or later;
- Git for branch/commit options;
- Node.js, npm and TypeScript compiler;
- FFmpeg and ffprobe.

## Verify

```powershell
python .\scripts\verify_bundle.py
```

Expected:

```text
result: PASS
operation_count: 112
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
  --create-branch implementation/phase-09-final-application
```

## Apply, validate and commit locally

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS `
  --create-branch implementation/phase-09-final-application `
  --commit
```

The script never pushes or merges.

## Rollback before committing

```powershell
python .\scripts\rollback_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

## Post-application validation

The application script runs the Phase 9 clean-install validator followed by the complete Phase 9 validator. These checks may take substantial time because the complete Phase 1–8 regression and media reference paths are included.
