# Studio Pipeline Recipe Harness Orchestration Spine Mapping

## Existing Spine Class Names

- `OrchestrationRun`
- `StageExecutionPlan`
- `ValidationContract`
- `AgentHandoffPacket`
- `StageExecutionReceipt`
- `FailureReceipt`
- `HumanHandoffRequest`
- `QuarantineReceipt`

## Recipe Harness Class Names

- `PipelineRecipe`
- `PipelineRecipeStep`
- `PipelineRun`
- `PipelineStepRun`
- `PipelineStepReceipt`
- `PipelineApprovalGate`
- `PipelineRunBlocker`
- `PipelineArtifactRef`
- `PipelineOrchestrationSpineBinding`

## Field Mapping

| Recipe Harness | Existing Spine | Mapping |
|---|---|---|
| `PipelineRun.orchestration_run_id` | `OrchestrationRun.orchestration_run_id` | Required for planned/running recipe runs. |
| `PipelineRun.recipe_id` | `OrchestrationRun.requested_outcome` or metadata later | Preserved in recipe read model; API/runtime wiring can attach as metadata later. |
| `PipelineRun.brand_context_version_id` | `ActiveObjectRef.version_id` or evidence refs | Preserved in recipe run and stage evidence refs. |
| `PipelineRecipeStep` | `StageExecutionPlan` | `PipelineOrchestrationSpineAdapterService.compile_stage_execution_plans(...)` emits real stage plans. |
| `PipelineRecipeStep.depends_on` | `StageExecutionPlan.required_inputs` | Encoded as `dependency_step:<step_id>` entries because the current spine has no explicit dependency field. |
| `PipelineApprovalGate` | `ValidationContract` / `HumanHandoffRequest` later | Current adapter includes approval criteria in validation contracts; runtime handoff creation is deferred to an approved orchestration service call path. |
| `PipelineStepReceipt` | `StageExecutionReceipt` | `compile_stage_execution_receipts(...)` maps step receipts to existing stage receipts. |
| `PipelineRunBlocker` | `FailureReceipt` / `QuarantineReceipt` later | Current adapter surfaces blocker codes in stage receipt decisions; persistent failure/quarantine recording is deferred to orchestration service runtime wiring. |
| `PipelineArtifactRef` | `AgentHandoffPacket.source_evidence_refs` / stage evidence refs | Pointer URIs are represented as evidence refs and output refs. |

## Adapter Output

`PipelineOrchestrationSpineAdapterService` emits:

- `PipelineOrchestrationSpineBinding`
- real `StageExecutionPlan` objects
- real `ValidationContract` objects
- real `StageExecutionReceipt` objects from `PipelineStepReceipt`
- deterministic stage-plan request dictionaries for future service/API wiring

## Fields That Could Not Map Cleanly

- The current `StageExecutionPlan` has no first-class `depends_on` field, so dependencies are encoded in `required_inputs`.
- The current `OrchestrationRun` has no metadata map, so `recipe_id` and `recipe_version` remain authoritative in `PipelineRun` until a runtime API decides how to store metadata.
- `HumanHandoffRequest`, `FailureReceipt`, and `QuarantineReceipt` require orchestration repository state and are not created by the recipe adapter in this prompt.

## Golden Path To Pipeline Recipe Mapping

`Format02GoldenPathRecipeAdapterService` maps an existing `GoldenPathRun` into:

- `PipelineRun.recipe_id = format02_golden_path`
- `PipelineRun.brand_context_version_id = GoldenPathRun.input.brand_context_version_id`
- `PipelineRun.orchestration_run_id = GoldenPathOrchestrationSpineAdapterService.map_to_orchestration_run(...).orchestration_run_id`
- `Format02GoldenPathOutput` ids -> pointer-only `PipelineArtifactRef`
- `GoldenPathRun` pass/fail state -> `PipelineRun.status`
- `PipelineRun` -> `PipelineRunSummary`

The adapter does not rerun Golden Path, call providers, call renderers, or call the Local Render Worker.

## Runtime Wiring Status

The adapter emits real spine contract objects and deterministic request dictionaries. Full runtime persistence through `OrchestrationService` is intentionally deferred because this prompt does not add API endpoints or execute pipeline stages.

## No Parallel Engine Confirmation

No parallel orchestration harness was created. The recipe harness is a recipe/catalog/read-model/control layer that preserves the existing orchestration spine as execution owner.

