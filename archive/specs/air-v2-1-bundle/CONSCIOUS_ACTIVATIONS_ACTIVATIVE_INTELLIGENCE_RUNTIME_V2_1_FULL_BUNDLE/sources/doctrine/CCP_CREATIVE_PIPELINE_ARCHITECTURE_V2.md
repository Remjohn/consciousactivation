# Conscious Media Factory Creative Pipeline Architecture V2

**Project:** Conscious Coaching Platform / Conscious Elite  
**Subsystem:** Conscious Media Factory (CMF)  
**Document Type:** Production Architecture + Agentic Creative Pipeline Contract  
**Version:** V2.0  
**Status:** Draft for implementation hardening  
**Primary Objective:** Convert the CCP creative/media pipeline from a strategic concept into an executable, schema-driven, renderer-agnostic creative operating system.

---

## 0. What Changed From V1

V1 defined the creative direction. V2 turns it into a more executable architecture.

This version adds:

1. explicit system boundaries,
2. a canonical Creative State Object,
3. stricter schemas for the main production objects,
4. a renderer routing matrix and decision tree,
5. a stronger Ideogram 4 composition contract,
6. a complete 64-state acting-library taxonomy,
7. reference retrieval scoring and fallback logic,
8. layer extraction contracts,
9. a visual style constitution for the paper-cut / stop-motion aesthetic,
10. pass/fail quality gates,
11. asset governance and object-storage conventions,
12. phase promotion and kill criteria.

The core architecture remains:

```text
Trigger / content intent
        -> Creative brief
        -> Scene specification
        -> Ideogram 4 composition
        -> approved acting-reference retrieval
        -> Flux 2 / Flux Kontext edit and character replacement
        -> layer extraction / asset preparation
        -> animation routing
        -> renderer compilation
        -> evaluation receipt
```

The key design principle is unchanged:

> The CMF should be a creative harness, not a single model wrapper.

---

# I. System Boundary

## I.1 What This Document Covers

This document defines the production architecture for the CCP creative/media pipeline.

It covers:

- visual scene specification,
- composition generation,
- identity-conditioned character replacement,
- approved acting-reference retrieval,
- paper-cut / stop-motion visual system,
- GPT Image 2 / image-editing asset factory,
- Flux 2 / Flux Kontext edit stage,
- layer extraction and layer manifests,
- 2D character rigging and modular animation,
- SCAIL-2 motion-transfer branch,
- cinematic video-generation branch,
- Remotion / Manim / Motion Canvas / HyperFrames renderer routing,
- data-story and quiz/ranking video branches,
- render receipts,
- quality gates,
- asset governance,
- implementation phases.

## I.2 What This Document Does Not Cover

This document does not replace the broader CCP architecture.

It does not define:

- the full Voice DNA extraction system,
- the complete Trigger Map engine,
- the Telegram invisible-app runtime,
- Neo4j client telemetry,
- sales-cycle logic,
- client coaching intervention policy,
- full CRAL research architecture,
- business intelligence and Tribe Soul extraction,
- Notion operations UX.

Those systems feed the creative pipeline, but they are not redefined here.

## I.3 Integration Point With CCP

The creative pipeline operates inside the CCP **Complete Editing Session** boundary.

The Complete Editing Session is the atomic production wrapper. It contains identity, trigger, context, process state, prefetched assets, validation metadata, render outputs, and receipts.

A creative workflow does not ship unless it can execute inside this wrapper.

---

# II. Core Creative Doctrine

## II.1 Orchestration Over Generation

The CMF does not ask one model to create the final artifact.

Instead, it decomposes creative production into separate contracts:

```text
Narrative intent
-> scene spec
-> composition plate
-> identity reference selection
-> controlled edit / replacement
-> layer preparation
-> animation plan
-> deterministic or generative renderer
-> evaluation receipt
```

Each stage has:

- typed inputs,
- typed outputs,
- acceptance criteria,
- failure modes,
- retry paths.

This prevents the system from becoming an untestable pile of prompts.

## II.2 Composition Before Rendering

Composition is the first creative bottleneck.

The system must decide:

- where the character stands,
- what the viewer sees first,
- where the text area lives,
- which objects carry the metaphor,
- how the eye moves through the frame,
- how emotional meaning is spatialized.

Therefore, Ideogram 4 is treated as the **composition-control engine**.

The output of Ideogram is a composition plate, not the final identity-correct production image.

## II.3 Identity Is Compiled, Not Improvised

Identity conditioning models are fixed at container build time.

Approved reference images live in object storage as a versioned reference album.

Neither changes at runtime.

Runtime agents may only:

- retrieve references,
- rank references,
- select references,
- combine approved primary and secondary references.

Runtime agents may not:

- train identity models,
- swap identity conditioning models,
- add unapproved references,
- mutate the identity pack.

This gives deterministic identity behavior between runs on the same container version.

## II.4 Acting Library, Not Pose Library

The 48-64 approved references should not be thought of as a pose set.

They are an **acting library**.

The primary retrieval axis is:

```text
communicative intent
-> emotional state
-> body language
-> gesture
-> facial expression
-> framing / layout utility
```

The point is not to cover every geometric pose.

The point is to cover enough meaningful performance states to let the agent choose the correct emotional reference for a scene.

## II.5 Imperfection as a Design Advantage

The preferred scalable visual language is:

```text
paper cut-out
stop-motion
felt and paper collage
textured cream paper
handmade shadows
small expressive cutout characters
colorful symbolic props
```

This style is strategically strong because:

- it is distinctive,
- it is warm and tactile,
- it is compatible with coaching content,
- it is forgiving of small AI artifacts,
- it decomposes naturally into layers,
- it can be animated deterministically,
- it avoids competing directly with photorealistic AI video.

In this style, imperfection is not a flaw. It is part of the signal.

## II.6 Determinism Is a Product Feature

The CMF should separate two forms of determinism.

### Identity determinism

Identity consistency is deterministic when the following are fixed:

- container version,
- identity model weights,
- identity conditioning stack,
- approved reference album,
- workflow graph,
- reference hashes.

### Pixel determinism

Pixel-level reproducibility additionally requires:

- seed,
- sampler,
- scheduler,
- model precision,
- workflow JSON,
- runtime hardware behavior,
- exact dependency versions.

The execution receipt must record all of these.

---

# III. High-Level Architecture

## III.1 Main Pipeline

```text
Content trigger / creative intent
        |
        v
Creative Brief Agent
        |
        v
SceneSpec JSON
        |
        v
Ideogram 4 Composition Compiler
        |
        v
Composition Plate
        |
        v
Acting Reference Retrieval
        |
        v
Flux 2 / Flux Kontext Edit Job
        |
        v
Refined Production Image / Asset Pack
        |
        v
Layer Extraction / Rig Preparation
        |
        v
Renderer Router
        |-------------------------------|
        |                               |
        v                               v
Deterministic 2D branch           Generative video branch
        |                               |
        v                               v
Remotion / Motion Canvas /        Veo / Kling / Seedance /
Manim / HyperFrames /             Wan-style model / SCAIL-2
Stretchy Studio
        |                               |
        |---------------|---------------|
                        v
                 Final Render
                        |
                        v
             Evaluation + Receipt
```

## III.2 Two Creative Super-Branches

The CMF has two major creative branches.

### Branch A: Deterministic 2D / motion-graphics branch

Used when editability, consistency, and brand repeatability matter most.

Best for:

- paper-cut explainers,
- animated avatar explainers,
- quizzes,
- rankings,
- data stories,
- coach commentary edits,
- subtitles and annotations,
- reusable social video formats.

### Branch B: Generative video branch

Used when cinematic complexity matters more than editability.

Best for:

- atmospheric cinematic metaphors,
- realistic motion,
- complex camera movement,
- dreamlike memory scenes,
- brand films,
- surreal transitions.

