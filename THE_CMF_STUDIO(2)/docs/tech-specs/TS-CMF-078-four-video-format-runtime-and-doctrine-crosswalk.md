---
tech_spec_id: "TS-CMF-078"
title: "Four-Video Format Runtime and Doctrine Crosswalk"
story_id: "6.11"
story_title: "Guest Asset Pack Four-Video Format Runtime"
epic_id: 6
epic_title: "Complete Expression Sessions, Extraction, Routing, and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "conversation-approved major update after TS-CMF-077"
fr_ids:
  - "FR-CMF-06.05"
  - "FR-CMF-06.06"
  - "FR-CMF-07.02"
  - "FR-CMF-07.03"
  - "FR-CMF-07.08"
  - "FR-CMF-07.09"
  - "FR-CMF-08.02"
  - "FR-CMF-09.01"
  - "FR-CMF-09.03"
pipeline_stage: "8 / 9 / 10 / 11 / 12"
entry_object: "AssetPackageSpec with source-backed short-video candidates"
exit_object: "FourVideoFormatPlan, VideoFormatRouteReceipt, approved SceneSpec lineage, render-ready format bundle"
validation_contract: "four video slot coverage, doctrine crosswalk, source support, composition/runtime dependency, eval blocker"
required_receipt: "FourVideoFormatPlanReceipt and per-slot VideoFormatRouteReceipt"
runtime_target: "Python / Pydantic v2 / DSPy / Command Bus / Remotion / Motion Canvas / GPU worker adapters"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-078: Four-Video Format Runtime and Doctrine Crosswalk

**Status:** Ready for Development  
**Implementation Boundary:** Define the canonical implementation contract for the Guest Asset Pack four-video set: Cinematic Story Commentary, Educational / Explainer, Challenger / Frame Breaker, and Reaction / Recognition Clip. This spec binds each video slot to the nine CMF doctrines, source-backed routing, composition JSON, renderer dependencies, evaluation receipts, and approval blockers.

## 1. Files Read

| File | Purpose |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Six moat doctrines, legacy extraction doctrine, Python-first runtime, and valid content formats. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Nine doctrine bullets, FR-CMF-06 and FR-CMF-07, Guest Asset Pack fulfillment. |
| `THE CMF STUDIO/CCP V9 - Interview-First Expression Engine.md` | Strategic interview-first doctrine and Guest Asset Pack proof logic. |
| `THE CMF STUDIO/CCP V9.1 - Expression Capture & Archetype Routing Update.md` | Complete Expression Session, Interview Asset Contract, and four-video package logic. |
| `THE CMF STUDIO/CCP Archetype System Migration Proposition.docx.md` | 4 video format mapping, source archetypes, CMF routes, reaction schemas. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Context Version, PaperCut rig, micro-semiotic anchoring, creative substrate. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Orchestration over generation, composition before rendering, identity compilation, acting library. |
| `THE CMF STUDIO/Matrix of Edging.md` | Tension selection doctrine and research-first edge discovery. |
| `docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md` | Content asset code, short-video subformat registry, reaction template routing. |
| `docs/tech-specs/TS-CMF-020-paper-cut-rig-and-creative-libraries.md` | PaperCut rig and creative library implementation dependency. |
| `docs/tech-specs/TS-CMF-071-reaction-editing-template-routing.md` | Conscious Reactions as governed live-filmed editing grammars. |
| `docs/tech-specs/TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md` | Scene-template binding dependency for reaction clips. |
| `docs/tech-specs/TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | Canonical composition JSON dependency. |
| `docs/tech-specs/TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md` | Stacked reaction renderer and background-removal dependency. |
| `docs/tech-specs/TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Doctrine test harness dependency. |

## 2. Overview

The Guest Asset Pack does not contain four arbitrary short videos. It contains four package-level proof slots selected from approved Expression Moments:

1. `SV-CSC` - Cinematic Story Commentary.
2. `SV-EDU` - Educational / Explainer.
3. `SV-FRB` - Challenger / Frame Breaker.
4. `SV-RRC` - Reaction / Recognition Clip.

Each slot must compile through the same source-backed production chain:

```text
Expression Moment
-> archetype route
-> asset derivative route
-> CMF render route
-> video slot assignment
-> Complete Editing Session
-> SceneSpec
-> composition/runtime dependency
-> renderer props
-> EvaluationReceipt
-> Operator approval
```

If the source material cannot support a slot, the system must record a rejected or candidate-only route instead of fabricating the asset. Quotas cannot force unsupported videos.

