---
tech_spec_id: "TS-CMF-080"
title: "Composition Template Runtime, Transcript Timing, and Brand Genesis Binding"
story_id: "7.10"
story_title: "Composition Template Runtime Binding"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "source-trace repair after composition gap audit"
fr_ids:
  - "FR-CMF-04.02"
  - "FR-CMF-04.03"
  - "FR-CMF-04.04"
  - "FR-CMF-06.05"
  - "FR-CMF-06.06"
  - "FR-CMF-07.02"
  - "FR-CMF-07.03"
  - "FR-CMF-07.04"
  - "FR-CMF-07.08"
  - "FR-CMF-07.09"
  - "FR-CMF-08.02"
  - "FR-CMF-08.08"
  - "FR-CMF-09.01"
  - "FR-CMF-09.03"
pipeline_stage: "8 / 9 / 10 / 11 / 12"
entry_object: "approved ExpressionMoment, locked BrandContextVersion, VisualFeelContract, CompositionTemplateJson"
exit_object: "CompositionRuntimeBindingReceipt, renderer props, eval blockers, render-ready template"
validation_contract: "source lineage, Brand Genesis substrate, primitive triad, transcript timing, renderer adapter boundary"
required_receipt: "CompositionRuntimeBindingReceipt"
runtime_target: "Python / Pydantic v2 / JSON Schema / Remotion / Motion Canvas / adapter registry / eval harness"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-080: Composition Template Runtime, Transcript Timing, and Brand Genesis Binding

**Status:** Ready for Development  
**Implementation Boundary:** Bind every composition template and renderer component to Brand Genesis substrate, V9/V9.1 expression lineage, transcript timing, primitive obligations, renderer routes, and open-source adapter decisions.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Context Version, 64-state acting library, Paper-Cut rig, props, micro-semiotic anchors, Ideogram 4, GPT Image 2, Flux/ComfyUI, layer extraction, renderer routing, evals, JSON contract chain. |
| `THE CMF STUDIO/CCP V9 - Interview-First Expression Engine.md` | Narrative State Induction, expression state vs archetype doctrine, Interview Asset Contract, Complete Expression Session, Matrix of Edging integration, V9 CMF input change, agent roles, eval doctrine. |
| `THE CMF STUDIO/CCP V9.1 - Expression Capture & Archetype Routing Update.md` | Complete Expression Session V2, recording config, quality gate, asset contract schema, required registries, four-video package logic, reaction seeds, CMF handoff object, eval requirements. |
| `THE CMF STUDIO/docs/audits/CMF_COMPOSITION_SOURCE_TRACE_GAP_AUDIT_2026-06-24.md` | Gap map and required repair target. |
| `docs/tech-specs/TS-CMF-020-paper-cut-rig-and-creative-libraries.md` | Rig, creative library, micro-semiotic, motion/SFX, and platform profile dependency. |
| `docs/tech-specs/TS-CMF-038-ideogram-4-compositionjob-lineage.md` | Ideogram 4 CompositionJob lineage and final text/identity boundaries. |
| `docs/tech-specs/TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | Canonical composition JSON and approval lifecycle. |
| `docs/tech-specs/TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` | Open-source candidate governance and adapter decision receipts. |
| `docs/tech-specs/TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Doctrine and primitive eval harness. |
| `docs/tech-specs/TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` | Four-video slot runtime and doctrine crosswalk. |
| `docs/tech-specs/TS-CMF-079-route-specific-visual-feel-and-primitive-composition-gates.md` | Route feel contract and primitive composition gate. |

## 2. Problem Statement

CMF STUDIO cannot approve composition templates merely because a still image or mockup looks good. A production composition must prove where it came from, which interview moment it serves, which brand substrate it uses, which primitives it validates, how transcript timing controls the scene, which renderer compiles it, and which open-source components are allowed to assist.

This spec turns visual compositions into runtime objects.

It explicitly repairs the failure mode where:

- Paper-Cut becomes a flat aesthetic instead of a rigged Brand Genesis system;
- reaction templates become generic viral UI instead of interview-timed human proof;
- Ideogram plates become final text or identity truth;
- open-source projects are implied but not governed;
- transcript timing, anchors, and expression moments are not mapped into renderer props.

## 3. Canonical Runtime Chain

Every composition-bearing object must belong to this chain:

```text
BrandGenesisSession
-> BrandContextVersion
-> CompleteExpressionSession
-> InterviewAssetContract
-> ExpressionMoment
-> ArchetypeRoute
-> AssetPackageSpec
-> CompleteEditingSession
-> SceneSpec
-> VisualFeelContract
-> CompositionTemplateJson
-> CompositionRuntimeBinding
-> LayerManifest
-> AnimationPlan
-> RendererProps
-> RenderJob
-> EvaluationReceipt
-> ApprovalEvent
-> PublishingIntent
-> BrandMemoryEvent
```

If any upstream object is missing, the composition is draft-only and cannot enter render.

## 4. Source Authority Rules

### 4.1 Brand Genesis Rules

Every composition template must bind a locked `BrandContextVersion` and prove selected creative assets come from that version.

Required Brand Genesis substrate:

- identity pack;
- 64-state acting library;
- Paper-Cut avatar rig, when used;
- visual constitution;
- micro-semiotic anchor library;
- motion library;
- SFX library;
- composition preference library;
- platform profile;
- source/eval/approval receipts for selected assets.

The backend must retrieve, compose, animate, evaluate, and remember from approved Brand Context. It must not reinvent the brand per template.

### 4.2 V9 / V9.1 Expression Rules

Every composition template must bind to:

- Complete Expression Session;
- Interview Asset Contract;
- source Expression Moment;
- transcript segment and timestamp range;
- First-Line Anchor or explicit source-start rationale;
- Depth Anchor or depth-eval rationale;
- expression state;
- core content archetype;
- asset derivative;
- CMF render route;
- four-video slot when producing Guest Asset Pack videos;
- primitive coalition and edge product;
- asset route rationale;
- evaluation requirements.

The correct chain is:

```text
Expression State -> Archetype Route -> Asset Contract -> Expression Moment -> Complete Editing Session -> Composition Runtime
```

Expression state is not the asset type.

### 4.3 Pricing and Format Override

Older source examples may mention outdated pricing or newsletters. Current product rules override those examples:

- subscription content charge: `$99/month`;
- trial guest packs: `$29/week`;
- newsletters are not a valid required CMF output format;
- output formats must use the documented valid content formats and registries.

## 5. Primary Contracts

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class RendererTarget(str, Enum):
    remotion = "remotion"
    motion_canvas = "motion_canvas"
    manim = "manim"
    gpu_batch_worker = "gpu_batch_worker"


class BrandGenesisSubstrateBinding(BaseModel):
    schema_version: Literal["cmf.brand_genesis_substrate_binding.v1"]
    brand_id: UUID
    brand_context_version_id: UUID
    brand_context_hash: str
    identity_pack_id: UUID
    acting_library_version_id: UUID | None = None
    selected_acting_reference_ids: list[UUID] = Field(default_factory=list)
    papercut_avatar_rig_id: UUID | None = None
    selected_avatar_state_ids: list[UUID] = Field(default_factory=list)
    visual_constitution_id: UUID
    micro_semiotic_anchor_ids: list[UUID] = Field(default_factory=list)
    micro_semiotic_no_anchor_rationale: str | None = None
    motion_recipe_id: UUID | None = None
    sfx_library_id: UUID | None = None
    composition_preference_library_id: UUID | None = None
    platform_profile_id: UUID
    creative_receipt_ids: list[UUID]
    forbidden_style_drift: list[str]


class ExpressionLineageBinding(BaseModel):
    schema_version: Literal["cmf.expression_lineage_binding.v1"]
    complete_expression_session_id: UUID
    interview_asset_contract_id: UUID
    expression_moment_id: UUID
    transcript_segment_ids: list[UUID]
    clip_start_timestamp_ms: int
    clip_end_timestamp_ms: int
    timestamped_anchor_hit_id: UUID | None = None
    first_line_anchor_text: str | None = None
    depth_anchor_ref: str | None = None
    target_expression_states: list[str]
    core_archetype: str
    asset_derivative: str
    cmf_route: str
    four_video_slot_code: Literal["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"] | None = None
    edge_product: str
    primitive_coalition_refs: list[str]
    reaction_seed_id: UUID | None = None
    route_rationale: str
    evaluation_requirement_refs: list[str]


