import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { TimelineProjection } from "./domain.js";
export interface VideoProgramElementInput {
    readonly element_id: string;
    readonly kind: string;
    readonly output_start_ms: number;
    readonly output_end_ms: number;
    readonly semantic_role: string;
    readonly sequence_role: string;
    readonly source_registration_ref?: ImmutableRef;
    readonly source_start_ms?: number;
    readonly source_end_ms?: number;
    readonly artifact_ref?: ArtifactRef;
}
export interface VideoProgramTrackInput {
    readonly track_id: string;
    readonly track_type: string;
    readonly role: string;
    readonly z_index: number;
    readonly elements: ReadonlyArray<VideoProgramElementInput>;
}
export interface VideoEditProgramInput {
    readonly program_id: string;
    readonly program_sha256: string;
    readonly canvas: {
        readonly width: number;
        readonly height: number;
        readonly fps_numerator: number;
        readonly fps_denominator: number;
        readonly duration_ms: number;
    };
    readonly tracks: ReadonlyArray<VideoProgramTrackInput>;
}
export declare function projectVideoEditProgram(program: VideoEditProgramInput): TimelineProjection;
