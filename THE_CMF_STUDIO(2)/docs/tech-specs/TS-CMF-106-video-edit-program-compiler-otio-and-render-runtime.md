---
tech_spec_id: "TS-CMF-106"
title: "Video Edit Program Compiler, OTIO, and Render Runtime"
story_id: "7.36"
story_title: "Video Edit Program Compiler"
epic_id: 7
epic_title: "Editing, Composition, and Rendering"
status: "ready-for-development"
created_at: "2026-06-25"
fr_ids:
  - "FR-CMF-07.02"
  - "FR-CMF-07.03"
  - "FR-CMF-07.04"
  - "FR-CMF-07.08"
  - "FR-CMF-07.09"
  - "FR-CMF-08.02"
  - "FR-CMF-09.01"
  - "FR-CMF-09.03"
pipeline_stage: "content sequence handoff, video edit program compilation, proxy render, eval, approval, final render"
entry_object: "CreateVideoEditProgramRequest"
exit_object: "VideoEditProgramReceipt"
validation_contract: "brand scope, source provenance, transcript clock, four-format grammar, beat-to-scene binding, provider plan, deterministic render contract, OTIO audit manifest, primitive/doctrine eval gates, operator approval"
required_receipt: "VideoEditProgramReceipt"
runtime_target: "FastAPI / Python / Pydantic v2 / command bus / Remotion / Motion Canvas / Manim / FFmpeg / OpenTimelineIO / provider workers / PWA review"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-106: Video Edit Program Compiler, OTIO, and Render Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 spec structure and brownfield integration rule. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Audit.md` | Five-lens audit protocol used for the post-write audit. |
| `THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Revision.md` | Section-targeted revision protocol used after audit findings. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | Phase 4 CBAR mandates for pipelines, rendering, routing, blocks, and actionable rejection. |
| `THE CMF STUDIO/docs/architecture/april_updates/Phase5_Growth_Epics.md` | Phase 5 artifact verification and earned escalation mandates. |
| `THE CMF STUDIO/docs/audits/CMF_VIDEO_EDITING_ENGINE_MCDA_2026-06-24.md` | Reserves TS-CMF-106 and identifies the missing parent abstraction: `VideoEditProgram`. |
| `THE CMF STUDIO/docs/audits/CMF_CAROUSEL_AND_SUPERVISUAL_SPEC_AUDIT_REVISION_2026-06-24.md` | Moves the video editing binding spec into the TS-CMF-106 slot. |
| `THE CMF STUDIO/docs/audits/CMF_2D_CHARACTER_ENGINE_SPEC_AUDIT_REVISION_2026-06-25.md` | Confirms TS-CMF-106 is reserved for video editing and that character specs feed it through TS-CMF-110 through TS-CMF-113. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-070-ui-architecture-and-operator-experience.md` | Parent PWA and operator experience architecture. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-071-reaction-editing-template-routing.md` | Existing Conscious Reactions routing dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md` | Reaction scene-template binding dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | Composition JSON source-of-truth dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md` | Lower-level reaction clip compositing dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-075-operator-composition-and-template-approval-workbench.md` | Approval workbench dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` | External integration governance dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` | Doctrine and primitive-driven testing requirement. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` | Canonical four video format slots and doctrine crosswalk. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-079-route-specific-visual-feel-and-primitive-composition-gates.md` | Prevents visual-feel collapse across video formats. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` | Composition runtime spine binding Brand Genesis, transcript timing, and renderer props. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-084-transcript-beat-map-and-timeline-cue-compiler.md` | Transcript-clock and beat-map dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-086-papercut-rig-layer-motion-and-sfx-runtime.md` | PaperCut and rigged educational scene dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-090-renderer-prop-compiler-and-component-harness.md` | Renderer-prop compiler dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Composition eval and approval dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-110-two-d-character-engine-object-model-and-character-genesis.md` | Character object model dependency for Educational / Explainer scenes. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-112-two-d-character-scene-program-and-performance-compiler.md` | `TwoDCharacterProgram` dependency for transcript-timed character performance. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-113-two-d-character-render-runtime-evals-approval-and-repair.md` | 2D character render/eval dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md` | Upstream sequence handoff dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-120-openmontage-reference-adapter-governance.md` | OpenMontage reference governance. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-121-production-pipeline-manifest-registry.md` | Stage manifest dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-122-stage-director-skill-contract-binding.md` | Stage Director and skill contract dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-123-capability-tool-registry-and-provider-menu.md` | Capability and tool registry dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-124-scored-provider-selector-and-capability-router.md` | Provider selection dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-126-reference-video-and-existing-footage-intake-adapter.md` | Reference and existing footage intake dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-127-real-footage-corpus-and-source-media-retrieval-adapter.md` | Real footage retrieval dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-128-render-runtime-selection-and-locking.md` | Render runtime lock dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-129-pre-compose-delivery-promise-and-slideshow-risk-gate.md` | Pre-compose QA dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-130-post-render-self-review-and-media-qa-gate.md` | Post-render QA dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md` | Human approval and stage artifact review dependency. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md` | Product requirement for reconstructable editing, composition, timing, and render lineage. |
| `THE CMF STUDIO/docs/prd/modules/PRD_CMF_08_Evals_and_Primitives.md` | Eval, primitive, and approval blocker requirements. |
| `THE CMF STUDIO/registries/evals/composition/cmf_composition_primitive_triads.v1.json` | Exact route-specific primitive IDs, roles, thresholds, evidence requirements, and hard failures. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Interview-first source doctrine for extracting and using human expression moments. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression capture and route binding update. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Brand Genesis, micro-semiotic, identity, and acting asset dependency. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Legacy creative pipeline and scene-building dependency. |
| `THE CMF STUDIO/src/ccp_studio/contracts/scene_spec.py` | Existing scene contract owner. |
| `THE CMF STUDIO/src/ccp_studio/services/scene_spec_compiler.py` | Existing scene compiler owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/composition.py` | Existing composition contract owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/deterministic_rendering.py` | Existing deterministic renderer contract owner. |
| `THE CMF STUDIO/src/ccp_studio/services/deterministic_rendering_service.py` | Existing deterministic render service owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/sonic_timeline.py` | Existing sonic timeline contract owner. |
| `THE CMF STUDIO/src/ccp_studio/services/sonic_timeline_service.py` | Existing sonic timeline service owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/reaction_editing.py` | Existing reaction editing contract owner. |
| `THE CMF STUDIO/src/ccp_studio/services/reaction_editing_service.py` | Existing reaction editing service owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/provider_jobs.py` | Existing provider job contract owner. |
| `THE CMF STUDIO/src/ccp_studio/services/provider_operations_service.py` | Existing provider operation owner. |
| `THE CMF STUDIO/src/ccp_studio/services/evaluation_receipt_service.py` | Existing evaluation receipt owner. |
| `THE CMF STUDIO/src/ccp_studio/services/approval_gate_service.py` | Existing approval blocker owner. |
| `THE CMF STUDIO/src/ccp_studio/services/review_state_service.py` | Existing review state owner. |
| `THE CMF STUDIO/src/ccp_studio/services/telegram_review_service.py` | Existing Telegram review owner. |
| `THE CMF STUDIO/src/ccp_studio/workflows/render_workflow.py` | Existing render workflow owner. |

## 2. Overview

CMF video editing cannot be implemented as isolated scene templates, isolated Remotion files, or loose generative video prompts. The platform needs a parent object that can receive interview-first source context, route it into one of the four canonical video formats, bind exact transcript timing, compile scene programs, plan provider work, run deterministic proxy and final renders, export an OpenTimelineIO audit manifest, and preserve review/eval receipts. This spec defines that parent object: `VideoEditProgram`.

`VideoEditProgram` is the canonical edit plan for a short-form video asset. It sits above `SceneSpec`, reaction routes, PaperCut or character scene programs, caption plans, audio mix plans, render props, provider jobs, and approval receipts. It is not a replacement for those contracts. It is the object that makes them operate together as one timed, reviewable, reproducible edit.

The feature requirement is: given a brand-scoped workspace, approved source context, a transcript beat map, expression moments, format target, asset package constraints, primitive obligations, and doctrine gates, the system must compile a complete video edit program that maps every scene, layer, caption, audio decision, generated asset, footage cut, and animation cue to source evidence and transcript time. The program must render a proxy preview, block approval when source, timing, brand scope, primitive triad, visual feel, caption, audio, mask, provider, or doctrine obligations fail, and only produce a final master after operator approval. The output must include a `VideoEditProgramReceipt`, deterministic render hashes, and an `OTIOAuditManifest` that lets an operator or developer reconstruct the edit without trusting hidden state.

This spec intentionally turns video editing into a compiler problem. Generative tools may create assets, masks, plates, candidate animations, or reference media, but the final timeline, composition, timing, source binding, and approval state must be deterministic CMF data.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-106-001 | `CreateVideoEditProgramRequest` | Structured command that selects guest workspace, source context, format slot, target duration, aspect ratio, source video refs, transcript refs, and package intent. |
| DEP-CMF-106-002 | `VideoEditProgram` | Parent object for scenes, tracks, layers, provider plans, render contracts, eval gates, approval state, and receipts. |
| DEP-CMF-106-003 | `TranscriptClock` | Canonical mapping between transcript time, source media timecode, output timeline time, frame rate, and drift tolerance. |
| DEP-CMF-106-004 | `BeatToSceneBinding` | Mapping from transcript beat/expression moment to scene, layer, caption, camera, audio, and animation cues. |
| DEP-CMF-106-005 | `FormatCompositionContract` | Four-format grammar contract for `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC`. |
| DEP-CMF-106-006 | `VideoEditProgramScene` | Scene-level wrapper that references `SceneSpec`, reaction templates, PaperCut subscenes, 2D character programs, visual inserts, or footage-only scenes. |
| DEP-CMF-106-007 | `VideoLayerManifest` | Ordered layer model for footage, subject cutouts, captions, UI panels, annotations, props, generated inserts, SFX, and overlays. |
| DEP-CMF-106-008 | `TrackedSubjectLayerManifest` | Guest/interviewer cutout model with mask refs, body framing, eye-line, occlusion, and safety checks. |
| DEP-CMF-106-009 | `PaperCutSubsceneManifest` | Educational / Explainer subscene model binding rigged PaperCut or 2D avatar scenes to transcript concepts. |
| DEP-CMF-106-010 | `CaptionLayoutPlan` | Caption timing, position, emphasis, word-level layout, text safety, and subtitle collision checks. |
| DEP-CMF-106-011 | `AudioMixPlan` | Voice intelligibility, music bed, SFX, room tone, silence emphasis, ducking, loudness, and export mix rules. |
| DEP-CMF-106-012 | `ProviderJobPlan` | Provider work graph for background removal, SAM3 masks, Qwen/Flux/GPT Image 2 assets, ComfyUI jobs, captions, and intermediate renders. |
| DEP-CMF-106-013 | `VideoRenderContract` | Deterministic render contract for proxy and final renders, including renderer lock, renderer props, asset hashes, and render hash expectations. |
| DEP-CMF-106-014 | `OTIOAuditManifest` | OpenTimelineIO-compatible interchange/audit export that reconstructs the sequence, clips, effects, markers, layers, and source refs. |
| DEP-CMF-106-015 | `VideoEditEvalGateSet` | Eval gate bundle for source, brand, timing, format feel, primitive triads, doctrine, masks, captions, audio, provider drift, OTIO, and approval. |
| DEP-CMF-106-016 | `VideoEditProgramReceipt` | Immutable receipt emitted after compile, proxy, eval, approval, final render, and OTIO export. |
| DEP-CMF-106-017 | `VideoEditProgramReviewReadModel` | Operator-readable projection for PWA and Telegram review. |
| DEP-CMF-106-018 | `VideoFormatGrammarRegistry` | Registry mapping each format slot to mandatory scenes, layer roles, composition obligations, provider roles, primitive triads, and eval gates. |

### Existing Backend Integration

This spec extends the current Python/FastAPI/Pydantic backend. It must not build a parallel editor runtime that bypasses existing contracts.

New modules:

| New Module | Required Responsibility |
|---|---|
| `src/ccp_studio/contracts/video_edit_program.py` | Pydantic contracts defined in Section 5. |
| `src/ccp_studio/repositories/video_edit_program.py` | Persistence for video edit programs, scenes, beat bindings, provider plans, render contracts, OTIO manifests, and receipts. |
| `src/ccp_studio/services/video_edit_program_service.py` | Compiler service that validates inputs, loads dependencies, compiles scenes/layers/tracks, and emits program state. |
| `src/ccp_studio/services/video_edit_otio_export_service.py` | OpenTimelineIO audit manifest exporter. |
| `src/ccp_studio/services/video_edit_eval_gate_service.py` | Video-specific gate orchestration over existing doctrine/eval/approval services. |
| `src/ccp_studio/workflows/video_edit_program_workflow.py` | End-to-end workflow from create request through final render and receipt. |
| `src/ccp_studio/api/v1/video_edit_programs.py` | FastAPI route family for compile, provider plan, proxy render, eval, review, approval, final render, and OTIO export. |
| `src/ccp_studio/generated/typescript/video_edit_program_contracts.ts` | Generated frontend contracts for the PWA review surface. |
| `THE CMF STUDIO/registries/composition/video_format_composition_grammars.v1.json` | Format-specific grammar, layer, timing, and eval obligations. |
| `THE CMF STUDIO/registries/evals/composition/video_edit_eval_gate_set.v1.json` | Video-edit gate definitions and blocker mappings. |

Existing modules that must be used:

| Existing Module | Required Use |
|---|---|
| `contracts/scene_spec.py` and `services/scene_spec_compiler.py` | Scene-level contract and compiler. `VideoEditProgramScene` wraps, not replaces, `SceneSpec`. |
| `contracts/composition.py` and `services/composition_service.py` | Composition JSON and visual binding dependency. |
| `contracts/deterministic_rendering.py` and `services/deterministic_rendering_service.py` | Proxy and final render contracts, hashes, and deterministic render state. |
| `contracts/sonic_timeline.py` and `services/sonic_timeline_service.py` | Voice, music, SFX, silence, and loudness planning. |
| `contracts/reaction_editing.py` and `services/reaction_editing_service.py` | Conscious Reactions route and template dependencies. |
| `contracts/provider_jobs.py` and `services/provider_operations_service.py` | Provider job planning, execution, retry, and receipts. |
| `services/generative_provider_service.py` | Approved generative provider execution only through governed provider jobs. |
| `services/evaluation_receipt_service.py` | Immutable eval receipt creation. |
| `services/doctrine_evaluation_service.py` and `services/doctrine_test_harness.py` | Doctrine and primitive-driven test/eval execution. |
| `services/approval_gate_service.py` | Approval blocker creation and waiver policy. |
| `services/review_state_service.py`, `review_decision_service.py`, and `telegram_review_service.py` | Operator review state, decisions, and Telegram/PWA review cards. |
| `workflows/render_workflow.py` and `workflows/provider_job_workflow.py` | Lower-level render/provider workflow orchestration. |

Persistence tables:

| Table | Required Fields |
|---|---|
| `video_edit_programs` | `program_id`, `workspace_id`, `guest_id`, `asset_package_id`, `format_slot`, `status`, `duration_ms`, `aspect_ratio`, `source_context_refs`, `program_hash`, `created_at`, `updated_at`. |
| `video_edit_program_scenes` | `scene_id`, `program_id`, `scene_index`, `format_role`, `scene_spec_ref`, `start_ms`, `end_ms`, `source_beat_refs`, `composition_ref`, `scene_hash`. |
| `video_edit_beat_bindings` | `binding_id`, `program_id`, `scene_id`, `transcript_beat_id`, `expression_moment_id`, `source_time_range`, `timeline_time_range`, `binding_confidence`, `drift_ms`. |
| `video_edit_layers` | `layer_id`, `program_id`, `scene_id`, `track_id`, `layer_role`, `asset_ref`, `mask_ref`, `z_index`, `time_range`, `safe_zone`, `layer_hash`. |
| `video_edit_provider_plans` | `provider_plan_id`, `program_id`, `provider_job_refs`, `capability_refs`, `estimated_cost`, `retry_policy_ref`, `receipt_refs`. |
| `video_edit_render_contracts` | `render_contract_id`, `program_id`, `render_kind`, `runtime`, `renderer_props_ref`, `input_hashes`, `output_hash`, `status`. |
| `video_edit_otio_manifests` | `otio_manifest_id`, `program_id`, `otio_json_ref`, `otio_hash`, `coverage_report`, `created_at`. |
| `video_edit_program_receipts` | `receipt_id`, `program_id`, `receipt_type`, `actor_ref`, `input_hash`, `output_hash`, `blocker_refs`, `approval_ref`, `created_at`. |

API route family:

| Route | Behavior |
|---|---|
| `POST /api/v1/video-edit-programs` | Create a draft program request. |
| `GET /api/v1/video-edit-programs/{program_id}` | Return canonical program state. |
| `POST /api/v1/video-edit-programs/{program_id}/compile` | Compile full `VideoEditProgram` from source context and transcript clock. |
| `POST /api/v1/video-edit-programs/{program_id}/provider-plan` | Compile provider job plan without executing unsafe work. |
| `POST /api/v1/video-edit-programs/{program_id}/proxy-render` | Produce deterministic proxy render for review. |
| `POST /api/v1/video-edit-programs/{program_id}/evaluate` | Run video edit gate set and emit eval receipts/blockers. |
| `GET /api/v1/video-edit-programs/{program_id}/review` | Return `VideoEditProgramReviewReadModel`. |
| `POST /api/v1/video-edit-programs/{program_id}/approve` | Approve only when blockers are clear or eligible warnings are explicitly waived. |
| `POST /api/v1/video-edit-programs/{program_id}/final-render` | Render final master only after approval. |
| `POST /api/v1/video-edit-programs/{program_id}/export-otio` | Export OTIO audit manifest. |

### ADR-05 Primitives

Every `VideoEditProgram` must load `registries/evals/composition/cmf_composition_primitive_triads.v1.json` and validate at least three registered primitives across meaning, delivery, and format/material roles. The program-level primitive obligations are separate from scene-level primitive obligations. A scene can pass while the full program still fails if the edit sequence collapses the intended route.

Required minimum by format is resolved from `CMF-COMP-PRIMITIVE-TRIADS-001`. The table below lists the minimum route triad that TS-CMF-106 must enforce. Additional route-allowed primitives may be selected from the same registry, but the compiler cannot substitute fuzzy names for exact IDs.

| Format Slot | Role | Required Primitive ID | Canonical Name | Registry Ref | Minimum Score |
|---|---|---|---|---|---:|
| `SV-CSC` | `meaning_transform` | `PRM-ACT-005` | Backstory Architecture | `registries/primitives/meaning_plane/performance_delivery/PRM-ACT-005.yaml` | 0.84 |
| `SV-CSC` | `delivery_shape` | `PRM-PRS-002` | Tension-and-Release Narrative Engine | `registries/primitives/meaning_plane/persuasion/PRM-PRS-002.yaml` | 0.84 |
| `SV-CSC` | `format_material` | `PRM-VSG-021` | Punctum, Air, and Felt Truth | `registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-021.yaml` | 0.86 |
| `SV-EDU` | `meaning_transform` | `PRM-HUM-025` | Analogy Bridge | `registries/primitives/meaning_plane/humor_distortion/PRM-HUM-025.yaml` | 0.86 |
| `SV-EDU` | `delivery_shape` | `PRM-PRS-032` | The Explanation Engine | `registries/primitives/meaning_plane/persuasion/PRM-PRS-032.yaml` | 0.84 |
| `SV-EDU` | `format_material` | `PRM-VSG-020` | Perspective and Layering as Meaning | `registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-020.yaml` | 0.88 |
| `SV-FRB` | `meaning_transform` | `PRM-HUM-021` | Irony Inversion | `registries/primitives/meaning_plane/humor_distortion/PRM-HUM-021.yaml` | 0.86 |
| `SV-FRB` | `delivery_shape` | `PRM-REF-009` | Constructive Tension Control | `registries/primitives/meaning_plane/referral_trust_transfer/PRM-REF-009.yaml` | 0.86 |
| `SV-FRB` | `format_material` | `PRM-VSG-012` | Frame as Active Meaning Device | `registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-012.yaml` | 0.86 |
| `SV-RRC` | `meaning_transform` | `PRM-PSY-001` | Matching Principle | `registries/primitives/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | 0.86 |
| `SV-RRC` | `delivery_shape` | `PRM-REF-009` | Constructive Tension Control | `registries/primitives/meaning_plane/referral_trust_transfer/PRM-REF-009.yaml` | 0.84 |
| `SV-RRC` | `format_material` | `PRM-VSG-015` | Composition as Attention Routing | `registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-015.yaml` | 0.86 |

