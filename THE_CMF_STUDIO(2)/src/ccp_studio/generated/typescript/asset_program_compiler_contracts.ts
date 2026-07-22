// Generated consumer-facing asset program compiler contracts for TS-CMF-093 through TS-CMF-119.

export type VideoFormatCode = "SV-CSC" | "SV-EDU" | "SV-FRB" | "SV-RRC";
export type StillFormatCode = "CAR-LST" | "CAR-JUX" | "SIMG-QUOTE" | "SIMG-ASSERTION" | "SUPERVISUAL";
export type CompilerDecision = "approved" | "blocked" | "repair_required";
export type ProgramStatus = "draft" | "compiled" | "blocked" | "repair_required" | "approved";

export interface RegistryBundleLoadReceipt {
  schema_version: "cmf.registry_bundle_load_receipt.v1";
  registry_bundle_load_receipt_id: string;
  registry_ref: string;
  absolute_path: string;
  decision: "loaded" | "blocked";
  entry_count: number;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface PrimitiveTriadContract {
  schema_version: "cmf.primitive_triad_contract.v1";
  primitive_id: string;
  canonical_name: string;
  role: "meaning_transform" | "delivery_shape" | "format_material";
  evidence_ref: string;
}

export interface CarouselSlideAtom {
  schema_version: "cmf.carousel_slide_atom.v1";
  slide_atom_code: string;
  display_name: string;
  composition_meaning: string;
  allowed_positions: string[];
  compatible_format_codes: string[];
  primitive_triads: PrimitiveTriadContract[];
  visual_grammar: Record<string, unknown>;
  query_tags: string[];
}

export interface CarouselSlideLibrary {
  schema_version: "cmf.carousel_slide_library.v1";
  carousel_slide_library_id: string;
  registry_id: string;
  recognized_format_codes: string[];
  slide_atoms: CarouselSlideAtom[];
  global_rules: Record<string, unknown>;
  registry_load_receipt_id: string;
  compiled_at: string;
}

export interface CarouselSequencePlan {
  schema_version: "cmf.carousel_sequence_plan.v1";
  carousel_sequence_plan_id: string;
  format_code: "CAR-LST" | "CAR-JUX";
  source_context_refs: string[];
  slide_atom_codes: string[];
  sequence_rationale: string;
  primitive_validation_ids: string[];
  deterministic_inputs_hash: string;
}

export interface CarouselBuilderProgram {
  schema_version: "cmf.carousel_builder_program.v1";
  carousel_builder_program_id: string;
  carousel_sequence_plan_id: string;
  slide_specs: Record<string, unknown>[];
  geometrics_layout_plan_ref: string;
  skia_render_job_refs: string[];
  qwen_layered_required: boolean;
  ideogram_composition_refs: string[];
  deterministic_inputs_hash: string;
}

export interface SingleImageRouteDecision {
  schema_version: "cmf.single_image_route_decision.v1";
  single_image_route_decision_id: string;
  composition_id: string;
  archetype_ref: string;
  format_code: StillFormatCode;
  selected_family: string;
  decision_code: string;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface SingleImageSkiaScene {
  schema_version: "cmf.single_image_skia_scene.v1";
  single_image_skia_scene_id: string;
  single_image_route_decision_id: string;
  canvas: Record<string, number>;
  zones: Record<string, unknown>[];
  layer_stack: Record<string, unknown>[];
  rough_notation_plan: Record<string, unknown>;
  skia_component_refs: string[];
  primitive_validation_ids: string[];
  deterministic_inputs_hash: string;
}

export interface SingleImageEvalReviewReceipt {
  schema_version: "cmf.single_image_eval_review_receipt.v1";
  single_image_eval_review_receipt_id: string;
  single_image_skia_scene_id: string;
  score: number;
  decision: CompilerDecision;
  blocker_codes: string[];
  golden_fixture_refs: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface VideoEditScene {
  schema_version: "cmf.video_edit_scene.v1";
  scene_code: string;
  video_format_code: VideoFormatCode;
  start_seconds: number;
  end_seconds: number;
  composition_template_ref: string;
  transcript_beat_refs: string[];
  layer_stack_refs: string[];
}

export interface OTIOAuditManifest {
  schema_version: "cmf.otio_audit_manifest.v1";
  otio_audit_manifest_id: string;
  timeline_ref: string;
  scene_refs: string[];
  marker_refs: string[];
  deterministic_inputs_hash: string;
  audit_notes: string[];
}

export interface VideoRenderContract {
  schema_version: "cmf.video_render_contract.v1";
  video_render_contract_id: string;
  render_target: "remotion" | "motion_canvas" | "skia" | "manim" | "ffmpeg" | "open_timeline_io";
  render_tier: "proxy" | "final";
  timeline_ref: string;
  expected_output_ref: string;
  deterministic_inputs_hash: string;
}

export interface VideoEditProgram {
  schema_version: "cmf.video_edit_program.v1";
  video_edit_program_id: string;
  interview_asset_contract_ref: string;
  transcript_beat_map_ref: string;
  content_format_targets: VideoFormatCode[];
  scenes: VideoEditScene[];
  otio_audit_manifest: OTIOAuditManifest;
  render_contracts: VideoRenderContract[];
  approval_status: "draft" | "blocked" | "repair_required" | "approved";
  blocker_codes: string[];
}

export interface TwoDCharacterSceneProgram {
  schema_version: "cmf.two_d_character_scene_program.v1";
  two_d_character_scene_program_id: string;
  character_rig_id: string;
  video_format_code: "SV-EDU";
  papercut_materiality_ref: string;
  performance_cues: Record<string, unknown>[];
  rough_notation_refs: string[];
  deterministic_inputs_hash: string;
}

export interface InterviewBriefV2Plan {
  schema_version: "cmf.interview_brief_v2_plan.v1";
  interview_brief_v2_plan_id: string;
  brand_context_ref: string;
  sequence_hypotheses: Record<string, unknown>[];
  expression_acquisition_plan: Record<string, unknown>;
  doctrine_refs: string[];
  decision_code: string;
  blocker_codes: string[];
}

export interface CompositionHandoffPackage {
  schema_version: "cmf.composition_handoff_package.v1";
  composition_handoff_package_id: string;
  target_compiler: "carousel" | "single_image" | "supervisual" | "video_edit" | "two_d_character";
  handoff_refs: string[];
  required_receipt_refs: string[];
  no_fabricated_guest_truth: boolean;
}

export interface ContentSequenceProgram {
  schema_version: "cmf.content_sequence_program.v1";
  content_sequence_program_id: string;
  sequencing_registry_kernel_id: string;
  expression_ingredient_inventory_id: string;
  handoff_packages: CompositionHandoffPackage[];
  sequence_slots: Record<string, unknown>[];
  decision: CompilerDecision;
  blocker_codes: string[];
  deterministic_inputs_hash: string;
}

export interface SequenceEvalReceipt {
  schema_version: "cmf.sequence_eval_receipt.v1";
  sequence_eval_receipt_id: string;
  content_sequence_program_id: string;
  primitive_score: number;
  doctrine_score: number;
  decision: CompilerDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}
