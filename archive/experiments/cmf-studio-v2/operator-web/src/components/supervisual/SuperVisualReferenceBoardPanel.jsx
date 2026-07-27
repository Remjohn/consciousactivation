export function SuperVisualReferenceBoardPanel({ displayPayload = {}, lineage = {} }) {
  const board = displayPayload.reference_board || displayPayload.asset_reference_board || null;
  const boardId = lineage.asset_reference_board_id || board?.reference_board_id;

  return (
    <section className="sv-card">
      <div className="sv-panel-header">
        <div>
          <p className="sv-eyebrow">Assets</p>
          <h3>Reference Board</h3>
        </div>
        {boardId ? <code>{boardId}</code> : <span className="sv-muted">not produced</span>}
      </div>

      {board ? (
        <pre className="sv-json-preview">{JSON.stringify(board, null, 2)}</pre>
      ) : (
        <p className="sv-muted">No backend reference board in the latest snapshot.</p>
      )}
    </section>
  );
}
