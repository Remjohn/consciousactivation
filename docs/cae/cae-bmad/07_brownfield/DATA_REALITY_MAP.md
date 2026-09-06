# Data Reality Map

**Artifact ID:** CAE-ART-DRM-001  
**Status:** APPROVED  
**Total Entities:** 4  
**Generated Date:** 2026-09-03T11:10:04.152269  

---

## 1. Data Entities and Models

| Entity Name | Storage Engine | Model File | Key Fields | Status |
|---|---|---|---|---|
| `ResearchSignal` | `IN_MEMORY_CAS` | `services/world-intelligence/src/cae_world_intelligence/domain.py` | signal_id, source_url, content, relevance_score, timestamp | `ACTIVE` |
| `ProgramStateAggregate` | `IN_MEMORY_CAS` | `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | program_id, current_state, cas_version, state_history | `ACTIVE` |
| `CompiledWorkflowStep` | `FILESYSTEM_YAML` | `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py` | step_id, agent_binding, input_schema, output_schema | `ACTIVE` |
| `EvidenceReceipt` | `FILESYSTEM_YAML` | `docs/cae/constitutions/CA-CAN-01C_RECEIPT.yaml` | receipt_id, source_hash, signature, verified_at | `ACTIVE` |

---

## 2. Canonical State Alignments

| Constitution Ref | State Model | Verified Valid |
|---|---|---|
| `CA-CAN-02_STATE_AGGREGATE.yaml` | `ProgramStateAggregate` | YES |
| `CA-CAN-01C_RECEIPT.yaml` | `EvidenceReceipt` | YES |
| `CA-CAN-01B_EVIDENCE_SOURCE.yaml` | `ResearchSignal` | YES |
