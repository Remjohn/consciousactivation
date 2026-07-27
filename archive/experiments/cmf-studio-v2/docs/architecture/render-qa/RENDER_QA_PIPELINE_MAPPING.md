# Render QA Pipeline Mapping

## 1. Pipeline Step Kind

Studio Pipeline Recipe Harness already has:

- `PipelineStepKind.QA`

Render QA V1 composite reports should attach to QA steps after render observations are available.

## 2. PipelineArtifactRef Role

Render QA reports map to:

- `PipelineArtifactRole.QA_RECEIPT`

Implemented bridge:

- `src/ccp_studio/services/pipeline_render_qa_bridge_service.py`

The bridge creates pointer-only `PipelineArtifactRef` values:

- `render_qa://composite/{render_qa_composite_report_id}`

No raw rendered file bytes are embedded.

## 3. Blocking Behavior

- `RenderQACompositeReport.pass_status == pass` -> QA step can pass.
- `RenderQACompositeReport.pass_status == fail` -> bridge creates `PipelineRunBlocker` values.
- `RenderQACompositeReport.pass_status == warn` -> operator review should remain required.

Existing `PipelineStepReceipt` law prevents a step receipt from passing with blockers.

## 4. No Execution

This integration does not call:

- providers
- renderers
- Remotion
- FFmpeg
- ffprobe
- subprocesses
- Local Render Worker jobs

## Optional Integration Test

Added:

- `tests/cmf_studio/test_render_qa_pipeline_bridge_v1.py`

The test verifies that a failing Render QA composite report maps to a QA artifact pointer and blocks a passing pipeline receipt.
