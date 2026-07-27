// Generated-consumer style contracts. Pydantic remains source of truth.
export type ProgramStatus =
  | 'draft'
  | 'compiled'
  | 'blocking_preview_ready'
  | 'revision_requested'
  | 'final_preview_ready'
  | 'approved_for_render'
  | 'rendering'
  | 'rendered'
  | 'approved_for_publish'
  | 'rejected';

export interface AssetRef {
  uri: string;
  sha256: string;
  mime_type?: string | null;
  size_bytes?: number | null;
}

export interface Timebase {
  ticks_per_second: number;
  audio_sample_rate: number;
  fps_numerator: number;
  fps_denominator: number;
  duration_ticks: number;
}

export interface PerformanceCue {
  cue_id: string;
  start_tick: number;
  end_tick?: number | null;
  action: string;
  clip_id?: string | null;
  state_id?: string | null;
  target_id?: string | null;
  value?: unknown;
  loop: boolean;
  mix_in_ticks: number;
  mix_out_ticks: number;
  semantic_target?: string | null;
}

export interface PerformanceTrack {
  track_id: string;
  priority: number;
  property_scope: string[];
  cues: PerformanceCue[];
}

export interface TwoDCharacterProgram {
  schema_version: string;
  program_id: string;
  status: ProgramStatus;
  timebase: Timebase;
  context_refs: Record<string, unknown>;
  character: Record<string, unknown>;
  asset_bundle: Record<string, unknown>;
  rig_manifest: Record<string, unknown>;
  performance_library: Record<string, unknown>;
  transcript_alignment: Record<string, unknown>;
  performance_tracks: PerformanceTrack[];
  motion_canvas_choreography: Record<string, unknown>;
  remotion_composition: Record<string, unknown>;
  ffmpeg_finishing: Record<string, unknown>;
  evaluation: Record<string, unknown>;
  operator_approval: Record<string, unknown>;
  receipt: Record<string, unknown>;
}
