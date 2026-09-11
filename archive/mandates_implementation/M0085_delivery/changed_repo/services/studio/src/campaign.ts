import { canonicalSha256, deterministicId } from "./canonical";
import { StudioValidationError } from "./errors";
import type { CampaignOrder, CampaignState } from "./domain";

export const ALLOWED_TRANSITIONS: Readonly<Record<string, ReadonlyArray<string>>> = {
  DRAFT: ["LAUNCHED", "CANCELLED"],
  LAUNCHED: ["RUNNING", "CANCELLED"],
  RUNNING: ["AWAITING_REVIEW", "BLOCKED_EXCEPTION", "READY_TO_SHIP", "CANCELLED"],
  AWAITING_REVIEW: ["RUNNING", "READY_TO_SHIP", "CANCELLED"],
  BLOCKED_EXCEPTION: ["RUNNING", "AWAITING_REVIEW", "CANCELLED"],
  READY_TO_SHIP: ["SHIPPED", "AWAITING_REVIEW", "CANCELLED"],
  SHIPPED: [], CANCELLED: [],
};

function refValid(label: string, value: any): void {
  if (!value?.object_id || !value?.version || !/^[0-9a-f]{64}$/.test(value?.sha256 ?? "")) throw new StudioValidationError("INVALID_REF", `${label} must be a valid immutable ref`);
}

export function validateCampaignOrder(order: CampaignOrder): void {
  const required = ["workspace_id", "project_id", "category_id", "objective", "initial_seed"] as const;
  for (const key of required) if (!String(order[key]).trim()) throw new StudioValidationError("EMPTY_VALUE", `${key} must not be empty`);
  refValid("source_ref", order.source_ref); refValid("harness_ref", order.harness_ref);
  if (!Number.isInteger(order.budget_units) || order.budget_units < 1) throw new StudioValidationError("INVALID_INTEGER", "budget_units must be an integer >= 1");
  if (!order.output_targets.length) throw new StudioValidationError("OUTPUT_TARGET_REQUIRED", "at least one output target is required");
  if (order.category_id === "2d_character_animation" || String(order.format_profile_id).startsWith("format02_")) throw new StudioValidationError("FORMAT02_DEFERRED", "Format 02 is deferred pending a current validated Atomic Harness");
  if (order.operator_actor.actor_type !== "human" || order.operator_actor.workflow_role !== "operator") throw new StudioValidationError("OPERATOR_REQUIRED", "operator actor must be human/operator");
}

export function createCampaignOrder(core: Omit<CampaignOrder, "order_id">): CampaignOrder {
  const order = { ...core, order_id: deterministicId("campaign-order", core) } as CampaignOrder;
  validateCampaignOrder(order); return order;
}

export function launchCampaign(order: CampaignOrder): CampaignState {
  validateCampaignOrder(order);
  const orderRef = { object_id: order.order_id, version: "1.0.0", sha256: canonicalSha256(order) };
  return { campaign_id: deterministicId("campaign", { order_ref: orderRef }), order_ref: orderRef, lifecycle_state: "LAUNCHED", autonomy_mode: order.autonomy_policy.mode, active_checkpoint_id: null, exception_ids: [], run_refs: [], artifact_refs: [], evaluation_refs: [], version: 1 };
}

export function transitionCampaign(state: CampaignState, next: CampaignState["lifecycle_state"]): CampaignState {
  if (!ALLOWED_TRANSITIONS[state.lifecycle_state]?.includes(next)) throw new StudioValidationError("CAMPAIGN_TRANSITION_DENIED", `${state.lifecycle_state} cannot transition to ${next}`);
  if (next === "SHIPPED" && state.autonomy_mode === "SHADOW") throw new StudioValidationError("SHADOW_CANNOT_SHIP", "SHADOW campaigns cannot transition to SHIPPED");
  return { ...state, lifecycle_state: next, version: state.version + 1 };
}