Primitive validation must bind to:

- source expression moment refs;
- transcript beat refs;
- scene role;
- layer role;
- caption or annotation plan;
- visual feel contract;
- timing decision;
- eval receipt.

If a program cannot prove primitive coverage with registered primitive IDs, it must block with `VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED`.

Primitive verdicts:

| Verdict | Rule | Downstream Consequence |
|---|---|---|
| `PASS` | At least three registered primitive IDs validate, all three roles are covered, all selected scores meet route threshold, and evidence refs exist. | Program may proceed to provider planning or render evaluation. |
| `PROVISIONAL` | Not allowed for required route triad primitives. Allowed only for optional additional primitives within 0.04 below their registry threshold and only before final approval. | Program remains editable and cannot final render until repaired or waived as a warning by an authorized operator. |
| `FAIL` | Any selected primitive ID is unregistered, below threshold, missing evidence, or assigned to the wrong role. | Emit eval receipt and repair command. |
| `BLOCKED` | Required minimum count or role coverage is missing, or route feel collapses. | Stop provider execution or final render with `VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED` or `VIDEO_EDIT_FORMAT_FEEL_COLLAPSE`. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| `Phase4-M01 Intelligence-Gated Intercept` | The compiler must stop before provider work when source, brand, transcript, or format grammar requirements are missing. |
| `Phase4-M02 Cinematic Meaning` | Format-specific visual feel and primitive gates must prevent generic premium-social sameness. |
| `Phase4-M03 Inline Routing SLA` | The program must expose exact route, blocker, and repair target in the review model, not hidden logs. |
| `Phase4-M04 Frictionless Block` | Hard blockers must stop final render without requiring the operator to search for why. |
| `Phase4-M05 Actionable Rejection` | Every blocker must include a repair command target and missing evidence. |
| `Phase5-M01 Verifiable Artifact` | Final master, proxy, OTIO audit, render contract, provider receipts, and approval receipts must be reconstructable. |
| `Phase5-M02 Earned Escalation` | Waivers are allowed only for eligible warning gates and must be signed by an authorized operator. |

