# Conscious Activations Phase 6 — Composition and Media Production Runtimes

Bundle ID: `CA-PHASE06-COMPOSITION-MEDIA-RUNTIMES-2026-07-24`

This bundle applies the bounded Phase 6 runtime to a repository that already
contains Phases 1–5. It is governed by the exact audited bytes of:

- `TS-VID-001` through `TS-VID-006`
- `TS-STA-001`
- `TS-SPV-001`
- `TS-CAR-001`
- `TS-ANI-001`
- `TS-EVAL-001` through `TS-EVAL-003`

The bundle produces actual local FFmpeg video, PNG, PDF, and non-Format-02
animation artifacts in its reference proof. It compiles Remotion and
HyperFrames bindings but does not claim those external runtimes executed. It
uses real `skia-python` when available; otherwise it emits an explicitly
non-production `SKIA_COMPATIBLE_REFERENCE_RASTERIZER` receipt.

## Commands

```powershell
python .\scripts\verify_bundle.py
python .\scripts\apply_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS --dry-run
python .\scripts\apply_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS --create-branch implementation/phase-06-composition-media-runtimes
python .\scripts\rollback_bundle.py --repo D:\Work\CONSCIOUS_ACTIVATIONS
```

The apply script verifies the Phase 5 baseline, applies replacement bytes
atomically, runs the Phase 1–6 regression and clean-install proof, and records a
rollback receipt. It never pushes or merges.