The default should be Branch A unless the creative task clearly demands Branch B.

---

# IV. Canonical Creative State Object

## IV.1 Purpose

The Creative State Object is the single evolving state object for a creative job.

It prevents the pipeline from fragmenting into unrelated prompts, files, and model outputs.

Every stage reads and writes to this object.

## IV.2 Creative State Object

```json
{
  "creative_state_id": "cs_2026_000001",
  "session_id": "ces_2026_000001",
  "coach_id": "coach_emmanuel",
  "stage": "composition_generated",
  "status": "in_progress",
  "identity_pack_id": "emmanuel_brand_actor_v1",
  "container_version": "cmf-image-worker:2026.06.16",
  "content_intent": {},
  "trigger_context": {},
  "voice_dna_context": {},
  "visual_negative_space": {},
  "scene_spec": {},
  "composition_job": {},
  "composition_outputs": [],
  "selected_references": [],
  "edit_jobs": [],
  "edit_outputs": [],
  "layer_manifest": null,
  "animation_plan": null,
  "renderer_route": null,
  "render_manifest": null,
  "evaluation_receipt": null,
  "lineage": [],
  "errors": [],
  "manual_review_flags": []
}
```

## IV.3 Required State Transitions

```text
created
-> brief_compiled
-> scene_spec_validated
-> composition_requested
-> composition_generated
-> references_selected
-> edit_requested
-> edit_generated
-> layers_extracted
-> animation_planned
-> renderer_selected
-> rendered
-> evaluated
-> approved | rejected | needs_retry | needs_manual_review
```

No stage may be skipped unless explicitly marked as not applicable.

---

# V. Production Object Schemas

This section provides implementation-oriented schemas. They are not final JSON Schema files, but they define the contracts that should become JSON Schema or Pydantic models.

## V.1 SceneSpec

The SceneSpec is the core creative source of truth.

```json
{
  "scene_id": "scene_001",
  "format": "vertical_video",
  "aspect_ratio": "9:16",
  "duration_seconds": 12,
  "content_type": "paper_cutout_explainer",
  "visual_style": "paper_cutout_stop_motion",
  "platform_target": ["linkedin", "tiktok", "youtube_shorts"],
  "message_role": "hook",
  "emotional_intent": "confident_reframe",
  "subject": {
    "identity_pack_id": "emmanuel_brand_actor_v1",
    "role": "personal_brand_paper_cut_character",
    "emotion": "confident",
    "gesture": "open_hands_explaining",
    "body_language": "upright_open",
    "facial_expression": "half_smile",
    "position": "lower_left_third",
    "scale": "small_medium"
  },
  "composition": {
    "main_metaphor": "climbing a colorful mountain",
    "visual_flow": "bottom_left_to_top_right",
    "text_area": "upper_right",
    "depth_layers": ["background", "midground", "foreground"],
    "objects": [
      {
        "type": "paper_mountain",
        "position": "center_bottom",
        "symbolic_role": "growth_obstacle"
      },
      {
        "type": "paper_arrow",
        "position": "right_rising",
        "symbolic_role": "forward_motion"
      }
    ]
  },
  "style": {
    "material": "textured_cream_paper",
    "texture_level": "visible",
    "color_palette": "warm_colorful_handmade",
    "shadow_style": "soft_paper_shadow",
    "edge_style": "imperfect_cutout"
  },
  "motion_intent": {
    "motion_style": "tactile_stop_motion",
    "camera_motion": "locked_with_subtle_push",
    "layer_motion": ["paper_wiggle", "subtle_parallax", "arrow_bounce"],
    "character_motion": ["blink", "small_hand_emphasis"]
  },
  "negative_constraints": {
    "forbidden_visuals": ["glossy_3d", "corporate_vector_saas", "photorealistic_avatar"],
    "forbidden_mood": ["sterile", "cold", "generic_ai_art"]
  }
}
```

## V.2 IdentityPack

```json
{
  "identity_pack_id": "emmanuel_brand_actor_v1",
  "coach_id": "coach_emmanuel",
  "runtime_mutable": false,
  "container_version": "cmf-image-worker:2026.06.16",
  "model_digest": "sha256:MODEL_DIGEST",
  "conditioning_stack": [
    {
      "name": "fixed_face_identity_adapter",
      "version": "v1",
      "digest": "sha256:..."
    },
    {
      "name": "fixed_ip_adapter",
      "version": "v1",
      "digest": "sha256:..."
    },
    {
      "name": "fixed_pulid_or_instantid",
      "version": "v1",
      "digest": "sha256:..."
    }
  ],
  "reference_album": {
    "album_id": "emmanuel_64_acting_refs_v1",
    "storage_uri": "s3://ccp-assets/identity_packs/emmanuel/v1/acting_refs/",
    "album_hash": "sha256:ALBUM_HASH",
    "reference_count": 64
  },
  "allowed_runtime_actions": [
    "select_reference",
    "rank_reference",
    "combine_primary_secondary_reference"
  ],
  "forbidden_runtime_actions": [
    "train_identity_model",
    "swap_identity_model",
    "add_unapproved_reference",
    "modify_identity_conditioning"
  ]
}
```

## V.3 ActingReference

```json
{
  "reference_id": "act_confident_open_explain_01",
  "identity_pack_id": "emmanuel_brand_actor_v1",
  "asset_uri": "s3://ccp-assets/identity_packs/emmanuel/v1/acting_refs/act_confident_open_explain_01.png",
  "asset_hash": "sha256:...",
  "approval_status": "approved",
  "emotion_primary": "confident",
  "emotion_secondary": "warm",
  "communicative_intent": "explaining important idea",
  "gesture_family": "open_hands_explaining",
  "body_language": "upright_open",
  "facial_expression": "confident_half_smile",
  "energy_level": "medium_high",
  "hand_visibility": "both_hands_visible",
  "orientation": "front_3_4_right",
  "framing": "medium_shot",
  "layout_bias": "left_third",
  "text_space": "right",
  "best_use_cases": [
    "linkedin_explainer",
    "framework_breakdown",
    "personal_brand_commentary"
  ],
  "do_not_use_for": [
    "sad_memory",
    "grief_context",
    "high_urgency_warning"
  ]
}
```

## V.4 CompositionJob

```json
{
  "composition_job_id": "comp_001",
  "scene_id": "scene_001",
  "provider": "ideogram_4",
  "purpose": "composition_plate",
  "prompt": "Vertical 9:16 paper cut-out stop-motion composition...",
  "prompt_hash": "sha256:...",
  "constraints": {
    "aspect_ratio": "9:16",
    "subject_position": "lower_left_third",
    "text_area": "upper_right",
    "visual_flow": "bottom_left_to_top_right",
    "style": "paper_cutout_stop_motion"
  },
  "output_requirements": {
    "must_leave_text_space": true,
    "must_have_discrete_objects": true,
    "must_not_finalize_identity": true
  }
}
```

## V.5 EditJob

```json
{
  "edit_job_id": "edit_001",
  "provider": "flux_2_edit_or_flux_kontext",
  "input_composition_uri": "s3://.../composition.png",
  "identity_pack_id": "emmanuel_brand_actor_v1",
  "selected_references": [
    {
      "role": "primary_body_language",
      "reference_id": "act_confident_open_explain_01"
    },
    {
      "role": "secondary_identity_anchor",
      "reference_id": "face_confident_half_smile_03"
    }
  ],
  "edit_instruction": "Preserve the composition and paper-cut style. Replace the generic character with the approved brand character using the primary acting reference. Keep the emotion confident and the gesture open-hands explaining.",
  "preserve": [
    "composition",
    "text_area",
    "visual_flow",
    "paper_texture",
    "object_positions"
  ],
  "modify": [
    "generic_character_identity",
    "character_face",
    "character_body_language",
    "character_integration"
  ],
  "hard_constraints": [
    "do_not_change_scene_layout",
    "do_not_introduce_unapproved_identity",
    "do_not_remove_text_space"
  ]
}
```