### Gate Threshold and Verdict Matrix

Every gate in `VideoEditEvalGateSet` must emit a deterministic verdict: `PASS`, `PROVISIONAL`, `FAIL`, or `BLOCKED`. Hard gates may only emit `PASS` or `BLOCKED`. Warning gates may emit `PROVISIONAL` only inside the threshold band below.

| Gate | Hard Gate | PASS Threshold | PROVISIONAL Threshold | BLOCKED / FAIL Consequence |
|---|---:|---|---|---|
| Source timing | Yes | `scene_beat_binding_coverage == 1.00`, every production scene has at least one transcript beat or approved contextual insert, and `abs(drift_ms) <= 80`. | Not allowed. | `VIDEO_EDIT_SOURCE_TIMING_MISSING` |
| Brand and guest scope | Yes | `workspace_id`, `guest_id`, Brand Context version, source media refs, and generated assets all share the same approved workspace scope. | Not allowed. | `VIDEO_EDIT_BRAND_SCOPE_MISSING` |
| Format route | Yes | `format_slot in ["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"]` and grammar version resolves. | Not allowed. | `VIDEO_EDIT_FORMAT_ROUTE_UNSUPPORTED` |
| Format feel | Yes | Visual feel gate score `>= 0.86` and no route-specific hard failures from `CMF-COMP-PRIMITIVE-TRIADS-001`. | Not allowed. | `VIDEO_EDIT_FORMAT_FEEL_COLLAPSE` |
| Primitive triad | Yes | `primitive_validation_count >= 3`, all required roles covered, every required primitive score meets its registry threshold, and evidence refs exist. | Not allowed for required primitives. Optional primitives may be provisional within `threshold - 0.04`. | `VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED` |
| Doctrine eval | Yes | All doctrine gates required by the selected format return `PASS`; no doctrine conflict hard failure exists. | Not allowed for hard doctrine gates. | `VIDEO_EDIT_DOCTRINE_EVAL_MISSING` |
| Subject mask and identity safety | Yes | Mask quality score `>= 0.88`, identity safety score `>= 0.92`, visible artifact score `<= 0.08`, and all subject layers carry mask and identity receipts. | Not allowed for identity safety; mask quality may be provisional from `0.84` to `0.879` before final render only. | `VIDEO_EDIT_SUBJECT_MASK_UNSAFE` |
| Caption layout | Yes | Transcript word timing drift `<= 120ms`, safe-zone collisions `== 0`, face overlap `== 0`, max lines `<= 4`, and text contrast ratio `>= 4.5:1`. | Contrast ratio from `4.0` to `4.49` is provisional for proxy only. | `VIDEO_EDIT_CAPTION_LAYOUT_FAILED` |
| Audio intelligibility | Yes | Voice intelligibility score `>= 0.86`, integrated loudness target `-16 LUFS +/- 1`, true peak `<= -1 dBTP`, and speech-bed ducking `>= 12 dB`. | Voice intelligibility from `0.82` to `0.859` is provisional for proxy only. | `VIDEO_EDIT_AUDIO_SOURCE_INTELLIGIBILITY_FAILED` |
| Generated asset source drift | Yes | Unsupported biographical claim count `== 0`, source alignment score `>= 0.88`, and every generated asset has provider receipt and layer role. | Source alignment from `0.84` to `0.879` is provisional before final approval only. | `VIDEO_EDIT_GENERATED_ASSET_SOURCE_DRIFT` |
| OTIO audit coverage | Yes | `otio_scene_coverage == 1.00`, `otio_source_clip_coverage == 1.00`, `otio_marker_coverage == 1.00`, and OTIO hash exists. | Not allowed. | `VIDEO_EDIT_OTIO_AUDIT_MISSING` |
| Operator approval | Yes | Authorized operator approval exists after eval and before final render. | Not allowed. | `VIDEO_EDIT_OPERATOR_APPROVAL_REQUIRED` |

