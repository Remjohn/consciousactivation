import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { AutonomyMode, CampaignLifecycleState, CampaignOrder, CampaignState, ExceptionReviewPackage, ReviewDecision } from "./domain.js";
export declare function defaultAutonomyPolicy(mode: AutonomyMode): CampaignOrder["autonomy_policy"];
export declare function createCampaignOrder(input: Omit<CampaignOrder, "order_id">): CampaignOrder;
export declare function launchCampaign(order: CampaignOrder): CampaignState;
export declare function transitionCampaign(state: CampaignState, next: CampaignLifecycleState, updates?: {
    readonly checkpoint_id?: string | null;
    readonly exception_ids?: ReadonlyArray<string>;
    readonly run_refs?: ReadonlyArray<ImmutableRef>;
    readonly artifact_refs?: ReadonlyArray<ArtifactRef>;
    readonly evaluation_refs?: ReadonlyArray<ImmutableRef>;
}): CampaignState;
export declare function shouldInterruptOperator(state: CampaignState, checkpointId: string | null, hasException: boolean): boolean;
export declare function buildExceptionReviewPackage(input: {
    readonly campaign_ref: ImmutableRef;
    readonly exception_code: string;
    readonly responsible_product: string;
    readonly summary: string;
    readonly evidence_refs: ReadonlyArray<ImmutableRef>;
    readonly candidate_refs?: ReadonlyArray<ImmutableRef>;
    readonly allowed_decisions?: ReadonlyArray<ReviewDecision>;
    readonly recommended_next_actions: ReadonlyArray<string>;
}): ExceptionReviewPackage;
