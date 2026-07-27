import { createContext, useContext, useEffect, useMemo, useReducer, useState } from "react";
import {
  fetchVideoTimelineWorkbench,
  proposeTimelineEdit,
  requestOtioExport,
  requestProxyRerender,
  submitTimelineEditCommand,
  TIMELINE_FIXTURE_MODE,
} from "../../api/videoTimeline.js";
import {
  buildTimelineEditCommand,
  buildTimelineEditDraft,
  initialTimelineDraftState,
  timelineDraftReducer,
} from "../../state/timelineDraftReducer.js";

const TimelineWorkbenchContext = createContext(null);

export function TimelineWorkbenchProvider({ activeFormat, onCommandReceipt, onStartRender, children }) {
  const [workbenchState, setWorkbenchState] = useState(null);
  const [loadState, setLoadState] = useState("loading");
  const [error, setError] = useState(null);
  const [draftState, dispatch] = useReducer(timelineDraftReducer, initialTimelineDraftState);

  useEffect(() => {
    let alive = true;
    setLoadState("loading");
    fetchVideoTimelineWorkbench({ formatSlot: activeFormat })
      .then((state) => {
        if (!alive) return;
        setWorkbenchState(state);
        setLoadState("ready");
        dispatch({ type: "select_segment", segmentId: state.selected_segment_id });
      })
      .catch((timelineError) => {
        if (!alive) return;
        setError(timelineError);
        setLoadState("failed");
      });

    return () => {
      alive = false;
    };
  }, [activeFormat]);

  const selectedSegment = useMemo(() => {
    if (!workbenchState) return null;
    return workbenchState.lanes.flatMap((lane) => lane.segments).find((segment) => segment.segment_id === draftState.selectedSegmentId) || null;
  }, [draftState.selectedSegmentId, workbenchState]);

  const selectedLane = useMemo(() => {
    if (!workbenchState || !selectedSegment) return null;
    return workbenchState.lanes.find((lane) => lane.lane_id === selectedSegment.lane_id) || null;
  }, [selectedSegment, workbenchState]);

  const setPlayhead = (frame) => dispatch({ type: "set_playhead", frame, durationFrames: workbenchState?.duration_frames || 0 });
  const nudgePlayhead = (delta) => dispatch({ type: "nudge_playhead", delta, durationFrames: workbenchState?.duration_frames || 0 });
  const setZoom = (zoom) => dispatch({ type: "set_zoom", zoom });
  const selectSegment = (segmentId) => dispatch({ type: "select_segment", segmentId });

  async function createDraft(editType, payload = {}) {
    if (!workbenchState || !selectedSegment) return;
    const draft = buildTimelineEditDraft({ state: workbenchState, segment: selectedSegment, editType, payload });
    const proposed = await proposeTimelineEdit({ draft });
    dispatch({ type: "create_draft", draft: proposed });
  }

  async function submitDraft() {
    if (!workbenchState || !draftState.activeDraft) return;
    const command = buildTimelineEditCommand({ state: workbenchState, draft: draftState.activeDraft });
    const receipt = await submitTimelineEditCommand({ command });
    setWorkbenchState((current) => applyTimelineEdit(current, draftState.activeDraft, receipt));
    onCommandReceipt?.(
      {
        ...receipt,
        command_type: "submit_timeline_edit",
        edit_type: draftState.activeDraft.edit_type,
        payload: draftState.activeDraft.payload,
      },
      `${draftState.activeDraft.edit_type} submitted for ${draftState.activeDraft.target_segment_id}`,
    );
    dispatch({ type: "mark_submitted", receipt });
  }

  async function rerenderProxy() {
    if (!workbenchState) return;
    const receipt = await requestProxyRerender({
      programId: workbenchState.program_id,
      payload: { output_profile: "proxy_720p" },
    });
    setWorkbenchState((current) => ({
      ...current,
      playback_proxy_status: receipt.render_job_state?.job_status || receipt.status || "queued",
      proxy_render_ref: receipt.output_preview_url || receipt.output_uri || `proxy://cmf/${current.guest_id}/${receipt.receipt_id}.mp4`,
      output_preview_url: receipt.output_preview_url || receipt.output_uri || current.output_preview_url,
      last_render_job_state: receipt.render_job_state || current.last_render_job_state,
      last_render_qa: receipt.render_qa || current.last_render_qa,
      last_render_receipt: receipt,
      render_summaries: mergeProxyRenderSummary(current.render_summaries, receipt),
    }));
    onCommandReceipt?.({ ...receipt, command_type: "rerender_proxy", runtime_mode: "timeline-workbench" }, "Proxy rerender requested");
  }

  async function exportOtio() {
    if (!workbenchState) return;
    const receipt = await requestOtioExport({ programId: workbenchState.program_id });
    setWorkbenchState((current) => ({
      ...current,
      otio_manifest_ref: `otio://cmf/${current.guest_id}/${receipt.receipt_id}.otio`,
      last_otio_receipt: receipt,
    }));
    onCommandReceipt?.({ ...receipt, command_type: "export_otio", runtime_mode: "timeline-workbench" }, "OTIO coverage export requested");
  }

  const value = {
    workbenchState,
    loadState,
    error,
    fixtureMode: TIMELINE_FIXTURE_MODE || workbenchState?.source_mode === "fixture",
    draftState,
    selectedSegment,
    selectedLane,
    dispatch,
    setPlayhead,
    nudgePlayhead,
    setZoom,
    selectSegment,
    createDraft,
    submitDraft,
    rerenderProxy,
    exportOtio,
    onStartRender,
  };

  return <TimelineWorkbenchContext.Provider value={value}>{children}</TimelineWorkbenchContext.Provider>;
}

