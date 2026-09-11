import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { CampaignOrder, CampaignState, ControlTowerProjection, ExceptionReviewPackage, KnowledgeProjection, RunNodeProjection, RuntimeHealthProjection, StudioSurfaceBinding, TimelineProjection } from "./domain.js";
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
export declare function buildControlTowerProjection(input: ControlTowerInput): ControlTowerProjection;
export declare function controlTowerSummary(projection: ControlTowerProjection): Readonly<Record<string, string | number>>;