Gate receipts must include `gate_id`, `gate_version`, `verdict`, `threshold`, `observed_value`, `blocker_code`, `repair_target`, `evidence_refs`, `input_hash`, `output_hash`, and `created_at`.

### Technical Decisions

| Decision | Rationale |
|---|---|
| `VideoEditProgram` is the source of truth for video edits. | Existing scene specs and render contracts are necessary but not enough to represent a full transcript-timed edit. |
| Remotion is the primary program render spine for deterministic social video. | It can express React-based video composition, component props, captions, layers, and reproducible frame rendering. |
| Motion Canvas is allowed as a subscene engine. | It is fit for animated diagrams and explainer panels, but should emit a locked subscene manifest back into the parent program. |
| Manim is allowed only for procedural educational inserts. | It should not become the general video editor. Its outputs must be imported as subscene assets or clips. |
| FFmpeg is the finishing and media operation layer. | It handles muxing, transcoding, audio normalization, proxies, frame extraction, and final export. |
| OpenTimelineIO is an audit/interchange artifact, not the canonical editor. | OTIO must reconstruct the edit for inspection and external tooling, but the canonical truth remains `VideoEditProgram`. |
| React video editors and OpenVideo-style UIs are review/edit surfaces only. | They may display and request structured revisions, but they cannot become the hidden production source of truth. |
| Generative media providers are materializers, not directors. | GPT Image 2, Flux 2, Qwen layered extraction, ComfyUI, SAM3 masks, background removal, and caption engines must operate through provider job plans. |
| Every timing decision must bind to `TranscriptClock`. | CMF is interview-first; the edit must respect actual spoken time, reaction pauses, and expression moments. |
| Every final render must require operator approval. | Eval passing is necessary but not sufficient for publishing or Guest Asset Pack delivery. |

## 4. Implementation Plan

### Step 1: Add Contracts and Registry Loaders

Create `contracts/video_edit_program.py` with the schema in Section 5. Add registry loaders for:

- `video_format_composition_grammars.v1.json`;
- `video_edit_eval_gate_set.v1.json`;
- `cmf_composition_primitive_triads.v1.json`.

The contract must validate:

- workspace and guest scope;
- source context refs;
- transcript clock;
- canonical format slot;
- scene time ranges;
- layer time ranges;
- layer/source refs;
- provider responsibility refs;
- primitive obligations;
- eval gate obligations.

### Step 2: Add Persistence and Program Hashing

Create repository methods for draft creation, compile save, provider plan save, proxy render contract save, eval receipt refs, approval refs, final render refs, OTIO manifest refs, and immutable receipt save.

The program hash must include:

- request hash;
- source context refs and hashes;
- transcript clock hash;
- format grammar version;
- scene and layer manifests;
- provider plan hash;
- renderer props hash;
- eval gate version;
- approval state.

### Step 3: Implement the Compiler Service

`video_edit_program_service.py` must implement:

1. Validate request and scope.
2. Load Brand Context, Interview Brief, Interview Asset Contract, Transcript Beat Map, Expression Moments, Voice/Visual DNA, Asset Package Spec, and Content Sequence Program where available.
3. Select the four-format slot and format grammar.
4. Compile `FormatCompositionContract`.
5. Compile `TranscriptClock`.
6. Bind beats to scenes with `BeatToSceneBinding`.
7. Call existing scene, reaction, PaperCut, 2D character, composition, and sonic services as needed.
8. Compile `VideoLayerManifest`, `CaptionLayoutPlan`, and `AudioMixPlan`.
9. Compile `ProviderJobPlan`.
10. Compile `VideoRenderContract`.
11. Persist draft, receipts, and review model.

### Step 4: Implement Provider Job Planning

Provider planning must describe work before execution. The compiler must be able to tell the operator:

- what providers will be called;
- why each provider is necessary;
- which layer or scene each job serves;
- whether output is deterministic, generated, masked, extracted, or transformed;
- expected cost and retry policy;
- approval requirement before final use.

Provider jobs include, but are not limited to:

- background removal for guest/interviewer cutouts;
- SAM3 segmentation/mask refinement;
- Qwen layered image extraction;
- GPT Image 2 or Flux 2 asset materialization;
- ComfyUI Docker worker jobs;
- rough-notation cue rendering;
- caption alignment;
- audio cleanup and loudness normalization;
- proxy frame generation;
- subscene render jobs from Motion Canvas or Manim.

### Step 5: Implement Render Runtime Binding

Render binding must produce:

- Remotion renderer props for the parent program;
- subscene manifests for Motion Canvas, Manim, PaperCut, or 2D avatar assets;
- FFmpeg finishing plan;
- deterministic input hashes;
- proxy render contract;
- final render contract.

The renderer must be locked by `TS-CMF-128` before final render. If the selected runtime differs between proxy and final render, the program must include a runtime-drift explanation and run post-render QA.

### Step 6: Implement OTIO Audit Export

`video_edit_otio_export_service.py` must export an `OTIOAuditManifest` that includes:

- tracks;
- clips;
- source media refs;
- timeline start/end;
- frame rate;
- markers for transcript beats and expression moments;
- scene boundaries;
- captions or text overlays as markers/effects;
- audio clips and mix decisions;
- generated asset refs;
- effect refs;
- render contract refs;
- approval/eval refs.

The OTIO export is required for final approval. Missing OTIO export blocks with `VIDEO_EDIT_OTIO_AUDIT_MISSING`.

### Step 7: Implement Eval Gates and Approval

Run the `VideoEditEvalGateSet` before approval. The gate set must call existing eval and approval services and must create blockers with repair targets.

Hard blockers:

- `VIDEO_EDIT_SOURCE_TIMING_MISSING`;
- `VIDEO_EDIT_BRAND_SCOPE_MISSING`;
- `VIDEO_EDIT_FORMAT_ROUTE_UNSUPPORTED`;
- `VIDEO_EDIT_FORMAT_FEEL_COLLAPSE`;
- `VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED`;
- `VIDEO_EDIT_DOCTRINE_EVAL_MISSING`;
- `VIDEO_EDIT_SUBJECT_MASK_UNSAFE`;
- `VIDEO_EDIT_CAPTION_LAYOUT_FAILED`;
- `VIDEO_EDIT_GENERATED_ASSET_SOURCE_DRIFT`;
- `VIDEO_EDIT_AUDIO_SOURCE_INTELLIGIBILITY_FAILED`;
- `VIDEO_EDIT_OTIO_AUDIT_MISSING`;
- `VIDEO_EDIT_OPERATOR_APPROVAL_REQUIRED`.

### Step 8: Implement PWA and Telegram Review Read Model

`VideoEditProgramReviewReadModel` must show:

- program summary;
- format slot and route reason;
- source refs and transcript coverage;
- timeline with scenes and beat bindings;
- proxy preview;
- layer stack;
- subject cutout/mask status;
- caption layout status;
- audio mix status;
- provider job status;
- eval gate status;
- blockers and repair commands;
- OTIO export readiness;
- approval state;
- final render readiness.

The PWA can allow structured revisions. It must not allow freehand timeline edits that bypass the program compiler.

