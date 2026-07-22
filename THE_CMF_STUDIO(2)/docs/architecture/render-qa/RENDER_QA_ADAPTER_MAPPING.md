# Render QA Adapter Mapping

## 1. Receipt Names That Overlap

The Remotion / FFmpeg Render Adapter V1.1 already defines:

- `FFprobeValidationReceipt`
- `FrameSamplingReceipt`
- `AudioLevelAnalysisReceipt`
- `DurationToleranceReceipt`
- `RenderQAReport`

Render QA V1 also defines:

- `FFprobeValidationReceipt`
- `FrameSamplingReceipt`
- `AudioLevelAnalysisReceipt`
- `RenderQACompositeReport`

The names overlap, but the scopes differ.

## 2. Canonical Module for V1 Render QA

Canonical operational Render QA V1 contracts live in:

- `src/ccp_studio/contracts/render_qa.py`

The Remotion / FFmpeg adapter contracts remain adapter-level dry-run/runtime-adapter receipts.

## 3. Adapter Receipt Mapping

Implemented bridge:

- `src/ccp_studio/services/render_qa_adapter_bridge_service.py`

Mapping:

- Adapter `FFprobeValidationReceipt` -> `render_qa.FFprobeValidationReceipt`
- Adapter `FrameSamplingReceipt` -> `render_qa.FrameSamplingReceipt`
- Adapter `AudioLevelAnalysisReceipt` -> `render_qa.AudioLevelAnalysisReceipt`
- Adapter `DurationToleranceReceipt` -> `DeliveryPromiseValidationReceipt` duration check
- Adapter `RenderQAReport` -> `RenderQACompositeReport`

## 4. Fields Missing From Adapter Receipts

Adapter receipts do not fully contain:

- `playable`
- `has_video_stream`
- caption burn state
- visual regression screenshot refs
- character identity QA
- motion downgrade state
- V9.1 delivery metrics

The bridge accepts safe defaults or caller-supplied synthetic observations. It does not call external tools.

## 5. Backward Compatibility Plan

- Keep adapter `RenderQAService.compile_report(...)` unchanged.
- Add Render QA V1 builder methods to the existing `RenderQAService`.
- Add bridge service for explicit conversion.
- Do not delete or rename adapter receipts.
- Future real worker observations should populate Render QA V1 receipts after runtime gates pass.

## Safety Confirmation

The bridge does not call ffprobe, FFmpeg, Remotion, providers, subprocesses, or Local Render Worker jobs.