## 3. Canonical Four-Video Slots

| Slot | Format Code | Source Archetypes | CMF Routes | Primary Purpose |
|---|---|---|---|---|
| Video 1 | `SV-CSC` | Transformation Story, Backstory Reveal, Worst Case Scenario, Witness Story | Cinematic Story Commentary, Personal-Brand Commentary | Make the audience feel the story and trust the lived experience. |
| Video 2 | `SV-EDU` | Core Educator / Explainer, Conceptual Contrast, Scene-to-Principle, Visual Timeline | Paper-Cut Explainer, Animated Avatar Explainer | Make the audience understand the idea or framework. |
| Video 3 | `SV-FRB` | Myth Debunk, Challenger / Frame Breaker, Industry Hypocrisy Exposure, Shocking Comparison | Personal-Brand Commentary, Conscious Reactions Editing | Correct a belief, expose a contradiction, or establish authority. |
| Video 4 | `SV-RRC` | Validation Reaction, Solo Reaction, Vote Then React, Audience Mirror Quiz, Reaction Seed | Living Commentary Reaction, Conscious Reactions Editing | Create recognition, social proof, participation, or comment pressure. |

Video 4 is not the only reaction-aware slot. Conscious Reactions Editing can also serve Video 3 when the moment is a debate, contradiction, ranking, or myth-breaking mechanic. Video 4 remains the recognition/social-proof slot, with Living Commentary Reaction as the calmer human-proof route and Conscious Reactions Editing as the higher-energy participatory route.

## 4. Nine Doctrine Crosswalk

| Doctrine | Implementation Implication | Required Proof |
|---|---|---|
| Narrative State Induction | Interview Asset Contracts must ask questions that intentionally produce one or more four-video slots. | Asset contract stores target slot, target expression state, First-Line Anchors, Depth Anchors, and intended extraction outcome. |
| Matrix of Edging | Slot selection must be driven by live pressure, primitive coalition, and edge product, not generic social format taste. | `MatrixOfEdgingBrief` and route rationale are referenced by each `VideoFormatRouteReceipt`. |
| Brand Genesis | Every slot renders from locked Brand Context: acting library, PaperCut rig, micro-semiotic anchors, motion/SFX libraries, composition preferences. | Complete Editing Session links locked `BrandContextVersion`, selected assets, rig/acting refs, and creative library receipts. |
| Archetype Routing | Each slot must map from core archetype to asset derivative to CMF route to format code. | Route receipt stores archetype, derivative, CMF route, format code, and unsupported-route rejection state. |
| Legacy Intelligence Migration | Legacy prompts, scene containers, reaction apps, creative subsystems, and render mechanics are migration sources, not direct runtime imports. | Migration ledger refs, source app refs, scene-template binding refs, and no direct legacy runtime import checks. |
| Complete Editing Session | Every video slot becomes a traceable editing container before composition/rendering. | `CompleteEditingSession`, `SceneSpec`, `RenderContract`, provider receipts, and reconstruction audit are linked. |
| Evaluation Critics | Semantic, visual, voice, anti-draft, CBAR, and tonal checks block weak or unfaithful outputs. | `EvaluationReceipt`, `DoctrineTestRunReceipt`, and approval blockers for hard failures. |
| Operator Arbitration | The Operator can inspect source, route, composition, preview, eval failures, and approve/reject/repair. | PWA/Telegram read model exposes slot status, evidence, preview, blockers, and approval action. |
| Publishing and Memory | Approved videos become publishing intents and memory events without losing route/performance history. | `PublishingIntent`, Publer schedule refs, memory admission/rejection receipts, and performance feedback refs. |

## 5. Primary Contracts

