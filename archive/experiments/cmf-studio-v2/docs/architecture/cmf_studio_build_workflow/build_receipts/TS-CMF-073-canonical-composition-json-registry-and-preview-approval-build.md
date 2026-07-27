---
title: "TS-CMF-073 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md"
---

# TS-CMF-073 Build Receipt

Implemented canonical composition JSON through `CompositionTemplateJson`, `CompositionZone`, `CompositionTemplateLayer`, `CompositionTemplateApprovalReceipt`, and `CompositionRuntimeService.register_composition_template_json`. Preview refs are stored as evidence only; `composition_json_hash` is the source of truth for approval and renderer handoff.

Verification: `test_batch1_scene_binding_and_composition_json_are_canonical_and_primitive_gated`.

