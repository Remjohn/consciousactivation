# CCP Studio V2 — Pydantic Domain Contracts, Commands, Events, and State Machines

**Companion to:** `01_CCP_STUDIO_GREENFIELD_MASTER_SPEC.md`  
**Purpose:** provide an implementation-oriented catalog of the canonical objects and durable state transitions  
**Rule:** these examples define semantics. Implementation must encode them as canonical Pydantic v2 models, then project them into JSON Schema, OpenAPI, generated TypeScript types, optional client-side Zod validators, database mappings, DSPy input/output models, and workflow payloads.

---

# 1. Contract Conventions

## 1.0 Contract Authority

Pydantic is the sole semantic contract authority.

Rules:

1. Every canonical object is a versioned `BaseModel` or a discriminated union of Pydantic models.
2. Immutable historical objects use frozen model configuration and content hashes.
3. Commands, events, provider jobs, workflow inputs, render contracts, receipts, and registry entries must reject unknown or invalid fields according to their compatibility policy.
4. SQLAlchemy models are persistence mappings, not competing domain contracts.
5. DSPy signatures consume and return Pydantic-compatible structures. A DSPy prediction is validated before it enters domain state.
6. JSON Schema and OpenAPI are generated from the Python source models.
7. TypeScript interfaces and optional Zod validators are generated outputs. Hand edits are forbidden.
8. Backward compatibility is tested at the Pydantic/model-migration layer.
9. Pi Coding Agent may propose contract instances but may not invent unregistered command types at runtime.

Recommended package split:

```text
ccp_studio.contracts.domain
ccp_studio.contracts.commands
ccp_studio.contracts.events
ccp_studio.contracts.providers
ccp_studio.contracts.workflows
ccp_studio.contracts.rendering
```

---


## 1.1 Envelope

All commands, events, and provider jobs use a common envelope.

```json
{
  "schema_version": "1.0.0",
  "id": "01J...",
  "organization_id": "01J...",
  "brand_id": "01J...",
  "brand_context_version_id": "01J... or null",
  "correlation_id": "01J...",
  "causation_id": "01J... or null",
  "idempotency_key": "string",
  "actor": {
    "type": "user|agent|workflow|system|provider",
    "id": "..."
  },
  "created_at": "ISO-8601 UTC"
}
```

## 1.2 Common Versioned Fields

```json
{
  "version_id": "01J...",
  "semantic_version": "1.0.0",
  "parent_version_id": null,
  "status": "draft|in_review|approved|locked|deprecated",
  "content_hash": "sha256:...",
  "created_by": "user-or-agent-id",
  "approved_by": null,
  "approved_at": null
}
```

## 1.3 Common Review Fields

```json
{
  "review_status": "not_requested|awaiting_review|approved|needs_fix|rejected",
  "review_notes": [],
  "review_tags": [],
  "last_review_event_id": null
}
```

## 1.4 Source Reference

```json
{
  "source_type": "recording|transcript|research_evidence|uploaded_file|registry|asset",
  "source_id": "...",
  "start_ms": null,
  "end_ms": null,
  "line_range": null,
  "claim_scope": "supports|contradicts|contextualizes",
  "note": null
}
```

---

# 2. Brand Contracts

## 2.1 BrandWorkspace

```json
{
  "brand_id": "brand_...",
  "organization_id": "org_...",
  "name": "Maison Naturopathie",
  "slug": "maison-naturopathie",
  "status": "genesis|active|paused|archived",
  "primary_language": "fr",
  "supported_languages": ["fr", "en"],
  "industry": "holistic_health",
  "default_time_zone": "Europe/Paris",
  "active_brand_context_version_id": null,
  "publishing_profile_version_id": null,
  "created_at": "...",
  "updated_at": "..."
}
```

## 2.2 BrandGenesisSession

