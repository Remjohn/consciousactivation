# Studio Pipeline Existing Orchestration Audit

Branch: `feat/studio-pipeline-recipe-harness-v1`

## Existing Orchestration Spine Files Found

- `src/ccp_studio/contracts/orchestration.py`
- `src/ccp_studio/services/orchestration.py`
- `src/ccp_studio/repositories/orchestration.py`
- `tests/cmf_studio/test_orchestration_records.py`
- `tests/cmf_studio/test_spec_governance.py`

The spine is real and should remain the execution owner.

## Existing Spine Models Found

- `OrchestrationRun`
- `StageExecutionPlan`
- `ValidationContract`
- `AgentHandoffPacket`
- `StageExecutionReceipt`
- `FailureReceipt`
- `FrictionReceipt`
- `HumanHandoffRequest`
- `QuarantineReceipt`

## Existing Golden Path Orchestrator Files Found

- `src/ccp_studio/contracts/golden_path_orchestrator.py`
- `src/ccp_studio/services/format02_golden_path_orchestrator_service.py`
- `src/ccp_studio/repositories/golden_path_orchestrator.py`
- `src/ccp_studio/services/golden_path_orchestration_spine_adapter_service.py`
- `tests/cmf_studio/test_format02_golden_path_orchestrator_v1.py`
- `tests/cmf_studio/test_format02_golden_path_orchestration_spine_mapping_v1.py`

Golden Path already maps into the orchestration spine through `GoldenPathOrchestrationSpineAdapterService`.

## Existing Workflow / Pipeline / Recipe Files Found

- `src/ccp_studio/workflows/orchestration_run.py`
- `src/ccp_studio/workflows/tech_spec_compiler.py`
- `src/ccp_studio/services/production_orchestration.py`
- `src/ccp_studio/api/v1/production_orchestration.py`
- `docs/architecture/operator-web/OPERATOR_WEB_UI_WIRING_MATRIX.md`
- `docs/architecture/operator-web/OPERATOR_WEB_MISSING_BACKEND_ENDPOINTS.md`

No existing `PipelineRecipe` / `PipelineRun` contract equivalent was found before this bundle.

## Existing API / UI Pipeline Screens Found

- Operator-web has `PipelineView` in `operator-web/src/App.jsx`.
- The operator-web audit identifies Golden Path / Pipeline visibility as backend-only or missing.
- This prompt does not add UI or API endpoints.

## Existing Stage Plan / Receipt / Handoff / Quarantine Coverage

- `OrchestrationService.create_stage_execution_plan(...)`
- `OrchestrationService.record_validation_contract(...)`
- `OrchestrationService.create_agent_handoff_packet(...)`
- `OrchestrationService.close_stage_execution(...)`
- `OrchestrationService.record_failure_receipt(...)`
- `OrchestrationService.request_human_handoff(...)`
- `OrchestrationService.record_quarantine_receipt(...)`

## Existing Tests That Cover Orchestration

- `tests/cmf_studio/test_orchestration_records.py`
- `tests/cmf_studio/test_spec_governance.py`
- `tests/cmf_studio/test_format02_golden_path_orchestration_spine_mapping_v1.py`

## Naming Conflicts

No file-level naming conflicts were found for:

- `studio_pipeline_recipe_harness.py`
- `pipeline_recipe_*_service.py`
- `pipeline_run_*_service.py`
- `pipeline_orchestration_spine_adapter_service.py`

## Additive Application Decision

The bundle can be applied additively. The recipe harness is a read-model/control layer over the existing spine. It does not replace `orchestration.py`, `orchestration.py` service, or Golden Path files.

## Files Requiring Merge Instead Of Copy

None. Target files did not previously exist.

## No Parallel Harness Confirmation

No second orchestration engine was created. `PipelineRun` is a recipe/run read model that must bind to `orchestration_run_id` for active runs.

