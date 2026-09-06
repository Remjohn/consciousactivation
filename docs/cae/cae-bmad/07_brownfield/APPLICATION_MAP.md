# Application Map

**Artifact ID:** CAE-ART-APP-001  
**Status:** APPROVED  
**Total Services:** 5  
**Generated Date:** 2026-09-03T11:07:50.415897  

---

## 1. Deployable Services & Runtimes

| Service ID | Name | Directory Path | Entrypoint | Type | Status |
|---|---|---|---|---|---|
| `SVC-WORLD-INTEL` | World Intelligence Service | `services/world-intelligence/` | `services/world-intelligence/src/cae_world_intelligence/domain.py` | `MICROSERVICE` | `ACTIVE` |
| `SVC-PIPELINE` | CMF Workflow Pipeline Runtime | `services/pipeline/` | `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py` | `PIPELINE_RUNTIME` | `ACTIVE` |
| `SVC-BUILDER` | Service Builder Engine | `services/builder/` | `services/builder/main.py` | `MICROSERVICE` | `STANDALONE` |
| `SVC-DELEGATION` | Task Delegation Daemon | `services/delegation/` | `services/delegation/worker.py` | `DAEMON_WORKER` | `STANDALONE` |
| `SVC-CA-RUNTIME` | Conscious Activation Core Runtime Package | `packages/ca_runtime/` | `packages/ca_runtime/src/ca_runtime/agent_invocation.py` | `LIBRARY_PACKAGE` | `ACTIVE` |

---

## 2. Runtime Dependencies

- Python >= 3.11
- PyYAML >= 6.0
- jsonschema >= 4.20
- pytest >= 8.0

---

## 3. Health Summary

All 5 core microservices and runtime packages have verified entrypoints on disk and satisfy constitutional contracts.
