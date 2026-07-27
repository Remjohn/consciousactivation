---
tech_spec_id: "TS-CMF-144"
title: "Video Timeline Workbench Inside Operator Web"
story_id: "15.9"
story_title: "Build the Operator Video Timeline Workbench"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-06"
  - "FR-CMF-07"
  - "FR-CMF-08"
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "video edit review, timeline inspection, timed repair, proxy preview, approval, and OTIO handoff"
entry_object: "VideoEditProgramReviewReadModel, CompositionBeatMap, RendererPropsManifest, OTIOAuditManifest"
exit_object: "VideoTimelineWorkbenchState, TimelineEditCommand, UiActionReceipt, RevisionRequestCommand"
validation_contract: "frame-accurate timeline read model, transcript beat binding, track scope, command-only mutation, proxy/final parity, eval blocker visibility"
required_receipt: "VideoTimelineWorkbenchReceipt"
runtime_target: "React operator-web / generated TypeScript contracts / FastAPI / Pydantic v2 / Command Bus / event stream"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-144: Video Timeline Workbench Inside Operator Web

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture.md` | Defines PWA as the primary deep-work surface and keeps mutations behind the Command Bus. |
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec protocol. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-047-audio-caption-timeline-and-mix-assembly.md` | Audio, caption, timeline, and mix assembly dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | Parent operator UI architecture. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-084-transcript-beat-map-and-timeline-cue-compiler.md` | Source for `CompositionBeatMap`, `TimelineCue`, frame conversion, and transcript-clock truth. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Source for renderer prop manifests, preview/final parity, and component compatibility. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md` | Parent video edit compiler and OTIO/runtime source of truth. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` | Human approval and reviewer protocol dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-136-operator-web-api-client-and-generated-contract-binding.md` | Frontend API client and generated contract dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-139-operator-command-console-and-chat-to-command-proposal-runtime.md` | Command proposal and confirmation dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-140-revision-update-and-repair-workflow-runtime.md` | Revision and repair workflow dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-142-live-operations-event-stream-and-read-model-sync.md` | Live event/read-model sync dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-143-operator-auth-scope-permission-and-contract-version-gates.md` | Auth, scope, permission, consent, and contract-version gates. |
| `THE CMF STUDIO/operator-web/src/App.jsx` | Current React app does not include a true video editing timeline. |
| `THE CMF STUDIO/operator-web/src/data.js` | Current mock video/composition data must become fixture mode only. |

## 2. Overview

The current operator web app can show pipeline state and composition concepts, but it does not yet provide a real video editing timeline. CMF needs a dedicated Video Timeline Workbench where the operator can inspect the actual `VideoEditProgram`: source clips, scene boundaries, transcript beats, caption cues, audio mix, reaction UI timing, subject cutouts, PaperCut or 2D character subscenes, provider assets, eval blockers, proxy preview, and OTIO export status.

This workbench is not a separate video editor that owns truth. It is a controlled operator surface over CMF's backend video edit program. The source of truth remains `VideoEditProgram`, `CompositionBeatMap`, `TimelineCueManifest`, `RendererPropsManifest`, `AudioMixPlan`, `CaptionLayoutPlan`, and `OTIOAuditManifest`. The operator can inspect, scrub, zoom, compare, request repairs, create timed edit drafts, and approve, but every mutation must become a typed command through the Command Bus or a structured revision request.

The workbench must make the four canonical video formats visually and operationally clear:

1. `SV-CSC` Cinematic Story Commentary: scene beats, memory objects, captions, atmosphere, source clips, and emotional pacing.
2. `SV-EDU` Educational / Explainer: PaperCut/2D avatar tracks, diagram objects, rough annotations, teaching labels, and transcript concept timing.
3. `SV-FRB` Challenger / Frame Breaker: proof inserts, contradiction cards, punch-ins, captions, and faster visual emphasis.
4. `SV-RRC` Reaction / Recognition Clip: upper reaction UI, lower human subject cutouts, guest/interviewer interaction, pause emphasis, and reaction timing.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-144-001 | `VideoEditProgramReviewReadModel` | Backend read model that supplies the workbench with current program state. |
| DEP-CMF-144-002 | `CompositionBeatMap` | Source-of-truth transcript beat and frame timing. |
| DEP-CMF-144-003 | `TimelineCueManifest` | Source for caption, camera, cut, layer, UI, SFX, avatar, and PaperCut cues. |
| DEP-CMF-144-004 | `RendererPropsManifest` | Source for proxy preview and final renderer parity. |
| DEP-CMF-144-005 | `AudioMixPlan` | Source for source audio, interviewer audio, music, SFX, silence, ducking, and loudness. |
| DEP-CMF-144-006 | `OTIOAuditManifest` | Source for audit/export coverage and external timeline reconstruction. |
| DEP-CMF-144-007 | `VideoTimelineWorkbenchState` | UI read model consumed by operator-web. |
| DEP-CMF-144-008 | `TimelineEditDraft` | Local, unsaved draft created by drag/split/trim interactions. |
| DEP-CMF-144-009 | `TimelineEditCommand` | Command Bus mutation object created after confirmation. |
| DEP-CMF-144-010 | `VideoTimelineWorkbenchReceipt` | Receipt proving the workbench opened current, scoped, receipt-backed state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `api/v1/video_edit_programs.py` | Add or expose `/review` and `/timeline-workbench` read model endpoint. |
| `contracts/video_edit_program.py` | Add workbench state, track lane, clip segment, timeline edit draft, and command schemas. |
| `services/video_edit_program_service.py` | Build timeline workbench read model from program, beats, cues, captions, audio, render contracts, evals, and OTIO. |
| `services/revision_service.py` | Convert timeline repair requests into structured `RevisionRequestCommand`. |
| `services/operator_ui_service.py` | Create `UiCommandEnvelope` for timeline edit commands. |
| `operator-web/src` | Add dedicated `timeline` route/screen and remove video-timing reliance on mock data. |

### ADR-05 Primitive Implementation

The timeline must expose primitive coverage where the operator makes timed judgments. It should show which primitives justify scene duration, caption emphasis, visual insert, reaction UI, PaperCut object, or cut timing. At least three primitive roles must be visible for composition-bearing video programs:

1. meaning transform;
2. delivery shape;
3. format/material expression.

Each role must reference at least one exact primitive registry identifier, not a fuzzy label. A composition-bearing segment is valid only when it carries at least three distinct primitive IDs across those roles or an explicit blocker explains why the segment cannot yet be approved. The UI must not flatten this into a single "quality score." Primitive failures should appear as track markers and blocker rows tied to exact time ranges.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase1-M01 Optimistic Render | Drag/trim/split actions may create local drafts, but production state changes only after command receipt. |
| Phase1-M05 Deterministic Override | Stale program version blocks edit submit and forces read-model refresh. |
| Phase3-M04 Telemetry Surfacing | Timeline shows live render, provider, eval, revision, and approval events. |
| Phase4-M04 Frictionless Block | Hard blockers appear on the relevant track and disable final approval. |
| Phase4-M05 Actionable Rejection | Timeline blockers include repair target, timestamp, track, and command option. |
| Phase5-M01 Verifiable Artifact | Timeline state links to beat map, renderer props, proxy render, eval receipts, and OTIO manifest. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-06 | Timeline starts from approved expression moments and source-bound transcript beats. |
| FR-CMF-07 | Timeline makes complete editing sessions, scene reproducibility, and composition control inspectable. |
| FR-CMF-08 | Renderer, provider, GPU worker, caption, audio, and asset assembly states are visible without direct worker calls. |
| FR-CMF-09 | Eval, review, revision, approval, and publishing readiness are visible and commandable. |
| FR-CMF-10 | Operations, recovery, event stream, and memory/projection state remain scoped and receipt-backed. |

## 5. Canonical Pipeline Stage Trace

| Stage | Workbench Responsibility |
|---|---|
| Source ingestion | Show source media refs, transcript alignment, timecode origin, and drift warnings. |
| Extraction | Show expression moment boundaries and source evidence for selected clips. |
| Routing | Show format slot, route grammar, primitive obligations, and scene roles. |
| Composition | Show scene/layer tracks, reaction UI, PaperCut/2D character lanes, inserts, masks, and captions. |
| Render | Show proxy render, renderer props hash, render runtime lock, and final render eligibility. |
| Eval/review | Show eval markers, approval blockers, revision commands, and operator approval actions. |
| Export | Show OTIO coverage, export readiness, and final render receipt state. |

