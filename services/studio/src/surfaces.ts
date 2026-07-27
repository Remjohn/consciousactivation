import { canonicalSha256, deterministicId, uniqueSorted } from "./canonical.js";
import type { ImmutableRef } from "./generated/contracts.js";
import type { OutputTarget, StudioModuleDescriptor, StudioSurfaceBinding, StudioSurfaceId } from "./domain.js";
import { StudioValidationError, validateImmutableRef } from "./validators.js";

export const STUDIO_MODULES: ReadonlyArray<StudioModuleDescriptor> = Object.freeze([
  {
    surface_id: "INTERVIEW_EXPRESSION_STUDIO",
    title: "Interview Expression Studio",
    status: "ACTIVE_DEVELOPMENT",
    capabilities: ["source_package", "expression_moments", "ingredient_inventory", "asset_package_spec"],
    supported_output_types: ["INTERVIEW_SOURCE"],
  },
  {
    surface_id: "STATIC_COMPOSITION_STUDIO",
    title: "Static Composition Studio",
    status: "ACTIVE_DEVELOPMENT",
    capabilities: ["supervisual", "carousel", "composition_ir", "semantic_bbox", "pretext", "static_evaluation"],
    supported_output_types: ["SUPERVISUAL", "CAROUSEL"],
  },
  {
    surface_id: "VIDEO_PRODUCTION_STUDIO",
    title: "Video Production Studio",
    status: "ACTIVE_DEVELOPMENT",
    capabilities: ["video_edit_program", "timeline_projection", "captions", "audio", "motion_slots", "render_evaluation"],
    supported_output_types: ["SOURCE_LED_SHORT", "ANIMATION_SHORT", "ANIMATION_SCENE_PACKAGE"],
  },
  {
    surface_id: "VISUAL_ASSET_STUDIO",
    title: "Visual Asset Studio",
    status: "ACTIVE_DEVELOPMENT",
    capabilities: ["visual_asset_demands", "candidate_review", "asset_repair", "vae_boundary"],
    supported_output_types: ["VISUAL_ASSET"],
  },
  {
    surface_id: "KNOWLEDGE_MODEL_STUDIO",
    title: "Knowledge and Programmed Model Studio",
    status: "ACTIVE_DEVELOPMENT",
    capabilities: ["skills", "steering_recipes", "retrieval_receipts", "jit_capsules", "programmed_model_claims"],
    supported_output_types: ["KNOWLEDGE", "PROGRAMMED_MODEL"],
  },
  {
    surface_id: "FUTURE_CHARACTER_PERFORMANCE_STUDIO",
    title: "Future Character Performance Studio",
    status: "DEFERRED_AWAITING_FORMAT02_HARNESS",
    capabilities: [],
    supported_output_types: ["FORMAT02"],
  },
]);

const outputToSurface: Readonly<Record<string, StudioSurfaceId>> = Object.freeze({
  SOURCE_LED_SHORT: "VIDEO_PRODUCTION_STUDIO",
  ANIMATION_SHORT: "VIDEO_PRODUCTION_STUDIO",
  ANIMATION_SCENE_PACKAGE: "VIDEO_PRODUCTION_STUDIO",
  SUPERVISUAL: "STATIC_COMPOSITION_STUDIO",
  CAROUSEL: "STATIC_COMPOSITION_STUDIO",
});

export function moduleById(surfaceId: StudioSurfaceId): StudioModuleDescriptor {
  const module = STUDIO_MODULES.find((item) => item.surface_id === surfaceId);
  if (!module) throw new StudioValidationError("UNKNOWN_STUDIO_SURFACE", `unknown Studio surface ${surfaceId}`);
  return module;
}

export function routeHarnessToSurfaces(args: {
  readonly harness_ref: ImmutableRef;
  readonly category_id: string;
  readonly output_targets: ReadonlyArray<OutputTarget>;
  readonly explicit_primary_surface?: StudioSurfaceId;
  readonly operator_entry_policy?: "EXCEPTION_ONLY" | "REVIEW_ALLOWED";
}): StudioSurfaceBinding {
  validateImmutableRef(args.harness_ref, "harness_ref");
  if (args.category_id === "2d_character_animation" || args.output_targets.some((target) => target.profile_id.startsWith("format02_"))) {
    throw new StudioValidationError("FORMAT02_DEFERRED", "Future Character Performance Studio is deferred pending a current Format 02 Harness");
  }
  const routed = args.output_targets.map((target) => outputToSurface[target.output_type]);
  if (routed.some((value) => value === undefined)) throw new StudioValidationError("UNROUTABLE_OUTPUT", "one or more outputs have no Studio route");
  const primary = args.explicit_primary_surface ?? routed[0]!;
  const module = moduleById(primary);
  if (module.status !== "ACTIVE_DEVELOPMENT") throw new StudioValidationError("STUDIO_SURFACE_DEFERRED", `${primary} is deferred`);
  const supporting = uniqueSorted([
    ...routed.filter((surface) => surface !== primary),
    "KNOWLEDGE_MODEL_STUDIO",
    ...(args.output_targets.some((target) => ["SOURCE_LED_SHORT", "ANIMATION_SHORT", "ANIMATION_SCENE_PACKAGE"].includes(target.output_type)) ? ["VISUAL_ASSET_STUDIO"] : []),
  ]) as ReadonlyArray<StudioSurfaceId>;
  const payload = {
    harness_ref: args.harness_ref,
    category_id: args.category_id,
    primary_surface: primary,
    supporting_surfaces: supporting,
    operator_entry_policy: args.operator_entry_policy ?? "EXCEPTION_ONLY",
  };
  return {
    binding_id: deterministicId("studio-surface-binding", payload),
    ...payload,
    binding_reason: `Primary surface selected from ${args.output_targets.map((target) => target.output_type).join(", ")}; semantic authority remains upstream.`,
  };
}

export function studioModuleRegistryDigest(): string {
  return canonicalSha256(STUDIO_MODULES);
}
