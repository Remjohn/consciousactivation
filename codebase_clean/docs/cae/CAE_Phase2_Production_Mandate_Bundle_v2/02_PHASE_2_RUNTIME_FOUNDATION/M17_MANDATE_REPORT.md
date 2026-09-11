# CAE Phase 2 Mandate M17 — Workflow + Capability Metadata Bridge Report

**Mandate ID:** CAE M17  
**Subsystem:** Runtime Foundation / Metadata Resolution Bridge  
**Authority Reference:** `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`  
**Execution Date:** August 31, 2026  
**Status:** COMPLETED & VERIFIED  

---

## 1. Executive Summary

Mandate M17 eliminates the empty placeholder dictionary path in the atomic harness intake compiler (`compile_portable_to_intake()`) and connects workflow and capability metadata to governed existing sources. Prior to M17, compilation of atomic harnesses lacked authoritative resolution for required capability metadata, execution workflow DAGs, versioned semantic lineage, and evaluation/repair contracts, causing calls to fail or bypass governance.

Under M17, the `WorkflowCapabilityMetadataBridge` (`packages/ca_runtime/src/ca_runtime/metadata_bridge.py`) was introduced as the canonical source/transform bridge. It resolves:
1. **Governed Capability Metadata:** Resolves metadata across a 5-level precedence hierarchy: explicit caller overrides &rarr; `ImplementationEligibilityRegistry` &rarr; `ProgrammedModelRegistry` &rarr; harness definition embeddings &rarr; `GOVERNED_BASELINE_CAPABILITIES`. Fails closed with `TS-APP-BRIDGE-001#blocker-2` if any required capability remains unresolved.
2. **Deterministic Workflow DAG:** Derives and validates workflow nodes and edges mapped strictly to the four CAE Authority Lanes (`HUNTER`, `ANALYST`, `COMPOSER`, `COMMANDER`), valid `NodeKind` actors (`DETERMINISTIC_MODULE`, `GOVERNED_AGENT_TEAM`, `HUMAN_OPERATOR_GATE`), and `ProductBoundary`. Fails closed with `TS-APP-BRIDGE-001#blocker-5` if workflow is missing or contains lane bypasses.
3. **Semantic Lineage Dependencies:** Resolves versioned, content-addressed digests (`sha256:...`) from category bindings, provenance refs, and AIR script dependencies. Fails closed with `TS-APP-BRIDGE-001#blocker-1` on unversioned/unhashed references.
4. **Evaluation and Repair Laws:** Resolves evaluation contracts and repair policies fail-closed with `TS-APP-BRIDGE-001#blocker-6`.
5. **Campaign Router Integration:** Connects the API campaign creation endpoint (`api/routers/campaigns.py`) to the governed bridge, dynamically recording `BRIDGE_SUCCEEDED` or `BRIDGE_BLOCKED` diagnostics.

---

## 2. Authority & Code Inspection Baseline