## 6. Greenfield Integration and Legacy Migration Context

The workbench belongs inside `THE CMF STUDIO/operator-web`. It may adapt visual ideas from legacy CMF editors or open-source editor references only through CMF specs, generated contracts, and evaluated adapter decisions. It must not import legacy runtime code or treat a browser timeline as the canonical edit engine.

## 7. Architecture Component Map

| Component | Owner | Responsibility |
|---|---|---|
| `VideoTimelineRoute` | `operator-web` | Dedicated route/screen for video edit programs. |
| `TimelineWorkbenchProvider` | `operator-web` | Loads workbench state, live events, command drafts, and active scope. |
| `TimelineRuler` | `operator-web` | Frame/timecode ruler, zoom, playhead, snap indicators. |
| `TrackLaneStack` | `operator-web` | Virtualized lanes for scenes, source clips, captions, audio, SFX, UI, subjects, PaperCut, avatar, evals, and approvals. |
| `ProxyPreviewPanel` | `operator-web` | Synchronized video preview bound to proxy render and playhead. |
| `TranscriptBeatPanel` | `operator-web` | Transcript segments, word/pause markers, expression moments, and source evidence. |
| `TimelineInspector` | `operator-web` | Selected clip/cue/layer details, primitive evidence, receipts, and repair actions. |
| `TimelineCommandBridge` | `operator-web` | Converts confirmed edits into `UiCommandEnvelope` or revision commands. |
| `VideoTimelineWorkbenchService` | Backend | Builds workbench read model and validates command drafts. |

### Concrete Operator-Web File Targets

The current React app only has `src/App.jsx`, `src/data.js`, `src/styles.css`, and `src/main.jsx`. This spec must create a real module boundary instead of adding timeline logic to the monolithic app.

| File Target | Required Responsibility |
|---|---|
| `operator-web/src/screens/VideoTimelineWorkbench.jsx` | Route-level screen that composes preview, transcript, lanes, inspector, and command drawer. |
| `operator-web/src/components/timeline/TimelineWorkbenchProvider.jsx` | Fetches `VideoTimelineWorkbenchState`, subscribes to live events, holds draft state, and exposes refresh/stale state. |
| `operator-web/src/components/timeline/TimelineRuler.jsx` | Frame/timecode ruler with zoom, snap ticks, playhead, and keyboard focus model. |
| `operator-web/src/components/timeline/TrackLaneStack.jsx` | Virtualized lane container for large programs; owns lane height, horizontal scroll, and playhead overlay. |
| `operator-web/src/components/timeline/TimelineTrackLane.jsx` | Renders one lane with locked/editable state, marker overlays, and segment hit targets. |
| `operator-web/src/components/timeline/TimelineSegment.jsx` | Renders clip/cue/marker segments from frame ranges; never stores canonical timing. |
| `operator-web/src/components/timeline/ProxyPreviewPanel.jsx` | Displays signed read-only proxy preview synchronized to the playhead and renderer props hash. |
| `operator-web/src/components/timeline/TranscriptBeatPanel.jsx` | Shows transcript beats, words, pauses, expression moments, and source evidence for selected range. |
| `operator-web/src/components/timeline/TimelineInspector.jsx` | Shows selected segment metadata, primitive IDs, receipts, blockers, and available repairs. |
| `operator-web/src/components/timeline/TimelineCommandDrawer.jsx` | Shows proposed command payload, object version, scope, receipt result, and cancellation. |
| `operator-web/src/api/videoTimeline.js` | Calls read-model, proposal, command, proxy-rerender, and OTIO endpoints through generated contracts. |
| `operator-web/src/state/timelineDraftReducer.js` | Holds local drafts only; reducer output must be serializable to `TimelineEditDraft`. |
| `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js` | Design QA fixture only, guarded by explicit fixture mode and visible fixture banner. |
| `operator-web/src/styles/timeline.css` | Timeline-specific layout, lane, ruler, marker, preview, inspector, and accessibility states. |

## 8. Implementation Plan

