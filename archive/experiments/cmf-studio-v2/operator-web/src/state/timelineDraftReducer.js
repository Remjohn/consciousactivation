export const initialTimelineDraftState = {
  playheadFrame: 300,
  zoom: 1,
  selectedSegmentId: null,
  activeDraft: null,
  lastReceipt: null,
};

export function timelineDraftReducer(state, action) {
  switch (action.type) {
    case "set_playhead":
      return { ...state, playheadFrame: clampFrame(action.frame, action.durationFrames) };
    case "nudge_playhead":
      return { ...state, playheadFrame: clampFrame(state.playheadFrame + action.delta, action.durationFrames) };
    case "set_zoom":
      return { ...state, zoom: Math.max(0.65, Math.min(3, action.zoom)) };
    case "select_segment":
      return { ...state, selectedSegmentId: action.segmentId };
    case "create_draft":
      return { ...state, activeDraft: action.draft, lastReceipt: null };
    case "cancel_draft":
      return { ...state, activeDraft: null };
    case "mark_submitted":
      return { ...state, activeDraft: null, lastReceipt: action.receipt };
    default:
      return state;
  }
}

function clampFrame(frame, durationFrames) {
  return Math.max(0, Math.min(durationFrames || 0, frame));
}

export function buildTimelineEditDraft({ state, segment, editType, payload = {} }) {
  return {
    schema_version: "cmf.timeline_edit_draft.v1",
    draft_id: `draft-${segment.segment_id}-${editType}`,
    program_id: state.program_id,
    target_segment_id: segment.segment_id,
    edit_type: editType,
    proposed_time_range: segment.time_range,
    payload,
    expected_object_version: state.object_version,
    blocker_codes: segment.blocker_codes || [],
  };
}

export function buildTimelineEditCommand({ state, draft }) {
  return {
    schema_version: "cmf.timeline_edit_command.v1",
    command_id: `cmd-${Date.now()}`,
    draft_id: draft.draft_id,
    program_id: state.program_id,
    brand_workspace_id: state.brand_workspace_id,
    guest_id: state.guest_id,
    target_segment_id: draft.target_segment_id,
    edit_type: draft.edit_type,
    expected_object_version: draft.expected_object_version,
    expected_renderer_props_hash: state.renderer_props_hash,
    expected_scope_ref: `${state.brand_workspace_id}:${state.guest_id}`,
    payload: draft.payload,
    submitted_by_operator_id: "operator-demo",
  };
}