## V.6 LayerManifest

```json
{
  "layer_manifest_id": "layers_001",
  "source_asset_uri": "s3://.../edited_scene.png",
  "canvas": {
    "width": 1080,
    "height": 1920,
    "aspect_ratio": "9:16"
  },
  "layers": [
    {
      "layer_id": "background_paper",
      "semantic_type": "background",
      "file_uri": "s3://.../background_paper.png",
      "z_index": 0,
      "bbox": [0, 0, 1080, 1920],
      "anchor_point": [0.5, 0.5],
      "alpha_quality_score": 1.0,
      "edge_quality_score": 1.0,
      "casts_shadow": false,
      "motion_affordances": ["camera_push", "grain_jitter"]
    },
    {
      "layer_id": "paper_arrow_01",
      "semantic_type": "paper_arrow",
      "file_uri": "s3://.../paper_arrow_01.png",
      "z_index": 12,
      "bbox": [600, 780, 260, 110],
      "anchor_point": [0.5, 0.5],
      "alpha_quality_score": 0.94,
      "edge_quality_score": 0.90,
      "casts_shadow": true,
      "shadow_layer_id": "shadow_paper_arrow_01",
      "motion_affordances": ["bounce", "wiggle", "point_pulse"]
    }
  ]
}
```

## V.7 AnimationPlan

```json
{
  "animation_plan_id": "anim_001",
  "duration_frames": 360,
  "fps": 30,
  "motion_style": "tactile_stop_motion",
  "global_motion": {
    "camera": "subtle_push_in",
    "paper_jitter": {
      "position_px": 1.5,
      "rotation_deg": 0.7,
      "frequency_frames": 4
    }
  },
  "layer_animations": [
    {
      "target_layer_id": "paper_arrow_01",
      "motion_primitive_id": "arrow_bounce_01",
      "start_frame": 30,
      "end_frame": 90,
      "params": {
        "amplitude_px": 14,
        "cycles": 2
      }
    },
    {
      "target_layer_id": "character_mouth",
      "motion_primitive_id": "mouth_flap_simple_01",
      "start_frame": 0,
      "end_frame": 300,
      "params": {
        "audio_sync_source": "coach_audio_or_tts_proxy"
      }
    }
  ]
}
```

## V.8 RendererRoute

```json
{
  "renderer_route_id": "route_001",
  "recommended_renderer": "remotion",
  "secondary_renderer": "motion_canvas",
  "route_reason": "paper-cut explainer with layered assets and subtitles",
  "forbidden_renderers": ["scail_2"],
  "requires_final_packaging": true,
  "packaging_renderer": "remotion",
  "confidence": 0.92
}
```

## V.9 ExecutionReceipt

```json
{
  "receipt_id": "cmf_receipt_001",
  "creative_state_id": "cs_2026_000001",
  "session_id": "ces_2026_000001",
  "identity_pack_id": "emmanuel_brand_actor_v1",
  "container_version": "cmf-image-worker:2026.06.16",
  "scene_spec_hash": "sha256:...",
  "composition_prompt_hash": "sha256:...",
  "selected_references": [
    "act_confident_open_explain_01",
    "face_confident_half_smile_03"
  ],
  "edit_workflow_hash": "sha256:...",
  "renderer": "remotion",
  "renderer_version": "x.x.x",
  "seed": 123456,
  "asset_hashes": [],
  "evaluation_scores": {
    "identity_consistency": 0.91,
    "emotion_match": 0.88,
    "gesture_match": 0.84,
    "composition_clarity": 0.90,
    "style_consistency": 0.95,
    "negative_space_compliance": 0.97
  },
  "status": "approved"
}
```

---

# VI. Complete Editing Session Contract

## VI.1 Role

The Complete Editing Session is the top-level production container.

Every creative output belongs to one session.

The session must contain enough state to reproduce, audit, debug, and improve the output.

## VI.2 Session Object

```json
{
  "session_id": "ces_2026_000001",
  "coach_id": "coach_emmanuel",
  "identity_pack_id": "emmanuel_brand_actor_v1",
  "container_version": "cmf-worker:2026.06.16",
  "trigger_context": {},
  "voice_dna_context": {},
  "negative_space_constraints": {},
  "content_intent": {},
  "creative_state": {},
  "assets_prefetched": [],
  "render_outputs": [],
  "evaluation_receipts": [],
  "approval_status": "pending"
}
```

## VI.3 Session Rule

If a creative workflow cannot run inside a Complete Editing Session, it should not be considered production-ready.

---

# VII. Ideogram 4 Composition Stage

## VII.1 Role

Ideogram 4 is the primary composition-control model.

Its purpose is to transform a structured scene specification into a precise visual composition.

It answers:

- where should objects go?
- where should the subject stand?
- where does the text live?
- what is the visual metaphor?
- what is the color and spatial rhythm?
- what is the first-frame visual hook?

## VII.2 Non-Role

Ideogram 4 is not responsible for final identity consistency.

It should not be asked to perfectly reproduce the coach.

It should create a composition plate that is close enough for Flux 2 / Flux Kontext to perform character replacement and refinement.

## VII.3 Ideogram Input Contract

Ideogram receives:

```json
{
  "scene_spec": {},
  "composition_constraints": {},
  "style_constitution": {},
  "visual_negative_space": {},
  "text_area_requirements": {},
  "subject_placement": {},
  "metaphor_objects": []
}
```

## VII.4 Ideogram Output Contract

Ideogram should return:

```json
{
  "composition_image_uri": "s3://.../ideogram_composition.png",
  "composition_analysis": {
    "subject_position": "lower_left_third",
    "text_space": "upper_right",
    "dominant_visual_flow": "bottom_left_to_top_right",
    "object_count": 12,
    "layerability_score": 0.82,
    "style_match_score": 0.90,
    "identity_specificity": "generic_placeholder"
  }
}
```

## VII.5 Prompt Compiler Example

Input SceneSpec:

```json
{
  "visual_style": "paper_cutout_stop_motion",
  "subject": {
    "position": "lower_left_third",
    "emotion": "confident",
    "gesture": "open_hands_explaining"
  },
  "composition": {
    "main_metaphor": "climbing a colorful paper mountain",
    "text_area": "upper_right",
    "visual_flow": "bottom_left_to_top_right"
  }
}
```

Compiled prompt:

```text
Vertical 9:16 paper cut-out stop-motion composition on textured cream paper background. Handmade colorful felt and paper shapes. A small simple black paper-cut personal-brand character stands in the lower-left third, confidently explaining with open hands. Leave clean empty space for headline text in the upper-right. Include colorful paper mountains, playful rising arrows, small plants, stars, dots, and abstract squiggles. Tactile, imperfect, handmade, cheerful, colorful, soft paper shadows, visible paper grain, editorial composition, clear visual flow from bottom-left to top-right.
```

## VII.6 Ideogram Acceptance Criteria

A composition plate passes if:

- subject position matches target region,
- text area is usable,
- visual flow is clear,
- paper-cut style is present,
- metaphor objects are recognizable,
- layerability score is acceptable,
- character is generic enough to replace cleanly,
- no forbidden style appears.

A composition plate fails if:

- text area is missing,
- character is fused with background objects,
- composition is too crowded,
- layout contradicts the SceneSpec,
- style drifts into glossy 3D or generic vector art,
- subject location is unusable.

---

# VIII. Flux 2 / Flux Kontext Editing Stage

## VIII.1 Role

Flux 2 / Flux Kontext is the controlled editing and refinement engine.

It receives:

- Ideogram composition plate,
- selected approved acting reference,
- optional secondary face/identity anchor,
- identity pack,
- edit job contract.