```json
{
  "brand_genesis_session_id": "bgs_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "status": "draft",
  "current_stage": "client_intake",
  "input_source_media_ids": [],
  "consent_record_version_id": null,
  "business_intelligence_version_id": null,
  "tribe_soul_version_id": null,
  "character_lexicon_version_id": null,
  "voice_dna_version_id": null,
  "negative_space_version_id": null,
  "visual_constitution_version_id": null,
  "identity_summary_id": null,
  "identity_pack_version_id": null,
  "acting_library_version_id": null,
  "papercut_rig_version_id": null,
  "prop_library_version_id": null,
  "anchor_library_version_id": null,
  "motion_library_version_id": null,
  "sfx_library_version_id": null,
  "composition_preference_version_id": null,
  "publishing_profile_version_id": null,
  "output_brand_context_version_id": null,
  "genesis_clearance_certificate_id": null,
  "errors": [],
  "created_at": "...",
  "updated_at": "..."
}
```

## 2.3 ConsentRecordVersion

```json
{
  "consent_record_version_id": "crv_...",
  "brand_id": "brand_...",
  "subject_person_id": "person_...",
  "permissions": {
    "store_source_photos": true,
    "store_source_video": true,
    "generate_realistic_derivatives": true,
    "generate_stylized_avatar": true,
    "generate_memes": false,
    "use_motion_transfer": false,
    "publish_socially": true,
    "reuse_future_sessions": true,
    "train_custom_model": false,
    "use_external_image_provider": true
  },
  "allowed_providers": [],
  "prohibited_contexts": [],
  "retention_policy_id": "...",
  "signed_at": "...",
  "revoked_at": null,
  "document_asset_id": "..."
}
```

## 2.4 BrandContextVersion

```json
{
  "brand_context_version_id": "bcv_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "semantic_version": "1.0.0",
  "status": "locked",
  "components": {
    "business_intelligence_version_id": "biv_...",
    "tribe_soul_version_id": "tsv_...",
    "character_lexicon_version_id": "clv_...",
    "voice_dna_version_id": "vdv_...",
    "negative_space_version_id": "nsv_...",
    "visual_constitution_version_id": "vcv_...",
    "identity_pack_version_id": "ipv_...",
    "acting_library_version_id": "alv_...",
    "papercut_rig_version_id": "prv_...",
    "prop_library_version_id": "plv_...",
    "anchor_library_version_id": "msav_...",
    "motion_library_version_id": "mlv_...",
    "sfx_library_version_id": "slv_...",
    "composition_preference_version_id": "cpv_...",
    "publishing_profile_version_id": "ppv_...",
    "registry_bundle_version_id": "rbv_..."
  },
  "content_hash": "sha256:...",
  "locked_at": "...",
  "locked_by": "user_..."
}
```

## 2.5 GenesisClearanceCertificate

```json
{
  "certificate_id": "gcc_...",
  "brand_id": "brand_...",
  "brand_context_version_id": "bcv_...",
  "requirements": {
    "consent_valid": true,
    "identity_summary_approved": true,
    "acting_library_complete": true,
    "papercut_rig_approved": true,
    "negative_space_approved": true,
    "visual_constitution_approved": true,
    "registries_valid": true
  },
  "validation_run_ids": [],
  "issued_at": "...",
  "issued_by": "workflow_..."
}
```

---

# 3. Identity and Creative Library Contracts

## 3.1 ActingReference

```json
{
  "acting_reference_id": "act_...",
  "brand_id": "brand_...",
  "acting_library_version_id": "alv_...",
  "asset_id": "asset_...",
  "emotion_primary": "confident",
  "emotion_secondary": "warm",
  "communicative_intent": "explain_important_idea",
  "gesture_family": "open_hands_explaining",
  "body_language": "upright_open",
  "facial_expression": "confident_half_smile",
  "energy_level": "medium_high",
  "framing": "medium_shot",
  "orientation": "front_3_4_right",
  "layout_bias": "left_subject_text_right",
  "hand_visibility": "both",
  "quality_scores": {
    "likeness": 0.93,
    "emotion": 0.88,
    "gesture": 0.9,
    "hands": 0.86,
    "crop": 0.95
  },
  "review_status": "approved",
  "content_hash": "sha256:..."
}
```

## 3.2 ActingLibraryVersion

```json
{
  "acting_library_version_id": "alv_...",
  "brand_id": "brand_...",
  "matrix_definition": {
    "emotions": [],
    "gesture_families": []
  },
  "cell_reference_ids": {},
  "coverage": {
    "required": 64,
    "approved": 64,
    "missing_cells": []
  },
  "status": "locked",
  "content_hash": "sha256:..."
}
```

