---
title: "TS-CMF-128 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 3"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-128-render-runtime-selection-and-locking.md"
---

# TS-CMF-128 Build Receipt

Implemented `RenderRuntimeCandidate`, `RenderRuntimeSelectionRequest`, `RenderRuntimeLock`, and `RenderRuntimeDriftReceipt` so deterministic runtime selection is locked before final render and drift blocks release.

Verification: `test_batch3_provider_workspace_footage_and_runtime_locking_are_governed`.
