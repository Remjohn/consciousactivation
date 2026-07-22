export type DeterministicRenderer = "remotion" | "motion_canvas";

export interface RendererPropsBundleV1 {
  schema_version: "cmf.renderer_props_bundle.v1";
  renderer_props_bundle_id: string;
  render_contract_id: string;
  assembly_plan_id: string;
  renderer: DeterministicRenderer;
  layer_manifest_id: string;
  animation_plan_id: string;
  timeline_manifest_id: string;
  caption_manifest_id?: string | null;
  audio_mix_manifest_id?: string | null;
  final_text_plan_id: string;
  brand_context_version_id: string;
  rig_manifest_id: string;
  selected_brand_layer_ids: string[];
  motion_recipe_ids: string[];
  sfx_asset_ids: string[];
  platform_variant_ids: string[];
  props_payload: Record<string, unknown>;
  props_hash: string;
}
