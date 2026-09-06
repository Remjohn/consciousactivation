# Module Map

**Artifact ID:** CAE-ART-MOD-001  
**Status:** APPROVED  
**Total Modules:** 4  
**Generated Date:** 2026-09-03T11:10:04.154265  

---

## 1. Package Namespaces and Public APIs

| Module Namespace | Root Directory | Public Symbols | Dependencies | Status |
|---|---|---|---|---|
| `cae_world_intelligence` | `services/world-intelligence/src/cae_world_intelligence/` | ResearchSignal, WorldSignalProvenanceVerifier, NormalizationPipeline | typing, pydantic, datetime | `ACTIVE` |
| `cmf_pipeline.workflow` | `services/pipeline/src/cmf_pipeline/workflow/` | WorkflowCompiler, WorkflowRunService, DeterministicStepScheduler | ca_runtime, typing, pathlib | `ACTIVE` |
| `ca_runtime` | `packages/ca_runtime/src/ca_runtime/` | AgentInvocationContract, ProgramStateRuntime, CASMutationEngine | typing, json, asyncio | `ACTIVE` |
| `caebmad_rebuild_tools` | `docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/` | validate_rebuild, investigate_operating_levels, reconstruct_product_lineage | yaml, json, pathlib, pytest | `ACTIVE` |

---

## 2. Dependency Graph Summary

Clean acyclic module hierarchy: packages/ca_runtime serves as foundational leaf dependency consumed by services/pipeline and services/world-intelligence.
- **Circular Dependencies Detected:** `NO`
