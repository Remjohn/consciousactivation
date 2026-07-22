# Tech-Spec: FR-ERA3-01 - Webinar Companion Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 3 - Experience Mini Apps
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms all new Mini App routes extend the existing FastAPI app rooted at
                      `src/ccp/api/main.py`, while Section 5.3 reserves `startapp=webinar` for the Webinar Companion.
2. PRD LOADED:        PRD-07 Brownfield exact FR definition:
                      "The Webinar Delivery Pipeline must split the experience into two distinct sovereign surfaces:
                      Coaches broadcast natively from the AFFiNE Studio Block, while the audience consumes and interacts
                      via a Telegram Mini App Webinar Companion."
3. EPIC LOADED:       "Given I am watching a V2WS webinar replay inside the Mini App, When the webinar hits a predefined
                      extraction marker or high-tension moment, Then a timed participation prompt appears as a
                      non-blocking ambient overlay (lower-third bar or slide-in drawer) that never covers the coach's face
                      or primary video focal point..."
4. CBAR LOADED:       Phase3-M01 (Ambient Prompt Rule) and Phase3-M02 (Per-Slide Feedback Rule) confirmed from the
                      Phase 3 audit. Hallucination purge also confirms `EXP-TRB-003` is invalid here and must be
                      corrected to `EXP-TRS-003`, plus all primitive names must follow the YAML registry.
5. PRIMITIVES:        `experience_primitive_id: "EXP-TRS-003"` / `canonical_name: "Reflective Social Proof (The Status Share)"`
                      `experience_primitive_id: "EXP-FBK-001"` / `canonical_name: "RIM Feedback Discipline"`
