# Phase 06 Start Here — Composition and Media Production Runtimes

Phase 6 implements a bounded, audited-Spec-guided composition and media runtime on top of the Phase 5 semantic-production baseline.

## Read first

1. `AGENTS.md`
2. `CURRENT_PROJECT_STATUS.md`
3. `README.md`
4. `docs/implementation/PHASE_06_IMPLEMENTATION_REPORT.md`
5. the controlling audited Specs:
   - `docs/tech-specs/TS-VID-001.md` through `TS-VID-006.md`
   - `docs/tech-specs/TS-STA-001.md`
   - `docs/tech-specs/TS-SPV-001.md`
   - `docs/tech-specs/TS-CAR-001.md`
   - `docs/tech-specs/TS-ANI-001.md`
   - `docs/tech-specs/TS-EVAL-001.md` through `TS-EVAL-003.md`
6. `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/PHASE_06_COMPOSITION_MEDIA_RUNTIME/`

## Implemented bounded core

- source-media registration and real `ffprobe` evidence;
- exact word-boundary EDL;
- canonical `VideoEditProgram` with one primary A-roll spine;
- actual local FFmpeg source-led MP4 render;
- Remotion and HyperFrames binding manifests;
- Composition IR, semantic BBOXes, hierarchy and Negative Space;
- PRETEXT-compatible deterministic reference measurement;
- optional real `skia-python` path plus an explicitly labeled reference rasterizer fallback;
- actual SuperVisual PNG;
- actual Carousel slide PNGs and PDF;
- actual reusable non-Format-02 animation-scene MP4;
- rendered cut evidence and static reparse;
- evaluator separation and hard-gate evaluation;
- responsible-layer diagnosis and bounded repair plans.

## Claim ceiling

`PHASE_06_COMPOSITION_MEDIA_RUNTIME_DEVELOPMENT_EVIDENCE`

No audited Spec is claimed fully complete. External Remotion/HyperFrames execution, certified independent visual judgment, complete Skia-worker proof, VAE Stage 5, Format 02, production readiness, and certification remain outside this phase.
