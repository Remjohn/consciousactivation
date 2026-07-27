---
title: "TS-CMF-076 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md"
---

# TS-CMF-076 Build Receipt

Implemented open-source adapter evaluation through `IntegrationCandidate`, `IntegrationAdapterDecision`, `CompositionRuntimeService.register_integration_candidate`, and `run_integration_fit_eval`. Fit checks score deterministic boundary, license fit, contractability, sandboxability, and production authority, with direct authority blocked.

Verification: `test_batch1_open_source_adapters_eval_conversion_and_operator_approval_are_sandboxed`.