## 3.3 RigManifest

```json
{
  "rig_manifest_version_id": "prv_...",
  "brand_id": "brand_...",
  "type": "2d_cutout_rig",
  "coordinate_system": {
    "width": 1080,
    "height": 1920,
    "origin": "top_left"
  },
  "layers": [
    {
      "layer_id": "torso",
      "asset_id": "asset_torso",
      "z_index": 10,
      "anchor": [0.5, 0.15],
      "parent_layer_id": null,
      "motion_affordances": ["translate", "rotate_small", "scale_small"]
    }
  ],
  "bones": [
    {
      "bone_id": "neck",
      "parent_layer_id": "torso",
      "child_layer_id": "head",
      "rotation_min_deg": -8,
      "rotation_max_deg": 8
    }
  ],
  "expression_presets": {},
  "gesture_presets": {},
  "mouth_map": {},
  "preview_validation_run_id": "val_...",
  "status": "locked",
  "content_hash": "sha256:..."
}
```

## 3.4 MicroSemioticAnchor

```json
{
  "micro_semiotic_anchor_id": "msa_...",
  "brand_id": "brand_...",
  "library_version_id": "msav_...",
  "name": "budget supermarket-coded socks",
  "category": "ordinary_life_object",
  "cultural_context": "French fitness audience",
  "audience_segment_ids": [],
  "visual_description": "...",
  "preferred_placements": ["feet"],
  "prominence": "subtle_but_visible",
  "recognition_effects": ["relatability", "humor", "comment_trigger"],
  "risk_scores": {
    "trademark": 0.35,
    "stereotype": 0.1,
    "distraction": 0.12
  },
  "approved_asset_ids": [],
  "review_status": "approved"
}
```

## 3.5 MotionRecipe

```json
{
  "motion_recipe_id": "motion.myth_busted.v1",
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "compatible_archetype_ids": ["archetype.myth_debunk.v1"],
  "beats": [
    {
      "beat_id": "hook",
      "relative_duration": 0.12,
      "required_layer_classes": ["headline_strip"],
      "actions": ["headline_strip_slide_in", "background_slow_push"]
    },
    {
      "beat_id": "myth",
      "relative_duration": 0.2,
      "actions": ["note_drop", "underline_draw"]
    },
    {
      "beat_id": "debunk",
      "relative_duration": 0.15,
      "actions": ["stamp_pop", "note_micro_shake", "x_draw"]
    },
    {
      "beat_id": "truth",
      "relative_duration": 0.38,
      "actions": ["line_reveal", "parallax_drift"]
    },
    {
      "beat_id": "cta",
      "relative_duration": 0.15,
      "actions": ["cta_slide_up", "camera_settle"]
    }
  ],
  "constraints": {
    "max_simultaneous_motion": 4,
    "max_bounces_per_10s": 2
  }
}
```

---

# 4. Research and Interview Contracts

## 4.1 ResearchField

```json
{
  "research_field_id": "rf_...",
  "brand_id": "brand_...",
  "objective": "Prepare an interview about identity and belonging.",
  "scope": {
    "guest_id": "guest_...",
    "audience_segment_ids": [],
    "time_horizon": "current_plus_historical"
  },
  "status": "collecting",
  "evidence_ids": [],
  "quality_gate": {},
  "completed_at": null
}
```

## 4.2 ResearchEvidence

```json
{
  "evidence_id": "ev_...",
  "research_field_id": "rf_...",
  "source_type": "official_web",
  "source_locator": "...",
  "title": "...",
  "author": "...",
  "published_at": "...",
  "captured_at": "...",
  "summary": "...",
  "claim": "...",
  "classification": "fact|quote|inference|opinion",
  "confidence": 0.9,
  "temporal_sensitivity": "high",
  "citation_payload": {},
  "content_hash": "sha256:..."
}
```

## 4.3 ContextPremise