1. Add backend contracts for `VideoTimelineWorkbenchState`, `TimelineTrackLane`, `TimelineClipSegment`, `TimelineMarker`, `TimelineEditDraft`, and `TimelineEditCommand`.
2. Add endpoint: `GET /api/v1/video-edit-programs/{program_id}/timeline-workbench`.
3. Add endpoint or command creator for timeline edit drafts: `POST /api/v1/video-edit-programs/{program_id}/timeline-edits/propose`.
4. Add `operator-web` route: `video-timeline` or nested route from the composition/review asset page. The route must run TS-CMF-143 scope and permission preflight before fetching timeline data.
5. Add layout:
   - left rail: program, format, guest scope, approval state;
   - top: proxy preview and transcript beat panel;
   - center: frame-accurate timeline;
   - right: inspector, blockers, receipts, repair actions;
   - bottom or drawer: command proposal/receipt log.
6. Add track lanes:
   - scene boundaries;
   - source video clips;
   - guest/interviewer cutouts;
   - reaction UI;
   - caption/subtitle;
   - audio waveform proxy;
   - music/SFX;
   - PaperCut/2D character;
   - generated inserts;
   - annotations/rough-notation;
   - eval/blocker markers;
   - approval/OTIO markers.
7. Add timeline interactions:
   - scrub/play/pause;
   - zoom in/out;
   - snap to beat, word, pause, scene, or frame;
   - select segment;
   - create edit draft;
   - request repair;
   - submit confirmed command.
8. Add visual composition awareness for all format slots:
   - `SV-CSC`: preview area emphasizes full-frame guest closeups, atmospheric plates, memory inserts, slow push markers, and emotional subtitle lanes;
   - `SV-EDU`: preview area exposes PaperCut/2D avatar lanes, diagram object lanes, rough-notation lanes, metaphor object lanes, and transcript concept timing;
   - `SV-FRB`: preview area exposes proof inserts, contradiction cards, punch-in/punch-out lanes, emphasis captions, and challenger claim markers;
   - `SV-RRC`: preview area exposes upper reaction UI lanes and lower guest/interviewer cutout lanes, with reaction pause markers and eye-line/talk-turn timing.
9. Add live event integration from TS-CMF-142 for render/eval/revision/approval changes.
10. Add fixture mode only for design QA. Production mode must use backend read models; if backend data is unavailable, show an unavailable/stale state instead of silently rendering `data.js`.
11. Add keyboard and accessibility behavior: play/pause, one-frame nudge, beat-jump, lane focus, segment focus, inspector open, repair action, and command drawer confirmation must be keyboard reachable and screen-reader labeled.
12. Add performance rules: timelines with at least 500 segments and 30 lanes must render with lane virtualization, stable dimensions, no horizontal layout shift during scrub, and no full-lane reflow on playhead movement.
13. Add tests for frame alignment, scope isolation, command-only mutation, stale object blocking, blocker visibility, fixture gating, accessibility, and virtualization.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class TimelineTimeRange(BaseModel):
    start_frame: int = Field(ge=0)
    end_frame: int = Field(ge=0)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    source_timecode_start: str | None = None
    source_timecode_end: str | None = None

class TimelineClipSegment(BaseModel):
    schema_version: Literal["cmf.timeline_clip_segment.v1"] = "cmf.timeline_clip_segment.v1"
    segment_id: UUID
    lane_id: str = Field(min_length=1)
    segment_type: Literal[
        "scene",
        "source_clip",
        "caption",
        "audio",
        "music",
        "sfx",
        "reaction_ui",
        "subject_cutout",
        "papercut",
        "avatar",
        "annotation",
        "generated_insert",
        "eval_marker",
        "approval_marker",
        "otio_marker",
    ]
    label: str = Field(min_length=1)
    time_range: TimelineTimeRange
    source_refs: list[str] = Field(default_factory=list)
    primitive_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[UUID] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    locked: bool = False

class TimelineTrackLane(BaseModel):
    schema_version: Literal["cmf.timeline_track_lane.v1"] = "cmf.timeline_track_lane.v1"
    lane_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    lane_kind: Literal[
        "scene",
        "video",
        "subject",
        "ui",
        "caption",
        "audio",
        "animation",
        "asset",
        "eval",
        "approval",
    ]
    editable: bool
    edit_policy_ref: str | None = None
    segments: list[TimelineClipSegment] = Field(default_factory=list)

