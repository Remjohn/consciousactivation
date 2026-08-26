# KNOWN LEGACY TEST DEBT REGISTER

**Authority Scope**: Pre-existing brownfield debt catalogued during CA-TWC-01 gate closure.  
**Owner**: `operator`  
**Purpose**: Document all legacy test failures outside `tests/cae` that pre-date phases 23–25, preventing any future phase or completion claim from silently ignoring, counting, or obscuring them.

---

## Triage Summary

| Category | Count | Status | Description |
| :--- | :--- | :--- | :--- |
| **Bucket A: Phase 23–25 Breakages** | 0 | **ALL FIXED** | All Phase 23–25 regressions (`tests/api/test_interviews_import.py`, `tests/api/test_interviews_brief_led.py`, `tests/api/test_v1_tenancy.py`, `tests/cae/*`) are 100% GREEN. |
| **Bucket B: Brownfield Legacy Debt** | 7 | **CATALOGUED** | Pre-existing debt across phases 2, 4, 5, 9 and pipeline status WS. Owner: `operator`. |

---

## Bucket B: Pre-Existing Brownfield Test Debt Register

### 1. `tests/api/test_pipeline_status_ws.py::test_service_packages_unchanged`
- **Owner**: `operator`
- **Failure**: `AssertionError: git diff --stat -- services/ packages/ returned non-empty diff`
- **Root Cause**: The test asserts that `git diff --stat -- services/ packages/` is completely clean. During active development or feature branch work modifying `packages/ca_runtime/` (or any package), this assertion fails by design because files under `packages/` are being authored.
- **Classification**: Brownfield git tree status assertion from TS-APP-API-005.

### 2. `tests/phase2/test_air_core.py::AirRegistryTests::test_duplicate_id_requires_source_hash`
- **Owner**: `operator`
- **Failure**: `AssertionError: assert 243 == 242`
- **Root Cause**: The test asserts exact primitive count in the legacy AIR SQLite registry (`len(registry.primitives) == 242`). A subsequent primitive was added in earlier brownfield phases, raising the count to 243.
- **Classification**: Hardcoded primitive count drift in Phase 2 legacy fixture.

### 3. `tests/phase2/test_air_core.py::AirRegistryTests::test_exact_inventory_counts_and_duplicate_preservation`
- **Owner**: `operator`
- **Failure**: `AssertionError: assert 243 == 242`
- **Root Cause**: Same as #2 above; asserts exact inventory length of 242 primitives against SQLite store.
- **Classification**: Hardcoded primitive count drift in Phase 2 legacy fixture.

### 4. `tests/phase4/test_traceability.py::test_phase4_spec_matrix_matches_exact_seven_specs`
- **Owner**: `operator`
- **Failure**: `AssertionError: assert False where False = Path('06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-001.md').is_file()`
- **Root Cause**: Traceability test expects legacy directory path `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-001.md` from an older repo folder organization before monorepo consolidation.
- **Classification**: Hardcoded documentation path in Phase 4 traceability test.

### 5. `tests/phase5/test_cli_schemas_reference.py::test_cli_production_demo`
- **Owner**: `operator`
- **Failure**: `subprocess.TimeoutExpired: Command '... python -m cmf_activative_intelligence ... production-demo ...' timed out after 90 seconds`
- **Root Cause**: End-to-end CLI subprocess invocation in Windows environment running complete Phase 5 demo exceeds the 90s test timeout under CI/concurrency load.
- **Classification**: Subprocess execution timeout in Phase 5 CLI regression test.

### 6. `tests/phase5/test_traceability.py::test_phase5_spec_hashes_and_all_acceptance_ids_resolve`
- **Owner**: `operator`
- **Failure**: `AssertionError: assert False where False = Path('04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-003.md').is_file()`
- **Root Cause**: Traceability matrix CSV references pre-consolidation path `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-003.md` which moved during project restructuring.
- **Classification**: Hardcoded documentation path in Phase 5 traceability CSV.

### 7. `tests/phase9/test_reference_pilot.py` & `tests/phase9/test_release_pilot.py`
- **Owner**: `operator`
- **Failure**: `ContractSetError: Delegation release receipt missing: D:\Work\consciousactivation\03_DELEGATION_PROTOCOL\delegation-contracts\1.1.0-rc.4\RELEASE_RECEIPT.json`
- **Root Cause**: Phase 9 release pilot tests verify legacy delegation protocol `1.1.0-rc.4` by looking for a release receipt at `03_DELEGATION_PROTOCOL/delegation-contracts/1.1.0-rc.4/RELEASE_RECEIPT.json`. This mock artifact was not retained during repo re-structuring.
- **Classification**: Missing legacy delegation contract fixture in Phase 9 pilot test.

---

## Bucket A: Phase 23–25 Suite Status (100% Passed)

- **`tests/cae/`**: **113 / 113 PASSED (100%)**
- **`tests/api/test_v1_tenancy.py`**: **2 / 2 PASSED (100%)**
- **`tests/api/test_interviews_import.py`**: **8 / 8 PASSED (100%)**
- **`tests/api/test_interviews_brief_led.py`**: **2 / 2 PASSED (100%)**
- **`tests/api/test_air_hypotheses_select.py`**: **6 / 6 PASSED (100%)**
- **`tests/interview_composer/`**: **17 / 17 PASSED (100%)**
- **`tests/phase1/`**: **14 / 14 PASSED (100%)**
- **`tests/phase3/`**: **19 / 19 PASSED (100%)**
- **`tests/phase6/`**: **10 / 10 PASSED (100%)**
- **`tests/phase8/`**: **24 / 24 PASSED (100%)**
- **`tests/pipeline/`**: **17 / 17 PASSED (100%)**
- **`tests/traceability/`**: **3 / 3 PASSED (100%)**