6. BACKEND:           `src/ccp/services/v2ws_interactive_service.py` - `def create_session(self) -> InteractiveV2WSState`
                      `src/ccp/services/v2ws_yolo_service.py` - `def run_yolo_pipeline(self, intake: YoloIntake) -> V2WSExcalidrawPayload`
                      `src/ccp/services/trait_scoring_engine.py` - `def score_all_traits(self) -> list[ScoredTrait]`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper builders, direct typed
                      assertions, class-per-scenario organization, and local `_run()` wrappers for async service calls.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P3_S15_FR-ERA3-01_Webinar_Companion.md` | 2026-05-11 | Assignment prompt, dual-surface boundary, explicit M-01 and M-02 constraints |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory protocol, Mini App routing, backend extension rules |
| 3 | `docs/prd/modules/PRD_07_V2WS_Webinar.md` | v7.1, 2026-05-07 | Source PRD, 4 operating modes, Brownfield FR definitions, obsolete inventory |
| 4 | `docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md` | 2026-05-10 | Story 1.1 and 1.2 acceptance criteria plus Phase 3 mandates |
| 5 | `docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md` | 2026-05-10 | Audit corrections for M-01/M-02 and primitive hallucination purge |
| 6 | `docs/architecture/FR-CA11-16_CCP_Studio_Block_Tech_Spec.md` | 2026-03-25 | AFFiNE Studio Block recording/broadcasting source surface |
| 7 | `docs/architecture/FR33_YOLO_Webinar_Tech_Spec.md` | 2026-03-13 | Existing YOLO webinar build doctrine and payload shape |
| 8 | `primitives/experience/trust_branding/EXP-TRS-003.yaml` | Codified registry | Verified ambient status/proof primitive referenced by Story 1.1 |
| 9 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Codified registry | Verified per-slide immediacy primitive referenced by Story 1.2 |
| 10 | `src/ccp/services/v2ws_interactive_service.py` | Existing service | Interactive webinar session and module state source |
| 11 | `src/ccp/services/v2ws_yolo_service.py` | Existing service | YOLO-generated webinar payload source |
| 12 | `src/ccp/services/trait_scoring_engine.py` | Existing service | FR61 trait scoring substrate for Rep Mode scorecards |
| 13 | `src/ccp/models/cross_system_models.py` | Existing models | Current V2WS model vocabulary and constants |
| 14 | `src/ccp/api/main.py` | 1.0.0 | FastAPI route registration and `/health` extension point |
| 15 | `src/ccp/core/receipt_chain.py` | Current | Immutable audit trail for prompt, capture, and rep-score events |
| 16 | `src/ccp/scripts/setup_supabase.py` | Current | Existing schema bootstrap and migration extension point |
| 17 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Webinar-adjacent test organization and receipt-chain assertion pattern |
| 18 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Streaming/recording integration test pattern and `_run()` helper style |

## 2. Overview

### 2.1 Problem Statement

The current V2WS backend already knows how to build webinars and how the coach records from AFFiNE, but it does not yet provide the dedicated Telegram consumption surface the PRD explicitly calls for. Without that audience-facing Mini App:
- webinar viewers are pushed out of Telegram into generic external players
- prompt interactions become blocking modals that sever attention from the coach
- replay participation becomes untagged and useless for downstream extraction
- Rep Mode feedback risks drifting into a delayed end-of-session summary instead of actionable slide-level correction

That breaks the core product claim for FR-ERA3-01. The coach can remain in AFFiNE, but the audience still experiences a fragmented, low-conversion webinar flow, and the coach loses the tight rep loop that makes webinars a training surface rather than just a deck artifact.

### 2.2 Solution

This spec creates `startapp=webinar` as the sovereign Telegram Webinar Companion Mini App. It is not a builder. It is the consumption and participation layer for webinar sessions produced upstream by YOLO Build and Interactive Build, and it exposes two strict operating planes:
- **Viewer plane:** live and replay webinar watching with non-blocking participation overlays, polls, and voice-note reactions
- **Rep review plane:** slide-synchronous scorecard delivery triggered by coach-side AFFiNE slide advancement, surfaced through the same companion event stream for mobile review and operator audit

The app reads webinar payloads and timing data from the existing V2WS services, enforces overlay-safe geometry so the speaker remains visually dominant, and defines a deterministic slide-advance event that produces Slide N scoring before Slide N+1 can begin.

### 2.3 Scope

**In scope:**
- `startapp=webinar` Telegram Mini App scaffold and routing
- live and replay webinar session viewing
- timed audience prompts anchored to slide/module/extraction markers
- non-blocking overlay geometry with face/focal-point protection rules
- typed participation capture objects for polls, reactions, CTA clicks, and voice-note submissions
- Rep Mode slide-advance event contract and per-slide scorecard projection
- read-only consumption of YOLO/Interactive webinar payloads and rep state from existing V2WS services
- DPA branding continuity and immutable receipt logging

**Out of scope:**
- webinar generation itself
- AFFiNE Studio Block recording implementation
- CMF extraction rendering internals
- generalized Zoom replacement or arbitrary video conferencing
- modifying `v2ws_yolo_service.py` into a playback system
- monolithic end-of-webinar report UX for Rep Mode

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Data Object | Source FR | What It Does |
|---|---|---|---|
| DEP-WBN-CMP-001 | `WebinarCompanionSessionProjection` | FR-ERA3-01 | Typed projection for a viewer session, acting as the root payload for the Mini App |
| DEP-WBN-CMP-002 | `WebinarPromptAnchor` | Story 1.1 | Timed overlay prompt marker containing specific execution and expiration geometry |
| DEP-WBN-CMP-003 | `ParticipationCaptureRecord` | Story 1.1 | Immutable record of audience reaction, poll choice, or voice-note linked to the active slide |
| DEP-WBN-CMP-004 | `RepSlideAdvanceEvent` | Story 1.2 / Phase3-M02 | Deterministic slide-advance event emitted from the coach-side rep flow |
| DEP-WBN-CMP-005 | `RepSlideScoreCard` | Phase3-M02 | Per-slide rep score feedback surfaced before the next slide can be recorded |
| DEP-WBN-CMP-006 | `VideoRect` (Protected Focal Region) | Phase3-M01 | Defines the non-obstructable video rectangle that overlays may never intersect |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `v2ws_interactive_service.py` | `src/ccp/services/v2ws_interactive_service.py` | Reads `InteractiveV2WSState` session/module progression from the Interactive Build path and uses module indexing as one session source for companion playback |
| `v2ws_yolo_service.py` | `src/ccp/services/v2ws_yolo_service.py` | Reads `V2WSExcalidrawPayload` and generated `WebinarModuleScript` structure from the YOLO path for replay payload hydration |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Supplies FR61 trait evidence used by the new `RepModeScoreAdapter` for per-slide delivery scoring, without modifying the existing engine |
| `cross_system_models.py` | `src/ccp/models/cross_system_models.py` | Reuses `WebinarPart`, `InteractiveModuleState`, `InteractiveV2WSState`, and YOLO constants to avoid inventing a parallel V2WS vocabulary |
| `main.py` | `src/ccp/api/main.py` | Registers the webinar companion router and extends `/health` with viewer-prompt, rep-score, and session-resolution readiness |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs prompt rendered, prompt submitted, voice-note attached, slide advanced, score emitted, and score-acknowledged events |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends the canonical schema with webinar companion tables |
| `FR-CA11-16_CCP_Studio_Block_Tech_Spec.md` | `docs/architecture/FR-CA11-16_CCP_Studio_Block_Tech_Spec.md` | Defines the upstream coach-side AFFiNE surface and recording lifecycle that emits rep data into the companion |
| `FR33_YOLO_Webinar_Tech_Spec.md` | `docs/architecture/FR33_YOLO_Webinar_Tech_Spec.md` | Defines the existing YOLO webinar artifact contract consumed by replay mode |

**Existing database tables consumed:**
- `asset_registry` - webinar deck assets, session assets, downloadable resource links
- `person_registry` - participant identity resolution from Telegram
- `receipt_chain` - immutable event logging
- `resolved_palettes` - DPA theming continuity
- `content_performance` - optional downstream link between extraction markers and resulting content assets

**New companion tables introduced by this spec:**
- `webinar_companion_sessions` - normalized viewer/replay session metadata and focal geometry
- `webinar_participation_captures` - slide-tagged audience responses and CTA interactions
- `webinar_rep_slide_scores` - per-slide rep scorecards keyed to slide advance events
- `webinar_prompt_anchors` - timed overlay prompt markers for live/replay sessions

**Existing API routes extended or called:**
- `GET /health` - extended with webinar companion readiness
- `POST /api/sacred-audio/upload` - audience voice-note reaction ingestion
- `GET /api/webinar/{session_id}` - viewer session projection
- `POST /api/webinar/{session_id}/prompt/{prompt_id}/submit` - ambient prompt response capture
- `POST /api/webinar/rep/{rep_session_id}/slide-advance` - deterministic slide-advance event ingress
- `GET /api/webinar/rep/{rep_session_id}/slide/{slide_index}/score` - per-slide rep scorecard projection

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-TRS-003` | Reflective Social Proof (The Status Share) | trust_branding | Viewer participation prompts must increase identification with the speaker and webinar moment rather than visually competing with it |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Rep Mode scorecards must be relevant to the exact slide, immediate on advance, and actionable before the next slide begins |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| Ambient Prompt Rule | Phase3-M01 | Story 1.1 | All prompts render only inside approved safe zones that are intersect-tested against `ProtectedFocalRegion`. If no safe placement exists, the prompt is deferred to the next anchor rather than displayed over the speaker. Full-screen blocking modals are banned while video is playing. |
| Per-Slide Feedback Rule | Phase3-M02 | Story 1.2 | A deterministic `slide_advanced` event emitted from the coach-side rep flow finalizes Slide N, triggers score generation for Slide N immediately, and blocks Slide N+1 from entering `recordable=true` until Slide N score emission is acknowledged. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| Build one companion app with mode-specific projections rather than separate viewer and rep apps | `startapp=webinar` is the canonical Telegram surface for all webinar consumption states | Create separate `webinar-viewer` and `webinar-rep` Mini Apps | Splits context, duplicates session plumbing, and breaks the dual-interface product claim |
| Treat the companion as read-only relative to webinar generation | The PRD is explicit that builder services already exist | Rebuild webinar planning/generation in the Mini App | Duplicates FR33/FR34 and violates the audience-surface boundary |
| Define `ProtectedFocalRegion` in normalized video coordinates | Overlay safety must work across resolutions and aspect ratios | Hard-code pixel rectangles only | Fails on responsive players and replay scaling |
| Use two approved overlay geometries: lower-third and right drawer | These are the only shapes consistently compatible with the audit language and mobile ergonomics | Arbitrary pop-up modals or centered cards | High risk of obscuring the face and severing attention |
| Trigger rep scoring on `slide_advanced(previous_slide_index)` rather than end-of-session | M-02 requires immediacy tied to the exact slide transition | Batch all 45 minutes and summarize at the end | Mathematically accurate but behaviorally useless |
| Add a `RepModeScoreAdapter` around `TraitScoringEngine` instead of modifying the engine | The existing FR61 engine remains reusable and coach-agnostic | Put webinar-specific per-slide heuristics directly into `TraitScoringEngine` | Couples unrelated surfaces and muddies the FR61 contract |