class LayerCue(BaseModel):
    schema_version: Literal["cmf.layer_cue.v1"]
    layer_ref: str
    action: str
    start_frame: int
    end_frame: int
    easing: str | None = None
    source_evidence_ref: str
    primitive_refs: list[str]


class CompositionBeat(BaseModel):
    schema_version: Literal["cmf.composition_beat.v1"]
    beat_id: UUID
    transcript_segment_id: UUID
    spoken_role: Literal["guest", "interviewer", "narrator", "system_caption"]
    start_timestamp_ms: int
    end_timestamp_ms: int
    start_frame: int
    end_frame: int
    semantic_function: str
    visual_action: str
    caption_cue_refs: list[str] = Field(default_factory=list)
    layer_cues: list[LayerCue] = Field(default_factory=list)
    sfx_cue_refs: list[str] = Field(default_factory=list)
    primitive_refs: list[str]


class OpenSourceAdapterBinding(BaseModel):
    schema_version: Literal["cmf.open_source_adapter_binding.v1"]
    candidate_id: str
    decision_receipt_id: UUID
    allowed_use: str
    prohibited_use: str
    runtime_boundary: str


class CompositionRuntimeBinding(BaseModel):
    schema_version: Literal["cmf.composition_runtime_binding.v1"]
    composition_runtime_binding_id: UUID
    composition_template_id: UUID
    visual_feel_contract_id: UUID
    composition_preflight_receipt_id: UUID
    brand_substrate: BrandGenesisSubstrateBinding
    expression_lineage: ExpressionLineageBinding
    beat_map: list[CompositionBeat]
    renderer_targets: list[RendererTarget]
    renderer_props_uri: str | None = None
    layer_manifest_id: UUID | None = None
    animation_plan_id: UUID | None = None
    open_source_adapter_bindings: list[OpenSourceAdapterBinding] = Field(default_factory=list)
    eval_obligation_refs: list[str]
    blocker_codes: list[str] = Field(default_factory=list)
    state: Literal["draft", "bound", "blocked", "render_ready", "superseded"]
    runtime_hash: str


class CompositionRuntimeBindingReceipt(BaseModel):
    schema_version: Literal["cmf.composition_runtime_binding_receipt.v1"]
    receipt_id: UUID
    composition_runtime_binding_id: UUID
    composition_template_id: UUID
    brand_context_version_id: UUID
    expression_moment_id: UUID
    visual_feel_contract_id: UUID
    primitive_eval_receipt_id: UUID
    adapter_decision_receipt_ids: list[UUID]
    renderer_target_summary: list[str]
    blocker_codes: list[str]
    decision: Literal["allow_renderer_props", "blocked", "needs_repair"]
    written_at: datetime
