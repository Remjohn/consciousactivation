import { deterministicId, uniqueSorted } from "./canonical.js";
import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type { TimelineItemProjection, TimelineProjection, TimelineTrackProjection } from "./domain.js";
import { StudioValidationError, requireSafeInteger, validateImmutableRef } from "./validators.js";

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

function msToFrame(ms: number, numerator: number, denominator: number): number {
  return Math.round((ms * numerator) / (1000 * denominator));
}

export function projectVideoEditProgram(program: VideoEditProgramInput): TimelineProjection {
  validateImmutableRef({ object_id: program.program_id, version: "1.0.0", sha256: program.program_sha256 }, "video_edit_program_ref");
  requireSafeInteger(program.canvas.width, "canvas.width", 1);
  requireSafeInteger(program.canvas.height, "canvas.height", 1);
  requireSafeInteger(program.canvas.fps_numerator, "fps_numerator", 1);
  requireSafeInteger(program.canvas.fps_denominator, "fps_denominator", 1);
  requireSafeInteger(program.canvas.duration_ms, "duration_ms", 1);
  if (!program.tracks.some((track) => track.role === "PRIMARY_A_ROLL_SPINE")) {
    throw new StudioValidationError("PRIMARY_A_ROLL_SPINE_REQUIRED", "timeline projection requires the canonical talking-head spine");
  }
  const itemIds = new Set<string>();
  const items: TimelineItemProjection[] = [];
  const tracks: TimelineTrackProjection[] = [];
  for (const track of [...program.tracks].sort((a, b) => a.z_index - b.z_index || a.track_id.localeCompare(b.track_id))) {
    const ids: string[] = [];
    for (const element of [...track.elements].sort((a, b) => a.output_start_ms - b.output_start_ms || a.element_id.localeCompare(b.element_id))) {
      if (itemIds.has(element.element_id)) throw new StudioValidationError("DUPLICATE_TIMELINE_ITEM", `duplicate timeline item ${element.element_id}`);
      if (element.output_end_ms <= element.output_start_ms) throw new StudioValidationError("INVALID_TIMELINE_RANGE", `invalid range for ${element.element_id}`);
      itemIds.add(element.element_id);
      ids.push(element.element_id);
      const operations = track.role === "PRIMARY_A_ROLL_SPINE"
        ? ["TRIM_SEGMENT", "REORDER_ITEM"]
        : element.kind === "TEXT"
          ? ["MOVE_BBOX", "RESIZE_BBOX", "EDIT_TEXT", "SET_PARAMETER"]
          : ["MOVE_BBOX", "RESIZE_BBOX", "SET_PARAMETER"];
      items.push({
        item_id: element.element_id,
        track_id: track.track_id,
        kind: element.kind,
        role: element.semantic_role,
        start_frame: msToFrame(element.output_start_ms, program.canvas.fps_numerator, program.canvas.fps_denominator),
        end_frame: msToFrame(element.output_end_ms, program.canvas.fps_numerator, program.canvas.fps_denominator),
        source_start_ms: element.source_start_ms ?? null,
        source_end_ms: element.source_end_ms ?? null,
        source_ref: element.source_registration_ref ?? null,
        artifact_ref: element.artifact_ref ?? null,
        editable_operations: operations,
      });
    }
    tracks.push({ track_id: track.track_id, track_type: track.track_type, role: track.role, z_index: track.z_index, item_ids: uniqueSorted(ids) });
  }
  const ref: ImmutableRef = { object_id: program.program_id, version: "1.0.0", sha256: program.program_sha256 };
  const payload = { video_edit_program_ref: ref, width: program.canvas.width, height: program.canvas.height, fps_numerator: program.canvas.fps_numerator, fps_denominator: program.canvas.fps_denominator, tracks, items };
  return {
    projection_id: deterministicId("timeline-projection", payload),
    video_edit_program_ref: ref,
    state: "READ_ONLY_CANONICAL_PROGRAM_PROJECTION",
    width: program.canvas.width,
    height: program.canvas.height,
    fps_numerator: program.canvas.fps_numerator,
    fps_denominator: program.canvas.fps_denominator,
    duration_frames: msToFrame(program.canvas.duration_ms, program.canvas.fps_numerator, program.canvas.fps_denominator),
    tracks,
    items,
  };
}