```json
{
  "context_premise_id": "cp_...",
  "research_field_id": "rf_...",
  "statement": "...",
  "evidence_ids": [],
  "confidence": 0.78,
  "status": "proposed|approved|rejected|expired",
  "guest_implication": "...",
  "audience_implication": "...",
  "question_implication": "...",
  "risk_if_wrong": "...",
  "expires_at": "...",
  "approved_by": null
}
```

## 4.4 InterviewerResonanceContext

```json
{
  "interviewer_resonance_context_id": "irc_...",
  "interviewer_id": "user_...",
  "guest_id": "guest_...",
  "research_field_id": "rf_...",
  "scenes_that_resonate": [],
  "personal_implication": [],
  "unresolved_curiosities": [],
  "authentic_emotional_bridges": [],
  "questions_that_feel_alive": [],
  "questions_to_avoid": [],
  "self_centering_risks": [],
  "recommended_opening_state": "cinematic",
  "source_thread_id": "thread_..."
}
```

## 4.5 MatrixOfEdgingBrief

```json
{
  "matrix_of_edging_brief_id": "moe_...",
  "research_field_id": "rf_...",
  "broad_primary_signals": [],
  "tension_sites": [
    {
      "boundary": "identity imposed vs identity claimed",
      "magnitude": 0.88,
      "evidence_ids": [],
      "risk": "medium"
    }
  ],
  "candidate_edge_products": [],
  "primitive_candidates": [],
  "safety_constraints": [],
  "status": "approved"
}
```

## 4.6 InterviewAssetContract

Use the full object from the master specification. Required fields:

```text
contract_id
question
target_expression_states
target_archetypes
target_derivatives
edge_product_hypothesis
first_line_anchors
depth_anchor
repair_followups
expected_source_material
clip_start_rule
landing_eval_targets
potential_asset_routes
safety_notes
evidence_ids
```

---

# 5. Expression Contracts

## 5.1 CompleteExpressionSession

Required object fields:

```text
expression_session_id
brand_id
brand_context_version_id
session_context_snapshot_id
guest_id
interviewer_id
session_type
session_goal
recording_configuration
interview_preparation_id
interview_asset_contract_ids
recording_artifact_ids
transcript_revision_id
anchor_hit_ids
expression_moment_ids
asset_package_spec_id
evaluation_receipt_id
status
```

## 5.2 ExpressionMoment

Required fields:

```text
expression_moment_id
expression_session_id
source_artifact_id
transcript_revision_id
start_ms
end_ms
verbatim_text
expression_states
source_contract_id
meaning_summary
edge_product_candidates
route_candidates
sensitivity
allowed_uses
review_status
```

## 5.3 ArchetypeRoute

```json
{
  "archetype_route_id": "route_...",
  "expression_moment_id": "em_...",
  "core_archetype_id": "archetype.conceptual_contrast.v1",
  "asset_derivative_id": "asset_derivative.identity_mirror.v1",
  "meme_mechanism_id": null,
  "reaction_archetype_id": null,
  "cmf_render_mode_id": "cmf.paper_cut_explainer.v1",
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "confidence": 0.86,
  "rationale": "...",
  "registry_bundle_version_id": "rbv_...",
  "review_status": "approved"
}
```

## 5.4 AssetPackageSpec

```json
{
  "asset_package_spec_id": "aps_...",
  "expression_session_id": "xes_...",
  "package_type": "guest_asset_pack",
  "target_counts": {
    "short_video": 4,
    "carousel": 2,
    "meme_visual": 2,
    "poll_visual": 2,
    "reaction_seed": 3
  },
  "items": [
    {
      "package_item_id": "...",
      "expression_moment_id": "em_...",
      "archetype_route_id": "route_...",
      "asset_type": "short_video",
      "priority": "required",
      "status": "planned"
    }
  ],
  "diversity_constraints": {
    "minimum_expression_states": 3,
    "minimum_archetypes": 3,
    "minimum_render_modes": 2
  },
  "review_status": "approved"
}
```

---

# 6. Production Contracts

## 6.1 CompleteEditingSession

Required fields:

```text
complete_editing_session_id
brand_id
brand_context_version_id
registry_bundle_version_id
source_expression_session_id
source_expression_moment_id
asset_package_spec_id
asset_type
core_archetype_id
asset_derivative_id
cmf_render_mode_id
visual_style_id
platform_targets
status
```