## 4. Implementation Plan

### Phase 1 - App Scaffold and Session Routing
- [ ] Create `apps/webinar-companion/package.json`
- [ ] Create `apps/webinar-companion/tsconfig.json`
- [ ] Create `apps/webinar-companion/next.config.mjs`
- [ ] Create `apps/webinar-companion/app/layout.tsx`
- [ ] Create `apps/webinar-companion/app/page.tsx`
- [ ] Create `apps/webinar-companion/app/globals.css`

### Phase 2 - Viewer Contracts and Geometry Rules
- [ ] Create `apps/webinar-companion/app/lib/types.ts`
- [ ] Create `apps/webinar-companion/app/lib/api.ts`
- [ ] Create `apps/webinar-companion/app/lib/overlay-geometry.ts`
- [ ] Create `apps/webinar-companion/app/lib/prompt-scheduler.ts`
- [ ] Create `apps/webinar-companion/app/lib/rep-score-state.ts`

### Phase 3 - UI Components
- [ ] Create `apps/webinar-companion/app/components/video-stage.tsx`
- [ ] Create `apps/webinar-companion/app/components/lower-third-prompt.tsx`
- [ ] Create `apps/webinar-companion/app/components/right-drawer-prompt.tsx`
- [ ] Create `apps/webinar-companion/app/components/poll-prompt.tsx`
- [ ] Create `apps/webinar-companion/app/components/voice-note-prompt.tsx`
- [ ] Create `apps/webinar-companion/app/components/replay-timeline.tsx`
- [ ] Create `apps/webinar-companion/app/components/rep-slide-scorecard.tsx`
- [ ] Create `apps/webinar-companion/app/components/downloadables-panel.tsx`