### Pipeline Transformation and Receipt Chain Guard

Every state-changing step must write through the receipt chain guard. A `VideoEditProgramReceipt` is not a generic log entry; it is the immutable proof that the compiler transformed a specific input object into a specific output object under a named gate/version.

| Stage | Input Object(s) | Transformation | Output Object(s) | Receipt Chain Guard Write |
|---|---|---|---|---|
| Draft create | `CreateVideoEditProgramRequest` | Validate workspace, guest, source refs, target format, and request hash. | Draft `VideoEditProgram` shell. | `action=video_edit_program.draft_created`, table `video_edit_program_receipts`, idempotency key `workspace_id:guest_id:request_hash`. |
| Source load | Draft program, Brand Context, Interview Asset Contract, Transcript Beat Map, Expression Moments, source media refs. | Resolve source authority and reject cross-workspace refs. | `SourceCoverageSnapshot`. | `action=video_edit_program.source_loaded`, includes source hashes and blocker refs. |
| Format compile | Source snapshot, `format_slot`, grammar registry. | Resolve four-format grammar, route-specific primitives, required scenes/layers, and visual feel contract. | `FormatCompositionContract`. | `action=video_edit_program.format_compiled`, includes grammar version and route decision hash. |
| Transcript clock compile | Transcript beat map, source media timecode, target frame rate. | Align transcript time to source media and output timeline. | `TranscriptClock`. | `action=video_edit_program.transcript_clock_compiled`, includes alignment receipt and drift report. |
| Scene and layer compile | Format contract, transcript clock, scene specs, reaction routes, PaperCut/2D character subscenes. | Bind beats to scenes and materialize layer stack. | `VideoEditProgramScene[]`, `VideoLayerManifest[]`, `BeatToSceneBinding[]`. | `action=video_edit_program.scenes_compiled`, includes scene/layer hashes and primitive evidence refs. |
| Provider plan | Program scenes, layers, missing assets, provider registry. | Plan deterministic and generative provider jobs before execution. | `ProviderJobPlan`. | `action=video_edit_program.provider_planned`, includes provider plan hash, cost estimate, capability refs. |
| Proxy render | Program, provider outputs, renderer props, renderer lock. | Produce reviewable deterministic proxy. | Proxy `VideoRenderContract`. | `action=video_edit_program.proxy_rendered`, includes input asset hashes and proxy hash. |
| Eval gate run | Program, proxy, source coverage, provider receipts, OTIO readiness. | Run video edit gates and generate blockers/repair targets. | `VideoEditEvalGateSet`. | `action=video_edit_program.evaluated`, includes gate receipts and blocker refs. |
| Operator review | Review read model, eval gate set, proxy. | Approve, reject, waive eligible warnings, or request structured repair. | Approval or repair decision. | `action=video_edit_program.review_decided`, includes actor, decision, reason, waiver refs, and repair target. |
| Final render | Approved program, final render contract, provider receipts. | Render locked final master and run post-render QA. | Final `VideoRenderContract`, final media ref. | `action=video_edit_program.final_rendered`, includes render hash, QA receipt, and approval ref. |
| OTIO export | Final program, scenes, layers, clips, markers, effects. | Export reconstructable timeline audit artifact. | `OTIOAuditManifest`. | `action=video_edit_program.otio_exported`, includes OTIO hash and coverage report. |
| Package handoff | Final render, OTIO manifest, approval, eval receipts. | Bind asset to Guest Asset Pack or publishing intent. | Packaged video asset ref. | `action=video_edit_program.packaged`, includes package ref and final output hash. |

Receipt chain write requirements:

- every write includes `program_id`, `workspace_id`, `guest_id`, `actor_ref`, `input_hash`, `output_hash`, `gate_version`, and `created_at`;
- every write is idempotent by `(program_id, action, input_hash)`;
- every write emits a domain event with the same action name;
- failed stages still write a blocker receipt when they produce a deterministic rejection;
- repair commands must reference the receipt that caused the blocker.

## 5. Primary Output Schema

The schema below is the canonical contract target. Names may be split into modules during implementation, but field meaning must remain stable.

