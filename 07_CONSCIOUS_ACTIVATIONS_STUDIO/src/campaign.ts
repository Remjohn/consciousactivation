import { canonicalSha256, deterministicId, uniqueSorted } from "./canonical.js";
import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { AutonomyMode, CampaignLifecycleState, CampaignOrder, CampaignState, ExceptionReviewPackage, ReviewDecision } from "./domain.js";
import { StudioValidationError, validateCampaignOrder } from "./validators.js";

export function defaultAutonomyPolicy(mode: AutonomyMode): CampaignOrder["autonomy_policy"] {
  return {
    mode,
    checkpoint_ids: mode === "CHECKPOINTED" ? ["final-script-approval", "final-artifact-review"] : [],
    exception_only: mode === "AUTOPILOT" || mode === "REVIEW_BEFORE_SHIP",
    final_review_required: mode !== "AUTOPILOT",
    publication_authority_required: true,
  };
}

export function createCampaignOrder(input: Omit<CampaignOrder, "order_id">): CampaignOrder {
  const order: CampaignOrder = { ...input, order_id: deterministicId("campaign-order", input) };
  validateCampaignOrder(order);
  return order;
}

export function launchCampaign(order: CampaignOrder): CampaignState {
  validateCampaignOrder(order);
  const orderRef: ImmutableRef = { object_id: order.order_id, version: "1.0.0", sha256: canonicalSha256(order) };
  return {
    campaign_id: deterministicId("campaign", { order_ref: orderRef }),
    order_ref: orderRef,
    lifecycle_state: "LAUNCHED",
    autonomy_mode: order.autonomy_policy.mode,
    active_checkpoint_id: null,
    exception_ids: [],
    run_refs: [],
    artifact_refs: [],
    evaluation_refs: [],
    version: 1,
  };
}

const allowedTransitions: Readonly<Record<CampaignLifecycleState, ReadonlyArray<CampaignLifecycleState>>> = Object.freeze({
  DRAFT: ["LAUNCHED", "CANCELLED"],
  LAUNCHED: ["RUNNING", "CANCELLED"],
  RUNNING: ["AWAITING_REVIEW", "BLOCKED_EXCEPTION", "READY_TO_SHIP", "CANCELLED"],
  AWAITING_REVIEW: ["RUNNING", "READY_TO_SHIP", "CANCELLED"],
  BLOCKED_EXCEPTION: ["RUNNING", "AWAITING_REVIEW", "CANCELLED"],
  READY_TO_SHIP: ["SHIPPED", "AWAITING_REVIEW", "CANCELLED"],
  SHIPPED: [],
  CANCELLED: [],
});

export function transitionCampaign(
  state: CampaignState,
  next: CampaignLifecycleState,
  updates: {
    readonly checkpoint_id?: string | null;
    readonly exception_ids?: ReadonlyArray<string>;
    readonly run_refs?: ReadonlyArray<ImmutableRef>;
    readonly artifact_refs?: ReadonlyArray<ArtifactRef>;
    readonly evaluation_refs?: ReadonlyArray<ImmutableRef>;
  } = {},
): CampaignState {
  if (!allowedTransitions[state.lifecycle_state].includes(next)) {
    throw new StudioValidationError("CAMPAIGN_TRANSITION_DENIED", `${state.lifecycle_state} cannot transition to ${next}`);
  }
  if (next === "SHIPPED" && state.autonomy_mode === "SHADOW") {
    throw new StudioValidationError("SHADOW_CANNOT_SHIP", "SHADOW campaigns cannot transition to SHIPPED");
  }
  return {
    ...state,
    lifecycle_state: next,
    active_checkpoint_id: updates.checkpoint_id === undefined ? state.active_checkpoint_id : updates.checkpoint_id,
    exception_ids: uniqueSorted(updates.exception_ids ?? state.exception_ids),
    run_refs: updates.run_refs ?? state.run_refs,
    artifact_refs: updates.artifact_refs ?? state.artifact_refs,
    evaluation_refs: updates.evaluation_refs ?? state.evaluation_refs,
    version: state.version + 1,
  };
}

export function shouldInterruptOperator(state: CampaignState, checkpointId: string | null, hasException: boolean): boolean {
  if (hasException) return true;
  if (state.autonomy_mode === "SHADOW") return false;
  if (state.autonomy_mode === "CHECKPOINTED") return checkpointId !== null;
  if (state.autonomy_mode === "REVIEW_BEFORE_SHIP") return checkpointId === "final-artifact-review";
  return false;
}

export function buildExceptionReviewPackage(input: {
  readonly campaign_ref: ImmutableRef;
  readonly exception_code: string;
  readonly responsible_product: string;
  readonly summary: string;
  readonly evidence_refs: ReadonlyArray<ImmutableRef>;
  readonly candidate_refs?: ReadonlyArray<ImmutableRef>;
  readonly allowed_decisions?: ReadonlyArray<ReviewDecision>;
  readonly recommended_next_actions: ReadonlyArray<string>;
}): ExceptionReviewPackage {
  const payload = {
    campaign_ref: input.campaign_ref,
    exception_code: input.exception_code,
    responsible_product: input.responsible_product,
    summary: input.summary,
    evidence_refs: input.evidence_refs,
    candidate_refs: input.candidate_refs ?? [],
    allowed_decisions: input.allowed_decisions ?? ["REQUEST_REVISION", "REJECT"],
    recommended_next_actions: input.recommended_next_actions,
  };
  return { package_id: deterministicId("exception-review", payload), ...payload };
}
