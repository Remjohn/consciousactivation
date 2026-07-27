import { useTimelineWorkbench } from "./TimelineWorkbenchProvider.jsx";

export function TimelineCommandDrawer() {
  const { workbenchState, draftState, submitDraft, dispatch, rerenderProxy, exportOtio, onStartRender } = useTimelineWorkbench();
  if (!workbenchState) return null;

  return (
    <section className="timeline-command-drawer" aria-label="Timeline command drawer">
      <div>
        <span>Command Bus Draft</span>
        <strong>{draftState.activeDraft ? draftState.activeDraft.edit_type : "No active draft"}</strong>
      </div>
      {draftState.activeDraft ? (
        <>
          <pre>{JSON.stringify(draftState.activeDraft, null, 2)}</pre>
          <div className="drawer-actions">
            <button type="button" onClick={() => dispatch({ type: "cancel_draft" })}>Cancel draft</button>
            <button type="button" onClick={submitDraft}>Submit command</button>
          </div>
        </>
      ) : (
        <p>Select a segment, then create a draft from the inspector. The browser never mutates the canonical edit program directly.</p>
      )}
      {draftState.lastReceipt && (
        <div className="receipt-callout">
          <span>Last receipt</span>
          <strong>{draftState.lastReceipt.receipt_id}</strong>
          <small>{workbenchState.object_version}</small>
        </div>
      )}
      <div className="drawer-actions">
        <button type="button" onClick={rerenderProxy}>Rerender proxy</button>
        <button type="button" onClick={exportOtio}>Export OTIO</button>
        <button type="button" onClick={onStartRender}>Start final render</button>
      </div>
    </section>
  );
}