```python
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field


VideoFormatSlotCode = Literal["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"]
VideoProgramStatus = Literal[
    "draft",
    "compiled",
    "provider_planned",
    "proxy_rendered",
    "evaluated",
    "blocked",
    "approved",
    "final_rendered",
    "otio_exported",
    "packaged",
]
RenderKind = Literal["proxy", "final"]
RenderRuntimeCode = Literal["remotion", "motion_canvas", "manim", "ffmpeg", "composite"]
LayerRoleCode = Literal[
    "source_footage",
    "guest_cutout",
    "interviewer_cutout",
    "background_plate",
    "memory_object",
    "paper_cut_character",
    "avatar_character",
    "diagram",
    "annotation",
    "caption",
    "quote_overlay",
    "reaction_ui",
    "poll_ui",
    "ranking_ui",
    "tierlist_ui",
    "meme_cue",
    "audio_voice",
    "audio_music",
    "audio_sfx",
]
PrimitiveRoleCode = Literal["meaning_transform", "delivery_shape", "format_material"]
GateVerdictCode = Literal["PASS", "PROVISIONAL", "FAIL", "BLOCKED"]


class PrimitiveValidationRef(BaseModel):
    primitive_id: str = Field(pattern=r"^(PRM|EXP)-[A-Z]{3}-[0-9]{3}$")
    primitive_name: str
    role: PrimitiveRoleCode
    registry_ref: str
    minimum_score: float = Field(ge=0, le=1)
    observed_score: float | None = Field(default=None, ge=0, le=1)
    evidence_ref: str
    composition_element_ref: str
    decision: GateVerdictCode = "BLOCKED"


class VideoEditGateVerdict(BaseModel):
    gate_id: str
    gate_version: str
    gate_name: str
    verdict: GateVerdictCode
    threshold: str
    observed_value: str
    blocker_code: str | None = None
    repair_target: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    receipt_ref: str | None = None


class VideoEditReceiptChainWrite(BaseModel):
    action: str
    program_id: str
    workspace_id: str
    guest_id: str
    actor_ref: str
    input_hash: str
    output_hash: str
    gate_version: str | None = None
    idempotency_key: str
    event_name: str


class CreateVideoEditProgramRequest(BaseModel):
    workspace_id: str
    guest_id: str
    operator_id: str
    asset_package_id: str | None = None
    content_sequence_program_id: str | None = None
    interview_brief_id: str | None = None
    interview_asset_contract_id: str
    transcript_beat_map_id: str
    source_media_refs: list[str] = Field(min_length=1)
    expression_moment_refs: list[str] = Field(min_length=1)
    brand_context_version_id: str
    format_slot: VideoFormatSlotCode
    target_duration_ms: int = Field(gt=0)
    aspect_ratio: Literal["9:16", "1:1", "4:5", "16:9"] = "9:16"
    target_platforms: list[str] = Field(default_factory=list)
    primitive_ref_requirements: list[str] = Field(min_length=3, description="Exact registered primitive IDs only.")
    doctrine_gate_refs: list[str] = Field(min_length=1)
    requested_renderer: RenderRuntimeCode = "remotion"
    request_metadata: dict[str, Any] = Field(default_factory=dict)


class TranscriptClock(BaseModel):
    transcript_id: str
    source_media_ref: str
    source_frame_rate: float
    output_frame_rate: float
    source_time_start_ms: int
    source_time_end_ms: int
    output_time_start_ms: int
    output_time_end_ms: int
    drift_tolerance_ms: int = 80
    alignment_receipt_ref: str
    clock_hash: str


class FormatCompositionContract(BaseModel):
    format_slot: VideoFormatSlotCode
    grammar_version: str
    format_name: str
    required_scene_roles: list[str]
    required_layer_roles: list[LayerRoleCode]
    forbidden_layer_roles: list[LayerRoleCode] = Field(default_factory=list)
    visual_feel_contract_ref: str
    primitive_validations: list[PrimitiveValidationRef] = Field(min_length=3)
    doctrine_gate_refs: list[str] = Field(min_length=1)
    timing_rules_ref: str
    caption_rules_ref: str
    audio_rules_ref: str
    approval_requirements: list[str]


class BeatToSceneBinding(BaseModel):
    binding_id: str
    scene_id: str
    transcript_beat_id: str
    expression_moment_id: str | None = None
    source_time_start_ms: int
    source_time_end_ms: int
    timeline_time_start_ms: int
    timeline_time_end_ms: int
    source_quote_ref: str | None = None
    binding_reason: str
    primitive_refs: list[str] = Field(min_length=1, description="Exact registered primitive IDs only.")
    confidence_score: float = Field(ge=0, le=1)
    drift_ms: int


class VideoLayerManifest(BaseModel):
    layer_id: str
    scene_id: str
    track_id: str
    layer_role: LayerRoleCode
    z_index: int
    asset_ref: str | None = None
    generated_asset_ref: str | None = None
    source_media_ref: str | None = None
    time_start_ms: int
    time_end_ms: int
    safe_zone: dict[str, Any] = Field(default_factory=dict)
    transform: dict[str, Any] = Field(default_factory=dict)
    effect_refs: list[str] = Field(default_factory=list)
    layer_hash: str


class TrackedSubjectLayerManifest(BaseModel):
    layer_id: str
    subject_ref: str
    subject_role: Literal["guest", "interviewer", "host", "third_party"]
    mask_ref: str
    mask_provider_job_ref: str
    body_framing: Literal["face", "head_shoulders", "upper_body", "waist_up"]
    eye_line_target: str | None = None
    background_removed: bool
    occlusion_policy_ref: str
    identity_safety_receipt_ref: str
    mask_eval_receipt_ref: str


class PaperCutSubsceneManifest(BaseModel):
    subscene_id: str
    scene_id: str
    two_d_character_program_id: str | None = None
    rig_manifest_ref: str | None = None
    motion_recipe_ref: str
    textured_background_ref: str
    diagram_layer_refs: list[str] = Field(default_factory=list)
    rough_annotation_cue_refs: list[str] = Field(default_factory=list)
    transcript_concept_refs: list[str] = Field(min_length=1)
    subscene_render_contract_ref: str | None = None


class CaptionLayoutPlan(BaseModel):
    caption_plan_id: str
    word_alignment_ref: str
    caption_style_ref: str
    placement_policy_ref: str
    max_lines: int = Field(ge=1, le=4)
    max_chars_per_line: int = Field(ge=8)
    emphasis_token_refs: list[str] = Field(default_factory=list)
    collision_report_ref: str
    caption_eval_receipt_ref: str | None = None


class AudioMixPlan(BaseModel):
    audio_mix_plan_id: str
    voice_track_refs: list[str] = Field(min_length=1)
    music_track_refs: list[str] = Field(default_factory=list)
    sfx_track_refs: list[str] = Field(default_factory=list)
    silence_emphasis_ranges: list[dict[str, int]] = Field(default_factory=list)
    ducking_policy_ref: str
    loudness_target_lufs: float
    intelligibility_eval_receipt_ref: str | None = None


class VideoEditProgramScene(BaseModel):
    scene_id: str
    scene_index: int
    format_role: str
    timeline_start_ms: int
    timeline_end_ms: int
    scene_spec_ref: str | None = None
    reaction_template_route_ref: str | None = None
    paper_cut_subscene_ref: str | None = None
    two_d_character_program_ref: str | None = None
    beat_bindings: list[BeatToSceneBinding] = Field(min_length=1)
    layers: list[VideoLayerManifest] = Field(min_length=1)
    caption_plan_ref: str | None = None
    audio_mix_plan_ref: str | None = None
    scene_eval_receipt_refs: list[str] = Field(default_factory=list)
    scene_hash: str


class ProviderJobPlan(BaseModel):
    provider_plan_id: str
    program_id: str
    provider_job_refs: list[str]
    planned_capabilities: list[str]
    deterministic_jobs: list[str] = Field(default_factory=list)
    generative_jobs: list[str] = Field(default_factory=list)
    estimated_cost_usd: float = Field(ge=0)
    retry_policy_ref: str
    provider_plan_hash: str


class VideoRenderContract(BaseModel):
    render_contract_id: str
    program_id: str
    render_kind: RenderKind
    runtime: RenderRuntimeCode
    renderer_props_ref: str
    input_asset_hashes: list[str] = Field(min_length=1)
    expected_output_profile: dict[str, Any]
    proxy_ref: str | None = None
    final_master_ref: str | None = None
    render_hash: str | None = None
    render_receipt_ref: str | None = None


class OTIOAuditManifest(BaseModel):
    otio_manifest_id: str
    program_id: str
    otio_version: str
    otio_json_ref: str
    otio_hash: str
    coverage_report: dict[str, Any]
    source_clip_refs: list[str]
    track_refs: list[str]
    marker_refs: list[str]
    effect_refs: list[str]
    export_receipt_ref: str


class VideoEditEvalGateSet(BaseModel):
    gate_set_id: str
    program_id: str
    gate_registry_version: str
    source_gate_receipt_ref: str | None = None
    brand_scope_gate_receipt_ref: str | None = None
    transcript_timing_gate_receipt_ref: str | None = None
    format_feel_gate_receipt_ref: str | None = None
    primitive_gate_receipt_ref: str | None = None
    doctrine_gate_receipt_ref: str | None = None
    mask_gate_receipt_ref: str | None = None
    caption_gate_receipt_ref: str | None = None
    audio_gate_receipt_ref: str | None = None
    provider_drift_gate_receipt_ref: str | None = None
    otio_gate_receipt_ref: str | None = None
    gate_verdicts: list[VideoEditGateVerdict] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    approved_for_final_render: bool = False


class VideoEditProgram(BaseModel):
    program_id: str
    workspace_id: str
    guest_id: str
    status: VideoProgramStatus
    request_ref: str
    format_contract: FormatCompositionContract
    transcript_clock: TranscriptClock
    scenes: list[VideoEditProgramScene] = Field(min_length=1)
    caption_layout_plan: CaptionLayoutPlan
    audio_mix_plan: AudioMixPlan
    provider_job_plan: ProviderJobPlan | None = None
    proxy_render_contract: VideoRenderContract | None = None
    final_render_contract: VideoRenderContract | None = None
    eval_gate_set: VideoEditEvalGateSet | None = None
    otio_manifest: OTIOAuditManifest | None = None
    approval_ref: str | None = None
    program_hash: str
    created_at: datetime
    updated_at: datetime


class VideoEditProgramReceipt(BaseModel):
    receipt_id: str
    program_id: str
    receipt_type: Literal[
        "compiled",
        "provider_planned",
        "proxy_rendered",
        "evaluated",
        "approved",
        "final_rendered",
        "otio_exported",
        "packaged",
    ]
    actor_ref: str
    input_hash: str
    output_hash: str
    source_context_refs: list[str]
    eval_receipt_refs: list[str] = Field(default_factory=list)
    blocker_refs: list[str] = Field(default_factory=list)
    receipt_chain_write: VideoEditReceiptChainWrite
    approval_ref: str | None = None
    created_at: datetime


class VideoEditProgramReviewReadModel(BaseModel):
    program_id: str
    status: VideoProgramStatus
    workspace_label: str
    guest_label: str
    format_slot: VideoFormatSlotCode
    route_reason: str
    timeline_summary: list[dict[str, Any]]
    source_coverage: dict[str, Any]
    scene_cards: list[dict[str, Any]]
    layer_stack_summary: list[dict[str, Any]]
    provider_job_summary: list[dict[str, Any]]
    eval_gate_summary: list[dict[str, Any]]
    blocker_summary: list[dict[str, Any]]
    proxy_preview_ref: str | None
    otio_manifest_ref: str | None
    approval_actions: list[str]
    repair_commands: list[dict[str, Any]]
```

### Format Composition JSON Requirements

`FormatCompositionContract` must resolve a JSON grammar for each format:

```json
{
  "format_slot": "SV-RRC",
  "format_name": "Reaction / Recognition Clip",
  "required_scene_roles": [
    "context_setup",
    "human_reaction",
    "quote_recognition",
    "participation_prompt"
  ],
  "required_layer_roles": [
    "source_footage",
    "guest_cutout",
    "interviewer_cutout",
    "caption",
    "quote_overlay",
    "reaction_ui"
  ],
  "timing_rules": {
    "reaction_pause_min_ms": 240,
    "reaction_pause_max_ms": 1800,
    "quote_hold_min_ms": 900,
    "cut_on_expression_moment": true
  },
  "primitive_validations": [
    {
      "primitive_id": "PRM-PSY-001",
      "primitive_name": "Matching Principle",
      "role": "meaning_transform",
      "registry_ref": "registries/primitives/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml",
      "minimum_score": 0.86,
      "evidence_ref": "expression_moment:em_042",
      "composition_element_ref": "scene:human_reaction",
      "decision": "PASS"
    },
    {
      "primitive_id": "PRM-REF-009",
      "primitive_name": "Constructive Tension Control",
      "role": "delivery_shape",
      "registry_ref": "registries/primitives/meaning_plane/referral_trust_transfer/PRM-REF-009.yaml",
      "minimum_score": 0.84,
      "evidence_ref": "transcript_beat:tb_118",
      "composition_element_ref": "timing:reaction_pause_hold",
      "decision": "PASS"
    },
    {
      "primitive_id": "PRM-VSG-015",
      "primitive_name": "Composition as Attention Routing",
      "role": "format_material",
      "registry_ref": "registries/primitives/meaning_plane/visual_sonic_guidance/PRM-VSG-015.yaml",
      "minimum_score": 0.86,
      "evidence_ref": "layer_stack:upper_reaction_ui_lower_subject_cutouts",
      "composition_element_ref": "scene:reaction_frame",
      "decision": "PASS"
    }
  ],
  "approval_blockers": [
    "VIDEO_EDIT_SOURCE_TIMING_MISSING",
    "VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED",
    "VIDEO_EDIT_OPERATOR_APPROVAL_REQUIRED"
  ]
}
```

