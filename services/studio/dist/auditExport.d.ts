import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { AuditExportManifest, ShipDecision } from "./domain.js";
export interface AuditExportInput {
    readonly campaign_ref: ImmutableRef;
    readonly source_refs: ReadonlyArray<ImmutableRef>;
    readonly semantic_refs: ReadonlyArray<ImmutableRef>;
    readonly run_refs: ReadonlyArray<ImmutableRef>;
    readonly artifact_refs: ReadonlyArray<ArtifactRef>;
    readonly evaluation_refs: ReadonlyArray<ImmutableRef>;
    readonly command_refs: ReadonlyArray<ImmutableRef>;
    readonly receipt_refs: ReadonlyArray<ImmutableRef>;
    readonly human_resolution_refs: ReadonlyArray<ImmutableRef>;
    readonly ship_decision: ShipDecision | null;
    readonly replay_instructions: ReadonlyArray<string>;
}
export declare function buildAuditExportManifest(input: AuditExportInput): AuditExportManifest;
export declare function writeAuditExport(path: string, manifest: AuditExportManifest): void;
