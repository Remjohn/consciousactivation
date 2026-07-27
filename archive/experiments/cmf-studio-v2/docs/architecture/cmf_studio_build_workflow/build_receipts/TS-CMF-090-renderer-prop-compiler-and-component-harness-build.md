---
title: "TS-CMF-090 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-090-renderer-prop-compiler-and-component-harness.md"
---

# TS-CMF-090 Build Receipt

Implemented renderer prop compiler contracts through `RendererComponentRegistration`, `RendererPropsManifest`, `RendererComponentCompatibilityReport`, `RendererPropsCompilationReceipt`, and `compile_renderer_props`. The compiler checks format compatibility, sandbox policy, deterministic hash, and locked asset policy refs.

Verification: `test_batch1_ideogram_layer_extraction_and_renderer_props_stay_downstream_deterministic`.