## 6. Backward Compatibility Fallback

Existing scene and render contracts remain valid as lower-level building blocks. This spec does not invalidate:

- `SceneSpec`;
- reaction editing routes;
- composition JSON;
- deterministic renderer props;
- sonic timeline contracts;
- provider job receipts;
- 2D character programs;
- PaperCut subscene manifests;
- still visual composition programs.

Fallback rules:

| Existing Capability | Compatibility Rule |
|---|---|
| Standalone `SceneSpec` render | Allowed for lab previews and isolated component tests, but not sufficient for final Guest Asset Pack video delivery. |
| Reaction template route from TS-CMF-071 | Must become a `VideoEditProgramScene` input when used in a complete video. |
| PaperCut or 2D avatar render | Must be referenced through `PaperCutSubsceneManifest` or `two_d_character_program_ref`. |
| Deterministic render contract | Remains the render authority, but is wrapped by proxy and final `VideoRenderContract`. |
| Open-source UI editor | Can display and request structured repairs. It cannot overwrite canonical program state. |
| Manual editing in external tools | Allowed only as an external review/export path when OTIO coverage and approval receipts remain intact. |

No production path may export a final video from:

- a browser screenshot;
- an untracked video editor timeline;
- a generated video file with no source refs;
- a provider output that lacks a provider job receipt;
- a template preview with no transcript clock;
- a composition with no primitive triad.

## 7. Tasks

| Task ID | Task | Owner Area | Done When |
|---|---|---|---|
| T106-001 | Create `contracts/video_edit_program.py`. | Contracts | All Section 5 models validate with Pydantic v2 and generated TypeScript contracts. |
| T106-002 | Create video format grammar registry. | Registries | `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC` load with scene, layer, timing, primitive, and eval obligations. |
| T106-003 | Create video edit eval gate registry. | Registries/Evals | All hard blockers are registered with severity, repair target, waiver policy, and CBAR mandate. |
| T106-004 | Create `video_edit_program` repository. | Persistence | Program, scene, beat binding, layer, provider plan, render contract, OTIO manifest, and receipt persistence exists. |
| T106-005 | Implement compiler service. | Services | Request compiles into valid `VideoEditProgram` using existing scene/composition/reaction/sonic services. |
| T106-006 | Implement transcript clock validation. | Services | Source media, transcript beat map, and output timeline drift checks block unsafe edits. |
| T106-007 | Implement provider job planner integration. | Services/Providers | Provider plans are created before execution and each job maps to scene/layer responsibility. |
| T106-008 | Implement render contract integration. | Render Workflow | Proxy and final render contracts are produced with renderer locks and input hashes. |
| T106-009 | Implement OTIO audit exporter. | Services | OTIO JSON and coverage report reconstruct program scenes, clips, tracks, effects, and markers. |
| T106-010 | Implement eval gate orchestration. | Evals | Gate set calls existing doctrine/eval services and emits blockers/receipts. |
| T106-011 | Implement approval gate integration. | Approval | Final render is blocked until evals pass and operator approval exists. |
| T106-012 | Implement API route family. | FastAPI | Routes in Section 3 exist with request/response validation. |
| T106-013 | Implement review read model. | PWA/Telegram | Operator can inspect timeline, source, layers, proxy, evals, blockers, and repair commands. |
| T106-014 | Add golden fixtures for four formats. | Tests | Each canonical format has source fixtures, expected program JSON, eval receipts, and render contract. |
| T106-015 | Add OTIO replay/coverage tests. | Tests | OTIO manifest covers 100 percent of required source clips, scenes, and markers. |

## 8. Acceptance Criteria

| AC-ID | Criterion | Failure Example | CBAR / Blocker |
|---|---|---|---|
| AC106-01 | A valid request compiles into a `VideoEditProgram` with source refs, transcript clock, format contract, scenes, beat bindings, caption plan, audio plan, and program hash. | Compiler returns only a Remotion props object. | `Phase5-M01`; `VIDEO_EDIT_SOURCE_TIMING_MISSING` |
| AC106-02 | Each scene is bound to at least one transcript beat or approved non-human contextual insert. | Scene exists because "it looks good" with no beat or source ref. | `Phase4-M01`; `VIDEO_EDIT_SOURCE_TIMING_MISSING` |
| AC106-03 | Each program declares one of the four canonical slots and loads matching grammar. | Program accepts `viral_clip` or another unsupported route. | `Phase4-M03`; `VIDEO_EDIT_FORMAT_ROUTE_UNSUPPORTED` |
| AC106-04 | Format feel cannot collapse across routes. | Cinematic story, PaperCut explainer, and reaction poll all share the same dark hype template. | `Phase4-M02`; `VIDEO_EDIT_FORMAT_FEEL_COLLAPSE` |
| AC106-05 | At least three registered primitives validate at program level with exact YAML IDs, role coverage for `meaning_transform`, `delivery_shape`, and `format_material`, and every required score meets its route threshold from `CMF-COMP-PRIMITIVE-TRIADS-001`. | Program includes primitive names as free text with no registry IDs. | `Phase4-M02`; `VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED` |
| AC106-06 | Brand and guest workspace scope are enforced. | A guest cutout or Brand Genesis asset from another workspace is included. | `Phase4-M01`; `VIDEO_EDIT_BRAND_SCOPE_MISSING` |
| AC106-07 | Tracked subject layers include mask refs, safety receipts, and framing rules. | Guest background removal is used with no mask receipt or identity safety check. | `Phase4-M04`; `VIDEO_EDIT_SUBJECT_MASK_UNSAFE` |
| AC106-08 | Captions pass placement, collision, readability, and transcript alignment gates: `<=120ms` timing drift, zero safe-zone/face collisions, max four lines, and contrast ratio `>=4.5:1`. | Captions cover the guest face or drift from spoken words. | `Phase4-M04`; `VIDEO_EDIT_CAPTION_LAYOUT_FAILED` |
| AC106-09 | Audio mix passes intelligibility and loudness checks: voice intelligibility `>=0.86`, loudness `-16 LUFS +/- 1`, true peak `<= -1 dBTP`, and speech-bed ducking `>=12 dB`. | Music bed buries the guest voice or final loudness is outside target. | `Phase4-M04`; `VIDEO_EDIT_AUDIO_SOURCE_INTELLIGIBILITY_FAILED` |
| AC106-10 | Generated assets are tied to source context, provider receipts, and layer roles with unsupported claim count `0` and source alignment score `>=0.88`. | A visual insert invents an unsupported biographical detail. | `Phase4-M01`; `VIDEO_EDIT_GENERATED_ASSET_SOURCE_DRIFT` |
| AC106-11 | OTIO export is created before final approval and covers `100%` of required tracks, clips, scenes, and markers. | Final render exists but no reconstructable timeline artifact exists. | `Phase5-M01`; `VIDEO_EDIT_OTIO_AUDIT_MISSING` |
| AC106-12 | Final render cannot execute without successful eval gates and explicit operator approval. | Final master renders after proxy render without review decision. | `Phase4-M04`; `VIDEO_EDIT_OPERATOR_APPROVAL_REQUIRED` |
| AC106-13 | Review read model exposes repair commands for every blocker. | Operator sees "failed eval" but no target, cause, or repair path. | `Phase4-M05` |
| AC106-14 | Four golden fixtures compile, proxy render, evaluate, export OTIO, and produce receipts for every state-changing pipeline stage. | Only the reaction format has tests. | `Phase5-M01` |

## 9. Dependencies

### Upstream Dependencies

