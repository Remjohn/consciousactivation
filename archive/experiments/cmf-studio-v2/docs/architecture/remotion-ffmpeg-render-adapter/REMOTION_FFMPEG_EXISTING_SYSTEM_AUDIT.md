# Remotion + FFmpeg Existing System Audit

Branch: `feat/remotion-ffmpeg-render-adapter-v1-1`

Baseline before integration:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result: `851 passed, 10 skipped`.

## 1. Existing Remotion-related files found

- `src/ccp_studio/contracts/video_editing_engine.py` already defines `RemotionInputProps`.
- `src/ccp_studio/services/video_render_contract_service.py` already compiles `RemotionInputProps` from `VideoTimelineProgram`.
- `src/ccp_studio/contracts/avatar_asset_production.py` and `src/ccp_studio/services/avatar_remotion_layer_payload_service.py` define avatar Remotion layer payload contracts.
- `docs/architecture/avatar-asset-production-rig-export/` documents the Remotion avatar payload boundary.
- `docs/architecture/video-editing-engine/` documents that Video Editing Engine V1 emits fake render receipts and leaves real Remotion execution for a later adapter.
- `docs/stories/story-8-2-deterministic-remotion-and-motion-canvas-rendering.md` documents deterministic Remotion/Motion Canvas rendering as a future worker boundary.
- `operator-web/src/data.js` and timeline workbench docs mention Remotion as a production/render route, but no real Remotion runtime call was found in backend tests or services.

## 2. Existing FFmpeg/ffprobe files found

- `src/ccp_studio/contracts/video_editing_engine.py` already defines `FFmpegFinishPlan`.
- `src/ccp_studio/services/video_render_contract_service.py` already compiles `FFmpegFinishPlan` from final render contracts.
- `registries/canonical/capability_preflight/runtime_profiles.v1.json` defines FFmpeg and ffprobe runtime capabilities.
- `registries/canonical/capability_preflight/pipeline_requirements.v1.json` gates `VIDEO_REAL_RENDER` through required runtime capabilities.
- `docs/architecture/capability-preflight/` documents FFmpeg/ffprobe availability as preflight status only.

## 3. Existing Video Editing Engine render contract files found

- `src/ccp_studio/contracts/video_editing_engine.py`
  - `OTIOAuditTimeline`
  - `RemotionInputProps`
  - `ProxyRenderContract`
  - `FinalRenderContract`
  - `ProxyRenderReceipt`
  - `FinalRenderReceipt`
  - `FFmpegFinishPlan`
  - `VideoEvaluationReceipt`
- `src/ccp_studio/services/video_render_contract_service.py`
  - `compile_otio_audit_timeline`
  - `compile_remotion_input_props`
  - `compile_proxy_render_contract`
  - `execute_proxy_render_fake`
  - `compile_final_render_contract`
  - `compile_ffmpeg_finish_plan`
  - `execute_final_render_fake`

The new adapter must not replace these contracts. It should sit after them as a gated local runtime adapter.

## 4. Existing Local Render Worker files found

- `src/ccp_studio/contracts/local_render_worker.py`
- `src/ccp_studio/services/local_render_worker_service.py`
- `src/ccp_studio/services/render_job_queue_service.py`
- `src/ccp_studio/services/render_job_lease_service.py`
- `src/ccp_studio/services/render_job_result_service.py`
- `src/ccp_studio/services/render_job_heartbeat_service.py`
- `src/ccp_studio/services/render_worker_health_service.py`
- `src/ccp_studio/services/local_render_worker_orchestrator_service.py`
- `registries/canonical/local_render_worker/`
- `tests/cmf_studio/test_local_render_worker_v1.py`
- Integration tests for local worker, video engine, workspace, and capability preflight already exist.

The local worker is fake/deterministic in V1. The Remotion/FFmpeg adapter must preserve that by default and require an explicit local worker lease for real-local execution.

## 5. Existing Render QA / evaluation files found

- `src/ccp_studio/contracts/evaluation_receipts.py`
- `src/ccp_studio/services/evaluation_receipt_service.py`
- `src/ccp_studio/contracts/video_editing_engine.py` defines `VideoEvaluationReceipt`.
- `src/ccp_studio/services/video_eval_service.py` evaluates Video Editing Engine receipts.
- `docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md` specifies post-render QA with ffprobe, frame sampling, audio analysis, duration checks, and actionable repair commands.

No existing `RenderQAReport`, `FrameSamplingReceipt`, `AudioLevelAnalysisReceipt`, or `DurationToleranceReceipt` contract was found before this bundle.

## 6. Existing OTIO/export files found

- `src/ccp_studio/contracts/video_editing_engine.py` defines `OTIOAuditTimeline` and `VideoExportPack`.
- `src/ccp_studio/services/video_render_contract_service.py` compiles OTIO audit timelines.
- `src/ccp_studio/services/video_export_service.py` compiles export packs.
- `src/ccp_studio/api/v1/video_timeline_workbench.py` exposes OTIO export read-model behavior for the workbench.
- `operator-web/src/components/timeline/TimelineInspector.jsx` and related timeline workbench components expose OTIO export actions.

## 7. Existing subprocess/shell render paths found

No backend service path was found that executes Remotion, FFmpeg, ffprobe, or provider render tools through `subprocess`, `Popen`, or `os.system`.

The repo does contain docs and product specifications describing future worker/runtime boundaries. Those are not executable runtime calls.

## 8. Existing docs/specs mentioning Remotion + @remotion/skia

- `docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md`
- `docs/prd/modules/PRD_CMF_13_OpenMontage_Inspired_Production_Orchestration_Adapters.md`
- `docs/stories/story-8-2-deterministic-remotion-and-motion-canvas-rendering.md`
- `docs/architecture/video-editing-engine/VIDEO_EDITING_ENGINE_V1_INTEGRATION_MAPPING.md`
- `docs/architecture/video-editing-engine/VIDEO_EDITING_ENGINE_V1_INTEGRATION_SUMMARY.md`
- `docs/architecture/avatar-asset-production-rig-export/AVATAR_ASSET_PRODUCTION_INTEGRATION_MAPPING.md`
- `docs/ui/composition-boards/CMF_COMPOSITION_RUNTIME_BEHIND_THE_SCENES.md`
- `docs/ux/ux-design-specification.md`

The exact `@remotion/skia` package anchor was not present in executable code before this bundle. The adapter docs and contracts should record the explicit Remotion Node.js + `@remotion/skia` target.

## 9. Naming conflicts

No target file conflicts were found for:

- `src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py`
- new Remotion/FFmpeg adapter services
- `registries/canonical/remotion_ffmpeg_render_adapter/`
- `registries/canonical/skills/shared/remotion_ffmpeg_render_adapter/`
- `tests/cmf_studio/test_remotion_ffmpeg_render_adapter_v1_1.py`

Related names already exist in Video Editing Engine and Local Render Worker, but they are upstream owners, not collisions.

## 10. Additive application decision

This bundle can be applied additively.

The adapter should:

- consume `VideoTimelineProgram`, `RemotionInputProps`, `FinalRenderContract`, and `FFmpegFinishPlan` later through explicit integration points;
- require Local Render Worker lease and tested runtime capability for real-local execution;
- respect Capability Preflight before real execution;
- remain dry-run-only in tests;
- preserve fake render paths as the default behavior in Video Editing Engine V1.

## 11. Files requiring merge instead of copy

No files require merge for this integration.

Do not copy the bundle's package `__init__.py` files into the real repo.