```python
class FourVideoSlotCode(str, Enum):
    cinematic_story = "SV-CSC"
    educational_explainer = "SV-EDU"
    challenger_frame_breaker = "SV-FRB"
    reaction_recognition = "SV-RRC"


class FourVideoSlotRequirement(BaseModel):
    schema_version: Literal["cmf.four_video_slot_requirement.v1"]
    slot_code: FourVideoSlotCode
    required_source_archetypes: list[str]
    allowed_cmf_routes: list[str]
    required_doctrine_refs: list[str]
    required_evidence_types: list[str]
    required_downstream_specs: list[str]
    unsupported_route_policy: Literal["reject", "candidate_only"]


class VideoFormatRouteReceipt(BaseModel):
    schema_version: Literal["cmf.video_format_route_receipt.v1"]
    video_format_route_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    asset_package_spec_id: UUID
    expression_moment_id: UUID
    content_asset_code: str
    slot_code: FourVideoSlotCode
    archetype_route: str
    asset_derivative: str
    cmf_route: str
    source_support_evidence: list[str]
    doctrine_refs: list[str]
    primitive_refs: list[str]
    downstream_dependency_refs: list[str]
    decision_code: Literal["VIDEO_SLOT_ACCEPTED", "VIDEO_SLOT_REJECTED", "VIDEO_SLOT_CANDIDATE_ONLY"]
    blocker_codes: list[str]
    written_at: datetime


class FourVideoFormatPlan(BaseModel):
    schema_version: Literal["cmf.four_video_format_plan.v1"]
    four_video_format_plan_id: UUID
    organization_id: UUID
    brand_id: UUID
    asset_package_spec_id: UUID
    slot_receipt_ids: list[UUID]
    coverage_state: Literal["complete", "partial_source_supported", "blocked"]
    missing_slot_codes: list[FourVideoSlotCode]
    operator_review_required: bool
    doctrine_test_run_receipt_id: UUID | None
```

## 6. Slot-Specific Build Dependencies

| Slot | Required Implementation Dependencies |
|---|---|
| `SV-CSC` | Interview Asset Contract, Expression Moment extraction, SceneSpec, composition control, cinematic captions, audio/caption/timeline assembly, deterministic renderer. |
| `SV-EDU` | PaperCut rig and creative libraries, motion recipe, composition preference, SceneSpec, layer manifest, animation plan, deterministic renderer, PaperCut doctrine eval. |
| `SV-FRB` | Matrix of Edging route, myth/challenge archetype, personal-brand commentary or reaction editing route, route-evidence gate, semantic/CBAR eval. |
| `SV-RRC` | Reaction template routing, scene-template runtime binding, approved composition JSON, background-removed upper-body subject layers, beat sync, reaction renderer receipt. |

## 7. Composition and Renderer Rules

All four slots must be composition-first, but not all use the same composition schema.

| Slot | Composition Source | Renderer Route |
|---|---|---|
| `SV-CSC` | SceneSpec plus CompositionJob JSON or approved cinematic composition template. | Remotion deterministic video with captions, audio mix, optional B-roll or composition plate. |
| `SV-EDU` | SceneSpec plus PaperCut/Animated Avatar composition template and locked rig manifest. | Motion Canvas or Remotion PaperCut animation route. |
| `SV-FRB` | SceneSpec plus commentary/challenge composition template; optional reaction template when routed to Conscious Reactions. | Remotion commentary route or reaction renderer route. |
| `SV-RRC` | Approved `CompositionTemplateJson` with reaction UI upper zone and human scene lower zone. | Reaction clip renderer with background removal and beat sync. |

The unified rule is not "one visual layout for every video." The unified rule is:

```text
source-backed route -> approved composition JSON or CompositionJob lineage -> deterministic renderer props -> receipt
```

For reaction clips, the canonical stacked layout is required by TS-CMF-073 and TS-CMF-074. For PaperCut explainers, the rig/layer/motion contracts from TS-CMF-020 and deterministic rendering contracts from TS-CMF-043 apply.

## 8. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileFourVideoFormatPlanCommand`, `AssignExpressionMomentToVideoSlotCommand`, `RejectUnsupportedVideoSlotCommand`, `RecordVideoFormatRouteReceiptCommand`, `RunFourVideoDoctrineCoverageCommand` |
| Events | `FourVideoFormatPlanCompiled`, `VideoSlotAccepted`, `VideoSlotRejected`, `VideoSlotCandidateOnlyRecorded`, `FourVideoDoctrineCoverageCompleted` |
| Workflow | Stage 8 asset package planning through Stage 12 rendering |
| Receipts | `FourVideoFormatPlanReceipt`, `VideoFormatRouteReceipt`, downstream `ReactionTemplateRouteReceipt`, `CompositionTemplateApprovalReceipt`, `RenderReceipt`, `EvaluationReceipt`, `DoctrineTestRunReceipt` |

## 9. Read Models and UI Requirements

The Operator UI must show a Guest Asset Pack video board with four fixed slots:

- `SV-CSC` Cinematic Story Commentary;
- `SV-EDU` Educational / Explainer;
- `SV-FRB` Challenger / Frame Breaker;
- `SV-RRC` Reaction / Recognition Clip.

Each slot card must display:

