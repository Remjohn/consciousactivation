# Golden Path Orchestration Integration

## Upstream Layers Verified

The Format 02 Golden Path integration was applied only after verifying the real repo already contains the required upstream compiler layers:

- Narrative Story Doctor / Extraction Intelligence:
  - `src/ccp_studio/contracts/narrative_story_doctor.py`
  - `src/ccp_studio/services/narrative_story_doctor_service.py`
- Narrative to Format Bridge:
  - `src/ccp_studio/contracts/narrative_format_bridge.py`
  - `src/ccp_studio/services/narrative_to_format_bridge_service.py`
- Format Intelligence:
  - `src/ccp_studio/contracts/format_intelligence.py`
  - `src/ccp_studio/services/format_intelligence_service.py`
- Composition Intelligence / Format 02 Pack:
  - `src/ccp_studio/contracts/composition_intelligence.py`
  - `src/ccp_studio/contracts/format02_composition_intelligence.py`
  - `src/ccp_studio/services/composition_intelligence_service.py`
  - `src/ccp_studio/services/format02_composition_service.py`
- Avatar Performance Layer:
  - `src/ccp_studio/contracts/avatar_performance.py`
  - `src/ccp_studio/services/avatar_performance_service.py`
  - `src/ccp_studio/services/format02_avatar_performance_adapter_service.py`
- Video Editing Engine V1:
  - `src/ccp_studio/contracts/video_editing_engine.py`
  - `src/ccp_studio/services/video_editing_engine_service.py`
  - `src/ccp_studio/services/video_render_contract_service.py`
  - `src/ccp_studio/services/video_eval_service.py`
  - `src/ccp_studio/services/video_export_service.py`

## Orchestration Spine Verified

The existing orchestration spine is present and contains the canonical concepts required by this prompt:

- `src/ccp_studio/contracts/orchestration.py`
- `src/ccp_studio/services/orchestration.py`
- `OrchestrationRun`
- `StageExecutionPlan`
- `ValidationContract`
- `StageExecutionReceipt`

## Exact Mapping

`GoldenPathRun` maps to `OrchestrationRun` through `GoldenPathOrchestrationSpineAdapterService.map_to_orchestration_run(...)`.

- `golden_path_run_id` becomes a deterministic UUID-backed `orchestration_run_id`.
- `brand_id` becomes a deterministic UUID-backed `brand_id`.
- `brand_context_version_id` is preserved as `ActiveObjectRef.version_id`.
- `requested_outcome` is `format02_golden_path_source_to_fake_export`.
- Golden Path pass/fail status maps to `StageRunStatus`.

`GoldenPathRecipeSpec.stage_names` and actual `GoldenPathRun.stage_results` map to `StageExecutionPlan[]`.

- Each stage becomes one `StageExecutionPlan`.
- Plans block `skip_stage`, provider calls, Remotion calls, FFmpeg calls, and second-harness creation.
- Plans require brand context and source span references.

Golden Path gate codes map to `ValidationContract[]`.

- Every stage gets a validation contract.
- Common gates include missing brand context, missing source refs, second harness creation, provider calls, and real renderer calls.
- Stage-specific gates include composition lock, no-lip-sync, fake render hash, eval pass, and export approval.

`GoldenPathStageResult` maps to `StageExecutionReceipt[]`.

- Each stage result becomes one receipt.
- Stage output refs and receipt refs become `evidence_refs`.
- Output objects use the `golden_path.<stage>.output` object type.

`GoldenPathObjectSpineMap` maps to orchestration evidence refs and active object lineage.

- The existing orchestration contract has no free-form metadata field.
- Object spine references are therefore preserved as evidence refs rather than being added as a new contract shape.

## Field Mismatches

- Golden Path contracts use string IDs; orchestration contracts use UUIDs.
- The adapter uses deterministic UUID projection with `uuid5` so repeated mappings are stable.
- Golden Path has `brand_context_version_id` as a string; orchestration `ActiveObjectRef.version_id` is a UUID.
- The adapter preserves the original string as an evidence ref and also projects it to a deterministic UUID for orchestration linking.
- The existing `OrchestrationRun` has no metadata/artifact reference field, so rich Golden Path object-spine values are represented in `StageExecutionReceipt.evidence_refs`.

## Adapter Limitations

- The adapter is projection-only.
- It does not run the Golden Path.
- It does not call `OrchestrationService` runtime methods.
- It does not write into an orchestration repository.
- It does not create handoff packets or command-bus envelopes.
- Full runtime wiring can be added later if `OrchestrationService` gains a public batch creation API for plan, contract, and receipt projection.

## Runtime Wiring Status

Full runtime wiring was not added in this branch. A thin mapping helper was added at:

`src/ccp_studio/services/golden_path_orchestration_spine_adapter_service.py`

This keeps the existing orchestration spine canonical while proving the Golden Path can be represented by its contracts.

## No Second Harness

No second orchestration harness was created. The Golden Path service remains a deterministic recipe runner for the Format 02 proof path, and the new adapter maps its outputs into the existing orchestration contracts.