function applyTimelineEdit(current, draft, receipt) {
  if (!current) return current;
  const receiptRef = receipt.receipt_id || receipt.command_id || "timeline-receipt";
  const lanes = current.lanes.map((lane) => {
    if (!lane.segments.some((segment) => segment.segment_id === draft.target_segment_id)) return lane;

    if (draft.edit_type === "remove_segment") {
      return {
        ...lane,
        segments: lane.segments.filter((segment) => segment.segment_id !== draft.target_segment_id),
      };
    }

    return {
      ...lane,
      segments: lane.segments.map((segment) => {
        if (segment.segment_id !== draft.target_segment_id) return segment;
        if (draft.edit_type === "trim") {
          const nudge = Number(draft.payload?.nudge_frames || 12);
          const endFrame = Math.max(segment.time_range.start_frame + 12, segment.time_range.end_frame - nudge);
          return {
            ...segment,
            label: `${segment.label} (trimmed)`,
            time_range: frameRange(segment.time_range.start_frame, endFrame, current.fps),
            receipt_refs: [...segment.receipt_refs, receiptRef],
            note: "Trim command applied in the operator workbench.",
          };
        }
        if (draft.edit_type === "fix_quote_alignment") {
          return {
            ...segment,
            label: draft.payload?.replacement_label || "Aligned source quote",
            blocker_codes: [],
            receipt_refs: [...segment.receipt_refs, receiptRef],
            note: "Quote alignment repair command applied in the operator workbench.",
          };
        }
        return {
          ...segment,
          receipt_refs: [...segment.receipt_refs, receiptRef],
          note: `${draft.edit_type} requested from operator workbench.`,
        };
      }),
    };
  });

  return {
    ...current,
    lanes,
    object_version: `${current.object_version}+ui.${Date.now()}`,
    hard_blocker_codes: lanes.flatMap((lane) => lane.segments.flatMap((segment) => segment.blocker_codes || [])),
  };
}

function mergeProxyRenderSummary(renderSummaries = [], receipt) {
  const nextSummary = {
    render_summary_id: receipt.receipt_id || `render-summary-${Date.now()}`,
    render_type: "proxy",
    status: receipt.render_job_state?.job_status || receipt.status || "queued",
    output_uri: receipt.output_preview_url || receipt.output_uri || null,
    output_sha256: receipt.output_sha256 || receipt.render_job_state?.output_sha256 || null,
    fake_render: receipt.fake_render !== false,
    provider_calls_executed: Boolean(receipt.provider_calls_executed),
    remotion_called: Boolean(receipt.remotion_called),
    ffmpeg_called: Boolean(receipt.ffmpeg_called),
  };
  return [nextSummary, ...renderSummaries.filter((summary) => summary.render_type !== "proxy")];
}

function frameRange(start, end, fps) {
  return {
    start_frame: start,
    end_frame: end,
    start_ms: Math.round((start / fps) * 1000),
    end_ms: Math.round((end / fps) * 1000),
  };
}

export function useTimelineWorkbench() {
  const value = useContext(TimelineWorkbenchContext);
  if (!value) {
    throw new Error("useTimelineWorkbench must be used inside TimelineWorkbenchProvider");
  }
  return value;
}