It outputs:

- refined production image,
- character-replaced scene,
- optional asset-ready composition,
- optional layer extraction source.

## VIII.2 Why This Comes After Ideogram

Ideogram decides composition.

Flux performs adaptation.

The goal is not to make Flux invent the whole scene.

The goal is:

```text
preserve Ideogram composition
+ replace generic subject with approved brand actor
+ preserve emotional gesture
+ harmonize paper-cut style
```

## VIII.3 Recommended Reference Strategy

Use at least two references when possible.

```text
Primary reference = body language / gesture match
Secondary reference = face / identity / expression anchor
```

Optional third reference:

```text
Tertiary reference = hand gesture or facial expression close-up
```

## VIII.4 Flux Edit Acceptance Criteria

Pass conditions:

- branded character is recognizable,
- selected emotion is preserved,
- selected gesture is preserved,
- composition remains close to Ideogram plate,
- text area is preserved,
- paper-cut style remains consistent,
- no unapproved identity features appear,
- hands and face are acceptable for the output size.

Hard failures:

- wrong identity,
- face distortion,
- broken hands in hero frame,
- changed scene layout,
- removed text area,
- style drift,
- emotion contradicts content intent.

---

# IX. Identity Pack and Acting Library

## IX.1 Identity Pack Definition

The identity pack is the compiled brand actor.

It includes:

- fixed identity conditioning models,
- approved reference album,
- container version,
- model digests,
- workflow graph hash,
- permitted runtime actions,
- forbidden runtime actions.

## IX.2 Why LoRA Is Not Required in Phase 1

Phase 1 can validate the creative pipeline without training a LoRA.

The starting strategy is:

```text
Ideogram composition
-> select closest approved acting reference
-> Flux edit / character replacement
-> evaluate identity + emotion + gesture
```

Train a LoRA only after observed failure cases prove it is necessary.

## IX.3 Acting Library Size

Recommended Phase 1 size:

```text
48 minimum
64 preferred
96-128 later only if failure cases demand it
```

64 is not too small if it is designed as an acting matrix rather than random poses.

## IX.4 64-State Acting Matrix

### Emotional families

1. confident,
2. warm,
3. reflective,
4. serious,
5. challenging,
6. playful,
7. urgent,
8. celebratory.

### Gesture / body-language families

1. open explain,
2. point / direct,
3. invite / offer,
4. grounded authority,
5. think / process,
6. emphasize,
7. shrug / tension,
8. dynamic uplift.

### Full 64-state grid

| Emotion | Open explain | Point/direct | Invite/offer | Grounded authority | Think/process | Emphasize | Shrug/tension | Dynamic uplift |
|---|---|---|---|---|---|---|---|---|
| Confident | confident_open_explain | confident_point_direct | confident_invite_offer | confident_grounded_authority | confident_think_process | confident_emphasize | confident_shrug_tension | confident_dynamic_uplift |
| Warm | warm_open_explain | warm_point_direct | warm_invite_offer | warm_grounded_authority | warm_think_process | warm_emphasize | warm_shrug_tension | warm_dynamic_uplift |
| Reflective | reflective_open_explain | reflective_point_direct | reflective_invite_offer | reflective_grounded_authority | reflective_think_process | reflective_emphasize | reflective_shrug_tension | reflective_dynamic_uplift |
| Serious | serious_open_explain | serious_point_direct | serious_invite_offer | serious_grounded_authority | serious_think_process | serious_emphasize | serious_shrug_tension | serious_dynamic_uplift |
| Challenging | challenging_open_explain | challenging_point_direct | challenging_invite_offer | challenging_grounded_authority | challenging_think_process | challenging_emphasize | challenging_shrug_tension | challenging_dynamic_uplift |
| Playful | playful_open_explain | playful_point_direct | playful_invite_offer | playful_grounded_authority | playful_think_process | playful_emphasize | playful_shrug_tension | playful_dynamic_uplift |
| Urgent | urgent_open_explain | urgent_point_direct | urgent_invite_offer | urgent_grounded_authority | urgent_think_process | urgent_emphasize | urgent_shrug_tension | urgent_dynamic_uplift |
| Celebratory | celebratory_open_explain | celebratory_point_direct | celebratory_invite_offer | celebratory_grounded_authority | celebratory_think_process | celebratory_emphasize | celebratory_shrug_tension | celebratory_dynamic_uplift |

## IX.5 Optional Auxiliary Reference Sets

The 64 acting references are the core.

Add small auxiliary sets when possible:

- 8-16 face-expression anchors,
- 8-16 hand-gesture anchors,
- 8-16 close-up identity anchors,
- 8-16 paper-cut avatar expression layers.

These can improve Flux edits without expanding the core acting matrix.

---

# X. Reference Retrieval Logic

## X.1 Retrieval Inputs

The retriever receives:

- communicative intent,
- primary emotion,
- secondary emotion,
- gesture family,
- body language,
- facial expression,
- framing target,
- layout target,
- do-not-use constraints.

## X.2 Scoring Function

Recommended scoring:

```text
reference_score =
  0.30 * emotion_primary_match
+ 0.25 * communicative_intent_match
+ 0.20 * gesture_family_match
+ 0.15 * body_language_match
+ 0.05 * facial_expression_match
+ 0.05 * framing_layout_match
```

This reflects the priority:

```text
emotion + intent + gesture + body language > technical framing
```

## X.3 Candidate Selection

The retriever should return:

```json
{
  "primary_reference": "act_confident_open_explain_01",
  "secondary_reference": "face_confident_half_smile_03",
  "fallback_reference": "act_warm_open_explain_01",
  "score": 0.87,
  "confidence": "high",
  "reason": "Strong match on confident emotion, open explaining gesture, upright body language, and left-third layout utility."
}
```

## X.4 Fallback Logic

If no reference scores above 0.75:

1. choose nearest emotion match,
2. prioritize gesture second,
3. mark session as `low_reference_confidence`,
4. require stricter edit evaluation,
5. log the missing state for dataset expansion.

If no reference scores above 0.60:

1. use a universal neutral reference,
2. lower automation confidence,
3. route to manual review or generate a new candidate for future approval.

## X.5 Dataset Expansion Rule

Do not expand the library randomly.

Only expand when repeated failure logs show specific missing states.

Example:

```json
{
  "missing_state": "urgent_point_direct_profile_left",
  "failure_count_30d": 18,
  "average_reference_score": 0.52,
  "recommendation": "create_new_approved_reference"
}
```

---

# XI. Paper-Cut / Stop-Motion Visual Style Constitution

## XI.1 Style Definition

The primary scalable CMF aesthetic is:

```text
paper cut-out, stop-motion, tactile, handmade, colorful, imperfect, warm, expressive
```

Core scene material:

```text
textured cream paper background
colorful felt or paper shapes
visible paper grain
soft physical shadows
imperfect cutout edges
simple expressive characters
paper props and metaphor objects
```

## XI.2 Allowed Visual Elements

Allowed:

- cream paper background,
- colored construction paper,
- felt shapes,
- torn edges,
- small paper shadows,
- playful arrows,
- plants,
- mountains,
- stars,
- dots,
- abstract squiggles,
- simple black cutout character,
- personal-brand photo cutout character,
- paper objects from real life,
- handmade typography,
- simple label cards,
- collage-style diagrams.

## XI.3 Forbidden Visual Elements

Forbidden by default:

- glossy 3D,
- sterile SaaS vector illustration,
- neon cyberpunk gradients,
- hyperrealistic human skin unless intentionally photo-cut,
- generic AI influencer realism,
- plastic-looking textures,
- overly smooth corporate icons,
- perfect symmetry,
- crowded stock-template layouts,
- flat Canva-style clip art without tactile texture.

## XI.4 Material Rules

