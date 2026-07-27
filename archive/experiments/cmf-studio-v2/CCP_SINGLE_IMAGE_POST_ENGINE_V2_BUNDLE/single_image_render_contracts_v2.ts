// GENERATED CONSUMER CONTRACT — semantic source of truth is Python/Pydantic.
export type AspectRatio = '1:1' | '4:5' | '9:16' | '16:9';

export interface Bounds { x:number; y:number; w:number; h:number; }
export interface CompositionZone {
  id:string; role:string; bounds:Bounds; z_index:number;
  required:boolean; content_type:string; alignment:string;
}
export interface TextElement {
  id:string; zone_id:string; role:string; text:string; font_token:string;
  color_token:string; max_lines:number; alignment:string;
  emphasis_spans:Array<Record<string, unknown>>;
}
export interface VisualAssetPlacement {
  id:string; zone_id:string; asset_id:string; asset_role:string;
  fit:string; focal_point?:{x:number;y:number}; mask_asset_id?:string;
  layer_manifest_id?:string;
}
export interface AnnotationSpec {
  id:string; target_element_id:string; annotation_type:string;
  color_token:string; roughness:number; seed:number;
}
export interface SingleImageSceneSpecV2 {
  scene_spec_id:string; input_context_hash:string;
  brand_context_version_id:string; registry_bundle_version:string;
  composition_id:string; aspect_ratio:AspectRatio;
  canvas_width:number; canvas_height:number; background_token:string;
  text_elements:TextElement[]; visual_assets:VisualAssetPlacement[];
  annotations:AnnotationSpec[];
  micro_semiotic_anchors:Array<Record<string, unknown>>;
  provider_jobs:Array<Record<string, unknown>>;
  evaluation_profile_id:string;
}
