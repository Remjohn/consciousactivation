# Apply Guide — Phase 1–3 Traceability and Gap Closure

Apply this bundle only after Phase 3 has been applied.

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

## Apply and validate

```powershell
python .\scripts\apply_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

The application validates Phase 1, Phase 2, Phase 3, and traceability tests with `ResourceWarning` promoted to an error.

## Rollback

```powershell
python .\scripts\rollback_bundle.py `
  --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

## Result

This bundle does not mark any affected Tech Spec fully complete. It creates exact matrices and per-Spec assessments, fixes SQLite connection lifecycle leaks, and bounds Phase 1–3 claims to core-subset development evidence.