## 6.2 SceneSpec

```json
{
  "scene_spec_id": "scene_...",
  "complete_editing_session_id": "ces_...",
  "format": "vertical_video",
  "aspect_ratio": "9:16",
  "duration_seconds": 30,
  "platform_targets": ["instagram_reels"],
  "source_message": {
    "verbatim_or_approved_copy": "...",
    "source_references": []
  },
  "text_hierarchy": {
    "headline": "MYTHS BUSTED",
    "subtitle": "Holistic health edition",
    "body_points": []
  },
  "emotional_intent": "compassionate_authority",
  "subject": {
    "identity_pack_version_id": "ipv_...",
    "acting_intent": "serious_open_explain",
    "position": "lower_right",
    "scale": "medium"
  },
  "composition": {
    "layout_family": "headline_top_notes_left_avatar_lower_right",
    "main_metaphor": "...",
    "visual_flow": "top_to_left_to_avatar",
    "density": "medium",
    "text_safe_area": "left_middle"
  },
  "objects": [],
  "micro_semiotic_anchor_ids": [],
  "visual_style_id": "visual.editorial_2_5d_papercut_reel.v1",
  "motion_intent": {
    "recipe_id": "motion.myth_busted.v1",
    "intensity": "restrained"
  }
}
```

## 6.3 AssetSelection

```json
{
  "asset_selection_id": "sel_...",
  "complete_editing_session_id": "ces_...",
  "selected": [
    {
      "role": "primary_acting_reference",
      "asset_id": "act_...",
      "score": 0.91,
      "reason": "best communicative intent and gesture match"
    },
    {
      "role": "secondary_face_anchor",
      "asset_id": "act_...",
      "score": 0.88,
      "reason": "best identity clarity"
    }
  ],
  "low_confidence": false
}
```

## 6.4 ProviderJob

```json
{
  "provider_job_id": "pj_...",
  "complete_editing_session_id": "ces_...",
  "capability": "image_edit",
  "provider_capability_id": "pc_...",
  "workflow_template_id": "wf_...",
  "input_asset_hashes": [],
  "parameters": {},
  "idempotency_key": "...",
  "status": "queued",
  "cost_budget": {},
  "external_job_id": null,
  "receipt_id": null
}
```

## 6.5 LayerManifest

```json
{
  "layer_manifest_id": "lm_...",
  "source_asset_id": "asset_...",
  "layers": [
    {
      "layer_id": "layer_avatar",
      "semantic_type": "portrait_cutout",
      "asset_id": "asset_...",
      "mask_asset_id": "mask_...",
      "z_index": 30,
      "bbox": [620, 780, 380, 1020],
      "anchor": [0.5, 0.9],
      "parent_layer_id": null,
      "alpha_quality": 0.92,
      "edge_quality": 0.89,
      "semantic_confidence": 0.95,
      "motion_affordances": ["drift", "scale_small", "expression_swap"],
      "review_status": "approved"
    }
  ],
  "required_layers_present": true,
  "text_baked": false,
  "review_status": "approved"
}
```

## 6.6 AnimationPlan

```json
{
  "animation_plan_id": "anim_...",
  "complete_editing_session_id": "ces_...",
  "fps": 30,
  "duration_frames": 900,
  "motion_recipe_id": "motion.myth_busted.v1",
  "events": [
    {
      "event_id": "aev_1",
      "start_frame": 0,
      "duration_frames": 20,
      "target_layer_id": "headline",
      "primitive_id": "paper_slide_in",
      "parameters": {},
      "sync_reference": "audio_phrase_1",
      "sfx_asset_id": "sfx_paper_slide"
    }
  ],
  "global": {
    "camera_motion": "slow_push_in",
    "jitter_px": 0.7,
    "rotation_jitter_deg": 0.3
  }
}
```

## 6.7 EvaluationReceipt

