import { canonicalSha256, deterministicId, uniqueSorted } from "./canonical.js";
import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type {
  CampaignOrder,
  CampaignState,
  ControlTowerProjection,
  ExceptionReviewPackage,
  KnowledgeProjection,
  RunNodeProjection,
  RuntimeHealthProjection,
  StudioSurfaceBinding,
  TimelineProjection,
} from "./domain.js";
import { validateArtifactRef, validateCampaignOrder, validateImmutableRef } from "./validators.js";

export interface ControlTowerInput {
  readonly campaign: CampaignState;
  readonly order: CampaignOrder;
  readonly studio_binding: StudioSurfaceBinding;
  readonly source_package_ref: ImmutableRef;
  readonly observed_activative_pack_ref: ImmutableRef | null;
  readonly semantic_production_package_ref: ImmutableRef | null;
  readonly final_script_ref: ImmutableRef | null;
  readonly activation_transfer_contract_ref: ImmutableRef | null;
  readonly run_nodes: ReadonlyArray<RunNodeProjection>;
  readonly artifacts: ReadonlyArray<ArtifactRef>;
  readonly evaluations: ReadonlyArray<ImmutableRef>;
  readonly knowledge: KnowledgeProjection;
  readonly runtime_health: ReadonlyArray<RuntimeHealthProjection>;
  readonly timeline: TimelineProjection | null;
  readonly exception_packages: ReadonlyArray<ExceptionReviewPackage>;
}

function availableActions(input: ControlTowerInput): ReadonlyArray<string> {
  const actions = ["INSPECT_SOURCE", "INSPECT_SEMANTIC_PROGRAM", "EXPORT_AUDIT"];
  if (input.timeline) actions.push("OPEN_TIMELINE", "REQUEST_REVISION", "DIRECT_MANIPULATION");
  if (input.artifacts.length) actions.push("COMPARE_ARTIFACTS", "REQUEST_REVISION");
  if (input.exception_packages.length) actions.push("RESOLVE_EXCEPTION");
  if (input.campaign.lifecycle_state === "READY_TO_SHIP") actions.push("REQUEST_SHIP_DECISION");
  return uniqueSorted(actions);
}

export function buildControlTowerProjection(input: ControlTowerInput): ControlTowerProjection {
  validateCampaignOrder(input.order);
  validateImmutableRef(input.source_package_ref, "source_package_ref");
  for (const ref of [input.observed_activative_pack_ref, input.semantic_production_package_ref, input.final_script_ref, input.activation_transfer_contract_ref]) {
    if (ref) validateImmutableRef(ref);
  }
  for (const artifact of input.artifacts) validateArtifactRef(artifact);
  const nodes = [...input.run_nodes]
    .map((node) => ({ ...node, dependency_ids: uniqueSorted(node.dependency_ids), blocker_codes: uniqueSorted(node.blocker_codes) }))
    .sort((a, b) => a.node_id.localeCompare(b.node_id));
  const payload = {
    campaign: input.campaign,
    order: input.order,
    studio_binding: input.studio_binding,
    source_package_ref: input.source_package_ref,
    observed_activative_pack_ref: input.observed_activative_pack_ref,
    semantic_production_package_ref: input.semantic_production_package_ref,
    final_script_ref: input.final_script_ref,
    activation_transfer_contract_ref: input.activation_transfer_contract_ref,
    run_nodes: nodes,
    artifacts: [...input.artifacts].sort((a, b) => a.artifact_id.localeCompare(b.artifact_id)),
    evaluations: [...input.evaluations].sort((a, b) => a.object_id.localeCompare(b.object_id)),
    knowledge: {
      skill_refs: [...input.knowledge.skill_refs].sort((a, b) => a.object_id.localeCompare(b.object_id)),
      steering_recipe_refs: [...input.knowledge.steering_recipe_refs].sort((a, b) => a.object_id.localeCompare(b.object_id)),
      retrieval_receipt_refs: [...input.knowledge.retrieval_receipt_refs].sort((a, b) => a.object_id.localeCompare(b.object_id)),
      programmed_model_claim_refs: [...input.knowledge.programmed_model_claim_refs].sort((a, b) => a.object_id.localeCompare(b.object_id)),
      exclusion_codes: uniqueSorted(input.knowledge.exclusion_codes),
    },
    runtime_health: [...input.runtime_health].sort((a, b) => a.component_id.localeCompare(b.component_id)),
    timeline: input.timeline,
    exception_packages: [...input.exception_packages].sort((a, b) => a.package_id.localeCompare(b.package_id)),
    available_actions: availableActions(input),
  } as const;
  return {
    projection_id: deterministicId("control-tower-projection", payload),
    ...payload,
    projection_sha256: canonicalSha256(payload),
  };
}

export function controlTowerSummary(projection: ControlTowerProjection): Readonly<Record<string, string | number>> {
  return {
    campaign_id: projection.campaign.campaign_id,
    campaign_state: projection.campaign.lifecycle_state,
    autonomy_mode: projection.campaign.autonomy_mode,
    primary_surface: projection.studio_binding.primary_surface,
    run_nodes: projection.run_nodes.length,
    completed_nodes: projection.run_nodes.filter((node) => node.status === "SUCCEEDED").length,
    failed_nodes: projection.run_nodes.filter((node) => node.status === "FAILED").length,
    artifacts: projection.artifacts.length,
    exceptions: projection.exception_packages.length,
    unhealthy_components: projection.runtime_health.filter((component) => component.status !== "HEALTHY").length,
  };
}