class TimelineMarker(BaseModel):
    schema_version: Literal["cmf.timeline_marker.v1"] = "cmf.timeline_marker.v1"
    marker_id: UUID
    marker_type: Literal[
        "primitive_pass",
        "primitive_fail",
        "eval_blocker",
        "approval_blocker",
        "stale_state",
        "proxy_final_mismatch",
        "otio_gap",
        "receipt",
        "operator_note",
    ]
    lane_id: str | None = None
    time_range: TimelineTimeRange
    severity: Literal["info", "warning", "hard_blocker"]
    label: str = Field(min_length=1)
    primitive_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[UUID] = Field(default_factory=list)
    repair_command_type: str | None = None

class VideoTimelineWorkbenchState(BaseModel):
    schema_version: Literal["cmf.video_timeline_workbench_state.v1"] = "cmf.video_timeline_workbench_state.v1"
    workbench_id: UUID
    program_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID
    format_slot: Literal["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"]
    fps: int = Field(gt=0)
    duration_frames: int = Field(gt=0)
    duration_ms: int = Field(gt=0)
    object_version: str
    proxy_render_ref: str | None = None
    renderer_props_manifest_ref: str | None = None
    beat_map_ref: str
    otio_manifest_ref: str | None = None
    lanes: list[TimelineTrackLane]
    markers: list[TimelineMarker] = Field(default_factory=list)
    selected_segment_id: UUID | None = None
    playback_proxy_status: Literal["missing", "ready", "stale", "failed"]
    contract_gate_status: Literal["valid", "stale_contract", "scope_blocked", "permission_blocked"]
    hard_blocker_codes: list[str] = Field(default_factory=list)
    next_valid_commands: list[str] = Field(default_factory=list)
    built_at: datetime

class TimelineEditDraft(BaseModel):
    schema_version: Literal["cmf.timeline_edit_draft.v1"] = "cmf.timeline_edit_draft.v1"
    draft_id: UUID
    program_id: UUID
    target_segment_id: UUID
    edit_type: Literal["trim", "split", "move", "replace_asset", "adjust_caption", "adjust_audio", "request_repair", "rerender_proxy", "export_otio"]
    proposed_time_range: TimelineTimeRange | None = None
    payload: dict = Field(default_factory=dict)
    expected_object_version: str
    blocker_codes: list[str] = Field(default_factory=list)

class TimelineEditCommand(BaseModel):
    schema_version: Literal["cmf.timeline_edit_command.v1"] = "cmf.timeline_edit_command.v1"
    command_id: UUID
    draft_id: UUID
    program_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID
    target_segment_id: UUID | None = None
    edit_type: Literal["trim", "split", "move", "replace_asset", "adjust_caption", "adjust_audio", "request_repair", "rerender_proxy", "export_otio"]
    expected_object_version: str
    expected_renderer_props_hash: str | None = None
    expected_scope_ref: str
    payload: dict = Field(default_factory=dict)
    submitted_by_operator_id: UUID

class VideoTimelineWorkbenchReceipt(BaseModel):
    schema_version: Literal["cmf.video_timeline_workbench_receipt.v1"] = "cmf.video_timeline_workbench_receipt.v1"
    receipt_id: UUID
    workbench_id: UUID
    program_id: UUID
    object_version: str
    source_receipt_refs: list[UUID] = Field(default_factory=list)
    read_model_hash: str
    created_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `OpenVideoTimelineWorkbenchCommand` | Opens scoped workbench and writes `VideoTimelineWorkbenchReceipt`. |
| `ProposeTimelineEditCommand` | Creates a draft for trim/split/move/replace/caption/audio/repair. |
| `SubmitTimelineEditCommand` | Converts confirmed draft into backend command. |
| `RevisionRequestCommand` | Used when the edit is a repair, not a direct timing adjustment. |
| `RenderProxyCommand` | Requests deterministic proxy rerender after accepted edit. |
| `ExportOTIOCommand` | Requests OTIO audit export. |
| `timeline.workbench.opened` | Event emitted when current workbench state is built. |
| `timeline.edit.receipted` | Event emitted after accepted edit command. |
| `timeline.state.stale` | Event emitted when live version differs from loaded workbench state. |

### Command Submission Rules

Every submitted `TimelineEditCommand` must include:

1. `program_id`, `brand_workspace_id`, and `guest_id` matching the active operator scope;
2. `expected_object_version` matching the loaded workbench state;
3. `expected_renderer_props_hash` when the command can affect proxy/final render parity;
4. an idempotency key supplied by the Command Bus client;
5. a receipt target so the UI can refresh from accepted backend state.