- Every object should look physically cut or placed.
- Shadows should be soft and offset, not cinematic hard shadows.
- Edges should be slightly imperfect.
- Textures should be visible but not distracting.
- Color palette should be warm, playful, and legible.
- The background should be tactile, not pure white digital canvas.

## XI.5 Motion Rules

Allowed motion:

- paper wiggle,
- stop-motion jitter,
- small bounce,
- slide-in,
- parallax drift,
- expression swap,
- blink,
- mouth flap,
- star pop,
- arrow pulse,
- hand emphasis,
- gentle camera push.

Forbidden motion:

- overly smooth corporate easing,
- excessive 3D camera moves,
- uncanny realistic body motion,
- motion that breaks paper materiality,
- chaotic meme editing unless routed to Format 04.

## XI.6 Density Rules

A 9:16 scene should usually contain:

- one primary subject,
- one main metaphor object,
- three to seven supporting paper objects,
- one clear text area,
- one dominant visual flow.

If more than ten objects appear, the composition must pass a clutter check.

---

# XII. GPT Image 2 / Image Asset Factory

## XII.1 Role

GPT Image 2 or an equivalent high-instruction image model is used as an asset factory.

It should generate reusable components, not only final images.

## XII.2 Asset Types

The asset factory should create:

- character sheets,
- expression sheets,
- mouth-shape sheets,
- hand-gesture sheets,
- paper-cut avatar variants,
- object packs,
- props,
- backgrounds,
- metaphor packs,
- paper social icons,
- thematic layouts.

## XII.3 Character Asset Outputs

For a personal-brand paper-cut character:

```text
front neutral
front smile
front serious
front skeptical
front surprised
front celebratory
3/4 left
3/4 right
mouth shapes
eyes / blink states
eyebrow states
left arm / right arm variants
hand gesture variants
```

## XII.4 Object Pack Outputs

Example object packs:

```text
paper_mountains_pack_v1
paper_arrows_pack_v1
paper_plants_pack_v1
paper_stars_pack_v1
paper_dots_squiggles_pack_v1
paper_business_icons_pack_v1
paper_ai_metaphor_pack_v1
paper_sports_quiz_pack_v1
paper_data_story_pack_v1
```

## XII.5 Asset Factory Acceptance Criteria

An asset pack passes if:

- objects are visually consistent,
- objects have clear edges,
- objects are suitable for alpha extraction,
- style matches the constitution,
- objects can be reused across scenes,
- metadata can be attached cleanly.

---

# XIII. Layer Extraction Pipeline

## XIII.1 Purpose

The paper-cut style is valuable because it can become layers.

The goal is to turn a composition into an editable asset pack.

## XIII.2 Layer Sources

Layers can come from:

1. direct generated asset packs,
2. Ideogram/Flux composition segmentation,
3. See-Through-style decomposition,
4. segmentation models,
5. manual correction for hero assets,
6. GPT Image 2 / Flux repair passes.

## XIII.3 Required Layer Types

A standard paper-cut scene should attempt to produce:

```text
background_paper.png
mountain_01.png
mountain_02.png
arrow_01.png
plant_01.png
star_01.png
dots_group_01.png
squiggle_01.png
character_body.png
character_head.png
character_eyes.png
character_eyebrows.png
character_mouth.png
character_left_arm.png
character_right_arm.png
character_shadow.png
text_layer.svg
shadow_layers/*.png
```

## XIII.4 Layer Quality Metrics

Each layer receives:

- alpha quality score,
- edge quality score,
- semantic confidence,
- z-index validity,
- anchor-point validity,
- shadow consistency score,
- motion affordance score.

## XIII.5 Layer Failure Modes

Common failures:

- bad alpha,
- fused object,
- missing shadow,
- wrong z-index,
- broken cutout edge,
- background contamination,
- text baked into background,
- character merged with prop,
- object too small to animate,
- unusable anchor point.

## XIII.6 Layer Acceptance Gate

A layer manifest passes if:

```json
{
  "minimum_alpha_quality": 0.86,
  "minimum_edge_quality": 0.82,
  "minimum_semantic_confidence": 0.80,
  "required_layers_present": true,
  "text_not_baked_into_background": true,
  "character_separable": true
}
```

---

# XIV. 2D Character Rigging and Animation

## XIV.1 Role

For paper-cut personal-brand content, a deterministic 2D actor is often better than a video model.

The actor can be:

- stable,
- expressive,
- cheap to render,
- easy to edit,
- reusable across formats.

## XIV.2 Character Layer Structure

```text
root
  body
  head
  eyes
  eyebrows
  mouth
  left_arm
  right_arm
  left_hand
  right_hand
  legs
  shadow
```

## XIV.3 Facial Expression States

```text
neutral
warm_smile
confident_half_smile
serious_focus
skeptical_brow
surprised
concerned
celebratory
```

## XIV.4 Mouth Shapes

```text
closed
m
open_small
open_wide
ee
oo
smile_open
frown
```

## XIV.5 Animation Methods

Potential tools:

- Stretchy Studio for rigging and mesh deformation,
- See-Through-style decomposition for layer generation,
- Remotion for final timeline and packaging,
- Motion Canvas for procedural explainers,
- custom JSON animation interpreter,
- Rive-like state-machine logic if later needed.

## XIV.6 Animation Primitive Example

```json
{
  "motion_id": "paper_character_explain_01",
  "style": "stop_motion",
  "duration_frames": 72,
  "targets": ["body", "left_arm", "right_arm", "head"],
  "curves": {
    "body_y": [0, -6, 0, -3, 0],
    "head_rotation": [0, -1, 1, 0],
    "left_arm_rotation": [0, -8, 3, 0],
    "right_arm_rotation": [0, 7, -2, 0]
  },
  "jitter": {
    "position_px": 1.2,
    "rotation_deg": 0.6
  }
}
```

---

# XV. Motion Library

## XV.1 Purpose

The motion library stores reusable motion behaviors.

It is separate from the acting-reference library.

```text
Acting library = what the character means emotionally
Motion library = how layers move over time
```

## XV.2 Motion Categories

### Character motions

- blink,
- mouth flap,
- hand emphasis,
- open-hand explain,
- small nod,
- skeptical head tilt,
- celebratory bounce,
- thinking pause.

### Object motions

- arrow bounce,
- star pop,
- mountain parallax,
- plant sway,
- dot sparkle,
- squiggle wiggle,
- paper card slide.

### Camera motions

- subtle push-in,
- gentle drift,
- parallax reveal,
- locked-off stop-motion frame.

### Transitions

- paper wipe,
- object slide cover,
- torn-paper reveal,
- sticky-note pop,
- flip-card reveal.

## XV.3 Motion Metadata

Each motion primitive should include:

- duration,
- compatible layer types,
- compatible emotion states,
- intensity,
- loopability,
- renderer compatibility,
- parameter schema.

---

# XVI. SCAIL-2 Motion Transfer Branch

## XVI.1 Role

SCAIL-2 is a motion-transfer branch.

It is best used for:

- memes,
- dances,
- recurring reactions,
- signature gestures,
- preselected viral motion clips,
- simple character replacement in known motion formats.

## XVI.2 Non-Role

SCAIL-2 should not be the default for:

- complex cinematic storytelling,
- multi-shot narratives,
- subtle personal-brand coaching delivery,
- advanced camera movement,
- precise paper-cut layer animation.

## XVI.3 SCAIL-2 Pipeline

```text
Motion library video
+ selected character reference
+ style constraints
-> SCAIL-2 output
-> optional Flux cleanup
-> Remotion packaging
```

## XVI.4 Motion Asset Library

The motion asset library should store:

```json
{
  "motion_video_id": "dance_meme_042",
  "source_uri": "s3://.../dance_meme_042.mp4",
  "motion_type": "dance",
  "energy": "high",
  "body_region": "full_body",
  "duration_seconds": 7,
  "loopable": true,
  "safe_for_brand": true,
  "best_use_cases": ["celebration", "viral_reaction", "playful_announcement"],
  "do_not_use_for": ["grief", "serious_warning", "trauma_context"]
}
```

---

# XVII. Cinematic Video Generation Branch

## XVII.1 Role

Use cinematic video generation models when the output requires visual richness that is not practical through deterministic 2D animation.

Best for:

- cinematic metaphors,
- atmospheric memory scenes,
- symbolic transitions,
- realistic or semi-real camera motion,
- brand films,
- high-emotion visual sequences.

## XVII.2 Pipeline

```text
SceneSpec
-> Ideogram composition or Flux keyframe
-> motion prompt
-> video generation model
-> quality evaluation
-> Remotion final packaging
```

## XVII.3 Tradeoff

This branch is less deterministic and less editable.

Use it only when:

```text
cinematic richness > editability
```

The paper-cut / 2D branch should remain the default for scalable repeated content.

---

# XVIII. Renderer Router

## XVIII.1 Purpose

The renderer router prevents tool confusion.

The agent should not choose a renderer based on preference.

It should choose based on task requirements.

## XVIII.2 Renderer Matrix

| Content type | Primary renderer | Secondary renderer | Reason |
|---|---|---|---|
| Paper-cut explainer | Remotion + Stretchy assets | Motion Canvas | Layered character, subtitles, branded layout |
| Animated avatar explainer | Stretchy Studio + Remotion | Motion Canvas | Rigged 2D actor with deterministic timeline |
| Authentic coach commentary | Remotion | None | SAM cutout, subtitles, annotations, packaging |
| Goal.com-style quiz | Remotion | HyperFrames | Component logic: question, timer, reveal, score |
| All-time ranking video | Remotion | Manim / Motion Canvas | Component ranking plus optional data moments |
| Bar-chart race | Manim / Motion Canvas | Remotion packaging | Procedural data storytelling |
| Data explainer | Manim / Motion Canvas | Remotion packaging | Visual metaphors, graphs, timelines |
| Meme / dance / reaction | SCAIL-2 | Remotion packaging | Motion transfer from library |
| Cinematic metaphor | Video generation model | Remotion packaging | Complex camera/motion |
| Rapid HTML motion graphic | HyperFrames | Remotion | Fast agent-authored web-style video |

## XVIII.3 Decision Tree

```text
Does the task require complex cinematic camera movement?
  yes -> video generation branch
  no -> continue

Does it use a reusable meme/dance/reaction motion clip?
  yes -> SCAIL-2 branch
  no -> continue

Does it require data-driven procedural animation?
  yes -> Manim or Motion Canvas, then Remotion packaging
  no -> continue

Does it require quiz/ranking/timer/reveal logic?
  yes -> Remotion
  no -> continue

Does it require a rigged 2D paper-cut character?
  yes -> Stretchy Studio / custom rig + Remotion
  no -> continue

Does it need rapid agent-generated HTML motion?
  yes -> HyperFrames
  no -> Remotion default
```

## XVIII.4 Renderer Router Output

```json
{
  "recommended_renderer": "remotion",
  "secondary_renderer": "motion_canvas",
  "route_confidence": 0.91,
  "reason": "Layered paper-cut explainer with subtitles and character animation.",
  "forbidden_renderers": ["scail_2"],
  "packaging_renderer": "remotion"
}
```

---

# XIX. Remotion Production Compiler

## XIX.1 Role

Remotion is the default deterministic production compiler.

It handles:

- vertical video compilation,
- subtitles,
- text layout,
- motion graphics,
- quiz/ranking templates,
- split screens,
- final packaging,
- audio sync,
- platform-specific exports.

## XIX.2 Why Remotion Is Default

Remotion maps naturally to:

```text
JSON spec -> React components -> deterministic video
```

This is ideal for agentic content production.

## XIX.3 Standard Remotion Components

```text
<SceneFrame />
<PaperBackground />
<PaperCharacter />
<HeadlineText />
<SubtitleTrack />
<AnnotationArrow />
<ProofCard />
<QuizQuestion />
<TimerRing />
<AnswerReveal />
<RankingList />
<CTA />
```

---

# XX. Manim and Motion Canvas Branch

## XX.1 Role

Manim and Motion Canvas are procedural animation engines.

They should be used when the content needs:

- data storytelling,
- mathematical or conceptual visualization,
- ranking motion beyond templates,
- bar-chart races,
- animated diagrams,
- abstract visual metaphors,
- novel procedural movement.

## XX.2 Why Keep Them

Remotion is strong for templates.

Manim and Motion Canvas are strong for procedural visual invention.

The long-term moat is not only producing many videos. It is giving agents the ability to create diverse motion languages.

## XX.3 Bar-Chart Race Pipeline

```text
Dataset
-> data validation
-> narrative beat detection
-> animation spec
-> Manim or Motion Canvas render
-> Remotion packaging
-> evaluation
```

## XX.4 Bar-Chart Race Spec Example

```json
{
  "video_type": "bar_chart_race",
  "topic": "largest AI companies by valuation",
  "time_range": "2015-2026",
  "highlight_events": [
    "Nvidia acceleration",
    "OpenAI valuation jump",
    "legacy tech catch-up"
  ],
  "visual_style": "paper_cutout_data_story",
  "data_encoding": {
    "bar_material": "paper_strip",
    "labels": "paper_tags",
    "highlight_effect": "star_pop_and_arrow_bounce"
  },
  "renderer": "manim",
  "packaging_renderer": "remotion"
}
```

---

# XXI. HyperFrames Branch

## XXI.1 Role

HyperFrames is useful for agent-authored HTML/CSS/JS motion videos.

It is best for:

- rapid prototypes,
- web-style explainers,
- simple motion graphics,
- fast layout generation,
- deterministic HTML-driven video scenes.

## XXI.2 When To Use

Use HyperFrames when:

- speed matters,
- the scene is mostly HTML-like layout,
- the animation is simple,
- a coding agent can generate the entire scene quickly.

Do not use it as the primary character-animation engine.

---

# XXII. Goal.com-Style Quiz and Ranking Videos

## XXII.1 Role

Goal.com-style quiz/ranking videos are component systems.

They usually need:

- question cards,
- option grids,
- countdowns,
- player/team cards,
- answer reveals,
- score beats,
- comments bait,
- CTA.

## XXII.2 Recommended Stack

```text
Data source / database
-> fact validation
-> quiz generation agent
-> video spec JSON
-> Remotion template
-> final render
```

## XXII.3 Quiz Spec

```json
{
  "video_type": "football_quiz",
  "style": "paper_cutout_sports_cards",
  "questions": [
    {
      "question": "Who scored more Champions League goals?",
      "options": ["Player A", "Player B"],
      "answer": "Player A",
      "timer_seconds": 5,
      "reveal_animation": "paper_card_flip"
    }
  ],
  "cta": "Comment your score"
}
```

## XXII.4 Diversification Rule

Even quiz/ranking videos should not all look the same.

Use renderer-level variation:

- Remotion for standard episodes,
- Manim/Motion Canvas for special data episodes,
- paper-cut animation for branded episodes,
- SCAIL-2 for meme/reaction interludes.

---

# XXIII. Creative Asset Libraries

## XXIII.1 Asset Library Types

The CMF requires these libraries:

1. identity packs,
2. acting references,
3. face-expression anchors,
4. hand-gesture anchors,
5. paper object packs,
6. background texture packs,
7. motion primitives,
8. SCAIL-2 motion videos,
9. composition plates,
10. approved render templates,
11. rejected/failure examples.

## XXIII.2 Object Storage Convention

Recommended structure:

```text
s3://ccp-assets/
  identity_packs/
    emmanuel/
      v1/
        identity_pack.json
        acting_refs/
        face_refs/
        hand_refs/
        expression_refs/
  paper_assets/
    v1/
      arrows/
      mountains/
      plants/
      stars/
      dots/
      squiggles/
      business_icons/
      sports_icons/
  backgrounds/
    paper_textures/
    felt_textures/
    cardboard_textures/
  motion_primitives/
    character/
    object/
    camera/
    transitions/
  motion_videos/
    scail2/
      memes/
      dances/
      reactions/
  compositions/
    ideogram/
      approved/
      rejected/
  renders/
    complete_editing_sessions/
```

## XXIII.3 Asset Metadata

Every asset should have:

```json
{
  "asset_id": "paper_arrow_001",
  "asset_type": "paper_object",
  "semantic_type": "arrow",
  "storage_uri": "s3://...",
  "asset_hash": "sha256:...",
  "source": "generated_or_manual_or_stock",
  "generator": "gpt_image_2_or_flux_or_manual",
  "prompt_hash": "sha256:...",
  "license_status": "owned_or_safe",
  "approval_status": "approved",
  "style_version": "paper_cutout_v1",
  "tags": ["arrow", "upward", "growth", "yellow"],
  "created_at": "2026-06-16T00:00:00Z",
  "deprecated_at": null
}
```

## XXIII.4 Asset Lifecycle

```text
candidate
-> generated
-> evaluated
-> approved
-> active
-> deprecated
-> archived
```

Rejected assets should not be deleted immediately. They are useful for failure analysis and negative examples.

---

# XXIV. Quality Gates

## XXIV.1 Evaluation Categories

Every output is evaluated on:

1. identity consistency,
2. emotion match,
3. gesture match,
4. body-language match,
5. composition clarity,
6. text-space safety,
7. style consistency,
8. layerability,
9. platform fit,
10. negative-space compliance.

## XXIV.2 Minimum Thresholds

```json
{
  "minimum_scores": {
    "identity_consistency": 0.86,
    "emotion_match": 0.82,
    "gesture_match": 0.80,
    "body_language_match": 0.80,
    "composition_clarity": 0.85,
    "text_space_safety": 0.90,
    "style_consistency": 0.88,
    "layerability": 0.78,
    "platform_fit": 0.84,
    "negative_space_compliance": 0.95
  }
}
```

## XXIV.3 Hard Fail Conditions

Hard fail if:

- wrong identity,
- distorted face,
- broken hands in hero frame,
- emotion contradicts message,
- text area unusable,
- subject fused with background,
- style becomes generic AI art,
- scene violates visual negative space,
- synthetic voice is used as the coach's primary message,
- the output cannot produce a receipt.

## XXIV.4 Decision States

```text
approved
soft_fail_retry
hard_fail_reject
manual_review_required
asset_library_gap_detected
```

## XXIV.5 Evaluation Receipt Example

```json
{
  "evaluation_id": "eval_001",
  "status": "soft_fail_retry",
  "scores": {
    "identity_consistency": 0.91,
    "emotion_match": 0.78,
    "gesture_match": 0.84,
    "composition_clarity": 0.88,
    "style_consistency": 0.92,
    "negative_space_compliance": 0.96
  },
  "failure_reasons": [
    "emotion_match_below_threshold"
  ],
  "recommended_action": "retry_flux_edit_with_secondary_face_expression_anchor"
}
```

---

# XXV. Visual Negative Space

## XXV.1 Purpose

CCP already uses Negative Space for language and identity.

The CMF needs a visual equivalent.

Visual Negative Space defines what the brand must not look like.

## XXV.2 Visual Negative Space Object

```json
{
  "visual_negative_space_id": "vns_emmanuel_v1",
  "forbidden_styles": [
    "generic_ai_influencer",
    "glossy_3d_avatar",
    "corporate_saas_vector",
    "stock_template_canva",
    "neon_cyberpunk",
    "sterile_minimal_whiteboard"
  ],
  "forbidden_moods": [
    "cold",
    "synthetic",
    "over_polished",
    "salesy",
    "hype_bro"
  ],
  "forbidden_motifs": [
    "generic_lightbulb",
    "robot_shaking_hands",
    "abstract_business_people_without_identity"
  ],
  "required_counter_signals": [
    "tactile_materiality",
    "visible_handmade_texture",
    "warm_imperfection",
    "emotionally_legible_character"
  ]
}
```

## XXV.3 Evaluation

An output should be rejected if it visually drifts toward the forbidden centroid even when technically attractive.

---

# XXVI. Pipeline Modes

## XXVI.1 Mode 1: Paper-Cut Explainer

```text
Content intent
-> SceneSpec
-> Ideogram composition
-> acting reference retrieval
-> Flux edit / character replacement
-> layer extraction
-> animation plan
-> Remotion / Motion Canvas render
-> evaluation
```

## XXVI.2 Mode 2: Authentic Coach Commentary

```text
Coach authentic video
-> SAM cutout
-> background / paper object retrieval
-> depth / parallax preparation
-> Remotion composition
-> subtitles / rough annotations
-> final render
```

Rule: the coach's primary message must use authentic recorded audio, not synthetic voice.

## XXVI.3 Mode 3: Animated Paper-Cut Avatar Explainer

```text
Script or approved narration
-> paper-cut actor rig
-> expression + mouth-shape timeline
-> paper object animation
-> Remotion packaging
```

## XXVI.4 Mode 4: Meme / Dance / Reaction

```text
Motion video asset
-> character reference
-> SCAIL-2
-> cleanup
-> Remotion packaging
```

## XXVI.5 Mode 5: Cinematic Metaphor

```text
SceneSpec
-> Ideogram / Flux keyframe
-> video-generation model
-> evaluation
-> Remotion packaging
```

## XXVI.6 Mode 6: Data Story

```text
Dataset
-> validation
-> narrative beat detection
-> Manim / Motion Canvas
-> Remotion packaging
```

## XXVI.7 Mode 7: Quiz / Ranking

```text
Data source
-> fact validation
-> quiz/ranking spec
-> Remotion template
-> render
```

---

# XXVII. Failure Handling

## XXVII.1 Failure Taxonomy

```text
composition_failure
identity_replacement_failure
emotion_mismatch
reference_gap
style_drift
layer_extraction_failure
renderer_failure
data_validation_failure
video_model_uncontrolled_output
receipt_missing
```

## XXVII.2 Retry Logic

### Composition failure

Retry Ideogram with stricter spatial constraints.

### Identity failure

Retry Flux edit with stronger identity anchor or different approved reference.

### Emotion mismatch

Select alternate acting reference from the same emotion family or add secondary expression anchor.

### Layer extraction failure

Use segmentation repair or route to deterministic asset-pack composition instead of extracting from a fused image.

### Renderer failure

Fallback to Remotion default if secondary renderer fails.

### Data validation failure

Do not render. Return to fact-validation stage.

## XXVII.3 Manual Review Triggers

Manual review required if:

- identity score below 0.75,
- emotion score below 0.70,
- visual negative space violation,
- synthetic-looking face,
- legal/licensing ambiguity,
- trauma-sensitive trigger context,
- public-facing high-stakes claim.

---

# XXVIII. Implementation Phases

## Phase 1: Validate Without LoRA

### Goal

Prove the pipeline with approved references and fixed identity conditioning.

### Build

- 48-64 approved acting references,
- acting-reference metadata schema,
- SceneSpec schema,
- Ideogram prompt compiler,
- Flux edit workflow,
- Remotion packaging template,
- evaluation receipt.

### Promotion Criteria

```text
80%+ outputs pass identity threshold
80%+ outputs pass emotion/gesture threshold
average regeneration count below 2.5
reference retrieval correct in 85%+ test cases
receipt generated for 100% of renders
```

### Kill Criteria