### Phase 4 - Backend Models and Routes
- [ ] Create `src/ccp/models/webinar_companion_models.py`
- [ ] Create `src/ccp/services/webinar_companion_projection.py`
- [ ] Create `src/ccp/api/webinar_companion_api.py`
- [ ] Register webinar companion routes in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with webinar companion tables and indexes

### Phase 5 - Rep Scoring and Verification
- [ ] Create `src/ccp/services/webinar_rep_score_adapter.py`
- [ ] Create `tests/integration/test_era3_fr01_webinar_companion_api.py`
- [ ] Create `tests/integration/test_era3_fr01_webinar_overlay_geometry.py`
- [ ] Create `tests/integration/test_era3_fr01_webinar_rep_scoring.py`
- [ ] Create `apps/webinar-companion/app/__tests__/overlay-geometry.test.tsx`
- [ ] Create `apps/webinar-companion/app/__tests__/prompt-scheduler.test.tsx`
- [ ] Create `apps/webinar-companion/app/__tests__/rep-slide-scorecard.test.tsx`

## 5. Primary Output Schema

**Target model file:** `src/ccp/models/webinar_companion_models.py`

```python
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ResolvedPalette
from src.ccp.models.cross_system_models import WebinarPart


class VideoRect(BaseModel):
    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)
    width: float = Field(..., gt=0.0, le=1.0)
    height: float = Field(..., gt=0.0, le=1.0)


class WebinarPromptAnchor(BaseModel):
    prompt_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    slide_index_start: int = Field(..., ge=0)
    slide_index_end: int = Field(..., ge=0)
    trigger_at_seconds: float = Field(..., ge=0.0)
    prompt_type: Literal["poll", "voice_note", "reaction", "cta"]
    copy: str = Field(..., min_length=1, max_length=280)
    poll_choices: list[str] | None = None
    cta_url: str | None = None
    preferred_geometry: Literal["lower_third", "right_drawer"] = Field(default="lower_third")
    expires_at_seconds: float | None = Field(default=None, ge=0.0)


class ParticipationCaptureRecord(BaseModel):
    capture_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    participant_person_id: str = Field(..., min_length=1)
    prompt_id: str = Field(..., min_length=1)
    module_part: WebinarPart | None = None
    slide_index_start: int = Field(..., ge=0)
    slide_index_end: int = Field(..., ge=0)
    reaction_type: Literal["poll", "voice_note", "reaction", "cta"]
    poll_choice_key: str | None = None
    voice_note_asset_id: str | None = None
    reaction_emoji: str | None = None
    submitted_at: datetime = Field(...)


class RepSlideAdvanceEvent(BaseModel):
    rep_session_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    previous_slide_index: int = Field(..., ge=0)
    next_slide_index: int = Field(..., ge=0)
    previous_slide_started_at: datetime = Field(...)
    previous_slide_stopped_at: datetime = Field(...)
    advanced_at: datetime = Field(...)
    previous_slide_transcript: str = Field(..., min_length=1)


class RepSlideScoreCard(BaseModel):
    rep_session_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    slide_index: int = Field(..., ge=0)
    delivered_at: datetime = Field(...)
    hedge_density: float = Field(..., ge=0.0)
    pause_architecture_score: float = Field(..., ge=0.0, le=100.0)
    cta_pressure_stability: float = Field(..., ge=0.0, le=100.0)
    highlighted_traits: list[str] = Field(default_factory=list)
    feedback_summary: str = Field(..., min_length=1)
    next_slide_unlocked: bool = Field(default=False)


class WebinarCompanionSessionProjection(BaseModel):
    startapp: Literal["webinar"] = Field(default="webinar")
    webinar_id: str = Field(..., min_length=1)
    session_mode: Literal["live_watch", "replay_watch", "rep_review", "extract_review"]
    palette: ResolvedPalette = Field(...)
    video_url: str = Field(..., min_length=1)
    protected_focal_region: VideoRect = Field(...)
    prompt_anchors: list[WebinarPromptAnchor] = Field(default_factory=list)
    participation_open: bool = Field(default=True)
    downloadable_asset_ids: list[str] = Field(default_factory=list)
    current_rep_score: RepSlideScoreCard | None = None
```