If any value is missing or stale, the backend must reject the command with an actionable error and emit `timeline.state.stale` or a permission/scope blocker event.

## 11. DSPy Programs, JIT Skills, or Deterministic Services

No DSPy or JIT skill runs in the browser. A timeline repair may request an agent/JIT-backed proposal, such as caption rewrite, narrative pacing repair, or composition repair, but the browser only submits the command. Deterministic services own frame conversion, snap rules, proxy render validation, and OTIO coverage checks.

## 12. Provider, Renderer, Projection, or Worker Boundaries

The workbench never calls Remotion, Motion Canvas, FFmpeg, ComfyUI, SAM3, Qwen, provider APIs, or object storage directly. It calls CMF APIs and displays receipt-backed status. Proxy previews are signed/read-only media refs. Final renders are created only by backend workflows after approval gates pass.

Telegram integration is limited to notification, quick status, and deep-link handoff into the PWA workbench. Telegram must not expose frame-level drag/trim/split controls, cannot submit `TimelineEditCommand`, and cannot approve a final video when timeline hard blockers exist. Telegram repair buttons may only create the same scoped `RevisionRequestCommand` path defined by TS-CMF-140.

Fixture mode is not a fallback for production. `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js` may be used for local visual QA only when an explicit fixture flag is enabled and the UI displays a persistent fixture banner. Production unavailable states must show stale/offline/retry controls and must not imply the timeline is current.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Operators need hands-on timeline control, but the browser cannot become the source of truth. |
| Failure Scenario | Operator drags a caption and the app mutates local state without backend receipt. |
| Resolution Demand | Drag creates `TimelineEditDraft`; submit creates command envelope; receipt refreshes workbench state. |
| Downstream Proof | Workbench shows command receipt, updated object version, proxy hash, and eval state. |

### Executable Gate Thresholds