### Authority Read Set
- `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
- `00_CONTROL/14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md`
- `00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md`
- `00_CONTROL/22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md`
- `00_CONTROL/27_PHASE2_CONTEXT_BUDGET_CONTRACT.md`
- `docs/PRD/CURRENT.md` (Runtime blockers and TS-APP-BRIDGE-001 specification)
- `CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`

### Source Files Inspected & Modified
1. `packages/ca_runtime/src/ca_runtime/metadata_bridge.py` (NEW): Full metadata bridge implementation, baseline catalogue, and blocker mappings.
2. `packages/ca_runtime/src/ca_runtime/__init__.py` (MODIFIED): Exported `WorkflowCapabilityMetadataBridge`, `BridgeCompilationResult`, and `GOVERNED_BASELINE_CAPABILITIES`.
3. `api/routers/campaigns.py` (MODIFIED): Integrated `WorkflowCapabilityMetadataBridge` into `_try_compile_harness` and `create_campaign`.
4. `tests/cae/test_workflow_capability_metadata_bridge.py` (NEW): 7 unit and integration tests verifying end-to-end compilation, fail-closed blockers, and API routing.

---

## 3. Architectural Design & Implementation Details

### A. Governed Baseline Capabilities Catalogue
Authoritative baseline dictionary `GOVERNED_BASELINE_CAPABILITIES` defines governance boundaries across all four Authority Lanes:

| Capability ID | Authority Lane | Owner Kind | Authority Boundary |
|---|---|---|---|
| `activative_contract_validation` | `HUNTER` | `CODE` | `cae_hunter_contract_validation_boundary` |
| `lineage_preservation` | `ANALYST` | `CODE` | `cae_analyst_lineage_boundary` |
| `identity_dna_verification` | `HUNTER` | `CODE` | `cae_hunter_identity_boundary` |
| `context_budget_enforcement` | `COMMANDER` | `CODE` | `cae_commander_budget_boundary` |
| `activative_expression_generation` | `COMPOSER` | `AGENT` | `cae_composer_generation_boundary` |
| `taste_evaluation` | `ANALYST` | `CODE` | `cae_analyst_evaluation_boundary` |
| `operator_gate_approval` | `COMMANDER` | `HUMAN` | `cae_commander_operator_boundary` |

### B. Fail-Closed Blocker Mappings (TS-APP-BRIDGE-001)

The bridge reports structured failures conforming to `TS-APP-BRIDGE-001`:
- **Blocker 1 (`semantic_dependencies`):** Raised when references lack version or `sha256` hash (`TS-APP-BRIDGE-001#blocker-1`).
- **Blocker 2 (`capabilities`):** Raised when required capabilities cannot be resolved (`TS-APP-BRIDGE-001#blocker-2`).
- **Blocker 3 (`atomic_boundary`):** Raised when `atomic_boundary` is missing or invalid (`TS-APP-BRIDGE-001#blocker-3`).
- **Blocker 4 (`definition_version`):** Raised when `manifest_version` violates SemVer (`TS-APP-BRIDGE-001#blocker-4`).
- **Blocker 5 (`workflow`):** Raised when workflow DAG is missing or invalid (`TS-APP-BRIDGE-001#blocker-5`).
- **Blocker 6 (`evaluation_requirements` / `repair_laws`):** Raised when evaluation or repair contracts are missing (`TS-APP-BRIDGE-001#blocker-6`).

---

## 4. Verification Evidence

### Execution Environment
- **Operating System:** Windows (PowerShell)
- **Python Version:** 3.12.0
- **Pytest Version:** 8.3.4
- **Repository Commit:** `e5cd35ed6448f8454aa3a4a1d20e75563723ecb8`

### Test Suite Execution Summary
```
============================= test session starts =============================
tests/cae/test_workflow_capability_metadata_bridge.py::test_pilot_harness_compiles_end_to_end_with_governed_metadata PASSED [ 14%]
tests/cae/test_workflow_capability_metadata_bridge.py::test_missing_capability_metadata_fails_closed_blocker_2 PASSED [ 28%]
tests/cae/test_workflow_capability_metadata_bridge.py::test_missing_workflow_fails_closed_blocker_5 PASSED [ 42%]
tests/cae/test_workflow_capability_metadata_bridge.py::test_invalid_authority_lane_fails_closed PASSED [ 57%]
tests/cae/test_workflow_capability_metadata_bridge.py::test_missing_semantic_dependencies_fails_closed_blocker_1 PASSED [ 71%]
tests/cae/test_workflow_capability_metadata_bridge.py::test_eligibility_registry_dynamic_resolution PASSED [ 85%]
tests/cae/test_workflow_capability_metadata_bridge.py::test_campaign_creation_with_governed_bridge_succeeds PASSED [100%]

============================= 7 passed in 32.36s ==============================
```

### Full Regression Suite
```
======================= 163 passed in 375.91s (0:06:15) =======================
```
All 163 tests in `tests/cae` and `tests/api/test_campaigns_create.py` passed cleanly without any regressions.

---

## 5. Non-Negotiable Protocol Invariants

1. **CAE Remains Authoritative:** Mutation and execution contracts remain governed by CAE runtime boundaries.
2. **Authority Lane Separation:** All workflow DAG nodes are strictly mapped to `HUNTER`, `ANALYST`, `COMPOSER`, and `COMMANDER`. No lane collapse.
3. **Passive Flat Skills:** No nested Skills or dynamic Skill composition introduced.
4. **Typed Mutation Boundaries:** All bridge outputs pass `AtomicHarnessDefinitionIntake().validate()`.
5. **No Parallel Ontology:** Reuses existing domain models (`NodeKind`, `ProductBoundary`, `AuthorityLane`, `ImplementationEligibilityRegistry`).

---

**Sign-off:** Mandate M17 complete. Ready for next mandate.