**Schema notes:**
- `protected_focal_region` is mandatory in every projection because overlay placement is a first-class safety constraint
- `RepSlideAdvanceEvent` exists even though the coach records from AFFiNE, because the companion must consume the slide transition deterministically
- `RepSlideScoreCard.next_slide_unlocked` is false until the score is emitted and acknowledged

## 6. Backward Compatibility Fallback

This spec follows the explicit fail-closed posture established by `circuit_breaker.py`.

| Failure Mode | Graceful Degradation |
|---|---|
| Prompt placement intersects the protected focal region | The prompt is deferred or re-routed to the secondary safe geometry; it is never rendered over the face |
| Session payload lacks a valid `protected_focal_region` | The companion falls back to the conservative default focal rectangle and suppresses non-essential prompts until corrected |
| Replay marker timing is missing or corrupt | The webinar still plays, but prompt interactions are disabled and the session is marked `participation_open=false` rather than free-floating prompts at unsafe times |
| Per-slide score generation exceeds the immediacy budget (strictly 1500ms) | Slide N+1 remains locked, the UI shows `scoring_in_progress`, and no monolithic end-session report path is allowed to silently replace the missing immediate score |
| Trait scoring dependencies are missing for Rep Mode | The adapter returns a partial deterministic slide scorecard with explicit `trait_score_unavailable=true` metadata and blocks final quality claims that depend on FR61 trait evidence |