```json
{
  "evaluation_receipt_id": "eval_...",
  "object_type": "render_output",
  "object_id": "render_...",
  "rubric_version_ids": [],
  "scores": {
    "source_truth": 0.98,
    "identity": 0.92,
    "emotion": 0.87,
    "composition": 0.9,
    "style": 0.94,
    "motion_restraint": 0.89,
    "micro_semiotic_anchor": 0.84,
    "negative_space": 0.97,
    "platform_fit": 0.91
  },
  "hard_failures": [],
  "warnings": [],
  "evidence": [],
  "decision": "needs_human_review",
  "evaluator_versions": [],
  "created_at": "..."
}
```

---

# 7. Agent Runtime and Command Contracts

## 7.1 AgentExecutionContext

The Agent Gateway builds this immutable, request-scoped object before Pi or a specialist agent may act.

```json
{
  "execution_context_id": "actx_...",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "brand_context_version_id": "bcv_...",
  "registry_bundle_version_id": "rbv_...",
  "user": {
    "user_id": "user_...",
    "roles": ["owner"],
    "permissions": ["render.review", "publishing.schedule"]
  },
  "surface": "pwa|telegram_bot|telegram_mini_app|system",
  "mode": "brand_genesis|research|interview_preparation|live_interview|post_session_extraction|production_planning|render_review|publishing|system_administration",
  "thread_id": "thread_...",
  "active_object": {
    "type": "render_output",
    "id": "render_...",
    "version": 3
  },
  "retrieved_context_refs": [],
  "available_tool_ids": [],
  "available_dspy_program_ids": [],
  "provider_policy_id": "pp_...",
  "cost_policy_id": "cp_...",
  "consent_policy_id": "consent_policy_...",
  "confirmation_policy_id": "confirm_...",
  "expires_at": "...",
  "context_hash": "sha256:..."
}
```

The context may contain references to sensitive objects, but tools must retrieve the minimum required data at execution time. It is not a dump of the entire brand corpus.

## 7.2 DSPyProgramSpec

```json
{
  "program_id": "dspy.interview_asset_contract_compiler",
  "program_version": "1.2.0",
  "status": "approved",
  "input_model": "InterviewContractCompilerInput@1.0.0",
  "output_model": "InterviewAssetContract@2.0.0",
  "signature_id": "sig_...",
  "module_class": "InterviewAssetContractCompiler",
  "optimizer": {
    "type": "approved_optimizer_or_none",
    "artifact_id": "opt_..."
  },
  "model_policy_id": "model_policy_interview_high_quality",
  "evaluation_dataset_version_id": "evalset_...",
  "minimum_scores": {
    "grounding": 0.95,
    "contract_validity": 1.0,
    "human_acceptance": 0.85
  },
  "fallback_program_id": "dspy.interview_asset_contract_compiler_safe",
  "artifact_hash": "sha256:..."
}
```

Production DSPy programs are versioned assets. Changing a signature, optimizer artifact, demonstration set, evaluation threshold, or output model requires a new program version.

## 7.3 AgentCommand

```json
{
  "command_id": "cmd_...",
  "command_type": "APPROVE_RENDER",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "actor_user_id": "user_...",
  "thread_id": "thread_...",
  "target_type": "render_output",
  "target_id": "render_...",
  "payload": {},
  "confirmation_level": "human_confirm",
  "idempotency_key": "...",
  "status": "proposed",
  "created_at": "..."
}
```

## 7.4 Command Status

```text
proposed
→ awaiting_confirmation
→ confirmed
→ executing
→ succeeded | failed | cancelled | rejected
```

## 7.5 Command Result

```json
{
  "command_result_id": "...",
  "command_id": "cmd_...",
  "status": "succeeded",
  "created_object_ids": [],
  "domain_event_ids": [],
  "message": "Render approved.",
  "error": null
}
```

---

# 8. State Machines

## 8.1 Brand Genesis

```text
draft
→ intake_in_progress
→ consent_pending
→ source_qc
→ intelligence_compilation
→ identity_summary_review
→ acting_library_generation
→ acting_library_review
→ avatar_generation
→ layer_and_rig_build
→ rig_review
→ library_generation
→ final_validation
→ context_lock_pending
→ completed

Failure/alternate:
any_state → blocked
any_review → needs_fix
blocked → resumed | cancelled
```

Lock is impossible unless required components are approved.

## 8.2 Acting Reference

