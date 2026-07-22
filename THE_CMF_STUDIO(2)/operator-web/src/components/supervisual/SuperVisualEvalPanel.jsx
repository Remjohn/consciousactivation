export function SuperVisualEvalPanel({ displayPayload = {}, lineage = {} }) {
  const evaluation = displayPayload.eval || displayPayload.evaluation || null;
  const evalId = lineage.evaluation_receipt_id || evaluation?.evaluation_receipt_id;

  return (
    <section className="sv-card">
      <div className="sv-panel-header">
        <div>
          <p className="sv-eyebrow">Quality Gates</p>
          <h3>Evaluation</h3>
        </div>
        {evalId ? <code>{evalId}</code> : <span className="sv-muted">not evaluated</span>}
      </div>

      {evaluation ? (
        <pre className="sv-json-preview">{JSON.stringify(evaluation, null, 2)}</pre>
      ) : (
        <p className="sv-muted">Run evaluation to produce approval gates.</p>
      )}
    </section>
  );
}