## 7. Tasks

### Frontend
- [ ] Build the standalone Webinar Companion Mini App in `apps/webinar-companion/`
- [ ] Add typed viewer, prompt, and rep-score contracts in `apps/webinar-companion/app/lib/types.ts`
- [ ] Implement session and prompt APIs in `apps/webinar-companion/app/lib/api.ts`
- [ ] Implement overlay collision logic in `apps/webinar-companion/app/lib/overlay-geometry.ts`
- [ ] Implement timed replay prompt scheduling in `apps/webinar-companion/app/lib/prompt-scheduler.ts`
- [ ] Implement per-slide score state and acknowledgment flow in `apps/webinar-companion/app/lib/rep-score-state.ts`
- [ ] Build the protected video stage in `apps/webinar-companion/app/components/video-stage.tsx`
- [ ] Build the lower-third prompt surface in `apps/webinar-companion/app/components/lower-third-prompt.tsx`
- [ ] Build the right-drawer prompt surface in `apps/webinar-companion/app/components/right-drawer-prompt.tsx`
- [ ] Build poll and reaction prompt components in `apps/webinar-companion/app/components/poll-prompt.tsx`
- [ ] Build voice-note reaction capture in `apps/webinar-companion/app/components/voice-note-prompt.tsx`
- [ ] Build replay marker and timeline controls in `apps/webinar-companion/app/components/replay-timeline.tsx`
- [ ] Build the per-slide rep scorecard in `apps/webinar-companion/app/components/rep-slide-scorecard.tsx`
- [ ] Build the downloadable resources panel in `apps/webinar-companion/app/components/downloadables-panel.tsx`

### Backend
- [ ] Create `src/ccp/models/webinar_companion_models.py`
- [ ] Create `src/ccp/services/webinar_companion_projection.py`
- [ ] Create `src/ccp/services/webinar_rep_score_adapter.py`
- [ ] Create `src/ccp/api/webinar_companion_api.py`
- [ ] Register webinar companion routes in `src/ccp/api/main.py`
- [ ] Extend `src/ccp/scripts/setup_supabase.py` with `webinar_companion_sessions`, `webinar_participation_captures`, `webinar_rep_slide_scores`, and `webinar_prompt_anchors`
- [ ] Write companion and rep-score receipt events through `src/ccp/core/receipt_chain.py` consumers

### Verification
- [ ] Create `tests/integration/test_era3_fr01_webinar_companion_api.py`
- [ ] Create `tests/integration/test_era3_fr01_webinar_overlay_geometry.py`
- [ ] Create `tests/integration/test_era3_fr01_webinar_rep_scoring.py`
- [ ] Create `apps/webinar-companion/app/__tests__/overlay-geometry.test.tsx`
- [ ] Create `apps/webinar-companion/app/__tests__/prompt-scheduler.test.tsx`
- [ ] Create `apps/webinar-companion/app/__tests__/rep-slide-scorecard.test.tsx`

## 8. Acceptance Criteria

### AC-1.1A - Ambient Webinar Prompts Never Obscure the Speaker's Primary Focal Region

**CBAR Mandate enforced:** Phase3-M01

**Given** I am watching a V2WS webinar replay inside the Mini App,
**When** the webinar hits a predefined extraction marker or high-tension moment,
**Then** the participation prompt renders only as a lower-third or right-drawer ambient overlay,
**And** the rendered prompt rectangle has zero intersection area with the session's `protected_focal_region`,
**And** the coach's face remains fully visible while video playback continues.