```text
draft
→ generation_requested
→ generated
→ auto_qc_passed | auto_qc_failed
→ awaiting_human_review
→ approved | needs_fix | rejected
needs_fix → generation_requested
approved → locked
locked → deprecated
```

## 8.3 Interview Preparation

```text
draft
→ research_collecting
→ evidence_review
→ premises_proposed
→ interviewer_preinduction
→ edging_compiled
→ state_map_compiled
→ contracts_compiled
→ deck_review
→ approved
→ frozen
```

## 8.4 Complete Expression Session

```text
draft
→ scheduled
→ calibration_pending
→ ready
→ live
→ capture_complete
→ uploading
→ transcribing
→ extracting
→ moment_review
→ package_compilation
→ evaluating
→ completed
```

Alternate:

```text
live → interrupted
uploading → missing_artifact
transcribing → failed
any → cancelled
```

## 8.5 Expression Moment

```text
candidate
→ awaiting_review
→ approved | rejected | needs_boundary_fix | sensitive_hold
needs_boundary_fix → candidate
approved → routed
routed → production_allowed
```

## 8.6 Complete Editing Session

```text
planned
→ ready
→ compiling
→ assets_selected
→ provider_jobs_running
→ layer_preparation
→ animation_planning
→ render_queued
→ rendering
→ rendered
→ auto_evaluating
→ needs_review
→ approved | revision_requested | rejected
revision_requested → compiling
approved → publishing_ready
```

## 8.7 Provider Job

```text
created
→ queued
→ dispatched
→ running
→ succeeded | retryable_failed | terminal_failed | cancelled
retryable_failed → queued
```

## 8.8 Publishing Intent

```text
draft
→ ready_for_review
→ approved
→ confirmation_pending
→ confirmed
→ uploading_media
→ scheduling
→ scheduled
→ published
```

Alternate:

```text
scheduling → failed
scheduled → cancelled
published → metrics_syncing
```

---

# 9. Domain Events and Projection Rules

Each successful command emits domain events.

Events are immutable and processed through the outbox.

Example:

```json
{
  "event_id": "evt_...",
  "event_type": "RenderApproved",
  "aggregate_type": "render_output",
  "aggregate_id": "render_...",
  "aggregate_version": 4,
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "payload": {
    "approval_event_id": "ae_..."
  },
  "occurred_at": "..."
}
```

Projection consumers:

- read models;
- Neo4j;
- search/vector index;
- operator notifications;
- analytics;
- workflow signals;
- audit enrichment.

A projection failure never rewrites or loses the source event.

---

# 10. Idempotency and Concurrency

## 10.1 Idempotency

Required for:

- agent commands;
- provider jobs;
- uploads;
- webhooks;
- render starts;
- publish/schedule;
- workflow signals.

## 10.2 Optimistic Concurrency

Mutable aggregates carry a version.

A command must state expected version or be conflict-safe.

Examples:

- two reviewers approving the same asset;
- Telegram and PWA revision at the same time;
- brand context fork while a session is starting.

## 10.3 Context Freeze

When an interview starts or editing job becomes `ready`, store the exact context IDs/hashes.

Later changes do not leak into the active job.

---

# 11. Receipt Chain

The receipt chain links:

```text
Research Evidence Receipt
→ Interview Preparation Receipt
→ Expression Session Receipt
→ Expression Moment Approval
→ Asset Route Receipt
→ Provider Receipts
→ Render Receipt
→ Evaluation Receipt
→ Approval Event
→ Publishing Receipt
```

A public asset must be traceable through the full chain.

---

# 12. Minimum Schema/Test Deliverables

The coding agent must create:

```text
python/ccp_studio/contracts/**/*.py
generated/json-schema/*.json
generated/openapi/openapi.json
generated/typescript/**/*.ts
generated/zod/**/*.ts                 # optional generated validators
docs/contracts/*.md
tests/contracts/test_*.py
fixtures/contracts/*.json
```

Every contract requires:

- valid fixture;
- invalid fixtures;
- backward-compatibility test;
- migration test where versioned;
- human-readable documentation.

No API, workflow, database mapping, DSPy module, frontend, or renderer may define a conflicting shadow type. Contract generation must be reproducible in CI, and generated TypeScript artifacts must be checked for drift.
