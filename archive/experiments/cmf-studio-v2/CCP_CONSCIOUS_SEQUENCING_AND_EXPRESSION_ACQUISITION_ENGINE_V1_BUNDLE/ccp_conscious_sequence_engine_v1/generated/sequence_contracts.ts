// Generated consumer contract summary. Python/Pydantic remains authoritative.
export type IngredientClass =
  | 'human_expression'
  | 'research_evidence'
  | 'audience_reality'
  | 'visual'
  | 'brand_continuity';

export type ViewerState =
  | 'perceptual_entry'
  | 'relevant_open_question'
  | 'active_prediction'
  | 'truthful_payoff'
  | 'human_affinity'
  | 'expected_future_value';

export interface SequenceBeat {
  beat_id: string;
  order: number;
  viewer_state: ViewerState;
  semantic_role: string;
  ingredient_ids: string[];
  information_state: string;
  primitive_coalition: string[];
  composition_function: string;
  emotional_state?: string | null;
  duration_ms?: number | null;
  slide_index?: number | null;
  attention_order?: number | null;
}

export interface ContentSequenceProgram {
  schema_version: string;
  sequence_program_id: string;
  version: number;
  status: string;
  scope: 'single_asset' | 'asset_package' | 'series';
  brand_id: string;
  brand_context_version_id: string;
  doctrine_bundle_id: string;
  interview_brief_id: string;
  expression_session_id: string;
  ingredient_inventory_id: string;
  target_archetype: string;
  asset_derivative?: string | null;
  format_target: string;
  sequence_pattern_id: string;
  viewer_journey: {
    entry_state: string;
    target_exit_state: string;
    central_question: string;
    promised_payoff: string;
    future_value_key?: string | null;
  };
  loops: Array<{
    loop_id: string;
    question: string;
    opened_at_beat_id: string;
    closed_at_beat_id?: string | null;
    closure_required: boolean;
    policy: 'must_close' | 'discussion_open' | 'series_deferred';
  }>;
  beats: SequenceBeat[];
  operator_approval_status: 'not_reviewed' | 'needs_revision' | 'approved' | 'rejected';
}