**FAILURE EXAMPLE:** A prompt opens as a centered modal over the coach's face during the emotional climax of the teaching sequence. The UI has severed attention from the speaker in order to ask for interaction. This is a spec violation.

**Measurable pass condition:** for every rendered prompt, `intersection(prompt_rect, protected_focal_region) == 0` and the overlay root z-index remains below any full-screen takeover layer because full-screen takeover is banned during active playback.

### AC-1.1B - Participation Captures Are Tagged to the Exact Webinar Moment

**CBAR Mandate enforced:** Phase3-M01

**Given** a viewer submits a poll, reaction, CTA click, or voice-note response from an ambient prompt,
**When** the submission is persisted,
**Then** the capture record includes webinar ID, participant identity, reaction type, and slide/module range,
**And** replay and extraction systems can recover the exact teaching claim the audience responded to.

**FAILURE EXAMPLE:** Audience voice notes are saved with no slide or module tags, so later the team knows that a response happened but not which claim triggered it. The capture is socially interesting but operationally useless. This is a spec violation.

**Measurable pass condition:** every `ParticipationCaptureRecord` row contains non-null `webinar_id`, `participant_person_id`, `reaction_type`, `slide_index_start`, and `slide_index_end`.

### AC-1.2A - Slide N Feedback Is Emitted on Slide Advance Before Slide N+1 Begins

**CBAR Mandate enforced:** Phase3-M02

**Given** the coach is running Rep Mode from the AFFiNE Studio Block,
**When** the coach advances from Slide N to Slide N+1,
**Then** the system emits a `RepSlideAdvanceEvent` finalizing Slide N,
**And** Slide N scoring begins immediately from that event,
**And** Slide N+1 does not become `recordable=true` until the Slide N scorecard has been delivered.

**FAILURE EXAMPLE:** The coach clicks forward from Slide 3 to Slide 4, starts recording Slide 4 immediately, and only later receives a bulk report saying Slide 3 had hedge issues. The feedback arrived too late to change behavior at the relevant moment. This is a spec violation.

**Measurable pass condition:** for each rep transition, `RepSlideScoreCard.slide_index == previous_slide_index`, and `next_slide_unlocked` remains false until the scorecard exists.

### AC-1.2B - Per-Slide Scorecards Are Actionable, Not Monolithic

**CBAR Mandate enforced:** Phase3-M02

**Given** a per-slide rep score is produced,
**When** the scorecard renders,
**Then** it includes hedge density, pause architecture, CTA pressure stability, and a one-line actionable summary for that exact slide,
**And** the system does not defer those metrics into a session-end aggregate as the primary UX.

**FAILURE EXAMPLE:** After a 45-minute rehearsal, the coach receives one long final report with averaged metrics across every slide. The data is too diluted and too delayed to fix the weak transition that happened on Slide 7. This is a spec violation.

**Measurable pass condition:** every `RepSlideScoreCard` is addressable by `slide_index`, includes the named fields, and is retrievable independently before the rep session completes.

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|---|---|---|
| `src/ccp/services/v2ws_interactive_service.py` | Runtime dependency | Interactive webinar session/module structure |
| `src/ccp/services/v2ws_yolo_service.py` | Runtime dependency | YOLO webinar payload and script/module shape |
| `src/ccp/services/trait_scoring_engine.py` | Runtime dependency | Trait evidence substrate for Rep Mode scoring |
| `src/ccp/models/cross_system_models.py` | Model dependency | Existing V2WS enums, constants, and session objects |
| `src/ccp/api/main.py` | Code extension | Router registration and health diagnostics |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Immutable logging for prompt and score events |
| `src/ccp/scripts/setup_supabase.py` | Migration dependency | Canonical place to extend PostgreSQL schema |
| `docs/architecture/FR-CA11-16_CCP_Studio_Block_Tech_Spec.md` | Upstream spec dependency | Coach-side recording and slide-advance event source |
| `docs/architecture/FR33_YOLO_Webinar_Tech_Spec.md` | Upstream spec dependency | YOLO payload assumptions and webinar artifact structure |