| Gate | Threshold | Downstream Consequence |
|---|---|---|
| Frame alignment | Segment start/end must match `CompositionBeatMap` frame values exactly for locked segments and be within `1` frame for provisional draft previews. | Block submit when outside tolerance. |
| Primitive coverage | Composition-bearing segment must expose at least `3` distinct primitive IDs across meaning, delivery, and material/expression roles. | Add hard blocker marker until coverage or exception receipt exists. |
| Proxy/final parity | Loaded proxy `renderer_props_hash` must equal the active `RendererPropsManifest` hash. | Disable final approval and offer proxy rerender command. |
| Stale state | `expected_object_version` must equal current backend object version at submit time. | Reject command and force read-model refresh. |
| Scope isolation | `program_id`, `brand_workspace_id`, and `guest_id` must match active operator scope. | Reject read model or command and record scope blocker. |
| Hard blocker approval | `hard_blocker_codes` must be empty before final approval/export. | Disable approval/export actions. |
| OTIO coverage | OTIO manifest must cover `100%` of accepted source clip, caption, audio, and renderer prop references. | Disable final export and show OTIO gap marker. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC144-01 | Workbench loads from backend `VideoTimelineWorkbenchState`, not mock `data.js`, in production mode. | Timeline renders from local fixtures as if live. | Phase5-M01 |
| AC144-02 | Timeline shows scene, source clip, caption, audio, UI, subject, animation, eval, and approval lanes when present. | Reaction clip shows only a flat preview. | Phase3-M04 |
| AC144-03 | Playhead, ruler, and selected segments use frame/timecode values from `CompositionBeatMap`. | UI uses approximate CSS percentages with no frame refs. | Phase1-M05 |
| AC144-04 | Drag/trim/split actions create draft commands, not direct state mutation. | Segment moves permanently before receipt. | Phase5-M01 |
| AC144-05 | Stale object version blocks edit submission and refreshes state. | Operator edits old proxy after backend rerender. | Phase1-M05 |
| AC144-06 | Hard blockers appear on exact lanes/time ranges and disable final approval. | Approval button enabled while caption blocker exists. | Phase4-M04 |
| AC144-07 | Workbench can request structured repairs for timing, caption, audio, layer, provider, primitive, render, and OTIO targets. | Operator only gets generic "try again" action. | Phase4-M05 |
| AC144-08 | Proxy preview and timeline state share renderer props hash. | Operator approves preview A while final render uses props B. | Phase5-M01 |
| AC144-09 | OTIO coverage status is visible before final export. | Final video is approved without OTIO audit status. | Phase5-M01 |
| AC144-10 | Cross-guest scope is impossible. | Claude timeline displays Adele source clip. | Phase4-M04 |
| AC144-11 | The operator-web implementation creates the dedicated timeline module files listed in Section 7 instead of adding all logic to `App.jsx`. | Timeline code is embedded inside the monolithic app and cannot be tested independently. | Phase3-M04 |
| AC144-12 | Production mode cannot silently render fixture timeline data. | Backend is unavailable but fixture data appears as live truth. | Phase5-M01 |
| AC144-13 | Telegram can deep-link to the PWA workbench but cannot perform frame-level timeline edits or final approval. | Telegram button submits a trim command directly. | Phase4-M04 |
| AC144-14 | Keyboard users can scrub, focus lanes, select segments, inspect blockers, and submit/cancel drafts without pointer-only controls. | Drag-only timeline prevents keyboard repair of a caption blocker. | Phase4-M05 |
| AC144-15 | A timeline with at least 500 segments across 30 lanes remains usable with virtualization and stable lane dimensions. | Scrubbing causes full timeline reflow and visible lane jump. | Phase3-M04 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-047 | Audio/caption/timeline/mix manifests. |
| TS-CMF-084 | Transcript beat map and timeline cue compiler. |
| TS-CMF-090 | Renderer prop compiler and component harness. |
| TS-CMF-106 | Video edit program compiler, OTIO, and render runtime. |
| TS-CMF-132 | Human approval and reviewer protocol. |
| TS-CMF-136 | Operator-web API client and generated contracts. |
| TS-CMF-137 | Backend production composition root. |
| TS-CMF-140 | Revision and repair workflow runtime. |
| TS-CMF-142 | Live operations event stream. |
| TS-CMF-143 | Auth, scope, permission, and contract version gates. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Contract | Generated frontend types include all workbench state and edit draft schemas. |
| Unit | Frame-to-pixel and pixel-to-frame conversion is stable across zoom levels. |
| Unit | Snap rules target frame, beat, word, pause, and scene boundaries. |
| Component | Track lanes render large timelines with virtualization and no layout shift. |
| Component | Drag/trim creates `TimelineEditDraft` and does not mutate canonical state. |
| Component | Fixture banner appears in fixture mode and production mode refuses fixture data. |
| Accessibility | Keyboard can focus lanes, move playhead by frame/beat, open inspector, and submit/cancel draft commands. |
| Performance | 500 segments across 30 lanes scrub without full-lane reflow or timeline dimension changes. |
| Integration | Submit edit command returns `UiActionReceipt` and refreshes workbench state. |
| Integration | Live event updates render/eval/revision status. |
| Integration | Telegram deep link opens scoped PWA timeline but cannot submit `TimelineEditCommand`. |
| Negative | Cross-guest timeline data is rejected. |
| Negative | Stale object version blocks command submit. |
| Negative | Missing primitive IDs create hard blocker markers on the relevant time range. |
| E2E | Operator opens video program, scrubs proxy, selects caption blocker, submits repair, sees receipt and refreshed state. |

## 17. Observability, Recovery, and Rollback

1. Log workbench open, command draft, command submit, receipt, stale state, and refresh events with correlation ids.
2. Show offline/reconnecting/stale status clearly.
3. Keep unsent edit drafts local only until scope, object version, or route changes.
4. Roll back a failed accepted edit through `RevisionRequestCommand` or workflow recovery, not direct browser state revert.
5. If proxy media fails to load, keep timeline and evidence inspectable and offer rerender/refresh commands.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-144 |
| Protocol | CMF/ERA3 18-section spec |
| Files read declared | Yes |
| FR-CMF trace declared | Yes |
| Pipeline trace declared | Yes |
| Command Bus boundary | Preserved |
| Browser as source of truth | Prohibited |
| Timeline mutation mode | Draft command then receipt |
| Video format coverage | `SV-CSC`, `SV-EDU`, `SV-FRB`, `SV-RRC` |
| 5-lens audit status | revised after audit |
| Status | ready-for-development |