```text
identity pass rate below 70%
Flux cannot preserve composition reliably
reference library misses common content states
manual cleanup required for most outputs
```

## Phase 2: Build Reusable Asset Libraries

### Goal

Reduce per-output generation cost and increase consistency.

### Build

- paper object packs,
- paper backgrounds,
- expression anchors,
- hand-gesture anchors,
- composition library,
- rejected/failure library.

### Promotion Criteria

```text
50%+ of scenes reuse existing assets
style consistency above 0.90
average generation cost reduced
```

## Phase 3: Layered Animation

### Goal

Turn paper-cut scenes into reusable animated systems.

### Build

- layer extraction pipeline,
- LayerManifest schema,
- motion primitive library,
- simple character rig,
- expression swap system,
- Remotion animation interpreter.

### Promotion Criteria

```text
70%+ paper-cut scenes produce usable layer manifests
core character rig supports 8 expression states
at least 20 motion primitives active
```

## Phase 4: Renderer Router

### Goal

Diversify output formats without losing governance.

### Build

- renderer router,
- Remotion templates,
- Manim / Motion Canvas data branch,
- HyperFrames prototype branch,
- SCAIL-2 meme branch.

### Promotion Criteria

```text
router selects correct renderer in 90%+ golden test cases
all renderer outputs produce receipts
fallback path exists for each renderer
```

## Phase 5: LoRA Only If Needed

### Goal

Add LoRA only when real failure data proves the need.

### Trigger Conditions

Train LoRA if:

- identity drift persists after reference selection,
- edge-angle performance is weak,
- approved references are too rigid,
- repeated failures show same identity gap,
- scale demands more flexible character generation.

### Non-Trigger Conditions

Do not train LoRA merely because it seems more advanced.

## Phase 6: Full Creative Operating System

### Goal

Autonomous multi-format content production.

Final state:

```text
Trigger
-> SceneSpec
-> renderer route
-> asset retrieval
-> composition
-> edit/refine
-> animate
-> render
-> evaluate
-> publish
```

---

# XXIX. Golden Test Sessions

## XXIX.1 Purpose

Golden sessions are fixed test cases used to regression-test the pipeline.

They should cover the most important creative modes.

## XXIX.2 Required Golden Sessions

1. confident paper-cut LinkedIn explainer,
2. reflective coaching metaphor,
3. serious warning / caution post,
4. playful meme-style announcement,
5. celebratory breakthrough post,
6. authentic coach commentary with SAM cutout,
7. animated avatar explainer,
8. football quiz video,
9. all-time ranking video,
10. bar-chart race data story,
11. SCAIL-2 reaction clip,
12. cinematic metaphor clip.

## XXIX.3 Golden Session Rule

Every code change affecting the CMF must run against golden sessions.

A change fails if it regresses:

- identity,
- style,
- composition,
- renderer success,
- receipts,
- quality thresholds.

---

# XXX. Security, Tenancy, and Governance

## XXX.1 Single-Tenant Principle

Each coach should have isolated:

- identity packs,
- reference albums,
- asset libraries,
- model containers,
- storage namespaces,
- receipts,
- evaluation logs.

## XXX.2 Runtime Mutability Rule

The production runtime cannot mutate identity conditioning.

All identity changes require:

- new identity pack version,
- new container version,
- approval process,
- regression test pass,
- migration receipt.

## XXX.3 Asset Permission Rule

Every external asset must have a license/provenance status.

No asset may enter approved production libraries without provenance metadata.

---

# XXXI. Implementation Directory Proposal

```text
cmf/
  schemas/
    scene_spec.schema.json
    creative_state.schema.json
    identity_pack.schema.json
    acting_reference.schema.json
    composition_job.schema.json
    edit_job.schema.json
    layer_manifest.schema.json
    animation_plan.schema.json
    renderer_route.schema.json
    execution_receipt.schema.json
    evaluation_receipt.schema.json
  agents/
    creative_brief_agent/
    scene_spec_compiler/
    ideogram_prompt_compiler/
    reference_retriever/
    renderer_router/
    evaluation_agent/
  adapters/
    ideogram/
    flux/
    comfyui_runninghub/
    gpt_image_asset_factory/
    scail2/
    remotion/
    manim/
    motion_canvas/
    hyperframes/
    stretchystudio/
  libraries/
    identity_packs/
    paper_assets/
    motion_primitives/
    renderer_templates/
  pipelines/
    paper_cutout_explainer/
    coach_commentary/
    animated_avatar/
    meme_reaction/
    cinematic_metaphor/
    data_story/
    quiz_ranking/
  tests/
    golden_sessions/
    fixtures/
    regression/
```

---

# XXXII. Minimum Viable Build

The minimum viable production system should not try to implement everything.

## XXXII.1 MVP Scope

Build only:

1. SceneSpec schema,
2. 64 acting-reference metadata set,
3. Ideogram prompt compiler,
4. Flux edit workflow,
5. Remotion final compiler,
6. execution receipt,
7. identity / emotion / composition evaluation gates.

## XXXII.2 MVP Output Types

Only two output modes at first:

1. Paper-cut explainer image/video,
2. Authentic coach commentary with paper-cut visual layer.

Everything else comes after proof.

## XXXII.3 MVP Success Metric

The MVP succeeds if the system can repeatedly produce:

```text
recognizable brand character
+ correct emotional gesture
+ strong Ideogram composition
+ consistent paper-cut style
+ deterministic Remotion render
+ complete receipt
```

---

# XXXIII. Strategic Conclusion

The strongest CMF architecture is not a normal AI video generator.

It is a modular creative operating system.

The long-term moat is the combination of:

- structured scene specifications,
- Ideogram 4 composition control,
- fixed identity packs,
- 64-state acting libraries,
- Flux 2 / Flux Kontext controlled editing,
- reusable paper-cut asset libraries,
- layer extraction and 2D rigs,
- motion primitive libraries,
- renderer routing across Remotion, Manim, Motion Canvas, HyperFrames, SCAIL-2, and cinematic video models,
- strict receipts and evaluation gates.

This gives CCP a production system that can create outputs that feel:

```text
authored
consistent
expressive
emotionally precise
tactile
visually distinctive
scalable
```

The CMF should not chase photorealistic AI video as the default.

It should own a distinctive paper-cut / stop-motion / handmade visual language while still routing to cinematic video, data animation, quizzes, rankings, or motion transfer when the content demands it.

The result is a renderer-agnostic creative harness that transforms the coach's identity, triggers, and emotional intelligence into scalable media artifacts without sacrificing authenticity or control.

---

# Appendix A: Required Schema Files

The following schemas should be created as separate files:

```text
creative_state.schema.json
scene_spec.schema.json
identity_pack.schema.json
acting_reference.schema.json
composition_job.schema.json
edit_job.schema.json
layer_manifest.schema.json
animation_plan.schema.json
renderer_route.schema.json
execution_receipt.schema.json
evaluation_receipt.schema.json
visual_negative_space.schema.json
asset_metadata.schema.json
motion_primitive.schema.json
```

---

# Appendix B: Required First Engineering Tickets

1. Create `SceneSpec` Pydantic model.
2. Create `CreativeState` Pydantic model.
3. Create `IdentityPack` Pydantic model.
4. Build 64-state acting-reference CSV/JSON.
5. Build reference retrieval scoring function.
6. Build Ideogram prompt compiler.
7. Build Flux edit-job generator.
8. Build Remotion packaging template.
9. Build evaluation receipt writer.
10. Build golden test session fixtures.
11. Build object-storage asset metadata conventions.
12. Build renderer router decision tree.

---

# Appendix C: One-Line Operating Rule

When in doubt, the CMF should choose the path that maximizes:

```text
identity consistency
+ emotional precision
+ composition control
+ editability
+ receiptability
```

not the path that merely looks most impressive on one generation.