```

## 6. Four-Video Template Families

The 24 previsual composition directions become production candidates only when converted into JSON and runtime bindings.

| Slot | Template Codes | Primary Renderer | Required Runtime Substrate |
|---|---|---|---|
| `SV-CSC` Cinematic Story Commentary | `SV-CSC-CIN-001` through `SV-CSC-CIN-006` | Remotion | Expression Moment, memory/tension beat map, cinematic caption plan, optional B-roll/plate, source-backed emotion pacing. |
| `SV-EDU` Educational / Paper-Cut / Animated Avatar Explainer | `SV-EDU-PAP-001` through `SV-EDU-PAP-006` | Motion Canvas or Remotion | Locked rig, paper layer manifest, props, micro-semiotic anchors, motion recipe, SFX, teaching beat map. |
| `SV-FRB` Challenger / Frame Breaker | `SV-FRB-CHL-001` through `SV-FRB-CHL-006` | Remotion | False belief object, evidence/receipt layers, proof cards, reframe beats, source claim support, Matrix edge. |
| `SV-RRC` Reaction / Recognition Clip | `SV-RRC-RCT-001` through `SV-RRC-RCT-006` | Remotion reaction renderer | Upper reaction UI, lower human proof, background-removed guest/interviewer or guest-only cutouts, interaction beat sync. |

## 7. Renderer Routing

| Route | Default Runtime | Conditions |
|---|---|---|
| Cinematic Story Commentary | Remotion | Uses transcript-timed captions, B-roll plates, memory objects, controlled pacing, audio mix, and final export. |
| Paper-Cut Explainer | Motion Canvas or Remotion | Requires Paper-Cut rig/layers/motion/SFX. Motion Canvas is preferred for procedural paper/vector motion; Remotion can assemble final video and captions. |
| Animated Avatar Explainer | Motion Canvas or Remotion | Requires avatar rig, mouth/eye/body layers, expression state, and rig preview pass. |
| Challenger / Frame Breaker | Remotion | Uses evidence panels, receipts, contradiction maps, proof cards, title punches, and source-backed claims. |
| Living Commentary Reaction | Remotion | Uses real human footage, background removal when needed, authentic pauses, quote highlights, and subtle emphasis. |
| Conscious Reactions Editing | Remotion reaction renderer, with optional Motion Canvas mechanics | Uses poll/ranking/quiz/debate UI plus timed human reaction layer. |
| Data Story / Procedural Framework | Manim or Motion Canvas | Use only when the source moment requires procedural diagrams, timelines, charts, or abstract explanation. |
| Cinematic Metaphor | GPU/video-generation worker or Remotion plate | Allowed for non-editable metaphor/B-roll only. Do not use for final text, final identity, or reusable layer control. |

## 8. Transcript Timing and Beat Mapping

Every renderer prop file must be derived from transcript timing and beat maps.

Required timing steps:

1. Align source transcript to master recording.
2. Select Expression Moment timestamp range.
3. Validate clip start against First-Line Anchor or approved start rationale.
4. Split the moment into `CompositionBeat` objects.
5. Convert timestamps to frames using renderer FPS.
6. Assign each beat a semantic function:
   - hook;
   - memory image;
   - claim;
   - proof;
   - myth;
   - reversal;
   - teaching step;
   - reaction prompt;
   - human pause;
   - CTA.
7. Bind each beat to layer cues, caption cues, SFX cues, and primitive refs.
8. Emit renderer props and hash them.

Rules:

- Captions must never invent meaning beyond source transcript or approved copy.
- Visual reveals must match what the guest/interviewer is saying at that beat.
- Reaction UI must correspond to the question, answer, pause, or reaction seed.
- Paper-Cut object reveals must serve teaching clarity or metaphor, not decoration.
- Challenger proof cards must be backed by transcript evidence or approved research evidence.

## 9. Open-Source Adapter Use Map

| Candidate | Allowed Use in Composition Runtime | Prohibited Use |
|---|---|---|
| `apps/react-debate`, `react-tierlist`, `react-ranking-quiz`, `react-blind-rank`, `react-elimination`, `react-authority-quiz`, `react-mirror-quiz` | Convert mechanics into JSON-defined Remotion/Motion Canvas components for Conscious Reactions templates. | Directly importing app state as CMF truth or using mechanic without source Expression Moment. |
| `openvideodev/react-video-editor`, `openvideodev/openvideo` | Operator timeline UI reference or leaf editing UI after adapter approval. | Replacing CMF transcript, EDL, SceneSpec, CompositionTemplateJson, or RendererProps. |
| `OmniShotCut`, `video-use`, `yt-short-clipper`, `AI-Youtube-Shorts-Generator` | Lab evaluation for clip discovery, automated editing assistance, or fixture comparison. | Production use on guest data without adapter decision receipt. |
| `Manim` | Procedural data, framework, timeline, and abstract explainer animations. | Default Paper-Cut, reaction, or cinematic story renderer. |
| `hyperframes` | Reference/lab for scene/frame generation ideas. | Source of truth for scene structure or approval. |
| `stretchystudio` | 2D rigging reference for paper/avatar motion. | Bypassing CMF `RigManifest` and preview tests. |
| `see-through` | Layer decomposition and transparent layer extraction candidate. | Accepting layers without CMF `LayerManifest` scores and review. |
| `SCAIL-2` | Motion transfer for memes, dancing motions, reaction clips, recurring motion formats. | Default cinematic, identity, Paper-Cut, or final render engine. |
| `searxng`, `Gen-Searcher`, `last30days-skill`, `Open-Generative-AI` | CRAL/SVRE/Aurore/Audience Reality research retrieval with evidence receipts. | Unattributed research, hidden search state, or direct claims in render without evidence. |
| `delta-Mem` | Reference for memory design and comparison. | Direct memory runtime replacement without CMF memory admission, quarantine, and evidence contracts. |

No adapter can be used in a production runtime binding without `IntegrationAdapterDecisionReceipt`.

## 10. Required Approval Blockers

| Blocker | Trigger |
|---|---|
| `COMPOSITION_SOURCE_LINEAGE_MISSING` | Missing CES, Interview Asset Contract, Expression Moment, transcript segment, or timestamp range. |
| `BRAND_GENESIS_SUBSTRATE_MISSING` | Missing locked Brand Context Version or required creative substrate. |
| `ACTING_STATE_BINDING_MISSING` | Human/avatar state is used without acting reference, emotion/gesture, or state metadata. |
| `PAPERCUT_RIG_BINDING_MISSING` | Paper-Cut/Animated Avatar route lacks rig manifest, layer manifest, preview tests, or motion recipe. |
| `MICRO_SEMIOTIC_ANCHOR_NOT_APPROVED` | High-identification composition uses unapproved anchor, dominant anchor, stereotype, or legal-risk anchor. |
| `TRANSCRIPT_TIMING_MISSING` | Renderer props cannot map beats to transcript timestamps and frames. |
| `PRIMITIVE_TRIAD_NOT_VALIDATED` | Fewer than three primitive obligations pass across meaning, delivery, and material/format. |
| `OPEN_SOURCE_ADAPTER_DECISION_MISSING` | Template uses open-source-derived component or logic without decision receipt. |
| `IDEOGRAM_FINAL_TEXT_OR_IDENTITY_DRIFT` | Ideogram plate is used as final text or final identity without downstream text/identity boundary. |
| `ROUTE_FEEL_COLLAPSE` | Template borrows another slot's visual grammar or generic social style. |
| `RENDER_EVAL_RECEIPT_MISSING` | Render output lacks required evaluation receipt. |

## 11. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `BindCompositionRuntimeCommand`, `GenerateCompositionBeatMapCommand`, `ValidateBrandSubstrateBindingCommand`, `ValidateExpressionLineageBindingCommand`, `ValidateOpenSourceAdapterBindingsCommand`, `EmitRendererPropsCommand`, `RecordCompositionRuntimeBindingReceiptCommand` |
| Events | `CompositionRuntimeBound`, `CompositionRuntimeBlocked`, `CompositionBeatMapGenerated`, `RendererPropsEmitted`, `CompositionRuntimeBindingReceiptRecorded` |
| Workflow | Stage 10 composition runtime binding before Stage 11 renderer execution |
| Receipts | `CompositionRuntimeBindingReceipt`, `PrimitiveEvalReceipt`, `IntegrationAdapterDecisionReceipt`, downstream `RenderReceipt`, `EvaluationReceipt`, `ApprovalReceipt` |

## 12. UI / Operator Requirements

The Operator Composition Workbench must show:

- four-video slot code and content asset code;
- guest / brand workspace scope;
- source Expression Moment and timestamp;
- Interview Asset Contract and anchor evidence;
- Brand Context Version and selected creative substrate;
- 64-state acting or avatar state selection;
- micro-semiotic anchors and risk/subtlety scores;
- route feel contract and primitive triad status;
- beat map with transcript-to-frame mapping;
- open-source adapter decisions;
- rendered preview;
- blockers and repair instructions;
- approve, repair, reject, or supersede controls.

## 13. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Beautiful visual boards vs source truth | Runtime binding must prove source, brand, primitive, timing, and renderer lineage. | `CompositionRuntimeBindingReceipt` links all required IDs and hashes. |
| Open-source acceleration vs CMF sovereignty | External components can assist only through adapter decisions and CMF contracts. | Adapter decision receipts are required before template runtime use. |
| Template reuse vs guest/brand specificity | Templates are reusable structures, but every render binds guest, brand, expression, and timing. | Renderer props include Brand Context, Expression Moment, beat map, and asset hashes. |
| Paper-Cut charm vs deterministic animation | Paper-Cut must use rig, layers, motion recipe, SFX, and preview tests. | Missing rig/layer/motion blocks render. |
| Reaction virality vs interview-first integrity | Reaction UI must match the question, answer, pause, or reaction seed. | Beat map and source evidence bind UI changes to transcript timing. |

## 14. Acceptance Criteria With Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Every production composition emits `CompositionRuntimeBindingReceipt`. | Renderer consumes JSON with no runtime receipt. |
| AC2 | Runtime binding includes locked Brand Context Version and selected creative substrate. | Template only stores colors and logo. |
| AC3 | Runtime binding includes CES, IAC, Expression Moment, transcript segment IDs, and timestamps. | Template is built from a visual idea without source. |
| AC4 | Paper-Cut route requires rig, layer, motion, SFX, and anchor rules. | Flat paper-cut image is accepted as animated explainer. |
| AC5 | Reaction route maps upper UI and lower human proof to beat timing. | Poll UI is unrelated to guest response. |
| AC6 | Open-source-derived components require adapter decision receipts. | Local reaction app is copied into renderer with no fit eval. |
| AC7 | Renderer props are generated from runtime binding and hashed. | Renderer props are hand-authored from a screenshot. |
| AC8 | Approval is blocked by missing primitive triad, route feel collapse, source drift, identity drift, or missing eval receipt. | Operator approves a beautiful preview with no source lineage. |

## 15. Testing Strategy

Unit tests:

- `BrandGenesisSubstrateBinding` rejects unlocked, stale, cross-brand, or incomplete Brand Context refs.
- `ExpressionLineageBinding` rejects missing IAC, CES, Expression Moment, timestamp range, route, or eval refs.
- `CompositionBeat` rejects negative durations, out-of-range frames, and beats with no source evidence.
- `OpenSourceAdapterBinding` rejects production use without decision receipt.

Contract tests:

- `CompositionRuntimeBinding` schema includes brand, expression, beat map, renderer targets, adapter refs, eval refs, blocker codes, and runtime hash.
- JSON Schema generated from Pydantic matches TypeScript renderer prop consumers.

Integration tests:

- `AssetPackageSpec -> CompleteEditingSession -> SceneSpec -> VisualFeelContract -> CompositionTemplateJson -> CompositionRuntimeBinding -> RendererProps`.
- `SV-EDU` fixture reproduces Brand Genesis holistic-health Paper-Cut myth-busting golden case with rig, anchors, tactile paper, motion recipe, SFX, and evals.
- `SV-RRC` fixture maps upper reaction UI and lower human proof to transcript timing.
- `SV-FRB` fixture blocks unsupported claims or proof-card decoration with no source.
- `SV-CSC` fixture preserves emotional pacing and source-backed memory object.

Negative fixtures:

- composition with no Expression Moment;
- Paper-Cut composition with no rig;
- reaction composition with no human proof;
- Ideogram plate with baked final text used as final render;
- open-source component used without decision receipt;
- template with fewer than three validated primitives;
- template with all primitives in one role;
- all four video formats sharing the same visual feel.

## 16. Implementation Tasks

1. Add Pydantic contracts in the composition/runtime contract module.
2. Add JSON Schema and TypeScript generated types for renderer consumers.
3. Implement runtime binding service.
4. Implement beat map generation from transcript alignment and Expression Moment timestamps.
5. Implement Brand Genesis substrate validator.
6. Implement expression lineage validator.
7. Implement adapter decision validator.
8. Implement renderer prop emitter for Remotion, Motion Canvas, and Manim-compatible routes.
9. Add Operator Workbench read model.
10. Add doctrine/eval harness bindings and blockers.
11. Create the first 24 `CompositionTemplateJson` files only after this runtime binding is in place.
12. Implement renderer components for approved templates after JSON, runtime bindings, and preview receipts pass.

## 17. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-080 |
| Requirement Trace | FR-CMF-04.02, FR-CMF-04.03, FR-CMF-04.04, FR-CMF-06.05, FR-CMF-06.06, FR-CMF-07.02, FR-CMF-07.03, FR-CMF-07.04, FR-CMF-07.08, FR-CMF-07.09, FR-CMF-08.02, FR-CMF-08.08, FR-CMF-09.01, FR-CMF-09.03 |
| Pipeline Trace | Stage 8 through 12, AssetPackageSpec to RenderOutput |
| Legacy Inventory Referenced | Yes |
| CMF Source Docs Re-Read | Yes - Brand Genesis V3, CCP V9, CCP V9.1 |
| CBAR Included | Yes |
| Forbidden Drift Check | No aesthetic-only templates, no flat Paper-Cut, no generic reaction UI, no open-source component without adapter receipt, no render without expression lineage and Brand Context substrate |