| Dependency | Required From |
|---|---|
| Brand Context version | Brand Genesis / substrate resolver. |
| Interview Brief and Interview Asset Contract | Interview-first pipeline and sequence procurement. |
| Transcript Beat Map | TS-CMF-084. |
| Expression Moments | CCP V9/V9.1 expression extraction. |
| Content Sequence Program | TS-CMF-118 when available. |
| Format Slot | TS-CMF-078. |
| Visual Feel Contract | TS-CMF-079. |
| Composition Runtime Binding | TS-CMF-080. |
| Reaction Template Route | TS-CMF-071/072/074 when using reaction formats. |
| PaperCut and 2D Character Programs | TS-CMF-086 and TS-CMF-110 through TS-CMF-113. |
| Provider Capability Registry | TS-CMF-123/124. |
| Reference Footage Intake | TS-CMF-126/127 when using existing footage. |
| Render Runtime Lock | TS-CMF-128. |
| Pre-compose and Post-render QA | TS-CMF-129/130. |
| Approval Protocol | TS-CMF-132. |

### External Technology Dependencies

| Technology | Role | Boundary |
|---|---|---|
| Remotion | Parent render spine for deterministic timeline composition. | Receives locked renderer props from `VideoEditProgram`; does not own source truth. |
| Motion Canvas | Animated educational subscenes and diagrams. | Emits rendered subscene clips/manifests back to parent program. |
| Manim | Procedural math/diagram explainer inserts. | Narrow subscene worker only. |
| FFmpeg | Proxy generation, muxing, audio normalization, transcode, final export. | Media operation layer. |
| OpenTimelineIO | Timeline audit/interchange export. | Audit artifact, not canonical source of truth. |
| SAM3 / background removal | Subject and object masks. | Provider job outputs with safety receipts. |
| Qwen layered extraction | Layer extraction from approved composition plates. | Materializer only. |
| GPT Image 2 / Flux 2 / ComfyUI worker | Generated plates, assets, backgrounds, and visual inserts. | Provider jobs with source binding and drift checks. |
| rough-notation | Text and annotation animation cues. | Deterministic annotation cues inside renderer props or subscene manifests. |
| React video editor / OpenVideo-style UI | Operator review and structured repair UX. | Cannot directly mutate canonical program JSON. |

## 10. Testing Strategy

### Unit Tests

| Test | Expectation |
|---|---|
| `test_create_video_edit_program_request_requires_source_scope` | Missing workspace, guest, interview asset contract, transcript beat map, or source media fails validation. |
| `test_format_slot_must_be_canonical` | Non-canonical format codes fail with `VIDEO_EDIT_FORMAT_ROUTE_UNSUPPORTED`. |
| `test_transcript_clock_detects_drift` | Source/output time drift beyond tolerance fails. |
| `test_primitive_triads_require_registry_refs` | Free-text primitive declarations fail. |
| `test_route_primitive_triads_match_registry_thresholds` | Each format uses exact required primitive IDs, role coverage, and minimum scores from `CMF-COMP-PRIMITIVE-TRIADS-001`. |
| `test_gate_verdicts_require_threshold_and_receipt_ref` | Each gate verdict carries threshold, observed value, blocker/repair target when applicable, and receipt ref after evaluation. |
| `test_video_layer_manifest_requires_time_bounds` | Layers outside scene or program time range fail. |
| `test_subject_layer_requires_mask_and_identity_receipts` | Subject cutouts without mask/safety refs fail. |
| `test_receipt_chain_write_is_idempotent_by_program_action_input_hash` | Duplicate state-changing writes do not create duplicate receipts. |

### Integration Tests

| Test | Expectation |
|---|---|
| `test_video_edit_program_compiles_cinematic_story_commentary` | `SV-CSC` fixture compiles with memory-object layers, emotional captions, audio plan, eval gates, and proxy render contract. |
| `test_video_edit_program_compiles_educational_papercut_explainer` | `SV-EDU` fixture compiles with PaperCut/2D character subscene manifests and rough annotation cues. |
| `test_video_edit_program_compiles_challenger_frame_breaker` | `SV-FRB` fixture compiles with contrast UI, evidence refs, format feel gates, and edge integrity evals. |
| `test_video_edit_program_compiles_reaction_recognition_clip` | `SV-RRC` fixture compiles with upper-body cutouts, reaction timing, quote overlays, participatory UI, and mask receipts. |
| `test_provider_job_plan_maps_every_job_to_layer` | Each provider job maps to scene/layer/capability/provider responsibility. |
| `test_proxy_render_requires_renderer_lock` | Proxy render contract includes runtime, renderer props, and input hashes. |
| `test_final_render_requires_approval` | Final render route fails without approval ref. |
| `test_otio_manifest_covers_all_scenes_and_clips` | OTIO coverage report reaches `1.00` for scenes, source clips, and required markers. |
| `test_each_pipeline_stage_writes_receipt_chain_guard` | Draft, source load, format compile, transcript clock, scene compile, provider plan, proxy render, eval, review, final render, OTIO export, and package handoff each write receipts. |

### Golden Fixtures

Create fixture packs:

| Fixture | Required Coverage |
|---|---|
| `fixtures/video_edit/sv_csc_claude_origin_story.json` | Cinematic Story Commentary with memory inserts and emotional subtitles. |
| `fixtures/video_edit/sv_edu_papercut_concept.json` | Educational / Explainer with PaperCut, character rig, diagrams, and rough annotations. |
| `fixtures/video_edit/sv_frb_frame_breaker_poll.json` | Challenger / Frame Breaker with contrast panel, evidence cards, punch-ins, and caption emphasis. |
| `fixtures/video_edit/sv_rrc_living_reaction.json` | Reaction / Recognition Clip with guest/interviewer cutouts, split-frame reaction, quote hold, and pause preservation. |

### Negative Fixtures

| Fixture | Expected Blocker |
|---|---|
| `missing_transcript_clock.json` | `VIDEO_EDIT_SOURCE_TIMING_MISSING` |
| `wrong_guest_workspace_asset.json` | `VIDEO_EDIT_BRAND_SCOPE_MISSING` |
| `unsupported_format_route.json` | `VIDEO_EDIT_FORMAT_ROUTE_UNSUPPORTED` |
| `generic_visual_feel_all_formats.json` | `VIDEO_EDIT_FORMAT_FEEL_COLLAPSE` |
| `primitive_names_without_registry_refs.json` | `VIDEO_EDIT_PRIMITIVE_TRIAD_NOT_VALIDATED` |
| `generated_asset_invents_story_detail.json` | `VIDEO_EDIT_GENERATED_ASSET_SOURCE_DRIFT` |
| `unsafe_subject_mask.json` | `VIDEO_EDIT_SUBJECT_MASK_UNSAFE` |
| `captions_overlap_face.json` | `VIDEO_EDIT_CAPTION_LAYOUT_FAILED` |
| `music_overpowers_voice.json` | `VIDEO_EDIT_AUDIO_SOURCE_INTELLIGIBILITY_FAILED` |
| `final_render_without_otio.json` | `VIDEO_EDIT_OTIO_AUDIT_MISSING` |
| `final_render_without_approval.json` | `VIDEO_EDIT_OPERATOR_APPROVAL_REQUIRED` |

### Determinism and Reproducibility Tests

- Same request and same provider artifacts produce the same program hash.
- Same program and same renderer inputs produce the same proxy render hash.
- OTIO export hash remains stable for unchanged program state.
- Any provider output change changes provider plan hash and program hash.
- Any approval waiver changes receipt hash and review read model state.

### Operator Review Tests

- Review model shows exact source context, format route, scene timeline, layer stack, proxy preview, eval gates, blockers, repair commands, OTIO status, and approval actions.
- Operator can approve only when hard blockers are clear.
- Operator can waive only eligible warning blockers.
- Operator can request structured repair against scene, layer, caption, audio, provider, primitive, route, or OTIO target.

### Build Completion Definition

TS-CMF-106 is implementation-complete only when:

1. `VideoEditProgram` contracts exist and generate TypeScript.
2. Four format grammar fixtures exist.
3. Program compiler integrates existing scene, composition, reaction, sonic, provider, eval, render, and approval services.
4. Proxy render and final render contracts are emitted.
5. OTIO audit export exists and passes coverage tests.
6. Four positive and eleven negative fixtures pass.
7. PWA/Telegram review read models expose blockers and repair commands.
8. Final render is impossible without approval.
9. `VideoEditProgramReceipt` is emitted for compile, eval, approval, final render, and OTIO export.
