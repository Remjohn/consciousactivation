import type { ActorRef, ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { CampaignOrder, ChangeRequestProgram, DependencyGraphNode, DirectManipulationDelta, OperatorRevisionRequest, ToolDescriptor } from "./domain.js";
export declare class StudioValidationError extends Error {
    readonly code: string;
    readonly context: Readonly<Record<string, string | number | boolean>>;
    constructor(code: string, message: string, context?: Readonly<Record<string, string | number | boolean>>);
}
export declare function requireNonEmpty(value: string, label: string): void;
export declare function requireSafeInteger(value: number, label: string, minimum?: number): void;
export declare function validateImmutableRef(ref: ImmutableRef, label?: string): void;
export declare function validateArtifactRef(ref: ArtifactRef): void;
export declare function validateActor(actor: ActorRef): void;
export declare function validateCampaignOrder(order: CampaignOrder): void;
export declare function validateToolRegistry(tools: ReadonlyArray<ToolDescriptor>): Map<string, ToolDescriptor>;
export declare function validateOperatorRequest(request: OperatorRevisionRequest): void;
export declare function validateDirectDelta(delta: DirectManipulationDelta): void;
export declare function validateDependencyGraph(nodes: ReadonlyArray<DependencyGraphNode>): void;
export declare function validateChangeProgram(program: ChangeRequestProgram, tools: ReadonlyArray<ToolDescriptor>, allowedNodeIds: ReadonlyArray<string>): void;
