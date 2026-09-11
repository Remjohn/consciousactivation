import type { ChangeRequestProgram, DirectManipulationDelta, OperatorRevisionRequest, SteeringRecipeBinding, ToolDescriptor } from "./domain.js";
export interface RevisionContext {
    readonly tools: ReadonlyArray<ToolDescriptor>;
    readonly steering_recipes: ReadonlyArray<SteeringRecipeBinding>;
    readonly allowed_node_ids: ReadonlyArray<string>;
    readonly target_layers_by_ref: Readonly<Record<string, string>>;
    readonly state_version: number;
    readonly default_validation_plan: ReadonlyArray<string>;
    readonly default_invariants: ReadonlyArray<string>;
    readonly wrong_reading_locks: ReadonlyArray<string>;
}
export declare const DEFAULT_STUDIO_TOOLS: ReadonlyArray<ToolDescriptor>;
export declare function compileNaturalLanguageRevision(request: OperatorRevisionRequest, context: RevisionContext): ChangeRequestProgram;
export declare function compileDirectManipulation(delta: DirectManipulationDelta, context: RevisionContext): ChangeRequestProgram;