- content asset code;
- source Expression Moment and timestamp;
- archetype, derivative, CMF route, and reaction template when applicable;
- doctrine coverage state;
- composition lineage and preview state;
- eval receipt state and blockers;
- render state;
- approval/revision/publish state.

## 10. Doctrine Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. Minimum doctrine invariants:

| Invariant | Failure Code |
|---|---|
| Four-video slots cannot be filled without source-supported Expression Moments. | `VIDEO_SLOT_SOURCE_SUPPORT_MISSING` |
| Every slot must map through archetype, derivative, CMF route, and format code. | `VIDEO_SLOT_ROUTE_CHAIN_INCOMPLETE` |
| `SV-EDU` PaperCut/Animated Avatar output cannot render without locked Brand Context, rig/motion, or composition dependency. | `EDU_PAPERCUT_SUBSTRATE_MISSING` |
| `SV-RRC` reaction output cannot render without approved composition JSON, scene-template binding, and subject-layer requirements. | `REACTION_COMPOSITION_CHAIN_MISSING` |
| Conscious Reactions templates cannot be treated as generic UI toys outside source-backed live-filmed editing grammar. | `REACTION_TEMPLATE_SOURCE_DRIFT` |
| Operator approval cannot occur while any slot has hard eval failures. | `FOUR_VIDEO_APPROVAL_BLOCKED` |

Required primitive obligation families:

- `STR` for narrative and teaching structure;
- `TRG` for tension timing and participation pressure;
- `PSY` for recognition, belief correction, and audience mirror integrity;
- `VSG` for composition, negative space, visual clarity, and PaperCut/reaction layouts;
- `ACT` for acting library, upper-body subject layers, and expression state;
- `FBK` for source-backed claims, route evidence, and evaluation receipts;
- `SAF` for consent, likeness, claim safety, and publishing approval.

## 11. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Four slots vs available source | Missing source creates partial/candidate state, not fabricated video. | `VideoFormatRouteReceipt` with rejected or candidate-only decision. |
| Visual variety vs unified system | Layouts differ, but all slots share source, route, composition, renderer, eval, approval lineage. | `FourVideoFormatPlan` links per-slot receipts and downstream dependencies. |
| Conscious Reactions vs cheap viral format | Reaction mechanics remain source-backed live-filmed editing grammars. | Reaction slot carries template route receipt, slot requirements, beat sync, and doctrine eval. |
| PaperCut appeal vs production truth | PaperCut requires locked rig, layers, pivots, previews, motion recipe, and eval. | Rig/creative receipts and PaperCut doctrine test run are linked. |

## 12. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | A Guest Asset Pack can compile a four-slot plan from approved Expression Moments. | Package only stores "4 videos" with no slot codes. |
| AC2 | Each slot stores archetype, derivative, CMF route, source evidence, doctrine refs, primitive refs, and content asset code. | Slot only stores filename and caption. |
| AC3 | Unsupported or missing slots are rejected or marked candidate-only. | System fabricates a reaction clip because quota says four videos. |
| AC4 | `SV-EDU` can route to PaperCut/Animated Avatar only with locked creative substrate and render dependency. | Flat generated image is accepted as a PaperCut explainer. |
| AC5 | `SV-RRC` requires reaction template routing, scene-template binding, composition JSON, and renderer props. | Reaction clip renders directly from a mockup image. |
| AC6 | Operator UI exposes doctrine/eval/approval state per slot. | Operator sees thumbnails but not route lineage or blockers. |

## 13. Testing Strategy

- Unit tests for `FourVideoSlotRequirement`, `VideoFormatRouteReceipt`, and `FourVideoFormatPlan`.
- Registry tests proving `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC` are the canonical four short-video package slots.
- Service tests for complete, partial, rejected, and candidate-only plans.
- Doctrine harness tests using the invariants in section 10.
- Integration tests from `AssetPackageSpec` to Complete Editing Sessions and downstream composition/render dependencies.
- UI read-model tests proving each slot displays route, source, composition, eval, and approval state.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-078 |
| Requirement Trace | FR-CMF-06.05, FR-CMF-06.06, FR-CMF-07.02, FR-CMF-07.03, FR-CMF-07.08, FR-CMF-07.09, FR-CMF-08.02, FR-CMF-09.01, FR-CMF-09.03 |
| Pipeline Trace | Stage 8 asset package planning to Stage 12 render output |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Doctrine Crosswalk Included | Yes, nine doctrines mapped to slot implementation proof |
| Forbidden Drift Check | No unsupported four-video quota fill, no generic reaction UI toys, no flat PaperCut output, no render without composition/eval/approval lineage |
