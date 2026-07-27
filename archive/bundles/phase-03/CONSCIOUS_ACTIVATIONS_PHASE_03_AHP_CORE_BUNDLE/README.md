# Conscious Activations Phase 3 — Atomic Harness Pipeline Core Bundle

Bundle ID: `CA-PHASE03-AHP-CORE-2026-07-23`

This deterministic bundle upgrades a validated Phase 2 repository into the Phase 3 Atomic Harness Pipeline execution kernel.

## Verify

```bash
python scripts/verify_bundle.py
```

## Dry run

```powershell
python .\scripts\apply_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS --dry-run
```

## Apply and validate

```powershell
python .\scripts\apply_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS --create-branch implementation/phase-03-ahp-core
```

The script never pushes or merges. Production authorization and certification remain false.
