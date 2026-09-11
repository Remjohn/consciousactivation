# CAE M25 Execution Report: Workspace + Guest Operating Context Program

**Status:** COMPLETE — OPERATOR-RATIFICATION-REQUESTED  
**Date:** 2026-08-31  
**Commit SHA:** `e5cd35ed6448f8454aa3a4a1d20e75563723ecb8`  
**Governing Mandate:** `M25_workspace_guest_operating_context_program.md`  
**PRD Section:** `docs/PRD/CURRENT.md` (§1.4 Tenancy & App Layer)

---

## 1. Executive Summary

CAE Phase 3 Mandate M25 establishes the **Workspace + Guest Operating Context Program** (`workspace_guest_operating_context_program` v1.0.0) as an operator-addressable, governed Program package and state machine runtime.

The implementation reconciles the live PostgreSQL/RLS tenancy authority (`workspace_core.py`, `v1_tenancy.py`, `TS-CAE-TEN-001`) with the universal program state machine engine (`program_state_runtime.py`, `state_lifecycle.py`), resolving and strictly enforcing:
1. **One-Workspace / One-Active-Guest Operating Model:** A Workspace is the single root customer tenant isolation boundary (`CA-ENT-001`). Within an active Program aggregate, exactly one Guest operating context (`CA-ENT-003`) is active. Attempting to bind or activate multiple conflicting active guests raises `SingleActiveGuestViolationError` fail-closed.
2. **Subordinate Persona / Brand Context with Lineage:** Persona / Brand Context (Brand DNA, Voice DNA, Visual DNA) is NOT a secondary tenant or independent entity. It is a subordinate derived dimension scoped strictly under the active Guest and Workspace. All derived expressions must record and verify SHA-256 evidence digests (`source_evidence_hashes`), failing closed with `LineageMissingError` if unverified.
3. **Four Authority Lanes Preservation:** Enforces `COMMANDER` for workspace configuration, context activation, and repair; `HUNTER` for guest participant registration; and `ANALYST` for evidence binding and brand context derivation.
4. **No Parallel Tenancy Layer:** Reuses live PostgreSQL RLS tenancy structures and typed operations.

---

## 2. Baseline Authority Read Set & Evidence

### Read Set Reported
1. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
2. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/08_INITIAL_PROGRAM_INVENTORY.md`
3. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md`
4. `docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS/M02_canonical_program_inventory_lifecycle_contract.md`
5. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M25_workspace_guest_operating_context_program.md`
6. `docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M25_GEMINI_ACTIVATION.md`
7. `docs/PRD/CURRENT.md` (§1.4 Tenancy, lines 110–250)
8. `docs/cae/constitutions/CA-CAN-01A_WORKSPACE.yaml`
9. `docs/cae/constitutions/CA-CAN-01B_GUEST.yaml`
10. `docs/cae/specs/current/SPEC-TWC-UI-001.md`
11. `docs/cae/specs/current/SPEC-GST-UI-001.md`
12. `api/routers/v1_tenancy.py`
13. `api/routers/programs.py`
14. `packages/ca_runtime/src/ca_runtime/workspace_core.py`
15. `packages/ca_runtime/src/ca_runtime/tenant_operations.py`
16. `packages/ca_runtime/src/ca_runtime/models/tenant_slice.py`
17. `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
18. `packages/ca_runtime/src/ca_runtime/program_registry.py`
19. `packages/ca_runtime/src/ca_runtime/tenancy.py`
20. `packages/ca_runtime/src/ca_runtime/agent_team.py`
21. `packages/ca_runtime/src/ca_runtime/hook_runtime.py`
22. `tests/cae/test_tenant_slice_operations.py`
23. `tests/cae/test_tenant_slice_scaffolding.py`
24. `tests/cae/test_ca_twc_01_structure.py`

---

## 3. Implementation Details

