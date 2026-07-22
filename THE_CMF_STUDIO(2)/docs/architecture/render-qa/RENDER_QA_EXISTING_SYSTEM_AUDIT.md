# Render QA Existing System Audit

Branch: `feat/render-qa-v1`

## 1. Existing Render QA Files Found

- `src/ccp_studio/services/render_qa_service.py`
  - Existing Remotion/FFmpeg adapter QA report compiler.
  - Kept and merged additively. The existing `compile_report(...)` method remains intact.
- `src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py`
  - Already defines adapter-level `FFprobeValidationReceipt`, `FrameSamplingReceipt`, `AudioLevelAnalysisReceipt`, `DurationToleranceReceipt`, and `RenderQAReport`.

## 2. Existing Evaluation Receipt Files Found

- `src/ccp_studio/contracts/evaluation_receipts.py`
- `src/ccp_studio/services/evaluation_receipt_service.py`
- `src/ccp_studio/workflows/evaluation_workflow.py`
- Existing tests and docs reference `EvaluationReceipt` and `EvaluationReviewReadModel`.

These remain separate from Render QA V1. Render QA V1 validates rendered asset observations before review, approval, export, or publishing.

## 3. Existing Remotion / FFmpeg Adapter QA Files Found

- `src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py`
- `src/ccp_studio/services/remotion_render_adapter_service.py`
- `src/ccp_studio/services/ffmpeg_finish_adapter_service.py`
- `src/ccp_studio/services/ffprobe_validation_service.py`
- `src/ccp_studio/services/frame_sampling_service.py`
- `src/ccp_studio/services/audio_level_analysis_service.py`
- `src/ccp_studio/services/duration_tolerance_service.py`
- `src/ccp_studio/services/render_qa_service.py`

The adapter remains a dry-run/gated render adapter layer. Render QA V1 becomes the canonical operational QA receipt layer.

## 4. Existing Video Editing Engine Evaluation Files Found

- `src/ccp_studio/contracts/video_editing_engine.py`
- `src/ccp_studio/services/video_eval_service.py`
- `src/ccp_studio/services/video_render_contract_service.py`

Video Editing Engine V1 still owns timeline and render contracts. Render QA V1 should gate proxy review, final approval, export, and publishing after render observations are available.

## 5. Existing Operator-Web QA / Review UI Files Found

- `operator-web/src/App.jsx`
  - Contains Review and Evals views.
- `operator-web/src/components/timeline/TimelineWorkbenchProvider.jsx`
  - Shows render receipt and QA-like fields from Video Timeline Workbench.
- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
  - Contains caption/timeline fixture state.

No UI or API endpoints were added in this integration.

## 6. Existing ffprobe / Frame / Audio / Caption Checks Found

- Adapter ffprobe/frame/audio/duration services exist and compile deterministic receipts from supplied metadata.
- Video Timeline Workbench already displays dry-run render QA status fields.
- Caption checks exist throughout Video Editing Engine and Review tests, but not as a rendered-asset QA composite.

## 7. Existing V9 / V9.1 Evaluation Metric References Found

Searches found existing references to:

- `identity_consistency`
- `composition_quality`
- `style_consistency`
- `emotional_accuracy`
- `platform_fit`
- `negative_space`
- `hook_strength`
- `shareability`
- `routeability`

Render QA V1 codifies these as rendered-asset delivery promise metrics.

## 8. Naming Conflicts

Conflict found:

- Bundle wanted `src/ccp_studio/services/render_qa_service.py`.
- Repo already had `RenderQAService.compile_report(...)` for Remotion/FFmpeg adapter reports.

Decision:

- Do not overwrite the existing service.
- Merge Render QA V1 builder methods into the existing `RenderQAService`.
- Keep adapter `compile_report(...)` for backward compatibility.
- Add `src/ccp_studio/services/render_qa_adapter_bridge_service.py` for explicit adapter-to-V1 mapping.

## 9. Additive Application Decision

The bundle can be applied additively.

Added:

- Canonical Render QA V1 contracts.
- V1 docs, fixtures, registries, skill manifests, tests.
- Adapter and pipeline bridge services/tests.

Modified:

- Existing `src/ccp_studio/services/render_qa_service.py` only to add V1 methods while preserving adapter behavior.

## 10. Files Requiring Merge Instead of Copy

- `src/ccp_studio/services/render_qa_service.py`

All other bundle files were copied additively.
