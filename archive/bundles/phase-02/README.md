# Conscious Activations Phase 2 — Activative Intelligence Runtime Core Bundle

Bundle ID: `CA-PHASE02-AIR-CORE-2026-07-23`

This bundle upgrades the Phase 1 AIR shell to a deterministic semantic runtime. It
preserves the Phase 1 shared contract spine and does not modify AHP, Interview
Expression, Studio, VAE, Delegation, Builder, or current constitutional authority.

## Apply

```powershell
python .\scripts\verify_bundle.py
python .\scripts\apply_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS --dry-run
python .\scripts\apply_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS --create-branch implementation/phase-02-air-core
```

Add `--commit` to create a local commit after validation. The script never pushes or
merges. Roll back with:

```powershell
python .\scripts\rollback_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

## Evidence boundary

Maximum claim: `AIR_PHASE_02_CORE_IMPLEMENTED_DEVELOPMENT_PASS`.

The bundle contains no external-model call, real-human evidence, media-production
runtime, VAE Stage 5 authorization, Format 02 activation, production readiness, or
certification claim.