### 3.1 State Machine Grammar (`WORKSPACE_GUEST_STATE_MACHINE_V1`)
- **Initial State:** `INITIAL`
- **Terminal State:** `CONTEXT_ACTIVE`
- **Transitions:**
  1. `configure_workspace` (`INITIAL` $\rightarrow$ `WORKSPACE_CONFIGURED`): Lane `COMMANDER`, trigger `cae.workspace.configure@1.0.0`, preconditions `("workspace_active", "operator_authorized")`, side effect `TRANSACTIONAL_COMMIT`.
  2. `register_guest` (`WORKSPACE_CONFIGURED` $\rightarrow$ `GUEST_REGISTERED`): Lane `HUNTER`, trigger `cae.guest.register@1.0.0`, preconditions `("workspace_active", "single_active_guest_enforced")`, side effect `LOCAL_STATE_WRITE`.
  3. `bind_guest_evidence` (`GUEST_REGISTERED` $\rightarrow$ `EVIDENCE_BOUND`): Lane `ANALYST`, trigger `cae.guest.bind_evidence@1.0.0`, preconditions `("workspace_active", "evidence_integrity_verified")`, side effect `LOCAL_STATE_WRITE`.
  4. `activate_guest_context` (`EVIDENCE_BOUND` $\rightarrow$ `CONTEXT_ACTIVE`): Lane `COMMANDER`, trigger `cae.guest.activate_context@1.0.0`, preconditions `("workspace_active", "lineage_provenance_verified")`, side effect `TRANSACTIONAL_COMMIT`.
  5. `repair_context` (`REPAIRING` $\rightarrow$ `WORKSPACE_CONFIGURED`): Lane `COMMANDER`, trigger `cae.guest.repair_context@1.0.0`, preconditions `("workspace_active", "operator_authorized")`, side effect `TRANSACTIONAL_COMMIT`.

### 3.2 Program Package Files
- `programs/workspace_guest_program/program_manifest.yaml`
- `programs/workspace_guest_program/CAE.md`
- `programs/workspace_guest_program/instructions.md`
- `programs/workspace_guest_program/skills/workspace_boundary_verifier/SKILL.md`
- `programs/workspace_guest_program/skills/guest_evidence_indexer/SKILL.md`
- `programs/workspace_guest_program/skills/brand_context_deriver/SKILL.md`

### 3.3 Core Runtime Modules
- `packages/ca_runtime/src/ca_runtime/workspace_guest_program.py`: `WorkspaceGuestProgramCoordinator`, `GuestEvidenceItem`, `DerivedBrandContext`, `WorkspaceGuestContextSnapshot`, and typed error hierarchy.
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`: Added `get_canonical_workspace_guest_state_machine()` and registered in runtime.
- `packages/ca_runtime/src/ca_runtime/__init__.py`: Exported all new symbols.

---

## 4. Verification Evidence

### 4.1 Test Commands & Results
- **Dedicated Suite:**
  ```bash
  python -m pytest tests/cae/test_workspace_guest_program.py -v
  ```
  Result: **10 passed in 1.18s**
  - `test_workspace_guest_program_package_discovery_and_manifest` (PASSED)
  - `test_workspace_guest_state_machine_definition` (PASSED)
  - `test_full_lifecycle_initial_to_active_context` (PASSED)
  - `test_single_active_guest_enforcement_fail_closed` (PASSED)
  - `test_subordinate_brand_context_lineage_preservation_and_validation` (PASSED)
  - `test_cross_workspace_isolation_denial` (PASSED)
  - `test_authority_lane_enforcement` (PASSED)
  - `test_evidence_integrity_and_guest_unregistered_errors` (PASSED)
  - `test_governed_repair_and_resume_lifecycle` (PASSED)
  - `test_optimistic_concurrency_version_conflict` (PASSED)

- **Complete CAE Suite:**
  ```bash
  python -m pytest tests/cae -v
  ```
  Result: **188 passed in 64.45s (0 regressions)**

- **API & Registry Suite:**
  ```bash
  python -m pytest tests/api/test_programs_api.py tests/phase2/test_program_registry.py -v
  ```
  Result: **18 passed in 3.94s**

---

## 5. Non-Negotiable Compliance Matrix

| Rule | Status | Verification Detail |
|---|---|---|
| CAE remains authoritative | COMPLIANT | All state and mutations are governed by CAE state machine and PostgreSQL RLS. |
| Four Authority Lanes preserved | COMPLIANT | Strict lane checks (`COMMANDER`, `HUNTER`, `ANALYST`) enforced at every transition. |
| Passive flat skills | COMPLIANT | 3 flat skills added without nesting or skill-to-skill calls. |
| One-Workspace / One-Active-Guest | COMPLIANT | Concurrency check raises `SingleActiveGuestViolationError` fail-closed. |
| Protected evidence immutability | COMPLIANT | Guest evidence items are indexed with SHA-256; never silently rewritten. |
| Subordinate Persona/Brand Lineage | COMPLIANT | Requires non-empty, matching `source_evidence_hashes` producing deterministic `lineage_sha256`. |
| No parallel tenancy schema | COMPLIANT | Bound to existing `workspace_core.py` and PostgreSQL `cae` schema. |
| Deterministic receipts | COMPLIANT | Every transition emits a cryptographically verified transition receipt. |

---

## 6. PRD Update & Operator Decision Request

`docs/PRD/CURRENT.md` (§1.4 Tenancy) has been updated and dated `2026-08-31`.

**Operator Action Requested:**
Review and ratify the M25 execution report and evidence.
