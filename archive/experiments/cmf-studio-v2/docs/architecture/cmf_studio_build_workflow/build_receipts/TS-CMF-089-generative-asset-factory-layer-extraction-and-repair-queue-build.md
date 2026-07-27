---
title: "TS-CMF-089 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md"
---

# TS-CMF-089 Build Receipt

Implemented generative asset factory and layer extraction contracts through `GenerativeAssetFactoryJob`, `QwenLayeredDecompositionReceipt`, `SAM3SaliencyReceipt`, `LayerManifestEntry`, `LayerExtractionResult`, `RepairJobReceipt`, and `extract_layers`. The factory records provider boundaries and deterministic downstream ownership.

Verification: `test_batch1_ideogram_layer_extraction_and_renderer_props_stay_downstream_deterministic`.