### External

| API/Library | Version | Purpose |
|---|---|---|
| Next.js | workspace-pinned | Webinar companion runtime |
| React | workspace-pinned | Viewer, prompt, and scorecard UI |
| TypeScript | workspace-pinned | Typed client contracts |
| FastAPI | existing backend dependency | Webinar companion API routes |
| Pydantic v2 | existing backend dependency | Typed companion models |
| Telegram Web App API | current platform | Mini App launch and identity context |
| HTML5 video | browser capability | Live/replay playback surface |
| Browser `MediaRecorder` | browser capability | Audience voice-note capture |

## 10. Testing Strategy

### Unit Tests

**File:** `apps/webinar-companion/app/__tests__/overlay-geometry.test.tsx`
- `describe("overlay-geometry")`
- `it("places lower-third prompts outside the protected focal region")`
- `it("falls back to right-drawer or deferred mode when a lower-third would intersect the face region")`

**File:** `apps/webinar-companion/app/__tests__/prompt-scheduler.test.tsx`
- `describe("prompt-scheduler")`
- `it("fires prompt anchors at the correct replay timestamps")`
- `it("suppresses expired prompt anchors instead of replaying them late")`

**File:** `apps/webinar-companion/app/__tests__/rep-slide-scorecard.test.tsx`
- `describe("rep-slide-scorecard")`
- `it("blocks next slide unlock until the current slide scorecard exists")`
- `it("renders hedge density, pause architecture, cta pressure stability, and feedback summary per slide")`

### Integration Tests

Modeled explicitly on `tests/integration/test_cpsc_fr52_webinar_brief.py` and `tests/integration/test_ca11_fr16_studio_block.py`:
- use helper builders for sessions, prompt anchors, and rep events
- use local `_run()` wrappers for async service calls
- assert exact typed fields, not vague response blobs
- verify receipt chain side effects directly

**File:** `tests/integration/test_era3_fr01_webinar_overlay_geometry.py`

```python
class TestWebinarOverlayGeometry:
    def test_prompt_never_intersects_protected_focal_region(self): ...
    def test_unsafe_center_modal_layout_is_rejected(self): ...
```

**File:** `tests/integration/test_era3_fr01_webinar_companion_api.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestWebinarCompanionApi:
    def test_prompt_submission_persists_slide_and_participant_tags(self): ...
    def test_voice_note_capture_routes_through_sacred_audio_upload_pattern(self): ...
    def test_replay_session_reads_yolo_or_interactive_payload_without_mutating_builder_state(self): ...
```

**File:** `tests/integration/test_era3_fr01_webinar_rep_scoring.py`

```python
class TestWebinarRepScoring:
    def test_slide_advance_event_generates_score_for_previous_slide_only(self): ...
    def test_next_slide_unlock_waits_for_scorecard_delivery(self): ...
    def test_missing_trait_dependencies_returns_partial_scorecard_with_explicit_degraded_flag(self): ...
```

### Manual Verification

1. Launch the Mini App with `startapp=webinar` from a Telegram webinar share.
2. Confirm the webinar video remains visible and prompts render only in lower-third or right-drawer form.
3. Force a prompt placement case where the lower-third would collide with the focal region and confirm the app re-routes or defers the prompt instead of covering the face.
4. Submit a poll and verify the capture row includes webinar ID, participant ID, prompt ID, and slide range.
5. Submit a voice-note response and confirm the upload follows the existing `sacred-audio` ingestion pattern.
6. Start a replay session and verify prompt anchors reappear at the intended timestamps.
7. Trigger a Rep Mode slide advance from the AFFiNE side and confirm Slide N scoring is emitted before Slide N+1 becomes recordable.
8. Verify the rendered scorecard includes hedge density, pause architecture, CTA pressure stability, and one actionable summary line.
9. Attempt to rely on a session-end monolithic report without per-slide cards and confirm the flow is rejected as non-compliant.
10. Inspect receipt entries and confirm prompt render, prompt submit, slide advance, and score delivery are all logged independently.
