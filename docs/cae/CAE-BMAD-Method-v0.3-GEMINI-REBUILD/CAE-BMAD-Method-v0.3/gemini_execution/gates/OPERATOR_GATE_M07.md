# Operator Gate — M07: Rebuild the Repository / Application / CLI Investigation Agents

## 1. Execution Summary
- **Mandate ID:** `M07`
- **Mandate Title:** Rebuild the Repository / Application / CLI Investigation Agents
- **Phase Name:** Physical Repository Layout, Deployable Services, and Command & Control Systems
- **Execution Date:** 2026-09-03
- **Status:** `AWAITING OPERATOR RATIFICATION`

---

## 2. Deliverables Summary

| Deliverable Artifact | Path | Status | Verification Check |
|---|---|---|---|
| **Repository, Application & CLI Spec** | [`method/CAE_BMAD_REPOSITORY_APP_CLI_SPEC.md`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/method/CAE_BMAD_REPOSITORY_APP_CLI_SPEC.md) | Created | Reality contact rules for Level 06 (Repository), Level 07 (Application), and Level 08 (Script/CLI). |
| **Repository Reality Map (MD & JSON)** | [`docs/cae-bmad/07_brownfield/REPOSITORY_REALITY_MAP.md`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/docs/cae-bmad/07_brownfield/REPOSITORY_REALITY_MAP.md) | Created | Audits 7 managed workspace directories, cross-repo contracts, and orphan paths with GOVERNED hygiene verdict. |
| **Application Map (MD & JSON)** | [`docs/cae-bmad/07_brownfield/APPLICATION_MAP.md`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/docs/cae-bmad/07_brownfield/APPLICATION_MAP.md) | Created | Maps 5 deployable services and runtime packages (`world-intelligence`, `pipeline`, `builder`, `delegation`, `ca_runtime`) with verified entrypoints. |
| **Command & Control Map (MD & JSON)** | [`docs/cae-bmad/07_brownfield/COMMAND_CONTROL_MAP.md`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/docs/cae-bmad/07_brownfield/COMMAND_CONTROL_MAP.md) | Created | Catalogs 5 automation script suites and CLI entrypoints with 100% verified executable status. |
| **Repository Reality Map Schema** | [`schemas/repository_reality_map.schema.json`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/schemas/repository_reality_map.schema.json) | Created | Enforces min 5 workspace directories, cross-repo contract validation, and hygiene verdict enum. |
| **Application Map Schema** | [`schemas/application_map.schema.json`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/schemas/application_map.schema.json) | Created | Enforces min 4 deployable services, resolvable entrypoints, service types, and runtime dependencies. |
| **Command Control Map Schema** | [`schemas/command_control_map.schema.json`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/schemas/command_control_map.schema.json) | Created | Enforces min 3 command suites, runtime engines, and verified executable boolean tags. |
| **Templates (x3)** | [`templates/repository_reality_map.md`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/templates/repository_reality_map.md), [`templates/application_map.md`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/templates/application_map.md), [`templates/command_control_map.md`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/templates/command_control_map.md) | Created | Standardized templates for Level 06, Level 07, and Level 08 investigation deliverables. |
| **Skills (x3)** | [`skills/caebmad-repository-investigate/`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/skills/caebmad-repository-investigate/SKILL.md), [`caebmad-application-investigate/`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/skills/caebmad-application-investigate/SKILL.md), [`caebmad-cli-investigate/`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/skills/caebmad-cli-investigate/SKILL.md) | Created | Concrete execution logic for repository auditing, service mapping, and CLI validation. |
| **Workflow** | [`workflows/caebmad_m07_repo_app_cli_workflow.yaml`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/workflows/caebmad_m07_repo_app_cli_workflow.yaml) | Created | 4-step pipeline: audit repository → map applications → map command suites → gate validation. |
| **Generator & Validator (x2)** | [`scripts/generate_repo_app_cli_maps.py`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/generate_repo_app_cli_maps.py), [`scripts/validate_repo_app_cli_system.py`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/validate_repo_app_cli_system.py) | Created | Automated inspection and validation of workspace reality across Levels 06, 07, and 08. |
| **Automated Test Suite** | [`tests/test_m07_repo_app_cli.py`](file:///d:/Work/consciousactivation/docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/tests/test_m07_repo_app_cli.py) | Created | 8 unit, negative, and stale-reference tests (100% Pass). |

---

## 3. Evidence and Proof Standard

### 3.1 Automated Verification Output
```text
pytest tests/test_m07_repo_app_cli.py -v
============================= test session starts =============================
tests/test_m07_repo_app_cli.py::test_repository_reality_map_exists_and_valid PASSED [ 12%]
tests/test_m07_repo_app_cli.py::test_application_map_exists_and_valid PASSED [ 25%]
tests/test_m07_repo_app_cli.py::test_command_control_map_exists_and_valid PASSED [ 37%]
tests/test_m07_repo_app_cli.py::test_m07_schemas_valid PASSED            [ 50%]
tests/test_m07_repo_app_cli.py::test_countertest_rejects_truncated_services_count PASSED [ 62%]
tests/test_m07_repo_app_cli.py::test_countertest_rejects_invalid_service_type PASSED [ 75%]
tests/test_m07_repo_app_cli.py::test_countertest_rejects_unverified_executable_command PASSED [ 87%]
tests/test_m07_repo_app_cli.py::test_m07_scripts_skills_templates_workflows_exist PASSED [100%]
============================== 8 passed in 0.16s ===============================

python scripts/validate_repo_app_cli_system.py
============================================================
CAE-BMAD Repo/App/CLI Validator — Passed: 9, Errors: 0
============================================================
ALL REPO/APP/CLI SYSTEM VALIDATIONS PASSED.

pytest tests/ -v
============================= 58 passed in 2.47s ==============================
```

### 3.2 Evidence Classification Ledger
- `KNOWN`: Physical directory structure across `services/`, `packages/`, `programs/`, `docs/`, `governance/`, `scripts/`, and `tests/`.
- `INHERITED`: Microservice architecture and cross-repo contracts from brownfield lineage.
- `VERIFIED`: 58/58 full regression pytest tests passing; 5 services mapped with resolvable entrypoints; 5 script suites verified executable.
- `PROPOSED`: Standardized reality contact rules for Levels 06, 07, and 08.
- `MISSING`: Downstream mandates M08 through M12.
- `CONTRADICTED`: None remaining in M07 scope.

---

## 4. Promotion Checklist

- [x] Required mandate file read
- [x] Required original BMAD equivalent surfaces inspected
- [x] Required CAE sources inspected
- [x] Operating levels selected and justified (`REPOSITORY`, `APPLICATION`, `SCRIPT / CLI`, descended to `MODULE` and `LINE`)
- [x] Actual method components created/updated
- [x] Agent routing verified
- [x] Skill/workflow loading verified
- [x] Positive tests run
- [x] Negative/countertests run
- [x] False-proof defenses checked
- [x] Historical lineage preserved
- [x] Missing implementation explicitly documented
- [x] Contradictions documented
- [x] Decision ledger updated
- [x] Execution ledger updated
- [ ] Operator reviewed evidence
- [ ] Operator approved promotion
